"""
module: dfa_extend.py
author: Gregor Soennichsen


"""

import random
import copy

from planarity import planarity_test


def __new_state(dfa, final):
    # Helper method for creating new states.

    newState = '0'

    while newState in dfa.states:
        newState = chr(ord(newState) + 1)

    dfa.states.append(newState)

    if final:
        dfa.final.append(newState)

    return newState


# -------------------------------------------------------------------


# dfa is expected to have no unreachable states
def __add_unr_states(dfa, nUnr=1, complete=True):

    dfa = copy.deepcopy(dfa)

    dfa.unrStates = []

    for i in range(nUnr):

        newState = __new_state(dfa, random.randint(0,1)) # -------------------------------- here we can enumerate

        available = (q for q in dfa.states if q not in dfa.unrStates)

        symbols = None
        
        if complete:
            symbols = dfa.alphabet
        else:
            symbols = random.sample(dfa.alphabet, random.randint(dfa.k))

        for c in dfa.alphabet:
            dfa.transitions.append(((newState, c), next(available))) # -------------------------------- here we can enumerate

        dfa.unrStates.append(newState)

    dfa.eqClasses.append(dfa.unrStates)

    # update informations

    dfa.n = len(dfa.states)
    dfa.f = len(dfa.final)

    return dfa


# dfa is expected to be complete
def __add_dupl_states(dfa, nDupl=1):

    if dfa.k <= 1 and nDupl > 0:
        print('DFA cannot be extended with equivalent state pairs.')
        return
        
    dfa = copy.deepcopy(dfa)

    for i in range(nDupl):

        # find a fitting state1, that shall be duplicated, and update eq.classes

        isDuplicatable     = lambda q: len(tuple( t for t in dfa.transitions if t[1] == q )) >= 2
        duplicatableStates = tuple(filter(isDuplicatable, dfa.states))

        state1 = random.choice(duplicatableStates) # -------------------------------- here we can enumerate
        state2 = __new_state(dfa, state1 in dfa.final)

        for equivClass in dfa.eqClasses:
            if state1 in equivClass:
                equivClass.append(state2)

        # split ingoing transitions

        inTransitions = tuple(t for t in dfa.transitions if t[1] == state1)

        for i in range(len(inTransitions) // 2): # -------------------------------- here we can enumerate

            (q1,c),q2 = t = inTransitions[i]
            dfa.transitions.append(((q1,c),state2))
            dfa.transitions.remove(t)

        # split/duplicate outgoing transitions

        for (q1,c),q2 in dfa.transitions:
            if q1 == state1:

                # compute equiv.class to delta(state1, c)

                q2EquivClass = None

                for equivClass in dfa.eqClasses:
                    if q2 in equivClass:
                        q2EquivClass = equivClass
                        break

                # choose p of [delta(state1,c)] as end point for delta(state2,c)

                dfa.transitions.append(((state2,c), random.choice(q2EquivClass))) # -------------------------------- here we can enumerate

    # update informations

    dfa.n = len(dfa.states)
    dfa.f = len(dfa.final)
    
    return dfa


def extend_dfa(dfa, nDupl, nUnr, planar=False, complete=True):

    dfa.eqClasses = [[state] for state in dfa.states]

    while True:

        reachDFA = __add_dupl_states(dfa, nDupl)
        taskDFA  = __add_unr_states(reachDFA, nUnr, complete)
        
        if not planar or planarity_test(taskDFA):
            return reachDFA, taskDFA
            

if __name__ == '__main__':
    pass
