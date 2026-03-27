"""
Merge Sort — Step-by-Step Histogram Visualiser

Each subplot shows the full array as a bar chart after a merge operation:
  Blue  → untouched element
  Red   → elements just merged into position
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ─── Step-Tracking Sort ────────────────────────────────────────────────────────

def _tracked(full_arr, steps, highlights):
    """Merge sort that records the global array state after every merge."""
    buf = full_arr[:]

    def _merge_sort(start, end):
        if end - start <= 1:
            return
        mid = (start + end) // 2
        _merge_sort(start, mid)
        _merge_sort(mid, end)

        left  = buf[start:mid]
        right = buf[mid:end]
        i = j = 0
        k = start
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                buf[k] = left[i]; i += 1
            else:
                buf[k] = right[j]; j += 1
            k += 1
        while i < len(left):
            buf[k] = left[i]; i += 1; k += 1
        while j < len(right):
            buf[k] = right[j]; j += 1; k += 1

        steps.append(buf[:])
        highlights.append(list(range(start, end)))

    _merge_sort(0, len(buf))
    # propagate back
    for i, v in enumerate(buf):
        full_arr[i] = v


# ─── Shared Renderer ──────────────────────────────────────────────────────────

def _render(steps, highlights, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Merge Sort",
        active_sequences=highlights,
        info_sequences=["Merge current subarrays" for _ in steps],
        save_path=save_path,
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Merge Sort — Step-by-Step", save_path=None):
    """Show histogram visualisation of merge sort steps."""
    if arr is None:
        arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    work = arr[:]
    _tracked(work, steps, highlights)
    _render(steps, highlights, title, save_path)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}")
    visualize_sort(demo)
