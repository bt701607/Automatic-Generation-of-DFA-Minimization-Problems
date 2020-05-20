# Generation-of-DFA-Minimization-Problems

Dependencies:

* python >=3.4
* PGF/TikZ 2.0 or later (e.g. https://www.tug.org/texlive/)
* Graphviz (https://graphviz.org/download/)
Note for the "Stable 2.38 Windows install packages": The installer does not automatically add "C:\Program Files (x86)\Graphviz2.38\bin" (or similar) to the PATH environment variable, this must thus be done manually.

* pyparsing (pip install pyparsing)

Profiling needs:

* vprof (pip install vprof)

The dot2tex library has been obtained from https://github.com/kjellmf/dot2tex .
It is included here, to be able to apply a fix.

The pygraph library has been obtained from the pip repositories.
It is included here, to be able to make it python3 compatible.

# Usage

To generate a DFA minimization problem, use
```bash
python main.py
```
Note that you have to use 'python3' instead of 'python' if you have both Python 2 and 3 installed.

The output consists of the task DFA and the minimal solution DFA, both given as TEX and PDF. There are a lot of parameters you can use to influence the nature of the output problem and how it is generated - see 'python main.py -h' for a list.

The related bachelor-thesis provides the theoretical background and explains the generator in detail.
