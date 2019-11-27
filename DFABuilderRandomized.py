from DFA 	      import DFA
from minimize_dfa import minimize_dfa, minimization_mark_depth

import random


def build_random_minimal_dfa(numberOfStates, minDepth, maxDepth, alphabetSize, numberOfAcceptingStates):
    
    A = [ chr(i) for i in range(ord('a'), ord('a')+alphabetSize) ]
    Q = [ str(i) for i in range(numberOfStates) ]
    
    is_good = False
    
    while not is_good:
        
        dfa = DFA(A, Q, [], '0', random.sample(Q, numberOfAcceptingStates))
        
        for q in dfa.states:
            for sigma in dfa.alphabet:
                dfa.transitions.append(random.choice([((q,sigma),p) for p in dfa.states]))
                
        min_dfa = minimize_dfa(dfa)
        #print("----------------------------")
        #print(dfa)
        #print(min_dfa)
        #print("----------------------------")
                
        if len(minimize_dfa(dfa).states) == len(dfa.states) and minDepth <= minimization_mark_depth(dfa) <= maxDepth:
            is_good = True
            
    return dfa
            
    
if __name__ == "__main__":
    
    print(build_random_minimal_dfa(6, 2, 2, 3, 2))
