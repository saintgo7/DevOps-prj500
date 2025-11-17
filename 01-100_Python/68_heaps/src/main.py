"""
Program 68: Heaps - Min/Max Heap, Heapify, and Heap Sort
Demonstrates heap data structure and its applications
"""

import heapq


class MinHeap:
    """Min Heap implementation"""

    def __init__(self):
        self.heap = []

    def parent(self, i):
        """Get parent index"""
        return (i - 1) // 2

    def left_child(self, i):
        """Get left child index"""
        return 2 * i + 1

    def right_child(self, i):
        """Get right child index"""
        return 2 * i + 2

    # Time Complexity: O(log n)
    def insert(self, value):
        """Insert value into heap"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """Maintain heap property upward"""
        parent = self.parent(index)

        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    # Time Complexity: O(log n)
    def extract_min(self):
        """Remove and return minimum element"""
        if not self.heap:
            raise IndexError("extract_min from empty heap")

        if len(self.heap) == 1:
            return self.heap.pop()

        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return min_val

    def _heapify_down(self, index):
        """Maintain heap property downward"""
        smallest = index
        left = self.left_child(index)
        right = self.right_child(index)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    # Time Complexity: O(1)
    def get_min(self):
        """Return minimum element without removing"""
        if not self.heap:
            raise IndexError("get_min from empty heap")
        return self.heap[0]

    def size(self):
        """Return heap size"""
        return len(self.heap)

    def is_empty(self):
        """Check if heap is empty"""
        return len(self.heap) == 0

    def display(self):
        """Display heap array"""
        return self.heap


class MaxHeap:
    """Max Heap implementation"""

    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    # Time Complexity: O(log n)
    def insert(self, value):
        """Insert value into heap"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """Maintain heap property upward"""
        parent = self.parent(index)

        if index > 0 and self.heap[index] > self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    # Time Complexity: O(log n)
    def extract_max(self):
        """Remove and return maximum element"""
        if not self.heap:
            raise IndexError("extract_max from empty heap")

        if len(self.heap) == 1:
            return self.heap.pop()

        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return max_val

    def _heapify_down(self, index):
        """Maintain heap property downward"""
        largest = index
        left = self.left_child(index)
        right = self.right_child(index)

        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left

        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

    def get_max(self):
        """Return maximum element without removing"""
        if not self.heap:
            raise IndexError("get_max from empty heap")
        return self.heap[0]

    def display(self):
        """Display heap array"""
        return self.heap


def build_heap_from_array():
    """Build heap from array - Time: O(n)"""

    print("\n=== Build Heap from Array ===\n")

    def heapify(arr, n, i):
        """Heapify subtree rooted at index i (for max heap)"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    def build_max_heap(arr):
        """Build max heap from array"""
        n = len(arr)
        # Start from last non-leaf node
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        return arr

    arr = [4, 10, 3, 5, 1, 8, 9, 2, 7, 6]
    print(f"Original array: {arr}")

    heap_arr = arr.copy()
    build_max_heap(heap_arr)
    print(f"Max heap: {heap_arr}")


