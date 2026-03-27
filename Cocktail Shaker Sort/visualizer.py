"""
Cocktail Shaker Sort — Step-by-Step Histogram Visualiser

Forward passes bubble large elements right; backward passes bubble small elements left.
  Blue   → untouched
  Red    → active comparison pair
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights, directions):
    n, start, end, swapped = len(arr), 0, len(arr) - 1, True
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]; swapped = True
            steps.append(arr[:]); highlights.append([i, i + 1]); directions.append("→")
        end -= 1
        if not swapped: break
        swapped = False
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]; swapped = True
            steps.append(arr[:]); highlights.append([i, i + 1]); directions.append("←")
        start += 1


def _render(steps, highlights, directions, title, save_path=None):
    direction_names = {"-": "Initial state", "→": "Forward pass", "←": "Backward pass"}
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Cocktail Shaker Sort",
        active_sequences=highlights,
        info_sequences=[direction_names.get(direction, "Pass") for direction in directions],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Cocktail Shaker Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, directions = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, directions)
    _render(steps, highlights, directions, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
