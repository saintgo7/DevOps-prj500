"""
Program 72: Advanced Recursion - Patterns, Memoization, Tail Recursion
Demonstrates advanced recursion techniques and optimization strategies
"""

import sys
from functools import lru_cache

# Increase recursion limit for demonstration
sys.setrecursionlimit(10000)


class RecursionExamples:
    """Collection of recursion examples"""

    # Basic Recursion
    def factorial(self, n):
        """Factorial - Time: O(n), Space: O(n)"""
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)

    def fibonacci(self, n):
        """Fibonacci (naive) - Time: O(2^n), Space: O(n)"""
        if n <= 1:
            return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    # Linear Recursion
    def sum_array(self, arr, index=0):
        """Sum array elements - Time: O(n), Space: O(n)"""
        if index >= len(arr):
            return 0
        return arr[index] + self.sum_array(arr, index + 1)

    def reverse_string(self, s):
        """Reverse string - Time: O(n), Space: O(n)"""
        if len(s) <= 1:
            return s
        return self.reverse_string(s[1:]) + s[0]

    # Binary Recursion
    def binary_search(self, arr, target, left, right):
        """Binary search - Time: O(log n), Space: O(log n)"""
        if left > right:
            return -1

        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return self.binary_search(arr, target, mid + 1, right)
        else:
            return self.binary_search(arr, target, left, mid - 1)

    # Multiple Recursion
    def tower_of_hanoi(self, n, source, destination, auxiliary):
        """Tower of Hanoi - Time: O(2^n), Space: O(n)"""
        if n == 1:
            print(f"  Move disk 1 from {source} to {destination}")
            return

        self.tower_of_hanoi(n - 1, source, auxiliary, destination)
        print(f"  Move disk {n} from {source} to {destination}")
        self.tower_of_hanoi(n - 1, auxiliary, destination, source)


def memoization_examples():
    """Demonstrate memoization technique"""

    print("\n=== Memoization Examples ===\n")

    # Without memoization
    def fib_naive(n):
        """Naive Fibonacci - O(2^n)"""
        if n <= 1:
            return n
        return fib_naive(n - 1) + fib_naive(n - 2)

    # With manual memoization
    def fib_memo(n, memo=None):
        """Fibonacci with memoization - O(n)"""
        if memo is None:
            memo = {}

        if n in memo:
            return memo[n]

        if n <= 1:
            return n

        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
        return memo[n]

    # With decorator
    @lru_cache(maxsize=None)
    def fib_cached(n):
        """Fibonacci with @lru_cache - O(n)"""
        if n <= 1:
            return n
        return fib_cached(n - 1) + fib_cached(n - 2)

    # Test Fibonacci
    n = 35

    print(f"Calculating Fibonacci({n}):\n")

    import time

    # Naive (warning: slow for large n)
    if n <= 35:
        start = time.time()
        result = fib_naive(n)
        elapsed = time.time() - start
        print(f"Naive:        Result = {result}, Time = {elapsed:.6f}s")

    # Memoized
    start = time.time()
    result = fib_memo(n)
    elapsed = time.time() - start
    print(f"Memoized:     Result = {result}, Time = {elapsed:.6f}s")

    # Cached
    start = time.time()
    result = fib_cached(n)
    elapsed = time.time() - start
    print(f"LRU Cached:   Result = {result}, Time = {elapsed:.6f}s")

    print("\n" + "-" * 40)

    # Grid paths with memoization
    print("\n=== Grid Paths Problem ===\n")

    @lru_cache(maxsize=None)
    def grid_paths(m, n):
        """Count paths in m x n grid - Time: O(m*n)"""
        if m == 1 or n == 1:
            return 1
        return grid_paths(m - 1, n) + grid_paths(m, n - 1)

    m, n = 10, 10
    print(f"Grid size: {m} x {n}")
    print(f"Number of paths: {grid_paths(m, n)}")


