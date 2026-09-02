# Comparative Study of Algorithm Efficiency and Performance Analysis

**Lab 1 — Design and Analysis of Algorithms (ENCA301)**

| Field | Details |
|---|---|
| **Student Name** | RAKESH G |
| **Roll Number** | 2401201064 |
| **Course** | BCA (AI & DS) |
| **Semester** | 5th Semester |
| **University** | K.R. Mangalam University |
| **Subject** | Design and Analysis of Algorithms |
| **Lab** | Lab 1 |

---

## Objective

To implement, benchmark, and compare the time complexity, space complexity, and real-world performance of four classical sorting algorithms (Bubble Sort, Insertion Sort, Merge Sort, Quick Sort) and three Fibonacci computation strategies (Recursive, Iterative, Dynamic Programming) across varying input sizes and conditions.

---

## Problem Statement

Algorithm selection directly influences a software system's speed, memory footprint, and scalability. Two algorithms may solve the same problem correctly yet differ by orders of magnitude in execution time. This study measures those differences experimentally and connects them to Big-O theory, helping us understand when to choose one algorithm over another.

---

## Algorithms Implemented

### Sorting Algorithms

| Algorithm | Best Case | Average Case | Worst Case | Space | Stable |
|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |

> **Note:** Quick Sort uses randomized pivot selection, which avoids the O(n²) worst case in practice.

### Fibonacci Algorithms

| Algorithm | Time Complexity | Space Complexity |
|---|---|---|
| Recursive | O(2ⁿ) | O(n) |
| Iterative | O(n) | O(1) |
| Dynamic Programming | O(n) | O(n) |

---

## Project Structure

```
algorithm-efficiency-case-study-Rakesh_240120164/
│
├── README.md                         ← This file
├── .gitignore                        ← Ignored files list
├── requirements.txt                  ← Python dependencies
│
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py                    ← Bubble, Insertion, Merge, Quick Sort
│   └── fibonacci.py                  ← Recursive, Iterative, DP Fibonacci
│
├── analysis/
│   ├── __init__.py
│   ├── performance.py                ← Timing and memory measurement utilities
│   └── visualizations.py             ← Matplotlib graph-generation functions
│
├── data/
│   ├── sorting_performance.csv       ← Generated sorting results
│   └── fibonacci_performance.csv     ← Generated Fibonacci results
│
├── graphs/
│   ├── sorting_time_comparison.png
│   ├── sorting_memory_comparison.png
│   ├── sorting_comparisons.png
│   ├── fibonacci_time_comparison.png
│   └── fibonacci_memory_comparison.png
│
├── notebook/
│   ├── algorithm_efficiency_analysis.ipynb   ← Main Jupyter Notebook
│   └── run_analysis.py                       ← Standalone runner script
│
└── reports/
    ├── final_report.md               ← Full analytical report (Markdown)
    └── final_report.pdf              ← PDF version for submission
```

---

## How to Run

### Step 1 — Clone the repository

```bash
git clone <your-repository-url>
cd algorithm-efficiency-case-study-Rakesh_240120164
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4A — Run via Jupyter Notebook (recommended)

```bash
jupyter notebook notebook/algorithm_efficiency_analysis.ipynb
```

Select **Kernel → Restart & Run All** to execute all cells from top to bottom.

### Step 4B — Run via standalone script

```bash
cd notebook
python run_analysis.py
```

### Generated outputs

| Output | Location |
|---|---|
| 5 performance graphs (PNG) | `graphs/` |
| Sorting performance data | `data/sorting_performance.csv` |
| Fibonacci performance data | `data/fibonacci_performance.csv` |

---

## Experimental Methodology

| Parameter | Value |
|---|---|
| Sorting input sizes | 100, 500, 1000, 5000, 10000 |
| Input conditions | Sorted (ascending), Reverse-sorted, Random |
| Fibonacci n values | 10, 20, 30, 40 |
| Runs per data point | 5 (median used to reduce noise) |
| Timing method | `time.perf_counter()` |
| Memory method | `tracemalloc` (peak heap allocation) |
| Random seed | 42 (reproducible) |
| Comparison counting | Built into each sorting algorithm |

---

## Tools and Libraries

| Tool | Purpose |
|---|---|
| Python 3.x | Implementation language |
| `matplotlib` | Graph generation |
| `numpy` | Numerical utilities |
| `pandas` | Results tabulation and CSV export |
| `tracemalloc` | Peak memory measurement |
| `time.perf_counter` | High-resolution execution timing |
| Jupyter Notebook | Interactive analysis and report |

---

## Results Summary

### Sorting (n = 10,000, random input)

| Algorithm | Execution Time (s) | Memory (KB) | Comparisons |
|---|---|---|---|
| Bubble Sort | ~4.50 | ~78 | ~49,988,000 |
| Insertion Sort | ~1.71 | ~78 | ~25,086,000 |
| Merge Sort | ~0.024 | ~243 | ~120,383 |
| Quick Sort | ~0.013 | ~78 | ~148,160 |

### Fibonacci (n = 40)

| Algorithm | Execution Time (s) | Memory (KB) |
|---|---|---|
| Recursive | ~6.70 | ~0.00 |
| Iterative | ~0.000002 | ~0.00 |
| Dynamic Programming | ~0.000007 | ~1.63 |

---

## Key Observations

1. **Quick Sort is fastest** in practice for in-memory sorting, beating Bubble Sort by more than 400× at n = 10,000 (random).
2. **Merge Sort is the most consistent**: its execution time barely changes between sorted, reverse, and random inputs — confirming O(n log n) in all cases.
3. **Insertion Sort beats Bubble Sort** by ~39% even at the same O(n²) complexity, because shifts are cheaper than swaps.
4. **Bubble and Insertion Sort show O(n) best-case** behaviour on sorted input thanks to the early-exit flag.
5. **Recursive Fibonacci explodes** from 0.053 s at n = 30 to 6.70 s at n = 40 — a 126× jump for just 10 extra steps.
6. **Iterative Fibonacci** computes any of the tested n values in under 0.00001 s and uses virtually zero extra memory.
7. **Merge Sort uses 3–4× more memory** than the other sorting algorithms because it allocates auxiliary arrays during the merge step.

---

## Conclusion

Theoretical complexity analysis predicts general growth trends, but actual execution time depends on constant factors, cache behaviour, and input characteristics. This study confirms that selecting the right algorithm for the right context — factoring in input size, ordering, and available memory — is a core software engineering skill that cannot be reduced to a single metric.

---

*Submitted for Lab 1 — Design and Analysis of Algorithms, BCA (AI & DS), K.R. Mangalam University, Semester 5*
