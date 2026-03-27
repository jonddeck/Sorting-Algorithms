"""
Comb Sort — Step-by-Step Histogram Visualiser

Each subplot shows the array after a comparison/swap at the current gap:
  Blue  → untouched
  Red   → comb pair being compared/swapped
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights, gap_labels):
    n, gap, swapped = len(arr), len(arr), True
    while gap > 1 or swapped:
        gap = max(1, int(gap / 1.3))
        swapped = False
        for i in range(n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
            steps.append(arr[:]); highlights.append([i, i + gap])
            gap_labels.append(gap)


def _render(steps, highlights, gap_labels, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Comb Sort",
        active_sequences=highlights,
        info_sequences=[f"Gap = {gap}" for gap in gap_labels],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Comb Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, gap_labels = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, gap_labels)
    _render(steps, highlights, gap_labels, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
