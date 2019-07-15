from DFA import DFA
from DFAManipulationInterface import *

import random


class DFAExtender(DFAManipulationInterface):

    def __init__(self, accepting=[], lonely=[], ingoing_only=[], outgoing_only=[], connected=[], unused_symbols={}, dfa=None, equiv_classes=None):
        
        DFAManipulationInterface.__init__(self, accepting=accepting, lonely=lonely, ingoing_only=ingoing_only, outgoing_only=outgoing_only, connected=connected, unused_symbols=unused_symbols, dfa=dfa)

        if equiv_classes == None:
            self._equiv_classes = [[state] for state in dfa.states]
        else:
            self._equiv_classes = equiv_classes


    def lonely(self, number=1):
        # Adds 'number' states that have no transitions at all.

        for i in range(number):
            
            newState = self._new_state()

            self._lonely.append(newState)

        return self


    def ingoing_only(self, number=1):
        """
        Adds 'number' non accepting states that have ingoing transitions (at least one) only.

        Transition end points are chosen by a custom sample of existing states
        having outgoing transitions.
        """

        for i in range(number):
            
            newState = self._new_state(is_accepting = False)

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


    def duplicate(self, number=1):

        for i in range(number):

            state1 = random.choice(tuple(q for q in self._dfa.states if len(tuple( t for t in self._dfa.transitions if t[0][1] == q )) >= 2)) # self._connected
            state2 = self._new_state(is_accepting = state1 in self._dfa.accepting)

            for equivClass in self._equiv_classes:
                if state1 in equivClass:
                    equivClass.append(state2)

            # split ingoing transitions upon state1, state2

            ingoingTransitions  = [ t for t in self._dfa.transitions if t[0][1] == state1 ]

            if len(ingoingTransitions) < 2:
                print("len(ingoingTransitions) < 2")
                break

            ingoingTransitions1 = random.sample(ingoingTransitions, len(ingoingTransitions) // 2)

            for t in ingoingTransitions:
                if t not in ingoingTransitions1:
                    (q1,q2),c = t
                    self._dfa.transitions.append(((q1,state2),c))
                    self._dfa.transitions.remove(t)

            # split outgoing transitions if possible

            outgoingTransitions = [ t for t in self._dfa.transitions if t[0][0] == state1 ]

            for t in outgoingTransitions:

                (q1,q2),c = t

                q2EquivClass = self._equiv_class_to_state(q2)

                if q2EquivClass == None:
                    print(q2, self._equiv_classes)

                if len(q2EquivClass) >= 2:

                    stateEquivToQ2 = next(q for q in q2EquivClass if q != q2)

                    self._dfa.transitions.append(((state2,stateEquivToQ2),c))

                else:

                    self._dfa.transitions.append(((state2,q2),c))

        return self


    def _new_state(self, is_start=False, is_accepting=(random.randint(0,1) == 1)):
        """
        Helper method for creating new states.
        A new state has a 50% chance of being accepting.
        """
            
        newState = self._dfa.add_state(is_start, is_accepting)
                
        if is_accepting:
            self._accepting.append(newState)

        self._unused_symbols[newState] = list(self._dfa.alphabet)

        return newState


    def _equiv_class_to_state(self, state):

        for equivClass in self._equiv_classes:
            if state in equivClass:
                return equivClass

