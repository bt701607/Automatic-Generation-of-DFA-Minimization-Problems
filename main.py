from DFA                   import DFA
from DFABuilderRandomized  import build_random_minimal_dfa
from DFABuilderEnumerating import build_next_minimal_dfa
from DFAExtender           import extend_minimal_complete_dfa
from pdf_from_dfa          import save_task, save_solution

import clean
import log

import pathlib
import argparse


def main():

    parser = argparse.ArgumentParser(description='Generates a DFA minimization problem and its solution.', formatter_class=argparse.MetavarTypeHelpFormatter)

    parser.add_argument('-k', type=int, default=2, help='alphabet size of generated DFAs (default: 2)')
    parser.add_argument('-n', type=int, default=4, help='number of states of solution DFA (default: 4)')
    parser.add_argument('-f', type=int, default=1, help='number of final states of solution DFA (default: 1)')
    parser.add_argument('-dmin', type=int, default=2, help='lower bound for D-value (default: 2)')
    parser.add_argument('-dmax', type=int, default=3, help='upper bound for D-value (default: 3)')
    parser.add_argument('-ps', type=bool, default=True, help='toggle whether solution DFA shall be planar (default: True)')
    parser.add_argument('-pt', type=bool, default=True, help='toggle whether task DFA shall be planar (default: True)')

    parser.add_argument('-b', type=str, choices=['enum','random'], default='enum', help='toggle whether solution DFA shall be build by enumeration or randomization (default: enum)')

    parser.add_argument('-e', type=int, default=2, help='number of distinct equivalent reachable state pairs in task DFA (default: 2)')
    parser.add_argument('-u', type=int, default=1, help='number of unreachable states in task DFA (default: 1)')
    parser.add_argument('-c', type=bool, default=True, help='toggle whether all unreachable states shall be complete (default: True)')

    parser.add_argument('-p', type=str, default=pathlib.Path.cwd(), help='working directory; here results will be saved (default: {})'.format(pathlib.Path.cwd()))
    
    
    # check paramters

    args = parser.parse_args()
    
    args.p = pathlib.Path(args.p)
    
    if not args.p.exists():
        print("Error: Path '{}' does not exist.".format(args.p))
        return
    
    if not args.p.exists() or not args.p.is_dir():
        print("Error: '{}' does not specify a directory.".format(args.p))
        return
    
    if args.k < 2 and args.e > 0:
        print('Error: DFAs with less than two alphabet symbols cannot be extended with equivalent state pairs.')
        return
        
    log.start(args)
    

    # construct solution dfa

    log.building_solution(args)

    if args.b == 'enum':
        solDFA = build_next_minimal_dfa(args.k, args.n, args.f, args.dmin, args.dmax, args.ps, args.p)
        
        if solDFA == None:
            log.failed()
            print('Error: All DFAs with the specified parameters have been enumerated. Generate respective random DFA instead (y/n)?')
            
            if input() in ('y',''):
                args.b = 'random'
            else:
                return
        
    if args.b == 'random':
        solDFA = build_random_minimal_dfa(args.k, args.n, args.f, args.dmin, args.dmax, args.ps, args.p)
    
    log.done()


    # extend dfa
    
    log.extending_solution(args)

    reachDFA, taskDFA = extend_minimal_complete_dfa(solDFA, args.e, args.u, args.pt, args.c)
    
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
