# dag_dot

import time
import logging
import pygraphviz as pgv

logger = logging.getLogger()

class DAG(object): # functionality
    '''Base DAG'''

    def __init__(self, label):
        self.G=pgv.AGraph(directed=True, strict=True, rankdir='LR', label=label, labelloc="t")
        self.input_nodes=[]

    def makeNode(self,label,calc,usedby,nodetype, display_name=None):
        n = Node(label,calc,usedby,nodetype,display_name)
        if nodetype == 'in':
            self.input_nodes.append(n)
        self.defNode(n,usedby =usedby, nodetype=nodetype)
        return n

    def defNode(self,node,usedby,nodetype):
        doc = node.display_name
        if nodetype == 'in':
            self.G.add_node(doc, shape="square")
            for n in usedby:
                self.AddEdge(doc,n.display_name)
        elif nodetype == 'internal':
            for n in usedby:
                self.AddEdge(doc,n.display_name)
        elif nodetype == 'out':
            self.G.add_node(doc, color="white")


    def AddEdge(self,node1,node2):
        self.G.add_edge(node1,node2,label='Undefined', fontname="Courier")

    def update_node(self,node1,node2,value):
        print('UPDATE_NODE')
        color = 'green'
        fontcolor='blue'
        if value == '-':
            fontcolor='black'
        elif value in ( 0, 'e'):
            fontcolor='red'
            color='red'

        self.G.add_node(node1,color=color,fontcolor=fontcolor,URL=node1+'.html',tooltip=node1)
        self.G.add_edge(node1,node2, label=value,fontcolor=fontcolor,color=color, fontname="Courier")
        print('added node and edge')
        #self.dot_pp()

    def fade(self,node1, node2,value,color):
        print ('FADE')
        1/0
        fontcolor=color
        color = color
        self.G.add_node(node1,color=color,fontcolor=fontcolor,URL=node1+'.html',tooltip=node1)
        self.G.add_edge(node1,node2, label=value,fontcolor=fontcolor,color=color, fontname="Courier")
        self.dot_pp()
        print('fade')


    def set_input1(self,node_id,value):
        print(f'set_input1 {node_id=} {value=}')
        for node in self.input_nodes:
            if node.node_id == node_id:
                
                for usedby in node.usedby:
                    print(f' . UPDATE NODE used by...')
                    self.update_node(node.display_name,usedby.node_id, value=value)


    def set_input(self,node_id,value):
        print(f'set_input {node_id=} {value=}')
        for node in self.input_nodes:
            if node.node_id == node_id:
                
                for usedby in node.usedby:
                    self.update_node(node.display_name,usedby.node_id, value=value)
                    print(f' . UPDATE NODE used by...')

                print(f'.. SET node {node.node_id=} {node.display_name=} to {value=}')
                self.setValue(node,value)


    def setValue(self,n,v):
        if v == n.value:
            return

        # build the DAG
        n.value = v
        for u in n.usedby:
           if u.calc == None:
               continue
           new_value = None
           new_value = u.calc(node=n)
           try:
              #u.pp()
              new_value = u.calc(node=n)
           except Exception as e:
              print('Error in setValue')
              print (str(e))

           self.setValue(u,new_value)

           # if output print
        print ('SET VALUE used by', n.usedby[0].node_id)
        if n.usedby[0].usedby == []:
            #print '!! SET VALUE OF OUTPUT'
            msg = 'update dag_dot.py %s %s' %(n.usedby[0].node_id, n.value)
            logger.info (msg)


    def pp(self): # must be over ridden by a borg
        # use doc string on class
        print (self.__doc__)
        for k, v in self.__dict__ .items():
            if type(v) == type(Node()):
                print (k,)
                v.pp()

    def ppInputs(self):
        print (self.__doc__, ' Inputs')
        for n in self.input_nodes:
            n.pp()

    def ppOutputs(self):
        print (self.__doc__, ' Outputs')
        for k, v in self.__dict__ .items():
            if type(v) == type(Node()):
                if v.usedby == []:
                    print (k,)
                    print ('=', v.value, v.node_id)

def calc(f1):
        print('CALC')
        def f3(self,*args, **kwargs):
            node=kwargs['node']

            for u_node in node.usedby:
                for o_node in u_node.usedby:
                    self.update_node(u_node.node_id,o_node.node_id, value='-')

            try:
                rtn = f1(self,*args, **kwargs)
                print(f'RETURN {rtn=}')
            except Exception as e:
                print ('Error in %s: %s' %(u_node.node_id,str(e)))
                #rtn = str(e)
                rtn = 'e'

            for u_node in node.usedby:
                for o_node in u_node.usedby:
                    self.update_node(u_node.node_id,o_node.node_id, value=rtn)

            return rtn
        return f3


class Node(object):
    def __init__(self, node_id=None, calc=None,usedby=None, nodetype=None, display_name=None):
        self.calc = calc
        self.node_id = node_id
        self.usedby = usedby
        self.value = None
        self.nodetype = nodetype
        if display_name:
            self.display_name = display_name
        else:
            self.display_name = node_id

    def pp(self):
        if self.usedby:
            print ("= %s, %s, used by, %s" %( self.value , self.node_id, [n.doc for n in self.usedby]))
        #else:
        #    print "= %s, %s, 'output node', %s" %( self.value , self.doc,  self.calc.__doc__)
