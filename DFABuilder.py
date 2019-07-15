from DFA import DFA
from DFAManipulationInterface import *

import random

from copy import deepcopy


class DFABuilder(DFAManipulationInterface):
    """
    Implements the 'Builder' design pattern for the 'DFA' class,
    such that 'sensible' DFAs can be created.

    Methods are provided to add states with varying transition modalities.

    Decisions upon start/accepting states and number of transitions are made by the class.

    Notes:
    - randomness is used to create different DFAs in different run-throughs
    - 'custom sample' shall refer in this context to the semantics defined by the 'custom_sample' method
    """

    def __init__(self, accepting=[], lonely=[], ingoing_only=[], outgoing_only=[], connected=[], unused_symbols={}, dfa=None):
        
        DFAManipulationInterface.__init__(self, accepting=accepting, lonely=lonely, ingoing_only=ingoing_only, outgoing_only=outgoing_only, connected=connected, unused_symbols=unused_symbols, dfa=dfa)


    def lonely(self, number=1):
        # Adds 'number' states that have no transitions at all.

        for i in range(number):
            
            newState = self._new_state()

            self._lonely.append(newState)

        return self


    def ingoing_only(self, number=1):
        """
        Adds 'number' states that have ingoing transitions (at least one) only.

        Transition end points are chosen by a custom sample of existing states
        having outgoing transitions.
        """

        for i in range(number):
            
            newState = self._new_state()

            availableEndPoints = list(
                s
                for s in self._outgoing_only + self._connected
                    if self._unused_symbols[s] != []
            )

            statesToConnect = custom_sample(availableEndPoints, len(availableEndPoints))
            
            for state in statesToConnect:
                self._dfa.add_transition(state, newState, self._next_free_symbol(state))

            self._ingoing_only.append(newState)

        return self


    def outgoing_only(self, number=1):
        """
        Adds 'number' states that have outgoing transitions (at least one) only.

        Transition end points are chosen by a custom sample of existing states
        having ingoing transitions.
        """

        for i in range(number):
            
            newState = self._new_state()

            statesToConnect = custom_sample(self._ingoing_only + self._connected, len(self._dfa.alphabet))
                
            for state in statesToConnect:
                self._dfa.add_transition(newState, state, self._next_free_symbol(newState))
                
            self._outgoing_only.append(newState)

        return self


    def connected(self, number=1):
        """
        Adds 'number' states that have ingoing and outgoing transitions (of each at least one).

        Transition end points are chosen by a custom sample of existing states having
        outgoing/ingoing transitions, if an ingoing/outgoing transition is created.
        """

        for i in range(number):
            
            newState = self._new_state()

            availableEndPoints = list(
                s
                for s in self._outgoing_only + self._connected
                    if self._unused_symbols[s] != []
            )

            statesToConnectIngoing = custom_sample(availableEndPoints, len(availableEndPoints))

            statesToConnectOutgoing = custom_sample(self._ingoing_only + self._connected, len(self._dfa.alphabet))
                
            for state in statesToConnectIngoing:
                self._dfa.add_transition(state, newState, self._next_free_symbol(state))
                    
            for state in statesToConnectOutgoing:
                self._dfa.add_transition(newState, state, self._next_free_symbol(newState))
                    
            self._connected.append(newState)

        return self


    def mix(self, lonely=0, ingoing_only=0, outgoing_only=0, connected=0):

        jobs = []
        for i in range(lonely):         jobs.append("L")
        for i in range(ingoing_only):   jobs.append("I")
        for i in range(outgoing_only):  jobs.append("O")
        for i in range(connected):      jobs.append("C")
        random.shuffle(jobs)

        execute_mapping = {
            "L" : self.lonely,
            "I" : self.ingoing_only,
            "O" : self.outgoing_only,
            "C" : self.connected
        }

        for job in jobs:
            execute_mapping[job]()

        return self


    def _new_state(self, is_start=False):
        """
        Helper method for creating new states.
        A new state has a 50% chance of being accepting.
        """
            
        is_accepting = random.randint(0,1) == 1
            
        newState = self._dfa.add_state(is_start, is_accepting)
                
        if is_accepting:
            self._accepting.append(newState)

        self._unused_symbols[newState] = list(self._dfa.alphabet)

        return newState

