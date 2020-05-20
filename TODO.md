 proper tests

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