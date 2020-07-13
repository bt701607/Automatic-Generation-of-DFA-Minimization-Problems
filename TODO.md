* proper tests

* proper rendering (http://www.graphdrawing.org/books.html, http://gdea.informatik.uni-koeln.de/view/subjects/)

* replace pygraph or fix bug in the library


# Optimization ideas

* use a building algorithm from research

* Enumerate all combinations of k elements from n

https://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n

https://stackoverflow.com/questions/1851134/generate-all-binary-strings-of-length-n-with-k-bits-set

https://www.geeksforgeeks.org/find-combinations-k-bit-numbers-n-bits-set-1-n-k-sorted-order/

* In enumeration increments make interpretation of transitions progress cleverer, such that the unreachable DFAs are more distributed.

* Use integer instead of integer-lists for enumeration.

* profile the code
