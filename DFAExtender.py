from DFA  import DFA

from copy import deepcopy

import random


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


class DFAExtender():
    """
    Implements the 'Builder' design pattern for the 'DFA' class,
    such that 'sensible' task-DFAs can be created.

    Methods are provided to add states with varying transition modalities.

    Decisions upon start/accepting states and number of transitions are made by the class.

    Notes:
    - randomness is used to create different DFAs in different run-throughs
    - 'custom sample' shall refer in this context to the semantics defined by the 'custom_sample' method
    """

    def __init__(self, dfa):
        """
        Expects a minimal dfa as input.
        
        Initializes tracking lists for various categories of states
        and creates an DFA with a start state.
        """

        self._accepting = deepcopy(dfa.accepting)
        
        self._lonely         = []
        self._ingoing_only   = []
        self._outgoing_only  = []

        self._unused_symbols = {}
        
        if dfa == None:

            self._dfa = DFA()
            self._connected.append(self._new_state(is_start = True))

        else:

            self._dfa = deepcopy(dfa)
            
            for q in self._dfa.states:
                    
                self._unused_symbols[q] = []
                    
                for c in self._dfa.alphabet:
                
                    ocurrences = len(tuple(filter(lambda t: t[0][0] == q and t[0][1] == c, self._dfa.transitions)))
                    
                    if ocurrences == 0:
                        self._unused_symbols[q].append(c)

        self._equiv_classes = [[state] for state in self._dfa.states]
        
        
    # -------------------------------------------------------------------
        

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
        
        
    # -------------------------------------------------------------------


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

            availableEndPoints = tuple(
                q
                for q in self._dfa.states
                    if self._unused_symbols[q] != [] and q not in self._ingoing_only+self._lonely
            )

            statesToConnect = custom_sample(availableEndPoints, len(availableEndPoints))
            
            for state in statesToConnect:
                self._dfa.transitions.append(((state, self._next_free_symbol(state)), newState))

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

            availableEndPoints = tuple(
                q
                for q in self._dfa.states
                    if q not in self._outgoing_only+self._lonely
            )

            statesToConnect = custom_sample(availableEndPoints, len(self._dfa.alphabet))
                
            for state in statesToConnect:
                self._dfa.transitions.append(((newState, self._next_free_symbol(newState)), state))
                
            self._outgoing_only.append(newState)

        return self
        
        
    def make_complete(self):
        """
        Adds - if needed - a sink state which makes the automaton complete.
        All states which have not used symbols on outgoing transitions yet,
        will get an outgoing transition to this sink state.
        """
        
        # check if there are any missing transitions
        if sum(len(unused_symbols_of_state) for unused_symbols_of_state in self._unused_symbols.values()) == 0:
            return self
        
        newState = self._new_state(is_start=False, is_accepting=False)
        
        for state in self._dfa.states:
            for symbol in self._unused_symbols[state]:
                self._dfa.transitions.append(((state, symbol), newState))
            self._unused_symbols[state] = []

        self._ingoing_only.append(newState)
            
        return self


    def duplicate(self, number=1):

        for i in range(number):

            # make sure that the chosen state has enough ingoing transitions
            state1 = random.choice(tuple(q for q in self._dfa.states if len(tuple( t for t in self._dfa.transitions if t[1] == q )) >= 2))
            state2 = self._new_state(is_accepting = state1 in self._dfa.accepting)

            print("Duplicating %s by creating %s." % (state1,state2))

            for equivClass in self._equiv_classes:
                if state1 in equivClass:
                    equivClass.append(state2)

            # split ingoing transitions upon state1, state2

            ingoingTransitions  = [ t for t in self._dfa.transitions if t[1] == state1 ]

            if len(ingoingTransitions) < 2:
                print("len(ingoingTransitions) < 2")
                break

            ingoingTransitions1 = random.sample(ingoingTransitions, len(ingoingTransitions) // 2)

            for t in ingoingTransitions:
                if t not in ingoingTransitions1:
                    (q1,c),q2 = t
                    self._dfa.transitions.append(((q1,c),state2))
                    self._dfa.transitions.remove(t)

            # split outgoing transitions if possible

            outgoingTransitions = [ t for t in self._dfa.transitions if t[0][0] == state1 ]

            for t in outgoingTransitions:

                (q1,c),q2 = t

                q2EquivClass = self._equiv_class_to_state(q2)

                if q2EquivClass == None:
                    print(q2, self._equiv_classes)

                if len(q2EquivClass) >= 2:

                    stateEquivToQ2 = next(q for q in q2EquivClass if q != q2)

                    self._dfa.transitions.append(((state2,c),stateEquivToQ2))
                    
                    self._unused_symbols[state2].remove(c)

                else:

                    self._dfa.transitions.append(((state2,c),q2))
                    
                    self._unused_symbols[state2].remove(c)

        return self

