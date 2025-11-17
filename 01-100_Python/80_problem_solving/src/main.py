"""
Program 80: Problem Solving - Common Patterns, Techniques, Strategies
Demonstrates problem-solving patterns and strategies for coding interviews
"""


def two_pointer_technique():
    """
    Two Pointer Technique
    Used for: Array problems, string problems, linked lists
    """

    print("\n=== Two Pointer Technique ===\n")

    # Problem 1: Two Sum (sorted array)
    def two_sum_sorted(arr, target):
        """Find pair that sums to target - Time: O(n)"""
        left, right = 0, len(arr) - 1

        while left < right:
            current_sum = arr[left] + arr[right]

            if current_sum == target:
                return [left, right]
            elif current_sum < target:
                left += 1
            else:
                right -= 1

        return None

    arr = [1, 2, 3, 4, 6]
    target = 6
    print(f"Two Sum (sorted array):")
    print(f"  Array: {arr}, Target: {target}")
    print(f"  Indices: {two_sum_sorted(arr, target)}")

    # Problem 2: Container with most water
    def max_area(heights):
        """Find container with most water - Time: O(n)"""
        left, right = 0, len(heights) - 1
        max_water = 0

        while left < right:
            width = right - left
            height = min(heights[left], heights[right])
            max_water = max(max_water, width * height)

            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1

        return max_water

    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"\nContainer with Most Water:")
    print(f"  Heights: {heights}")
    print(f"  Max area: {max_area(heights)}")

    # Problem 3: Remove duplicates from sorted array
    def remove_duplicates(arr):
        """Remove duplicates in-place - Time: O(n)"""
        if not arr:
            return 0

        write = 1
        for read in range(1, len(arr)):
            if arr[read] != arr[read - 1]:
                arr[write] = arr[read]
                write += 1

        return write

    arr = [1, 1, 2, 2, 2, 3, 4, 4, 5]
    print(f"\nRemove Duplicates:")
    print(f"  Original: {arr}")
    length = remove_duplicates(arr)
    print(f"  Result: {arr[:length]}")


def sliding_window_technique():
    """
    Sliding Window Technique
    Used for: Substring problems, subarray problems
    """

    print("\n=== Sliding Window Technique ===\n")

    # Problem 1: Maximum sum subarray of size k
    def max_sum_subarray(arr, k):
        """Find max sum of k consecutive elements - Time: O(n)"""
        if len(arr) < k:
            return None

        window_sum = sum(arr[:k])
        max_sum = window_sum

        for i in range(k, len(arr)):
            window_sum = window_sum - arr[i - k] + arr[i]
            max_sum = max(max_sum, window_sum)

        return max_sum

    arr = [1, 4, 2, 10, 23, 3, 1, 0, 20]
    k = 4
    print(f"Maximum Sum Subarray (size {k}):")
    print(f"  Array: {arr}")
    print(f"  Max sum: {max_sum_subarray(arr, k)}")

    # Problem 2: Longest substring without repeating characters
    def longest_unique_substring(s):
        """Find longest substring without repeats - Time: O(n)"""
        char_set = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1

            char_set.add(s[right])
            max_length = max(max_length, right - left + 1)

        return max_length

    s = "abcabcbb"
    print(f"\nLongest Unique Substring:")
    print(f"  String: {s}")
    print(f"  Length: {longest_unique_substring(s)}")


def fast_slow_pointer():
    """
    Fast & Slow Pointer (Floyd's Algorithm)
    Used for: Linked list cycle detection, finding middle
    """

    print("\n=== Fast & Slow Pointer ===\n")

    class ListNode:
        def __init__(self, val):
            self.val = val
            self.next = None

    # Problem 1: Detect cycle
    def has_cycle(head):
        """Detect cycle in linked list - Time: O(n)"""
        if not head:
            return False

        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False

    # Create list with cycle
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = head.next  # Create cycle

    print("Linked List Cycle Detection:")
    print(f"  Has cycle: {has_cycle(head)}")

    # Problem 2: Find middle element
    def find_middle(head):
        """Find middle element - Time: O(n)"""
        if not head:
            return None

        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.val

    # Create list without cycle
    head2 = ListNode(1)
    head2.next = ListNode(2)
    head2.next.next = ListNode(3)
    head2.next.next.next = ListNode(4)
    head2.next.next.next.next = ListNode(5)

    print(f"\nFind Middle Element:")
    print(f"  Middle: {find_middle(head2)}")


def divide_and_conquer():
    """
    Divide and Conquer
    Used for: Sorting, searching, optimization problems
    """

    print("\n=== Divide and Conquer ===\n")

    # Problem 1: Maximum subarray sum (Kadane's)
    def max_subarray_sum(arr):
        """Find maximum subarray sum - Time: O(n)"""
        max_sum = current_sum = arr[0]

        for num in arr[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum

    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"Maximum Subarray Sum:")
    print(f"  Array: {arr}")
    print(f"  Max sum: {max_subarray_sum(arr)}")

    # Problem 2: Merge K sorted lists
    import heapq

    def merge_k_sorted_lists(lists):
        """Merge k sorted lists - Time: O(n log k)"""
        heap = []
        result = []

        # Initialize heap with first element from each list
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(heap, (lst[0], i, 0))

        while heap:
            val, list_idx, elem_idx = heapq.heappop(heap)
            result.append(val)

            if elem_idx + 1 < len(lists[list_idx]):
                next_val = lists[list_idx][elem_idx + 1]
                heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

        return result

    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print(f"\nMerge K Sorted Lists:")
    print(f"  Lists: {lists}")
    print(f"  Merged: {merge_k_sorted_lists(lists)}")


