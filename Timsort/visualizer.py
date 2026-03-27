"""
Timsort — Step-by-Step Histogram Visualiser

Shows each insertion-sort run and each merge of runs.
  Blue   → unsorted / not yet merged
  Orange → current run being insertion-sorted
  Red    → regions being merged
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow

MIN_RUN = 8


def _calc_min_run(n):
    r = 0
    while n >= 64: r |= n & 1; n >>= 1
    return n + r


def _insertion_sort_range(arr, lo, hi, steps, highlights, labels):
    for i in range(lo + 1, hi + 1):
        key, j = arr[i], i - 1
        while j >= lo and arr[j] > key:
            arr[j + 1] = arr[j]
            steps.append(arr[:]); highlights.append([j, j + 1]); labels.append("run")
            j -= 1
        arr[j + 1] = key


def _merge(arr, lo, mid, hi, steps, highlights, labels):
    left, right = arr[lo:mid+1], arr[mid+1:hi+1]
    i = j = 0; k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]: arr[k] = left[i]; i += 1
        else:                   arr[k] = right[j]; j += 1
        k += 1
    while i < len(left): arr[k] = left[i]; i += 1; k += 1
    while j < len(right): arr[k] = right[j]; j += 1; k += 1
    steps.append(arr[:]); highlights.append(list(range(lo, hi + 1))); labels.append("merge")


def _tracked(arr, steps, highlights, labels):
    n = len(arr)
    min_run = _calc_min_run(n)
    for lo in range(0, n, min_run):
        hi = min(lo + min_run - 1, n - 1)
        _insertion_sort_range(arr, lo, hi, steps, highlights, labels)
    size = min_run
    while size < n:
        for lo in range(0, n, 2 * size):
            mid = min(lo + size - 1, n - 1)
            hi  = min(lo + 2 * size - 1, n - 1)
            if mid < hi:
                _merge(arr, lo, mid, hi, steps, highlights, labels)
        size *= 2


def _render(steps, highlights, labels, title, save_path=None):
    names = {"-": "Initial state", "run": "Build a run", "merge": "Merge runs"}
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Timsort",
        active_sequences=highlights,
        info_sequences=[names.get(label, label) for label in labels],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Timsort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, labels = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, labels)
    _render(steps, highlights, labels, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}"); visualize_sort(demo)
