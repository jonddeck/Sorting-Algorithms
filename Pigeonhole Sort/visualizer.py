"""
Pigeonhole Sort Visualizer
Histogram step-by-step visualization of the Pigeonhole Sort algorithm.

Phases:
  - Blue   (#3498DB): elements not yet placed
  - Orange (#F39C12): element being placed into its pigeonhole
  - Red    (#E74C3C): element being written back to output array
  - Green  (#2ECC71): final sorted result
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ── tracking ────────────────────────────────────────────────────────────────

def _tracked_pigeonhole_sort(arr):
    steps = []
    highlights = []
    labels = []

    if not arr:
        return steps, highlights, labels

    working = list(arr)
    min_val = min(working)
    max_val = max(working)
    size = max_val - min_val + 1

    # Phase 1 – distribute into holes (show input, highlight active element)
    holes = [0] * size
    for i, val in enumerate(working):
        holes[val - min_val] += 1
        snap = list(working)
        h = [0] * len(working)
        h[i] = 1
        steps.append(snap)
        highlights.append(h)
        labels.append(f"Hole {val - min_val}")

    # Phase 2 – reconstruct output
    output = list(working)   # will be overwritten element-by-element
    idx = 0
    for hole_idx in range(size):
        for _ in range(holes[hole_idx]):
            output[idx] = hole_idx + min_val
            snap = list(output)
            h = [0] * len(output)
            h[idx] = 1
            steps.append(snap)
            highlights.append(h)
            labels.append(f"Write back")
            idx += 1

    # final
    steps.append(list(output))
    highlights.append([0] * len(output))
    labels.append("Sorted")

    return steps, highlights, labels


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, title="Pigeonhole Sort", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Pigeonhole Sort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Pigeonhole Sort", save_path=None):
    """Visualize Pigeonhole Sort with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = [random.randint(1, 15) for _ in range(18)]
    steps, highlights, labels = _tracked_pigeonhole_sort(list(arr))
    _render(steps, highlights, labels, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
