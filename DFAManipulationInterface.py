from DFA import DFA

import random

from copy import deepcopy


def custom_sample(original_list, max_elements):
    """
    Returns a sublist with 1 to (max_elements+1) / 2 elements.

    Returns the empty list, if the empty list is passed.
    """

    if original_list == []:
        return []
    elif max_elements > len(original_list):
        return random.sample(original_list, random.randint(1, len(original_list)))
    else:
        return random.sample(original_list, random.randint(1, (max_elements + 1) // 2)) # (max_elements + 1) // 2


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

            self._dfa = DFA()
            self._connected.append(self._new_state(is_start = True))

        else:

            self._dfa = dfa
        

    def dfa(self):
        # Returns the so far constructed DFA.

        return deepcopy(self._dfa)


    def _next_free_symbol(self, state):
        """
        Returns a symbol of the so far constructed DFA,
        that is not labelled on an outgoing transition.
        """

        symbol = random.choice(self._unused_symbols[state])
        self._unused_symbols[state].remove(symbol)
        return symbol
