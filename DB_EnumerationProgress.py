from DFA import DFA

import sqlite3



def ensureValidity(dbConn):
    
    with dbConn:
        dbConn.execute('''
            CREATE TABLE IF NOT EXISTS EnumerationProgress 
            (alphabetSize INT, numberOfStates INT, numberOfAcceptingStates INT, acceptingStatesProgress TEXT, transitionsProgress TEXT, finished INT)'''
        )
    
    
    
def clear(dbConn):
    
    with dbConn:
        dbConn.execute('''DROP TABLE IF EXISTS EnumerationProgress''')
    
    
# -----------------------------------------------------------
    
    
def __encodeListOfInts(intList):

    resultString = ''
   
    for n in intList:
        resultString += str(n) + ','
        
    return resultString[:-1]
    
    
def fetchEnumerationProgress(dbConn, alphabetSize, numberOfStates, numberOfAcceptingStates):

    qFetch = '''
        SELECT acceptingStatesProgress, transitionsProgress, finished 
        FROM EnumerationProgress 
        WHERE alphabetSize = ? AND numberOfStates = ? AND numberOfAcceptingStates = ?
    '''

    c = dbConn.cursor()
    c.execute(qFetch, (alphabetSize, numberOfStates, numberOfAcceptingStates))
    dbResult = c.fetchone()
    
    if dbResult == None:
    
        enumProg = EnumerationProgress(alphabetSize, numberOfStates, numberOfAcceptingStates)

        dbTuple = (
            enumProg.alphabetSize,
            enumProg.numberOfStates,
            enumProg.numberOfAcceptingStates,
            __encodeListOfInts(enumProg.acceptingStatesProgress),
            __encodeListOfInts(enumProg.transitionsProgress),
            int(enumProg.finished)
        )
        
        with dbConn:
            dbConn.execute('''INSERT INTO EnumerationProgress VALUES (?,?,?,?,?,?)''', dbTuple)
    
        return enumProg
        
    else:
        
        acceptingStatesProgress, transitionsProgress, finished = dbResult
        
        acceptingStatesProgress = [int(i) for i in acceptingStatesProgress.split(',')]
        transitionsProgress     = [int(i) for i in transitionsProgress.split(',')]
        finished                = bool(finished)
        
        return EnumerationProgress.fromExisting(alphabetSize, numberOfStates, numberOfAcceptingStates, acceptingStatesProgress, transitionsProgress, finished)
            
            
            
def updateEnumerationProgress(dbConn, enumProg):

    qUpdate = '''
        UPDATE EnumerationProgress 
        SET acceptingStatesProgress = ?, transitionsProgress = ?, finished = ? 
        WHERE alphabetSize = ? AND numberOfStates = ? AND numberOfAcceptingStates = ?
    '''

    dbTuple = (
        __encodeListOfInts(enumProg.acceptingStatesProgress),
        __encodeListOfInts(enumProg.transitionsProgress),
        int(enumProg.finished),
        enumProg.alphabetSize,
        enumProg.numberOfStates,
        enumProg.numberOfAcceptingStates
    )
    
    with dbConn:
        dbConn.execute(qUpdate, dbTuple)
    
    
# -----------------------------------------------------------
    
    
class EnumerationProgress(object):

    def __init__(self, alphabetSize, numberOfStates, numberOfAcceptingStates):
    
        if numberOfStates < 1:
            raise Exception('Number of states must be greater than zero for a DFA.')
    
        self.alphabetSize   = alphabetSize
        self.numberOfStates = numberOfStates
        
        # ----
        
        self.numberOfAcceptingStates = numberOfAcceptingStates
        self.numberOfTransitions     = numberOfStates * alphabetSize
        
        self.acceptingStatesProgress = [1 for i in range(numberOfAcceptingStates)] + [0 for i in range(numberOfStates-numberOfAcceptingStates)]
        self.transitionsProgress     = [0 for i in range(self.numberOfTransitions)]
        
        # ----
        
        self.finished = False
        
        
    @staticmethod
    def fromExisting(alphabetSize, numberOfStates, numberOfAcceptingStates, acceptingStatesProgress, transitionsProgress, finished):
    
        if numberOfStates < 1:
            raise Exception('Number of states must be greater than zero for a DFA.')
            
        enumProg = EnumerationProgress(alphabetSize, numberOfStates, numberOfAcceptingStates)
        
        enumProg.acceptingStatesProgress = acceptingStatesProgress
        enumProg.transitionsProgress     = transitionsProgress
        enumProg.finished                = finished
        
        return enumProg
        
        
    def __str__(self):
    
        return str((self.alphabetSize, self.numberOfStates, self.numberOfAcceptingStates, self.acceptingStatesProgress, self.transitionsProgress, self.finished))
        
        
    def nextDFA(self):

        def addOneReverse(n, p):
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
        
        if addOneReverse(self.transitionsProgress, self.numberOfStates) != None:
            return self.__dfa()
        
        # if transition's end reached, iterate accepting state permutations
        # and reset transition progress if acceptingStatesProgress could be incremented
        
        while True:
        
            if addOneReverse(self.acceptingStatesProgress, 2) == None:
                self.finished = True
                return None
                
            if self.acceptingStatesProgress.count(1) == self.numberOfAcceptingStates:
                self.transitionsProgress = [0 for i in range(self.numberOfTransitions)]
                return self.__dfa()
                
        
    def __dfa(self):
    
        return DFA(
        
            list(chr(i)    for i in range(97, 97+self.alphabetSize)), # chr(97) = 'a'
            list(chr(48+i) for i in range(self.numberOfStates)),      # chr(48) = '0'
            list(((chr(48+i), chr(97+j)), chr(48+self.transitionsProgress[i * self.alphabetSize + j])) for i in range(self.numberOfStates) for j in range(self.alphabetSize)),
            '0',
            list(chr(48+i) for i in range(self.numberOfStates) if self.acceptingStatesProgress[i]),
            
            self.alphabetSize,
            self.numberOfStates,
            self.numberOfAcceptingStates
            
        )
    

if __name__ == '__main__':

    dbConn = sqlite3.connect('dfa.db')
    
    clear(dbConn)
    ensureValidity(dbConn)
    
    test_progress = fetchEnumerationProgress(dbConn, 2, 3, 1)
    print(str(test_progress) + '\n')
    print(test_progress.dfa())
    test_progress.increment()
    updateEnumerationProgress(dbConn, test_progress)
    
    print('\n')
    
    test_progress = fetchEnumerationProgress(dbConn, 2, 3, 1)
    print(str(test_progress) + '\n')
    print(test_progress.dfa())
    
    clear(dbConn)
    
    dbConn.close()
    