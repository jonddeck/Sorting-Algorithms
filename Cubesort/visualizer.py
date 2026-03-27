"""
Cubesort — Step-by-Step Histogram Visualiser

Shows each 3-way split merge.
  Blue  → unsorted
  Red   → active merge region
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights):
    def _ins(lo, hi):
        for i in range(lo + 1, hi + 1):
            key, j = arr[i], i - 1
            while j >= lo and arr[j] > key:
                arr[j + 1] = arr[j]; j -= 1
            arr[j + 1] = key

    def _merge3(lo, m1, m2, hi):
        tmp, i, j, k, t = [], lo, m1 + 1, m2 + 1, 0
        while i <= m1 and j <= m2 and k <= hi:
            mn = min(arr[i], arr[j], arr[k])
            if mn == arr[i]: tmp.append(arr[i]); i += 1
            elif mn == arr[j]: tmp.append(arr[j]); j += 1
            else: tmp.append(arr[k]); k += 1
        # drain remaining two
        rem = sorted(list(arr[i:m1+1]) + list(arr[j:m2+1]) + list(arr[k:hi+1]))
        tmp.extend(rem)
        for idx, v in enumerate(tmp): arr[lo + idx] = v
        steps.append(arr[:]); highlights.append(list(range(lo, hi + 1)))

    def _sort(lo, hi):
        if hi - lo < 8: _ins(lo, hi); return
        third = (hi - lo) // 3
        m1, m2 = lo + third, lo + 2 * third
        _sort(lo, m1); _sort(m1 + 1, m2); _sort(m2 + 1, hi)
        _merge3(lo, m1, m2, hi)

    _sort(0, len(arr) - 1)


def _render(steps, highlights, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Cubesort",
        active_sequences=highlights,
        info_sequences=["Three-way merge region" for _ in steps],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Cubesort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    _tracked(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}"); visualize_sort(demo)
