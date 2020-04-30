from DFA 	                 import DFA
from minimize_dfa            import *
from isomorphy_test_min_dfas import contains_isomorph_dfa
from planarity_test_dfa      import planarity_test_dfa

import DB_MinimalDFAs as db1

import random
import sqlite3


def build_random_minimal_dfa(alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth, planar, workingDir):

    dbConn = sqlite3.connect(workingDir / 'dfa.db')

    db1.ensureValidity(dbConn)

    matchingUsedDFAs = db1.fetchMatchingDFAs(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth, planar)

    A = [ chr(i) for i in range(ord('a'), ord('a')+alphabetSize) ]
    Q = [ str(i) for i in range(numberOfStates) ]

    while True:

        # generate random dfa with correct alphabetSize, numberOfStates, numberOfAcceptingStates

        testDFA = DFA(A, Q, [], '0', random.sample(Q, numberOfAcceptingStates), alphabetSize, numberOfStates, numberOfAcceptingStates)

        for q in testDFA.states:
            for sigma in testDFA.alphabet:
                testDFA.transitions.append(random.choice([((q,sigma),p) for p in testDFA.states]))

        # test dfa on properties and check if it was used already

        if has_unreachable_states(testDFA):
            continue

        if not has_duplicate_states(testDFA): # has_duplicate_states sets testDFA.minmarkDepth
            continue

        if not (minMinmarkDepth <= testDFA.minmarkDepth <= maxMinmarkDepth):
            continue

        if planar and not planarity_test_dfa(testDFA): # planarity_test_dfa sets testDFA.isPlanar
            continue

        if contains_isomorph_dfa(testDFA, matchingUsedDFAs):
            continue

        db1.saveNewDFA(dbConn, testDFA) # db1.saveNewDFA needs testDFA.minmarkDepth and testDFA.isPlanar to be set
        dbConn.close()

        return testDFA


if __name__ == "__main__":

    # alphabetSize, numberOfStates, numberOfAcceptingStates, minMinmarkDepth, maxMinmarkDepth, planar
    print(build_random_minimal_dfa(3, 6, 3, 2, 3, True))
