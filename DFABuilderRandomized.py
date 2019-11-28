from DFA 	            import DFA
from minimize_dfa       import minimize_dfa

from isomorphy_test_min_dfas import contains_isomorph_dfa
from planarity_test_dfa      import planarity_test_dfa

from pdf_from_dfa       import pdf_from_dfa
from clean              import clean_code_dir_keep_results

import DB_MinimalDFAs as db1


import random
import sqlite3


def build_random_minimal_dfa(alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth):

    dbConn = sqlite3.connect('dfa.db')
    
    db1.ensureValidity(dbConn)
    
    matchingUsedDFAs = db1.fetchMatchingDFAs(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth)
    
    A = [ chr(i) for i in range(ord('a'), ord('a')+alphabetSize) ]
    Q = [ str(i) for i in range(numberOfStates) ]
    
    while True:
    
        # generate random minimal dfa
        
        dfa = DFA(A, Q, [], '0', random.sample(Q, numberOfAcceptingStates), alphabetSize, numberOfStates, numberOfAcceptingStates)
        
        for q in dfa.states:
            for sigma in dfa.alphabet:
                dfa.transitions.append(random.choice([((q,sigma),p) for p in dfa.states]))
                
        minDFA = minimize_dfa(dfa)
        
        # test minimal dfa on properties and check if it was used already
                
        if len(minDFA.states) != numberOfStates or not (minMinmarkDepth <= minDFA.minmarkDepth <= maxMinmarkDepth):
            continue
        
        if not planarity_test_dfa(minDFA):
            continue
        
        if contains_isomorph_dfa(minDFA, matchingUsedDFAs):
            continue
        
        db1.saveNewDFA(dbConn, minDFA)
        dbConn.close()
                
        return minDFA
            
    
if __name__ == "__main__":
    
    # alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth
    dfa = build_random_minimal_dfa(4, 8, 3, 3, 4)
    
    print(dfa)

    pdf_from_dfa(dfa, "_random")

    clean_code_dir_keep_results()
