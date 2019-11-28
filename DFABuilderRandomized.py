from DFA 	      import DFA
from minimize_dfa import minimize_dfa

import random


def build_random_minimal_dfa(alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth):
    
    A = [ chr(i) for i in range(ord('a'), ord('a')+alphabetSize) ]
    Q = [ str(i) for i in range(numberOfStates) ]
    
    is_good = False
    
    minDFA = None
    
    while not is_good:
        
        dfa = DFA(A, Q, [], '0', random.sample(Q, numberOfAcceptingStates))
        
        for q in dfa.states:
            for sigma in dfa.alphabet:
                dfa.transitions.append(random.choice([((q,sigma),p) for p in dfa.states]))
                
        minDFA, minDFAminmarkDepth = minimize_dfa(dfa)
                
        if len(minDFA.states) == numberOfStates and minMinmarkDepth <= minDFAminmarkDepth <= maxMinmarkDepth:
            is_good = True
            
    return minDFA
            
    
if __name__ == "__main__":
    
    print(build_random_minimal_dfa(6, 2, 2, 3, 2))
