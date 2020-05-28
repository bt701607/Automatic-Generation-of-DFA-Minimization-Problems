"""
module: dfa_build_rand.py
author: Gregor Soennichsen


"""

import random
import sqlite3

import db_dfa

from dfa          import DFA, characters
from minimization import has_unr_states, has_dupl_states
from isomorphy    import isomorphy_test
from planarity    import planarity_test


def rand_min_dfa(k, n, f, dmin, dmax, planar, outDir):

    dbConn = sqlite3.connect(outDir / 'dfa.db')

    db_dfa.ensure_validity(dbConn)

    matchingUsedDFAs = db_dfa.fetch(dbConn, k, n, f, dmin, dmax)

    A = characters('a', k)
    Q = characters('0', n)

    while True:

        # generate random dfa with correct k, n, f

        testDFA = DFA(A, Q, [], '0', random.sample(Q,f), k, n, f)

        for q in testDFA.states:
            for sigma in testDFA.alphabet:
                p = random.choice(testDFA.states)
                testDFA.transitions.append(((q,sigma),p))

        # test dfa on properties and check if it was used already

        if has_unr_states(testDFA):
            continue

        if not has_dupl_states(testDFA): # sets testDFA.depth
            continue

        if not (dmin <= testDFA.depth <= dmax):
            continue

        if planar:
            try:
                if not planarity_test(testDFA): # sets testDFA.planar
                    continue
            except PygraphIndexErrorBug:
                log.failed()
                log.pygraph_bug('building')
                continue

        if any(isomorphy_test(testDFA, dfa) for dfa in matchingUsedDFAs):
            continue

        db_dfa.save(dbConn, testDFA) # needs testDFA.depth and testDFA.planar to be set
        dbConn.close()

        return testDFA


if __name__ == '__main__':

    # k, n, f, dmin, dmax, planar
    print(rand_min_dfa(3, 6, 3, 2, 3, True))
