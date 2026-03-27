"""
Crumsort — Step-by-Step Histogram Visualiser

Adaptive sort: uses insertion sort on nearly-sorted data, merge sort otherwise.
  Blue   → unsorted
  Red    → active merge region
  Orange → insertion pass
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _is_nearly_sorted(arr):
    pairs = sum(1 for i in range(len(arr) - 1) if arr[i] <= arr[i + 1])
    return pairs > len(arr) * 0.8 if len(arr) > 1 else True


def _tracked(arr, steps, highlights, labels):
    if _is_nearly_sorted(arr):
        for i in range(1, len(arr)):
            key, j = arr[i], i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]; j -= 1
                steps.append(arr[:]); highlights.append([j + 1, j + 2]); labels.append("insertion")
            arr[j + 1] = key
    else:
        def _ms(lo, hi):
            if lo >= hi: return
            mid = (lo + hi) // 2
            _ms(lo, mid); _ms(mid + 1, hi)
            left, right = arr[lo:mid+1], arr[mid+1:hi+1]
            i = j = 0; k = lo
            while i < len(left) and j < len(right):
                if left[i] <= right[j]: arr[k] = left[i]; i += 1
                else:                   arr[k] = right[j]; j += 1
                k += 1
            while i < len(left): arr[k] = left[i]; i += 1; k += 1
            while j < len(right): arr[k] = right[j]; j += 1; k += 1
            steps.append(arr[:]); highlights.append(list(range(lo, hi + 1))); labels.append("merge")
        _ms(0, len(arr) - 1)


def _render(steps, highlights, labels, title, save_path=None):
    labels_map = {"-": "Initial state", "insertion": "Insertion path", "merge": "Merge path"}
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Crumsort",
        active_sequences=highlights,
        info_sequences=[labels_map.get(label, label) for label in labels],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Crumsort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, labels = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, labels)
    _render(steps, highlights, labels, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}"); visualize_sort(demo)
