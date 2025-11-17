"""
Program 73: Dynamic Programming - Fibonacci, Knapsack, LCS, Coin Change
Demonstrates dynamic programming techniques with classic problems
"""

from functools import lru_cache


class DynamicProgramming:
    """Collection of dynamic programming solutions"""

    # 1. Fibonacci Sequence
    def fibonacci_recursive(self, n):
        """Naive recursive - Time: O(2^n), Space: O(n)"""
        if n <= 1:
            return n
        return self.fibonacci_recursive(n - 1) + self.fibonacci_recursive(n - 2)

    def fibonacci_memoization(self, n, memo=None):
        """Top-down DP - Time: O(n), Space: O(n)"""
        if memo is None:
            memo = {}

        if n in memo:
            return memo[n]

        if n <= 1:
            return n

        memo[n] = self.fibonacci_memoization(n - 1, memo) + \
                   self.fibonacci_memoization(n - 2, memo)
        return memo[n]

    def fibonacci_tabulation(self, n):
        """Bottom-up DP - Time: O(n), Space: O(n)"""
        if n <= 1:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    def fibonacci_optimized(self, n):
        """Space-optimized - Time: O(n), Space: O(1)"""
        if n <= 1:
            return n

        prev, curr = 0, 1

        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr

        return curr

    # 2. Longest Common Subsequence (LCS)
    def lcs_recursive(self, s1, s2, m=None, n=None):
        """Naive recursive - Time: O(2^n)"""
        if m is None:
            m = len(s1)
        if n is None:
            n = len(s2)

        if m == 0 or n == 0:
            return 0

        if s1[m - 1] == s2[n - 1]:
            return 1 + self.lcs_recursive(s1, s2, m - 1, n - 1)

        return max(self.lcs_recursive(s1, s2, m - 1, n),
                   self.lcs_recursive(s1, s2, m, n - 1))

    def lcs_dp(self, s1, s2):
        """Bottom-up DP - Time: O(m*n), Space: O(m*n)"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    def lcs_with_sequence(self, s1, s2):
        """Return LCS length and the actual sequence"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Build DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Backtrack to find sequence
        lcs = []
        i, j = m, n

        while i > 0 and j > 0:
            if s1[i - 1] == s2[j - 1]:
                lcs.append(s1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return dp[m][n], ''.join(reversed(lcs))

    # 3. 0/1 Knapsack
    def knapsack_recursive(self, weights, values, capacity, n=None):
        """Naive recursive - Time: O(2^n)"""
        if n is None:
            n = len(weights)

        if n == 0 or capacity == 0:
            return 0

        # If weight exceeds capacity, skip item
        if weights[n - 1] > capacity:
            return self.knapsack_recursive(weights, values, capacity, n - 1)

        # Max of including or excluding item
        include = values[n - 1] + self.knapsack_recursive(
            weights, values, capacity - weights[n - 1], n - 1)
        exclude = self.knapsack_recursive(weights, values, capacity, n - 1)

        return max(include, exclude)

    def knapsack_dp(self, weights, values, capacity):
        """Bottom-up DP - Time: O(n*W), Space: O(n*W)"""
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    dp[i][w] = dp[i - 1][w]

        return dp[n][capacity]

    # 4. Coin Change
    def coin_change_min(self, coins, amount):
        """Minimum coins to make amount - Time: O(amount * coins)"""
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1

    def coin_change_ways(self, coins, amount):
        """Number of ways to make amount - Time: O(amount * coins)"""
        dp = [0] * (amount + 1)
        dp[0] = 1

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]

        return dp[amount]


