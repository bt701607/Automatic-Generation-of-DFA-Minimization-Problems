"""
module: minimization.py
author: Gregor Soennichsen


"""

import copy

from dfa import DFA


# returned dfa has minmarkDepth set
def minimize_dfa(dfa):

    return __del_dupl_states(__del_unr_states(copy.deepcopy(dfa)))


# -----------------------------------------------------------


def has_unr_states(dfa):

    # find unreachable states via breadth-first search

    undiscovered = set(dfa.states)
    undiscovered.remove(dfa.start)

    observed = set([dfa.start])

    discovered = set()

    delta = dict(dfa.transitions)

    while len(observed) != 0:

        newObserved = set()

        for q in observed:
            for sigma in dfa.alphabet:
                if (q,sigma) in delta:

                    p = delta[(q,sigma)]
                    if p not in observed and p not in discovered:
                        newObserved.add(p)

        undiscovered.difference_update(newObserved)
        discovered.update(observed)
        observed = newObserved

    return len(undiscovered) > 0


def __del_unr_states(dfa):

    # find unreachable states via breadth-first search

    undiscovered = set(dfa.states)
    undiscovered.remove(dfa.start)

    observed = set([dfa.start])

    discovered = set()

    delta = dict(dfa.transitions)

    while len(observed) != 0:

        newObserved = set()

        for q in observed:
            for sigma in dfa.alphabet:
                if (q,sigma) in delta:

                    p = delta[(q,sigma)]
                    if p not in observed.union(discovered):
                        newObserved.add(p)

        undiscovered.difference_update(newObserved)
        discovered.update(observed)
        observed = newObserved

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

    dfa.k = len(dfa.alphabet)
    dfa.n = len(dfa.states)
    dfa.f = len(dfa.accepting)

    return dfa


# -----------------------------------------------------------


# sets depth of dfa
def has_dupl_states(dfa):

    # find duplicate states via the minimization-mark algorithm

    M = set()

    for q in dfa.accepting:
        for p in dfa.states:
            if p not in dfa.accepting:
                M.add((p,q))
                M.add((q,p))

    delta = dict(dfa.transitions)

    depth = 0

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
            depth += 1

    for p in dfa.states:
        for q in dfa.states:
            if p != q and (p,q) not in M:
                return False

    # update informations

    dfa.depth = depth

    return True


# sets depth of dfa
def __del_dupl_states(dfa):

    # find duplicate states via the minimization-mark algorithm

    M = set()

    for q in dfa.accepting:
        for p in dfa.states:
            if p not in dfa.accepting:
                M.add((p,q))
                M.add((q,p))

    delta = dict(dfa.transitions)

    depth = 0

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
            depth += 1

    # merge duplicate states
    duplStatePairs = [
        (p,q) 
        for p in dfa.states 
            for q in dfa.states 
               if (p,q) not in M and p != q
    ]

    while len(duplStatePairs) != 0:

        (p,q) = duplStatePairs.pop()

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

        for i in range(len(duplStatePairs)):
            (q1,q2) = duplStatePairs[i]
            if q1 == q:
                q1 = p
            if q2 == q:
                q2 = p
            duplStatePairs[i] = (q1,q2)

    dfa.transitions = list(set(dfa.transitions))

    # update informations

    dfa.depth  = depth
    dfa.planar = None

    dfa.k = len(dfa.alphabet)
    dfa.n = len(dfa.states)
    dfa.f = len(dfa.accepting)

    return dfa


def tex_min_table(dfa):

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

    columnSpec = '|'.join((dfa.n+1) * 'c' )
    tex += '\\begin{tabular}{' + columnSpec + '}\n'

    innerTableHead = ''.join(['& {0}  '.format(p) for p in dfa.states])
    tex += '	   ' + innerTableHead + '\\\\\\hline\n'

    for i in range(dfa.n):

        q = dfa.states[i]

        rowStart = '	{0}  '.format(q)

        for j in range(dfa.n):

            p = dfa.states[j]

            if (j-i) < 1:
                rowStart += '& \\x '
            elif (q,p) in m:
                rowStart += '& {0}  '.format(m[(q,p)])
            else:
                rowStart += '&    '

        tex += rowStart + '\\\\\\hline\n'

    return tex + '\\end{tabular}\n'



if __name__ == '__main__':

    testDFA = DFA(
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

    print(str(testDFA) + '\n')

    testDFA = __del_unr_states(testDFA)

    print(tex_min_table(testDFA))

    print('\n' + str(testDFA) + '\n')

    testDFA = __del_dupl_states(testDFA)

    print('\n' + str(testDFA) + '\ndepth = ' + str(testDFA.depth))