def heap_sort():
    """Heap Sort implementation - Time: O(n log n), Space: O(1)"""

    print("\n=== Heap Sort ===\n")

    def heapify(arr, n, i):
        """Heapify for max heap"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    def sort(arr):
        """Sort array using heap sort"""
        n = len(arr)

        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)

        print(f"After building max heap: {arr}")

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            heapify(arr, i, 0)

        return arr

    arr = [12, 11, 13, 5, 6, 7]
    print(f"Original array: {arr}")

    sorted_arr = sort(arr.copy())
    print(f"Sorted array: {sorted_arr}")


def kth_largest_smallest():
    """Find kth largest and smallest elements using heap"""

    print("\n=== Kth Largest and Smallest Elements ===\n")

    def kth_largest(arr, k):
        """Find kth largest - Time: O(n log k)"""
        # Use min heap of size k
        min_heap = []

        for num in arr:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return min_heap[0]

    def kth_smallest(arr, k):
        """Find kth smallest - Time: O(n log k)"""
        # Use max heap of size k
        max_heap = []

        for num in arr:
            heapq.heappush(max_heap, -num)
            if len(max_heap) > k:
                heapq.heappop(max_heap)

        return -max_heap[0]

    arr = [7, 10, 4, 3, 20, 15]
    k = 3

    print(f"Array: {arr}")
    print(f"K: {k}")
    print(f"\n{k}rd largest: {kth_largest(arr, k)}")
    print(f"{k}rd smallest: {kth_smallest(arr, k)}")


def merge_k_sorted_arrays():
    """Merge k sorted arrays using min heap"""

    print("\n=== Merge K Sorted Arrays ===\n")

    def merge_arrays(arrays):
        """Merge k sorted arrays - Time: O(n log k)"""
        min_heap = []
        result = []

        # Initialize heap with first element from each array
        for i, arr in enumerate(arrays):
            if arr:
                heapq.heappush(min_heap, (arr[0], i, 0))

        # Extract min and add next element from same array
        while min_heap:
            val, array_idx, element_idx = heapq.heappop(min_heap)
            result.append(val)

            if element_idx + 1 < len(arrays[array_idx]):
                next_val = arrays[array_idx][element_idx + 1]
                heapq.heappush(min_heap, (next_val, array_idx, element_idx + 1))

        return result

    arrays = [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9]
    ]

    print("Arrays to merge:")
    for i, arr in enumerate(arrays):
        print(f"  Array {i + 1}: {arr}")

    merged = merge_arrays(arrays)
    print(f"\nMerged array: {merged}")


def top_k_frequent_elements():
    """Find top k frequent elements using heap"""

    print("\n=== Top K Frequent Elements ===\n")

    def top_k_frequent(nums, k):
        """Find k most frequent elements - Time: O(n log k)"""
        # Count frequencies
        freq_map = {}
        for num in nums:
            freq_map[num] = freq_map.get(num, 0) + 1

        # Use min heap of size k
        min_heap = []

        for num, freq in freq_map.items():
            heapq.heappush(min_heap, (freq, num))
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return [num for freq, num in min_heap]

    nums = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]
    k = 2

    print(f"Array: {nums}")
    print(f"K: {k}")
    print(f"Top {k} frequent elements: {top_k_frequent(nums, k)}")


def median_in_stream():
    """Find median in a data stream using two heaps"""

    print("\n=== Median in Data Stream ===\n")

    class MedianFinder:
        """Find median using max heap and min heap"""

        def __init__(self):
            self.max_heap = []  # Lower half (max heap)
            self.min_heap = []  # Upper half (min heap)

        def add_num(self, num):
            """Add number - Time: O(log n)"""
            # Add to max heap (lower half)
            heapq.heappush(self.max_heap, -num)

            # Balance: move largest from max heap to min heap
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))

            # Balance sizes
            if len(self.min_heap) > len(self.max_heap):
                heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

        def find_median(self):
            """Find median - Time: O(1)"""
            if len(self.max_heap) > len(self.min_heap):
                return -self.max_heap[0]
            return (-self.max_heap[0] + self.min_heap[0]) / 2

    mf = MedianFinder()
    stream = [5, 15, 1, 3, 8, 7, 9, 10]

    print("Adding numbers to stream:")
    for num in stream:
        mf.add_num(num)
        print(f"  Added {num}, median: {mf.find_median()}")


def connect_ropes_min_cost():
    """Connect ropes with minimum cost using min heap"""

    print("\n=== Connect Ropes with Minimum Cost ===\n")

    def min_cost(ropes):
        """Calculate minimum cost - Time: O(n log n)"""
        heapq.heapify(ropes)
        total_cost = 0

        while len(ropes) > 1:
            # Take two smallest ropes
            first = heapq.heappop(ropes)
            second = heapq.heappop(ropes)

            # Connect them
            cost = first + second
            total_cost += cost

            # Add back to heap
            heapq.heappush(ropes, cost)

        return total_cost

    ropes = [4, 3, 2, 6]
    print(f"Rope lengths: {ropes}")
    print(f"Minimum cost to connect: {min_cost(ropes.copy())}")

    # Show steps
    print("\nStep-by-step:")
    ropes_copy = ropes.copy()
    heapq.heapify(ropes_copy)
    step = 1
    total = 0

    while len(ropes_copy) > 1:
        first = heapq.heappop(ropes_copy)
        second = heapq.heappop(ropes_copy)
        cost = first + second
        total += cost
        print(f"  Step {step}: Connect {first} and {second}, cost = {cost}, total = {total}")
        heapq.heappush(ropes_copy, cost)
        step += 1


def main():
    """Main function to demonstrate heap operations"""

    print("=" * 60)
    print("PROGRAM 68: HEAPS - MIN/MAX HEAP, HEAPIFY, HEAP SORT")
    print("=" * 60)

    # Min Heap Operations
    print("\n=== Min Heap Operations ===\n")

    min_heap = MinHeap()
    values = [4, 8, 2, 7, 3, 1, 10, 5]

    print(f"Inserting values: {values}")
    for val in values:
        min_heap.insert(val)

    print(f"Min heap array: {min_heap.display()}")
    print(f"Minimum element: {min_heap.get_min()}")

    print("\nExtracting minimum elements:")
    for _ in range(3):
        print(f"  Extracted: {min_heap.extract_min()}")

    print(f"Heap after extractions: {min_heap.display()}")

    print("\n" + "-" * 60)

    # Max Heap Operations
    print("\n=== Max Heap Operations ===\n")

    max_heap = MaxHeap()

    print(f"Inserting values: {values}")
    for val in values:
        max_heap.insert(val)

    print(f"Max heap array: {max_heap.display()}")
    print(f"Maximum element: {max_heap.get_max()}")

    print("\nExtracting maximum elements:")
    for _ in range(3):
        print(f"  Extracted: {max_heap.extract_max()}")

    print(f"Heap after extractions: {max_heap.display()}")

    print("\n" + "-" * 60)

    # Build heap from array
    build_heap_from_array()

    print("\n" + "-" * 60)

    # Heap sort
    heap_sort()

    print("\n" + "-" * 60)

    # Kth largest/smallest
    kth_largest_smallest()

    print("\n" + "-" * 60)

    # Merge k sorted arrays
    merge_k_sorted_arrays()

    print("\n" + "-" * 60)

    # Top k frequent
    top_k_frequent_elements()

    print("\n" + "-" * 60)

    # Median in stream
    median_in_stream()

    print("\n" + "-" * 60)

    # Connect ropes
    connect_ropes_min_cost()

    print("\n" + "=" * 60)
    print("Heap operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
