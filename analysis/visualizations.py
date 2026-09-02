"""
analysis/visualizations.py
──────────────────────────
Functions that generate Matplotlib graphs from the performance DataFrames
produced by analysis.performance.

All graphs are saved to the project-root ``graphs/`` directory.

Sorting graphs use a logarithmic y-axis so that both O(n²) and O(n log n)
curves are readable on the same chart.  Fibonacci graphs use a linear
y-axis because the recursive curve already separates itself dramatically
from the other two.

Student : RAKESH G
Roll No : 2401201064
Course  : BCA (AI & DS) — K.R. Mangalam University
Lab     : Lab 1 — Design and Analysis of Algorithms
"""

import os
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — safe inside notebooks
import matplotlib.pyplot as plt

# Colour palette — one distinct colour per algorithm
SORT_COLOURS = {
    "Bubble Sort"    : "#E63946",   # vivid red
    "Insertion Sort" : "#F4A261",   # warm orange
    "Merge Sort"     : "#2A9D8F",   # teal
    "Quick Sort"     : "#457B9D",   # steel blue
}

FIB_COLOURS = {
    "Recursive"          : "#E63946",
    "Iterative"          : "#2A9D8F",
    "Dynamic Programming": "#457B9D",
}

MARKER_SORT = {
    "Bubble Sort"    : "o",
    "Insertion Sort" : "s",
    "Merge Sort"     : "^",
    "Quick Sort"     : "D",
}

MARKER_FIB = {
    "Recursive"          : "o",
    "Iterative"          : "s",
    "Dynamic Programming": "^",
}

# Condition labels for subplot titles
CONDITION_TITLES = {
    "sorted" : "Sorted Input (Best Case)",
    "reverse": "Reverse-Sorted Input (Worst Case)",
    "random" : "Random Input (Avg Case)",
}


def _ensure_graphs_dir():
    """Create the graphs/ directory if it does not already exist."""
    os.makedirs("graphs", exist_ok=True)


# ─────────────────────────────────────────────
# Sorting — Execution Time
# ─────────────────────────────────────────────

