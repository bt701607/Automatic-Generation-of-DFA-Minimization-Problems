"""
module: pdf_from_dfa.py
author: Gregor Soennichsen


"""

import os
import platform
import pathlib

from dot2tex import dot2tex

import clean

from dfa          import DFA
from minimization import tex_min_table


__EXE_ENDING = ''

if platform.system() == 'Windows':
    EXE_ENDING = '.exe'


__TEMPLATE_TASK = r'''
\documentclass{{article}}
\usepackage[x11names, svgnames, rgb]{{xcolor}}
\usepackage[utf8]{{inputenc}}
\usepackage{{tikz}}
\usetikzlibrary{{snakes,arrows,shapes}}
\usetikzlibrary{{automata}}
\usepackage{{amsmath}}

\begin{{document}}

\subsection*{{Task DFA}}
{}

\end{{document}}
'''

__TEMPLATE_SOLUTION = r'''
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

\subsection*{{Remove unreachable states}}

Unreachable states: {}

\noindent DFA after removing all unreachable states:

{}

\subsection*{{Merge equivalent state pairs}}

States to merge:
\begin{{itemize}}
    {}
\end{{itemize}}
Minimization table:
\vspace{{1cm}}

{}

\vspace{{1cm}}
\noindent Minimal DFA after merging all equivalent states:

{}

\end{{document}}
'''


def dot_from_dfa(dfa):

    TEMPLATE_DFA = '''
digraph {{
    node [shape=circle]
{}
    node [shape=doublecircle]
{}
    node [color=white style=filled]
{}
}}'''

    TEMpPLATE_TRANSITION = '''    {} -> {} [label={}]
'''

    transitionsAsStr = ''

    for (q1,c),q2 in dfa.transitions:
        transitionsAsStr += TEMpPLATE_TRANSITION.format(q1, q2, c)

    statesAsStr = ''

    for q in dfa.states:
        if q not in dfa.accepting:
            statesAsStr += '''    {}\n'''.format(q)

    acceptingAsStr = ''

    for q in dfa.accepting:
        acceptingAsStr += '''    {}\n'''.format(q)

    return TEMPLATE_DFA.format(statesAsStr, acceptingAsStr, transitionsAsStr)


def tex_from_dfa(dfa):

    return dot2tex(dot_from_dfa(dfa), format='tikz', crop=True, program='dot', figonly=True)


def postprocess_tex(tex, minTable=None):
    ''' adds tikz automata library to TeX-code,
        to be able to display start states correctly'''

    lines = tex.split('\n')

    i = 0

    while i != len(lines):

        if '\\node (0)' in lines[i]:

            lines[i] = lines[i].replace('\\node', '\\node[initial] (0)')

        i += 1

    return '\n'.join(lines)
    
    
def next_task_path(outDir):

    counter = 0
    
    while True:
        path = outDir / 'task_{:03d}.tex'.format(counter)
        if not path.exists():
            return path
        counter += 1
    
    
def next_solution_path(outDir):

    counter = 0
    
    while True:
        path = outDir / 'solution_{:03d}.tex'.format(counter)
        if not path.exists():
            return path
        counter += 1


def save_task(taskDFA, outDir):

    if platform.system() == 'Windows':
        workingDir = pathlib.WindowsPath(outDir)
    else:
        workingDir = pathlib.PosixPath(outDir)

    path = next_task_path(outDir)

    path.write_text(
        __TEMPLATE_TASK.format(
            postprocess_tex(tex_from_dfa(taskDFA))
        )
    )

    os.popen(
        """pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape -output-directory='{}' '{}'"""
        .format(__EXE_ENDING, outDir, path)
    ).read()


def save_solution(solDFA, reachDFA, taskDFA, outDir):

    if platform.system() == 'Windows':
        workingDir = pathlib.WindowsPath(outDir)
    else:
        workingDir = pathlib.PosixPath(outDir)

    path = next_solution_path(outDir)

    path.write_text(
        __TEMPLATE_SOLUTION.format(
            '$' + ', '.join(taskDFA.unrStates) + '$',
            postprocess_tex(tex_from_dfa(reachDFA)),
            '\n'.join(['\item $' + ', '.join(class_) + '$' for class_ in reachDFA.eqClasses if len(class_) > 1]),
            tex_min_table(reachDFA),
            postprocess_tex(tex_from_dfa(solDFA))
        )
    )

    os.popen(
        """pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape -output-directory='{}' '{}'"""
        .format(__EXE_ENDING, outDir, path)
    ).read()



if __name__ == '__main__':

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

    #os.popen('''{}'''.format('output_dfa2tex.tex')).read()
    #os.popen('''{}'''.format('output_dfa2tex.pdf')).read()

    # clean up directory

    clean.basic()
