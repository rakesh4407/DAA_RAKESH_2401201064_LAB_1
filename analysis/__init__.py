"""
analysis/__init__.py

Package initialiser for the analysis module.

Student : RAKESH G
Roll No : 2401201064
Course  : BCA (AI & DS) — K.R. Mangalam University
Lab     : Lab 1 — Design and Analysis of Algorithms
"""

from analysis.performance import (
    measure_time_and_memory,
    build_sorting_datasets,
    run_sorting_experiments,
    run_fibonacci_experiments,
)
from analysis.visualizations import generate_all_plots

__all__ = [
    "measure_time_and_memory",
    "build_sorting_datasets",
    "run_sorting_experiments",
    "run_fibonacci_experiments",
    "generate_all_plots",
]
