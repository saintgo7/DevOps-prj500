"""
Program 70: Sorting Algorithms - Various Sorting Techniques
Demonstrates bubble, selection, insertion, merge, quick, and heap sort
"""

import time
import random


def bubble_sort(arr):
    """
    Bubble Sort - Repeatedly swap adjacent elements if in wrong order
    Time: O(n²), Space: O(1)
    Stable: Yes
    """
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True

        if not swapped:
            break

    return arr, comparisons, swaps


def selection_sort(arr):
    """
    Selection Sort - Select minimum and place at beginning
    Time: O(n²), Space: O(1)
    Stable: No
    """
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

    return arr, comparisons, swaps


def insertion_sort(arr):
    """
    Insertion Sort - Insert each element at correct position in sorted part
    Time: O(n²), Space: O(1)
    Stable: Yes
    """
    n = len(arr)
    comparisons = 0
    shifts = 0

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            j -= 1
            shifts += 1

        if j >= 0:
            comparisons += 1

        arr[j + 1] = key

    return arr, comparisons, shifts


def merge_sort(arr):
    """
    Merge Sort - Divide and conquer approach
    Time: O(n log n), Space: O(n)
    Stable: Yes
    """
    comparisons = [0]

    def merge(left, right):
        """Merge two sorted arrays"""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort_helper(arr):
        """Recursive merge sort"""
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = merge_sort_helper(arr[:mid])
        right = merge_sort_helper(arr[mid:])

        return merge(left, right)

    sorted_arr = merge_sort_helper(arr)
    return sorted_arr, comparisons[0], 0


def quick_sort(arr):
    """
    Quick Sort - Partition around pivot
    Time: Average O(n log n), Worst O(n²), Space: O(log n)
    Stable: No
    """
    comparisons = [0]
    swaps = [0]

    def partition(arr, low, high):
        """Partition array around pivot"""
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            comparisons[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if i != j:
                    swaps[0] += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if i + 1 != high:
            swaps[0] += 1

        return i + 1

    def quick_sort_helper(arr, low, high):
        """Recursive quick sort"""
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)

    quick_sort_helper(arr, 0, len(arr) - 1)
    return arr, comparisons[0], swaps[0]


