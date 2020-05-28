#!/usr/bin/env python

"""Specifies methods to handle the DB containing all found minimal DFAs.

- to methods concerned with the DB, a sqlite3 connection has to be passed
- table 'MinimalDFAs' of the given DB is used to store the DFAs

ensure_validity
    Ensures existence of 'MinimalDFAs'.
    
fetch
    Fetches all DFAs matching the search parameters k, n, f, dmin, dmax.
    
save
    Saves a DFA in the database.
    
_encode_dfa
    Encodes a DFA into a string representation.
    
_decode_dfa
    Decodes a DFA from the string representation defined by _encode_dfa.
"""

import sqlite3

from dfa import DFA


__all__ = ['ensure_validity', 'fetch', 'save']


def ensure_validity(dbConn):
    """Ensures that a table 'MinimalDFAs' with the correct columns exists."""
    
    with dbConn:
        dbConn.execute('''
            CREATE TABLE IF NOT EXISTS MinimalDFAs 
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                
                dfa TEXT, 
                
                k INT, 
                n INT, 
                f INT, 
                
                depth  INT, 
                planar INT
            )'''
        )


def fetch(dbConn, k, n, f, dmin, dmax):
    """Fetches all DFAs matching the parameters.
    
    - assumes, that table MinimalDFAs with correct columns exists in dbConn
    - resulting DFAs habe dfa.depth and dfa.planar set
    """
    
    query = '''
        SELECT dfa, depth, planar FROM MinimalDFAs WHERE 
            k = ? AND
            n = ? AND
            f = ? AND
            depth >= ? AND depth <= ?
    '''
    qTuple = (k, n, f, dmin, dmax)
            
    dfaList = []
            
    for encodedDFA, depth, planar in dbConn.execute(query, qTuple):
    
        dfa = _decode_dfa(encodedDFA)
        dfa.depth  = depth
        dfa.planar = planar
        dfaList.append(dfa)
            
    return dfaList
            
    
def save(dbConn, dfa):
    """Saves a DFA.
    
    - assumes, that table MinimalDFAs with correct columns exists in dbConn
    - requires dfa.depth and dfa.planar to be set
    """

    assert dfa.depth  != None, 'dfa.depth  is required to be set'
    assert dfa.planar != None, 'dfa.planar is required to be set'
    
    dbTuple = (_encode_dfa(dfa), dfa.k, dfa.n, dfa.f, dfa.depth, dfa.planar)

    with dbConn:
        dbConn.execute('''INSERT INTO MinimalDFAs VALUES (NULL,?,?,?,?,?,?)''', dbTuple)
    
    
# -----------------------------------------------------------


def _encode_dfa(dfa):
    """Encodes a DFA in a string representation.
    
    - assumes that all alphabet symbols and states are characters
    - counterpart to _decode_dfa
    """
    
    A = ','.join(dfa.alphabet)
    Q = ','.join(dfa.states)
    d = ','.join(('{}.{}.{}'.format(q1, c, q2)
                              for ((q1, c),q2) in dfa.transitions))
    F = ','.join(dfa.final)
    
    return ';'.join((A, Q, d, dfa.start, F))
    
    
def _decode_dfa(encodedDFA):
    """Decodes a DFA from a string representation.
    
    - assumes that all alphabet symbols and states are characters
    - counterpart to _encode_dfa
    """

    encodedElements = encodedDFA.split(';')
    
    A = encodedElements[0].split(',')
    if '' in A:
        A.remove('')
    
    Q = encodedElements[1].split(',')
    if '' in Q:
        Q.remove('')
    
    d = encodedElements[2].split(',')
    if '' in d:
        d.remove('')
    d = [t.split('.')  for t         in d]
    d = [((q1, c), q2) for (q1,c,q2) in d]
    
    s = encodedElements[3]
    
    F = encodedElements[4].split(',')
    if '' in F:
        F.remove('')
    
    return DFA(A, Q, d, s, F, len(A), len(Q), len(F))
