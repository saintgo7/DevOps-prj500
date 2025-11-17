"""
Program 79: Complexity Analysis - Big O, Time/Space Complexity Examples
Demonstrates algorithm complexity analysis with practical examples
"""

import time
import random
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend


def constant_time_operations():
    """
    O(1) - Constant Time
    Operations that take same time regardless of input size
    """

    print("\n=== O(1) - Constant Time ===\n")

    def access_array_element(arr, index):
        """Array element access - O(1)"""
        return arr[index]

    def insert_hash_table(hash_table, key, value):
        """Hash table insertion - O(1) average"""
        hash_table[key] = value

    def push_stack(stack, value):
        """Stack push - O(1)"""
        stack.append(value)

    arr = [1, 2, 3, 4, 5]
    print(f"Array: {arr}")
    print(f"Access arr[2]: {access_array_element(arr, 2)}")

    hash_table = {}
    insert_hash_table(hash_table, "key", "value")
    print(f"\nHash table after insertion: {hash_table}")

    stack = []
    push_stack(stack, 10)
    push_stack(stack, 20)
    print(f"\nStack: {stack}")

    print("\nTime Complexity: O(1)")
    print("Space Complexity: O(1)")


def linear_time_operations():
    """
    O(n) - Linear Time
    Operations that scale linearly with input size
    """

    print("\n=== O(n) - Linear Time ===\n")

    def linear_search(arr, target):
        """Linear search - O(n)"""
        for i, val in enumerate(arr):
            if val == target:
                return i
        return -1

    def find_max(arr):
        """Find maximum - O(n)"""
        if not arr:
            return None

        max_val = arr[0]
        for val in arr[1:]:
            if val > max_val:
                max_val = val

        return max_val

    def sum_array(arr):
        """Sum array elements - O(n)"""
        total = 0
        for val in arr:
            total += val
        return total

    arr = [3, 7, 2, 9, 1, 5, 8]
    print(f"Array: {arr}")
    print(f"Linear search for 9: index {linear_search(arr, 9)}")
    print(f"Maximum: {find_max(arr)}")
    print(f"Sum: {sum_array(arr)}")

    print("\nTime Complexity: O(n)")
    print("Space Complexity: O(1)")


def logarithmic_time_operations():
    """
    O(log n) - Logarithmic Time
    Operations that halve the problem size each iteration
    """

    print("\n=== O(log n) - Logarithmic Time ===\n")

    def binary_search(arr, target):
        """Binary search - O(log n)"""
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

    def power_recursive(base, exp):
        """Fast exponentiation - O(log n)"""
        if exp == 0:
            return 1
        if exp == 1:
            return base

        half = power_recursive(base, exp // 2)

        if exp % 2 == 0:
            return half * half
        else:
            return base * half * half

    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"Sorted array: {arr}")
    print(f"Binary search for 7: index {binary_search(arr, 7)}")

    print(f"\n2^10 = {power_recursive(2, 10)}")

    print("\nTime Complexity: O(log n)")
    print("Space Complexity: O(1) for iterative, O(log n) for recursive")


def quadratic_time_operations():
    """
    O(n²) - Quadratic Time
    Nested loops over input
    """

    print("\n=== O(n²) - Quadratic Time ===\n")

    def bubble_sort(arr):
        """Bubble sort - O(n²)"""
        n = len(arr)
        arr = arr.copy()

        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr

    def find_duplicates(arr):
        """Find duplicates using nested loops - O(n²)"""
        duplicates = []

        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] == arr[j] and arr[i] not in duplicates:
                    duplicates.append(arr[i])

        return duplicates

    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    print(f"Sorted: {bubble_sort(arr)}")

    arr_dup = [1, 2, 3, 2, 4, 1, 5]
    print(f"\nArray with duplicates: {arr_dup}")
    print(f"Duplicates: {find_duplicates(arr_dup)}")

    print("\nTime Complexity: O(n²)")
    print("Space Complexity: O(1)")