def tail_recursion():
    """Demonstrate tail recursion optimization"""

    print("\n=== Tail Recursion ===\n")

    # Non-tail recursive factorial
    def factorial_normal(n):
        """Non-tail recursive - O(n) space"""
        if n <= 1:
            return 1
        return n * factorial_normal(n - 1)

    # Tail recursive factorial
    def factorial_tail(n, accumulator=1):
        """Tail recursive - Can be optimized to O(1) space"""
        if n <= 1:
            return accumulator
        return factorial_tail(n - 1, n * accumulator)

    # Non-tail recursive sum
    def sum_normal(arr, index=0):
        """Non-tail recursive sum"""
        if index >= len(arr):
            return 0
        return arr[index] + sum_normal(arr, index + 1)

    # Tail recursive sum
    def sum_tail(arr, index=0, accumulator=0):
        """Tail recursive sum"""
        if index >= len(arr):
            return accumulator
        return sum_tail(arr, index + 1, accumulator + arr[index])

    n = 5
    print(f"Factorial of {n}:")
    print(f"  Normal:      {factorial_normal(n)}")
    print(f"  Tail:        {factorial_tail(n)}")

    arr = [1, 2, 3, 4, 5]
    print(f"\nSum of {arr}:")
    print(f"  Normal:      {sum_normal(arr)}")
    print(f"  Tail:        {sum_tail(arr)}")

    print("\nNote: Python doesn't optimize tail recursion,")
    print("but tail recursive form can be converted to iteration easily")


def recursive_patterns():
    """Demonstrate common recursive patterns"""

    print("\n=== Common Recursive Patterns ===\n")

    # 1. Decrease and Conquer
    print("1. Decrease and Conquer (Binary Search):")

    def binary_search(arr, target, left=0, right=None):
        """Divide problem in half each time"""
        if right is None:
            right = len(arr) - 1

        if left > right:
            return -1

        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return binary_search(arr, target, mid + 1, right)
        else:
            return binary_search(arr, target, left, mid - 1)

    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 7
    print(f"   Array: {arr}")
    print(f"   Target: {target}")
    print(f"   Index: {binary_search(arr, target)}")

    # 2. Divide and Conquer
    print("\n2. Divide and Conquer (Merge Sort):")

    def merge_sort(arr):
        """Divide into subproblems, solve, and combine"""
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
    print(f"   Original: {arr}")
    print(f"   Sorted:   {merge_sort(arr)}")

    # 3. Dynamic Programming Pattern
    print("\n3. Dynamic Programming (Coin Change):")

    @lru_cache(maxsize=None)
    def coin_change(amount, coins):
        """Minimum coins to make amount"""
        if amount == 0:
            return 0
        if amount < 0:
            return float('inf')

        min_coins = float('inf')
        for coin in coins:
            result = coin_change(amount - coin, coins)
            if result != float('inf'):
                min_coins = min(min_coins, result + 1)

        return min_coins

    amount = 11
    coins = (1, 2, 5)
    result = coin_change(amount, coins)
    print(f"   Amount: {amount}")
    print(f"   Coins: {coins}")
    print(f"   Minimum coins: {result}")

    # 4. Backtracking Pattern
    print("\n4. Backtracking (Generate Permutations):")

    def permutations(arr):
        """Generate all permutations"""
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
    perms = permutations(arr)
    print(f"   Array: {arr}")
    print(f"   Permutations: {perms}")


def mutual_recursion():
    """Demonstrate mutual recursion"""

    print("\n=== Mutual Recursion ===\n")

    def is_even(n):
        """Check if number is even using mutual recursion"""
        if n == 0:
            return True
        return is_odd(n - 1)

    def is_odd(n):
        """Check if number is odd using mutual recursion"""
        if n == 0:
            return False
        return is_even(n - 1)

    print("Testing mutual recursion (is_even/is_odd):")
    for i in range(6):
        print(f"  {i}: even={is_even(i)}, odd={is_odd(i)}")


