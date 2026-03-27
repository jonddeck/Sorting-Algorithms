"""Shared interactive slideshow renderer for sorting visualizers."""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button


def _normalize_active(step, active_data):
    if active_data is None:
        return set()
    if isinstance(active_data, (set, tuple, list)):
        seq = list(active_data)
        if len(seq) == len(step) and all(isinstance(v, (int, bool)) for v in seq):
            values = set(seq)
            if values.issubset({0, 1, 2, False, True}):
                return {i for i, value in enumerate(seq) if int(value) > 0}
        return {int(v) for v in seq if isinstance(v, (int, bool))}
    return set()


def play_sort_slideshow(
    steps,
    *,
    title,
    active_sequences=None,
    info_sequences=None,
    window_title=None,
    save_path=None,
    step_delay=2.0,
    max_steps=20,
):
    if not steps:
        print("No steps to render.")
        return

    if active_sequences is None:
        active_sequences = [[] for _ in steps]
    if info_sequences is None:
        info_sequences = ["" for _ in steps]

    if len(steps) > max_steps:
        indices = [int(round(i * (len(steps) - 1) / (max_steps - 1))) for i in range(max_steps)]
        steps = [steps[i] for i in indices]
        active_sequences = [active_sequences[i] for i in indices]
        info_sequences = [info_sequences[i] for i in indices]

    max_val = max((max(step) if step else 0) for step in steps) or 1

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor("#F8F9FA")
    plt.subplots_adjust(bottom=0.22, top=0.84)

    manager = getattr(fig.canvas, "manager", None)
    if manager is not None and hasattr(manager, "set_window_title"):
        manager.set_window_title(window_title or title)

    title_artist = fig.suptitle(
        title,
        fontsize=16,
        fontweight="bold",
        color="#1F2D3D",
        y=0.95,
    )
    subtitle_artist = fig.text(
        0.5,
        0.90,
        "",
        ha="center",
        va="center",
        fontsize=10,
        color="#5D6D7E",
    )

    legend_items = [
        mpatches.Patch(color="#3498DB", label="Inactive Items"),
        mpatches.Patch(color="#F39C12", label="Switched Items"),
        mpatches.Patch(color="#E74C3C", label="Active Block"),
        mpatches.Patch(color="#2ECC71", label="Final Sorted"),
    ]
    fig.legend(
        handles=legend_items,
        loc="lower center",
        ncol=4,
        frameon=False,
        bbox_to_anchor=(0.5, 0.02),
        fontsize=9,
    )

    button_home_ax = fig.add_axes([0.10, 0.10, 0.12, 0.07])
    button_prev_ax = fig.add_axes([0.25, 0.10, 0.12, 0.07])
    button_play_ax = fig.add_axes([0.40, 0.10, 0.12, 0.07])
    button_pause_ax = fig.add_axes([0.55, 0.10, 0.12, 0.07])
    button_next_ax = fig.add_axes([0.70, 0.10, 0.12, 0.07])

    btn_home = Button(button_home_ax, "Home")
    btn_prev = Button(button_prev_ax, "Previous")
    btn_play = Button(button_play_ax, "Play")
    btn_pause = Button(button_pause_ax, "Pause")
    btn_next = Button(button_next_ax, "Next")

    state = {"index": 0, "playing": False}
    timer = fig.canvas.new_timer(interval=max(100, int(step_delay * 1000)))

    def _draw(index):
        step = steps[index]
        prev = steps[index - 1] if index > 0 else step
        active = _normalize_active(step, active_sequences[index])
        switched = {j for j in range(len(step)) if prev[j] != step[j]}
        is_final = index == len(steps) - 1

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
        ax.set_title(
            f"Step {index + 1} of {len(steps)}",
            fontsize=11,
            pad=10,
            color="#334E68",
            fontweight="bold",
        )
        info = info_sequences[index] if index < len(info_sequences) else ""
        subtitle_artist.set_text(info or "Use Previous / Next or Play / Pause to navigate")

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

    def _next(_event=None):
        if state["index"] < len(steps) - 1:
            state["index"] += 1
            _draw(state["index"])
        else:
            state["playing"] = False
            timer.stop()

    def _home(_event=None):
        state["playing"] = False
        timer.stop()
        state["index"] = 0
        _draw(state["index"])

    def _prev(_event=None):
        if state["index"] > 0:
            state["index"] -= 1
            _draw(state["index"])

    def _play(_event=None):
        state["playing"] = True
        timer.start()

    def _pause(_event=None):
        state["playing"] = False
        timer.stop()

    def _tick():
        if state["playing"]:
            _next()

    def _stop_on_close(_event):
        state["playing"] = False
        timer.stop()

    timer.add_callback(_tick)
    btn_home.on_clicked(_home)
    btn_prev.on_clicked(_prev)
    btn_next.on_clicked(_next)
    btn_play.on_clicked(_play)
    btn_pause.on_clicked(_pause)
    fig.canvas.mpl_connect("close_event", _stop_on_close)

    _draw(state["index"])

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved to '{save_path}'")

    plt.show()
