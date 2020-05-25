"""
module: dfa_build_enum.py
author: Gregor Soennichsen


"""

import pathlib
import sqlite3
import random

import db_dfa
import db_enum

from dfa          import DFA
from minimization import has_unr_states, has_dupl_states
from isomorphy    import contains_isomorph_dfa
from planarity    import planarity_test


def next_min_dfa(k, n, f, dmin, dmax, planar, outDir):

    dbConn = sqlite3.connect(outDir / 'dfa.db')

    db_dfa.ensure_validity(dbConn)
    db_enum.ensure_validity(dbConn)

    matchingUsedDFAs = db_dfa.fetch(dbConn, k, n, f, dmin, dmax)

    enumState = db_enum.fetch(dbConn, k, n, f)

    testDFA = None

    while True:

        # generate next dfa with correct k, n, f

        if enumState.finished:
            testDFA = None
            break

        testDFA = enumState.next()

        # test dfa on properties and check if it was used already

        if has_unr_states(testDFA):
            continue

        if not has_dupl_states(testDFA): # sets testDFA.depth
            continue

        if not (dmin <= testDFA.depth <= dmax):
            continue

        if planar and not planarity_test(testDFA): # sets testDFA.planar
            continue

        if contains_isomorph_dfa(testDFA, matchingUsedDFAs):
            continue

        db_dfa.save(dbConn, testDFA) # needs testDFA.depth and testDFA.planar to be set
        break

    db_enum.update(dbConn, enumState)
    dbConn.close()

    return testDFA



if __name__ == '__main__':

    # k, n, f, dmin, dmax, planar, outDir
    dfa = next_min_dfa(2, 6, 2, 2, 3, True, pathlib.Path.cwd())

    print(dfa)
