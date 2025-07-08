# basic_dag.py

from pydagoras import dag_dot

class BasicDAG(dag_dot.DAG): # implementation
    __shared_state = {}

    def __init__(self,filename):
        self.__dict__ = self.__shared_state

        super(BasicDAG, self).__init__(filename)
        if hasattr(self,'o'):
            return

        # output node
        self.o = self.makeNode(label='Out',calc=None,usedby = [],    nodetype='out')

        # internal nodes
        self.add = self.makeNode(label='add',calc=self.calc_add,usedby=[self.o], nodetype='internal', tooltip='add')
        self.mult = self.makeNode(label='multiply',calc=self.calc_multiply,usedby=[self.add], nodetype='internal', tooltip='mult')
        self.x10 = self.makeNode(label='x10',calc=self.calc_x10,usedby=[self.add], nodetype='internal', tooltip='x10')

        # input nodes
        self.a = self.makeNode(label='A',calc=None,usedby=[self.mult], nodetype='in', tooltip='source A')
        self.b = self.makeNode(label='B',calc=None,usedby=[self.mult], nodetype='in', tooltip='source B')
        self.c = self.makeNode(label='C',calc=None,usedby=[self.x10], nodetype='in', tooltip='source C')

    @dag_dot.calc
    def calc_multiply(self, node=None):
        return self.a.value * self.b.value

    @dag_dot.calc
    def calc_add(self, node=None):
        return self.mult.value + self.x10.value

    @dag_dot.calc
    def calc_x10(self, node=None):
        return self.c.value *  10
 
