from DFA import DFA

from clean import clean_code_dir_keep_results

from graphviz import Digraph
from dot2tex  import dot2tex

import os
import platform


FILE_NAME  = "output"
EXE_ENDING = ""

# no ending for e.g. Linux, MacOS
if platform.system() == "Windows":
    EXE_ENDING = ".exe"


def dot_from_dfa_graphviz(dfa):

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

    print(graph.source)

    return graph.source


def dot_from_dfa_own(dfa):

    templateDFA = """
digraph {{
    node [shape=circle]
{}
    node [shape=doublecircle]
{}
    node [color=white style=filled]
{}
}}"""

    templateTransition = """    {} -> {} [label={}]
"""

    transitionsAsStr = ""

    for (q1,c),q2 in dfa.transitions:
        transitionsAsStr += templateTransition.format(q1, q2, c)

    statesAsStr = ""

    for q in dfa.states:
        if q not in dfa.accepting:
            statesAsStr += """    {}\n""".format(q)

    acceptingAsStr = ""

    for q in dfa.accepting:
        acceptingAsStr += """    {}\n""".format(q)

    return templateDFA.format(statesAsStr, acceptingAsStr, transitionsAsStr)


def tex_from_dfa(dfa):

    return dot2tex(dot_from_dfa_own(dfa), format='tikz', crop=True, program='dot')


def postprocess_tex(tex):
    """ adds tikz automata library to TeX-code,
        to be able to display start states correctly"""

    lines = tex.split('\n')

    i = 0

    while i != len(lines):

        if lines[i].startswith("\\usetikzlibrary"):

            lines.insert(i+1, "\\usetikzlibrary{automata}")
            i += 1

        if "\\node (0)" in lines[i]:

            lines[i] = lines[i].replace("\\node", "\\node[initial] (0)")

        i += 1

    return '\n'.join(lines)


def pdf_from_dfa(dfa, identifier):

    with open(FILE_NAME + identifier + ".tex", "w") as outputFile:
        outputFile.write(postprocess_tex(tex_from_dfa(dfa)))

    os.popen("pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape {}".format(EXE_ENDING, FILE_NAME + identifier + ".tex")).read()



if __name__ == "__main__":

    testDFA = DFA(
        ['a', 'b'],
        ['0', '1', '2', '3', '4', '5', '6'],
        [
                (('0', 'b'), '1'),
                (('2', 'a'), '0'),
                (('2', 'b'), '3'),
                (('3', 'a'), '0'),
                (('3', 'b'), '2'),
                (('1', 'b'), '4'),
                (('4', 'a'), '0'),
                (('4', 'b'), '3'),
                (('0', 'a'), '5'),
                (('1', 'a'), '5'),
                (('5', 'b'), '1'),
                (('5', 'a'), '5'),
                (('6', 'a'), '0'),
                (('6', 'b'), '1'),
        ],
        '0',
        ['3', '6']
    )

    pdf_from_dfa(testDFA, "_dfa2tex")

    #os.popen("""{}""".format("output_dfa2tex.tex")).read()
    #os.popen("""{}""".format("output_dfa2tex.pdf")).read()

    # clean up directory

    clean_code_dir_keep_results()
