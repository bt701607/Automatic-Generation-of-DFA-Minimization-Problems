from DFA 	                 import DFA
from minimize_dfa            import *
from isomorphy_test_min_dfas import contains_isomorph_dfa
from planarity_test_dfa      import planarity_test_dfa

import DB_MinimalDFAs         as db1
import DB_EnumerationProgress as db2

from clean import clean_code_dir_keep_results

import sqlite3
import random



def build_next_minimal_dfa(alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth, planar):

    dbConn = sqlite3.connect('dfa.db')

    db1.ensureValidity(dbConn)
    db2.ensureValidity(dbConn)

    matchingUsedDFAs = db1.fetchMatchingDFAs(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth, planar)

    enumProgress = db2.fetchEnumerationProgress(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates)

    urs = ds = wmmd = np = him  = 0

    testDFA = None

    while True:

        # generate next dfa with correct alphabetSize, numberOfStates, numberOfAcceptingStates

        if enumProgress.finished:
            print("Enum.progress finished.")
            testDFA = None
            break

        testDFA = enumProgress.nextDFA()

        # test dfa on properties and check if it was used already

        if has_unreachable_states(testDFA):
            urs += 1
            continue

        if not has_duplicate_states(testDFA): # has_duplicate_states sets testDFA.minmarkDepth
            ds += 1
            continue

        if not (minMinmarkDepth <= testDFA.minmarkDepth <= maxMinmarkDepth):
            wmmd += 1
            continue

        if planar and not planarity_test_dfa(testDFA): # planarity_test_dfa sets testDFA.isPlanar
            np += 1
            continue

        if contains_isomorph_dfa(testDFA, matchingUsedDFAs):
            him += 1
            continue

        db1.saveNewDFA(dbConn, testDFA) # db1.saveNewDFA needs testDFA.minmarkDepth and testDFA.isPlanar to be set
        break

    print(enumProgress)
    print("unreach. states/dupl. states/wrong mmDep./not planar/has isom. = {} | {} | {} | {} | {}\n".format(urs, ds, wmmd, np, him))

    db2.updateEnumerationProgress(dbConn, enumProgress)
    dbConn.close()

    return testDFA



if __name__ == "__main__":

    # alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth, planar
    dfa = build_next_minimal_dfa(2, 6, 2, 2, 3, True)

    print(dfa)

    #clean_code_dir_keep_results()
