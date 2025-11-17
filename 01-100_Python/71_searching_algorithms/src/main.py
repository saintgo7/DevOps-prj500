"""
Program 71: Searching Algorithms - Linear, Binary, Jump, Interpolation
Demonstrates various searching techniques with complexity analysis
"""

import math


def linear_search(arr, target):
    """
    Linear Search - Search sequentially through array
    Time: O(n), Space: O(1)
    Works on: Sorted and unsorted arrays
    """
    comparisons = 0

    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons

    return -1, comparisons


def binary_search(arr, target):
    """
    Binary Search - Divide and conquer on sorted array
    Time: O(log n), Space: O(1)
    Works on: Sorted arrays only
    """
    left, right = 0, len(arr) - 1
    comparisons = 0

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1

        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1, comparisons


def binary_search_recursive(arr, target, left=0, right=None, comparisons=None):
    """
    Recursive Binary Search
    Time: O(log n), Space: O(log n) due to recursion
    """
    if right is None:
        right = len(arr) - 1

    if comparisons is None:
        comparisons = [0]

    if left > right:
        return -1, comparisons[0]

    mid = (left + right) // 2
    comparisons[0] += 1

    if arr[mid] == target:
        return mid, comparisons[0]
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right, comparisons)
    else:
        return binary_search_recursive(arr, target, left, mid - 1, comparisons)


def jump_search(arr, target):
    """
    Jump Search - Jump ahead by fixed steps, then linear search
    Time: O(√n), Space: O(1)
    Works on: Sorted arrays only
    """
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    comparisons = 0

    # Jump to find block where target may exist
    while prev < n and arr[min(step, n) - 1] < target:
        comparisons += 1
        prev = step
        step += int(math.sqrt(n))

        if prev >= n:
            return -1, comparisons

    # Linear search in identified block
    while prev < n and arr[prev] < target:
        comparisons += 1
        prev += 1

        if prev == min(step, n):
            return -1, comparisons

    comparisons += 1
    if prev < n and arr[prev] == target:
        return prev, comparisons

    return -1, comparisons


def interpolation_search(arr, target):
    """
    Interpolation Search - Estimates position based on value distribution
    Time: O(log log n) for uniform distribution, O(n) worst case
    Space: O(1)
    Works on: Sorted arrays with uniformly distributed values
    """
    left, right = 0, len(arr) - 1
    comparisons = 0

    while left <= right and target >= arr[left] and target <= arr[right]:
        comparisons += 1

        if left == right:
            if arr[left] == target:
                return left, comparisons
            return -1, comparisons

        # Estimate position
        pos = left + int(((target - arr[left]) / (arr[right] - arr[left])) * (right - left))

        comparisons += 1
        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1, comparisons


def exponential_search(arr, target):
    """
    Exponential Search - Find range then binary search
    Time: O(log n), Space: O(1)
    Works on: Sorted arrays, good for unbounded arrays
    """
    if not arr:
        return -1, 0

    comparisons = 1
    if arr[0] == target:
        return 0, comparisons

    # Find range for binary search
    i = 1
    while i < len(arr) and arr[i] <= target:
        comparisons += 1
        i *= 2

    # Binary search in found range
    left = i // 2
    right = min(i, len(arr) - 1)

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1

        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1, comparisons


def ternary_search(arr, target):
    """
    Ternary Search - Divide into three parts
    Time: O(log₃ n), Space: O(1)
    Works on: Sorted arrays
    """
    left, right = 0, len(arr) - 1
    comparisons = 0

    while left <= right:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3

        comparisons += 1
        if arr[mid1] == target:
            return mid1, comparisons

        comparisons += 1
        if arr[mid2] == target:
            return mid2, comparisons

        comparisons += 1
        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1

    return -1, comparisons


def fibonacci_search(arr, target):
    """
    Fibonacci Search - Uses Fibonacci numbers to divide array
    Time: O(log n), Space: O(1)
    Works on: Sorted arrays
    """
    n = len(arr)
    fib_m2 = 0  # (m-2)'th Fibonacci number
    fib_m1 = 1  # (m-1)'th Fibonacci number
    fib_m = fib_m2 + fib_m1  # m'th Fibonacci number
    comparisons = 0

    # Find smallest Fibonacci >= n
    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m = fib_m2 + fib_m1

    offset = -1

    while fib_m > 1:
        i = min(offset + fib_m2, n - 1)
        comparisons += 1

        if arr[i] < target:
            fib_m = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i
        elif arr[i] > target:
            fib_m = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1
        else:
            return i, comparisons

    comparisons += 1
    if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1, comparisons

    return -1, comparisons


def search_in_rotated_array(arr, target):
    """
    Search in Rotated Sorted Array
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    comparisons = 0

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1

        if arr[mid] == target:
            return mid, comparisons

        # Determine which half is sorted
        comparisons += 1
        if arr[left] <= arr[mid]:
            # Left half is sorted
            comparisons += 1
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            comparisons += 1
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1, comparisons


def find_first_last_occurrence(arr, target):
    """
    Find first and last occurrence of target
    Time: O(log n), Space: O(1)
    """

    def find_first(arr, target):
        left, right = 0, len(arr) - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2

            if arr[mid] == target:
                result = mid
                right = mid - 1  # Continue searching left
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return result

    def find_last(arr, target):
        left, right = 0, len(arr) - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2

            if arr[mid] == target:
                result = mid
                left = mid + 1  # Continue searching right
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return result

    first = find_first(arr, target)
    last = find_last(arr, target)

    return first, last


def search_2d_matrix(matrix, target):
    """
    Search in 2D sorted matrix
    Time: O(m + n), Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False, 0

    rows = len(matrix)
    cols = len(matrix[0])
    row = 0
    col = cols - 1
    comparisons = 0

    # Start from top-right corner
    while row < rows and col >= 0:
        comparisons += 1

        if matrix[row][col] == target:
            return (row, col), comparisons
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1

    return False, comparisons


