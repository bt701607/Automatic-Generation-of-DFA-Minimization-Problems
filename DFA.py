class DFA(object):
    
    # states and alphabet-symbols must be chars.
    def __init__(self,
        alphabet, states, transition_function, start_state, accepting_states,
        alphabetSize=None, numberOfStates=None, numberOfAcceptingStates=None, minmarkDepth=None, isPlanar=None,
        eq_classes=None, unr_states=None):

        self.__state_counter = 0

        self.alphabet    = alphabet
        self.states      = states
        self.transitions = transition_function
        self.start       = start_state
        self.accepting   = accepting_states
        
        self.alphabetSize            = alphabetSize
        self.numberOfStates          = numberOfStates
        self.numberOfAcceptingStates = numberOfAcceptingStates
        
        self.minmarkDepth = minmarkDepth
        self.isPlanar     = isPlanar
        
        self.eqClasses = eq_classes
        self.unrStates = unr_states
        
        if alphabetSize == None:
            self.alphabetSize = len(alphabet)
            
        if numberOfStates == None:
            self.numberOfStates = len(states)
            
        if numberOfAcceptingStates == None:
            self.numberOfAcceptingStates = len(accepting_states)
        
        
    def __str__(self):
        
        string = "(\n"
        string += "\t" + str(self.alphabet) + ",\n"
        string += "\t" + str(self.states) + ",\n"
        string += "\t[\n"

        for transition in self.transitions:
            string += "\t\t" + str(transition) + ",\n"
            
        string += "\t],\n"
        string += "\t'" + str(self.start) + "',\n"
        string += "\t" + str(self.accepting) + "\n"
        string += ")\n"

        return string
