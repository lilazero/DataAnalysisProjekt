"""Algorithm benchmarks used in the analytics report."""

import timeit
from typing import List, Any, Callable, Optional

import numpy as np


def quicksort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    if len(arr) <= 1:
        return arr.copy()
    items = arr.copy()
    _quicksort_inplace(items, 0, len(items) - 1, key)
    return items


def _quicksort_inplace(
    arr: List[Any], low: int, high: int, key: Optional[Callable] = None
) -> None:
    if low < high:
        pivot_idx = _partition(arr, low, high, key)
        _quicksort_inplace(arr, low, pivot_idx - 1, key)
        _quicksort_inplace(arr, pivot_idx + 1, high, key)


def _partition(
    arr: List[Any], low: int, high: int, key: Optional[Callable] = None
) -> int:
    pivot = arr[high]
    pivot_val = key(pivot) if key else pivot
    i = low - 1
    for j in range(low, high):
        curr_val = key(arr[j]) if key else arr[j]
        if curr_val <= pivot_val:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def mergesort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    left = mergesort(arr[:mid], key)
    right = mergesort(arr[mid:], key)
    return _merge(left, right, key)


def _merge(
    left: List[Any], right: List[Any], key: Optional[Callable] = None
) -> List[Any]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_val = key(left[i]) if key else left[i]
        right_val = key(right[j]) if key else right[j]
        if left_val <= right_val:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def bubble_sort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    items = arr.copy()
    n = len(items)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            curr_val = key(items[j]) if key else items[j]
            next_val = key(items[j + 1]) if key else items[j + 1]
            if curr_val > next_val:
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        if not swapped:
            break
    return items


def linear_search(arr: List[Any], target: Any, key: Optional[Callable] = None) -> int:
    target_val = (
        key(target) if key and not isinstance(target, (int, float, str)) else target
    )
    for i, item in enumerate(arr):
        item_val = key(item) if key else item
        if item_val == target_val:
            return i
    return -1


def binary_search(arr: List[Any], target: Any, key: Optional[Callable] = None) -> int:
    left, right = 0, len(arr) - 1
    target_val = target
    while left <= right:
        mid = (left + right) // 2
        mid_val = key(arr[mid]) if key else arr[mid]
        if mid_val == target_val:
            return mid
        if mid_val < target_val:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def compare_sorting_performance(data: List[Any], iterations: int = 100) -> dict:
    if not data:
        return {}
    results = {}
    quicksort_time = timeit.timeit(lambda: quicksort(data), number=iterations)
    results["quicksort"] = {
        "time": quicksort_time / iterations,
        "complexity": "O(n log n) avg",
    }

    mergesort_time = timeit.timeit(lambda: mergesort(data), number=iterations)
    results["mergesort"] = {
        "time": mergesort_time / iterations,
        "complexity": "O(n log n)",
    }

    builtin_time = timeit.timeit(lambda: sorted(data), number=iterations)
    results["python_sorted"] = {
        "time": builtin_time / iterations,
        "complexity": "O(n log n)",
    }

    np_array = np.array(data) if data and isinstance(data[0], (int, float)) else None
    if np_array is not None:
        numpy_time = timeit.timeit(lambda: np.sort(np_array), number=iterations)
        results["numpy_sort"] = {
            "time": numpy_time / iterations,
            "complexity": "O(n log n)",
        }

    return results


def compare_searching_performance(
    data: List[Any], target: Any, iterations: int = 1000
) -> dict:
    if not data:
        return {}
    results = {}

    linear_time = timeit.timeit(lambda: linear_search(data, target), number=iterations)
    results["linear_search"] = {"time": linear_time / iterations, "complexity": "O(n)"}

    sorted_data = sorted(data) if data else data
    binary_time = timeit.timeit(
        lambda: binary_search(sorted_data, target), number=iterations
    )
    results["binary_search"] = {
        "time": binary_time / iterations,
        "complexity": "O(log n)",
    }

    builtin_time = timeit.timeit(lambda: target in data, number=iterations)
    results["python_in"] = {"time": builtin_time / iterations, "complexity": "O(n)"}

    np_array = np.array(data) if data and isinstance(data[0], (int, float)) else None
    if np_array is not None:
        numpy_time = timeit.timeit(
            lambda: np.where(np_array == target), number=iterations
        )
        results["numpy_where"] = {"time": numpy_time / iterations, "complexity": "O(n)"}

    return results


def generate_performance_report(sort_results: dict, search_results: dict) -> str:
    report = []
    report.append("=" * 60)
    report.append("ALGORITHM PERFORMANCE")
    report.append("=" * 60)

    report.append("\nSorting")
    for algo, data in sort_results.items():
        report.append(f"{algo}: {data['time'] * 1000:.4f} ms | {data['complexity']}")

    fastest_sort = min(sort_results.items(), key=lambda x: x[1]["time"])
    report.append(f"Fastest sort: {fastest_sort[0]}")

    report.append("\nSearching")
    for algo, data in search_results.items():
        report.append(f"{algo}: {data['time'] * 1000:.6f} ms | {data['complexity']}")

    fastest_search = min(search_results.items(), key=lambda x: x[1]["time"])
    report.append(f"Fastest search: {fastest_search[0]}")

    report.append("\nBuilt-ins are usually faster because they are in C and optimized.")
    return "\n".join(report)


if __name__ == "__main__":
    import random

    test_data = [random.randint(1, 10000) for _ in range(1000)]
    target = test_data[500]

    sort_results = compare_sorting_performance(test_data, iterations=50)
    search_results = compare_searching_performance(test_data, target, iterations=500)
    print(generate_performance_report(sort_results, search_results))