def plot_sorting_execution_time(df, save_path="graphs/sorting_time_comparison.png"):
    """
    Three-panel log-scale plot: Execution Time vs Input Size for each condition.

    Parameters
    ----------
    df        : DataFrame — sorting performance data
    save_path : str       — output file path
    """
    _ensure_graphs_dir()
    conditions = ["sorted", "reverse", "random"]

    fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharey=False)
    fig.suptitle(
        "Sorting Algorithms — Execution Time vs Input Size (log scale)",
        fontsize=14, fontweight="bold", y=1.02,
    )

    for ax, cond in zip(axes, conditions):
        subset = df[df["Input Condition"] == cond]
        for algo in SORTING_ALGORITHMS_ORDER:
            algo_df = subset[subset["Algorithm"] == algo].sort_values("Input Size")
            if algo_df.empty:
                continue
            ax.plot(
                algo_df["Input Size"],
                algo_df["Execution Time (s)"],
                marker=MARKER_SORT[algo],
                color=SORT_COLOURS[algo],
                linewidth=1.8,
                markersize=5,
                label=algo,
            )
        ax.set_yscale("log")
        ax.set_xlabel("Input Size (n)", fontsize=10)
        ax.set_ylabel("Execution Time (s) — log scale", fontsize=9)
        ax.set_title(CONDITION_TITLES[cond], fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


# ─────────────────────────────────────────────
# Sorting — Memory Usage
# ─────────────────────────────────────────────

def plot_sorting_memory(df, save_path="graphs/sorting_memory_comparison.png"):
    """
    Three-panel log-scale plot: Memory Usage (KB) vs Input Size for each condition.

    Parameters
    ----------
    df        : DataFrame — sorting performance data
    save_path : str       — output file path
    """
    _ensure_graphs_dir()
    conditions = ["sorted", "reverse", "random"]

    fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharey=False)
    fig.suptitle(
        "Sorting Algorithms — Peak Memory Usage vs Input Size (log scale)",
        fontsize=14, fontweight="bold", y=1.02,
    )

    for ax, cond in zip(axes, conditions):
        subset = df[df["Input Condition"] == cond]
        for algo in SORTING_ALGORITHMS_ORDER:
            algo_df = subset[subset["Algorithm"] == algo].sort_values("Input Size")
            if algo_df.empty:
                continue
            ax.plot(
                algo_df["Input Size"],
                algo_df["Memory (KB)"],
                marker=MARKER_SORT[algo],
                color=SORT_COLOURS[algo],
                linewidth=1.8,
                markersize=5,
                label=algo,
            )
        ax.set_yscale("log")
        ax.set_xlabel("Input Size (n)", fontsize=10)
        ax.set_ylabel("Peak Memory (KB) — log scale", fontsize=9)
        ax.set_title(CONDITION_TITLES[cond], fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


# ─────────────────────────────────────────────
# Sorting — Comparison Count
# ─────────────────────────────────────────────

def plot_sorting_comparisons(df, save_path="graphs/sorting_comparisons.png"):
    """
    Three-panel log-scale plot: Number of Comparisons vs Input Size.

    Parameters
    ----------
    df        : DataFrame — sorting performance data
    save_path : str       — output file path
    """
    _ensure_graphs_dir()
    conditions = ["sorted", "reverse", "random"]

    fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharey=False)
    fig.suptitle(
        "Sorting Algorithms — Number of Comparisons vs Input Size (log scale)",
        fontsize=14, fontweight="bold", y=1.02,
    )

    for ax, cond in zip(axes, conditions):
        subset = df[df["Input Condition"] == cond]
        for algo in SORTING_ALGORITHMS_ORDER:
            algo_df = subset[subset["Algorithm"] == algo].sort_values("Input Size")
            if algo_df.empty:
                continue
            ax.plot(
                algo_df["Input Size"],
                algo_df["Comparisons"],
                marker=MARKER_SORT[algo],
                color=SORT_COLOURS[algo],
                linewidth=1.8,
                markersize=5,
                label=algo,
            )
        ax.set_yscale("log")
        ax.set_xlabel("Input Size (n)", fontsize=10)
        ax.set_ylabel("Comparisons — log scale", fontsize=9)
        ax.set_title(CONDITION_TITLES[cond], fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


# ─────────────────────────────────────────────
# Fibonacci — Execution Time
# ─────────────────────────────────────────────

def plot_fibonacci_execution_time(df, save_path="graphs/fibonacci_time_comparison.png"):
    """
    Single-panel linear-scale plot: Fibonacci Execution Time vs n.

    Parameters
    ----------
    df        : DataFrame — Fibonacci performance data
    save_path : str       — output file path
    """
    _ensure_graphs_dir()
    fig, ax = plt.subplots(figsize=(9, 6))

    for algo in FIBONACCI_ALGORITHMS_ORDER:
        algo_df = df[(df["Algorithm"] == algo) & df["Execution Time (s)"].notna()]
        algo_df = algo_df.sort_values("n")
        ax.plot(
            algo_df["n"],
            algo_df["Execution Time (s)"],
            marker=MARKER_FIB[algo],
            color=FIB_COLOURS[algo],
            linewidth=2,
            markersize=7,
            label=algo,
        )

    ax.set_xlabel("n (Fibonacci index)", fontsize=11)
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    ax.set_title("Fibonacci Algorithms — Execution Time vs n", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


# ─────────────────────────────────────────────
# Fibonacci — Memory Usage
# ─────────────────────────────────────────────

def plot_fibonacci_memory(df, save_path="graphs/fibonacci_memory_comparison.png"):
    """
    Single-panel linear-scale plot: Fibonacci Peak Memory vs n.

    Parameters
    ----------
    df        : DataFrame — Fibonacci performance data
    save_path : str       — output file path
    """
    _ensure_graphs_dir()
    fig, ax = plt.subplots(figsize=(9, 6))

    for algo in FIBONACCI_ALGORITHMS_ORDER:
        algo_df = df[(df["Algorithm"] == algo) & df["Memory (KB)"].notna()]
        algo_df = algo_df.sort_values("n")
        ax.plot(
            algo_df["n"],
            algo_df["Memory (KB)"],
            marker=MARKER_FIB[algo],
            color=FIB_COLOURS[algo],
            linewidth=2,
            markersize=7,
            label=algo,
        )

    ax.set_xlabel("n (Fibonacci index)", fontsize=11)
    ax.set_ylabel("Peak Memory (KB)", fontsize=11)
    ax.set_title("Fibonacci Algorithms — Memory Usage vs n", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


# ─────────────────────────────────────────────
# Convenience wrapper — generate all five plots
# ─────────────────────────────────────────────

# Ordered lists used by plot functions to keep legend order consistent
SORTING_ALGORITHMS_ORDER   = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
FIBONACCI_ALGORITHMS_ORDER = ["Recursive", "Iterative", "Dynamic Programming"]


def generate_all_plots(sorting_df, fibonacci_df):
    """
    Generate and save all five performance graphs.

    Parameters
    ----------
    sorting_df   : DataFrame — output of run_sorting_experiments()
    fibonacci_df : DataFrame — output of run_fibonacci_experiments()
    """
    print("\nGenerating sorting graphs …")
    plot_sorting_execution_time(sorting_df)
    plot_sorting_memory(sorting_df)
    plot_sorting_comparisons(sorting_df)

    print("Generating Fibonacci graphs …")
    plot_fibonacci_execution_time(fibonacci_df)
    plot_fibonacci_memory(fibonacci_df)

    print("\nAll graphs saved to graphs/")
