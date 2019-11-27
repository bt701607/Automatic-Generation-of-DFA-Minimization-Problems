from DFA                     import DFA
from minimize_dfa            import minimization_mark_depth, minimize_dfa
from isomorphy_test_min_dfas import isomorphy_test_min_dfas

import sqlite3



def ensureValidity(dbConn):
    
    dbConn.cursor().execute('''
        CREATE TABLE IF NOT EXISTS MinimalDFAs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, dfa TEXT, numberOfStates INTEGER, minmarkDepth INTEGER, numberOfAcceptingStates INTEGER, alphabetSize INTEGER, used INTEGER)'''
    )
    dbConn.commit()
    
    
    
def clear(dbConn):
    
    dbConn.cursor().execute('''DROP TABLE IF EXISTS MinimalDFAs''')
    dbConn.commit()



def fetchMatchingDFAs(dbConn, numberOfStates, minDepth, maxDepth, alphabetSize, numberOfAcceptingStates):
    
    qFindMatchingDFA = '''SELECT * FROM MinimalDFAs WHERE 
        numberOfStates = ? AND
        minmarkDepth >= ? AND
        minmarkDepth <= ? AND
        numberOfAcceptingStates = ? AND
        alphabetSize = ?
    '''
    
    results = dbConn.cursor().execute(qFindMatchingDFA, (numberOfStates, minDepth, maxDepth, numberOfAcceptingStates, alphabetSize))
    
    resultList = []
    
    for row in results:
    
        id, dfa, properties, used = __interpretDBRow(row)
        
        resultList.append(dfa)
            
    return resultList
            
    

def saveNewDFA(dbConn, dfa, properties, used):

    qSaveDFA = '''INSERT INTO MinimalDFAs VALUES (NULL,?,?,?,?,?,?)'''
    
    row = (__encodeDFA(dfa), properties[0], properties[1], properties[2], properties[3], int(used))

    dbConn.cursor().execute(qSaveDFA, row)
    dbConn.commit()

        
        
def __interpretDBRow(row):

    id, dfa, numberOfStates, minmarkDepth, numberOfAcceptingStates, alphabetSize, used = row

    return id, __decodeDFA(dfa), (numberOfStates, minmarkDepth, numberOfAcceptingStates, alphabetSize), bool(used)



def __encodeDFA(dfa):

    encodedDFA = ""
    
    for c in dfa.alphabet:
        encodedDFA += str(c) + ","
    if len(dfa.alphabet) != 0:
        encodedDFA = encodedDFA[:-1] + ";"
    
    for q in dfa.states:
        encodedDFA += str(q) + ","
    if len(dfa.states) != 0:
        encodedDFA = encodedDFA[:-1] + ";"
    
    for ((q1,c),q2) in dfa.transitions:
        encodedDFA += str(q1) + "." + str(c) + "." + str(q2) + ","
    if len(dfa.transitions) != 0:
        encodedDFA = encodedDFA[:-1] + ";"
    
    encodedDFA += str(dfa.start) + ";"
    
    for q in dfa.accepting:
        encodedDFA += str(q) + ","
    if len(dfa.accepting) != 0:
        encodedDFA = encodedDFA[:-1]
    
    return encodedDFA
    
    
def __decodeDFA(encodedDFA):

    def d(e):
        if e in "0123456789":
            return int(e)
        else:
            return e

    encodedElements = encodedDFA.split(";")
    
    alphabet = encodedElements[0].split(",")
    if '' in alphabet:
        alphabet.remove('')
    
    states = encodedElements[1].split(",")
    if '' in states:
        states.remove('')
    states = [d(e) for e in states]
    
    transitions = encodedElements[2].split(",")
    if '' in transitions:
        transitions.remove('')
    transitions = [t.split(".") for t in transitions]
    transitions = [((d(q1), c), d(q2)) for (q1,c,q2) in transitions]
    
    start = d(encodedElements[3])
    
    accepting = encodedElements[4].split(",")
    if '' in accepting:
        accepting.remove('')
    accepting = [d(e) for e in accepting]
    
    return DFA(alphabet, states, transitions, start, accepting)



if __name__ == "__main__":

    test_dfa1 = DFA(
        ['a','b','c','d','e'],
        [1,2,3,4,5],
        [
            ((1,'a'),1),
            ((1,'b'),2),
            ((2,'c'),4),
            ((5,'d'),1),
            ((2,'e'),5)
        ],
        1,
        [4,5]
    )

    test_dfa2 = DFA(
        ['0', '1'],
        ['AD', 'B', 'CE', 'G'],
        [
            (('AD','1'),'CE'),
            (('AD','0'),'G' ),
            
            (('B' ,'0'),'CE'),
            (('B' ,'1'),'CE'),
            
            (('CE','0'),'B' ),
            (('CE','1'),'AD'),
            
            (('G' ,'0'),'B' ),
            (('G' ,'1'),'CE'),
        ],
        'AD',
        ['CE']
    )
    
    #print("En-/Decode-Test 1. Expecting equal DFAs:\n")
    
    #print(str(test_dfa1))
    #print(str(__decodeDFA(__encodeDFA(test_dfa1))) + "\n\n")
    
    #print("En-/Decode-Test 2. Expecting equal DFAs:\n")
    
    #print(str(test_dfa2))
    #print(str(__decodeDFA(__encodeDFA(test_dfa2))))


    #conn = sqlite3.connect('dfa.db')
    
    #clear(conn)
    #ensureValidity(conn)
    
    #minDFA = minimize_dfa(test_dfa1)
    #properties = (len(test_dfa1.states), minimization_mark_depth(test_dfa1), len(test_dfa1.accepting), len(test_dfa1.alphabet))
    
    #print(properties)
    
    #saveNewDFA(conn, minDFA, properties, False)
    
    #foundDFA1 = findMatchingUnusedMinimalDFA(conn, properties[0], properties[1], properties[1]+1, properties[2], properties[3])
    #foundDFA2 = findMatchingUnusedMinimalDFA(conn, properties[0], properties[1], properties[1]+1, properties[2], properties[3])
    
    #print(foundDFA1, foundDFA2, hasIsomorphMatchingDFA(conn, minDFA, properties))
    
    #clear(conn)
    
    #conn.close()
