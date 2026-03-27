"""
Odd-Even Sort — Step-by-Step Histogram Visualiser

Alternating odd and even phases compare/swap pairs at odd or even indices.
  Blue   → untouched
  Red    → odd-phase pair
  Purple → even-phase pair
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights, phases):
    n, sorted_flag = len(arr), False
    while not sorted_flag:
        sorted_flag = True
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]; sorted_flag = False
            steps.append(arr[:]); highlights.append([i, i + 1]); phases.append("odd")
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]; sorted_flag = False
            steps.append(arr[:]); highlights.append([i, i + 1]); phases.append("even")


def _render(steps, highlights, phases, title, save_path=None):
    phase_names = {"-": "Initial state", "odd": "Odd phase", "even": "Even phase"}
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Odd-Even Sort",
        active_sequences=highlights,
        info_sequences=[phase_names.get(phase, phase) for phase in phases],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Odd-Even Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, phases = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, phases)
    _render(steps, highlights, phases, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
