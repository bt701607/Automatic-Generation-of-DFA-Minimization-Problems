from DFA import DFA

import pygraph


# sets dfa.isPlanar
def planarity_test_dfa(dfa):

    graph = pygraph.UndirectedGraph()
    
    bijection = {}
    
    for q in dfa.states:
        bijection[q] = graph.new_node()
        
    for ((q1,c),q2) in dfa.transitions:
        graph.new_edge(bijection[q1], bijection[q2])
        
    dfa.isPlanar = pygraph.is_planar(graph)
        
    return dfa.isPlanar


if __name__ == "__main__":

    test_dfa = DFA(
        ['a','b','c','d','e'],
        ['1','2','3','4','5'],
        [
            (('1','a'),'1'),
            (('1','b'),'2'),
            (('2','c'),'4'),
            (('5','d'),'1'),
            (('2','e'),'5')
        ],
        '1',
        ['4','5']
    )
    
    print(planarity_test_dfa(test_dfa))
