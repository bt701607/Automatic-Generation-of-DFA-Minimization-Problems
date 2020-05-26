#!/usr/bin/env python

"""Definitions to specify deterministic finite automatons (DFAs)."""


__all__ = ['characters', 'DFA']


def characters(c0, n):
    """Returns a list of n characters starting (inclusive) with c0."""

    return list(chr(c) for c in range(ord(c0), ord(c0) + n))


class DFA(object):
    
    def __init__(self, 
            alphabet, states, transitions, start, final,
            k=None, n=None, f=None, 
            depth=None, planar=None,
            eqClasses=None, unrStates=None):
        """Initializes a DFA object.
        
        The five mandatory parameters correspond to the mathematical definition
        of a DFA. The remaining arguments provide additional informations.
        
        k,n,f are computed from alphabet,states,final if not provided.
        
        States and alphabet symbols are preferably single characters.
        """

        self.__stateCounter = 0

        self.alphabet    = alphabet
        self.states      = states
        self.transitions = transitions
        self.start       = start
        self.final       = final
        
        self.k = k
        self.n = n
        self.f = f
        
        self.depth  = depth
        self.planar = planar
        
        self.eqClasses = eqClasses
        self.unrStates = unrStates
        
        if k is None:
            self.k = len(alphabet)
            
        if n is None:
            self.n = len(states)
            
        if f is None:
            self.f = len(final)
        
        
    def __str__(self):
        """Returns the given DFA in string representation."""
        
        string = '(\n'
        string += '\t' + str(self.alphabet) + ',\n'
        string += '\t' + str(self.states) + ',\n'
        string += '\t[\n'

        for transition in self.transitions:
            string += '\t\t' + str(transition) + ',\n'
            
        string += '\t],\n'
        string += '\t' + str(self.start) + ',\n'
        string += '\t' + str(self.final) + '\n'
        string += ')\n'

        return string
