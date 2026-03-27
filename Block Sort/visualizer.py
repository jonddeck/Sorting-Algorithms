"""
Block Sort — Step-by-Step Histogram Visualiser

Shows each block merge (divide-and-conquer).
  Blue  → untouched
  Red   → block currently being merged
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights):
    def _merge(lo, mid, hi):
        tmp, i, j = [], lo, mid + 1
        while i <= mid and j <= hi:
            if arr[i] <= arr[j]: tmp.append(arr[i]); i += 1
            else:                tmp.append(arr[j]); j += 1
        while i <= mid: tmp.append(arr[i]); i += 1
        while j <= hi:  tmp.append(arr[j]); j += 1
        for k, v in enumerate(tmp): arr[lo + k] = v
        steps.append(arr[:]); highlights.append(list(range(lo, hi + 1)))

    def _sort(lo, hi):
        if lo >= hi: return
        mid = (lo + hi) // 2
        _sort(lo, mid); _sort(mid + 1, hi)
        _merge(lo, mid, hi)

    _sort(0, len(arr) - 1)


def _render(steps, highlights, title, save_path=None, step_delay=2.0):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Block Sort",
        active_sequences=highlights,
        info_sequences=["Merge current block range" for _ in steps],
        save_path=save_path,
        step_delay=step_delay,
    )


def visualize_sort(arr=None, title="Block Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    _tracked(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}"); visualize_sort(demo)
