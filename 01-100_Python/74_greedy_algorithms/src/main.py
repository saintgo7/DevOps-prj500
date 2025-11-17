"""
Program 74: Greedy Algorithms - Activity Selection, Huffman Coding
Demonstrates greedy algorithm techniques with classic problems
"""

import heapq
from collections import defaultdict, Counter


class Activity:
    """Activity with start and finish time"""

    def __init__(self, name, start, finish):
        self.name = name
        self.start = start
        self.finish = finish

    def __repr__(self):
        return f"{self.name}({self.start}-{self.finish})"


def activity_selection():
    """
    Activity Selection Problem
    Select maximum number of non-overlapping activities
    Time: O(n log n), Space: O(n)
    """

    print("\n=== Activity Selection Problem ===\n")

    def select_activities(activities):
        """Greedy: always pick earliest finishing activity"""
        # Sort by finish time
        sorted_activities = sorted(activities, key=lambda x: x.finish)

        selected = [sorted_activities[0]]
        last_finish = sorted_activities[0].finish

        for activity in sorted_activities[1:]:
            if activity.start >= last_finish:
                selected.append(activity)
                last_finish = activity.finish

        return selected

    activities = [
        Activity("A1", 1, 4),
        Activity("A2", 3, 5),
        Activity("A3", 0, 6),
        Activity("A4", 5, 7),
        Activity("A5", 3, 9),
        Activity("A6", 5, 9),
        Activity("A7", 6, 10),
        Activity("A8", 8, 11),
        Activity("A9", 8, 12),
        Activity("A10", 2, 14),
        Activity("A11", 12, 16),
    ]

    print("Activities:")
    for act in activities:
        print(f"  {act}")

    selected = select_activities(activities)

    print(f"\nSelected activities: {len(selected)}")
    for act in selected:
        print(f"  {act}")


class HuffmanNode:
    """Node for Huffman tree"""

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def huffman_coding():
    """
    Huffman Coding - Optimal prefix-free encoding
    Time: O(n log n), Space: O(n)
    """

    print("\n=== Huffman Coding ===\n")

    def build_huffman_tree(text):
        """Build Huffman tree from text"""
        # Count frequency
        freq = Counter(text)

        # Create heap of nodes
        heap = [HuffmanNode(char, f) for char, f in freq.items()]
        heapq.heapify(heap)

        # Build tree
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            parent = HuffmanNode(None, left.freq + right.freq)
            parent.left = left
            parent.right = right

            heapq.heappush(heap, parent)

        return heap[0]

    def generate_codes(node, code="", codes=None):
        """Generate Huffman codes"""
        if codes is None:
            codes = {}

        if node.char is not None:
            codes[node.char] = code
            return codes

        if node.left:
            generate_codes(node.left, code + "0", codes)
        if node.right:
            generate_codes(node.right, code + "1", codes)

        return codes

    def encode(text, codes):
        """Encode text using Huffman codes"""
        return ''.join(codes[char] for char in text)

    def decode(encoded, root):
        """Decode Huffman encoded text"""
        decoded = []
        current = root

        for bit in encoded:
            if bit == '0':
                current = current.left
            else:
                current = current.right

            if current.char is not None:
                decoded.append(current.char)
                current = root

        return ''.join(decoded)

    text = "huffman coding is awesome"

    print(f"Original text: '{text}'")
    print(f"Length: {len(text)} characters")

    # Build Huffman tree and generate codes
    root = build_huffman_tree(text)
    codes = generate_codes(root)

    print("\nHuffman Codes:")
    for char, code in sorted(codes.items()):
        print(f"  '{char}': {code}")

    # Encode
    encoded = encode(text, codes)
    print(f"\nEncoded: {encoded}")
    print(f"Encoded length: {len(encoded)} bits")

    # Compare with fixed-length encoding
    import math
    unique_chars = len(codes)
    fixed_bits = math.ceil(math.log2(unique_chars))
    fixed_length = len(text) * fixed_bits

    print(f"\nFixed-length encoding: {fixed_length} bits ({fixed_bits} bits/char)")
    print(f"Compression ratio: {len(encoded) / fixed_length:.2%}")

    # Decode
    decoded = decode(encoded, root)
    print(f"\nDecoded: '{decoded}'")
    print(f"Correct: {decoded == text}")


