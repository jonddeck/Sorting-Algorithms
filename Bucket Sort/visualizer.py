"""
Bucket Sort Visualizer
Histogram step-by-step visualization of the Bucket Sort algorithm.

Phases:
  - Each bucket gets a distinct hue during distribution
  - Red    (#E74C3C): element actively being placed into a bucket
  - Green  (#2ECC71): final sorted result
"""

import math
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


# ── tracking ────────────────────────────────────────────────────────────────

_BUCKET_COLORS = [
    "#E74C3C", "#E67E22", "#F1C40F", "#2ECC71",
    "#1ABC9C", "#3498DB", "#9B59B6", "#E91E63",
    "#FF5722", "#00BCD4",
]


def _tracked_bucket_sort(arr):
    steps = []
    highlights = []
    labels = []
    bucket_ids = []   # which bucket each bar belongs to (-1 = neutral)

    if not arr:
        return steps, highlights, labels, bucket_ids

    working = list(arr)
    min_val = min(working)
    max_val = max(working)
    n = len(working)
    num_buckets = max(1, int(math.sqrt(n)))
    spread = (max_val - min_val) or 1

    # Phase 1: distribute into buckets, show input with active highlight
    bucket_assign = [-1] * n
    for i, val in enumerate(working):
        b = min(int((val - min_val) / spread * num_buckets), num_buckets - 1)
        bucket_assign[i] = b
        snap = list(working)
        h = [0] * n
        h[i] = 2       # 2 = "being assigned"
        steps.append(snap)
        highlights.append(list(h))
        labels.append(f"Bucket {b}")
        bucket_ids.append(list(bucket_assign))

    # Phase 2: sort each bucket (insertion sort) and reconstruct
    buckets = [[] for _ in range(num_buckets)]
    for idx, val in enumerate(working):
        b = min(int((val - min_val) / spread * num_buckets), num_buckets - 1)
        buckets[b].append(val)

    for b_idx in range(num_buckets):
        buckets[b_idx].sort()

    output = [v for bucket in buckets for v in bucket]
    output_assign = []
    pos = 0
    for b_idx, bucket in enumerate(buckets):
        for _ in bucket:
            output_assign.append(b_idx)
            pos += 1

    # show reconstructed output
    steps.append(list(output))
    highlights.append([0] * n)
    labels.append("Reconstruct")
    bucket_ids.append(list(output_assign))

    # final sorted
    steps.append(list(output))
    highlights.append([0] * n)
    labels.append("Sorted")
    bucket_ids.append([-1] * n)

    return steps, highlights, labels, bucket_ids


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, bucket_ids,
            title="Bucket Sort", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Bucket Sort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Bucket Sort", save_path=None):
    """Visualize Bucket Sort with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = [random.randint(1, 50) for _ in range(18)]
    steps, highlights, labels, bucket_ids = _tracked_bucket_sort(list(arr))
    _render(steps, highlights, labels, bucket_ids, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
