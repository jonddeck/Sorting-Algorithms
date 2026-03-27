"""
Spreadsort Visualizer
Histogram step-by-step visualization of Spreadsort's recursive bucket-partition passes.

Spreadsort is a hybrid of radix/bucket sort + insertion sort.
It recursively splits elements into buckets based on their most-significant bits,
then falls back to comparison sort for small buckets.

Colors:
  - Blue   (#3498DB): unprocessed elements
  - Distinct hue per bucket during partition passes
  - Orange (#F39C12): bucket being insertion-sorted
  - Green  (#2ECC71): final sorted result
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


_BUCKET_COLORS = [
    "#E74C3C", "#E67E22", "#F1C40F", "#2ECC71",
    "#1ABC9C", "#3498DB", "#9B59B6", "#E91E63",
    "#FF5722", "#00BCD4",
]

BLUE   = "#3498DB"
ORANGE = "#F39C12"
GREEN  = "#2ECC71"


# ── tracking ────────────────────────────────────────────────────────────────

def _spreadsort_recursive(arr, offset, steps, highlights, labels, bid_map, depth=0):
    """In-place spreadsort tracked version. offset = position in parent array."""
    n = len(arr)
    if n <= 1:
        return
    if n <= 10 or depth > 8:
        # insertion sort fallback
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return

    min_val = min(arr)
    max_val = max(arr)
    if min_val == max_val:
        return

    num_buckets = min(n, 10)
    spread = (max_val - min_val) or 1

    # Assign each element to a bucket
    assignment = [-1] * n
    for i, v in enumerate(arr):
        b = min(int((v - min_val) / spread * num_buckets), num_buckets - 1)
        assignment[i] = b

    # snapshot: show distribution
    full_snap = list(arr)
    full_hi = [0] * n
    full_bid = list(assignment)
    steps.append(full_snap[:])
    highlights.append(full_hi[:])
    labels.append(f"Depth {depth} split")
    bid_map.append(full_bid[:])

    # Build buckets
    buckets = [[] for _ in range(num_buckets)]
    for i, v in enumerate(arr):
        buckets[assignment[i]].append(v)

    # Recurse on each bucket
    pos = 0
    for b_idx, bucket in enumerate(buckets):
        _spreadsort_recursive(bucket, offset + pos, steps, highlights, labels, bid_map, depth + 1)
        for i, v in enumerate(bucket):
            arr[pos + i] = v
        pos += len(bucket)


def _tracked_spreadsort(arr):
    steps = []
    highlights = []
    labels = []
    bid_map = []

    if not arr:
        return steps, highlights, labels, bid_map

    working = list(arr)

    # Initial snapshot
    steps.append(list(working))
    highlights.append([0] * len(working))
    labels.append("Initial")
    bid_map.append([-1] * len(working))

    _spreadsort_recursive(working, 0, steps, highlights, labels, bid_map)

    # final sorted
    steps.append(list(working))
    highlights.append([0] * len(working))
    labels.append("Sorted")
    bid_map.append([-1] * len(working))

    return steps, highlights, labels, bid_map


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, bid_map, title="Spreadsort", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Spreadsort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Spreadsort", save_path=None):
    """Visualize Spreadsort with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = [random.randint(1, 60) for _ in range(20)]
    steps, highlights, labels, bid_map = _tracked_spreadsort(list(arr))
    _render(steps, highlights, labels, bid_map, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
