"""
Burstsort Visualizer
Histogram step-by-step visualization of Burstsort's character-level bucket passes.

Burstsort is optimized for strings; here we adapt it to integers by treating
each decimal digit position as a "character level".

Colors:
  - Blue         (#3498DB): unprocessed
  - Bucket hues            : elements distributed to buckets at this depth level
  - Orange       (#F39C12): elements being merged/burst back
  - Green        (#2ECC71): final sorted result
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

def _tracked_burstsort(arr):
    """Simulate Burstsort as LSD radix with a burst-threshold flavor."""
    steps = []
    highlights = []
    labels = []
    bid_map = []

    if not arr:
        return steps, highlights, labels, bid_map

    working = list(arr)
    max_val = max(working) if working else 0
    num_digits = max(1, len(str(max_val)))
    BURST_THRESHOLD = 4  # max bucket size before "bursting"

    # Initial snapshot
    steps.append(list(working))
    highlights.append([0] * len(working))
    labels.append("Initial")
    bid_map.append([-1] * len(working))

    for digit_pos in range(num_digits - 1, -1, -1):  # MSD order for burstsort feel
        divisor = 10 ** digit_pos

        # Show each element being assigned to its bucket
        assignment = [-1] * len(working)
        for i, val in enumerate(working):
            digit = (val // divisor) % 10
            assignment[i] = digit

            snap = list(working)
            h = [0] * len(working)
            h[i] = 1
            steps.append(snap)
            highlights.append(h)
            labels.append(f"Digit {num_digits - digit_pos} bucket")
            bid_map.append(list(assignment))

        # Perform the pass
        buckets = [[] for _ in range(10)]
        for val in working:
            digit = (val // divisor) % 10
            buckets[digit].append(val)
            if len(buckets[digit]) >= BURST_THRESHOLD:
                # "burst" – sort this bucket immediately
                buckets[digit].sort()

        working = [v for bucket in buckets for v in bucket]

        # Reconstruct snapshot
        new_assign = []
        for b_idx, bucket in enumerate(buckets):
            new_assign.extend([b_idx] * len(bucket))

        steps.append(list(working))
        highlights.append([0] * len(working))
        labels.append(f"Digit {num_digits - digit_pos} pass done")
        bid_map.append(new_assign)

    # final
    working.sort()
    steps.append(list(working))
    highlights.append([0] * len(working))
    labels.append("Sorted")
    bid_map.append([-1] * len(working))

    return steps, highlights, labels, bid_map


# ── rendering ────────────────────────────────────────────────────────────────

def _render(steps, highlights, labels, bid_map, title="Burstsort", save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Burstsort",
        active_sequences=highlights,
        info_sequences=labels,
        save_path=save_path,
    )


# ── public API ───────────────────────────────────────────────────────────────

def visualize_sort(arr=None, title="Burstsort", save_path=None):
    """Visualize Burstsort with a histogram grid showing each step."""
    if arr is None:
        import random
        arr = [random.randint(1, 99) for _ in range(16)]
    steps, highlights, labels, bid_map = _tracked_burstsort(list(arr))
    _render(steps, highlights, labels, bid_map, title=title, save_path=save_path)


if __name__ == "__main__":
    visualize_sort()
