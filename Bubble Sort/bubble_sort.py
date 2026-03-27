"""
Bubble Sort Algorithm

Time Complexity: O(n²) - average and worst case, O(n) - best case (already sorted)
Space Complexity: O(1)

Description:
Bubble Sort repeatedly steps through the list, compares adjacent elements, and
swaps them if they are in the wrong order. The largest elements "bubble" to the end.

Use Cases:
- Small datasets
- Nearly sorted data (adaptive with early-exit optimization)
- Educational purposes
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def bubble_sort(arr):
    """
    Sorts an array using bubble sort algorithm.

    Args:
        arr: List of elements to sort

    Returns:
        Sorted list
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# ─── Step-Tracking Variant ─────────────────────────────────────────────────────

def _tracked_bubble_sort(arr, steps, highlights):
    """Runs bubble sort while recording each comparison/swap as a snapshot."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            highlights.append([j, j + 1])
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            steps.append(arr.copy())
        if not swapped:
            break


# ─── Visualization ─────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Bubble Sort — Step-by-Step", save_path=None):
    """
    Displays a grid of bar-chart histograms showing the array at each key step.

    Args:
        arr:       Input list (uses a built-in demo if None)
        title:     Plot title
        save_path: If given, saves the figure to this file path
    """
    if arr is None:
        arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]

    steps, highlights = [arr.copy()], [[]]
    _tracked_bubble_sort(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


def _render(steps, highlights, title, save_path=None):
    """Render as an interactive slideshow."""
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Bubble Sort",
        active_sequences=highlights,
        info_sequences=["Compare adjacent values" for _ in steps],
        save_path=save_path,
    )


# ─── Example Usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random

    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],   # Already sorted
        [5, 4, 3, 2, 1],   # Reverse sorted
        [3],                # Single element
        [],                 # Empty array
    ]

    for arr in test_cases:
        original = arr.copy()
        sorted_arr = bubble_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")

    # ── Visual demo ──
    demo = random.sample(range(1, 101), 12)
    print(f"\nVisualising Bubble Sort on: {demo}")
    visualize_sort(demo)
