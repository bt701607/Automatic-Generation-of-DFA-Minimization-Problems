import random

from DFA import DFA


class DFAManipulationInterface(object):

    def __init__(self, accepting=[], lonely=[], ingoing_only=[], outgoing_only=[], connected=[], unused_symbols={}, dfa=None):
        """
        Initializes tracking lists for various categories of states
        and creates an DFA with a start state.
        """

        self._accepting = accepting

        self._lonely = lonely
        self._ingoing_only = ingoing_only
        self._outgoing_only = outgoing_only
        self._connected = connected

        self._unused_symbols = unused_symbols
        
        if dfa == None:

            self.dfa = DFA()
            self._connected.append(self._new_state(is_start = True))

        else:

            self._dfa = dfa
        

    def dfa(self):
        # Returns the so far constructed DFA.

        return self._dfa


    def _next_free_symbol(self, state):

        symbol = random.choice(self._unused_symbols[state])
        self._unused_symbols[state].remove(symbol)
        return symbol