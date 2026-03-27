"""
All Sorts Visualizer (Clear Mode)
=================================
Single-image step player for sorting algorithms.

Display format per step:
  - Left chart : Current state (before applying step)
  - Right chart: Changed order (after step)
  - Delay      : 2 seconds between steps (configurable)

This gives a clearer visual evolution than multi-frame grid snapshots.

Run:
    python overview/all_sorts_visualizer.py

Menu options let you choose which type of sorting algorithms to run:
    - Comparison
    - Non-Comparison
    - Hybrid
    - All
"""

import random
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button

sys.path.append(str(Path(__file__).resolve().parents[1]))


# ── Step trackers (core representatives) ─────────────────────────────────────

def track_bubble(arr):
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                steps.append(a.copy())
                highlights.append([j, j + 1])
    return steps, highlights


def track_selection(arr):
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]
    n = len(a)
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            steps.append(a.copy())
            highlights.append([i, m])
    return steps, highlights


def track_insertion(arr):
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            steps.append(a.copy())
            highlights.append([j + 1, j + 2])
        a[j + 1] = key
        steps.append(a.copy())
        highlights.append([j + 1])
    return steps, highlights


def track_merge(arr):
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]

    def merge(lo, mid, hi):
        tmp = []
        i, j = lo, mid + 1
        while i <= mid and j <= hi:
            if a[i] <= a[j]:
                tmp.append(a[i]); i += 1
            else:
                tmp.append(a[j]); j += 1
        while i <= mid:
            tmp.append(a[i]); i += 1
        while j <= hi:
            tmp.append(a[j]); j += 1
        for k, v in enumerate(tmp):
            a[lo + k] = v
        steps.append(a.copy())
        highlights.append(list(range(lo, hi + 1)))

    def sort(lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid + 1, hi)
        merge(lo, mid, hi)

    sort(0, len(a) - 1)
    return steps, highlights


def track_quick(arr):
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]

    def partition(lo, hi):
        p = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            if a[j] <= p:
                i += 1
                a[i], a[j] = a[j], a[i]
                steps.append(a.copy())
                highlights.append([i, j])
        a[i + 1], a[hi] = a[hi], a[i + 1]
        steps.append(a.copy())
        highlights.append([i + 1, hi])
        return i + 1

    def sort(lo, hi):
        if lo < hi:
            pi = partition(lo, hi)
            sort(lo, pi - 1)
            sort(pi + 1, hi)

    sort(0, len(a) - 1)
    return steps, highlights


def track_counting(arr):
    if not arr:
        return [[]], [[]]
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]
    mn, mx = min(a), max(a)
    c = [0] * (mx - mn + 1)
    for i, v in enumerate(a):
        c[v - mn] += 1
    out = [0] * len(a)
    k = 0
    for i, cnt in enumerate(c):
        for _ in range(cnt):
            out[k] = i + mn
            steps.append(out.copy())
            highlights.append([k])
            k += 1
    return steps, highlights


