from DFA          import DFA
from copy         import deepcopy


def minimize_dfa(dfa):
    
    return delete_duplicate_states(delete_unreachable_states(dfa))


def delete_unreachable_states(dfa):
    
    dfa = deepcopy(dfa)
                
    # find unreachable states via breadth-first search
    
    undiscovered = set(dfa.states)
    undiscovered.remove(dfa.start)
    
    observed = set([dfa.start])
    
    discovered = set()
                
    delta = dict(dfa.transitions)
    
    while len(observed) != 0:
        
        new_observed = set()
        
        for q in observed:
            for sigma in dfa.alphabet:
                if (q,sigma) in delta:
                    
                    p = delta[(q,sigma)]
                    if p not in observed.union(discovered):
                        new_observed.add(p)

        undiscovered.difference_update(new_observed)
        discovered.update(observed)
        observed = new_observed
        
    # delete unreachable states
    
    for q in undiscovered:
        dfa.states.remove(q)
        
        if q in dfa.accepting:
            dfa.accepting.remove(q)
            
        transitions_to_remove = [((q1,s),q2) for ((q1,s),q2) in dfa.transitions if q1 == q or q2 == q]
        for t in transitions_to_remove:
            dfa.transitions.remove(t)
        
    return dfa


def delete_duplicate_states(dfa):
    
    dfa = deepcopy(dfa)
    
    # find duplicate states via the minimization-mark algorithm
    
    M = set()
    
    for q in dfa.accepting:
        for p in dfa.states:
            if p not in dfa.accepting:
                M.add((p,q))
                M.add((q,p))
                
    delta = dict(dfa.transitions)
                
    while True:
        
        N = set()
        
        for q in dfa.states:
            for p in dfa.states:
                if (p,q) not in M:
                    for sigma in dfa.alphabet:
                        
                        if (p,sigma) in delta and (q,sigma) in delta:
                            if (delta[(p,sigma)], delta[(q,sigma)]) in M:
                                N.add((p,q))
                                break
                            
        M = M.union(N)
        
        if len(N) == 0:
            break
        
    # merge duplicate states
    duplicate_state_pairs = [(p,q) for p in dfa.states for q in dfa.states if (p,q) not in M and p != q]
    
    while len(duplicate_state_pairs) != 0:
        
        #print(duplicate_state_pairs)
        (p,q) = duplicate_state_pairs.pop()
        #print(duplicate_state_pairs)
        
        if p == q:
            continue
        
        dfa.states.remove(q)
        
        if dfa.start == q:
            dfa.start = p
            
        if q in dfa.accepting:
            dfa.accepting.remove(q)
            
        for i in range(len(dfa.transitions)):
            t = (q1,s),q2 = dfa.transitions[i]
            
            if q1 == q:
                q1 = p
            if q2 == q:
                q2 = p
                
            dfa.transitions[i] = (q1,s),q2
            
        for i in range(len(duplicate_state_pairs)):
            (q1,q2) = duplicate_state_pairs[i]
            if q1 == q:
                q1 = p
            if q2 == q:
                q2 = p
            duplicate_state_pairs[i] = (q1,q2)
            
    dfa.transitions = list(set(dfa.transitions))
            
    return dfa


# -----------------------------------------------------


def minimization_mark_depth(dfa):
    
    dfa = deepcopy(dfa)
    
    # find duplicate states via the minimization-mark algorithm
    
    M = set()
    
    min_mark_depth = 0
    
    for q in dfa.accepting:
        for p in dfa.states:
            if p not in dfa.accepting:
                M.add((p,q))
                M.add((q,p))
                
    delta = dict(dfa.transitions)
                
    while True:
        
        N = set()
        
        for q in dfa.states:
            for p in dfa.states:
                if (p,q) not in M:
                    for sigma in dfa.alphabet:
                        
                        if (p,sigma) in delta and (q,sigma) in delta:
                            if (delta[(p,sigma)], delta[(q,sigma)]) in M:
                                N.add((p,q))
                                break
                            
        M = M.union(N)
        
        if len(N) == 0:
            break
        else:
            min_mark_depth += 1
            
    return min_mark_depth
    
    



if __name__ == "__main__":

    test_dfa = DFA(
        ['a','b','c','d','e'],
        [1,2,3,4,5,6],
        [
            ((1,'a'),1),
            ((1,'b'),2),
            ((2,'c'),4),
            ((5,'d'),1),
            ((2,'e'),5),
            ((6,'a'),4)
        ],
        1,
        [4,5]
    )
        
    test_dfa = DFA(
        ['0','1'],
        ['A','B','C','D','E','F','G'],
        [
            (('A','1'),'C'),
            (('A','0'),'G'),
            (('B','1'),'E'),
            (('B','0'),'C'),
            (('C','1'),'D'),
            (('C','0'),'B'),
            (('D','1'),'E'),
            (('D','0'),'G'),
            (('E','1'),'A'),
            (('E','0'),'B'),
            (('F','1'),'E'),
            (('F','0'),'B'),
            (('G','1'),'C'),
            (('G','0'),'B'),
        ],
        'A',
        ['C','E']
    )
        
    print(minimization_mark_depth(test_dfa))
    
    print("\n" + str(test_dfa) + "\n")
    
    test_dfa = delete_unreachable_states(test_dfa)
    
    print("\n" + str(test_dfa) + "\n")
    
    test_dfa = delete_duplicate_states(test_dfa)
    
    print("\n" + str(test_dfa) + "\n")
