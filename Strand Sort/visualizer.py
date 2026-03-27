"""
Strand Sort — Step-by-Step Histogram Visualiser

Each subplot shows the remaining unsorted pool after a strand (increasing subsequence)
is extracted and merged into the result.
  Blue   → elements still in unsorted pool
  Orange → strand just extracted
  Green  → elements now in sorted result / final frame

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _merge(a, b):
    res, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]: res.append(a[i]); i += 1
        else:             res.append(b[j]); j += 1
    res.extend(a[i:]); res.extend(b[j:])
    return res


def _tracked(arr, steps, highlights, labels):
    remaining, result = arr[:], []
    while remaining:
        strand = [remaining[0]]
        new_remaining = []
        for x in remaining[1:]:
            if x >= strand[-1]: strand.append(x)
            else:               new_remaining.append(x)
        result = _merge(result, strand)
        remaining = new_remaining

        # Show the current global view: result + remaining
        full = result + remaining
        steps.append(full[:])
        highlights.append(list(range(len(result))))      # sorted portion
        labels.append(f"strand={strand}")


def _render(steps, highlights, labels, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Strand Sort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Strand Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, labels = [arr.copy()], [[]], ["initial"]
    _tracked(arr.copy(), steps, highlights, labels)
    _render(steps, highlights, labels, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}"); visualize_sort(demo)
