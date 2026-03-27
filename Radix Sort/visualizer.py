"""
Radix Sort (LSD) Visualizer
Histogram step-by-step visualization of the Radix Sort algorithm.

Each pass processes one digit position (least-significant first).
Colors:
  - Blue   (#3498DB): unsorted / unprocessed
  - Red    (#E74C3C): elements currently being bucketed for this digit pass
  - Orange (#F39C12): pass complete, reconstructed array
  - Green  (#2ECC71): final sorted result
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ── tracking ────────────────────────────────────────────────────────────────

def _tracked_radix_sort(arr):
    steps = []
    highlights = []
    labels = []

    if not arr:
        return steps, highlights, labels

    working = list(arr)
    max_val = max(working)
    num_digits = len(str(max_val)) if max_val > 0 else 1

    for digit_pos in range(num_digits):
        divisor = 10 ** digit_pos
        # snapshot: show every element with red highlight while bucketing
        for i, val in enumerate(working):
            snap = list(working)
            h = [0] * len(working)
            h[i] = 1
            steps.append(snap)
            highlights.append(h)
            labels.append(f"Digit {digit_pos+1} – bucket")

        # perform the bucket-sort pass
        buckets = [[] for _ in range(10)]
        for val in working:
            digit = (val // divisor) % 10
            buckets[digit].append(val)

        working = [v for bucket in buckets for v in bucket]

        # snapshot: show reconstructed array after this pass
        steps.append(list(working))
        highlights.append([0] * len(working))
        labels.append(f"Digit {digit_pos+1} – reconstruct")

    # final
    steps.append(list(working))
    highlights.append([0] * len(working))
    labels.append("Sorted")

    return steps, highlights, labels


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, title="Radix Sort (LSD)", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Radix Sort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Radix Sort (LSD)", save_path=None):
    """Visualize Radix Sort (LSD) with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = [random.randint(1, 99) for _ in range(16)]
    steps, highlights, labels = _tracked_radix_sort(list(arr))
    _render(steps, highlights, labels, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
