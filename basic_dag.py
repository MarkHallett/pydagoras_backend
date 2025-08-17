# basic_dag.py

from pydagoras.dag_dot import DAG_dot, calc

class BasicDAG(DAG_dot): 

    def __init__(self):
        self.filename = 'basic_dag'
        super().__init__(self.filename)

        # internal nodes
        self.add = self.makeNode(label='add',calc=self.calc_add, tooltip='add')
        self.mult = self.makeNode(label='multiply',calc=self.calc_multiply,usedby=[self.add], tooltip='mult')
        self.x10 = self.makeNode(label='x10',calc=self.calc_x10,usedby=[self.add], tooltip='x10')

        # input nodes
        self.a = self.makeNode(label='A',calc=None,usedby=[self.mult], nodetype='in', tooltip='source A')
        self.b = self.makeNode(label='B',calc=None,usedby=[self.mult], nodetype='in', tooltip='source B')
        self.c = self.makeNode(label='C',calc=None,usedby=[self.x10], nodetype='in', tooltip='source C')

    @calc
    def calc_multiply(self, node=None):
        print('in calc_multiply')
        return self.a.get_value() * self.b.get_value()

    @calc
    def calc_add(self, node=None):
        print('in calc_add')
        return self.mult.get_value() + self.x10.get_value()

    @calc
    def calc_x10(self, node=None):
        print('in calc_x10')
        return self.c.get_value() *  10


if __name__ == '__main__':
    print('OK #######################################')
    my_dag = BasicDAG()

    # Set input values
    my_dag.set_input('A', 10)
    my_dag.set_input('B', 20)
    my_dag.set_input('C', 5)

    print(f'Output: {my_dag.o.get_value()}')  # Should print Output: 1005

    my_dag.ppValues()  # Print all node values
    my_dag.pp()
    print(my_dag.G.to_string())  # Print the graph representation  
