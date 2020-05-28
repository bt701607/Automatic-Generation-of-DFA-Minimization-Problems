"""
module: pdf_from_dfa.py
author: Gregor Soennichsen


"""

import os
import platform
import pathlib

from dot2tex import dot2tex

from dfa          import DFA
from minimization import tex_min_table


_EXE_ENDING = ''

if platform.system() == 'Windows':
    _EXE_ENDING = '.exe'

_TEX_HEADER = r'''
\documentclass{{article}}
\usepackage[x11names, svgnames, rgb]{{xcolor}}
\usepackage[utf8]{{inputenc}}
\usepackage{{tikz}}
\usetikzlibrary{{snakes,arrows,shapes}}
\usetikzlibrary{{automata}}
\usepackage{{amsmath}}
\usepackage{{MnSymbol}}

\newcommand{{\x}}{{$\blacksquare$}}
'''

_TEMPLATE_TASK = _TEX_HEADER + r'''
\begin{{document}}

\subsection*{{Task DFA}}
{}

\end{{document}}
'''

_TEMPLATE_SOLUTION = _TEX_HEADER + r'''
\begin{{document}}

\subsection*{{Remove unreachable states}}

List of unreachable states: {}
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

    TEMPLATE_DOT_DFA = '''
        digraph {{
            node [shape=circle]
            {}
            node [shape=doublecircle]
            {}
            node [color=white style=filled]
            {}
        }}
    '''

    stToStr = lambda q: '{}\n'.format(q)
    trToStr = lambda t: '{} -> {} [label={}]\n'.format(t[0][0], t[1], t[0][1])

    nonFinalStates = (q for q in dfa.states if q not in dfa.final)

    nonFinalAsStr = ''.join(map(stToStr, nonFinalStates))
    finalAsStr    = ''.join(map(stToStr, dfa.final))
    deltaAsStr    = ''.join(map(trToStr, dfa.transitions))

    return TEMPLATE_DOT_DFA.format(nonFinalAsStr, finalAsStr, deltaAsStr)


def _postprocess_tex(texCode):
    """Returns code such that start states are marked and states/symbols are
    set in math mode."""

    lines = texCode.split('\n')

    for line in lines:

        if '\\node (0)' in line:
            line = line.replace('\\node', '\\node[initial]')
            
        if 'node' in line:
            nPos = line.find('{') + 1
            line = line[:nPos] + '$' + line[nPos] + '$' + line[nPos+1:]

    return '\n'.join(lines)


def tex_from_dfa(dfa):

    return _postprocess_tex(dot2tex(
        dot_from_dfa(dfa), 
        format='tikz', crop=True, program='dot', figonly=True
    ))
    
    
def next_path_number(outDir):

    counter = 0
    
    while True:
    
        path1 = outDir / 'task_{:03d}.dfa'.format(counter)
        path2 = outDir / 'task_{:03d}.tex'.format(counter)
        path3 = outDir / 'task_{:03d}.pdf'.format(counter)
        
        if not (path1.exists() or path2.exists() or path3.exists()):
            return counter
            
        counter += 1
        
        
def save_exercise(solDFA, reachDFA, taskDFA, outDir, saveDFA, buildTEX, buildPDF):
    
    number = next_path_number(outDir)
    
    pathSol  = outDir / 'solution_{:03d}.dfa'.format(number)
    pathTask = outDir / 'task_{:03d}.dfa'.format(number)
    
    if saveDFA:
        pathSol.with_suffix('.dfa').write_text(str(solDFA))
        pathTask.with_suffix('.dfa').write_text(str(taskDFA))
    
    if buildPDF:
    
        pathSol.with_suffix('.tex').write_text(
            _TEMPLATE_SOLUTION.format(
                '$' + ', '.join(taskDFA.unrStates) + '$',
                tex_from_dfa(reachDFA),
                '\n'.join(['	\item $' + ', '.join(class_) + '$' for class_ in reachDFA.eqClasses if len(class_) > 1]),
                tex_min_table(reachDFA),
                tex_from_dfa(solDFA)
            )
        )
        pathTask.with_suffix('.tex').write_text(
            _TEMPLATE_TASK.format(tex_from_dfa(taskDFA))
        )
    
        os.popen(
            """pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape -output-directory='{}' '{}'"""
            .format(_EXE_ENDING, outDir, pathSol.with_suffix('.tex'))
        ).read()
        os.popen(
            """pdflatex{} -synctex=1 -interaction=nonstopmode -shell-escape -output-directory='{}' '{}'"""
            .format(_EXE_ENDING, outDir, pathTask.with_suffix('.tex'))
        ).read()
        
        if not buildTex:
            pathSol.with_suffix('.tex').unlink()
            pathTask.with_suffix('.tex').unlink()
