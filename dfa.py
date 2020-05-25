"""
module: dfa.py
author: Gregor Soennichsen


"""


def letters(start, number):

    return list(chr(c) for c in range(ord(start), ord(start) + number))


class DFA(object):
    
    # states and alphabet-symbols must be chars.
    def __init__(self,
        alphabet, states, transitionFunction, startState, acceptingStates,
        k=None, n=None, f=None, depth=None, planar=None,
        eqClasses=None, unrStates=None):

        self.__stateCounter = 0

        self.alphabet    = alphabet
        self.states      = states
        self.transitions = transitionFunction
        self.start       = startState
        self.accepting   = acceptingStates
        
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
            self.f = len(acceptingStates)
        
        
    def __str__(self):
        
        string = '(\n'
        string += '\t' + str(self.alphabet) + ',\n'
        string += '\t' + str(self.states) + ',\n'
        string += '\t[\n'

        for transition in self.transitions:
            string += '\t\t' + str(transition) + ',\n'
            
        string += '\t],\n'
        string += '\t' + str(self.start) + ',\n'
        string += '\t' + str(self.accepting) + '\n'
        string += ')\n'

        return string
