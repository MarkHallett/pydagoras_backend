# short_calc_dag
# duplicate_nodes_dag

import logging
import dag_dot

logger = logging.getLogger()


class MyDAG3(dag_dot.DAG): # implementation
    '''my dag'''
    __shared_state = {}


    def __init__(self,filename):
        self.__dict__ = self.__shared_state

        super(MyDAG3, self).__init__(filename)
        if hasattr(self,'o'):
            return

        # output node
        self.o = self.makeNode(label='Out',calc=None,usedby = [],    nodetype='out')

        # internal nodes
        self.i2 = self.makeNode(label='calc_B',calc=self.calcRateB,usedby=[self.o], nodetype='internal')
        self.i = self.makeNode(label='calc_A',calc=self.calcRateA,usedby=[self.i2], nodetype='internal')

        # input nodes
        self.a = self.makeNode(label='A',calc=None,usedby=[self.i], nodetype='in')
        self.b = self.makeNode(label='B',calc=None,usedby=[self.i], nodetype='in')
        self.a2 = self.makeNode(label='A',calc=None,usedby=[self.i2], nodetype='in', display_name='A1')


    @dag_dot.calc
    def calcRateA(self, node=None):
        return self.a.value * self.b.value


    @dag_dot.calc
    def calcRateB(self, node=None):
        return self.i.value + self.a.value
 