def fractional_knapsack():
    """
    Fractional Knapsack - Can take fractions of items
    Time: O(n log n), Space: O(n)
    """

    print("\n=== Fractional Knapsack ===\n")

    class Item:
        def __init__(self, name, weight, value):
            self.name = name
            self.weight = weight
            self.value = value
            self.ratio = value / weight

        def __repr__(self):
            return f"{self.name}(w={self.weight}, v={self.value}, r={self.ratio:.2f})"

    def fractional_knapsack_greedy(items, capacity):
        """Greedy: pick items with highest value/weight ratio"""
        # Sort by value/weight ratio
        sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)

        total_value = 0
        selected = []

        for item in sorted_items:
            if capacity >= item.weight:
                # Take whole item
                capacity -= item.weight
                total_value += item.value
                selected.append((item, 1.0))
            elif capacity > 0:
                # Take fraction
                fraction = capacity / item.weight
                total_value += item.value * fraction
                selected.append((item, fraction))
                capacity = 0
                break

        return total_value, selected

    items = [
        Item("A", 10, 60),
        Item("B", 20, 100),
        Item("C", 30, 120),
    ]
    capacity = 50

    print("Items:")
    for item in items:
        print(f"  {item}")

    print(f"\nKnapsack capacity: {capacity}")

    total_value, selected = fractional_knapsack_greedy(items, capacity)

    print(f"\nMaximum value: {total_value}")
    print("Selected items:")
    for item, fraction in selected:
        print(f"  {item.name}: {fraction * 100:.0f}%")


def job_sequencing():
    """
    Job Sequencing with Deadlines
    Time: O(n²), Space: O(n)
    """

    print("\n=== Job Sequencing with Deadlines ===\n")

    class Job:
        def __init__(self, name, deadline, profit):
            self.name = name
            self.deadline = deadline
            self.profit = profit

        def __repr__(self):
            return f"{self.name}(d={self.deadline}, p={self.profit})"

    def schedule_jobs(jobs):
        """Greedy: schedule highest profit jobs first"""
        # Sort by profit (descending)
        sorted_jobs = sorted(jobs, key=lambda x: x.profit, reverse=True)

        # Find max deadline
        max_deadline = max(job.deadline for job in jobs)

        # Create time slots
        slots = [None] * max_deadline
        total_profit = 0

        for job in sorted_jobs:
            # Find slot for this job (from deadline backwards)
            for i in range(min(max_deadline, job.deadline) - 1, -1, -1):
                if slots[i] is None:
                    slots[i] = job
                    total_profit += job.profit
                    break

        return [job for job in slots if job], total_profit

    jobs = [
        Job("J1", 2, 100),
        Job("J2", 1, 19),
        Job("J3", 2, 27),
        Job("J4", 1, 25),
        Job("J5", 3, 15),
    ]

    print("Jobs:")
    for job in jobs:
        print(f"  {job}")

    scheduled, profit = schedule_jobs(jobs)

    print(f"\nScheduled jobs: {len(scheduled)}")
    for i, job in enumerate(scheduled, 1):
        print(f"  Time {i}: {job}")

    print(f"\nTotal profit: {profit}")