def linearithmic_time_operations():
    """
    O(n log n) - Linearithmic Time
    Efficient sorting algorithms
    """

    print("\n=== O(n log n) - Linearithmic Time ===\n")

    def merge_sort(arr):
        """Merge sort - O(n log n)"""
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])

        return merge(left, right)

    def merge(left, right):
        """Merge two sorted arrays"""
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

    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original: {arr}")
    print(f"Sorted: {merge_sort(arr)}")

    print("\nTime Complexity: O(n log n)")
    print("Space Complexity: O(n)")


def exponential_time_operations():
    """
    O(2^n) - Exponential Time
    Recursive algorithms with multiple branches
    """

    print("\n=== O(2^n) - Exponential Time ===\n")

    def fibonacci_recursive(n):
        """Naive Fibonacci - O(2^n)"""
        if n <= 1:
            return n
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

    def generate_subsets(arr):
        """Generate all subsets - O(2^n)"""
        result = []

        def backtrack(index, current):
            if index == len(arr):
                result.append(current[:])
                return

            # Exclude current element
            backtrack(index + 1, current)

            # Include current element
            current.append(arr[index])
            backtrack(index + 1, current)
            current.pop()

        backtrack(0, [])
        return result

    n = 10
    print(f"Fibonacci({n}) = {fibonacci_recursive(n)}")

    arr = [1, 2, 3]
    subsets = generate_subsets(arr)
    print(f"\nSubsets of {arr}:")
    for subset in subsets:
        print(f"  {subset}")

    print("\nTime Complexity: O(2^n)")
    print("Space Complexity: O(n) for recursion stack")


def factorial_time_operations():
    """
    O(n!) - Factorial Time
    Generate all permutations
    """

    print("\n=== O(n!) - Factorial Time ===\n")

    def generate_permutations(arr):
        """Generate all permutations - O(n!)"""
        result = []

        def backtrack(first=0):
            if first == len(arr):
                result.append(arr[:])
                return

            for i in range(first, len(arr)):
                arr[first], arr[i] = arr[i], arr[first]
                backtrack(first + 1)
                arr[first], arr[i] = arr[i], arr[first]

        backtrack()
        return result

    arr = [1, 2, 3]
    perms = generate_permutations(arr)

    print(f"Permutations of {arr}:")
    for perm in perms:
        print(f"  {perm}")

    print(f"\nNumber of permutations: {len(perms)}")
    print("\nTime Complexity: O(n!)")
    print("Space Complexity: O(n)")


def space_complexity_examples():
    """Demonstrate space complexity"""

    print("\n=== Space Complexity Examples ===\n")

    # O(1) space
    def sum_iterative(n):
        """O(1) space"""
        total = 0
        for i in range(n + 1):
            total += i
        return total

    # O(n) space
    def sum_array_creation(n):
        """O(n) space"""
        arr = list(range(n + 1))
        return sum(arr)

    # O(n) space - recursion
    def factorial_recursive(n):
        """O(n) space due to recursion stack"""
        if n <= 1:
            return 1
        return n * factorial_recursive(n - 1)

    # O(n²) space
    def create_matrix(n):
        """O(n²) space"""
        return [[0] * n for _ in range(n)]

    n = 5

    print(f"Sum 1 to {n}:")
    print(f"  Iterative (O(1) space): {sum_iterative(n)}")
    print(f"  Array creation (O(n) space): {sum_array_creation(n)}")

    print(f"\nFactorial {n}:")
    print(f"  Recursive (O(n) space): {factorial_recursive(n)}")

    print(f"\nMatrix {n}x{n} (O(n²) space):")
    matrix = create_matrix(n)
    print(f"  Created {len(matrix)}x{len(matrix[0])} matrix")


