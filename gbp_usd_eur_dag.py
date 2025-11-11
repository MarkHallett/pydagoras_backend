# gbp_usd_eur_dag.py 

import sys
print(sys.executable)

from pydagoras.dag_dot import DAG_dot, calc


class FxDAG(DAG_dot): 

    def __init__(self):
        self.filename = 'fx_dag'

        super().__init__(self.filename)
        if hasattr(self,'o'):
            return

        # internal nodes
        self.bb = self.makeNode(label='calc_B',calc=self.calcRateB, tooltip='multiply')
        self.i = self.makeNode(label='calc_A',calc=self.calcRateA,usedby=[self.bb], tooltip='multiply')

        # input nodes
        self.gbp_usd = self.makeNode(label='gbp-usd',calc=None,usedby=[self.i], nodetype='in', tooltip='source 1')
        self.usd_eur = self.makeNode(label='usd-eur',calc=None,usedby=[self.i], nodetype='in', tooltip='source 2')
        self.eur_gbpc = self.makeNode(label='eur-gbp',calc=None,usedby=[self.bb], nodetype='in', tooltip='source 3')

    
    @calc
    def calcRateA(self, node=None):
        gbp_usd = self.gbp_usd.get_value()
        usd_eur = self.usd_eur.get_value()
        if gbp_usd <= 0 or usd_eur <= 0:
            raise Exception( f'Input parameters must be positive {gbp_usd=} {usd_eur=}' )
        return gbp_usd * usd_eur

    @calc
    def calcRateB(self, node=None):
        i = self.i.get_value()
        eur_gbp = self.eur_gbp.get_value()
         
        if isinstance(i, str):
            self.i.pp()
            raise Exception(f'{self.i.node_id}, value {i} is string, should be numeric')

        if eur_gbp <= 0:
            raise Exception( f'Input parameters must be positive {eur_gbp=}' )

        return i * eur_gbp

    # special cases
    @classmethod
    def get_colors(cls, value):
        if value in ( 0, 'e'):
            return 'red', 'red'
        if value == '-':
            return 'black', 'black'
        if value <= 0:
            return 'red', 'red'
        return 'blue', 'green'


if __name__ == '__main__':
    print('OK #######################################')
    my_dag = FxDAG()

    # Set input values
    my_dag.set_input('gbp-usd', 10)
    my_dag.set_input('usd-eur', 20)
    my_dag.set_input('eur-gbp', 5)

    #print(f'Output: {my_dag.o.get_value()}')  # Should print Output: 1000

    #my_dag.ppValues()
    my_dag.pp()
    
    print(my_dag.G.to_string())  # Print the graph representation 
