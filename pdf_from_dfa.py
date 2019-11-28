from DFA import DFA

from graphviz import Digraph
from dot2tex  import dot2tex

import os
import platform


FILE_NAME  = "output"
EXE_ENDING = ""

# no ending for e.g. Linux, MacOS
if platform.system() == "Windows":
    EXE_ENDING = ".exe"


def dot_from_dfa(dfa):
    """description of function"""

    graph = Digraph()

    graph.attr('node', shape='doublecircle')
    for q in dfa.accepting:
        graph.node(str(q))
        
    graph.attr('node', shape='circle')
    for q in dfa.states:
        if q not in dfa.accepting:
            graph.node(str(q))
    
    graph.attr('node', style='filled', color='white')
    graph.node("")

            
    graph.edge("", str(dfa.start))

    for (q1,c),q2 in dfa.transitions:
        graph.edge(str(q1), str(q2), label=str(c))

    return graph.source


def tex_from_dfa(dfa):
    """description of function"""

    return dot2tex(dot_from_dfa(dfa), format='tikz', crop=True)
	

def pdf_from_dfa(dfa, identifier):

    with open(FILE_NAME + identifier + ".tex", "w") as outputFile:
        outputFile.write(tex_from_dfa(dfa))
        
    os.popen("pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape {}".format(EXE_ENDING, FILE_NAME + identifier + ".tex")).read()



if __name__ == "__main__":

    fileName = "output"

    testDFA = DFA(
        (1,2,3,4,5),
        (
            ((1,1),'a'),
            ((1,2),'b'),
            ((2,4),'c'),
            ((5,1),'d'),
            ((2,5),'e')
        ),
        1,
        (4,5)
    )

    with open(fileName + ".tex", "w") as outputFile:

        outputFile.write(tex_from_dfa(testDFA))

    os.popen("""pdflatex.exe -synctex=1 -interaction=nonstopmode -shell-escape {}""".format(fileName + ".tex")).read()
    
    os.popen("""{}""".format(fileName + ".tex")).read()
    os.popen("""{}""".format(fileName + ".pdf")).read()
