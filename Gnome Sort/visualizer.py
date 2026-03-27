"""
Gnome Sort — Step-by-Step Histogram Visualiser

The gnome moves forward if the current element is in order, backward if not.
  Blue  → untouched
  Red   → pair being compared / swapped
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights):
    i, n = 0, len(arr)
    while i < n:
        if i == 0 or arr[i] >= arr[i - 1]:
            i += 1
        else:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            steps.append(arr[:]); highlights.append([i, i - 1])
            i -= 1


def _render(steps, highlights, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Gnome Sort",
        active_sequences=highlights,
        info_sequences=["Swap backward when order is wrong" for _ in steps],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Gnome Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    _tracked(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
