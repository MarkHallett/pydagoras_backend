# dup_nodes_dag

#from pydagoras import dag_dot
from pydagoras.dag_dot import DAG_dot, calc

class DupNodesDAG(DAG_dot): # implementation
    __shared_state = {}

    def __init__(self):
        self.filename = 'dup_nodes_dag'
        super().__init__(self.filename)

        # internal nodes
        self.i2 = self.makeNode(label='add',calc=self.calcRateB,tooltip='calc_B')
        self.i = self.makeNode(label='mutiply',calc=self.calcRateA,usedby=[self.i2], tooltip='calc_A')

        # input nodes
        self.a = self.makeNode(label='A',calc=None,usedby=[self.i], nodetype='in', tooltip='A')
        self.b = self.makeNode(label='B',calc=None,usedby=[self.i], nodetype='in', tooltip='B')
        self.d = self.makeNode(label='D',calc=None,usedby=[self.i], nodetype='in', display_name='D_1', tooltip='D')
        self.d2 = self.makeNode(label='D',calc=None,usedby=[self.i2], nodetype='in', display_name='D_2', tooltip='D')

    @calc
    #def calcRateA(self, node=None, tooltip='multiply'):
    def calcRateA(self, node):
        return self.a.get_value() * self.b.get_value() * self.d.get_value()

    @calc
    def calcRateB(self, node):
        return self.i.get_value() + self.d.get_value()

 
if __name__ == '__main__':
    print('OK #######################################')
    my_dag = DupNodesDAG()

    # Set input values
    my_dag.set_input('A', 10)
    my_dag.set_input('B', 20)
    my_dag.set_input('D', 5)
        
    print(f'Output: {my_dag.o.get_value()}')  # Should print Output: 250

    my_dag.ppValues()
    my_dag.pp()

    print(my_dag.G.to_string())  # Print the graph representation  
