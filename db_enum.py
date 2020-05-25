"""
module: db_enum.py
author: Gregor Soennichsen


"""

import sqlite3

from dfa import DFA, letters


def ensure_validity(dbConn):
    
    with dbConn:
        dbConn.execute('''
            CREATE TABLE IF NOT EXISTS EnumState
            (
                k INT, 
                n INT, 
                f INT, 
                
                state_f     TEXT, 
                state_delta TEXT, 
                    
                finished INT
            )'''
        )
    
    
def clear(dbConn):
    
    with dbConn:
        dbConn.execute('''DROP TABLE IF EXISTS EnumState''')
    
    
# -----------------------------------------------------------
    
    
def __encode_ints(intList):

    resStr = ''
   
    for n in intList:
        resStr += str(n) + ','
        
    return resStr[:-1]
    
    
def fetch(dbConn, k, n, f):

    query = '''
        SELECT state_f, state_delta, finished 
        FROM EnumState 
        WHERE k = ? AND n = ? AND f = ?
    '''

    c = dbConn.cursor()
    c.execute(query, (k, n, f))
    dbResult = c.fetchone()
    
    if dbResult is None:
    
        enumState = EnumState(k, n, f)

        dbTuple = (
            k, n, f,
            __encode_ints(enumState.stateF),
            __encode_ints(enumState.stateDelta),
            0
        )
        
        with dbConn:
            dbConn.execute('''INSERT INTO EnumState VALUES (?,?,?,?,?,?)''', dbTuple)
    
        return enumState
        
    else:
        
        stateF, stateDelta, finished = dbResult
        
        stateF     = [int(i) for i in stateF.split(',')]
        stateDelta = [int(i) for i in stateDelta.split(',')]
        finished   = bool(finished)
        
        return EnumState.from_existing(k, n, f, stateF, stateDelta, finished)
            
            
            
def update(dbConn, enumState):

    query = '''
        UPDATE EnumState 
        SET state_f = ?, state_delta = ?, finished = ? 
        WHERE k = ? AND n = ? AND f = ?
    '''

    dbTuple = (
        __encode_ints(enumState.stateF),
        __encode_ints(enumState.stateDelta),
        int(enumState.finished),
        enumState.k,
        enumState.n,
        enumState.f
    )
    
    with dbConn:
        dbConn.execute(query, dbTuple)
    
    
# -----------------------------------------------------------
    
    
class EnumState(object):

    def __init__(self, k, n, f):
    
        if n < 1:
            raise Exception('Number of states must be greater than zero for a DFA.')
    
        self.k = k
        self.n = n
        self.f = f
        self.deltaSize = n * k
        
        self.stateF     = [1 for i in range(f)] + [0 for i in range(n-f)]
        self.stateDelta = [0 for i in range(self.deltaSize)]
        
        self.finished = False
        
        
    @staticmethod
    def from_existing(k, n, f, stateF, stateDelta, finished):
            
        enumState = EnumState(k, n, f)
        
        enumState.stateF     = stateF
        enumState.stateDelta = stateDelta
        enumState.finished   = finished
        
        return enumState
        
        
    def __str__(self):
    
        return str((self.k, self.n, self.f, self.stateF, self.stateDelta, self.finished))
        
        
    def next(self):

        def add_one(n, p):
            i = 0
            while n[i] == p-1:
                n[i] = 0
                i += 1
                if i == len(n):
                    return None
            n[i] += 1
            return n
        
        # ----
        
        if self.finished:
            return None
        
        # further iterate through transitions, if possible
        
        if add_one(self.stateDelta, self.n) is not None:
            return self.__dfa()
        
        # if transition's end reached, iterate accepting state permutations
        # and reset transition progress if stateF could be incremented
        
        while True:
        
            if add_one(self.stateF, 2) is None:
                self.finished = True
                return None
                
            if self.stateF.count(1) == self.f:
                self.stateDelta = [0 for i in range(self.deltaSize)]
                return self.__dfa()
                
        
    def __dfa(self):
    
        K = letters('a', self.k)
        S = letters('0', self.n)
        
        delta = []
        
        for i in range(self.n):
            for j in range(self.k):
                delta.append((
                     (
                      chr(ord('0')+i), 
                      chr(ord('a')+j)
                     ),
                     chr(ord('0')+self.stateDelta[i * self.k + j])
                ))
    
        F = list(
            chr(ord('0')+i) 
            for i in range(self.n)
            if self.stateF[i]
        )
    
        return DFA(K, S, delta, '0', F, self.k, self.n, self.f)
    

if __name__ == '__main__':

    dbConn = sqlite3.connect('dfa.db')
    
    clear(dbConn)
    ensure_validity(dbConn)
    
    testState = fetch(dbConn, 2, 3, 1)
    print(str(testState) + '\n')
    print(testState.dfa())
    testState.next()
    update(dbConn, testState)
    
    print('\n')
    
    testState = fetch(dbConn, 2, 3, 1)
    print(str(testState) + '\n')
    print(testState.dfa())
    
    clear(dbConn)
    
    dbConn.close()
    
