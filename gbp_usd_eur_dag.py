# gbp_usd_eur_dag.py 

import logging
from pydagoras import dag_dot

logger = logging.getLogger()


class MyDAG(dag_dot.DAG): # implementation
    '''my dag'''
    __shared_state = {} 

    def __init__(self,filename):
        self.__dict__ = self.__shared_state

        super(MyDAG, self).__init__(filename)
        if hasattr(self,'o'):
            return

        # output node
        self.o = self.makeNode(label='GBP/USD/EUR',calc=None,usedby = [],    nodetype='out')

        # internal nodes
        self.bb = self.makeNode(label='calc_B',calc=self.calcRateB,usedby=[self.o], nodetype='internal', tooltip='multiply')
        self.i = self.makeNode(label='calc_A',calc=self.calcRateA,usedby=[self.bb], nodetype='internal', tooltip='multiply')

        # input nodes
        self.a = self.makeNode(label='gbp-usd',calc=None,usedby=[self.i], nodetype='in', tooltip='source 1')
        self.b = self.makeNode(label='usd-eur',calc=None,usedby=[self.i], nodetype='in', tooltip='source 2')
        self.c = self.makeNode(label='eur-gbp',calc=None,usedby=[self.bb], nodetype='in', tooltip='source 3')

    @dag_dot.calc
    def calcRateA(self, node=None):
        return self.a.value * self.b.value

    @dag_dot.calc
    def calcRateB(self, node=None):
        return self.i.value * self.c.value

    # special cases
    def get_colors(self, value):
        if value in ( 0, 'e'):
            return 'red', 'red'
        return super().get_colors(value)


