from DFA import DFA

import copy


# returned dfa has minmarkDepth set
def minimize_dfa(dfa):

    return __delete_duplicate_states(__delete_unreachable_states(copy.deepcopy(dfa)))


# -----------------------------------------------------------


def has_unreachable_states(dfa):

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
                    if p not in observed and p not in discovered:
                        new_observed.add(p)

        undiscovered.difference_update(new_observed)
        discovered.update(observed)
        observed = new_observed

    return len(undiscovered) > 0


def __delete_unreachable_states(dfa):

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

        for i in reversed(range(len(dfa.transitions))):
            t = dfa.transitions[i]
            if t[0][0] == q or t[1] == q:
                dfa.transitions.remove(t)

    # update informations

    dfa.alphabetSize            = len(dfa.alphabet)
    dfa.numberOfStates          = len(dfa.states)
    dfa.numberOfAcceptingStates = len(dfa.accepting)

    return dfa


# -----------------------------------------------------------


# sets minmarkDepth of dfa
def has_duplicate_states(dfa):

    # find duplicate states via the minimization-mark algorithm

    M = set()

    for q in dfa.accepting:
        for p in dfa.states:
            if p not in dfa.accepting:
                M.add((p,q))
                M.add((q,p))

    delta = dict(dfa.transitions)

    min_mark_depth = 0

    while True:

        N = set()

        for q in dfa.states:
            for p in dfa.states:
                if (p,q) not in M:
                    for sigma in dfa.alphabet:

                        if (p,sigma) in delta and (q,sigma) in delta:
                            if (delta[(p,sigma)], delta[(q,sigma)]) in M:
                                N.add((p,q))
                                N.add((q,p))
                                break

        M = M.union(N)

        if len(N) == 0:
            break
        else:
            min_mark_depth += 1

    duplicate_state_pairs = [(p,q) for p in dfa.states for q in dfa.states if (p,q) not in M and p != q]

    for p in dfa.states:
        for q in dfa.states:
            if p != q and (p,q) not in M:
                return False

    # update informations

    dfa.minmarkDepth = min_mark_depth

    return True


# sets minmarkDepth of dfa
def __delete_duplicate_states(dfa):

    # find duplicate states via the minimization-mark algorithm

    M = set()

    for q in dfa.accepting:
        for p in dfa.states:
            if p not in dfa.accepting:
                M.add((p,q))
                M.add((q,p))

    delta = dict(dfa.transitions)

    min_mark_depth = 0

    while True:

        N = set()

        for q in dfa.states:
            for p in dfa.states:
                if (p,q) not in M:
                    for sigma in dfa.alphabet:

                        if (p,sigma) in delta and (q,sigma) in delta:
                            if (delta[(p,sigma)], delta[(q,sigma)]) in M:
                                N.add((p,q))
                                N.add((q,p))
                                break

        M = M.union(N)

        if len(N) == 0:
            break
        else:
            min_mark_depth += 1

    # merge duplicate states
    duplicate_state_pairs = [(p,q) for p in dfa.states for q in dfa.states if (p,q) not in M and p != q]

    while len(duplicate_state_pairs) != 0:

        (p,q) = duplicate_state_pairs.pop()

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

    # update informations

    dfa.minmarkDepth = min_mark_depth
    dfa.isPlanar     = None

    dfa.alphabetSize            = len(dfa.alphabet)
    dfa.numberOfStates          = len(dfa.states)
    dfa.numberOfAcceptingStates = len(dfa.accepting)

    return dfa


def tex_minimization_table(dfa):

    # find duplicate states via the minimization-mark algorithm

    m = {}

    M = set()
    for q in dfa.accepting:
        for p in dfa.states:
            if p not in dfa.accepting:
                M.add((p,q))
                M.add((q,p))
                m[(p,q)] = 0
                m[(q,p)] = 0

    delta = dict(dfa.transitions)

    i = 0

    while True:

        N = set()

        for q in dfa.states:
            for p in dfa.states:
                if (p,q) not in M:
                    for sigma in dfa.alphabet:

                        if (p,sigma) in delta and (q,sigma) in delta:
                            if (delta[(p,sigma)], delta[(q,sigma)]) in M:
                                N.add((p,q))
                                N.add((q,p))
                                m[(p,q)] = i
                                m[(q,p)] = i
                                break

        M = M.union(N)

        if len(N) == 0:
            break
        else:
            i += 1

    # create tex code for minimization table

    tex = ''

    column_spec = '|'.join((dfa.numberOfStates+1) * 'c' )
    tex += '\\begin{tabular}{' + column_spec + '}\n'

    inner_table_head = ''.join(['& {0}  '.format(p) for p in dfa.states])
    tex += '	   ' + inner_table_head + '\\\\\\hline\n'

    for i in range(dfa.numberOfStates):

        q = dfa.states[i]

        row_start = '	{0}  '.format(q)

        for j in range(dfa.numberOfStates):

            p = dfa.states[j]

            if (j-i) < 1:
                row_start += '& \\x '
            elif (q,p) in m:
                row_start += '& {0}  '.format(m[(q,p)])
            else:
                row_start += '&    '

        tex += row_start + '\\\\\\hline\n'

    return tex + '\\end{tabular}\n'



if __name__ == "__main__":

    test_dfa = DFA(
        ['0','1','2'],
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

    print(str(test_dfa) + "\n")

    test_dfa = __delete_unreachable_states(test_dfa)

    print(tex_minimization_table(test_dfa))

    print("\n" + str(test_dfa) + "\n")

    test_dfa = __delete_duplicate_states(test_dfa)

    print("\n" + str(test_dfa) + "\nminmarkDepth = " + str(test_dfa.minmarkDepth))
