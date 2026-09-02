"""
analysis/performance.py
───────────────────────
Utilities for measuring execution time, peak memory usage,
and comparison counts for the sorting and Fibonacci algorithms.

Design choices
--------------
• Each measurement is repeated ``NUM_RUNS`` times and the *median* is
  recorded.  The median is more robust than the mean because it is not
  skewed by the occasional long pause caused by the operating system
  scheduler or garbage collection.
• Execution time is measured with ``time.perf_counter()``, the highest-
  resolution clock available on both Windows and Linux.
• Memory is measured with ``tracemalloc``, which tracks *heap* allocations
  made by Python objects.  It reports the *peak* allocation during the
  measured call, which corresponds to the algorithm's auxiliary space.
• A fixed random seed (RANDOM_SEED = 42) is used for all dataset
  generation so results are fully reproducible.

Student : RAKESH G
Roll No : 2401201064
Course  : BCA (AI & DS) — K.R. Mangalam University
Lab     : Lab 1 — Design and Analysis of Algorithms
"""

import time
import tracemalloc
import random
import statistics
import os

import pandas as pd

from algorithms.sorting import bubble_sort, insertion_sort, merge_sort, quick_sort
from algorithms.fibonacci import fib_recursive, fib_iterative, fib_dp

# ── Constants ────────────────────────────────────────────────────────────────
RANDOM_SEED = 42          # reproducible random data
NUM_RUNS    = 5           # repetitions per data point (median used)

SORTING_ALGORITHMS = {
    "Bubble Sort"    : bubble_sort,
    "Insertion Sort" : insertion_sort,
    "Merge Sort"     : merge_sort,
    "Quick Sort"     : quick_sort,
}

FIBONACCI_ALGORITHMS = {
    "Recursive"          : fib_recursive,
    "Iterative"          : fib_iterative,
    "Dynamic Programming": fib_dp,
}


# ─────────────────────────────────────────────
# Core measurement helper
# ─────────────────────────────────────────────

def measure_time_and_memory(func, *args, runs=NUM_RUNS, **kwargs):
    """
    Run *func* with the given arguments *runs* times and return the
    median execution time and peak memory usage.

    Parameters
    ----------
    func   : callable
        The function to benchmark.
    *args  : any
        Positional arguments forwarded to *func*.
    runs   : int, optional
        Number of repetitions (default 5).
    **kwargs : any
        Keyword arguments forwarded to *func*.

    Returns
    -------
    last_result   : any
        Return value from the last call to *func*.
    median_time   : float
        Median wall-clock time across all runs (seconds).
    median_memory : float
        Median peak heap allocation across all runs (bytes).
    """
    times    = []
    memories = []
    last_result = None

    for _ in range(runs):
        tracemalloc.start()
        clock_start  = time.perf_counter()
        last_result  = func(*args, **kwargs)
        elapsed      = time.perf_counter() - clock_start
        _, peak_mem  = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(elapsed)
        memories.append(peak_mem)

    return last_result, statistics.median(times), statistics.median(memories)


# ─────────────────────────────────────────────
# Dataset generation
# ─────────────────────────────────────────────

def build_sorting_datasets(n, seed=RANDOM_SEED):
    """
    Generate three input lists of length *n*: sorted, reverse-sorted, random.

    Using the same seed for every size ensures the random data differs
    only in length, not in any incidental pattern.

    Parameters
    ----------
    n    : int  — number of elements
    seed : int  — random seed for reproducibility

    Returns
    -------
    dict with keys ``'sorted'``, ``'reverse'``, ``'random'``, each mapped
    to a list of *n* integers in [0, 100000].
    """
    rng = random.Random(seed)
    random_list  = [rng.randint(0, 100_000) for _ in range(n)]
    sorted_list  = sorted(random_list)
    reverse_list = sorted(random_list, reverse=True)

    return {
        "sorted" : sorted_list,
        "reverse": reverse_list,
        "random" : random_list,
    }


# ─────────────────────────────────────────────
# Sorting experiments
# ─────────────────────────────────────────────

def run_sorting_experiments(sizes=None):
    """
    Benchmark all four sorting algorithms across the specified input sizes
    and all three input conditions (sorted, reverse, random).

    Parameters
    ----------
    sizes : list[int], optional
        Input sizes to test.  Defaults to [100, 500, 1000, 5000, 10000].

    Returns
    -------
    pandas.DataFrame
        One row per (algorithm, size, condition) combination with columns:
        Algorithm, Input Size, Input Condition, Comparisons,
        Execution Time (s), Memory Usage (bytes), Memory Usage (KB).
    """
    if sizes is None:
        sizes = [100, 500, 1000, 5000, 10000]

    records = []

    for n in sizes:
        print(f"  >> input size {n:,} ...")
        datasets = build_sorting_datasets(n)

        for condition_label, dataset in datasets.items():
            for algo_name, algo_fn in SORTING_ALGORITHMS.items():
                (sorted_arr, comparisons), t_sec, mem_bytes = measure_time_and_memory(
                    algo_fn, dataset
                )

                records.append({
                    "Algorithm"         : algo_name,
                    "Input Size"        : n,
                    "Input Condition"   : condition_label,
                    "Comparisons"       : comparisons,
                    "Execution Time (s)": round(t_sec, 6),
                    "Memory (bytes)"    : int(mem_bytes),
                    "Memory (KB)"       : round(mem_bytes / 1024, 2),
                })

    return pd.DataFrame(records)


# ─────────────────────────────────────────────
# Fibonacci experiments
# ─────────────────────────────────────────────

def run_fibonacci_experiments(n_values=None):
    """
    Benchmark all three Fibonacci algorithms for each value in *n_values*.

    Parameters
    ----------
    n_values : list[int], optional
        Fibonacci indices to test.  Defaults to [10, 20, 30, 40].

    Returns
    -------
    pandas.DataFrame
        One row per (algorithm, n) combination with columns:
        Algorithm, n, Fibonacci Result, Execution Time (s),
        Memory (bytes), Memory (KB).
    """
    if n_values is None:
        n_values = [10, 20, 30, 40]

    records = []

    for n in n_values:
        print(f"  >> n = {n} ...")
        for algo_name, algo_fn in FIBONACCI_ALGORITHMS.items():
            try:
                fib_val, t_sec, mem_bytes = measure_time_and_memory(algo_fn, n)
                records.append({
                    "Algorithm"          : algo_name,
                    "n"                  : n,
                    "Fibonacci Result"   : int(fib_val),
                    "Execution Time (s)" : round(t_sec, 8),
                    "Memory (bytes)"     : int(mem_bytes),
                    "Memory (KB)"        : round(mem_bytes / 1024, 4),
                })
            except RecursionError:
                print(f"    [RecursionError] {algo_name} — n={n} skipped")
                records.append({
                    "Algorithm"          : algo_name,
                    "n"                  : n,
                    "Fibonacci Result"   : None,
                    "Execution Time (s)" : None,
                    "Memory (bytes)"     : None,
                    "Memory (KB)"        : None,
                })

    return pd.DataFrame(records)


# ─────────────────────────────────────────────
# Quick self-test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("Sorting Performance -- small sizes (100, 500, 1000)")
    print("=" * 55)
    sort_df = run_sorting_experiments([100, 500, 1000])
    print(sort_df.to_string(index=False))

    print()
    print("=" * 55)
    print("Fibonacci Performance -- n in {10, 20, 30, 35}")
    print("=" * 55)
    fib_df = run_fibonacci_experiments([10, 20, 30, 35])
    print(fib_df.to_string(index=False))