def coin_change_greedy():
    """
    Coin Change using Greedy (works for canonical coin systems)
    Time: O(n), Space: O(1)
    """

    print("\n=== Coin Change (Greedy) ===\n")

    def min_coins(coins, amount):
        """Greedy: always pick largest coin possible"""
        # Sort coins in descending order
        coins = sorted(coins, reverse=True)

        result = []
        remaining = amount

        for coin in coins:
            count = remaining // coin
            if count > 0:
                result.extend([coin] * count)
                remaining -= coin * count

            if remaining == 0:
                break

        return result if remaining == 0 else None

    coins = [1, 5, 10, 25]
    amounts = [41, 63, 99]

    print(f"Coins: {coins}")

    for amount in amounts:
        result = min_coins(coins, amount)
        if result:
            print(f"\nAmount: {amount}")
            print(f"Coins: {result}")
            print(f"Count: {len(result)}")


def minimum_platforms():
    """
    Minimum Platforms Required for Railway Station
    Time: O(n log n), Space: O(n)
    """

    print("\n=== Minimum Platforms Required ===\n")

    def min_platforms(arrivals, departures):
        """Find minimum platforms needed"""
        arrivals = sorted(arrivals)
        departures = sorted(departures)

        platforms_needed = 0
        max_platforms = 0
        i = j = 0
        n = len(arrivals)

        while i < n and j < n:
            if arrivals[i] <= departures[j]:
                platforms_needed += 1
                i += 1
                max_platforms = max(max_platforms, platforms_needed)
            else:
                platforms_needed -= 1
                j += 1

        return max_platforms

    arrivals = [900, 940, 950, 1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]

    print("Train Schedule:")
    for i in range(len(arrivals)):
        print(f"  Train {i + 1}: {arrivals[i]:04d} - {departures[i]:04d}")

    platforms = min_platforms(arrivals, departures)
    print(f"\nMinimum platforms required: {platforms}")


def minimum_spanning_tree_prims():
    """
    Prim's Algorithm for Minimum Spanning Tree
    Time: O(E log V), Space: O(V)
    """

    print("\n=== Minimum Spanning Tree (Prim's) ===\n")

    def prims_mst(graph, start):
        """Find MST using Prim's algorithm"""
        mst = []
        visited = {start}
        edges = [(weight, start, to) for to, weight in graph[start]]
        heapq.heapify(edges)
        total_weight = 0

        while edges:
            weight, frm, to = heapq.heappop(edges)

            if to not in visited:
                visited.add(to)
                mst.append((frm, to, weight))
                total_weight += weight

                for next_to, next_weight in graph[to]:
                    if next_to not in visited:
                        heapq.heappush(edges, (next_weight, to, next_to))

        return mst, total_weight

    # Graph as adjacency list
    graph = {
        'A': [('B', 2), ('C', 3)],
        'B': [('A', 2), ('C', 1), ('D', 1), ('E', 4)],
        'C': [('A', 3), ('B', 1), ('E', 5)],
        'D': [('B', 1), ('E', 1)],
        'E': [('B', 4), ('C', 5), ('D', 1)],
    }

    print("Graph edges:")
    for u in graph:
        for v, w in graph[u]:
            if u < v:  # Print each edge once
                print(f"  {u} -- {v} (weight: {w})")

    mst, total_weight = prims_mst(graph, 'A')

    print("\nMinimum Spanning Tree:")
    for u, v, w in mst:
        print(f"  {u} -- {v} (weight: {w})")

    print(f"\nTotal weight: {total_weight}")


def main():
    """Main function to demonstrate greedy algorithms"""

    print("=" * 60)
    print("PROGRAM 74: GREEDY ALGORITHMS")
    print("=" * 60)

    # Activity Selection
    activity_selection()

    print("\n" + "=" * 60)

    # Huffman Coding
    huffman_coding()

    print("\n" + "=" * 60)

    # Fractional Knapsack
    fractional_knapsack()

    print("\n" + "=" * 60)

    # Job Sequencing
    job_sequencing()

    print("\n" + "=" * 60)

    # Coin Change
    coin_change_greedy()

    print("\n" + "=" * 60)

    # Minimum Platforms
    minimum_platforms()

    print("\n" + "=" * 60)

    # Minimum Spanning Tree
    minimum_spanning_tree_prims()

    print("\n" + "=" * 60)
    print("Greedy algorithms demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
