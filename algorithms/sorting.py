"""
algorithms/sorting.py
─────────────────────
Implementations of four classical sorting algorithms.

Each function:
  • accepts an unsorted list
  • works on a copy (does not mutate the input)
  • returns (sorted_list, comparison_count)

Algorithms
----------
1. Bubble Sort     — O(n) best / O(n²) average & worst
2. Insertion Sort  — O(n) best / O(n²) average & worst
3. Merge Sort      — O(n log n) all cases
4. Quick Sort      — O(n log n) average / O(n²) worst (randomised pivot)

Student : RAKESH G
Roll No : 2401201064
Course  : BCA (AI & DS) — K.R. Mangalam University
Lab     : Lab 1 — Design and Analysis of Algorithms
"""

import random


# ─────────────────────────────────────────────
# 1.  BUBBLE SORT
# ─────────────────────────────────────────────

def bubble_sort(data):
    """
    Sort *data* in ascending order using Bubble Sort.

    How it works
    ────────────
    The algorithm scans the list from left to right, comparing every pair
    of adjacent elements and swapping them when the left value is greater
    than the right.  After each full pass the largest unseen element has
    "bubbled up" to its final position at the right end of the unsorted
    portion.  A ``swapped`` flag enables early termination: if a complete
    pass completes without a single swap the list is already sorted and
    we stop immediately (best-case O(n)).

    Parameters
    ----------
    data : list
        A list of comparable elements (integers, floats, strings, …).

    Returns
    -------
    sorted_data : list
        A new list sorted in ascending order.
    comparisons : int
        Total number of element comparisons performed.

    Complexity
    ----------
    ┌───────────┬────────┬────────┐
    │   Case    │  Time  │ Space  │
    ├───────────┼────────┼────────┤
    │ Best      │  O(n)  │  O(1)  │
    │ Average   │  O(n²) │  O(1)  │
    │ Worst     │  O(n²) │  O(1)  │
    └───────────┴────────┴────────┘

    Advantages
    ----------
    - Extremely simple — easy to understand and explain
    - Stable: equal elements preserve their original relative order
    - Adaptive: very fast when the input is nearly sorted

    Limitations
    -----------
    - Quadratic time on average/worst input makes it impractical for n > ~10 000
    - Performs many more swaps than Insertion Sort for the same disorder level

    Suitable Scenarios
    ------------------
    - Teaching and demonstration
    - Very small lists (n < 20) where simplicity beats performance
    - Nearly-sorted data combined with the early-exit optimisation

    Sample
    ------
    >>> bubble_sort([5, 3, 8, 1, 2])
    ([1, 2, 3, 5, 8], 8)
    """
    arr = data[:]          # work on a copy to preserve the original
    n = len(arr)
    comparisons = 0

    for outer in range(n - 1):
        made_a_swap = False
        # After each outer pass, the last (outer) positions are in place
        for inner in range(n - 1 - outer):
            comparisons += 1
            if arr[inner] > arr[inner + 1]:
                arr[inner], arr[inner + 1] = arr[inner + 1], arr[inner]
                made_a_swap = True
        if not made_a_swap:
            # Already sorted — exit early (best-case optimisation)
            break

    return arr, comparisons


# ─────────────────────────────────────────────
# 2.  INSERTION SORT
# ─────────────────────────────────────────────

