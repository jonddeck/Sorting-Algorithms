"""
Selection Sort Algorithm

Time Complexity: O(n²) - all cases
Space Complexity: O(1)

Description:
Selection Sort divides the array into a sorted and an unsorted region. It repeatedly
finds the minimum element from the unsorted region and places it at the beginning.

Use Cases:
- Small datasets
- Memory-constrained environments (in-place, O(1) extra space)
- When the number of writes must be minimised
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def selection_sort(arr):
    """
    Sorts an array using selection sort algorithm.

    Args:
        arr: List of elements to sort

    Returns:
        Sorted list
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# ─── Step-Tracking Variant ─────────────────────────────────────────────────────

def _tracked_selection_sort(arr, steps, highlights):
    """Runs selection sort while recording the state after each selection."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr.copy())
        highlights.append([i, min_idx])


# ─── Visualization ─────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Selection Sort — Step-by-Step", save_path=None):
    """
    Displays a grid of bar-chart histograms showing the array at each step.

    Args:
        arr:       Input list (uses a built-in demo if None)
        title:     Plot title
        save_path: If given, saves the figure to this file path
    """
    if arr is None:
        arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]

    steps, highlights = [arr.copy()], [[]]
    _tracked_selection_sort(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


def _render(steps, highlights, title, save_path=None):
    """Render as an interactive slideshow."""
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Selection Sort",
        active_sequences=highlights,
        info_sequences=["Select the next minimum" for _ in steps],
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
        sorted_arr = selection_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")

    # ── Visual demo ──
    demo = random.sample(range(1, 101), 12)
    print(f"\nVisualising Selection Sort on: {demo}")
    visualize_sort(demo)
