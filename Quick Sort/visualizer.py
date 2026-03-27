"""
Quick Sort — Step-by-Step Histogram Visualiser

Each subplot shows the full array after a partition step:
  Blue   → untouched element
  Orange → pivot element
  Red    → elements in the active partition window
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ─── Step-Tracking Sort ────────────────────────────────────────────────────────

def _tracked(arr, steps, highlights, pivots):
    def _partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(arr[:])
        highlights.append(list(range(low, high + 1)))
        pivots.append(i + 1)
        return i + 1

    def _quick(low, high):
        if low < high:
            p = _partition(low, high)
            _quick(low, p - 1)
            _quick(p + 1, high)

    _quick(0, len(arr) - 1)


# ─── Shared Renderer ──────────────────────────────────────────────────────────

def _render(steps, highlights, pivots, title, save_path=None):
    info = []
    for pv in pivots:
        info.append("Initial state" if pv is None else f"Pivot index: {pv}")
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Quick Sort",
        active_sequences=highlights,
        info_sequences=info,
        save_path=save_path,
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Quick Sort — Step-by-Step", save_path=None):
    """Show histogram visualisation of quick sort partition steps."""
    if arr is None:
        arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, pivots = [arr.copy()], [[]], [None]
    work = arr[:]
    _tracked(work, steps, highlights, pivots)
    _render(steps, highlights, pivots, title, save_path)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}")
    visualize_sort(demo)
