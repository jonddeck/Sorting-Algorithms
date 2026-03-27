"""
Patience Sort — Step-by-Step Histogram Visualiser

Shows piles being built (card placement), then the merge phase.
Each subplot shows the sorted-so-far result alongside remaining unsorted elements.
  Blue  → unsorted / unplaced
  Red   → current element being placed on a pile
  Green → merged / final sorted

Run directly:  python visualizer.py
"""

import bisect
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


def _tracked(arr, steps, highlights, labels):
    import heapq
    piles = []   # each pile: list, top = last element

    for val in arr:
        # Binary search for first pile whose top >= val
        tops = [p[-1] for p in piles]
        pos  = bisect.bisect_left(tops, val)
        if pos == len(piles):
            piles.append([val])
        else:
            piles[pos].append(val)

        # Snapshot: flatten piles (bottoms→tops) as current state
        flat = [item for pile in piles for item in pile]
        steps.append(flat[:] + arr[arr.index(val) + 1:] if val in arr else flat)
        highlights.append([len(flat) - 1])
        labels.append("place")

    # Merge phase: always extract the minimum top
    heap = [(piles[i][-1], i) for i in range(len(piles))]
    heapq.heapify(heap)
    result = []
    while heap:
        val, pi = heapq.heappop(heap)
        result.append(val)
        piles[pi].pop()
        if piles[pi]:
            heapq.heappush(heap, (piles[pi][-1], pi))
        remaining = [item for pile in piles for item in pile]
        steps.append(result[:] + remaining)
        highlights.append([len(result) - 1])
        labels.append("merge")


def _render(steps, highlights, labels, title, save_path=None):
    labels_map = {"-": "Initial state", "place": "Place on a pile", "merge": "Merge pile tops"}
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Patience Sort",
        active_sequences=highlights,
        info_sequences=[labels_map.get(label, label) for label in labels],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Patience Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, labels = [arr.copy()], [[]], ["-"]
    _tracked(arr.copy(), steps, highlights, labels)
    _render(steps, highlights, labels, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
