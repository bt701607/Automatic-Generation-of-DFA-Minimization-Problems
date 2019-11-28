from DFA 	      import DFA
from minimize_dfa import *

from isomorphy_test_min_dfas import contains_isomorph_dfa

import DB_MinimalDFAs         as db1
import DB_EnumerationProgress as db2

import sqlite3
        
        
        
def build_next_minimal_dfa(alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth):

    dbConn = sqlite3.connect('dfa.db')
    
    db1.ensureValidity(dbConn)
    db2.ensureValidity(dbConn)
        
    # ---
    
    matchingUsedDFAs = db1.fetchMatchingDFAs(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth)
    
    enumProgress = db2.fetchEnumerationProgress(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates)
    
    # DEBUG
    i = 0
    
    urs = ds = wmmd = him  = 0
    
    def log():
        print(i, enumProgress)
        print("unreach. states/dupl. states/wrong mmDep./has isom. = {} | {} | {} | {}\n".format(urs, ds, wmmd, him))
        
    def finishUp():
        db2.updateEnumerationProgress(dbConn, enumProgress)
        log()
        dbConn.close()
    
    try:
    
        while True:
        
            if enumProgress.finished:
                print("Enum.progress finished.")
                finishUp()
                return None
            
            i += 1
            
            if i % 300000 == 0:
                log()
                
            enumProgress.increment()
            
            # ---
            
            minDFA = enumProgress.dfa()
            
            if has_unreachable_states(minDFA):
                urs += 1
                continue
            
            result = has_duplicate_states(minDFA)
            
            if not result:
                ds += 1
                continue
                
            minDFA.minmarkDepth = result
                
            if not (minMinmarkDepth <= minDFA.minmarkDepth <= maxMinmarkDepth):
                wmmd += 1
                continue
            
            # ---
                
            if not contains_isomorph_dfa(minDFA, matchingUsedDFAs):
                
                db1.saveNewDFA(dbConn, minDFA)
                finishUp()
                return minDFA
                    
            else:
                
                him += 1
                        
    except KeyboardInterrupt:
        finishUp()
        exit()
        
        
            
if __name__ == "__main__":

    # alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth
    print(build_next_minimal_dfa(2, 5, 2, 2, 3))
