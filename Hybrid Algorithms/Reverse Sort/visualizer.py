"""
Reverse Hybrid Sort — Step-by-Step Histogram Visualiser

Combines reverse comparison phase with odd-even cleanup phases.
  Blue   → untouched
    Red    → reverse-phase pair
    Purple → odd/even-phase pair
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights, phases):
    n = len(arr)
    sorted_flag = False
    
    while not sorted_flag:
        sorted_flag = True
        arr_reverse = arr[::-1]
        
        # Reverse Comparison Phase
        for i in range(n):
            mirror = n - 1 - i
            if i < mirror and arr[i] > arr_reverse[i]:
                arr[i], arr[mirror] = arr[mirror], arr[i]
                sorted_flag = False
            steps.append(arr[:])
            highlights.append([i, mirror])
            phases.append("reverse")
        
        # Odd Phase: Compare (1,2), (3,4), ...
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False
            steps.append(arr[:])
            highlights.append([i, i + 1])
            phases.append("odd")
        
        # Even Phase: Compare (0,1), (2,3), ...
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False
            steps.append(arr[:])
            highlights.append([i, i + 1])
            phases.append("even")


def _render(steps, highlights, phases, title, save_path=None):
    phase_names = {"-": "Initial state", "reverse": "Reverse comparison phase", "odd": "Odd phase", "even": "Even phase"}
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Reverse Hybrid Sort",
        active_sequences=highlights,
        info_sequences=[phase_names.get(phase, phase) for phase in phases],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Reverse Hybrid Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, phases = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, phases)
    _render(steps, highlights, phases, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
