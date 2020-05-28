"""
module: log.py
author: Gregor Soennichsen


"""

def creating_output_dir():

    print("Working directory does not exist, creating...", end='', flush=True)

def not_extendable():

    print('''DFAs with less than two alphabet symbols cannot be 
            extended with equivalent state pairs.\nAbort.''', flush=True)

def start(args):

    print("Working directory: '{}'.".format(args.p), flush=True)

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
             no matching DFA was found.''', end='', flush=True)
    
def extending_solution(args):

    complete = 'complete ' if args.c  else ''
    planar   = 'planar '   if args.ps else ''
    
    print(
        'Extending DFA to {}{}task DFA with e={}, u={}..'.format(
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
    
def failed():

    print('failed.', flush=True)
    
def done():

    print('done.', flush=True)
