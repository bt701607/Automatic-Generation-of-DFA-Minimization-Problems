#!/usr/bin/env python

"""Definitions to handle enumeration states and their preservation in a DB.

- to methods concerned with the DB, a sqlite3 connection has to be passed
- table 'EnumStates' of the given DB is used to store the enumeration states

ensure_validity
    Ensures existence of 'EnumStates'.

fetch
    Fetches/Creates the enumeration state matching the search parameters k, n, f.

update
    Writes a previously loaded enumeration state back into the DB.

_add_one
    Increments b-ary numbers represented by lists.

EnumState
    Defines enumeration states. Contains methods to get a states successor 
    and to gain the DFA represented by it.
"""

import sqlite3

from dfa import DFA, characters


__all__ = ['ensure_validity', 'fetch', 'update', 'EnumState']


def ensure_validity(dbConn):
    """Ensures that a table 'EnumStates' with the correct columns exists."""
    
    with dbConn:
        dbConn.execute('''
            CREATE TABLE IF NOT EXISTS EnumStates
            (
                k INT, 
                n INT, 
                f INT, 
                
                state_f     TEXT, 
                state_delta TEXT, 
                    
                finished INT
            )'''
        )
    
    
def fetch(dbConn, k, n, f):
    """Fetches/Creates the enumeration state matching the parameters.
    
    Assumes, that table EnumStates with correct columns exists in dbConn.
    If no corresponding enumeration state is found, then a new one is created.
    """

    query = '''
        SELECT state_f, state_delta, finished 
        FROM EnumStates 
        WHERE k = ? AND n = ? AND f = ?
    '''

    c = dbConn.cursor()
    c.execute(query, (k, n, f))
    dbResult = c.fetchone()
    
    if dbResult is None:
    
        enumState = EnumState(k, n, f)

        dbTuple = (
            k, n, f,
            ','.join(map(str, enumState.stateF)),
            ','.join(map(str, enumState.stateDelta)),
            0
        )
        
        with dbConn:
            dbConn.execute('''INSERT INTO EnumStates VALUES (?,?,?,?,?,?)''', dbTuple)
    
        return enumState
        
    else:
        
        stateF, stateDelta, finished = dbResult
        
        stateF     = [int(i) for i in stateF.split(',')]
        stateDelta = [int(i) for i in stateDelta.split(',')]
        finished   = bool(finished)
        
        return EnumState.from_existing(k, n, f, stateF, stateDelta, finished)
            
            
            
def update(dbConn, enumState):
    """Updates the enumeration state in the DB belonging to enumState.
    
    Assumes, that table EnumStates with correct columns exists in dbConn.
    Assumes that enumState was created via 'fetch'.
    """

    query = '''
        UPDATE EnumStates 
        SET state_f = ?, state_delta = ?, finished = ? 
        WHERE k = ? AND n = ? AND f = ?
    '''

    dbTuple = (
        ','.join(map(str, enumState.stateF)),
        ','.join(map(str, enumState.stateDelta)),
        int(enumState.finished),
        enumState.k,
        enumState.n,
        enumState.f
    )
    
    with dbConn:
        dbConn.execute(query, dbTuple)
    
    
# -----------------------------------------------------------


def _add_one(n, b):
    """Adds one to list n, which is interpreted as b-ary number.
    
    - assumes that n is ordered, such that the least significant digit 
      is at index 0
    - returns None, if n cannot be incremented (n == b-1 ... b-1)
    """
    i = 0
    while n[i] == b-1:
        n[i] = 0
        i += 1
        if i == len(n):
            return None
    n[i] += 1
    return n
    
    
class EnumState(object):
    """A state in a DFA enumeration. Provides method to get next state.
    
    A DFA enumeration in this project is characterized by k, n, f, denoting
    what kind of DFAs are produced during the enumeration.
    
    A DFA enumeration state is characterized by two fields stateDelta, stateF, 
    representing delta and F of the current DFA (see '_dfa'):
        
            If delta(i, j) = p then stateDelta[i * k + j] = q.
        
            If i in F, then stateF[i] = 1, else stateF[i] = 0.
    
    To get to the next DFA, these two fields are incremented as described in
    'next'.
    """

    def __init__(self, k, n, f):
        """Initializes an initial enumeration state.
        
        The stateF-field states that the first f states are final.
        The stateDelta-field states that all transition end in the first state.
        """
    
        assert n >= f, '''Number of states must be greater than number of 
                          final states.'''
    
        self.k = k
        self.n = n
        self.f = f
        
        self.deltaSize = n * k
        
        self.stateF     = [1 for i in range(f)] + [0 for i in range(n-f)]
        self.stateDelta = [0 for i in range(self.deltaSize)]
        
        self.finished = False
        
        
    @staticmethod
    def from_existing(k, n, f, stateF, stateDelta, finished):
        """Initializes a non-initial enumeration state."""
            
        enumState = EnumState(k, n, f)
        
        enumState.stateF     = stateF
        enumState.stateDelta = stateDelta
        enumState.finished   = finished
        
        return enumState
        
        
    def __str__(self):
        """Returns the given enumeration state in string representation."""
    
        return str((self.k, self.n, self.f, self.stateF, self.stateDelta, self.finished))
        
        
    def next(self):
        """Performs one enumeration step and returns the resulting DFA.
        
        Returns None and sets 'finished = True', if the enumeration is finished.
        """
        
        if self.finished:
            return None
        
        # get next transitions-configuration by incrementing stateDelta 
        # and return new DFA
        
        if _add_one(self.stateDelta, self.n) is not None:
            return self._dfa()
        
        # If all transitions given the current stateF were enumerated, 
        # increment stateF until it marks f states as final again.
        
        # If all valid F-configurations have been enumerated as well,
        # the enumeration is finished.
        
        while True:
        
            if _add_one(self.stateF, 2) is None:
                self.finished = True
                return None
                
            if self.stateF.count(1) == self.f:
                self.stateDelta = [0 for i in range(self.deltaSize)]
                return self._dfa()
                
        
    def _dfa(self):
        """Extracts the DFA from the given enumeration state."""
    
        A = characters('a', self.k)
        Q = characters('0', self.n)
        
        d = []
        
        for i in range(self.n):
            for j in range(self.k):
                
                state1 = chr(ord('0') + i                              )
                symbol = chr(ord('a') + j                              )
                state2 = chr(ord('0') + self.stateDelta[i * self.k + j])
                
                d.append(((state1, symbol), state2))
    
        F = []
        
        for i in range(self.n):
            if self.stateF[i]:
                F.append(chr(ord('0') + i))
    
        return DFA(A, Q, d, '0', F, self.k, self.n, self.f)
