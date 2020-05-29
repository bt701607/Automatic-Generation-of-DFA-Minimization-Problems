#!/usr/bin/env python

"""Handles this project's output.

dot_from_dfa
    Computes a representation of dfa in the DOT-format.

_postprocess_tex
    Improves TeX-code output by the dot2tex-library.

tex_from_dfa
    Computes a representation of dfa in the TEX-format.

_next_path_number
    Helps ensuring the correct numbering of output files.

save_exercise
    Saves a DFA minimization exercise.
"""

import os
import platform
import pathlib
import random

from dot2tex import dot2tex

from dfa          import DFA
from minimization import tex_min_table


__all__ = ['dot_from_dfa', 'tex_from_dfa', 'save_exercise']


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

List of unreachable states: {}\newline
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
    """Computes a representation of dfa in the DOT-format."""

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

    for i in range(len(lines)):

        if '\\node (0)' in lines[i]:
            lines[i] = lines[i].replace('\\node', '\\node[initial]')
            
        if 'node' in lines[i]:
            nPos     = lines[i].find('{') + 1
            lines[i] = lines[i][:nPos] + '$' + lines[i][nPos] + '$' + lines[i][nPos+1:]

    return '\n'.join(lines)


def tex_from_dfa(dfa):
    """Computes a representation of dfa in the TEX-format."""

    return _postprocess_tex(dot2tex(
        dot_from_dfa(dfa), 
        format='tikz', crop=True, program='dot', figonly=True
    ))
    
    
def _next_path_number(outDir):
    """Computes next suffix to the file path where the results are saved."""

    counter = 0
    
    while True:
    
        path1 = outDir / '{:03d}_task.dfa'.format(counter)
        path2 = outDir / '{:03d}_task.tex'.format(counter)
        path3 = outDir / '{:03d}_task.pdf'.format(counter)
        
        if not (path1.exists() or path2.exists() or path3.exists()):
            return counter
            
        counter += 1
        
        
def _shuffle_state_labels(solDFA, reachDFA, taskDFA):
    """Shuffles the state labels of solDFA, reachDFA, taskDFA."""

    newQ = taskDFA.states[1:].copy()
    random.shuffle(newQ)
    newQ = ['0'] + newQ
    
    toNew = dict(zip(taskDFA.states, newQ)).get
    
    for dfa in (solDFA, reachDFA, taskDFA):
    
       dfa.states = list(map(toNew, dfa.states))
       dfa.states.sort()
    
       dfa.final = list(map(toNew, dfa.final))
       dfa.final.sort()
    
       for i in range(len(dfa.transitions)):
       
           ((q1,c),q2) = dfa.transitions[i]
           
           dfa.transitions[i] = (toNew(q1), c), toNew(q2)
           
       if dfa.unrStates is not None:
        
           dfa.unrStates = list(map(toNew, dfa.unrStates))
           dfa.unrStates.sort()
           
       if dfa.eqClasses is not None:
        
           for i in range(len(dfa.eqClasses)):
               
               dfa.eqClasses[i] = list(map(toNew, dfa.eqClasses[i]))
               dfa.eqClasses[i].sort()
           
        
def save_exercise(solDFA, reachDFA, taskDFA, outDir, saveDFA, buildTEX, buildPDF):
    """Saves a DFA minimization problem and its solution.
    
    saveDFA  - toggle whether solDFA,taskDFA shall be printed to .dfa-files
    buildTEX - toggle whether task,solution shall be saved as .tex-files
    buildPDF - toggle whether task,solution shall be saved as .pdf-files
    
    Shuffles the state labels of solDFA, reachDFA, taskDFA.
    """
    
    _shuffle_state_labels(solDFA, reachDFA, taskDFA)
    
    number = _next_path_number(outDir)
    
    pathSol  = outDir / '{:03d}_solution.dfa'.format(number)
    pathTask = outDir / '{:03d}_task.dfa'.format(number)
    
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
        
        if not buildTEX:
            pathSol.with_suffix('.tex').unlink()
            pathTask.with_suffix('.tex').unlink()
