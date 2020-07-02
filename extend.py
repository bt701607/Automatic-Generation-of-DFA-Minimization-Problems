#!/usr/bin/env python

"""Specifies methods to add equivalent and unreachable states to a DFA.

DFANotExtendable
    Specifies an exception that arises, if a given DFA cannot be extended.

_new_state
    Creates a new state in a given DFA.

_add_unr_states
    Adds unreachable states to a given DFA.

_add_equiv_states
    Adds equivalent states to a given DFA.

extend_dfa
    Adds unreachable and equivalent states to a copy of the given DFA.
"""

import random
import copy

from itertools import product

from planarity import planarity_test


__all__ = ['DFANotExtendable', 'extend_dfa']


class DFANotExtendable(Exception):
    """Is raised, if a DFA cannot be extended."""
    
    pass


def _new_state(dfa, final):
    """Adds a new state to dfa and returns it."""

    newState = '0'

    while newState in dfa.states:
        newState = chr(ord(newState) + 1)

    dfa.states.append(newState)

    if final:
        dfa.final.append(newState)

    return newState


def _add_unr_states(dfa, nUnr=1, complete=True):
    """Adds nUnr random unreachable states to dfa.
    
    If complete=False, then some of the added unreachable states might not
    have outgoing transitions for all symbols.
    
    - assumes that dfa has no unreachable states
    - assumes dfa.eqClasses to be a list of equivalence classes of dfa,
      where each class is a list of states
    - sets dfa.unrStates
    """

    dfa.unrStates = []
    
    randSubset = lambda s: random.sample(s, random.randint(0, len(s)))

    for i in range(nUnr):

        newState = _new_state(dfa, random.randint(0,1)) # here we could enumerate

        # ingoing transitions
        
        for q, c in randSubset(list(product(dfa.unrStates, dfa.alphabet))):
    
            delta = dict(dfa.transitions)
        
            if (q,c) in delta:
                dfa.transitions.remove(((q, c), delta[(q,c)]))
                
            dfa.transitions.append(((q, c), newState))
            
        # outgoing transitions

        available = (q for q in dfa.states)
        
        symbols   = dfa.alphabet if complete else randSubset(dfa.alphabet)

        for c in symbols:
            dfa.transitions.append(((newState, c), next(available))) # here we could enumerate

        dfa.unrStates.append(newState)

    dfa.eqClasses.append(dfa.unrStates)

    # update informations

    dfa.n += nUnr
    dfa.f  = len(dfa.final)

    return dfa


def _add_equiv_states(dfa, nEquiv=1):
    """Adds nEquiv random equivalent states to dfa.
    
    - assumes that dfa is complete
    - assumes dfa.eqClasses to be a list of equivalence classes of dfa,
      where each class is a list of states
    
    Raises DFANotExtendable, if it is not possible to add nEquiv equivalent 
    states cannot be added.
    """
    
    def _in(q):
        
        cnt = len(tuple( t for t in dfa.transitions if t[1] == q ))
        
        return cnt + (1 if q == dfa.start else 0)

    
    if dfa.k == 0 or (dfa.k == 1 and (_in(dfa.start) - nEquiv) >= 0):
        raise DFANotExtendable()


    for i in range(nEquiv):

        # find a fitting state1 that shall be duplicated, create a new state
        # state2 and add it to state1's equivalence class

        duplicatableStates = tuple(filter(lambda q: _in(q) >= 2, dfa.states))

        state1 = random.choice(duplicatableStates) # here we could enumerate
        state2 = _new_state(dfa, state1 in dfa.final)

        state1eqClass = None

        for eqClass in dfa.eqClasses:
            if state1 in eqClass:
                eqClass.append(state2)
                state1eqClass = eqClass

        # for every outgoing transition ((state1,c),q2) of  state1
        # add an    outgoing transition ((state2,c),p)  for state2
        # where p is in the same eq. class as q2

        for (q1,c),q2 in dfa.transitions:
            if q1 == state1:

                # compute equiv.class to delta(state1, c)

                q2EqClass = None

                for eqClass in dfa.eqClasses:
                    if q2 in eqClass:
                        q2EqClass = eqClass
                        break

                # choose a p in [delta(state1,c)] as end point for delta(state2,c)

                dfa.transitions.append(((state2,c), random.choice(q2EqClass))) # here we could enumerate

        # take half the ingoing transitions from state1 and give them state2

        possible = tuple(t for t in dfa.transitions 
                                if t[1] in state1eqClass and _in(t[1]) >= 2)
    
        nonEmptySubset = lambda s: random.sample(s, random.randint(1, len(s))) # here we could enumerate

        for t in nonEmptySubset(possible):

            (q1,c),q2 = t
            dfa.transitions.append(((q1,c),state2))
            dfa.transitions.remove(t)
                
    # update informations

    dfa.n += nEquiv
    dfa.f  = len(dfa.final)
    
    return dfa


def extend_dfa(dfa, nEquiv, nUnr, planar=False, complete=True):
    """Returns copies of dfa with random added equivalent and unreachable states.
    
    - adds nEquiv equivalent states first, yielding reachDFA
    - adds nUnr unreachable states to reachDFA, yielding taskDFA
    
    Returns (reachDFA, taskDFA).
    Raises DFANotExtendable, if dfa cannot be extended.
    Raises PygraphIndexErrorBug, if the specified bug occurs.
    
    - tries to find a planar taskDFA dfa if planar=True
    - unreachable states have outgoing transitions for all symbols if
      complete=True
    """

    dfa.eqClasses = [[state] for state in dfa.states]

    while True:
    
        reachDFA = _add_equiv_states(copy.deepcopy(dfa),      nEquiv        )
        taskDFA  = _add_unr_states  (copy.deepcopy(reachDFA), nUnr, complete)
        
        if not planar or planarity_test(taskDFA):
            return reachDFA, taskDFA
