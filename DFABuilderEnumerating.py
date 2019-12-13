from DFA 	      import DFA
from minimize_dfa import *

from isomorphy_test_min_dfas import contains_isomorph_dfa
from planarity_test_dfa      import planarity_test_dfa

import DB_MinimalDFAs         as db1
import DB_EnumerationProgress as db2

from pdf_from_dfa       import pdf_from_dfa
from clean              import clean_code_dir_keep_results

import sqlite3
        
        
        
def build_next_minimal_dfa(alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth):

    dbConn = sqlite3.connect('dfa.db')
    
    db1.ensureValidity(dbConn)
    db2.ensureValidity(dbConn)
        
    # ---
    
    matchingUsedDFAs = db1.fetchMatchingDFAs(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth)
    
    enumProgress = db2.fetchEnumerationProgress(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates)
    
    urs = ds = wmmd = np = him  = 0
    
    minDFA = None
    
    while True:
    
        if enumProgress.finished:
            print("Enum.progress finished.")
            minDFA = None
            break
        
        minDFA = enumProgress.nextDFA()
        
        if has_unreachable_states(minDFA):
            urs += 1
            continue
        
        if not has_duplicate_states(minDFA): # has_duplicate_states sets minDFA.minmarkDepth
            ds += 1
            continue
            
        if not (minMinmarkDepth <= minDFA.minmarkDepth <= maxMinmarkDepth):
            wmmd += 1
            continue
        
        if not planarity_test_dfa(minDFA):
            np += 1
            continue
            
        if contains_isomorph_dfa(minDFA, matchingUsedDFAs):
            him += 1
            continue
            
        db1.saveNewDFA(dbConn, minDFA)
        break
        
    print(enumProgress)
    print("unreach. states/dupl. states/wrong mmDep./not planar/has isom. = {} | {} | {} | {} | {}\n".format(urs, ds, wmmd, np, him))
    
    db2.updateEnumerationProgress(dbConn, enumProgress)
    dbConn.close()
    
    return minDFA
        
        
            
if __name__ == "__main__":
    
    # alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth
    dfa = build_next_minimal_dfa(2, 6, 2, 2, 3)
    
    print(dfa)

    pdf_from_dfa(dfa, "_enumerated")

    #clean_code_dir_keep_results()
