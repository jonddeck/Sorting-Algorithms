"""
Statsort Visualizer
Histogram step-by-step visualization of Statsort.

Statsort uses statistical properties (mean, std dev) of the data to estimate
ideal bucket placement, similar to interpolation sort.

Phases:
  1. Compute statistics (mean/std) → show current array
  2. Distribute into buckets using Gaussian-informed boundaries
  3. Sort buckets internally
  4. Reconstruct sorted array

Colors:
  - Blue   (#3498DB): unprocessed
  - Bucket hues     : elements per statistics-guided bucket
  - Orange (#F39C12): bucket being sorted internally
  - Green  (#2ECC71): final sorted result
"""

import math
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

def _tracked_statsort(arr):
    steps = []
    highlights = []
    labels = []
    bid_map = []

    if not arr:
        return steps, highlights, labels, bid_map

    working = list(arr)
    n = len(working)

    # Step 0: show initial array
    steps.append(list(working))
    highlights.append([0] * n)
    labels.append("Initial")
    bid_map.append([-1] * n)

    # Compute statistics
    mean = sum(working) / n
    variance = sum((x - mean) ** 2 for x in working) / n
    std = math.sqrt(variance) if variance > 0 else 1.0

    min_val = min(working)
    max_val = max(working)
    num_buckets = min(n, 10)
    spread = (max_val - min_val) or 1.0

    # Step 1: show stats snapshot
    steps.append(list(working))
    highlights.append([0] * n)
    labels.append(f"μ={mean:.1f} σ={std:.1f}")
    bid_map.append([-1] * n)

    # Phase: distribute using interpolation (stats-guided bucket index)
    assignment = [-1] * n
    for i, val in enumerate(working):
        # interpolation-sort style: bucket = n * (val - min) / (max - min)
        b = min(int(num_buckets * (val - min_val) / spread), num_buckets - 1)
        assignment[i] = b
        snap = list(working)
        h = [0] * n
        h[i] = 1
        steps.append(snap)
        highlights.append(h)
        labels.append(f"Bucket {b}")
        bid_map.append(list(assignment))

    # Build and sort buckets
    buckets = [[] for _ in range(num_buckets)]
    for val in working:
        b = min(int(num_buckets * (val - min_val) / spread), num_buckets - 1)
        buckets[b].append(val)

    # Show sorting within each bucket
    for b_idx in range(num_buckets):
        if len(buckets[b_idx]) > 1:
            buckets[b_idx].sort()
            # reconstruct so far
            partial = []
            b_assign = []
            for k, bkt in enumerate(buckets):
                partial.extend(bkt)
                b_assign.extend([k] * len(bkt))
            partial.extend([0] * (n - len(partial)))
            b_assign.extend([-1] * (n - len(b_assign)))
            steps.append(partial[:n])
            highlights.append([0] * n)
            labels.append(f"Sort bucket {b_idx}")
            bid_map.append(b_assign[:n])

    # Reconstruct final output
    output = [v for bkt in buckets for v in bkt]
    steps.append(list(output))
    highlights.append([0] * n)
    labels.append("Sorted")
    bid_map.append([-1] * n)

    return steps, highlights, labels, bid_map


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, bid_map, title="Statsort", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Statsort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Statsort", save_path=None):
    """Visualize Statsort with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = [random.randint(1, 50) for _ in range(18)]
    steps, highlights, labels, bid_map = _tracked_statsort(list(arr))
    _render(steps, highlights, labels, bid_map, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
