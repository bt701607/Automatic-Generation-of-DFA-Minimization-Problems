from planarity_test_dfa import planarity_test_dfa

import random
import copy



def __new_state(dfa, is_accepting):
    # Helper method for creating new states.

    newState = '0'

    while newState in dfa.states:
        newState = chr(ord(newState) + 1)

    dfa.states.append(newState)

    if is_accepting:
        dfa.accepting.append(newState)

    return newState


# -------------------------------------------------------------------


# dfa is expected to have no unreachable states
def __add_unreachable_states(dfa, numberOfUnreachableStates=1, complete=True):

    dfa = copy.deepcopy(dfa)

    dfa.unrStates = []

    for i in range(numberOfUnreachableStates):

        newState = __new_state(dfa, random.randint(0,1)) # -------------------------------- here we can enumerate

        availableEndPoints = (q for q in dfa.states if q not in dfa.unrStates)

        symbols = None
        
        if complete:
            symbols = dfa.alphabet
        else:
            symbols = random.sample(dfa.alphabet, random.randint(dfa.alphabetSize))

        for c in dfa.alphabet:
            dfa.transitions.append(((newState, c), next(availableEndPoints))) # -------------------------------- here we can enumerate

        dfa.unrStates.append(newState)

    dfa.eqClasses.append(dfa.unrStates)

    # update informations

    dfa.numberOfStates          = len(dfa.states)
    dfa.numberOfAcceptingStates = len(dfa.accepting)

    return dfa


# dfa is expected to be complete
def __add_duplicate_states(dfa, numberOfDuplicateStates=1):

    if dfa.alphabetSize <= 1 and numberOfDuplicateStates > 0:
        print('DFA cannot be extended with equivalent state pairs.')
        return
        
    dfa = copy.deepcopy(dfa)

    for i in range(numberOfDuplicateStates):

        # find a fitting state1, that shall be duplicated, and update eq.classes

        isDuplicatable     = lambda q: len(tuple( t for t in dfa.transitions if t[1] == q )) >= 2
        duplicatableStates = tuple(filter(isDuplicatable, dfa.states))

        state1 = random.choice(duplicatableStates) # -------------------------------- here we can enumerate
        state2 = __new_state(dfa, state1 in dfa.accepting)

        theirEquivClass = None

        for equivClass in dfa.eqClasses:
            if state1 in equivClass:
                equivClass.append(state2)
                theirEquivClass = equivClass

        # split ingoing transitions

        ingoingTransitions = tuple(t for t in dfa.transitions if t[1] == state1)

        for i in range(len(ingoingTransitions) // 2): # -------------------------------- here we can enumerate

            (q1,c),q2 = t = ingoingTransitions[i]
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

    dfa.numberOfStates          = len(dfa.states)
    dfa.numberOfAcceptingStates = len(dfa.accepting)
    
    return dfa


def extend_minimal_complete_dfa(dfa, numberOfDuplicateStates, numberOfUnreachableStates, planar=False, complete=True):

    dfa.eqClasses = [[state] for state in dfa.states]

    while True:

        reachDFA = __add_duplicate_states(dfa, numberOfDuplicateStates)
        taskDFA  = __add_unreachable_states(reachDFA, numberOfUnreachableStates, complete)

        if not planar or planarity_test_dfa(taskDFA):
            return reachDFA, taskDFA
    
        


