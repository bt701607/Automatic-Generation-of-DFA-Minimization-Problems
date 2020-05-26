"""
module: isomorphy.py
author: Gregor Soennichsen


"""

from dfa import DFA
        
        
def contains_isomorph_dfa(testDFA, dfaList):
    
    for dfa in dfaList:

        if isomorphy_test(testDFA, dfa) == True:
    
            return True
            
    return False


def isomorphy_test(dfa1, dfa2):

    if dfa1.n != dfa2.n or dfa1.f != dfa2.f or dfa1.k != dfa2.k:
        return False
        
    delta2 = dict(dfa2.transitions)

    bijection = dict()
    
    bijection[dfa1.start] = dfa2.start
    
    finished = [dfa1.start]
    observed = []
    
    actState = dfa1.start
    
    
    while True:
    
        for ((q1,c),p1) in dfa1.transitions:
            if q1 != actState:
                continue
                
            p2 = delta2[(bijection[actState], c)]

            p1Marked = p1 in bijection.keys()
            p2Marked = p2 in bijection.values()
            
            if p1Marked and p2Marked:
            
                if bijection[p1] != p2:
                    return False
                    
            elif not p1Marked and not p2Marked:
            
                bijection[p1] = p2
                if p1 not in finished:
                    observed.append(p1)

            else:

                return False
    
        if not observed:
            break
            
        actState = observed.pop()
        finished.append(actState)
        
    for q in dfa1.final:
        if bijection[q] not in dfa2.final:
            return False
        
    return True
   

if __name__ == '__main__':

    print('Executing test cases.\n')

    testDFA1 = DFA(
        ['0', '1'],
        ['B', 'D', 'E', 'G'],
        [
                (('D', '0'), 'G'),
                (('D', '1'), 'E'),
                (('E', '0'), 'B'),
                (('B', '1'), 'E'),
                (('G', '1'), 'E'),
                (('E', '1'), 'D'),
                (('G', '0'), 'B'),
                (('B', '0'), 'E'),
        ],
        'D',
        ['E']
    )

    testDFA1_1 = DFA(
        ['0', '1'],
        ['R', '1', 'e', 'q'],
        [
                (('1', '0'), 'q'),
                (('1', '1'), 'e'),
                (('e', '0'), 'R'),
                (('R', '1'), 'e'),
                (('q', '1'), 'e'),
                (('e', '1'), '1'),
                (('q', '0'), 'R'),
                (('R', '0'), 'e'),
        ],
        '1',
        ['e']
    )

    test_dfa1_2 = DFA(
        ['0', '1'],
        ['B', 'x', 'E', 'G'],
        [
                (('x', '0'), 'G'),
                (('x', '1'), 'E'),
                (('E', '0'), 'B'),
                (('B', '1'), 'E'),
                (('G', '1'), 'E'),
                (('E', '1'), 'E'),
                (('G', '0'), 'B'),
                (('B', '0'), 'E'),
        ],
        'x',
        ['E']
    )
    
    print('''TestDFA1. Expected - True. 
           Result: ''' + str(isomorphy_test(testDFA1, testDFA1_1)))
           
    print('''TestDFA1. Expected - False. 
           Result: ''' + str(isomorphy_test(testDFA1, testDFA1_2)))
    
    testDFA2 = DFA(
        ['a', 'b', 'c', 'd', 'e'],
        [2, 5],
        [
                ((5, 'd'), 2),
                ((2, 'c'), 5),
                ((2, 'a'), 2),
                ((2, 'e'), 5),
                ((2, 'b'), 2),
        ],
        2,
        [5]
    )
    
    testDFA2_1 = DFA(
        ['a', 'b', 'c', 'd', 'e'],
        [1, 2],
        [
                ((2, 'd'), 1),
                ((1, 'c'), 2),
                ((1, 'a'), 1),
                ((1, 'e'), 2),
                ((1, 'b'), 1),
        ],
        1,
        [2]
    )
    
    testDFA2_2 = DFA(
        ['a', 'B', 'c', 'd', 'e'],
        [2, 3],
        [
                ((3, 'd'), 2),
                ((2, 'c'), 3),
                ((2, 'a'), 2),
                ((2, 'e'), 3),
                ((2, 'B'), 2),
        ],
        2,
        [3]
    )
    
    print('''TestDFA2. Expected - True. 
           Result: ''' + str(isomorphy_test(testDFA2, testDFA2_1)))
           
    print('''TestDFA2. Expected - False. 
           Result: ''' + str(isomorphy_test(testDFA2, testDFA2_2)))
    
    
   
