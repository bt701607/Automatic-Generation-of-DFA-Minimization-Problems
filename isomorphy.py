#!/usr/bin/env python

"""Specifies an isomorphy test for DFAs."""

from dfa import DFA


__all__ = ['isomorphy_test']


def isomorphy_test(dfa1, dfa2):
    """Returns whether dfa1 and dfa2 are isomorphic.
    
    This is done by trying to build a bijection bij between their state sets.
    If this test returns true for two minimal DFAs, then their language is the same.
    """

    if dfa1.n != dfa2.n or dfa1.f != dfa2.f or dfa1.k != dfa2.k:
        return False
        
    delta2 = dict(dfa2.transitions)

    bij = dict()
    
    bij[dfa1.start] = dfa2.start
    
    finished = [dfa1.start]
    observed = []
    
    actState = dfa1.start
    
    
    while True:
    
        # in each while-iter. we look at all outgoing transitions of actState
        
        for ((q1,c),p1) in dfa1.transitions:
        
            if q1 != actState:
                continue
                
            #         for a transition ((actState,     c),p1), we determine the 
            # corresponding transition ((bij[actState],c),p2) in dfa2
                
            p2 = delta2[(bij[actState], c)]

            # p1 and p2 should be mapped onto each other by bij
            # we do a case distinction, depending on the facts,
            # whether p1 and p2 are 'marked' by bij

            p1Marked = p1 in bij.keys()
            p2Marked = p2 in bij.values()
            
            if p1Marked and p2Marked:
            
                if bij[p1] != p2:
                    return False
                    
            elif not p1Marked and not p2Marked:
            
                bij[p1] = p2
                if p1 not in finished:
                    observed.append(p1)

            else:

                return False
    
        if not observed: # no more reachable states left to visit
            break
            
        actState = observed.pop()
        finished.append(actState)
    
    # in order to check whether dfa1 and dfa2 have the same language,
    # we have to ensure bij is also preserves the final states property
        
    for q in dfa1.final:
        if bij[q] not in dfa2.final:
            return False
        
    return True
