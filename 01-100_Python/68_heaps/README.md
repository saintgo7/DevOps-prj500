# Program 68: Heap Data Structure

Implementation of min-heap and max-heap with priority queue applications.

## Description

This program demonstrates heap data structure, a complete binary tree where each node satisfies the heap property. Heaps are fundamental to priority queues, heap sort, and various optimization algorithms.

## Learning Objectives

- Understand heap property and structure
- Implement heapify operations
- Master heap-based algorithms
- Learn priority queue applications
- Compare heap with other data structures

## Features

- **Min-Heap**: Parent ≤ children
- **Max-Heap**: Parent ≥ children
- **Core Operations**: Insert, extract-min/max, peek
- **Heapify**: Build heap from array
- **Heap Sort**: O(n log n) sorting algorithm
- **Priority Queue**: Task scheduling, event simulation
- **K-way Merge**: Merge sorted arrays
- **Top K Elements**: Find k largest/smallest
- **Median Finding**: Using two heaps

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/68_heaps
python src/main.py
```

## Key Concepts

### Time Complexity

- **Insert**: O(log n) - Bubble up
- **Extract Min/Max**: O(log n) - Bubble down
- **Peek**: O(1) - View root
- **Build Heap**: O(n) - Heapify array
- **Heap Sort**: O(n log n) - Extract all elements

### Space Complexity

- **Storage**: O(n) for n elements
- **Operations**: O(1) additional space (in-place)

### Heap Property

**Min-Heap:**
- Parent value ≤ child values
- Root is minimum element

**Max-Heap:**
- Parent value ≥ child values
- Root is maximum element

### Array Representation

For node at index `i`:
- **Left child**: `2*i + 1`
- **Right child**: `2*i + 2`
- **Parent**: `(i-1) // 2`

### Common Applications

1. **Priority Queue**: OS process scheduling
2. **Heap Sort**: In-place O(n log n) sorting
3. **Graph Algorithms**: Dijkstra's, Prim's
4. **K-th Largest/Smallest**: Order statistics
5. **Median Maintenance**: Streaming data
6. **Merge K Sorted Arrays**: Efficient merging
7. **Event Simulation**: Discrete event simulation

## Best Practices

1. **Use heapq module**: Optimized C implementation
2. **Store tuples for priority queue**: (priority, item)
3. **Use max-heap via negation**: Negate values for heapq
4. **Check heap property**: Validate after operations
5. **Consider Fibonacci heap**: For better decrease-key
6. **Use heap for top-K problems**: O(n log k) vs O(n log n)
7. **Build heap bottom-up**: O(n) vs O(n log n)

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Insert and extract sequences
# - Heap property validation
# - Build heap from array
# - Heap sort correctness
# - Edge cases (empty, single element)
# - Priority queue scenarios
```

## Navigation

- **Previous**: [Program 67 - Binary Search Trees](../67_binary_search_trees/README.md)
- **Next**: [Program 69 - Graphs](../69_graphs/README.md)
- **Home**: [Main README](../README.md)
