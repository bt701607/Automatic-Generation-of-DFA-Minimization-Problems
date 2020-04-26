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
        end=''
    )
    
def extending_solution(args):

    complete = 'complete ' if args.c else ''
    planar = 'planar ' if args.ps else ''
    
    print(
        'Extending DFA to {}{}task DFA with e={}, u={}..'.format(
            complete, planar,
            args.e, args.u
        ),
        end=''
    )
    
def saving():

    print('Saving task and solution..', end='')
    
def cleaning():

    print('Cleaning working directory..', end='')
    
def failed():

    print('failed.')
    
def done():

    print('done.')