"""
Assignment 3: Empirical Analysis of Sorting Algorithms
Student: Ahmed Hamdan | Student ID: 71648

The program compares Selection Sort, Bubble Sort, Quick Sort, and Merge Sort.
Each algorithm is tested on four input cases. Every case is timed three times,
and the average execution time is reported.
"""

import time
from statistics import mean


def selection_sort(arr):
    """Sort in-place using Selection Sort."""
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if a[j] < a[min_index]:
                min_index = j
        if min_index != i:
            a[i], a[min_index] = a[min_index], a[i]
    return a


def bubble_sort(arr):
    """Sort in-place using optimized Bubble Sort."""
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def quick_sort(arr):
    """Return a sorted list using Quick Sort (middle element as pivot)."""
    if len(arr) <= 1:
        return arr.copy()

    a = arr.copy()
    pivot = a[len(a) // 2]
    left = [x for x in a if x < pivot]
    equal = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quick_sort(left) + equal + quick_sort(right)


def merge_sort(arr):
    """Return a sorted list using Merge Sort."""
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


ALGORITHMS = {
    "Selection Sort": selection_sort,
    "Bubble Sort": bubble_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}


def make_test_cases():
    return {
        "5 - Sorted": list(range(1, 6)),
        "5 - Reverse": list(range(5, 0, -1)),
        "100 - Sorted": list(range(1, 101)),
        "100 - Reverse": list(range(100, 0, -1)),
    }


def benchmark(sort_function, data, repetitions=3):
    """Return average elapsed time in milliseconds after 3 runs."""
    elapsed_times = []
    for _ in range(repetitions):
        start = time.perf_counter()
        result = sort_function(data)
        elapsed_times.append((time.perf_counter() - start) * 1000)
        assert result == sorted(data), "Sorting result is incorrect"
    return mean(elapsed_times)


def main():
    cases = make_test_cases()
    print("Average execution time (milliseconds; 3 runs)")
    print("-" * 78)

    for algorithm_name, sort_function in ALGORITHMS.items():
        print("\\n" + algorithm_name)
        for case_name, data in cases.items():
            average_ms = benchmark(sort_function, data)
            print(f"{case_name:16s}: {average_ms:.6f} ms")


if __name__ == "__main__":
    main()
