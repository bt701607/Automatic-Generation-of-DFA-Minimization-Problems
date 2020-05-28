"""
module: minimization.py
author: Gregor Soennichsen


"""

import copy

from dfa import DFA


# returned dfa has minmarkDepth set
def minimize_dfa(dfa):

    return _del_dupl_states(_del_unr_states(copy.deepcopy(dfa)))


# -----------------------------------------------------------


def _comp_unr_states(dfa):

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

    return undiscovered


def has_unr_states(dfa):

    return bool(_comp_unr_states(dfa))


def _del_unr_states(dfa):

    unreachable = _comp_unr_states(dfa)

    for q in unreachable:
        dfa.states.remove(q)

        if q in dfa.final:
            dfa.final.remove(q)

        for i in reversed(range(len(dfa.transitions))):
            t = dfa.transitions[i]
            if t[0][0] == q or t[1] == q:
                dfa.transitions.remove(t)

    # update informations

    dfa.k = len(dfa.alphabet)
    dfa.n = len(dfa.states)
    dfa.f = len(dfa.final)

    return dfa


# -----------------------------------------------------------


def _comp_dupl_states(dfa):

    m = {}

    M = set()
    for q in dfa.final:
        for p in dfa.states:
            if p not in dfa.final:
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
            
    return m, M, i


# sets depth of dfa
def has_dupl_states(dfa):

    m, M, depth = _comp_dupl_states(dfa)

    for p in dfa.states:
        for q in dfa.states:
            if p != q and (p,q) not in M:
                return False

    # update informations

    dfa.depth = depth

    return True


# sets depth of dfa
def _del_dupl_states(dfa):

    m, M, depth = _comp_dupl_states(dfa)

    # merge duplicate states
    duplStatePairs = [
        (p,q) 
        for p in dfa.states 
            for q in dfa.states 
               if (p,q) not in M and p != q
    ]

    while duplStatePairs:

        (p,q) = duplStatePairs.pop()

        if p == q:
            continue

        dfa.states.remove(q)

        if dfa.start == q:
            dfa.start = p

        if q in dfa.final:
            dfa.final.remove(q)

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
    dfa.f = len(dfa.final)

    return dfa


def tex_min_table(dfa):

    m, M, depth = _comp_dupl_states(dfa)

    tex = '\n'

    columnSpec = '|'.join((dfa.n+1) * 'c' )
    tex += '\\begin{tabular}{' + columnSpec + '}\n'

    innerTableHead = ''.join(['& ${}$ '.format(p) for p in dfa.states])
    tex += '	     ' + innerTableHead + '\\\\\\hline\n'

    for i in range(dfa.n):

        q = dfa.states[i]

        rowStart = '	${}$  '.format(q)

        for j in range(dfa.n):

            p = dfa.states[j]

            if (j-i) < 1:
                rowStart += '& \\x  '
            elif (q,p) in m:
                rowStart += '& ${}$ '.format(m[(q,p)])
            else:
                rowStart += '&     '

        tex += rowStart + '\\\\\\hline\n'

    return tex + '\\end{tabular}\n'
