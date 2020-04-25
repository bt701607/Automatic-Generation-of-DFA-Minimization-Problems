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
def __add_unreachable_states(dfa, equiv_classes, numberOfUnreachableStates=1):

    unreachable_states = []

    for i in range(numberOfUnreachableStates):

        newState = __new_state(dfa, random.randint(0,1)) # -------------------------------- here we can enumerate

        availableEndPoints = (q for q in dfa.states if q not in unreachable_states)

        for c in dfa.alphabet:
            dfa.transitions.append(((newState, c), next(availableEndPoints))) # -------------------------------- here we can enumerate

        unreachable_states.append(newState)

    equiv_classes.append(unreachable_states)

    # update informations

    dfa.numberOfStates          = len(dfa.states)
    dfa.numberOfAcceptingStates = len(dfa.accepting)

    return unreachable_states


# dfa is expected to be complete
def __add_duplicate_states(dfa, equiv_classes, numberOfDuplicateStates=1):

    duplicate_states = []

    for i in range(numberOfDuplicateStates):

        # find a fitting state1, that shall be duplicated, and update eq.classes

        isDuplicatable     = lambda q: len(tuple( t for t in dfa.transitions if t[1] == q )) >= 2
        duplicatableStates = tuple(filter(isDuplicatable, dfa.states))

        if not duplicatableStates:
            print("No state with >= 2 ingoing transitions.")
            return duplicate_states

        state1 = random.choice(duplicatableStates) # -------------------------------- here we can enumerate
        state2 = __new_state(dfa, state1 in dfa.accepting)

        print("Duplicating {} by creating {}.".format(state1,state2))

        theirEquivClass = None

        for equivClass in equiv_classes:
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

                for equivClass in equiv_classes:
                    if q2 in equivClass:
                        q2EquivClass = equivClass
                        break

                # choose p of [delta(state1,c)] as end point for delta(state2,c)

                dfa.transitions.append(((state2,c), random.choice(q2EquivClass))) # -------------------------------- here we can enumerate

        duplicate_states.append(state2)

    # update informations

    dfa.numberOfStates          = len(dfa.states)
    dfa.numberOfAcceptingStates = len(dfa.accepting)

    return duplicate_states


def extend_minimal_complete_dfa(dfa, numberOfDuplicateStates, numberOfUnreachableStates):

    while True:

        taskDFA = copy.deepcopy(dfa)

        equiv_classes = [[state] for state in dfa.states]

        duplicate_states   = __add_duplicate_states  (taskDFA, equiv_classes, numberOfDuplicateStates  )

        reachDFA = copy.deepcopy(taskDFA)

        unreachable_states = __add_unreachable_states(taskDFA, equiv_classes, numberOfUnreachableStates)

        if planarity_test_dfa(taskDFA):

            return taskDFA, reachDFA, duplicate_states, unreachable_states, equiv_classes


