from DFA import DFA
        
        
def contains_isomorph_dfa(testDFA, dfaList):
    
    for dfa in dfaList:

        if isomorphy_test_min_dfas(testDFA, dfa) == True:
    
            return True
            
    return False


def isomorphy_test_min_dfas(dfa1, dfa2):

    if dfa1.numberOfStates != dfa2.numberOfStates:
        return False

    if dfa1.numberOfAcceptingStates != dfa2.numberOfAcceptingStates:
        return False
        
    if dfa1.alphabet != dfa2.alphabet:
        return False
        
    delta2 = dict(dfa2.transitions)

    bijection = dict()
    
    bijection[dfa1.start] = dfa2.start
    
    finished_states = [dfa1.start]
    observed_states = []
    
    act_state = dfa1.start
    
    
    while True:
    
        for ((q1,c),p1) in dfa1.transitions:
            if q1 == act_state:
                
                p1Marked = p1 in bijection.keys()
                
                p2 = delta2[(bijection[act_state], c)]
                    
                p2Marked = p2 in bijection.values()
                
                if p1Marked and p2Marked:
                
                    if bijection[p1] != p2:
                        return False
                        
                elif not p1Marked and not p2Marked:
                
                    bijection[p1] = p2
                    
		    if p1 not in finished_states:
		        observed_states.append(p1)
                    
                else:
                
                    return False
    
        if not observed_states:
            break
            
        act_state = observed_states.pop()
        
        finished_states.append(act_state)
        
    for q in dfa1.accepting:
        if bijection[q] not in dfa2.accepting:
            return False
        
    return True
   

if __name__ == "__main__":

    print("Executing test cases.\n")

    test_dfa1 = DFA(
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

    test_dfa1_isomorph = DFA(
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

    test_dfa1_not_isomorph = DFA(
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
    
    print("TestDFA1. Expected - True. Result: " + str(isomorphy_test_min_dfas(test_dfa1, test_dfa1_isomorph)))
    print("TestDFA1. Expected - False. Result: " + str(isomorphy_test_min_dfas(test_dfa1, test_dfa1_not_isomorph)))
    
    test_dfa2 = DFA(
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
    
    test_dfa2_isomorph = DFA(
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
    
    test_dfa2_not_isomorph = DFA(
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
    
    print("TestDFA2. Expected - True. Result: " + str(isomorphy_test_min_dfas(test_dfa2, test_dfa2_isomorph)))
    print("TestDFA2. Expected - False. Result: " + str(isomorphy_test_min_dfas(test_dfa2, test_dfa2_not_isomorph)))
    
    
   