def edit_distance():
    """Edit Distance (Levenshtein Distance)"""

    print("\n=== Edit Distance ===\n")

    def min_edit_distance(s1, s2):
        """Minimum operations to convert s1 to s2 - Time: O(m*n)"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i

        for j in range(n + 1):
            dp[0][j] = j

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # Delete
                        dp[i][j - 1],      # Insert
                        dp[i - 1][j - 1]   # Replace
                    )

        return dp[m][n]

    s1 = "kitten"
    s2 = "sitting"

    print(f"String 1: {s1}")
    print(f"String 2: {s2}")
    print(f"Edit distance: {min_edit_distance(s1, s2)}")


def longest_increasing_subsequence():
    """Longest Increasing Subsequence"""

    print("\n=== Longest Increasing Subsequence ===\n")

    def lis_dp(arr):
        """LIS using DP - Time: O(n²), Space: O(n)"""
        n = len(arr)
        dp = [1] * n

        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Array: {arr}")
    print(f"Length of LIS: {lis_dp(arr)}")


def matrix_chain_multiplication():
    """Matrix Chain Multiplication"""

    print("\n=== Matrix Chain Multiplication ===\n")

    def matrix_chain_order(dimensions):
        """Minimum scalar multiplications - Time: O(n³)"""
        n = len(dimensions) - 1
        dp = [[0] * n for _ in range(n)]

        # Length of chain
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float('inf')

                for k in range(i, j):
                    cost = (dp[i][k] + dp[k + 1][j] +
                           dimensions[i] * dimensions[k + 1] * dimensions[j + 1])
                    dp[i][j] = min(dp[i][j], cost)

        return dp[0][n - 1]

    # Matrices: A1(10x20), A2(20x30), A3(30x40), A4(40x30)
    dimensions = [10, 20, 30, 40, 30]

    print(f"Matrix dimensions: {dimensions}")
    print(f"Minimum multiplications: {matrix_chain_order(dimensions)}")


def rod_cutting():
    """Rod Cutting Problem"""

    print("\n=== Rod Cutting Problem ===\n")

    def max_revenue(prices, length):
        """Maximum revenue from cutting rod - Time: O(n²)"""
        dp = [0] * (length + 1)

        for i in range(1, length + 1):
            max_val = float('-inf')
            for j in range(i):
                max_val = max(max_val, prices[j] + dp[i - j - 1])
            dp[i] = max_val

        return dp[length]

    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    length = 8

    print(f"Prices: {prices}")
    print(f"Rod length: {length}")
    print(f"Maximum revenue: {max_revenue(prices, length)}")


def subset_sum():
    """Subset Sum Problem"""

    print("\n=== Subset Sum Problem ===\n")

    def has_subset_sum(arr, target):
        """Check if subset with given sum exists - Time: O(n*sum)"""
        n = len(arr)
        dp = [[False] * (target + 1) for _ in range(n + 1)]

        # Empty subset has sum 0
        for i in range(n + 1):
            dp[i][0] = True

        for i in range(1, n + 1):
            for j in range(1, target + 1):
                if arr[i - 1] <= j:
                    dp[i][j] = dp[i - 1][j] or dp[i - 1][j - arr[i - 1]]
                else:
                    dp[i][j] = dp[i - 1][j]

        return dp[n][target]

    arr = [3, 34, 4, 12, 5, 2]
    target = 9

    print(f"Array: {arr}")
    print(f"Target sum: {target}")
    print(f"Subset exists: {has_subset_sum(arr, target)}")


def partition_equal_subset():
    """Partition Equal Subset Sum"""

    print("\n=== Partition Equal Subset Sum ===\n")

    def can_partition(arr):
        """Check if array can be partitioned into equal sum subsets"""
        total = sum(arr)

        if total % 2 != 0:
            return False

        target = total // 2
        n = len(arr)
        dp = [[False] * (target + 1) for _ in range(n + 1)]

        for i in range(n + 1):
            dp[i][0] = True

        for i in range(1, n + 1):
            for j in range(1, target + 1):
                if arr[i - 1] <= j:
                    dp[i][j] = dp[i - 1][j] or dp[i - 1][j - arr[i - 1]]
                else:
                    dp[i][j] = dp[i - 1][j]

        return dp[n][target]

    arr = [1, 5, 11, 5]
    print(f"Array: {arr}")
    print(f"Can partition: {can_partition(arr)}")


def climbing_stairs():
    """Climbing Stairs Problem"""

    print("\n=== Climbing Stairs ===\n")

    def count_ways(n):
        """Count ways to climb n stairs (1 or 2 steps) - Time: O(n)"""
        if n <= 2:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2

        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    n = 5
    print(f"Number of stairs: {n}")
    print(f"Ways to climb: {count_ways(n)}")


def main():
    """Main function to demonstrate dynamic programming"""

    print("=" * 60)
    print("PROGRAM 73: DYNAMIC PROGRAMMING")
    print("=" * 60)

    dp = DynamicProgramming()

    # Fibonacci
    print("\n=== Fibonacci Sequence ===\n")
    n = 10

    print(f"Fibonacci({n}):")
    print(f"  Memoization:  {dp.fibonacci_memoization(n)}")
    print(f"  Tabulation:   {dp.fibonacci_tabulation(n)}")
    print(f"  Optimized:    {dp.fibonacci_optimized(n)}")

    print("\n" + "=" * 60)

    # Longest Common Subsequence
    print("\n=== Longest Common Subsequence ===\n")

    s1 = "AGGTAB"
    s2 = "GXTXAYB"

    print(f"String 1: {s1}")
    print(f"String 2: {s2}")

    length, sequence = dp.lcs_with_sequence(s1, s2)
    print(f"LCS length: {length}")
    print(f"LCS: {sequence}")

    print("\n" + "=" * 60)

    # 0/1 Knapsack
    print("\n=== 0/1 Knapsack Problem ===\n")

    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    print(f"Weights:  {weights}")
    print(f"Values:   {values}")
    print(f"Capacity: {capacity}")
    print(f"Maximum value: {dp.knapsack_dp(weights, values, capacity)}")

    print("\n" + "=" * 60)

    # Coin Change
    print("\n=== Coin Change Problem ===\n")

    coins = [1, 2, 5]
    amount = 11

    print(f"Coins: {coins}")
    print(f"Amount: {amount}")
    print(f"Minimum coins: {dp.coin_change_min(coins, amount)}")
    print(f"Number of ways: {dp.coin_change_ways(coins, amount)}")

    print("\n" + "=" * 60)

    # Edit Distance
    edit_distance()

    print("\n" + "=" * 60)

    # Longest Increasing Subsequence
    longest_increasing_subsequence()

    print("\n" + "=" * 60)

    # Matrix Chain Multiplication
    matrix_chain_multiplication()

    print("\n" + "=" * 60)

    # Rod Cutting
    rod_cutting()

    print("\n" + "=" * 60)

    # Subset Sum
    subset_sum()

    print("\n" + "=" * 60)

    # Partition Equal Subset
    partition_equal_subset()

    print("\n" + "=" * 60)

    # Climbing Stairs
    climbing_stairs()

    print("\n" + "=" * 60)
    print("Dynamic programming demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
