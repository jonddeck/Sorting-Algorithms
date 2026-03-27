"""
Library Sort — Step-by-Step Histogram Visualiser

Tracks each element insertion into the gapped library array,
showing the sparse (gapped) array padded to equal length.
  Blue  → library slot (occupied)
  Grey  → gap (empty slot)
  Red   → element just inserted
  Green → fully sorted (final frame)

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow

_GAP = None   # sentinel for empty gap


def _tracked(arr, steps, highlights):
    n = len(arr)
    size = 2 * n
    lib = [_GAP] * size

    def _find_pos(val):
        left, right = 0, size - 1
        while left <= right:
            mid = (left + right) // 2
            if lib[mid] is _GAP:
                j = mid - 1
                while j >= left and lib[j] is _GAP: j -= 1
                if j >= left and lib[j] < val: left = mid + 1
                else: right = mid - 1
            elif lib[mid] < val: left = mid + 1
            else: right = mid - 1
        return left

    lib[size // 2] = arr[0]
    steps.append([x if x is not _GAP else 0 for x in lib])
    highlights.append([size // 2])

    for val in arr[1:]:
        pos = min(_find_pos(val), size - 1)
        if lib[pos] is _GAP:
            lib[pos] = val
        else:
            # shift right to find gap
            j = pos + 1
            while j < size and lib[j] is not _GAP: j += 1
            if j < size:
                while j > pos: lib[j] = lib[j - 1]; j -= 1
                lib[pos] = val
        steps.append([x if x is not _GAP else 0 for x in lib])
        highlights.append([pos])

    # compact
    final = sorted([x for x in lib if x is not _GAP])
    steps.append(final[:]); highlights.append([])


def _render(steps, highlights, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Library Sort",
        active_sequences=highlights,
        info_sequences=["Insert into gapped library" for _ in steps],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Library Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    _tracked(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 10)
    print(f"Sorting: {demo}"); visualize_sort(demo)
