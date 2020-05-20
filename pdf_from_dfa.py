from DFA          import DFA
from minimize_dfa import tex_minimization_table

import clean

from dot2tex import dot2tex

import os, platform, pathlib


EXE_ENDING = ''

if platform.system() == 'Windows':
    EXE_ENDING = '.exe'


TEMPLATE_TASK = r'''
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

    templateDFA = '''
digraph {{
    node [shape=circle]
{}
    node [shape=doublecircle]
{}
    node [color=white style=filled]
{}
}}'''

    templateTransition = '''    {} -> {} [label={}]
'''

    transitionsAsStr = ''

    for (q1,c),q2 in dfa.transitions:
        transitionsAsStr += templateTransition.format(q1, q2, c)

    statesAsStr = ''

    for q in dfa.states:
        if q not in dfa.accepting:
            statesAsStr += '''    {}\n'''.format(q)

    acceptingAsStr = ''

    for q in dfa.accepting:
        acceptingAsStr += '''    {}\n'''.format(q)

    return templateDFA.format(statesAsStr, acceptingAsStr, transitionsAsStr)


def tex_from_dfa(dfa):

    return dot2tex(dot_from_dfa(dfa), format='tikz', crop=True, program='dot', figonly=True)


def postprocess_tex(tex, minimization_table=None):
    ''' adds tikz automata library to TeX-code,
        to be able to display start states correctly'''

    lines = tex.split('\n')

    i = 0

    while i != len(lines):

        if '\\node (0)' in lines[i]:

            lines[i] = lines[i].replace('\\node', '\\node[initial] (0)')

        i += 1

    return '\n'.join(lines)
    
    
def next_task_path(workingDir):

    counter = 0
    
    while True:
        path = workingDir / 'task_{:03d}.tex'.format(counter)
        if not path.exists():
            return path
        counter += 1
    
    
def next_solution_path(workingDir):

    counter = 0
    
    while True:
        path = workingDir / 'solution_{:03d}.tex'.format(counter)
        if not path.exists():
            return path
        counter += 1


def save_task(taskDFA, workingDir):

    if platform.system() == 'Windows':
        workingDir = pathlib.WindowsPath(workingDir)
    else:
        workingDir = pathlib.PosixPath(workingDir)

    path = next_task_path(workingDir)

    path.write_text(
        TEMPLATE_TASK.format(
            postprocess_tex(tex_from_dfa(taskDFA))
        )
    )

    os.popen(
        """pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape -output-directory='{}' '{}'"""
        .format(EXE_ENDING, workingDir, path)
    ).read()


def save_solution(solDFA, reachDFA, taskDFA, workingDir):

    if platform.system() == 'Windows':
        workingDir = pathlib.WindowsPath(workingDir)
    else:
        workingDir = pathlib.PosixPath(workingDir)

    path = next_solution_path(workingDir)

    path.write_text(
        TEMPLATE_SOLUTION.format(
            '$' + ', '.join(taskDFA.unrStates) + '$',
            postprocess_tex(tex_from_dfa(reachDFA)),
            '\n'.join(['\item $' + ', '.join(class_) + '$' for class_ in reachDFA.eqClasses if len(class_) > 1]),
            tex_minimization_table(reachDFA),
            postprocess_tex(tex_from_dfa(solDFA))
        )
    )

    os.popen(
        """pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape -output-directory='{}' '{}'"""
        .format(EXE_ENDING, workingDir, path)
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
