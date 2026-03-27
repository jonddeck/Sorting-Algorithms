"""
Counting Sort Visualizer
Histogram step-by-step visualization of the Counting Sort algorithm.

Phases:
  - Blue   (#3498DB): untouched elements in output array
  - Red    (#E74C3C): element currently being placed into output
  - Orange (#F39C12): count array being populated
  - Green  (#2ECC71): fully sorted output
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ── tracking ────────────────────────────────────────────────────────────────

def _tracked_counting_sort(arr):
    """Run counting sort and collect (snapshot, highlights, phase_label) triples."""
    steps = []
    highlights = []
    labels = []

    if not arr:
        return steps, highlights, labels

    min_val = min(arr)
    max_val = max(arr)
    k = max_val - min_val + 1

    # Phase 1 – build count array; show input array with highlighted element
    count = [0] * k
    for i, val in enumerate(arr):
        count[val - min_val] += 1
        snap = list(arr)
        steps.append(snap)
        h = [0] * len(arr)
        h[i] = 1
        highlights.append(h)
        labels.append("Count phase")

    # Phase 2 – reconstruct output; show output being filled bar-by-bar
    output = [0] * len(arr)
    idx = 0
    for val_offset in range(k):
        for _ in range(count[val_offset]):
            output[idx] = val_offset + min_val
            steps.append(list(output))
            h = [0] * len(arr)
            h[idx] = 1
            highlights.append(h)
            labels.append("Place phase")
            idx += 1

    # Final sorted
    steps.append(list(output))
    highlights.append([0] * len(output))
    labels.append("Sorted")

    return steps, highlights, labels


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, title="Counting Sort", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Counting Sort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Counting Sort", save_path=None):
    """Visualize Counting Sort with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = random.sample(range(1, 31), 20)
    steps, highlights, labels = _tracked_counting_sort(list(arr))
    _render(steps, highlights, labels, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
