"""
Tournament Sort — Step-by-Step Histogram Visualiser

Shows each minimum extraction from the tournament (heap).
  Blue  → in heap
  Red   → element just extracted / placed
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

import heapq
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights):
    heap = arr[:]
    heapq.heapify(heap)
    result = []
    full = heap[:]  # visualise in original-length window
    steps.append(heap[:]); highlights.append([])
    while heap:
        val = heapq.heappop(heap)
        result.append(val)
        # pad result to same length with remaining heap items
        snapshot = result + list(heap)
        steps.append(snapshot[:]); highlights.append([len(result) - 1])
    for i, v in enumerate(result): arr[i] = v


def _render(steps, highlights, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Tournament Sort",
        active_sequences=highlights,
        info_sequences=["Extract next tournament winner" for _ in steps],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Tournament Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    _tracked(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
