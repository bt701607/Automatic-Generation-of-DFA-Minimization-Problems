#!/usr/bin/env python

"""DFA planarity tests."""

import pygraph

from dfa import DFA


__all__ = ['PygraphIndexErrorBug', 'planarity_test']


class PygraphIndexErrorBug(Exception):
    """Captures a bug in the pygraph library that raises an IndexError."""
    
    pass


def planarity_test(dfa):
    """Returns whether dfa can be embedded in a plane without crossing edges.
    
    - sets dfa.planar accordingly.
    - uses the pygraph library
    
    Raises PygraphIndexErrorBug if IndexError bug in the implementation of
    pygraph.is_planar occurs.
    """

    graph = pygraph.UndirectedGraph()
    
    bijection = {}
    
    for q in dfa.states:
        bijection[q] = graph.new_node()
        
    for ((q1,c),q2) in dfa.transitions:
        graph.new_edge(bijection[q1], bijection[q2])
        
    try:
        dfa.planar = pygraph.is_planar(graph)
    except IndexError:
        raise PygraphIndexErrorBug()
        
    return dfa.planar