def track_radix(arr):
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]
    if not a:
        return steps, highlights
    m = max(a)
    exp = 1
    while m // exp > 0:
        buckets = [[] for _ in range(10)]
        for v in a:
            buckets[(v // exp) % 10].append(v)
        a = [v for b in buckets for v in b]
        steps.append(a.copy())
        highlights.append(list(range(len(a))))
        exp *= 10
    return steps, highlights


def track_timsort(arr):
    # Fallback tracked version: progressively build sorted prefix
    a = list(arr)
    steps = [a.copy()]
    highlights = [[]]
    for i in range(1, len(a) + 1):
        prefix = sorted(a[:i])
        new_a = prefix + a[i:]
        steps.append(new_a.copy())
        highlights.append(list(range(i)))
    return steps, highlights


ALGO_TRACKERS = {
    "Bubble Sort": track_bubble,
    "Selection Sort": track_selection,
    "Insertion Sort": track_insertion,
    "Merge Sort": track_merge,
    "Quick Sort": track_quick,
    "Counting Sort": track_counting,
    "Radix Sort": track_radix,
    "Timsort": track_timsort,
}

ALGO_TYPES = {
    "comparison": [
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort",
        "Merge Sort",
        "Quick Sort",
    ],
    "non-comparison": [
        "Counting Sort",
        "Radix Sort",
    ],
    "hybrid": [
        "Timsort",
    ],
}


def _selection_options():
    options = [
        "All Sorts",
        "Comparison Sorts",
        "Non-Comparison Sorts",
        "Hybrid Sorts",
    ]
    options.extend(list(ALGO_TRACKERS.keys()))
    return options


def _algorithms_from_selection(selection):
    if selection == "All Sorts":
        return list(ALGO_TRACKERS.keys())
    if selection == "Comparison Sorts":
        return ALGO_TYPES["comparison"]
    if selection == "Non-Comparison Sorts":
        return ALGO_TYPES["non-comparison"]
    if selection == "Hybrid Sorts":
        return ALGO_TYPES["hybrid"]
    if selection in ALGO_TRACKERS:
        return [selection]
    return []


# ── Single Window Runner (with in-window dropdown) ──────────────────────────

def launch_overview_window():
    """Open one visualizer window with in-window selector and step controls."""
    base = random.sample(range(5, 80), 14)
    options = _selection_options()
    cache = {}

    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    fig.patch.set_facecolor("#F8F9FA")
    plt.subplots_adjust(bottom=0.20, top=0.78)

    manager = getattr(fig.canvas, "manager", None)
    if manager is not None and hasattr(manager, "set_window_title"):
        manager.set_window_title("All Sorts Visualizer")

    fig.suptitle("All Sorts Visualizer", fontsize=16, fontweight="bold", color="#1F2D3D", y=0.975)
    subtitle = fig.text(0.5, 0.93, "Use selector buttons, then click Load", ha="center", fontsize=10, color="#5D6D7E")

    selector_text = fig.text(
        0.5,
        0.885,
        "Selection: All Sorts",
        ha="center",
        fontsize=10,
        color="#334E68",
        fontweight="bold",
    )

    legend_items = [
        mpatches.Patch(color="#3498DB", label="Inactive Items"),
        mpatches.Patch(color="#F39C12", label="Switched Items"),
        mpatches.Patch(color="#E74C3C", label="Active Block"),
        mpatches.Patch(color="#2ECC71", label="Final Sorted"),
    ]
    fig.legend(handles=legend_items, loc="lower center", ncol=4, frameon=False,
               bbox_to_anchor=(0.5, 0.02), fontsize=9)

    selector_prev_ax = fig.add_axes([0.18, 0.835, 0.09, 0.05])
    selector_next_ax = fig.add_axes([0.73, 0.835, 0.09, 0.05])
    load_ax = fig.add_axes([0.84, 0.835, 0.11, 0.05])

    button_home_ax = fig.add_axes([0.16, 0.08, 0.12, 0.07])
    button_prev_ax = fig.add_axes([0.31, 0.08, 0.12, 0.07])
    button_next_ax = fig.add_axes([0.46, 0.08, 0.12, 0.07])
    button_end_ax = fig.add_axes([0.61, 0.08, 0.12, 0.07])

    btn_sel_prev = Button(selector_prev_ax, "◀")
    btn_sel_next = Button(selector_next_ax, "▶")
    btn_load = Button(load_ax, "Load")

    btn_home = Button(button_home_ax, "Home")
    btn_prev = Button(button_prev_ax, "Previous")
    btn_next = Button(button_next_ax, "Next")
    btn_end = Button(button_end_ax, "End")

    state = {
        "selection": "All Sorts",
        "pending_selection": "All Sorts",
        "pending_index": 0,
        "names": [],
        "algo_idx": 0,
        "step_idx": 0,
        "steps": [[]],
        "highlights": [[]],
    }

    def _get_algo_steps(name):
        if name not in cache:
            tracker = ALGO_TRACKERS[name]
            steps, highlights = tracker(base)
            if not steps:
                steps, highlights = [base.copy()], [[]]
            cache[name] = (steps, highlights)
        return cache[name]

    def _load_current_algorithm(reset_to_first_step=True):
        if not state["names"]:
            state["steps"], state["highlights"] = [base.copy()], [[]]
            state["algo_idx"] = 0
            state["step_idx"] = 0
            subtitle.set_text("No algorithms for selection")
            return

        current_name = state["names"][state["algo_idx"]]
        steps, highlights = _get_algo_steps(current_name)
        state["steps"] = steps
        state["highlights"] = highlights
        if reset_to_first_step:
            state["step_idx"] = 0

    def _set_selection(selection):
        state["selection"] = selection
        state["pending_selection"] = selection
        if selection in options:
            state["pending_index"] = options.index(selection)
        state["names"] = _algorithms_from_selection(selection)
        state["algo_idx"] = 0
        _load_current_algorithm(reset_to_first_step=True)
        _draw()

    def _load_pending(_event=None):
        _set_selection(state.get("pending_selection", "All Sorts"))

    def _refresh_selector_text():
        selector_text.set_text(f"Selection: {state['pending_selection']}")

    def _cycle_selector(direction):
        idx = state["pending_index"]
        idx = (idx + direction) % len(options)
        state["pending_index"] = idx
        state["pending_selection"] = options[idx]
        _refresh_selector_text()
        subtitle.set_text(f"Pending selection: {state['pending_selection']}  — click Load")
        fig.canvas.draw_idle()

    def _draw():
        steps = state["steps"]
        highlights = state["highlights"]
        if not steps:
            return

        idx = state["step_idx"]
        step = steps[idx]
        prev = steps[idx - 1] if idx > 0 else step
        active = set(highlights[idx]) if idx < len(highlights) else set()
        switched = {j for j in range(len(step)) if prev[j] != step[j]}
        is_final = idx == len(steps) - 1

        max_val = max((max(s) if s else 0) for s in steps) or 1

        ax.clear()
        ax.set_facecolor("#FFFFFF")

        colors = []
        for j in range(len(step)):
            if is_final:
                colors.append("#2ECC71")
            elif j in active:
                colors.append("#E74C3C")
            elif j in switched:
                colors.append("#F39C12")
            else:
                colors.append("#3498DB")

        ax.bar(range(len(step)), step, color=colors, edgecolor="white", linewidth=0.6, width=0.82)
        ax.set_ylim(0, max_val * 1.15)
        ax.set_xticks([])
        ax.set_yticks([])

        current_name = state["names"][state["algo_idx"]] if state["names"] else "None"
        ax.set_title(f"{current_name} — Step {idx + 1} of {len(steps)}", fontsize=11, pad=10,
                     color="#334E68", fontweight="bold")

        subtitle.set_text(
            f"Selection: {state['selection']}    |    Algorithm {state['algo_idx'] + 1} of {max(1, len(state['names']))}"
        )

        active_text = "None" if not active else ", ".join(str(v) for v in sorted(active))
        switched_text = "None" if not switched else ", ".join(str(v) for v in sorted(switched))
        ax.set_xlabel(
            f"Active block: {active_text}    |    Switched items: {switched_text}",
            fontsize=10,
            color="#3E4C59",
            labelpad=12,
        )

        for spine in ax.spines.values():
            spine.set_linewidth(0.8)
            spine.set_color("#D9E2EC")

        fig.canvas.draw_idle()

    def _home(_event=None):
        state["step_idx"] = 0
        _draw()

    def _prev(_event=None):
        if state["step_idx"] > 0:
            state["step_idx"] -= 1
            _draw()
            return
        if state["algo_idx"] > 0:
            state["algo_idx"] -= 1
            _load_current_algorithm(reset_to_first_step=False)
            state["step_idx"] = max(0, len(state["steps"]) - 1)
            _draw()

    def _next(_event=None):
        if state["step_idx"] < len(state["steps"]) - 1:
            state["step_idx"] += 1
            _draw()
            return
        if state["algo_idx"] < len(state["names"]) - 1:
            state["algo_idx"] += 1
            _load_current_algorithm(reset_to_first_step=True)
            _draw()
            return

    def _end(_event=None):
        if state["steps"]:
            state["step_idx"] = max(0, len(state["steps"]) - 1)
            _draw()

    def _selector_prev(_event=None):
        _cycle_selector(-1)

    def _selector_next(_event=None):
        _cycle_selector(1)

    btn_sel_prev.on_clicked(_selector_prev)
    btn_sel_next.on_clicked(_selector_next)
    btn_load.on_clicked(_load_pending)
    btn_home.on_clicked(_home)
    btn_prev.on_clicked(_prev)
    btn_next.on_clicked(_next)
    btn_end.on_clicked(_end)

    _set_selection("All Sorts")
    _refresh_selector_text()
    plt.show()


if __name__ == "__main__":
    launch_overview_window()
