#!/usr/bin/env python

"""Specifies methods to build complete minimal DFAs with some properties.

This module uses the DB at 'outDir/_DB_LOC'. It is assumed, that this DB is
not altered, except by methods called in this module.

_valid_dfa
    Checks whether a given DFA fulfills various properties.

rand_min_dfa
    Tries to generate minimal DFAs matching some properties by randomization.

next_min_dfa
    Tries to generate minimal DFAs matching some properties by enumeration.
"""

import sqlite3
import random

import log

import db_dfa
import db_enum

from dfa          import DFA, characters
from minimization import has_unr_states, has_equiv_states
from isomorphy    import isomorphy_test
from planarity    import planarity_test, PygraphIndexErrorBug


__all__ = ['rand_min_dfa', 'next_min_dfa']


_DB_LOC = 'dfa.db'



def _valid_dfa(dfa, dmin, dmax, planar, usedDFAs):
    """Returns True iff 'dfa' fulfills all below listed properties.
    
    The checked properties are:
    - dfa is minimal
    - dfa minimization depth is in (dmin, dmax)
    - dfa is planar (if wished)
    - dfa has not the same language as any DFA in 'usedDFAs'
    
    Assumes non-planarity, if the IndexError bug in the pygraph library orcurs.
    Sets dfa.depth and (if planar=True) dfa.planar.
    """

    if has_unr_states(dfa):
        return False
        
    if has_equiv_states(dfa): # sets dfa.depth
        return False

    if not (dmin <= dfa.depth <= dmax):
        return False

    if planar:
        try:
            if not planarity_test(dfa): # sets dfa.planar
                return False
        except PygraphIndexErrorBug:
            log.failed()
            log.pygraph_bug('building')
            return False

    if any(isomorphy_test(dfa, usedDFA) for usedDFA in usedDFAs):
        return False
        
    return True


def rand_min_dfa(k, n, f, dmin, dmax, planar, outDir):
    """Tries to generate a random minimal DFA matching some properties.
    
    Uses the DB mentioned in the module description.
    
    - all DFAs generated here and by 'next_min_dfa' have different languages
    - ensures properties checked by _valid_dfa
    - matching DFAs are saved in the DB at table 'MinimalDFAs'
    """

    dbConn = sqlite3.connect(outDir / _DB_LOC)

    db_dfa.ensure_validity(dbConn)

    matchingUsedDFAs = db_dfa.fetch(dbConn, k, n, f, dmin, dmax)

    A = characters('a', k)
    Q = characters('0', n)

    while True:

        testDFA = DFA(A, Q, [], '0', random.sample(Q,f), k, n, f)

        for q in testDFA.states:
            for c in testDFA.alphabet:
                p = random.choice(testDFA.states)
                testDFA.transitions.append(((q, c), p))

        # _valid_dfa sets testDFA.depth and testDFA.planar
        if _valid_dfa(testDFA, dmin, dmax, planar, matchingUsedDFAs):

            # save needs testDFA.depth and testDFA.planar
            db_dfa.save(dbConn, testDFA)
            dbConn.close()

            return testDFA
        


def next_min_dfa(k, n, f, dmin, dmax, planar, outDir):
    """Tries to generate a minimal DFA matching some properties by enumeration.
    
    Uses the DB mentioned in the module description.
    
    - all DFAs generated here and by 'next_min_dfa' have different languages
    - ensures properties checked by _valid_dfa
    - matching DFAs are saved in the DB at table 'MinimalDFAs'
    
    Uses an enumeration state. This state is stored in the DB, if
    - a DFA has been found or 
    - the enumeration reached its end.
    
    If a state matching k, n, f is already saved in the DB, then from this 
    state on enumeration is continued.
    
    Returns None, if the enumeration is finished.
    """

    dbConn = sqlite3.connect(outDir / _DB_LOC)

    db_dfa.ensure_validity(dbConn)
    db_enum.ensure_validity(dbConn)

    matchingUsedDFAs = db_dfa.fetch(dbConn, k, n, f, dmin, dmax)

    enumState = db_enum.fetch(dbConn, k, n, f, dmin, dmax, planar)

    if enumState.finished:
        dbConn.close()
        return None

    while True:

        testDFA = enumState.next()

        if enumState.finished:
        
            db_enum.update(dbConn, enumState, dmin, dmax, planar)
            
            dbConn.close()
            return None

        # _valid_dfa sets testDFA.depth and testDFA.planar
        if _valid_dfa(testDFA, dmin, dmax, planar, matchingUsedDFAs):
            
            # save needs testDFA.depth and testDFA.planar
            db_dfa.save(dbConn, testDFA)
            db_enum.update(dbConn, enumState, dmin, dmax, planar)
            
            dbConn.close()
            return testDFA
