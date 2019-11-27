from DFA import DFA

import sqlite3



def ensureValidity(dbConn):
    
    dbConn.cursor().execute('''
        CREATE TABLE IF NOT EXISTS EnumerationProgress 
        (numberOfStates INTEGER, alphabetSize INTEGER, numberOfAcceptingStates INTEGER, acceptingStatesProgress TEXT, transitionsProgress TEXT, finished INTEGER)'''
    )
    dbConn.commit()
    
    
    
def clear(dbConn):
    
    dbConn.cursor().execute('''DROP TABLE IF EXISTS EnumerationProgress''')
    dbConn.commit()
    
    
    
def __encodeListOfInts(l):
    s = ""
    for n in l:
        s += str(n) + ","
    return s[:-1]
    
    
    
def fetchEnumerationProgress(dbConn, numberOfStates, alphabetSize, numberOfAcceptingStates):

    c = dbConn.cursor()
    
    c.execute('''
        SELECT acceptingStatesProgress, transitionsProgress, finished 
        FROM EnumerationProgress 
        WHERE numberOfStates = ? AND alphabetSize = ? AND numberOfAcceptingStates = ?''', 
        (numberOfStates, alphabetSize, numberOfAcceptingStates)
    )
    result = c.fetchone()
    
    if result == None:
    
        enumProg = EnumerationProgress(numberOfStates, alphabetSize, numberOfAcceptingStates)

        dbTuple = (
            enumProg.numberOfStates,
            enumProg.alphabetSize,
            enumProg.numberOfAcceptingStates,
            __encodeListOfInts(enumProg.acceptingStatesProgress),
            __encodeListOfInts(enumProg.transitionsProgress),
            int(enumProg.finished)
        )
        
        c.execute('''INSERT INTO EnumerationProgress VALUES (?,?,?,?,?,?)''', dbTuple)
        dbConn.commit()
    
        return enumProg
        
    else:
        
        acceptingStatesProgress, transitionsProgress, finished = result
        
        acceptingStatesProgress = [int(i) for i in acceptingStatesProgress.split(",")]
        transitionsProgress     = [int(i) for i in transitionsProgress.split(",")]
        finished                = bool(finished)
        
        return EnumerationProgress.fromExisting(numberOfStates, alphabetSize, numberOfAcceptingStates, acceptingStatesProgress, transitionsProgress, finished)
            
            
            
def updateEnumerationProgress(dbConn, enumProg):

    dbTuple = (
        __encodeListOfInts(enumProg.acceptingStatesProgress),
        __encodeListOfInts(enumProg.transitionsProgress),
        int(enumProg.finished),
        enumProg.numberOfStates,
        enumProg.alphabetSize,
        enumProg.numberOfAcceptingStates
    )
    
    dbConn.cursor().execute('''
        UPDATE EnumerationProgress 
        SET acceptingStatesProgress = ?, transitionsProgress = ?, finished = ? 
        WHERE numberOfStates = ? AND alphabetSize = ? AND numberOfAcceptingStates = ?''',
        dbTuple
    )
    dbConn.commit()
    
    
    
class EnumerationProgress(object):

    def __init__(self, numberOfStates, alphabetSize, numberOfAcceptingStates):
    
        if numberOfStates < 1:
            raise Exception("Number of states must be greater than zero for a DFA.")
    
        self.numberOfStates = numberOfStates
        self.alphabetSize   = alphabetSize
        
        # ----
        
        self.numberOfTransitions     = numberOfStates * alphabetSize
        self.numberOfAcceptingStates = numberOfAcceptingStates
        
        self.acceptingStatesProgress = [1] + [0 for i in range(self.numberOfStates-1)]
        self.transitionsProgress     = [0 for i in range(self.numberOfTransitions)]
        
        # ----
        
        self.finished = False
        
        
    @staticmethod
    def fromExisting(numberOfStates, alphabetSize, numberOfAcceptingStates, acceptingStatesProgress, transitionsProgress, finished):
    
        if numberOfStates < 1:
            raise Exception("Number of states must be greater than zero for a DFA.")
            
        enumProg = EnumerationProgress(numberOfStates, alphabetSize, numberOfAcceptingStates)
        
        enumProg.acceptingStatesProgress = acceptingStatesProgress
        enumProg.transitionsProgress     = transitionsProgress
        enumProg.finished                = finished
        
        return enumProg
        
        
    def __str__(self):
    
        return str((self.numberOfStates, self.alphabetSize, self.numberOfAcceptingStates, self.acceptingStatesProgress, self.transitionsProgress, self.finished))
        
        
    def increment(self):

        def addOneReverse(n, p):
            i = 0
            if n[i] == 0:
                n[i] = 1
                return n
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
        
        if addOneReverse(self.transitionsProgress, self.numberOfStates) != None:
            return self
                
                
        # if transition's end reached, iterate accepting state permutations and reset transition progress
        
        self.transitionsProgress = [0 for i in range(self.numberOfTransitions)]
        
        while True:
        
            addOneReverse(self.acceptingStatesProgress, 2)
            
            actNumberOfAccStates = 0
            for n in p.acceptingStatesProgress:
                if n == 1:
                    actNumberOfAccStates += 1
            
            if actNumberOfAccStates == self.numberOfStates:
                self.finished = True
                return self
                
            if actNumberOfAccStates == self.numberOfAcceptingStates:
                return self
                
        
    def dfa(self):
    
        A = [ chr(i) for i in range(ord('a'), ord('a')+self.alphabetSize) ]
        Q = [ i for i in range(self.numberOfStates) ]
        
        d = []
        for i in range(self.numberOfStates):
            for j in range(self.alphabetSize):
                d.append(((Q[i],A[j]),self.transitionsProgress[i * self.alphabetSize + j]))
        
        s = 0
        F = [ q for q in Q if self.acceptingStatesProgress[q] ]
    
        return DFA(A, Q, d, s, F)
    

if __name__ == "__main__":

    conn = sqlite3.connect('dfa.db')
    
    clear(conn)
    ensureValidity(conn)
    
    test_progress = fetchEnumerationProgress(conn, 3, 2, 1)
    print(str(test_progress) + "\n")
    print(test_progress.dfa())
    test_progress.increment()
    updateEnumerationProgress(conn, test_progress)
    
    print("\n")
    
    test_progress = fetchEnumerationProgress(conn, 3, 2, 1)
    print(str(test_progress) + "\n")
    print(test_progress.dfa())
    
    clear(conn)
    
    conn.close()
    