def complexity_comparison():
    """Compare different complexities with timing"""

    print("\n=== Complexity Comparison (Timing) ===\n")

    sizes = [10, 100, 1000]

    print(f"{'Size':<10} {'O(1)':<12} {'O(log n)':<12} {'O(n)':<12} {'O(n log n)':<12} {'O(n²)':<12}")
    print("-" * 70)

    for n in sizes:
        # O(1)
        arr = list(range(n))
        start = time.time()
        _ = arr[0]
        t_constant = (time.time() - start) * 1000

        # O(log n)
        start = time.time()
        left, right = 0, n - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == n // 2:
                break
            elif arr[mid] < n // 2:
                left = mid + 1
            else:
                right = mid - 1
        t_log = (time.time() - start) * 1000

        # O(n)
        start = time.time()
        _ = sum(arr)
        t_linear = (time.time() - start) * 1000

        # O(n log n)
        start = time.time()
        _ = sorted(random.sample(range(n * 10), n))
        t_nlogn = (time.time() - start) * 1000

        # O(n²) - only for smaller sizes
        if n <= 100:
            start = time.time()
            for i in range(n):
                for j in range(n):
                    pass
            t_quadratic = (time.time() - start) * 1000
        else:
            t_quadratic = 0

        print(f"{n:<10} {t_constant:<12.6f} {t_log:<12.6f} {t_linear:<12.6f} {t_nlogn:<12.6f} {t_quadratic:<12.6f}")


def amortized_analysis():
    """Demonstrate amortized analysis"""

    print("\n=== Amortized Analysis ===\n")

    class DynamicArray:
        """Dynamic array with amortized O(1) append"""

        def __init__(self):
            self.capacity = 1
            self.size = 0
            self.array = [None] * self.capacity

        def append(self, value):
            """Amortized O(1) append"""
            if self.size == self.capacity:
                # Resize: O(n) but infrequent
                self.capacity *= 2
                new_array = [None] * self.capacity
                for i in range(self.size):
                    new_array[i] = self.array[i]
                self.array = new_array
                print(f"  Resized to capacity {self.capacity}")

            self.array[self.size] = value
            self.size += 1

    print("Dynamic Array (Amortized O(1) append):")
    da = DynamicArray()

    for i in range(10):
        print(f"Append {i}")
        da.append(i)

    print("\nTotal operations: 10")
    print("Resize operations: 4 (at size 1, 2, 4, 8)")
    print("Amortized cost per operation: O(1)")


def best_worst_average_case():
    """Demonstrate best, worst, and average case"""

    print("\n=== Best, Worst, Average Case ===\n")

    def quick_sort_analysis(arr):
        """Quick sort with different cases"""
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return quick_sort_analysis(left) + middle + quick_sort_analysis(right)

    # Best case: balanced partitions
    best_case = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Quick Sort - Best Case (balanced):")
    print(f"  Input: {best_case}")
    print(f"  Time: O(n log n)")

    # Worst case: already sorted
    worst_case = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("\nQuick Sort - Worst Case (sorted):")
    print(f"  Input: {worst_case}")
    print(f"  Time: O(n²)")

    # Average case
    print("\nQuick Sort - Average Case:")
    print(f"  Time: O(n log n)")


def main():
    """Main function to demonstrate complexity analysis"""

    print("=" * 60)
    print("PROGRAM 79: COMPLEXITY ANALYSIS")
    print("=" * 60)

    # Constant time
    constant_time_operations()

    print("\n" + "=" * 60)

    # Linear time
    linear_time_operations()

    print("\n" + "=" * 60)

    # Logarithmic time
    logarithmic_time_operations()

    print("\n" + "=" * 60)

    # Quadratic time
    quadratic_time_operations()

    print("\n" + "=" * 60)

    # Linearithmic time
    linearithmic_time_operations()

    print("\n" + "=" * 60)

    # Exponential time
    exponential_time_operations()

    print("\n" + "=" * 60)

    # Factorial time
    factorial_time_operations()

    print("\n" + "=" * 60)

    # Space complexity
    space_complexity_examples()

    print("\n" + "=" * 60)

    # Complexity comparison
    complexity_comparison()

    print("\n" + "=" * 60)

    # Amortized analysis
    amortized_analysis()

    print("\n" + "=" * 60)

    # Best/Worst/Average case
    best_worst_average_case()

    print("\n" + "=" * 60)
    print("Complexity analysis demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
