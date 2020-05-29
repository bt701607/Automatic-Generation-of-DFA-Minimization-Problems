#!/usr/bin/env python

"""Specifies methods concerned with minimization of DFAs.
The algorithms in this module are based on Hopcroft's Minimization Algorithm.

minimize_dfa
    Returns a minimized copy of a complete DFA.

_comp_unr_states
    Returns the set of unreachable states to a given DFA.

has_unr_states
    Returns whether a given DFA has unreachable states.

_del_unr_states
    Deletes all unreachable states from a given DFA.

_comp_inequiv_states
    Computes all inequivalent states to a given DFA.

has_equiv_states
    Returns whether a given DFA has equivalent states.

_del_equiv_states
    Merges all equivalent state pairs of a DFA.

tex_min_table
    Computes TeX-code representing a _comp_inequiv_states-computation.
"""

import copy

from dfa import DFA


__all__ = ['minimize_dfa', 'has_unr_states', 'has_equiv_states', 'tex_min_table']


def minimize_dfa(dfa):
    """Returns a minimized copy of dfa.
    
    Implements Hopcroft's minimization algorithm.
    Returned DFA has depth set.
    """

    return _del_equiv_states(_del_unr_states(copy.deepcopy(dfa)))


# -----------------------------------------------------------


def _comp_unr_states(dfa):
    """Returns the set of all unreachable states in dfa.
    Uses breadth first search to compute this set."""

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
    """Returns whether dfa contains unreachable states."""

    return bool(_comp_unr_states(dfa))


def _del_unr_states(dfa):
    """Deletes all unreachable states from dfa."""

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


def _comp_inequiv_states(dfa):
    """Computes all inequivalent state pairs in dfa.
    
    Returns a dictionary m, mapping inequivalent state pairs (p,q) to the
    iteration i in which they were found.
    
    Returns a set M, containing all inequivalent state pairs.
    
    Returns depth, which is the number of iterations this algorithm needed
    for this dfa.
    
    Sets dfa.depth.
    """

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

        if not N:
            break
        else:
            i += 1

    # update informations

    dfa.depth = i
            
    return m, M, i


def has_equiv_states(dfa):
    """Returns whether dfa contains equivalent states.
    Sets dfa.depth."""

    m, M, depth = _comp_inequiv_states(dfa)

    for p in dfa.states:
        for q in dfa.states:
            if p != q and (p,q) not in M:
                return True

    return False


def _del_equiv_states(dfa):
    """Merges all equivalent state pairs of dfa.
    Sets dfa.depth. Sets dfa.planar to None."""

    m, M, depth = _comp_inequiv_states(dfa)

    # merge equivalent states
    
    eqStatePairs = [
        (p,q) 
        for p in dfa.states 
            for q in dfa.states 
               if (p,q) not in M and p != q
    ]

    while eqStatePairs:

        (p,q) = eqStatePairs.pop()

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
    """Returns TeX-representation of the computation _comp_inequiv_states(dfa).
    Sets dfa.depth."""

    m, M, depth = _comp_inequiv_states(dfa)

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
