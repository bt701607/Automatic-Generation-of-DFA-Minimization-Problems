def start(args):

    print('Working directory: "{}".'.format(args.p), flush=True)

def building_solution(args):

    planar = 'planar ' if args.ps else ''
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
    
def extending_solution(args):

    complete = 'complete ' if args.c else ''
    planar = 'planar ' if args.ps else ''
    
    print(
        'Extending DFA to {}{}task DFA with e={}, u={}..'.format(
            complete, planar,
            args.e, args.u
        ),
        end='', flush=True
    )
    
def saving():

    print('Saving task and solution..', end='', flush=True)
    
def cleaning():

    print('Cleaning working directory..', end='', flush=True)
    
def failed():

    print('failed.', flush=True)
    
def done():

    print('done.', flush=True)