"""
Insertion Sort — Step-by-Step Histogram Visualiser

Each subplot shows the full array as a bar chart at a key moment:
  Blue  → untouched element
  Red   → element being inserted / shifted
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ─── Step-Tracking Sort ────────────────────────────────────────────────────────

def _tracked(arr, steps, highlights):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            steps.append(arr.copy())
            highlights.append([j, j + 1])
            j -= 1
        arr[j + 1] = key
        steps.append(arr.copy())
        highlights.append([j + 1])


# ─── Shared Renderer ──────────────────────────────────────────────────────────

def _render(steps, highlights, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Insertion Sort",
        active_sequences=highlights,
        info_sequences=["Insert element into sorted prefix" for _ in steps],
        save_path=save_path,
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Insertion Sort — Step-by-Step", save_path=None):
    """Show histogram visualisation of insertion sort steps."""
    if arr is None:
        arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    _tracked(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}")
    visualize_sort(demo)
