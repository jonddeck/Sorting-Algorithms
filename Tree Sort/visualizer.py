"""
Tree Sort — Step-by-Step Histogram Visualiser

Shows the sorted result growing as each element is inserted into the BST
and in-order traversal progressively extracts sorted values.
  Blue  → unsorted / not yet extracted
  Red   → just inserted into BST
  Green → extracted via in-order traversal / final frame

Run directly:  python visualizer.py
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from slideshow_visualizer import play_sort_slideshow


class _Node:
    __slots__ = ("val", "left", "right")
    def __init__(self, v): self.val = v; self.left = self.right = None


def _insert(root, val):
    if root is None: return _Node(val)
    if val < root.val: root.left  = _insert(root.left,  val)
    else:              root.right = _insert(root.right, val)
    return root


def _inorder(node, out):
    if node:
        _inorder(node.left, out); out.append(node.val); _inorder(node.right, out)


def _tracked(arr, steps, highlights):
    root, sorted_so_far = None, []
    n = len(arr)
    remaining = arr[:]
    for i, val in enumerate(arr):
        root = _insert(root, val)
        # In-order at this point
        tmp = []; _inorder(root, tmp)
        # Show: sorted region + unsorted remainder (n elements total)
        snapshot = tmp + remaining[i + 1:]
        steps.append(snapshot[:]); highlights.append([i])


def _render(steps, highlights, title, save_path=None):
    play_sort_slideshow(
        steps,
        title=title,
        window_title="Tree Sort",
        active_sequences=highlights,
        info_sequences=[f"Insert value {i + 1} into BST" for i in range(len(steps))],
        save_path=save_path,
    )


def visualize_sort(arr=None, title="Tree Sort — Step-by-Step", save_path=None):
    if arr is None: arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 45]
    steps, highlights = [arr.copy()], [[]]
    _tracked(arr.copy(), steps, highlights)
    _render(steps, highlights, title, save_path)


if __name__ == "__main__":
    import random
    demo = random.sample(range(1, 101), 12)
    print(f"Sorting: {demo}"); visualize_sort(demo)
