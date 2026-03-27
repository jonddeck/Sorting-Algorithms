"""
Sorting Algorithm Complexity Comparison
========================================
Generates two figures:
  1. A formatted table of all 32 sorting algorithms with
     Best / Average / Worst time complexity, Space complexity,
     Stable flag, and In-Place flag.
  2. A grouped bar chart scoring each algorithm on log-scale
     complexity (Best / Average / Worst) for quick visual comparison.

Run:
    python overview/complexity_comparison.py
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os


# ── Data ─────────────────────────────────────────────────────────────────────
# (name, best, avg, worst, space, stable, in_place, category)
# Complexity is stored as exponent of n (0=O(1), 1=O(n), 1.5=O(n√n), 2=O(n²))
# with special values: log=0.3 (O(log n)), nlog=1.3 (O(n log n)), nlog2=1.6

ALGORITHMS = [
    # ── Comparison Sorts ────────────────────────────────────────────────────
    ("Bubble Sort",          "O(n)",        "O(n²)",       "O(n²)",       "O(1)",      True,  True,  "Comparison"),
    ("Selection Sort",       "O(n²)",       "O(n²)",       "O(n²)",       "O(1)",      False, True,  "Comparison"),
    ("Insertion Sort",       "O(n)",        "O(n²)",       "O(n²)",       "O(1)",      True,  True,  "Comparison"),
    ("Merge Sort",           "O(n log n)",  "O(n log n)",  "O(n log n)",  "O(n)",      True,  False, "Comparison"),
    ("Quick Sort",           "O(n log n)",  "O(n log n)",  "O(n²)",       "O(log n)",  False, True,  "Comparison"),
    ("Heap Sort",            "O(n log n)",  "O(n log n)",  "O(n log n)",  "O(1)",      False, True,  "Comparison"),
    ("Shellsort",            "O(n log n)",  "O(n log² n)", "O(n²)",       "O(1)",      False, True,  "Comparison"),
    ("Comb Sort",            "O(n log n)",  "O(n²/2ᵖ)",   "O(n²)",       "O(1)",      False, True,  "Comparison"),
    ("Cocktail Shaker Sort", "O(n)",        "O(n²)",       "O(n²)",       "O(1)",      True,  True,  "Comparison"),
    ("Gnome Sort",           "O(n)",        "O(n²)",       "O(n²)",       "O(1)",      True,  True,  "Comparison"),
    ("Odd-Even Sort",        "O(n)",        "O(n²)",       "O(n²)",       "O(1)",      True,  True,  "Comparison"),
    ("Strand Sort",          "O(n)",        "O(n²)",       "O(n²)",       "O(n)",      True,  False, "Comparison"),
    ("Tournament Sort",      "O(n log n)",  "O(n log n)",  "O(n log n)",  "O(n)",      False, False, "Comparison"),
    ("Tree Sort",            "O(n log n)",  "O(n log n)",  "O(n²)",       "O(n)",      True,  False, "Comparison"),
    ("Patience Sort",        "O(n log n)",  "O(n log n)",  "O(n log n)",  "O(n)",      True,  False, "Comparison"),
    ("Smoothsort",           "O(n)",        "O(n log n)",  "O(n log n)",  "O(1)",      False, True,  "Comparison"),
    # ── Hybrid Sorts ────────────────────────────────────────────────────────
    ("Timsort",              "O(n)",        "O(n log n)",  "O(n log n)",  "O(n)",      True,  False, "Hybrid"),
    ("Introsort",            "O(n log n)",  "O(n log n)",  "O(n log n)",  "O(log n)",  False, True,  "Hybrid"),
    ("Fluxsort",             "O(n)",        "O(n log n)",  "O(n log n)",  "O(n)",      True,  False, "Hybrid"),
    ("Crumsort",             "O(n)",        "O(n log n)",  "O(n log n)",  "O(1)",      False, True,  "Hybrid"),
    ("Block Sort",           "O(n)",        "O(n log n)",  "O(n log n)",  "O(1)",      True,  True,  "Hybrid"),
    ("Library Sort",         "O(n log n)",  "O(n log n)",  "O(n log n)",  "O(n)",      True,  False, "Hybrid"),
    ("Cubesort",             "O(n)",        "O(n log n)",  "O(n log n)",  "O(n)",      True,  False, "Hybrid"),
    # ── Non-Comparison Sorts ────────────────────────────────────────────────
    ("Counting Sort",        "O(n+k)",      "O(n+k)",      "O(n+k)",      "O(n+k)",    True,  False, "Non-Comparison"),
    ("Radix Sort",           "O(nk)",       "O(nk)",       "O(nk)",       "O(n+k)",    True,  False, "Non-Comparison"),
    ("Bucket Sort",          "O(n+k)",      "O(n+k)",      "O(n²)",       "O(n+k)",    True,  False, "Non-Comparison"),
    ("Pigeonhole Sort",      "O(n+k)",      "O(n+k)",      "O(n+k)",      "O(n+k)",    True,  False, "Non-Comparison"),
    ("Spreadsort",           "O(n)",        "O(n·√(log n)","O(n·k/s)",    "O(n)",      False, False, "Non-Comparison"),
    ("Burstsort",            "O(wn)",       "O(wn log n)", "O(wn log n)", "O(wn)",     False, False, "Non-Comparison"),
    ("Flashsort",            "O(n)",        "O(n)",        "O(n²)",       "O(n)",      False, True,  "Non-Comparison"),
    ("Statsort",             "O(n)",        "O(n)",        "O(n²)",       "O(n)",      False, False, "Non-Comparison"),
    ("Postman Sort",         "O(nk)",       "O(nk)",       "O(nk)",       "O(n+k)",    True,  False, "Non-Comparison"),
]

# Numeric score for bar chart (lower = better): maps complexity label to score
_COMPLEXITY_SCORE = {
    "O(1)":         0,
    "O(log n)":     0.3,
    "O(n)":         1.0,
    "O(wn)":        1.1,
    "O(n+k)":       1.1,
    "O(nk)":        1.2,
    "O(n·√(log n)": 1.4,
    "O(n·k/s)":     1.5,
    "O(n log n)":   1.6,
    "O(n log² n)":  1.9,
    "O(n²/2ᵖ)":    2.0,
    "O(n²)":        2.0,
    "O(wn log n)":  2.2,
}

def _score(s):
    return _COMPLEXITY_SCORE.get(s, 1.5)


# ── Figure 1: Table ────────────────────────────────────────────────────────

def plot_complexity_table(save_path=None):
    cat_colors = {
        "Comparison":     "#3498DB",
        "Hybrid":         "#9B59B6",
        "Non-Comparison": "#E67E22",
    }

    fig, ax = plt.subplots(figsize=(18, len(ALGORITHMS) * 0.45 + 2))
    ax.axis("off")

    col_labels = ["Algorithm", "Category", "Best", "Average", "Worst", "Space", "Stable", "In-Place"]
    row_data = []
    row_colors = []
    for algo in ALGORITHMS:
        name, best, avg, worst, space, stable, in_place, cat = algo
        row_data.append([
            name, cat, best, avg, worst, space,
            "✓" if stable else "✗",
            "✓" if in_place else "✗",
        ])
        base = cat_colors.get(cat, "#ECF0F1")
        row_colors.append([base] + ["#FDFEFE"] * 7)

    table = ax.table(
        cellText=row_data,
        colLabels=col_labels,
        cellColours=row_colors,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.4)

    # Style header
    for j in range(len(col_labels)):
        table[(0, j)].set_facecolor("#2C3E50")
        table[(0, j)].set_text_props(color="white", fontweight="bold")

    ax.set_title("Sorting Algorithm Complexity Reference", fontsize=14,
                 fontweight="bold", pad=10)

    # Legend
    patches = [mpatches.Patch(color=c, label=l) for l, c in cat_colors.items()]
    fig.legend(handles=patches, loc="lower center", ncol=3, fontsize=9,
               bbox_to_anchor=(0.5, 0.0))

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=130)
        print(f"Saved complexity table → {save_path}")
    else:
        plt.show()
    plt.close(fig)


# ── Figure 2: Bar chart comparison ────────────────────────────────────────

def plot_complexity_bars(save_path=None):
    names  = [a[0] for a in ALGORITHMS]
    bests  = [_score(a[1]) for a in ALGORITHMS]
    avgs   = [_score(a[2]) for a in ALGORITHMS]
    worsts = [_score(a[3]) for a in ALGORITHMS]
    cats   = [a[7] for a in ALGORITHMS]

    cat_colors = {
        "Comparison":     "#3498DB",
        "Hybrid":         "#9B59B6",
        "Non-Comparison": "#E67E22",
    }

    n = len(names)
    x = range(n)
    width = 0.25

    fig, ax = plt.subplots(figsize=(22, 8))

    bar_best  = ax.bar([i - width for i in x], bests,  width, label="Best",    color="#2ECC71", alpha=0.85)
    bar_avg   = ax.bar([i         for i in x], avgs,   width, label="Average", color="#F39C12", alpha=0.85)
    bar_worst = ax.bar([i + width for i in x], worsts, width, label="Worst",   color="#E74C3C", alpha=0.85)

    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Complexity Score (higher = worse)", fontsize=10)
    ax.set_title("Sorting Algorithm Complexity Comparison (All 32)", fontsize=13, fontweight="bold")

    ytick_labels = {
        0.0: "O(1)",
        0.3: "O(log n)",
        1.0: "O(n)",
        1.1: "O(n+k)",
        1.2: "O(nk)",
        1.6: "O(n log n)",
        1.9: "O(n log² n)",
        2.0: "O(n²)",
    }
    ax.set_yticks(sorted(ytick_labels.keys()))
    ax.set_yticklabels([ytick_labels[y] for y in sorted(ytick_labels.keys())], fontsize=8)
    ax.set_ylim(0, 2.5)

    # Category background bands
    category_spans = []
    current_cat = cats[0]
    start = 0
    for i, cat in enumerate(cats[1:], 1):
        if cat != current_cat:
            category_spans.append((current_cat, start, i))
            current_cat = cat
            start = i
    category_spans.append((current_cat, start, len(cats)))

    for cat, s, e in category_spans:
        ax.axvspan(s - 0.5, e - 0.5, alpha=0.07,
                   color=cat_colors.get(cat, "gray"), label=f"_{cat}")

    # Legends
    complexity_legend = [
        mpatches.Patch(color="#2ECC71", label="Best case"),
        mpatches.Patch(color="#F39C12", label="Average case"),
        mpatches.Patch(color="#E74C3C", label="Worst case"),
    ]
    cat_legend = [mpatches.Patch(color=c, alpha=0.3, label=l)
                  for l, c in cat_colors.items()]
    ax.legend(handles=complexity_legend + cat_legend, fontsize=8,
              loc="upper right", ncol=2)

    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=130)
        print(f"Saved complexity bars → {save_path}")
    else:
        plt.show()
    plt.close(fig)


# ── Figure 3: Stability & In-Place summary ────────────────────────────────

def plot_properties_summary(save_path=None):
    from collections import Counter

    cat_order = ["Comparison", "Hybrid", "Non-Comparison"]
    data = {c: {"stable_inplace": 0, "stable_notinplace": 0,
                "unstable_inplace": 0, "unstable_notinplace": 0}
            for c in cat_order}

    for algo in ALGORITHMS:
        _, _, _, _, _, stable, in_place, cat = algo
        key = ("stable" if stable else "unstable") + "_" + ("inplace" if in_place else "notinplace")
        data[cat][key] += 1

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Algorithm Properties by Category", fontsize=13, fontweight="bold")

    prop_colors = {
        "stable_inplace":       "#2ECC71",
        "stable_notinplace":    "#3498DB",
        "unstable_inplace":     "#E74C3C",
        "unstable_notinplace":  "#F39C12",
    }
    prop_labels = {
        "stable_inplace":      "Stable + In-place",
        "stable_notinplace":   "Stable + Extra space",
        "unstable_inplace":    "Unstable + In-place",
        "unstable_notinplace": "Unstable + Extra space",
    }

    for ax, cat in zip(axes, cat_order):
        d = data[cat]
        vals   = [d[k] for k in prop_colors]
        colors = list(prop_colors.values())
        lbls   = [f"{prop_labels[k]}\n({d[k]})" if d[k] > 0 else "" for k in prop_colors]
        non_zero = [(v, c, l) for v, c, l in zip(vals, colors, lbls) if v > 0]
        if non_zero:
            v_, c_, l_ = zip(*non_zero)
            ax.pie(v_, labels=l_, colors=c_, autopct="%1.0f%%",
                   startangle=140, textprops={"fontsize": 8})
        ax.set_title(cat, fontsize=11, fontweight="bold")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=130)
        print(f"Saved properties summary → {save_path}")
    else:
        plt.show()
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    plot_complexity_table(save_path=os.path.join(out_dir, "complexity_table.png"))
    plot_complexity_bars(save_path=os.path.join(out_dir, "complexity_bars.png"))
    plot_properties_summary(save_path=os.path.join(out_dir, "properties_summary.png"))
    print("\nAll overview charts generated in the 'overview/' folder.")