def heap_sort(arr):
    """
    Heap Sort - Build max heap and extract elements
    Time: O(n log n), Space: O(1)
    Stable: No
    """
    comparisons = [0]
    swaps = [0]

    def heapify(arr, n, i):
        """Maintain heap property"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            comparisons[0] += 1
            if arr[left] > arr[largest]:
                largest = left

        if right < n:
            comparisons[0] += 1
            if arr[right] > arr[largest]:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            swaps[0] += 1
            heapify(arr, n, largest)

    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        swaps[0] += 1
        heapify(arr, i, 0)

    return arr, comparisons[0], swaps[0]


def counting_sort(arr):
    """
    Counting Sort - Count occurrences of each value
    Time: O(n + k), Space: O(k) where k is range of input
    Stable: Yes
    Only works for non-negative integers
    """
    if not arr:
        return arr, 0, 0

    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1

    count = [0] * range_size
    output = [0] * len(arr)

    # Count occurrences
    for num in arr:
        count[num - min_val] += 1

    # Cumulative count
    for i in range(1, range_size):
        count[i] += count[i - 1]

    # Build output array
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1

    return output, 0, 0


def radix_sort(arr):
    """
    Radix Sort - Sort digit by digit
    Time: O(d * (n + k)), Space: O(n + k)
    where d is number of digits, k is range of digits
    Stable: Yes
    """
    if not arr:
        return arr, 0, 0

    def counting_sort_for_radix(arr, exp):
        """Counting sort for specific digit"""
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10

    return arr, 0, 0


def shell_sort(arr):
    """
    Shell Sort - Generalization of insertion sort
    Time: O(n log n) to O(n²), Space: O(1)
    Stable: No
    """
    n = len(arr)
    gap = n // 2
    comparisons = 0
    swaps = 0

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            while j >= gap and arr[j - gap] > temp:
                comparisons += 1
                arr[j] = arr[j - gap]
                swaps += 1
                j -= gap

            if j >= gap:
                comparisons += 1

            arr[j] = temp

        gap //= 2

    return arr, comparisons, swaps


def compare_sorting_algorithms():
    """Compare performance of different sorting algorithms"""

    print("\n=== Sorting Algorithms Comparison ===\n")

    # Test arrays
    sizes = [10, 50, 100]

    for size in sizes:
        print(f"Array size: {size}")
        print("-" * 70)

        # Generate random array
        original = [random.randint(1, 100) for _ in range(size)]

        algorithms = [
            ("Bubble Sort", bubble_sort),
            ("Selection Sort", selection_sort),
            ("Insertion Sort", insertion_sort),
            ("Merge Sort", merge_sort),
            ("Quick Sort", quick_sort),
            ("Heap Sort", heap_sort),
            ("Shell Sort", shell_sort),
        ]

        if size <= 50:  # Only for smaller arrays
            algorithms.extend([
                ("Counting Sort", counting_sort),
                ("Radix Sort", radix_sort),
            ])

        print(f"{'Algorithm':<20} {'Time (ms)':<12} {'Comparisons':<15} {'Swaps/Shifts':<15}")
        print("-" * 70)

        for name, sort_func in algorithms:
            arr = original.copy()
            start = time.time()
            sorted_arr, comp, swaps = sort_func(arr)
            elapsed = (time.time() - start) * 1000

            print(f"{name:<20} {elapsed:>10.4f}   {comp:>12}   {swaps:>12}")

        print()


def stability_demonstration():
    """Demonstrate stable vs unstable sorting"""

    print("\n=== Sorting Stability Demonstration ===\n")

    class Item:
        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __repr__(self):
            return f"({self.key},{self.value})"

    # Create array with duplicate keys
    items = [
        Item(3, 'a'), Item(1, 'b'), Item(3, 'c'),
        Item(2, 'd'), Item(1, 'e'), Item(2, 'f')
    ]

    print(f"Original array: {items}")

    # Stable sort (merge sort)
    def stable_sort_items(items):
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left = stable_sort_items(items[:mid])
        right = stable_sort_items(items[mid:])

        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i].key <= right[j].key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    sorted_stable = stable_sort_items(items.copy())
    print(f"Stable sort:    {sorted_stable}")

    # Unstable sort (selection sort)
    def unstable_sort_items(items):
        arr = items.copy()
        n = len(arr)

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j].key < arr[min_idx].key:
                    min_idx = j

            arr[i], arr[min_idx] = arr[min_idx], arr[i]

        return arr

    sorted_unstable = unstable_sort_items(items)
    print(f"Unstable sort:  {sorted_unstable}")

    print("\nNote: Stable sort preserves relative order of equal keys")


def best_worst_cases():
    """Demonstrate best and worst case scenarios"""

    print("\n=== Best and Worst Case Scenarios ===\n")

    # Sorted array (best for insertion, worst for quick)
    sorted_arr = list(range(1, 21))

    # Reverse sorted (worst for bubble, selection, insertion)
    reverse_arr = list(range(20, 0, -1))

    # Random array
    random_arr = [random.randint(1, 100) for _ in range(20)]

    test_cases = [
        ("Sorted Array", sorted_arr.copy()),
        ("Reverse Sorted", reverse_arr.copy()),
        ("Random Array", random_arr.copy()),
    ]

    print("Testing Insertion Sort:")
    print("-" * 60)

    for name, arr in test_cases:
        test_arr = arr.copy()
        start = time.time()
        _, comparisons, shifts = insertion_sort(test_arr)
        elapsed = (time.time() - start) * 1000

        print(f"{name:<20} Comparisons: {comparisons:>5}, Shifts: {shifts:>5}, Time: {elapsed:.4f}ms")


def main():
    """Main function to demonstrate sorting algorithms"""

    print("=" * 60)
    print("PROGRAM 70: SORTING ALGORITHMS")
    print("=" * 60)

    # Test array
    test_arr = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]

    print(f"\nOriginal array: {test_arr}\n")
    print("=" * 60)

    # Bubble Sort
    arr = test_arr.copy()
    sorted_arr, comp, swaps = bubble_sort(arr)
    print(f"\nBubble Sort:")
    print(f"  Result: {sorted_arr}")
    print(f"  Comparisons: {comp}, Swaps: {swaps}")
    print(f"  Time: O(n²), Space: O(1), Stable: Yes")

    # Selection Sort
    arr = test_arr.copy()
    sorted_arr, comp, swaps = selection_sort(arr)
    print(f"\nSelection Sort:")
    print(f"  Result: {sorted_arr}")
    print(f"  Comparisons: {comp}, Swaps: {swaps}")
    print(f"  Time: O(n²), Space: O(1), Stable: No")

    # Insertion Sort
    arr = test_arr.copy()
    sorted_arr, comp, shifts = insertion_sort(arr)
    print(f"\nInsertion Sort:")
    print(f"  Result: {sorted_arr}")
    print(f"  Comparisons: {comp}, Shifts: {shifts}")
    print(f"  Time: O(n²), Space: O(1), Stable: Yes")

    # Merge Sort
    arr = test_arr.copy()
    sorted_arr, comp, _ = merge_sort(arr)
    print(f"\nMerge Sort:")
    print(f"  Result: {sorted_arr}")
    print(f"  Comparisons: {comp}")
    print(f"  Time: O(n log n), Space: O(n), Stable: Yes")

    # Quick Sort
    arr = test_arr.copy()
    sorted_arr, comp, swaps = quick_sort(arr)
    print(f"\nQuick Sort:")
    print(f"  Result: {sorted_arr}")
    print(f"  Comparisons: {comp}, Swaps: {swaps}")
    print(f"  Time: O(n log n) avg, Space: O(log n), Stable: No")

    # Heap Sort
    arr = test_arr.copy()
    sorted_arr, comp, swaps = heap_sort(arr)
    print(f"\nHeap Sort:")
    print(f"  Result: {sorted_arr}")
    print(f"  Comparisons: {comp}, Swaps: {swaps}")
    print(f"  Time: O(n log n), Space: O(1), Stable: No")

    # Shell Sort
    arr = test_arr.copy()
    sorted_arr, comp, swaps = shell_sort(arr)
    print(f"\nShell Sort:")
    print(f"  Result: {sorted_arr}")
    print(f"  Comparisons: {comp}, Swaps: {swaps}")
    print(f"  Time: O(n log n) to O(n²), Space: O(1), Stable: No")

    # Counting Sort (for small integers)
    arr = [4, 2, 2, 8, 3, 3, 1]
    sorted_arr, _, _ = counting_sort(arr)
    print(f"\nCounting Sort:")
    print(f"  Input: {[4, 2, 2, 8, 3, 3, 1]}")
    print(f"  Result: {sorted_arr}")
    print(f"  Time: O(n + k), Space: O(k), Stable: Yes")

    # Radix Sort
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    sorted_arr, _, _ = radix_sort(arr)
    print(f"\nRadix Sort:")
    print(f"  Input: {[170, 45, 75, 90, 802, 24, 2, 66]}")
    print(f"  Result: {sorted_arr}")
    print(f"  Time: O(d*(n+k)), Space: O(n+k), Stable: Yes")

    print("\n" + "=" * 60)

    # Compare algorithms
    compare_sorting_algorithms()

    print("=" * 60)

    # Stability demonstration
    stability_demonstration()

    print("\n" + "=" * 60)

    # Best/worst cases
    best_worst_cases()

    print("\n" + "=" * 60)
    print("Sorting algorithms demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
