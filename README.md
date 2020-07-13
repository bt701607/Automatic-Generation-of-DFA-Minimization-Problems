# Automatic Generation of DFA Minimization Problems

Dependencies:

* python >=3.4
* pdflatex, as provided by PGF/TikZ 2.0 or later (e.g. https://www.tug.org/texlive/) 
Only if you want to output DFAs as PDF using the -pdf option.
* Graphviz (https://graphviz.org/download/)
Must be added to the PATH environment variable. This should happen automatically on Linux and MacOS, whereas on Windows this has to be done manually.

* pyparsing (pip install pyparsing)

The dot2tex library has been obtained from https://github.com/kjellmf/dot2tex .
It is included here, to be able to apply a fix.

The pygraph library has been obtained from the pip repositories.
It is included here, to be able to make it python3 compatible.

# Usage

To generate a DFA minimization problem, use
```bash
python main.py
```
Note that you possibly have to use 'python3' instead of 'python'.

The output consists of the task DFA and the minimal solution DFA, both given as TEX and PDF. There are a lot of parameters you can use to influence the nature of the output problem and how it is generated - see 'python main.py -h' for a list.

The related bachelor-thesis provides the theoretical background and explains the generator in detail.
