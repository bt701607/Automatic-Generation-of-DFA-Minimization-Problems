class DFA(object):
	
    def __init__(self, alphabet=['a','b','c'], states=[], transition_function=[], start_state=None, accepting_states=[]):

        self.__state_counter = 0

        self.alphabet    = alphabet
        self.states      = states
        self.transitions = transition_function
        self.start       = start_state
        self.accepting   = accepting_states
        
        
    def __str__(self):
        
        string = "(\n"
        string += "\t" + str(self.alphabet) + ",\n"
        string += "\t" + str(self.states) + ",\n"
        string += "\t[\n"

        for transition in self.transitions:
            string += "\t\t" + str(transition) + ",\n"
            
        string += "\t],\n"
        string += "\t" + str(self.start) + ",\n"
        string += "\t" + str(self.accepting) + "\n"
        string += ")\n"

        return string


    def add_state(self, start=False, accepting=False):

        if start and self.start != None:
            raise ValueError("Start state already set.")

        newState = self.__next_state()
        
        self.states.append(newState)

        if start:
            self.start = newState

        if accepting:
            self.accepting.append(newState)

        return newState


    def add_transition(self, state1, symbol, state2):

        if state1 not in self.states:
            raise ValueError("State 1 does not exist.")

        if state2 not in self.states:
            raise ValueError("State 2 does not exist.")

        newTransition = (state1, symbol), state2

        if newTransition in self.transitions:
            raise ValueError("Transition exists already.")

        self.transitions.append(newTransition)

        return newTransition


    def remove_state(self, state_to_remove):

        if state_to_remove not in self.states:
            raise ValueError("State to remove does not exist.")

        self.states.remove(state_to_remove)

        def remainsValid(t):
            ((q1,s),q2) = t
            return state_to_remove not in (q1,q2)
            
        self.transitions = set(filter(remainsValid, self.transitions))

        if self.start == state_to_remove:
            self.start = None
            
        if state_to_remove in self.accepting:
            self.accepting.remove(state_to_remove)


    def remove_transition(self, transition_to_remove):

        if transition_to_remove not in self.transitions:
            raise ValueError("Transition to remove does not exist.")

        self.transitions.remove(transition_to_remove)


    def __next_state(self):

        while self.__state_counter in self.states or str(self.__state_counter) in self.states:
            self.__state_counter += 1

        return self.__state_counter
