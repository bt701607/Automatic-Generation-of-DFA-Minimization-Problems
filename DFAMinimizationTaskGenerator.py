from DFA          import DFA
from DFABuilder   import DFABuilder
from DFALanguagePreservingExtender import DFALanguagePreservingExtender
from tex_from_dfa import dot_from_dfa, tex_from_dfa

from copy import deepcopy

import os


FILE_NAME       = "output"

USE_DOT2TEX     = True
USE_DFA_BUILDER = False

EXE_ENDING	  = ".exe" # 


# construct dfa

test_dfa = None

if USE_DFA_BUILDER:

    test_dfa = DFABuilder().mix(1,1,1,3).dfa()

else:

    test_dfa = DFA(
        ['a','b','c','d','e'],
        [1,2,3,4,5],
        [
            ((1,1),'a'),
            ((1,2),'b'),
            ((2,4),'c'),
            ((5,1),'d'),
            ((2,5),'e')
        ],
        1,
        [4,5]
    )

    test_dfa = DFA(
        ['0', '1'],
        ['AD', 'B', 'CE', 'G'],
        [
            (('AD','CE'),'1'),
            (('AD','G' ),'0'),
            
            (('B' ,'CE'),'0'),
            (('B' ,'CE'),'1'),
            
            (('CE','B' ),'0'),
            (('CE','AD'),'1'),
            
            (('G' ,'B' ),'0'),
            (('G' ,'CE'),'1'),
        ],
        'AD',
        ['CE']
    )


# extend dfa

orig_dfa = deepcopy(test_dfa)

test_dfa = DFALanguagePreservingExtender(dfa = test_dfa).duplicate(3).dfa()


# generate and view dfa

def tex_to_pdf(dfa, suffix):

    with open(FILE_NAME + suffix + ".tex", "w") as outputFile:
        outputFile.write(tex_from_dfa(dfa))
        
    os.system("pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape {}".format(EXE_ENDING, FILE_NAME + suffix + ".tex"))
    
    os.system("{}".format(FILE_NAME + suffix + ".pdf"))

if USE_DOT2TEX:

    tex_to_pdf(orig_dfa, "1")
    tex_to_pdf(test_dfa, "2")

else:

    with open(FILE_NAME + ".dot", "w") as outputFile:
        outputFile.write(dot_from_dfa(test_dfa))

    os.system("dot -Tpng {fileName}.dot > {fileName}.png".format(fileName=FILE_NAME))
    os.system("{}".format(FILE_NAME + ".png"))