def greedy_approach():
    """
    Greedy Approach
    Used for: Optimization problems
    """

    print("\n=== Greedy Approach ===\n")

    # Problem 1: Jump game
    def can_jump(nums):
        """Can reach last index - Time: O(n)"""
        max_reach = 0

        for i in range(len(nums)):
            if i > max_reach:
                return False

            max_reach = max(max_reach, i + nums[i])

            if max_reach >= len(nums) - 1:
                return True

        return True

    nums = [2, 3, 1, 1, 4]
    print(f"Jump Game:")
    print(f"  Array: {nums}")
    print(f"  Can reach end: {can_jump(nums)}")

    # Problem 2: Gas station
    def can_complete_circuit(gas, cost):
        """Find starting gas station - Time: O(n)"""
        if sum(gas) < sum(cost):
            return -1

        total = 0
        start = 0

        for i in range(len(gas)):
            total += gas[i] - cost[i]

            if total < 0:
                total = 0
                start = i + 1

        return start

    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    print(f"\nGas Station:")
    print(f"  Gas: {gas}")
    print(f"  Cost: {cost}")
    print(f"  Starting station: {can_complete_circuit(gas, cost)}")


def dynamic_programming_patterns():
    """
    Dynamic Programming Patterns
    Used for: Optimization, counting problems
    """

    print("\n=== Dynamic Programming Patterns ===\n")

    # Pattern 1: Fibonacci-like (1D DP)
    def climb_stairs(n):
        """Ways to climb n stairs - Time: O(n)"""
        if n <= 2:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2

        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    n = 5
    print(f"Climbing Stairs ({n} steps):")
    print(f"  Ways: {climb_stairs(n)}")

    # Pattern 2: Grid-based (2D DP)
    def unique_paths(m, n):
        """Unique paths in m×n grid - Time: O(m*n)"""
        dp = [[1] * n for _ in range(m)]

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]

    m, n = 3, 7
    print(f"\nUnique Paths ({m}×{n} grid):")
    print(f"  Paths: {unique_paths(m, n)}")


def hash_map_patterns():
    """
    Hash Map Patterns
    Used for: Frequency counting, lookup optimization
    """

    print("\n=== Hash Map Patterns ===\n")

    # Problem 1: Two sum
    def two_sum(nums, target):
        """Find two numbers that sum to target - Time: O(n)"""
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i

        return None

    nums = [2, 7, 11, 15]
    target = 9
    print(f"Two Sum:")
    print(f"  Array: {nums}, Target: {target}")
    print(f"  Indices: {two_sum(nums, target)}")

    # Problem 2: Group anagrams
    def group_anagrams(strs):
        """Group anagrams together - Time: O(n*k log k)"""
        from collections import defaultdict

        groups = defaultdict(list)

        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)

        return list(groups.values())

    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"\nGroup Anagrams:")
    print(f"  Strings: {strs}")
    print(f"  Groups: {group_anagrams(strs)}")


def binary_search_patterns():
    """
    Binary Search Patterns
    Used for: Search in sorted array, optimization
    """

    print("\n=== Binary Search Patterns ===\n")

    # Problem 1: Find peak element
    def find_peak_element(nums):
        """Find peak element - Time: O(log n)"""
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > nums[mid + 1]:
                right = mid
            else:
                left = mid + 1

        return left

    nums = [1, 2, 3, 1]
    print(f"Find Peak Element:")
    print(f"  Array: {nums}")
    print(f"  Peak index: {find_peak_element(nums)}")

    # Problem 2: Search in rotated sorted array
    def search_rotated(nums, target):
        """Search in rotated array - Time: O(log n)"""
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Left half is sorted
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # Right half is sorted
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1

    nums = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    print(f"\nSearch in Rotated Array:")
    print(f"  Array: {nums}, Target: {target}")
    print(f"  Index: {search_rotated(nums, target)}")


def bit_manipulation_patterns():
    """
    Bit Manipulation Patterns
    Used for: Optimization, set operations
    """

    print("\n=== Bit Manipulation Patterns ===\n")

    # Problem 1: Single number
    def single_number(nums):
        """Find number that appears once - Time: O(n)"""
        result = 0
        for num in nums:
            result ^= num
        return result

    nums = [4, 1, 2, 1, 2]
    print(f"Single Number:")
    print(f"  Array: {nums}")
    print(f"  Single: {single_number(nums)}")

    # Problem 2: Count set bits
    def count_bits(n):
        """Count set bits in number - Time: O(log n)"""
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count

    n = 13
    print(f"\nCount Set Bits:")
    print(f"  Number: {n} (binary: {bin(n)})")
    print(f"  Set bits: {count_bits(n)}")


def main():
    """Main function to demonstrate problem-solving patterns"""

    print("=" * 60)
    print("PROGRAM 80: PROBLEM SOLVING PATTERNS & TECHNIQUES")
    print("=" * 60)

    # Two Pointer
    two_pointer_technique()

    print("\n" + "=" * 60)

    # Sliding Window
    sliding_window_technique()

    print("\n" + "=" * 60)

    # Fast & Slow Pointer
    fast_slow_pointer()

    print("\n" + "=" * 60)

    # Divide and Conquer
    divide_and_conquer()

    print("\n" + "=" * 60)

    # Greedy
    greedy_approach()

    print("\n" + "=" * 60)

    # Dynamic Programming
    dynamic_programming_patterns()

    print("\n" + "=" * 60)

    # Hash Map
    hash_map_patterns()

    print("\n" + "=" * 60)

    # Binary Search
    binary_search_patterns()

    print("\n" + "=" * 60)

    # Bit Manipulation
    bit_manipulation_patterns()

    print("\n" + "=" * 60)
    print("Problem solving patterns demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
