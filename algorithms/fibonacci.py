"""
algorithms/fibonacci.py
───────────────────────
Three approaches to computing the n-th Fibonacci number.

The Fibonacci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2)  for n ≥ 2

Approaches implemented
-----------------------
1. fib_recursive  — plain recursion, exponential time O(2ⁿ)
2. fib_iterative  — bottom-up loop, linear time O(n), constant space O(1)
3. fib_dp         — top-down memoisation, linear time O(n), linear space O(n)

Student : RAKESH G
Roll No : 2401201064
Course  : BCA (AI & DS) — K.R. Mangalam University
Lab     : Lab 1 — Design and Analysis of Algorithms
"""


# ─────────────────────────────────────────────
# 1.  NAIVE RECURSION
# ─────────────────────────────────────────────

def fib_recursive(n):
    """
    Return F(n) using naive (plain) recursion.

    How it works
    ────────────
    Directly translates the mathematical recurrence:
        F(n) = F(n-1) + F(n-2)
    into code.  Each call branches into two smaller calls, producing a
    binary call tree of depth n.  Many sub-problems are recomputed
    repeatedly — for example F(2) is recomputed 2^(n-2) times for large n.

    Parameters
    ----------
    n : int
        Non-negative integer index in the Fibonacci sequence.

    Returns
    -------
    int
        The n-th Fibonacci number.

    Complexity
    ----------
    Time  : O(2ⁿ) — exponential (each call spawns two recursive calls)
    Space : O(n)   — maximum recursion-stack depth

    Advantages
    ----------
    - Minimal code; directly mirrors the mathematical definition
    - Easy to understand conceptually

    Limitations
    -----------
    - Exponential time: F(40) takes ~6.7 s; F(50) would take hours
    - Same sub-problems recomputed an exponential number of times
    - Python's default recursion limit will cause RecursionError for large n

    Suitable Scenarios
    ------------------
    - Teaching recursion and showing exponential blowup
    - Very small n (n ≤ 25) where time does not matter

    Sample
    ------
    >>> fib_recursive(10)
    55
    >>> fib_recursive(0)
    0
    """
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


# ─────────────────────────────────────────────
# 2.  ITERATIVE (BOTTOM-UP)
# ─────────────────────────────────────────────

def fib_iterative(n):
    """
    Return F(n) using an iterative bottom-up approach.

    How it works
    ────────────
    We maintain only two variables — the two most recently computed
    Fibonacci numbers — and update them in a forward loop.  Because we
    never revisit a sub-problem, the total work is exactly proportional
    to n.

    Parameters
    ----------
    n : int
        Non-negative integer index in the Fibonacci sequence.

    Returns
    -------
    int
        The n-th Fibonacci number.

    Complexity
    ----------
    Time  : O(n) — single loop from 2 to n
    Space : O(1) — only two integer variables needed

    Advantages
    ----------
    - Extremely fast; outperforms recursive and DP approaches in practice
    - Constant space — no extra array or dictionary allocated
    - No recursion overhead or risk of stack overflow

    Limitations
    -----------
    - Slightly less intuitive than the recursive formulation
    - Cannot easily reuse intermediate results for multiple queries
      (though each call is already O(n), so it's not a major issue)

    Suitable Scenarios
    ------------------
    - Production code where performance and memory matter
    - Computing Fibonacci for very large n
    - Memory-constrained embedded or mobile environments

    Sample
    ------
    >>> fib_iterative(10)
    55
    >>> fib_iterative(1)
    1
    """
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


# ─────────────────────────────────────────────
# 3.  DYNAMIC PROGRAMMING (TOP-DOWN MEMOISATION)
# ─────────────────────────────────────────────

def fib_dp(n, _cache=None):
    """
    Return F(n) using top-down Dynamic Programming with memoisation.

    How it works
    ────────────
    We add a dictionary cache to the recursive approach.  Before computing
    F(n) we check whether it is already in the cache; if so we return the
    cached result immediately.  This ensures each sub-problem F(k) is
    computed exactly once.  The call tree collapses from an exponential
    binary tree to a single linear chain.

    Parameters
    ----------
    n      : int
        Non-negative integer index in the Fibonacci sequence.
    _cache : dict or None
        Memoisation dictionary.  Pass ``None`` (the default) to start a
        fresh computation; the function initialises its own empty dict.
        You may pass an existing dict to reuse results across calls.

    Returns
    -------
    int
        The n-th Fibonacci number.

    Complexity
    ----------
    Time  : O(n) — each of the n sub-problems is solved exactly once
    Space : O(n) — for the memoisation dictionary + recursion stack

    Advantages
    ----------
    - Same O(n) time as the iterative approach
    - Preserves the recursive structure, making the DP pattern explicit
    - The cache can be reused if many different n values are queried

    Limitations
    -----------
    - Uses O(n) extra memory for the cache
    - Recursive overhead (function call stack) makes it slightly slower
      than the iterative version in benchmarks
    - Python recursion limit still applies for very large n

    Suitable Scenarios
    ------------------
    - Teaching dynamic programming concepts
    - When multiple Fibonacci values are needed and cache reuse helps
    - Situations where the recursive structure aids code clarity

    Sample
    ------
    >>> fib_dp(10)
    55
    >>> fib_dp(0)
    0
    """
    if _cache is None:
        _cache = {}
    if n in _cache:
        return _cache[n]
    if n <= 1:
        return n
    _cache[n] = fib_dp(n - 1, _cache) + fib_dp(n - 2, _cache)
    return _cache[n]


# ─────────────────────────────────────────────
# Quick self-test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import time

    print("Fibonacci values for n = 0 … 10")
    print(f"{'n':>4}  {'Recursive':>12}  {'Iterative':>12}  {'DP':>12}")
    print("-" * 46)
    for idx in range(11):
        r = fib_recursive(idx)
        it = fib_iterative(idx)
        dp = fib_dp(idx)
        print(f"{idx:>4}  {r:>12}  {it:>12}  {dp:>12}")

    print("\nTiming comparison for n = 35")
    n_test = 35

    t0 = time.perf_counter()
    fib_recursive(n_test)
    print(f"  Recursive : {time.perf_counter() - t0:.6f} s")

    t0 = time.perf_counter()
    fib_iterative(n_test)
    print(f"  Iterative : {time.perf_counter() - t0:.6f} s")

    t0 = time.perf_counter()
    fib_dp(n_test)
    print(f"  DP        : {time.perf_counter() - t0:.6f} s")
