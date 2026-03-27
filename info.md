# Sorting Algorithms Info

This file contains short descriptions for every algorithm in this workspace.

## Comparison-Based Sorts

- **Bubble Sort**: Repeatedly swaps adjacent out-of-order elements until the list is sorted.
- **Selection Sort**: Repeatedly selects the minimum from the unsorted portion and places it in front.
- **Insertion Sort**: Builds the sorted list one item at a time by inserting each element in position.
- **Merge Sort**: Divide-and-conquer sort that splits, recursively sorts, and merges sublists.
- **Quick Sort**: Partition-based divide-and-conquer sort around a pivot.
- **Heap Sort**: Builds a heap and repeatedly extracts the maximum/minimum element.
- **Shellsort**: Generalized insertion sort using decreasing gaps.
- **Comb Sort**: Bubble-sort variant that compares elements at shrinking gaps.
- **Cocktail Shaker Sort**: Bidirectional bubble sort (left-to-right then right-to-left passes).
- **Gnome Sort**: Similar to insertion sort but swaps backward like a “gnome” stepping through the list.
- **Odd-Even Sort**: Alternates odd-index and even-index compare-swap passes.
- **Strand Sort**: Pulls increasing strands and merges them into a sorted output.
- **Tournament Sort**: Uses a tournament tree / heap-like structure to repeatedly pick the next minimum.
- **Tree Sort**: Inserts elements into a BST, then uses in-order traversal for sorted output.
- **Patience Sort**: Builds piles (like card game patience) and merges pile tops with a heap.
- **Smoothsort**: Dijkstra’s adaptive heap-based sort, efficient on partially sorted data.

## Hybrid Sorts

- **Timsort**: Hybrid of insertion sort + merge sort, optimized for real-world partially sorted data.
- **Introsort**: Starts with quicksort, switches to heapsort when recursion depth is high, and insertion sort for small slices.
- **Fluxsort**: Practical hybrid merge-like strategy designed for modern cache behavior.
- **Crumsort**: Adaptive hybrid approach targeting partially sorted data and practical performance.
- **Block Sort**: In-place block merge strategy reducing extra memory while keeping merge-sort-like behavior.
- **Library Sort**: Insertion-based sort with gaps to reduce shifting costs.
- **Cubesort**: Multi-way partition/merge hybrid designed for practical speed.

## Non-Comparison Sorts

- **Counting Sort**: Counts occurrences of each value and reconstructs the sorted array.
- **Radix Sort**: Sorts by digits/characters one position at a time (LSD/MSD).
- **Bucket Sort**: Distributes elements into buckets, sorts each bucket, then concatenates.
- **Pigeonhole Sort**: Places values in indexed “holes” by key offset and rebuilds output.
- **Spreadsort**: Hybrid distribution sort combining radix-like splitting with fallback comparison sorting.
- **Burstsort**: High-performance trie/bucket approach (typically for strings), here adapted for integer bucket passes.
- **Flashsort**: Classifies values into classes, permutes into place, then finishes with insertion sort.
- **Statsort**: Uses statistical distribution ideas for bucket assignment, then local sorting.
- **Postman Sort**: Multi-key routing/bucketing approach similar to radix sorting by successive keys.

## Notes

- Step-by-step histogram visualizers are in each algorithm folder (`visualizer.py`), while Bubble and Selection include visualization inside their main files.
- Overview scripts are in the `overview/` folder:
  - `complexity_comparison.py`
  - `performance_benchmark.py`
  - `all_sorts_visualizer.py` (to be added)
