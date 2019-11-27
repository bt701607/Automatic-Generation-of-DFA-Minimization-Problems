from DFA 	      import DFA
from minimize_dfa import *

from isomorphy_test_min_dfas import isomorphy_test_min_dfas

import DB_MinimalDFAs         as db1
import DB_EnumerationProgress as db2


import threading
import sqlite3


#DB_MUTEX = threading.Lock()

    
    
def propertiesMatch(properties, numberOfStates, minDepth, maxDepth, alphabetSize, numberOfAcceptingStates):

    return properties[0] == numberOfStates and minDepth <= properties[1] <= maxDepth and properties[2] == numberOfAcceptingStates and properties[3] == alphabetSize
        
        
        
def hasIsomorphMatchingDFA(testDFA, l):
    
    for dfa in l:

        if isomorphy_test_min_dfas(testDFA, dfa) == True:
    
            return True
            
    return False
        
        

# returns dfa, properties
def build_next_fitting_dfa(numberOfStates, minDepth, maxDepth, alphabetSize, numberOfAcceptingStates):

    conn = sqlite3.connect('dfa.db')
    
    db1.ensureValidity(conn)
    db2.ensureValidity(conn)
    
    # look whether our db of found minimal DFAs has a fitting, unused one
    
    #result = db1.findMatchingUnusedMinimalDFA(conn, numberOfStates, minDepth, maxDepth, alphabetSize, numberOfAcceptingStates)
    
    #if result != None:
        #conn.close()
        #return result

    # 
    
    enumProgress = db2.fetchEnumerationProgress(conn, numberOfStates, alphabetSize, numberOfAcceptingStates)
    
    matchingUsedDFAs = db1.fetchMatchingDFAs(conn, numberOfStates, minDepth, maxDepth, alphabetSize, numberOfAcceptingStates)
    
    # DEBUG
    iEnd = 10000
    i = 0
    
    while True:
    
        # DEBUG
        if i == iEnd:
            db2.updateEnumerationProgress(conn, enumProgress)
            print(i, enumProgress)
            conn.close()
            return None
            
    
        if enumProgress.finished:
            db2.updateEnumerationProgress(conn, enumProgress)
            conn.close()
            return None
        
        i += 1
        if not i % 10000:
            print(i/iEnd)
            
        enumProgress.increment()
        
        # ---
        
        reachDFA = delete_unreachable_states(enumProgress.dfa())
        
        if len(reachDFA.states) < numberOfStates:
            continue
        
        minDFA, min_mark_depth = delete_duplicate_states(reachDFA)
        
        minDFA = delete_useless_symbols(minDFA)
        
        
        minDFAproperties = (len(minDFA.states), min_mark_depth, len(minDFA.accepting), len(minDFA.alphabet))
        
        if propertiesMatch(minDFAproperties, numberOfStates, minDepth, maxDepth, alphabetSize, numberOfAcceptingStates):
            
            if not hasIsomorphMatchingDFA(minDFA, matchingUsedDFAs):
                
                    db2.updateEnumerationProgress(conn, enumProgress)
                    db1.saveNewDFA(conn, minDFA, minDFAproperties, used=True)
                    
                    conn.close()
                    
                    return minDFA
        
            
if __name__ == "__main__":

    print(build_next_fitting_dfa(7, 2, 3, 3, 2))
