from DFA          import DFA
from minimize_dfa import tex_minimization_table

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


TEMPLATE_TASK = r'''
\documentclass{{article}}
\usepackage[x11names, svgnames, rgb]{{xcolor}}
\usepackage[utf8]{{inputenc}}
\usepackage{{tikz}}
\usetikzlibrary{{snakes,arrows,shapes}}
\usetikzlibrary{{automata}}
\usepackage{{amsmath}}

\begin{{document}}

\pagestyle{{empty}}
\enlargethispage{{100cm}}
{}

\end{{document}}
'''

TEMPLATE_SOLUTION = r'''
\documentclass{{article}}
\usepackage[x11names, svgnames, rgb]{{xcolor}}
\usepackage[utf8]{{inputenc}}
\usepackage{{tikz}}
\usetikzlibrary{{snakes,arrows,shapes}}
\usetikzlibrary{{automata}}
\usepackage{{amsmath}}
\usepackage{{MnSymbol}}

\newcommand{{\x}}{{$\blacksquare$}}

\begin{{document}}

\pagestyle{{empty}}
\enlargethispage{{100cm}}
{}

\vspace{{1cm}}

{}

\end{{document}}
'''


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

    return dot2tex(dot_from_dfa_own(dfa), format='tikz', crop=True, program='dot', figonly=True)


def postprocess_tex(tex, minimization_table=None):
    """ adds tikz automata library to TeX-code,
        to be able to display start states correctly"""

    lines = tex.split('\n')

    i = 0

    while i != len(lines):

        if "\\node (0)" in lines[i]:

            lines[i] = lines[i].replace("\\node", "\\node[initial] (0)")

        i += 1

    return '\n'.join(lines)


def save_task(task_dfa, identifier):

    fileName = 'output_task_' + identifier + ".tex"

    with open(fileName, "w") as outputFile:
        outputFile.write(
            TEMPLATE_TASK.format(postprocess_tex(tex_from_dfa(task_dfa)))
        )

    os.popen("pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape {}".format(EXE_ENDING, fileName)).read()


def save_solution(solution_dfa, reach_dfa, identifier):

    fileName = 'output_solution_' + identifier + ".tex"

    with open(fileName, "w") as outputFile:
        outputFile.write(
            TEMPLATE_SOLUTION.format(
                tex_minimization_table(reach_dfa),
                postprocess_tex(tex_from_dfa(solution_dfa))
            )
        )

    os.popen("pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape {}".format(EXE_ENDING, fileName)).read()



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

    #os.popen("""{}""".format("output_dfa2tex.tex")).read()
    #os.popen("""{}""".format("output_dfa2tex.pdf")).read()

    # clean up directory

    clean_code_dir_keep_results()
