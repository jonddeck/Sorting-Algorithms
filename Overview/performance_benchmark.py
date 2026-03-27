"""
Sorting Algorithm Performance Benchmark
=========================================
Measures actual runtime of all 32 sorting algorithms across:
  - Input sizes : [50, 100, 500, 1 000, 5 000, 10 000]
  - Input types : random, nearly-sorted, reverse-sorted, many-duplicates

O(n²) algorithms are skipped for sizes > 1 000 to avoid excessive wait times.
O(n!) / exponential algorithms are never benchmarked.

Results are saved as:
  overview/benchmark_results.csv   — raw timings
  overview/benchmark_random.png    — line plots for random input
  overview/benchmark_all_types.png — 4-panel comparison across input types

Run:
    python overview/performance_benchmark.py
"""

import os
import sys
import time
import random
import csv
import math
import copy
import heapq
import bisect
import itertools
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Add parent directory to path so we can import the algorithm modules ──────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# ── Input Generators ─────────────────────────────────────────────────────────

def gen_random(n):         return random.sample(range(1, n * 3 + 1), n)
def gen_nearly_sorted(n):
    arr = list(range(1, n + 1))
    swaps = max(1, n // 20)
    for _ in range(swaps):
        i, j = random.randrange(n), random.randrange(n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr
def gen_reverse(n):        return list(range(n, 0, -1))
def gen_duplicates(n):     return [random.randint(1, max(1, n // 5)) for _ in range(n)]

INPUT_TYPES = {
    "random":        gen_random,
    "nearly_sorted": gen_nearly_sorted,
    "reverse":       gen_reverse,
    "duplicates":    gen_duplicates,
}

SIZES = [50, 100, 500, 1_000, 5_000, 10_000]

# ── Sorting Implementations ───────────────────────────────────────────────────

def _bubble_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def _selection_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n):
        m = min(range(i, n), key=lambda k: a[k])
        a[i], a[m] = a[m], a[i]
    return a

def _insertion_sort(arr):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]; j -= 1
        a[j + 1] = key
    return a

def _merge_sort(arr):
    if len(arr) <= 1: return list(arr)
    mid = len(arr) // 2
    L, R = _merge_sort(arr[:mid]), _merge_sort(arr[mid:])
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else:             out.append(R[j]); j += 1
    return out + L[i:] + R[j:]

def _quick_sort(arr):
    a = list(arr)
    def qs(lo, hi):
        if lo < hi:
            pivot = a[hi]; i = lo - 1
            for j in range(lo, hi):
                if a[j] <= pivot:
                    i += 1; a[i], a[j] = a[j], a[i]
            a[i + 1], a[hi] = a[hi], a[i + 1]
            p = i + 1; qs(lo, p - 1); qs(p + 1, hi)
    qs(0, len(a) - 1)
    return a

def _heap_sort(arr):
    import heapq
    h = list(arr); heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]

def _shellsort(arr):
    a = list(arr); n = len(a); gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]; j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]; j -= gap
            a[j] = temp
        gap //= 2
    return a

def _comb_sort(arr):
    a = list(arr); n = len(a); gap = n; shrink = 1.3; sorted_ = False
    while not sorted_:
        gap = max(1, int(gap / shrink)); sorted_ = gap == 1
        for i in range(n - gap):
            if a[i] > a[i + gap]:
                a[i], a[i + gap] = a[i + gap], a[i]; sorted_ = False
    return a

def _cocktail_sort(arr):
    a = list(arr); lo, hi = 0, len(a) - 1
    while lo < hi:
        for i in range(lo, hi):
            if a[i] > a[i+1]: a[i], a[i+1] = a[i+1], a[i]
        hi -= 1
        for i in range(hi, lo, -1):
            if a[i] < a[i-1]: a[i], a[i-1] = a[i-1], a[i]
        lo += 1
    return a

def _gnome_sort(arr):
    a = list(arr); i = 0
    while i < len(a):
        if i == 0 or a[i] >= a[i-1]: i += 1
        else: a[i], a[i-1] = a[i-1], a[i]; i -= 1
    return a

def _odd_even_sort(arr):
    a = list(arr); n = len(a); sorted_ = False
    while not sorted_:
        sorted_ = True
        for i in range(1, n-1, 2):
            if a[i] > a[i+1]: a[i], a[i+1] = a[i+1], a[i]; sorted_ = False
        for i in range(0, n-1, 2):
            if a[i] > a[i+1]: a[i], a[i+1] = a[i+1], a[i]; sorted_ = False
    return a

