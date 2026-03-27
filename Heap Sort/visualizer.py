"""
Heap Sort — Step-by-Step Histogram Visualiser

Phase 1 (Build-Heap): heap property enforced bottom-up — highlighted in orange.
Phase 2 (Extract):    max root swapped to end — highlighted in red.
Final frame shown in green.

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ─── Step-Tracking Sort ────────────────────────────────────────────────────────

def _tracked(arr, steps, highlights, phases):
    n = len(arr)

    def heapify(size, i):
        largest, l, r = i, 2*i+1, 2*i+2
        if l < size and arr[l] > arr[largest]: largest = l
        if r < size and arr[r] > arr[largest]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            steps.append(arr[:]); highlights.append([i, largest]); phases.append("build")
            heapify(size, largest)

    # Phase 1 – build max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # Phase 2 – extract max elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        steps.append(arr[:]); highlights.append([0, i]); phases.append("extract")
        heapify(i, 0)


# ─── Shared Renderer ──────────────────────────────────────────────────────────

def _render(steps, highlights, phases, title, save_path=None):
    info = [
        "Initial heap" if phase == "start" else ("Heapify build phase" if phase == "build" else "Extract max element")
        for phase in phases
    ]
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Heap Sort",
        active_sequences=highlights,
        info_sequences=info,
        save_path=save_path,
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Heap Sort — Step-by-Step", save_path=None):
    """Show histogram visualisation of heap sort steps."""
    if arr is None:
        arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, phases = [arr.copy()], [[]], ["start"]
    work = arr[:]
    _tracked(work, steps, highlights, phases)
    _render(steps, highlights, phases, title, save_path)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}")
    visualize_sort(demo)
