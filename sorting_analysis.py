"""
Empirical Analysis of Sorting Algorithms
Algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort
Input sizes: 5, 10, 50, 100
Worst-case test data: reverse-sorted versions of the assignment's arrays.

Run:
    python sorting_analysis.py

The program performs at least five timed batches per algorithm and input size.
Each batch repeats the sort many times to reduce timer noise.
"""
import csv
import time
from pathlib import Path

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def selection_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
}

SIZES = [5, 10, 50, 100]
BATCHES = 5

def main():
    rows = []
    for n in SIZES:
        # The assignment's arrays contain 1..N in ascending order.
        # Reverse them to create a descending (worst-case-style) input.
        test_data = list(range(n, 0, -1))
        # More repetitions for small arrays; enough work to reduce timer noise.
        repetitions = max(300, min(20000, 2_000_000 // (n * n)))
        for name, algorithm in ALGORITHMS.items():
            batch_times_us = []
            for _ in range(BATCHES):
                start = time.perf_counter_ns()
                for _ in range(repetitions):
                    result = algorithm(test_data)
                elapsed = time.perf_counter_ns() - start
                batch_times_us.append(elapsed / repetitions / 1000.0)
            average_us = sum(batch_times_us) / len(batch_times_us)
            # Correctness check
            assert result == list(range(1, n + 1))
            rows.append({
                "Algorithm": name,
                "Input Size (N)": n,
                "Average Time (microseconds)": average_us,
                "Batches": BATCHES,
                "Sorts per Batch": repetitions,
            })
            print(f"{name:15s} N={n:3d}: {average_us:.4f} microseconds")
    output = Path(__file__).with_name("sorting_results.csv")
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"\\nResults saved to: {output}")

if __name__ == "__main__":
    main()
