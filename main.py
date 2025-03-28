import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import gbp_usd_eur_dag
import long_calc_dag
import short_calc_dag
 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.D = gbp_usd_eur_dag.MyDAG('gbp_usd_eur')
app.D2 = long_calc_dag.MyDAG2('long_calc')
app.D3 = short_calc_dag.MyDAG3('duplicate_nodes')
app.D.set_input('eur-gbp',1)
app.D.set_input('usd-eur',10)
print('start ....')

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allows all origins
        allow_credentials=True,
        allow_methods=["*"], # Allows all methods
        allow_headers=["*"], # Allows all headers
        )

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

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


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print('broadcast message')
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    msg = app.D.G.to_string()
    msg2 = app.D2.G.to_string()
    msg3 = app.D3.G.to_string()
    
    await manager.broadcast(f'A:{msg}')
    await manager.broadcast(f'B:{msg2}')
    await manager.broadcast(f'C:{msg3}')

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        #await manager.broadcast(f"Client #{client_id} left the chat")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.patch("/items/{item_id}")
async def update_item(item_id:str, value:float):
    print(f'patch: {item_id=} {value=}')
    for dag, dag_name in zip([ app.D, app.D2, app.D3 ], ['A', 'B','C'] ):

        dag_update = False
        for node in dag.input_nodes:
            #print(f'{node.doc=}, {node.display_name=}')
            if item_id == node.node_id:
                #print('set input AAAAAAAA..................')
                #dag.set_input1(item_id, value)
                #msg = dag.G.to_string()
                #await manager.broadcast(f'{dag_name}:{msg}')
                #print('sent 1')
                #print('set input BBBBBB..................')
                dag.set_input(item_id, value)
                msg = dag.G.to_string()
                #await manager.broadcast(f'{dag_name}:{msg}')
                #print('sent 2')

                dag.set_input(item_id, value)
                
                dag_update = True

        if dag_update:
           msg = dag.G.to_string()
           await manager.broadcast(f'{dag_name}:{msg}')

           print('done broadcast')
           #print(msg)

    return {"item_name ?? out put ??" }



 # at last, the bottom of the file/module
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
