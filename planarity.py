"""
module: planarity.py
author: Gregor Soennichsen


"""

import pygraph

import log

from dfa import DFA


# sets dfa.planar
def planarity_test(dfa):

    graph = pygraph.UndirectedGraph()
    
    bijection = {}
    
    for q in dfa.states:
        bijection[q] = graph.new_node()
        
    for ((q1,c),q2) in dfa.transitions:
        graph.new_edge(bijection[q1], bijection[q2])
        
    try:
        dfa.planar = pygraph.is_planar(graph)
    except IndexError:
        log.failed()
        print('Error: Planarity test failed on the following DFA:')
        print(dfa, '\n')
        raise
        
    return dfa.planar


if __name__ == '__main__':

    dfa = DFA(
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
    
    print(planarity_test(dfa))
