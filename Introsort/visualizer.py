"""
Introsort — Step-by-Step Histogram Visualiser

Tracks depth: uses Quicksort partitions, switches to Heapsort at depth limit,
and Insertion Sort for small sub-arrays.
  Blue   → untouched
  Orange → pivot
  Red    → active partition
  Purple → heapsort phase
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

import math
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights, algo_labels):
    n = len(arr)
    max_depth = 2 * math.floor(math.log2(n)) if n > 1 else 0

    def _ins(lo, hi):
        for i in range(lo + 1, hi + 1):
            key, j = arr[i], i - 1
            while j >= lo and arr[j] > key:
                arr[j + 1] = arr[j]; j -= 1
                steps.append(arr[:]); highlights.append([j + 1, j + 2]); algo_labels.append("insertion")
            arr[j + 1] = key

    def _heapify(size, i, base):
        lg, l, r = i, 2*i+1, 2*i+2
        if l < size and arr[base+l] > arr[base+lg]: lg = l
        if r < size and arr[base+r] > arr[base+lg]: lg = r
        if lg != i:
            arr[base+i], arr[base+lg] = arr[base+lg], arr[base+i]
            steps.append(arr[:]); highlights.append([base+i, base+lg]); algo_labels.append("heap")
            _heapify(size, lg, base)

    def _heap(lo, hi):
        sz = hi - lo + 1
        for i in range(sz // 2 - 1, -1, -1): _heapify(sz, i, lo)
        for i in range(sz - 1, 0, -1):
            arr[lo], arr[lo+i] = arr[lo+i], arr[lo]
            steps.append(arr[:]); highlights.append([lo, lo+i]); algo_labels.append("heap")
            _heapify(i, 0, lo)

    def _partition(lo, hi):
        pivot, i = arr[hi], lo - 1
        for j in range(lo, hi):
            if arr[j] < pivot:
                i += 1; arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[hi] = arr[hi], arr[i+1]
        steps.append(arr[:]); highlights.append(list(range(lo, hi+1))); algo_labels.append("quick")
        return i + 1

    def _intro(lo, hi, depth):
        if hi - lo < 16:
            _ins(lo, hi)
        elif depth == 0:
            _heap(lo, hi)
        else:
            p = _partition(lo, hi)
            _intro(lo, p - 1, depth - 1)
            _intro(p + 1, hi, depth - 1)

    if n > 1: _intro(0, n - 1, max_depth)


def _render(steps, highlights, algo_labels, title, save_path=None):
    labels = {
        "-": "Initial state",
        "quick": "Quicksort partition",
        "heap": "Heapsort fallback",
        "insertion": "Insertion sort cleanup",
    }
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Introsort",
        active_sequences=highlights,
        info_sequences=[labels.get(label, label) for label in algo_labels],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Introsort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, algo_labels = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, algo_labels)
    _render(steps, highlights, algo_labels, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}"); visualize_sort(demo)
