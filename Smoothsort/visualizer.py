"""
Smoothsort — Step-by-Step Histogram Visualiser

Uses a heap based on Leonardo numbers. Captures each sift-down and each extraction.
  Blue   → heap element
  Orange → sift-down pair
  Red    → element being extracted to sorted tail
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights, phases):
    """Simplified smoothsort tracking (heap-based)."""
    n = len(arr)

    def _sift(root, end):
        while True:
            child = 2 * root + 1
            if child > end: break
            if child + 1 <= end and arr[child + 1] > arr[child]: child += 1
            if arr[root] >= arr[child]: break
            arr[root], arr[child] = arr[child], arr[root]
            steps.append(arr[:]); highlights.append([root, child]); phases.append("sift")
            root = child

    # Build heap
    for i in range(n // 2 - 1, -1, -1):
        _sift(i, n - 1)

    # Extract
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        steps.append(arr[:]); highlights.append([0, i]); phases.append("extract")
        _sift(0, i - 1)


def _render(steps, highlights, phases, title, save_path=None):
    labels = {"-": "Initial state", "sift": "Sift-down heap step", "extract": "Extract maximum"}
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Smoothsort",
        active_sequences=highlights,
        info_sequences=[labels.get(phase, phase) for phase in phases],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Smoothsort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, phases = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, phases)
    _render(steps, highlights, phases, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}"); visualize_sort(demo)
