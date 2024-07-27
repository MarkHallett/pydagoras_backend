# long_calc_dag.py

import time
import logging
import dag_dot

logger = logging.getLogger()


class MyDAG2(dag_dot.DAG): # implementation
    '''my dag'''
    __shared_state = {}

    def __init__(self,filename):
        self.__dict__ = self.__shared_state

        super(MyDAG2, self).__init__(filename)
        if hasattr(self,'o'):
            return

        # output node
        self.o = self.makeNode(label='Out',calc=None,usedby = [],    nodetype='out')

        # internal nodes
        self.bb = self.makeNode(label='calc_B',calc=self.calcRateB,usedby=[self.o], nodetype='internal')
        self.i = self.makeNode(label='calc_A',calc=self.calcRateA,usedby=[self.bb], nodetype='internal')
        self.cc = self.makeNode(label='10s',calc=self.calcRateC,usedby=[self.bb], nodetype='internal')

        # input nodes
        self.a = self.makeNode(label='A',calc=None,usedby=[self.i], nodetype='in')
        self.b = self.makeNode(label='B',calc=None,usedby=[self.i], nodetype='in')
        self.c = self.makeNode(label='C',calc=None,usedby=[self.cc], nodetype='in')

        #self.dot_pp()


    @dag_dot.calc
    def calcRateA(self, node=None):
        return self.a.value * self.b.value

    @dag_dot.calc
    def calcRateB(self, node=None):
        return self.i.value * self.c.value

    @dag_dot.calc
    def calcRateC(self, node=None):
        print('WAIT !!!!')
        time.sleep(5)
        return self.c.value *  10
 
