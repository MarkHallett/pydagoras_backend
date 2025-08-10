# main.py

import datetime
import string
import logging

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from fastapi import FastAPI

import basic_dag
import dup_nodes_dag
import gbp_usd_eur_dag
 
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logging.basicConfig( format='%(asctime)s %(levelname)s %(filename)s %(message)s')
logger = logging.getLogger(__name__)

logger.info('STARTING')

app = FastAPI()
app.basic_dag = basic_dag.BasicDAG()
app.dup_nodes_dag = dup_nodes_dag.DupNodesDAG()
app.gbp_usd_eur_dag = gbp_usd_eur_dag.FxDAG()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allows all origins
        allow_credentials=True,
        allow_methods=["*"], # Allows all methods
        allow_headers=["*"], # Allows all headers
        )

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>DagOutputs</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

def divmod_excel(n):
    a, b = divmod(n, 26)
    if b == 0:
        return a - 1, b + 26
    return a, b

def to_excel(num):
    chars = []
    while num > 0:
        num, d = divmod_excel(num)
        chars.append(string.ascii_uppercase[d - 1])
    return ''.join(reversed(chars))


def convert_count_to_reference(count: int) -> str:
    """Convert a count to a reference string."""
    if isinstance(count, str):
        return count # hacky!!
    return to_excel(count +26)

class ConnectionManager:
    connection_reference_count = 0
    connections = []

    @classmethod
    def get_connections_reference_count(cls):
        """Get the current count of connections."""
        #cls.connection_reference_count += 1  
        return cls.connection_reference_count    
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        ConnectionManager.connection_reference_count += 1
        time_of_connection = datetime.datetime.now().isoformat(' ', 'seconds')
        self.active_connections.append(websocket)
        self.connection_reference = convert_count_to_reference(ConnectionManager.connection_reference_count)
        logger.info(f'CONNECTED: {ConnectionManager.connection_reference_count=}, {self.connection_reference=}, {time_of_connection=}')

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f'DISCONNECTED: {ConnectionManager.connection_reference_count=}, {self.connection_reference=}')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        #print('broadcast message')
        #print(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @classmethod
    def get_connections(cls):
        rtn = []
        for value in client_connections.values():
            rtn.append(value)
        return rtn[::-1]

manager = ConnectionManager()
client_connections = {}
patches = []


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/connections")
async def get():
    logger.info(f'get connections, {len(client_connections)=}')
    return ConnectionManager.get_connections()

@app.get("/patches")
async def get():
    return patches[::-1]

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"JOINS Client {client_id=}")

    updater_id = ConnectionManager.get_connections_reference_count()
    updater_id = convert_count_to_reference(updater_id)

    client_connections[client_id] = { 'number': ConnectionManager.get_connections_reference_count(),
                                'updater_id': updater_id,
                                'client_id': client_id,
                                'connect_time': datetime.datetime.now().isoformat(' ', 'seconds'),
                                'disconnect_time': 'Active'
                                }    
    msg_basic = app.basic_dag.G.to_string()
    msg_dup_nodes = app.dup_nodes_dag.G.to_string()
    msg_gbp_usd_eur = app.gbp_usd_eur_dag.G.to_string()
    
    await manager.send_personal_message(f"Prime new connection", websocket)
    await manager.send_personal_message(f'BasicDAG:{msg_basic}', websocket)
    await manager.send_personal_message(f'DupNodes:{msg_dup_nodes}', websocket)
    await manager.send_personal_message(f'FX:{msg_gbp_usd_eur}',websocket)

    try:
        while True:
            now = datetime.datetime.now()
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat?") #
        client_connections[client_id]['disconnect_time'] = datetime.datetime.now().isoformat(' ', 'seconds')


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.patch("/items/{item_id}")
async def update_item(item_id:str, value:float, client_id: int=0):
    time_of_update = datetime.datetime.now().isoformat(' ', 'seconds')
    await manager.broadcast(f'INPUT {time_of_update} {client_id=} {item_id=} {value=}')

    updater_id = client_connections.get(client_id, {}).get('updater_id', 'unknown')
    updater_id = convert_count_to_reference(updater_id)
        
    patches.append({'update_number': len(patches) +1,
                    'input': item_id, 
                    'value':value, 
                    'time_of_update': time_of_update, 
                    #'client_id': 'client_id',
                    'updater_id': updater_id,
                    #'updater_id': client_connections[client_id]['updater_id'],                    
                    #'updater_id': 'AA',
                    'connection_time':'connection_time', 
                    }) 


    # for each dag, apply the value to the node if applicable
    for dag, dag_name in zip([ app.gbp_usd_eur_dag, app.basic_dag, app.dup_nodes_dag ], ['FX', 'BasicDAG','DupNodes'] ):

        dag_update = False
        for node in dag.input_nodes:
            if item_id == node.node_id:
                logger.info(f'Update {dag.label} {node.display_name=} {value=}')
                dag.set_input(item_id, value)
                dag_update = True

        if dag_update:
            msg = dag.G.to_string().replace(":", "")  # front end renderer cant handle a :
            await manager.broadcast(f'{dag_name}:{msg}')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)

