"""
module: main.py
author: Gregor Soennichsen


"""

import pathlib
import argparse

import log
import clean

from dfa            import DFA
from dfa_build_rand import rand_min_dfa
from dfa_build_enum import next_min_dfa
from dfa_extend     import extend_dfa
from pdf_from_dfa   import save_task, save_solution


__DEFAULT_OUTPUT = pathlib.Path.cwd() / 'output'

__ARGUMENTS = (

    ('-k',    int,  2,      'alphabet size of generated DFAs (default: 2)'),
    ('-n',    int,  4,      'number of states of solution DFA (default: 4)'),
    ('-f',    int,  1,      'number of final states of solution DFA (default: 1)'),
    ('-dmin', int,  2,      'lower bound for D-value (default: 2)'),
    ('-dmax', int,  3,      'upper bound for D-value (default: 3)'),
    ('-ps',   bool, True,   'toggle whether solution DFA shall be planar (default: True)'),
    ('-pt',   bool, True,   'toggle whether task DFA shall be planar (default: True)'),

    ('-b',    str,  'enum', '''toggle whether solution DFA shall be build by 
            enumeration or randomization (default: enum)''', ('enum','random')),

    ('-e',    int,   2,     'number of distinct equivalent reachable state pairs in task DFA (default: 2)'),
    ('-u',    int,   1,     'number of unreachable states in task DFA (default: 1)'),
    ('-c',    bool,  True,  'toggle whether all unreachable states shall be complete (default: True)'),

    ('-p',    str,   __DEFAULT_OUTPUT, 'working directory; here results will be saved (default: {})'.format(__DEFAULT_OUTPUT))

)


def main():
    
    # check parameters

    parser = argparse.ArgumentParser(
        description='Generates a DFA minimization problem and its solution.',
        formatter_class=argparse.MetavarTypeHelpFormatter)

    for a in __ARGUMENTS:
        if len(a) == 4:
            parser.add_argument(a[0], type=a[1], default=a[2], help=a[3])
        else:
            parser.add_argument(a[0], type=a[1], default=a[2], help=a[3], choices=a[4])
    
    args = parser.parse_args()
    
    args.p = pathlib.Path(args.p)
    
    if not args.p.exists():
        log.creating_output_dir()
        args.p.mkdir()
        log.done()
    
    if not args.p.exists() or not args.p.is_dir():
        print("Error: '{}' does not specify a directory.".format(args.p))
        return
    
    if args.k < 2 and args.e > 0:
        print('''Error: DFAs with less than two alphabet symbols cannot be 
               extended with equivalent state pairs.''')
        return
        
    log.start(args)
    

    # construct solution dfa

    log.building_solution(args)

    if args.b == 'enum':
        solDFA = next_min_dfa(args.k, args.n, args.f, args.dmin, args.dmax,
                              args.ps, args.p)
        
        if solDFA == None:
            log.failed()
            print('''Error: All DFAs with the specified parameters have been 
                   enumerated. Generate respective random DFA instead (y/n)?''')
            
            if input() in ('y',''):
                args.b = 'random'
            else:
                return
        
    if args.b == 'random':
        solDFA = rand_min_dfa(args.k, args.n, args.f, args.dmin, args.dmax,
                              args.ps, args.p)
    
    log.done()


    # extend dfa
    
    log.extending_solution(args)

    reachDFA, taskDFA = extend_dfa(solDFA, args.e, args.u, args.pt, args.c)
    
    log.done()
    

    # generate graphical representation of solution and task dfa

    log.saving()
    
    save_task(taskDFA, args.p)
    save_solution(solDFA, reachDFA, taskDFA, args.p)
    
    log.done()
    

    # clean up directory
    
    log.cleaning()

    clean.basic(args.p)
    
    log.done()
    


if __name__ == '__main__':

    main()
