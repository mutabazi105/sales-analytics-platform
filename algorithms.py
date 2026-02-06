"""
Sorting and searching algorithms for Sales Analytics Platform
"""
import time
import numpy as np


def quicksort(arr):
    """Custom implementation of quicksort"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def binary_search(arr, target):
    """Custom implementation of binary search"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def linear_search(arr, target):
    """Custom implementation of linear search"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def compare_sorting(data):
    """Compare custom vs built-in sorting performance"""
    results = {}

    # Test custom quicksort
    start = time.time()
    custom_sorted = quicksort(data.copy())
    results['custom_quicksort'] = time.time() - start

    # Test built-in sorted
    start = time.time()
    builtin_sorted = sorted(data.copy())
    results['builtin_sorted'] = time.time() - start

    return results


def compare_searching(data, target):
    """Compare custom vs built-in searching performance"""
    results = {}
    sorted_data = sorted(data.copy())

    # Test binary search
    start = time.time()
    binary_result = binary_search(sorted_data, target)
    results['binary_search'] = time.time() - start

    # Test Python 'in' operator
    start = time.time()
    in_result = target in data
    results['in_operator'] = time.time() - start

    return results
