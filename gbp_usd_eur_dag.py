# gbp_usd_eur_dag.py 

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
        self.a = self.makeNode(label='gbp-usd',calc=None,usedby=[self.i], nodetype='in', tooltip='source 1')
        self.b = self.makeNode(label='usd-eur',calc=None,usedby=[self.i], nodetype='in', tooltip='source 2')
        self.c = self.makeNode(label='eur-gbp',calc=None,usedby=[self.bb], nodetype='in', tooltip='source 3')

    
    @calc
    def calcRateA(self, node=None):
        return self.a.get_value() * self.b.get_value()

    @calc
    def calcRateB(self, node=None):
        if isinstance(self.i.get_value(), str):
            self.i.pp()
            raise Exception(f'{self.i.node_id}, value {self.i.get_value()} is string, should be numeric')
        return self.i.get_value() * self.c.get_value()

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

    print(f'Output: {my_dag.o.get_value()}')  # Should print Output: 1000

    my_dag.ppValues()
    my_dag.pp()
    
    print(my_dag.G.to_string())  # Print the graph representation 