def insertion_sort(data):
    """
    Sort *data* in ascending order using Insertion Sort.

    How it works
    ────────────
    Think of sorting a hand of playing cards one card at a time.  We
    maintain a growing sorted sub-list on the left.  For each new element
    (the "key") we slide it leftward past every element that is larger,
    until we find its correct slot and drop it in.

    Parameters
    ----------
    data : list
        A list of comparable elements.

    Returns
    -------
    sorted_data : list
        A new list sorted in ascending order.
    comparisons : int
        Total number of element comparisons performed.

    Complexity
    ----------
    ┌───────────┬────────┬────────┐
    │   Case    │  Time  │ Space  │
    ├───────────┼────────┼────────┤
    │ Best      │  O(n)  │  O(1)  │
    │ Average   │  O(n²) │  O(1)  │
    │ Worst     │  O(n²) │  O(1)  │
    └───────────┴────────┴────────┘

    Advantages
    ----------
    - Stable sorting algorithm
    - In-place: uses O(1) auxiliary space
    - Online: can sort a stream of arriving elements one at a time
    - Faster than Bubble Sort in practice (fewer writes per comparison)

    Limitations
    -----------
    - Still O(n²) for large random inputs — not suitable for big datasets

    Suitable Scenarios
    ------------------
    - Small lists (n < 50) or nearly-sorted data
    - Online / streaming scenarios where data arrives incrementally
    - Hybrid algorithms (e.g., TimSort uses Insertion Sort for small runs)

    Sample
    ------
    >>> insertion_sort([5, 3, 8, 1, 2])
    ([1, 2, 3, 5, 8], 6)
    """
    arr = data[:]
    comparisons = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Shift elements that are greater than 'key' one position to the right
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key

    return arr, comparisons


# ─────────────────────────────────────────────
# 3.  MERGE SORT  (helper functions first)
# ─────────────────────────────────────────────

def _merge_two_halves(left_half, right_half, cmp_counter):
    """
    Merge two sorted lists into one sorted list.

    Parameters
    ----------
    left_half  : list — left sorted sub-list
    right_half : list — right sorted sub-list
    cmp_counter: list[int] — single-element mutable counter (pass-by-ref trick)

    Returns
    -------
    list : merged sorted list
    """
    merged = []
    li = ri = 0  # pointers into left_half and right_half

    while li < len(left_half) and ri < len(right_half):
        cmp_counter[0] += 1
        if left_half[li] <= right_half[ri]:
            merged.append(left_half[li])
            li += 1
        else:
            merged.append(right_half[ri])
            ri += 1

    # Append any remaining elements (no comparisons needed)
    merged.extend(left_half[li:])
    merged.extend(right_half[ri:])
    return merged


