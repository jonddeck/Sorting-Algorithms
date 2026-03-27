"""
Shellsort — Step-by-Step Histogram Visualiser

Each subplot shows the array after one insertion pass with the current gap:
  Blue   → untouched element
  Red    → element being placed
  Purple → gap-pair being compared
  Green  → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ─── Step-Tracking Sort ────────────────────────────────────────────────────────

def _tracked(arr, steps, highlights, gaps_used):
    n   = len(arr)
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1          # Knuth's sequence

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j    = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                steps.append(arr[:]); highlights.append([j, j - gap])
                gaps_used.append(gap)
                j -= gap
            arr[j] = temp
        gap //= 3


# ─── Shared Renderer ──────────────────────────────────────────────────────────

def _render(steps, highlights, gaps_used, title, save_path=None):
    info = [f"Gap = {gap}" for gap in gaps_used]
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Shellsort",
        active_sequences=highlights,
        info_sequences=info,
        save_path=save_path,
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Shellsort — Step-by-Step", save_path=None):
    """Show histogram visualisation of shellsort gap passes."""
    if arr is None:
        arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights, gaps_used = [arr.copy()], [[]], ["-"]
    work = arr[:]
    _tracked(work, steps, highlights, gaps_used)
    _render(steps, highlights, gaps_used, title, save_path)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 14)
    print(f"Sorting: {demo}")
    visualize_sort(demo)
