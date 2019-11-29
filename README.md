# Generation-of-DFA-Minimization-Problems

Dependencies:

* PGF/TikZ 2.0 or later (e.g. https://www.tug.org/texlive/)
* Graphviz (https://graphviz.org/download/)
* preview (http://www.ctan.org/tex-archive/help/Catalogue/entries/preview.html)

* graphviz (pip install graphviz)
* pyparsing (pip install pyparsing)

Profiling needs:

* vprof (pip install vprof)

The dot2tex library has been obtained from https://github.com/kjellmf/dot2tex .
It is included here, to be able to apply a fix.

The pygraph library has been obtained from the pip repositories.
It is included here, to be able to make it python3 compatible.


# TODO

* put programmed concepts into writing
* make DFAExtender enumerating too, save progress in MinimalDFAs table
* ensure that there are dupl. states possible when building min. dfa (a state is duplicatable, iff it has 0 (unreachable dupl.) or more than 2 ingoing transitions).

This automatically ensured, since the generated DFAs are complete -> pidgeonhole principle. Write that down in thesis.

* Proper tests.

So far: isomorphy

Work in progress: minimization, pdf_from_dfa, planarity, DB_Enumeration, DB_Minimal, main

* proper rendering (http://www.graphdrawing.org/books.html, http://gdea.informatik.uni-koeln.de/view/subjects/)
* optional: create a GUI
* optional: optimize code further


# Optimization ideas

* Enumerate all combinations of k elements from n

https://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n

https://stackoverflow.com/questions/1851134/generate-all-binary-strings-of-length-n-with-k-bits-set

https://www.geeksforgeeks.org/find-combinations-k-bit-numbers-n-bits-set-1-n-k-sorted-order/

* In enumeration increments make interpretation of transitions progress cleverer, such that the unreachable DFAs are more distributed.

* Use integer instead of integer-lists for enumeration.

* Profile the Code and optimize thus.


__new_state(dfa, is_accepting, unused_symbols)
__equiv_class_to_state(equiv_classes, state)
