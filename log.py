#!/usr/bin/env python

"""Bundles logging messages used throughout the program."""

# ----------------------------------------

def k_too_big():

    print('There are no complete DFAs with n < k.\nAbort.', flush=True)
    
def f_too_big():

    print('Since F is a subset of Q, f > n is not possible.\nAbort.', flush=True)
    
def invalid_p_options():

    print('Task DFA can not be planar if solution DFA is not planar.\nAbort.',
          flush=True)

def not_extendable():

    print('''DFAs with less than two alphabet symbols cannot be 
            extended with equivalent state pairs.\nAbort.''', flush=True)
        
def neg_value():
    
    print('Parameters k,n,f,dmin,dmax,e,u have to be zero or positive.\nAbort.',
          flush=True)

def creating_output_dir():

    print('Working directory does not exist, creating...', end='', flush=True)

# ----------------------------------------

def start(args):

    print("Working directory: '{}'.".format(args.out), flush=True)

def building_solution(args):

    planar = 'planar '     if args.ps          else ''
    method = 'enumeration' if args.b == 'enum' else 'randomization'

    print(
        'Building {}solution DFA with k={}, n={}, f={}, D in [{},{}] by {}..'.format(
            planar,
            args.k, args.n, args.f,
            args.dmin, args.dmax,
            method
        ), 
        end='', flush=True
    )
    
def enum_finished():

    print('''All DFAs with the specified parameters have been enumerated but 
             no matching DFA was found.''', flush=True)
    
def extending_solution(args):

    complete = 'complete ' if args.c  else ''
    planar   = 'planar '   if args.ps else ''
    
    print(
        'Extending to {}{}task DFA with e={}, u={}..'.format(
            complete, planar,
            args.e, args.u
        ),
        end='', flush=True
    )
    
def pygraph_bug(where):

    print('Error: IndexError bug in lib pygraph. ', end='', flush=True)

    if where == 'building':
    
        print('\nDiscarding current DFA, searching another...', end='', flush=True)
        
    else: # where == 'extending'
    
        print('Retrying to extend...', end='', flush=True)
    
def pygraph_bug_abort():

    print('Abort. Generated solution DFA will remain unused.', 
          end='', flush=True)
    
def saving():

    print('Saving task and solution..', end='', flush=True)

def no_saving():

    print('Results are not saved.', flush=True)

def cleaning():

    print('Cleaning working directory..', end='', flush=True)

# ----------------------------------------
    
def failed():

    print('failed.', flush=True)
    
def done():

    print('done.', flush=True)
