from DFA                   import DFA
from DFABuilderRandomized  import build_random_minimal_dfa
from DFABuilderEnumerating import build_next_minimal_dfa
from DFAExtender           import extend_minimal_complete_dfa
from pdf_from_dfa          import save_task, save_solution

from clean import clean_code_dir_keep_results

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

    args = parser.parse_args()

    # construct dfa

    if args.b == 'enum':

        solution_dfa = build_next_minimal_dfa(args.k, args.n, args.f, args.dmin, args.dmax, args.ps)

    else: # args.b == 'random'

        solution_dfa = build_random_minimal_dfa(args.k, args.n, args.f, args.dmin, args.dmax, args.ps)

    # extend dfa

    task_dfa, reach_dfa, duplicate_states, unreachable_states, equiv_classes = extend_minimal_complete_dfa(solution_dfa, args.e, args.u)

    print(solution_dfa)
    print(reach_dfa)
    print(task_dfa)

    # generate graphical representation of solution and task dfa

    save_task(task_dfa, '0')
    save_solution(solution_dfa, reach_dfa, '0')

    # clean up directory

    clean_code_dir_keep_results()


if __name__ == "__main__":

    main()