def _merge_sort_recursive(arr, cmp_counter):
    """
    Recursive worker for merge_sort.

    Divides *arr* in half, recursively sorts each half, then merges.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_sorted  = _merge_sort_recursive(arr[:mid], cmp_counter)
    right_sorted = _merge_sort_recursive(arr[mid:], cmp_counter)
    return _merge_two_halves(left_sorted, right_sorted, cmp_counter)


def merge_sort(data):
    """
    Sort *data* in ascending order using Merge Sort (divide-and-conquer).

    How it works
    ────────────
    Recursively split the list into two halves until each half contains
    at most one element (trivially sorted).  Then merge pairs of sorted
    halves back together, always picking the smaller front element from
    either half, until the full sorted list is reconstructed.

    Parameters
    ----------
    data : list
        A list of comparable elements.

    Returns
    -------
    sorted_data : list
        A new list sorted in ascending order.
    comparisons : int
        Total number of element comparisons performed during merging.

    Complexity
    ----------
    ┌───────────┬────────────┬────────┐
    │   Case    │    Time    │ Space  │
    ├───────────┼────────────┼────────┤
    │ Best      │ O(n log n) │  O(n)  │
    │ Average   │ O(n log n) │  O(n)  │
    │ Worst     │ O(n log n) │  O(n)  │
    └───────────┴────────────┴────────┘

    Advantages
    ----------
    - Guaranteed O(n log n) — performance does not depend on input order
    - Stable sorting algorithm
    - Well-suited for linked lists and external (disk-based) sorting

    Limitations
    -----------
    - Requires O(n) auxiliary memory for the temporary merged arrays
    - Slightly slower than Quick Sort on in-memory data due to memory allocation

    Suitable Scenarios
    ------------------
    - Large datasets where consistent, predictable performance is required
    - External sorting (when data does not fit entirely in RAM)
    - Any situation that demands a stable sort

    Sample
    ------
    >>> merge_sort([5, 3, 8, 1, 2])
    ([1, 2, 3, 5, 8], 7)
    """
    arr = data[:]
    cmp_counter = [0]
    sorted_arr = _merge_sort_recursive(arr, cmp_counter)
    return sorted_arr, cmp_counter[0]


# ─────────────────────────────────────────────
# 4.  QUICK SORT  (helper functions first)
# ─────────────────────────────────────────────

def _lomuto_partition(arr, lo, hi, cmp_counter):
    """
    Lomuto partition scheme around arr[hi] (the pivot).

    Rearranges arr[lo..hi] so that:
      • everything ≤ pivot is to the left of the pivot's final index
      • everything > pivot is to the right
    Returns the final index of the pivot element.
    """
    pivot = arr[hi]
    wall = lo - 1            # boundary between ≤pivot and >pivot regions

    for scan in range(lo, hi):
        cmp_counter[0] += 1
        if arr[scan] <= pivot:
            wall += 1
            arr[wall], arr[scan] = arr[scan], arr[wall]

    # Place pivot into its final sorted position
    arr[wall + 1], arr[hi] = arr[hi], arr[wall + 1]
    return wall + 1


def _randomised_partition(arr, lo, hi, cmp_counter):
    """
    Choose a random pivot, move it to arr[hi], then run Lomuto partition.

    Randomisation eliminates the deterministic worst case that arises
    when the input is already sorted and we always pick the last element.
    """
    rand_pivot_idx = random.randint(lo, hi)
    arr[rand_pivot_idx], arr[hi] = arr[hi], arr[rand_pivot_idx]
    return _lomuto_partition(arr, lo, hi, cmp_counter)


def _quick_sort_recursive(arr, lo, hi, cmp_counter):
    """
    Recursive worker for quick_sort.

    Partitions arr[lo..hi], then recurses on the two sub-arrays.
    """
    if lo < hi:
        pivot_pos = _randomised_partition(arr, lo, hi, cmp_counter)
        _quick_sort_recursive(arr, lo, pivot_pos - 1, cmp_counter)
        _quick_sort_recursive(arr, pivot_pos + 1, hi, cmp_counter)


def quick_sort(data):
    """
    Sort *data* in ascending order using Quick Sort (divide-and-conquer).

    How it works
    ────────────
    Choose a pivot element at random, rearrange the list so that all
    elements smaller than or equal to the pivot are on its left and all
    larger elements are on its right (partition step), then recursively
    sort each side.  The randomised pivot avoids the O(n²) worst case
    that occurs on already-sorted input when always picking the last element.

    Parameters
    ----------
    data : list
        A list of comparable elements.

    Returns
    -------
    sorted_data : list
        A new list sorted in ascending order.
    comparisons : int
        Total number of element comparisons performed.

    Complexity
    ----------
    ┌───────────┬────────────┬──────────┐
    │   Case    │    Time    │  Space   │
    ├───────────┼────────────┼──────────┤
    │ Best      │ O(n log n) │ O(log n) │
    │ Average   │ O(n log n) │ O(log n) │
    │ Worst     │    O(n²)   │   O(n)   │
    └───────────┴────────────┴──────────┘
    (With randomised pivot, worst case is astronomically unlikely.)

    Advantages
    ----------
    - Very fast in practice — cache-friendly sequential memory access
    - In-place: only O(log n) stack space for recursion
    - Average-case performance beats Merge Sort on in-memory data

    Limitations
    -----------
    - Unstable: equal elements may change relative order
    - Theoretical worst case is O(n²) with a bad pivot choice

    Suitable Scenarios
    ------------------
    - General-purpose in-memory sorting
    - Large datasets where raw speed matters most
    - Situations where memory is limited (no O(n) auxiliary array needed)

    Sample
    ------
    >>> result, _ = quick_sort([5, 3, 8, 1, 2])
    >>> result
    [1, 2, 3, 5, 8]
    """
    arr = data[:]
    cmp_counter = [0]
    if len(arr) > 1:
        _quick_sort_recursive(arr, 0, len(arr) - 1, cmp_counter)
    return arr, cmp_counter[0]


# ─────────────────────────────────────────────
# Quick self-test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    test_input = [42, 17, 93, 5, 68, 31, 76]
    print("Original list :", test_input)
    print()

    for label, fn in [
        ("Bubble Sort   ", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort    ", merge_sort),
        ("Quick Sort    ", quick_sort),
    ]:
        result, comps = fn(test_input)
        print(f"{label} → {result}  |  comparisons: {comps}")