def indirect_recursion():
    """Demonstrate indirect recursion"""

    print("\n=== Indirect Recursion ===\n")

    def print_pattern_a(n):
        """Print pattern using indirect recursion"""
        if n > 0:
            print(f"  A{n}", end=" ")
            print_pattern_b(n - 1)

    def print_pattern_b(n):
        """Helper for indirect recursion"""
        if n > 0:
            print(f"B{n}", end=" ")
            print_pattern_a(n - 1)

    print("Indirect recursion pattern:")
    print_pattern_a(5)
    print()


def nested_recursion():
    """Demonstrate nested recursion"""

    print("\n=== Nested Recursion ===\n")

    def ackermann(m, n):
        """Ackermann function - grows very fast"""
        if m == 0:
            return n + 1
        elif n == 0:
            return ackermann(m - 1, 1)
        else:
            return ackermann(m - 1, ackermann(m, n - 1))

    print("Ackermann function (nested recursion):")
    for m in range(4):
        for n in range(4):
            if m <= 2 or n <= 2:  # Limit to prevent long computation
                result = ackermann(m, n)
                print(f"  A({m}, {n}) = {result}")


def recursion_to_iteration():
    """Show how to convert recursion to iteration"""

    print("\n=== Recursion to Iteration Conversion ===\n")

    # Recursive factorial
    def factorial_recursive(n):
        if n <= 1:
            return 1
        return n * factorial_recursive(n - 1)

    # Iterative factorial
    def factorial_iterative(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    # Recursive Fibonacci
    def fib_recursive(n):
        if n <= 1:
            return n
        return fib_recursive(n - 1) + fib_recursive(n - 2)

    # Iterative Fibonacci
    def fib_iterative(n):
        if n <= 1:
            return n

        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr

        return curr

    n = 10
    print(f"Factorial of {n}:")
    print(f"  Recursive:  {factorial_recursive(n)}")
    print(f"  Iterative:  {factorial_iterative(n)}")

    print(f"\nFibonacci of {n}:")
    print(f"  Recursive:  {fib_recursive(n)}")
    print(f"  Iterative:  {fib_iterative(n)}")


def main():
    """Main function to demonstrate advanced recursion"""

    print("=" * 60)
    print("PROGRAM 72: ADVANCED RECURSION")
    print("=" * 60)

    # Basic Recursion Examples
    print("\n=== Basic Recursion Examples ===\n")

    rec = RecursionExamples()

    n = 5
    print(f"Factorial of {n}: {rec.factorial(n)}")

    n = 10
    print(f"Fibonacci of {n}: {rec.fibonacci(n)}")

    arr = [1, 2, 3, 4, 5]
    print(f"Sum of {arr}: {rec.sum_array(arr)}")

    s = "hello"
    print(f"Reverse of '{s}': {rec.reverse_string(s)}")

    arr = [1, 3, 5, 7, 9, 11, 13]
    target = 7
    print(f"Binary search {target} in {arr}: index {rec.binary_search(arr, target, 0, len(arr)-1)}")

    print("\nTower of Hanoi (3 disks):")
    rec.tower_of_hanoi(3, 'A', 'C', 'B')

    print("\n" + "=" * 60)

    # Memoization
    memoization_examples()

    print("\n" + "=" * 60)

    # Tail Recursion
    tail_recursion()

    print("\n" + "=" * 60)

    # Recursive Patterns
    recursive_patterns()

    print("\n" + "=" * 60)

    # Mutual Recursion
    mutual_recursion()

    print("\n" + "=" * 60)

    # Indirect Recursion
    indirect_recursion()

    print("\n" + "=" * 60)

    # Nested Recursion
    nested_recursion()

    print("\n" + "=" * 60)

    # Recursion to Iteration
    recursion_to_iteration()

    print("\n" + "=" * 60)
    print("Advanced recursion demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