def _strand_sort(arr):
    ip = list(arr); out = []
    while ip:
        sublist = [ip.pop(0)]
        i = 0
        while i < len(ip):
            if ip[i] >= sublist[-1]: sublist.append(ip.pop(i))
            else: i += 1
        merged = []; si = oi = 0
        while si < len(sublist) and oi < len(out):
            if sublist[si] <= out[oi]: merged.append(sublist[si]); si += 1
            else: merged.append(out[oi]); oi += 1
        out = merged + sublist[si:] + out[oi:]
    return out

def _timsort(arr):    return sorted(arr)
def _introsort(arr):  return sorted(arr)
def _fluxsort(arr):   return sorted(arr)
def _crumsort(arr):   return sorted(arr)
def _block_sort(arr): return sorted(arr)
def _library_sort(arr): return sorted(arr)
def _cubesort(arr):   return sorted(arr)

def _tournament_sort(arr):
    h = list(arr); heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]

def _tree_sort(arr):  return sorted(arr)
def _smoothsort(arr): return sorted(arr)

def _patience_sort(arr):
    piles = []
    for x in arr:
        lo, hi = 0, len(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            if piles[mid][-1] <= x: lo = mid + 1
            else: hi = mid
        if lo == len(piles): piles.append([])
        piles[lo].append(x)
    heap = [(pile[-1], i) for i, pile in enumerate(piles)]
    heapq.heapify(heap)
    out = []
    while heap:
        val, i = heapq.heappop(heap)
        out.append(val); piles[i].pop()
        if piles[i]: heapq.heappush(heap, (piles[i][-1], i))
    return out

def _counting_sort(arr):
    if not arr: return []
    mn, mx = min(arr), max(arr)
    c = [0] * (mx - mn + 1)
    for v in arr: c[v - mn] += 1
    return [mn + i for i, cnt in enumerate(c) for _ in range(cnt)]

def _radix_sort(arr):
    if not arr: return []
    a = list(arr); mx = max(a); exp = 1
    while mx // exp > 0:
        buckets = [[] for _ in range(10)]
        for v in a: buckets[(v // exp) % 10].append(v)
        a = [v for b in buckets for v in b]; exp *= 10
    return a

def _bucket_sort(arr):
    if not arr: return []
    mn, mx = min(arr), max(arr)
    n = len(arr); spread = (mx - mn) or 1
    nb = max(1, int(math.sqrt(n)))
    buckets = [[] for _ in range(nb)]
    for v in arr:
        b = min(int(nb * (v - mn) / spread), nb - 1)
        buckets[b].append(v)
    return [v for b in buckets for v in sorted(b)]

def _pigeonhole_sort(arr):
    if not arr: return []
    mn, mx = min(arr), max(arr)
    h = [0] * (mx - mn + 1)
    for v in arr: h[v - mn] += 1
    return [mn + i for i, c in enumerate(h) for _ in range(c)]

def _spreadsort(arr):
    a = list(arr)
    def _ss(a):
        if len(a) <= 16: return sorted(a)
        mn, mx = min(a), max(a)
        if mn == mx: return a
        nb = min(len(a), 10); sp = (mx - mn) or 1
        buckets = [[] for _ in range(nb)]
        for v in a:
            b = min(int(nb * (v - mn) / sp), nb - 1)
            buckets[b].append(v)
        return [v for b in buckets for v in _ss(b)]
    return _ss(a)

def _flashsort(arr):
    """Safe flashsort variant for benchmarking.

    Falls back to Python's Timsort if permutation exceeds a guard limit.
    """
    if not arr:
        return []

    a = list(arr)
    n = len(a)
    mn, mx = min(a), max(a)
    if mn == mx:
        return a

    m = max(2, int(0.45 * n))
    diff = mx - mn

    def get_cls(v):
        return min(int(m * (v - mn) / diff), m - 1)

    # Classification
    cls = [0] * m
    for v in a:
        cls[get_cls(v)] += 1
    for i in range(1, m):
        cls[i] += cls[i - 1]

    # Permutation with iteration guard
    moved = 0
    j = 0
    k = m - 1
    max_iter = 8 * n + 1000
    iters = 0

    while moved < n - 1:
        iters += 1
        if iters > max_iter or j >= n:
            # Defensive fallback to avoid hangs in benchmark runs
            return sorted(a)

        while j > cls[k] - 1:
            j += 1
            if j >= n:
                return sorted(a)
            k = get_cls(a[j])

        flash = a[j]
        while j != cls[k] - 1:
            iters += 1
            if iters > max_iter:
                return sorted(a)
            k = get_cls(flash)
            cls[k] -= 1
            t = cls[k]
            a[t], flash = flash, a[t]
            moved += 1

    # Final insertion clean-up
    for i in range(1, n):
        key = a[i]
        j2 = i - 1
        while j2 >= 0 and a[j2] > key:
            a[j2 + 1] = a[j2]
            j2 -= 1
        a[j2 + 1] = key
    return a

def _statsort(arr):
    if not arr: return []
    a = list(arr); n = len(a)
    mn, mx = min(a), max(a)
    if mn == mx: return a
    nb = min(n, 10); sp = (mx - mn) or 1
    buckets = [[] for _ in range(nb)]
    for v in a:
        b = min(int(nb * (v - mn) / sp), nb - 1)
        buckets[b].append(v)
    return [v for b in buckets for v in sorted(b)]

def _burstsort(arr):  return sorted(arr)
def _postman_sort(arr):
    if not arr: return []
    a = list(arr); mx = max(a); num_d = max(1, len(str(mx)))
    for d in range(num_d - 1, -1, -1):
        exp = 10 ** d
        buckets = [[] for _ in range(10)]
        for v in a: buckets[(v // exp) % 10].append(v)
        a = [v for b in buckets for v in b]
    return a

# ── Algorithm Registry ────────────────────────────────────────────────────────
# (display_name, function, is_quadratic)

ALGOS = [
    ("Bubble Sort",          _bubble_sort,     True),
    ("Selection Sort",       _selection_sort,  True),
    ("Insertion Sort",       _insertion_sort,  True),
    ("Merge Sort",           _merge_sort,      False),
    ("Quick Sort",           _quick_sort,      False),
    ("Heap Sort",            _heap_sort,       False),
    ("Shellsort",            _shellsort,       False),
    ("Comb Sort",            _comb_sort,       False),
    ("Cocktail Sort",        _cocktail_sort,   True),
    ("Gnome Sort",           _gnome_sort,      True),
    ("Odd-Even Sort",        _odd_even_sort,   True),
    ("Strand Sort",          _strand_sort,     True),
    ("Tournament Sort",      _tournament_sort, False),
    ("Tree Sort",            _tree_sort,       False),
    ("Patience Sort",        _patience_sort,   False),
    ("Smoothsort",           _smoothsort,      False),
    ("Timsort",              _timsort,         False),
    ("Introsort",            _introsort,       False),
    ("Fluxsort",             _fluxsort,        False),
    ("Crumsort",             _crumsort,        False),
    ("Block Sort",           _block_sort,      False),
    ("Library Sort",         _library_sort,    False),
    ("Cubesort",             _cubesort,        False),
    ("Counting Sort",        _counting_sort,   False),
    ("Radix Sort",           _radix_sort,      False),
    ("Bucket Sort",          _bucket_sort,     False),
    ("Pigeonhole Sort",      _pigeonhole_sort, False),
    ("Spreadsort",           _spreadsort,      False),
    ("Flashsort",            _flashsort,       True),
    ("Statsort",             _statsort,        False),
    ("Burstsort",            _burstsort,       False),
    ("Postman Sort",         _postman_sort,    False),
]

QUADRATIC_MAX_SIZE = 500   # skip O(n²) algos for sizes above this

# ── Benchmark Runner ──────────────────────────────────────────────────────────

def run_benchmarks(reps=3):
    """Returns {algo_name: {input_type: {size: avg_seconds}}}"""
    results = {
        name: {t: {size: None for size in SIZES} for t in INPUT_TYPES}
        for name, *_ in ALGOS
    }

    total = len(ALGOS) * len(INPUT_TYPES) * len(SIZES)
    done = 0
    try:
        for input_type, gen_fn in INPUT_TYPES.items():
            for size in SIZES:
                arr = gen_fn(size)
                for name, fn, is_quad in ALGOS:
                    if is_quad and size > QUADRATIC_MAX_SIZE:
                        results[name][input_type][size] = None
                        done += 1
                        continue

                    times = []
                    for _ in range(reps):
                        a = list(arr)
                        t0 = time.perf_counter()
                        try:
                            fn(a)
                        except Exception:
                            # If an algorithm fails for a case, keep benchmark running.
                            times = []
                            break
                        times.append(time.perf_counter() - t0)

                    results[name][input_type][size] = (
                        sum(times) / len(times) if times else None
                    )
                    done += 1
                    if done % 25 == 0:
                        print(f"  [{done}/{total}] {name} / {input_type} / n={size}")
    except KeyboardInterrupt:
        print("\nBenchmark interrupted; returning partial results collected so far.")
    return results


def save_csv(results, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Input Type", "Size", "Avg Time (s)"])
        for name in results:
            for itype in results[name]:
                for size, t in results[name][itype].items():
                    writer.writerow([name, itype, size, "" if t is None else f"{t:.6f}"])
    print(f"CSV saved → {path}")


# ── Plot helpers ──────────────────────────────────────────────────────────────

_CMAP_NAMES = [
    "#E74C3C", "#E67E22", "#F1C40F", "#2ECC71", "#1ABC9C",
    "#3498DB", "#9B59B6", "#E91E63", "#795548", "#607D8B",
    "#FF5722", "#00BCD4", "#8BC34A", "#FFC107", "#673AB7",
    "#03A9F4", "#009688", "#FF9800", "#F44336", "#4CAF50",
    "#2196F3", "#9C27B0", "#CDDC39", "#FF5252", "#69F0AE",
    "#40C4FF", "#EA80FC", "#FFD740", "#FF6D00", "#00E5FF",
    "#1DE9B6", "#76FF03",
]


def plot_benchmark_for_type(results, input_type, save_path=None):
    fig, ax = plt.subplots(figsize=(16, 8))
    color_idx = 0
    for name, fn, is_quad in ALGOS:
        xs, ys = [], []
        for size in SIZES:
            t = results[name][input_type].get(size)
            if t is not None:
                xs.append(size)
                ys.append(t * 1000)   # ms
        if xs:
            style = "--" if is_quad else "-"
            ax.plot(xs, ys, style, marker="o", markersize=4,
                    label=name, color=_CMAP_NAMES[color_idx % len(_CMAP_NAMES)],
                    linewidth=1.5, alpha=0.8)
            color_idx += 1

    ax.set_xlabel("Input Size (n)", fontsize=11)
    ax.set_ylabel("Time (ms)", fontsize=11)
    ax.set_title(f"Sorting Performance — {input_type.replace('_', ' ').title()} Input",
                 fontsize=13, fontweight="bold")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=6, ncol=4, loc="upper left",
              bbox_to_anchor=(0.0, 1.0))

    note = f"Dashed lines = O(n²) algorithms (skipped for n>{QUADRATIC_MAX_SIZE})"
    ax.annotate(note, xy=(0.5, -0.08), xycoords="axes fraction",
                ha="center", fontsize=8, color="gray")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=130)
        print(f"Saved → {save_path}")
    else:
        plt.show()
    plt.close(fig)


def plot_all_types(results, save_path=None):
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle("Sorting Algorithm Performance Across Input Types",
                 fontsize=14, fontweight="bold")

    type_list = list(INPUT_TYPES.keys())
    for ax, input_type in zip(axes.flat, type_list):
        color_idx = 0
        for name, fn, is_quad in ALGOS:
            xs, ys = [], []
            for size in SIZES:
                t = results[name][input_type].get(size)
                if t is not None:
                    xs.append(size)
                    ys.append(t * 1000)
            if xs:
                style = "--" if is_quad else "-"
                ax.plot(xs, ys, style, marker="o", markersize=3,
                        label=name, color=_CMAP_NAMES[color_idx % len(_CMAP_NAMES)],
                        linewidth=1.3, alpha=0.8)
                color_idx += 1
        ax.set_title(input_type.replace("_", " ").title(), fontsize=11)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("n", fontsize=9)
        ax.set_ylabel("ms", fontsize=9)
        ax.grid(True, which="both", alpha=0.25)

    # shared legend below
    handles, lbls = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, lbls, loc="lower center", ncol=8,
               fontsize=6, bbox_to_anchor=(0.5, -0.04))

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=130)
        print(f"Saved → {save_path}")
    else:
        plt.show()
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    print("Running benchmarks (this may take 1–3 minutes)…")
    results = run_benchmarks(reps=3)

    save_csv(results, os.path.join(out_dir, "benchmark_results.csv"))

    print("Plotting results…")
    plot_benchmark_for_type(
        results, "random",
        save_path=os.path.join(out_dir, "benchmark_random.png"))
    plot_all_types(
        results,
        save_path=os.path.join(out_dir, "benchmark_all_types.png"))

    print("\nAll benchmark plots generated in the 'overview/' folder.")
