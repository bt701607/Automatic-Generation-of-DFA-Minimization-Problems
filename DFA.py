class DFA(object):
	
    def __init__(self, alphabet=['a','b','c'], states=[], transition_function=[], start_state=None, accepting_states=[]):

        self.__state_counter = 0

        self.alphabet    = alphabet
        self.states      = states
        self.transitions = transition_function
        self.start       = start_state
        self.accepting   = accepting_states


    def add_state(self, start=False, accepting=False):

        if start and self.start != None:
            raise ValueError("Start state already set.")

        newState = self.__state_counter

        self.__state_counter += 1

        self.states.append(newState)

        if start:
            self.start = newState

        if accepting:
            self.accepting.append(newState)

        return newState


    def add_transition(self, state1, state2, symbol):

        if state1 not in self.states:
            raise ValueError("State 1 does not exist.")

        if state2 not in self.states:
            raise ValueError("State 2 does not exist.")

        newTransition = (state1, state2), symbol

        if newTransition in self.transitions:
            raise ValueError("Transition exists already.")

        self.transitions.append(newTransition)

        return newTransition


    def remove_state(self, state_to_remove):

        if state_to_remove not in self.states:
            raise ValueError("State to remove does not exist.")

        self.states.remove(state_to_remove)

        remainsValid = lambda states,c: state_to_remove not in states
        self.transitions = set(filter(remainsValid, self.transitions))

        if self.start == state_to_remove:
            self.start = None


    def remove_transition(self, transition_to_remove):

        if transition_to_remove not in self.transitions:
            raise ValueError("Transition to remove does not exist.")

        self.transitions.remove(transition_to_remove)