def compare_search_algorithms():
    """Compare performance of different search algorithms"""

    print("\n=== Search Algorithms Comparison ===\n")

    # Create sorted array
    arr = list(range(0, 1000, 10))
    target = 500

    print(f"Array size: {len(arr)}")
    print(f"Target: {target}")
    print(f"Array: [0, 10, 20, ... , 990]\n")

    algorithms = [
        ("Linear Search", lambda a, t: linear_search(a, t)),
        ("Binary Search", lambda a, t: binary_search(a, t)),
        ("Jump Search", lambda a, t: jump_search(a, t)),
        ("Interpolation Search", lambda a, t: interpolation_search(a, t)),
        ("Exponential Search", lambda a, t: exponential_search(a, t)),
        ("Ternary Search", lambda a, t: ternary_search(a, t)),
        ("Fibonacci Search", lambda a, t: fibonacci_search(a, t)),
    ]

    print(f"{'Algorithm':<25} {'Index':<10} {'Comparisons':<15}")
    print("-" * 50)

    for name, search_func in algorithms:
        index, comparisons = search_func(arr, target)
        print(f"{name:<25} {index:<10} {comparisons:<15}")


def best_worst_cases():
    """Demonstrate best and worst case scenarios"""

    print("\n=== Best and Worst Case Scenarios ===\n")

    arr = list(range(0, 100, 2))

    # Best case: target at middle (for binary search)
    target_best = arr[len(arr) // 2]

    # Worst case: target not found or at ends
    target_worst = 99

    print("Binary Search:")
    print(f"Array: {arr[:10]} ... {arr[-10:]}")
    print()

    # Best case
    index, comp = binary_search(arr, target_best)
    print(f"Best case (target at middle: {target_best}):")
    print(f"  Index: {index}, Comparisons: {comp}")

    # Worst case
    index, comp = binary_search(arr, target_worst)
    print(f"\nWorst case (target not found: {target_worst}):")
    print(f"  Index: {index}, Comparisons: {comp}")


def main():
    """Main function to demonstrate searching algorithms"""

    print("=" * 60)
    print("PROGRAM 71: SEARCHING ALGORITHMS")
    print("=" * 60)

    # Test array
    arr = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78]
    target = 23

    print(f"\nSorted array: {arr}")
    print(f"Target: {target}\n")
    print("=" * 60)

    # Linear Search
    index, comp = linear_search(arr, target)
    print(f"\nLinear Search:")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(n), Space: O(1)")

    # Binary Search
    index, comp = binary_search(arr, target)
    print(f"\nBinary Search (Iterative):")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(log n), Space: O(1)")

    # Binary Search Recursive
    index, comp = binary_search_recursive(arr, target)
    print(f"\nBinary Search (Recursive):")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(log n), Space: O(log n)")

    # Jump Search
    index, comp = jump_search(arr, target)
    print(f"\nJump Search:")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(√n), Space: O(1)")

    # Interpolation Search
    index, comp = interpolation_search(arr, target)
    print(f"\nInterpolation Search:")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(log log n) avg, O(n) worst")

    # Exponential Search
    index, comp = exponential_search(arr, target)
    print(f"\nExponential Search:")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(log n), Space: O(1)")

    # Ternary Search
    index, comp = ternary_search(arr, target)
    print(f"\nTernary Search:")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(log₃ n), Space: O(1)")

    # Fibonacci Search
    index, comp = fibonacci_search(arr, target)
    print(f"\nFibonacci Search:")
    print(f"  Index: {index}, Comparisons: {comp}")
    print(f"  Time: O(log n), Space: O(1)")

    print("\n" + "=" * 60)

    # Search in rotated array
    print("\n=== Search in Rotated Sorted Array ===\n")
    rotated = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    print(f"Rotated array: {rotated}")
    print(f"Target: {target}")
    index, comp = search_in_rotated_array(rotated, target)
    print(f"Index: {index}, Comparisons: {comp}")

    print("\n" + "=" * 60)

    # First and last occurrence
    print("\n=== First and Last Occurrence ===\n")
    arr_dup = [1, 2, 2, 2, 3, 4, 5, 5, 5, 5, 6]
    target = 5
    print(f"Array: {arr_dup}")
    print(f"Target: {target}")
    first, last = find_first_last_occurrence(arr_dup, target)
    print(f"First occurrence: {first}")
    print(f"Last occurrence: {last}")

    print("\n" + "=" * 60)

    # Search in 2D matrix
    print("\n=== Search in 2D Matrix ===\n")
    matrix = [
        [1, 4, 7, 11],
        [2, 5, 8, 12],
        [3, 6, 9, 16],
        [10, 13, 14, 17]
    ]
    target = 5

    print("Matrix:")
    for row in matrix:
        print(f"  {row}")

    print(f"\nTarget: {target}")
    position, comp = search_2d_matrix(matrix, target)
    if position:
        print(f"Found at position: {position}, Comparisons: {comp}")
    else:
        print(f"Not found, Comparisons: {comp}")

    print("\n" + "=" * 60)

    # Compare algorithms
    compare_search_algorithms()

    print("\n" + "=" * 60)

    # Best/worst cases
    best_worst_cases()

    print("\n" + "=" * 60)
    print("Searching algorithms demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
