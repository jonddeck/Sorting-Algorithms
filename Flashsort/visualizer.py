"""
Flashsort Visualizer
Histogram step-by-step visualization of the Flashsort algorithm.

Flashsort works in two phases:
  1. Classification – distribute n elements into m buckets (classes) in O(n)
  2. Permutation    – cycle-sort elements into their buckets in-place
  3. Insertion sort – clean up within each class (small groups)

Colors:
  - Blue   (#3498DB): unclassified
  - Bucket hues     : elements classified into a class
  - Red    (#E74C3C): element being permuted/swapped
  - Orange (#F39C12): insertion-sort cleanup phase
  - Green  (#2ECC71): final sorted result
"""

import math
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


_CLASS_COLORS = [
    "#E74C3C", "#E67E22", "#F1C40F", "#2ECC71",
    "#1ABC9C", "#9B59B6", "#E91E63", "#FF5722",
    "#00BCD4", "#795548",
]

BLUE   = "#3498DB"
RED    = "#E74C3C"
ORANGE = "#F39C12"
GREEN  = "#2ECC71"


# ── tracking ────────────────────────────────────────────────────────────────

def _tracked_flashsort(arr):
    steps = []
    highlights = []
    labels = []
    class_map = []

    if not arr:
        return steps, highlights, labels, class_map

    working = list(arr)
    n = len(working)
    m = max(1, int(0.45 * n))

    min_val = min(working)
    max_val = max(working)
    if min_val == max_val:
        steps.append(list(working))
        highlights.append([0] * n)
        labels.append("Sorted")
        class_map.append([-1] * n)
        return steps, highlights, labels, class_map

    # Phase 1 – classify: count elements per class
    c = [0] * m
    diff = max_val - min_val
    assignment = [-1] * n

    for i, val in enumerate(working):
        k = min(int(m * (val - min_val) / diff), m - 1)
        c[k] += 1
        assignment[i] = k
        snap = list(working)
        h = [0] * n
        h[i] = 1
        steps.append(snap)
        highlights.append(h)
        labels.append(f"Classify k={k}")
        class_map.append(list(assignment))

    # Prefix sums for class boundaries
    for i in range(1, m):
        c[i] += c[i - 1]

    # Phase 2 – permutation cycle (in-place)
    # Track class_assign for display
    cur_assign = list(assignment)

    def get_class(v):
        return min(int(m * (v - min_val) / diff), m - 1)

    # Simple permutation: for each position, place element in correct class region
    j = 0
    k = m - 1
    num_moved = 0
    while num_moved < n - 1:
        while j > c[k] - 1:
            j += 1
            k = get_class(working[j])
        flash = working[j]
        while j != c[k] - 1:
            k = get_class(flash)
            c[k] -= 1
            target = c[k]
            working[target], flash = flash, working[target]
            cur_assign[target] = k
            num_moved += 1

            snap = list(working)
            h = [0] * n
            h[target] = 1
            steps.append(snap)
            highlights.append(h)
            labels.append(f"Permute")
            class_map.append(list(cur_assign))

    # Phase 3 – insertion sort within each class
    for i in range(1, n):
        key = working[i]
        j = i - 1
        while j >= 0 and working[j] > key:
            working[j + 1] = working[j]
            j -= 1
        working[j + 1] = key

    steps.append(list(working))
    highlights.append([0] * n)
    labels.append("Sorted")
    class_map.append([-1] * n)

    return steps, highlights, labels, class_map


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, class_map, title="Flashsort", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Flashsort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Flashsort", save_path=None):
    """Visualize Flashsort with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = [random.randint(1, 50) for _ in range(16)]
    steps, highlights, labels, class_map = _tracked_flashsort(list(arr))
    _render(steps, highlights, labels, class_map, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
