"""
notebook/run_analysis.py
────────────────────────
Standalone script — runs the full analysis pipeline without needing
Jupyter Notebook.

Usage (from the project root directory):
    python notebook/run_analysis.py

What it does
------------
1. Runs all sorting algorithm experiments (5 sizes × 3 conditions × 4 algorithms)
2. Runs all Fibonacci algorithm experiments (4 n-values × 3 algorithms)
3. Saves results to data/sorting_performance.csv and data/fibonacci_performance.csv
4. Generates 5 performance graphs in the graphs/ directory

Student : RAKESH G
Roll No : 2401201064
Course  : BCA (AI & DS) — K.R. Mangalam University
Lab     : Lab 1 — Design and Analysis of Algorithms
"""

import os
import sys

# ── Ensure the project root is on Python's import path ──────────────────────
# This script lives in notebook/, so we go up one level to reach project root.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from analysis.performance import run_sorting_experiments, run_fibonacci_experiments
from analysis.visualizations import generate_all_plots


def main():
    print("=" * 60)
    print("  DAA Lab 1 -- Algorithm Efficiency & Performance Analysis")
    print("  Student : RAKESH G  |  Roll No : 2401201064")
    print("  K.R. Mangalam University -- BCA (AI & DS)")
    print("=" * 60)

    # ── 1. Sorting experiments ───────────────────────────────────────────────
    print("[1/4] Running sorting algorithm experiments ...")
    print("      Input sizes : 100, 500, 1000, 5000, 10000")
    print("      Conditions  : sorted, reverse-sorted, random")
    print("      Runs/point  : 5 (median recorded)\n")

    sort_df = run_sorting_experiments(sizes=[100, 500, 1000, 5000, 10000])

    # ── 2. Save sorting results ──────────────────────────────────────────────
    os.makedirs("data", exist_ok=True)
    sort_csv = "data/sorting_performance.csv"
    sort_df.to_csv(sort_csv, index=False)
    print(f"\n[2/4] Sorting results saved to {sort_csv}")

    # ── 3. Fibonacci experiments ─────────────────────────────────────────────
    print("\n[3/4] Running Fibonacci algorithm experiments ...")
    print("      n values : 10, 20, 30, 40\n")

    fib_df = run_fibonacci_experiments(n_values=[10, 20, 30, 40])

    fib_csv = "data/fibonacci_performance.csv"
    fib_df.to_csv(fib_csv, index=False)
    print(f"      Fibonacci results saved to {fib_csv}")

    # ── 4. Generate graphs ───────────────────────────────────────────────────
    print("\n[4/4] Generating performance graphs ...")
    generate_all_plots(sort_df, fib_df)

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  Analysis complete.  Output files:")
    print("  * " + sort_csv)
    print("  * " + fib_csv)
    print("  * graphs/sorting_time_comparison.png")
    print("  * graphs/sorting_memory_comparison.png")
    print("  * graphs/sorting_comparisons.png")
    print("  * graphs/fibonacci_time_comparison.png")
    print("  * graphs/fibonacci_memory_comparison.png")
    print("=" * 60)

    # ── Print a small preview of results ────────────────────────────────────
    print("\nSorting -- Execution Time at n=10000 (random input):")
    preview = sort_df[
        (sort_df["Input Size"] == 10000) & (sort_df["Input Condition"] == "random")
    ][["Algorithm", "Execution Time (s)", "Memory (KB)", "Comparisons"]]
    print(preview.to_string(index=False))

    print("\nFibonacci — All results:")
    print(fib_df[["Algorithm", "n", "Fibonacci Result",
                  "Execution Time (s)", "Memory (KB)"]].to_string(index=False))


if __name__ == "__main__":
    main()
