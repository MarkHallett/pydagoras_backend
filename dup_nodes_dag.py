# dup_nodes_dag

from pydagoras import dag_dot

class DupNodesDAG(dag_dot.DAG): # implementation
    __shared_state = {}

    def __init__(self,filename):
        self.__dict__ = self.__shared_state

        super(DupNodesDAG, self).__init__(filename)
        if hasattr(self,'o'):
            return

        # output node
        self.o = self.makeNode(label='Out',calc=None,usedby = [],    nodetype='out')

        # internal nodes
        self.i2 = self.makeNode(label='calc_B',calc=self.calcRateB,usedby=[self.o], nodetype='internal', tooltip='add')
        self.i = self.makeNode(label='calc_A',calc=self.calcRateA,usedby=[self.i2], nodetype='internal', tooltip='multiply')

        # input nodes
        self.a = self.makeNode(label='A',calc=None,usedby=[self.i], nodetype='in', tooltip='A')
        self.b = self.makeNode(label='B',calc=None,usedby=[self.i], nodetype='in', tooltip='B')
        self.d = self.makeNode(label='D',calc=None,usedby=[self.i], nodetype='in', display_name='D1', tooltip='D')
        self.d2 = self.makeNode(label='D',calc=None,usedby=[self.i2], nodetype='in', display_name='D2', tooltip='D')

    @dag_dot.calc
    def calcRateA(self, node=None, tooltip='multiply'):
        return self.a.value * self.b.value * self.d.value

    @dag_dot.calc
    def calcRateB(self, node=None, tooltip='add'):
        return self.i.value + self.d.value

 
