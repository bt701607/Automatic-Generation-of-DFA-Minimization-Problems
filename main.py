from DFA                   import DFA
from DFABuilderRandomized  import build_random_minimal_dfa
from DFABuilderEnumerating import build_next_minimal_dfa
from DFAExtender           import DFAExtender
from pdf_from_dfa          import pdf_from_dfa
from clean                 import clean_code_dir_keep_results


CONSTRUCT_RANDOM_MINIMAL_DFA = False

CONSTRUCT_ENUMERATED_MINIMAL_DFA = True


def main():

    # construct dfa

    orig_dfa = None
    
    if CONSTRUCT_ENUMERATED_MINIMAL_DFA:

        orig_dfa = build_next_minimal_dfa(
            alphabetSize = 2,
            numberOfStates = 5,
            numberOfAcceptingStates = 1,
            minMinmarkDepth = 2,
            maxMinmarkDepth = 3
        )

    elif CONSTRUCT_RANDOM_MINIMAL_DFA:

        orig_dfa = build_random_minimal_dfa(
            alphabetSize = 2,
            numberOfStates = 5,
            numberOfAcceptingStates = 1,
            minMinmarkDepth = 2,
            maxMinmarkDepth = 3
        )

    else:

        orig_dfa = DFA(
            ['a','b','c','d','e'],
            ['1','2','3','4','5'],
            [
                (('1','a'),'1'),
                (('1','b'),'2'),
                (('2','c'),'4'),
                (('5','d'),'1'),
                (('2','e'),'5')
            ],
            '1',
            ['4','5']
        )

        orig_dfa = DFA(
            ['0', '1'],
            ['AD', 'B', 'CE', 'G'],
            [
                (('AD','1'),'CE'),
                (('AD','0'),'G' ),
                
                (('B' ,'0'),'CE'),
                (('B' ,'1'),'CE'),
                
                (('CE','0'),'B' ),
                (('CE','1'),'AD'),
                
                (('G' ,'0'),'B' ),
                (('G' ,'1'),'CE'),
            ],
            'AD',
            ['CE']
        )


    # extend dfa

    task_dfa = DFAExtender(orig_dfa).duplicate(1).outgoing_only(1).dfa()


    # generate graphical representation of original and extended dfa

    pdf_from_dfa(orig_dfa, "1")
    pdf_from_dfa(task_dfa, "2")

    print(planarity_test_dfa(orig_dfa), planarity_test_dfa(task_dfa))

    # clean up directory

    clean_code_dir_keep_results()


if __name__ == "__main__":

    main()
