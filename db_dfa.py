"""
module: db_dfa.py
author: Gregor Soennichsen


"""

import sqlite3

from dfa import DFA


def ensure_validity(dbConn):
    
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
    
    
def clear(dbConn):
    
    with dbConn:
        dbConn.execute('''DROP TABLE IF EXISTS MinimalDFAs''')
    
    
# -----------------------------------------------------------


# sets dfa.depth and dfa.planar
def fetch(dbConn, k, n, f, dmin, dmax):
    
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
    
        dfa = __decode_dfa(encodedDFA)
        dfa.depth  = depth
        dfa.planar = planar
        dfaList.append(dfa)
            
    return dfaList
            
    
    
# requires dfa.depth and dfa.planar to be set
def save(dbConn, dfa):

    assert dfa.depth  != None, 'dfa.depth  is required to be set'
    assert dfa.planar != None, 'dfa.planar is required to be set'
    
    dbTuple = (__encode_dfa(dfa), dfa.k, dfa.n, dfa.f, dfa.depth, dfa.planar)

    with dbConn:
        dbConn.execute('''INSERT INTO MinimalDFAs VALUES (NULL,?,?,?,?,?,?)''', dbTuple)
    
    
# -----------------------------------------------------------


def __encode_dfa(dfa):

    encodedDFA = ''
    
    for c in dfa.alphabet:
        encodedDFA += str(c) + ','
    if len(dfa.alphabet) != 0:
        encodedDFA = encodedDFA[:-1] + ';'
    
    for q in dfa.states:
        encodedDFA += str(q) + ','
    if len(dfa.states) != 0:
        encodedDFA = encodedDFA[:-1] + ';'
    
    for ((q1,c),q2) in dfa.transitions:
        encodedDFA += str(q1) + '.' + str(c) + '.' + str(q2) + ','
    if len(dfa.transitions) != 0:
        encodedDFA = encodedDFA[:-1] + ';'
    
    encodedDFA += str(dfa.start) + ';'
    
    for q in dfa.accepting:
        encodedDFA += str(q) + ','
    if len(dfa.accepting) != 0:
        encodedDFA = encodedDFA[:-1]
    
    return encodedDFA
    
    
def __decode_dfa(encodedDFA):

    encodedElements = encodedDFA.split(';')
    
    alphabet = encodedElements[0].split(',')
    if '' in alphabet:
        alphabet.remove('')
    
    states = encodedElements[1].split(',')
    if '' in states:
        states.remove('')
    
    transitions = encodedElements[2].split(',')
    if '' in transitions:
        transitions.remove('')
    transitions = [t.split('.') for t in transitions]
    transitions = [((q1, c), q2) for (q1,c,q2) in transitions]
    
    start = encodedElements[3]
    
    accepting = encodedElements[4].split(',')
    if '' in accepting:
        accepting.remove('')
    
    return DFA(alphabet, states, transitions, start, accepting,
               len(alphabet), len(states), len(accepting))



if __name__ == '__main__':

    test_dfa1 = DFA(
        ['a','b','c','d','e'],
        ['1','2','3','4','5'],
        [
            (('1','a'),'1'),
            (('1','b'),'2'),
            (('2','c'),'4'),
            (('5','d'),'1'),
            (('2','e'),'5')
        ],
        '1',
        ['4','5']
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
    
    #print('En-/Decode-Test 1. Expecting equal DFAs:\n')
    
    #print(str(test_dfa1))
    #print(str(__decodeDFA(__encodeDFA(test_dfa1))) + '\n\n')
    
    #print('En-/Decode-Test 2. Expecting equal DFAs:\n')
    
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
