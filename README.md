# Generation-of-DFA-Minimization-Problems

Dependencies:

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


# TODO

* proper tests

So far: isomorphy

Work in progress: minimization, pdf_from_dfa, planarity, DB_Enumeration, DB_Minimal, main

* proper rendering (http://www.graphdrawing.org/books.html, http://gdea.informatik.uni-koeln.de/view/subjects/)


# Optimization ideas

* Enumerate all combinations of k elements from n

https://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n

https://stackoverflow.com/questions/1851134/generate-all-binary-strings-of-length-n-with-k-bits-set

https://www.geeksforgeeks.org/find-combinations-k-bit-numbers-n-bits-set-1-n-k-sorted-order/

* In enumeration increments make interpretation of transitions progress cleverer, such that the unreachable DFAs are more distributed.

* Use integer instead of integer-lists for enumeration.

* Profile the Code and optimize thus.
