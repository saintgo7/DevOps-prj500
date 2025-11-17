# Program 70: Sorting Algorithms

Implementation and comparison of various sorting algorithms with complexity analysis.

## Description

This program demonstrates multiple sorting algorithms including bubble sort, selection sort, insertion sort, merge sort, quick sort, and heap sort. Each algorithm is analyzed for time and space complexity with practical examples.

## Learning Objectives

- Understand different sorting techniques
- Analyze time and space complexity
- Compare algorithm performance
- Learn stability and adaptiveness
- Choose appropriate algorithm for use case

## Features

- **Simple Sorts**: Bubble, Selection, Insertion
- **Efficient Sorts**: Merge, Quick, Heap
- **Specialized Sorts**: Counting, Radix, Bucket
- **Performance Comparison**: Benchmark different algorithms
- **Stability Analysis**: Preserve relative order
- **Adaptive Behavior**: Performance on sorted data
- **Visualization**: Step-by-step execution

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/70_sorting_algorithms
python src/main.py
```

## Key Concepts

### Time Complexity Summary

| Algorithm | Best | Average | Worst | Stable | Space |
|-----------|------|---------|-------|--------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | Yes | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | No | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | Yes | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | Yes | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | No | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | No | O(1) |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | Yes | O(k) |

### Algorithm Characteristics

**Bubble Sort:**
- Simple but inefficient
- Good for educational purposes
- Adaptive (detects sorted data)

**Selection Sort:**
- Minimizes swaps
- Not adaptive
- Poor performance

**Insertion Sort:**
- Efficient for small/nearly sorted data
- Adaptive
- Online algorithm

**Merge Sort:**
- Guaranteed O(n log n)
- Stable
- Good for linked lists
- Requires extra space

**Quick Sort:**
- Average O(n log n)
- In-place
- Not stable
- Cache-friendly

**Heap Sort:**
- Guaranteed O(n log n)
- In-place
- Not stable
- Poor cache locality

## Best Practices

1. **Use built-in sort()**: Highly optimized (Timsort)
2. **Use sorted() for new list**: Non-destructive
3. **Provide key function**: For custom sorting
4. **Consider stability**: When order matters
5. **Use insertion sort for small data**: < 10 elements
6. **Use quick sort for in-place sorting**: Average case
7. **Use merge sort for stability guarantee**

## Testing

```bash
# Run tests
pytest tests/

# Benchmark
python src/main.py --benchmark

# Test cases
# - Empty array
# - Single element
# - Already sorted
# - Reverse sorted
# - Random data
# - Duplicates
# - Large datasets
```

## Navigation

- **Previous**: [Program 69 - Graphs](../69_graphs/README.md)
- **Next**: [Program 71 - Searching Algorithms](../71_searching_algorithms/README.md)
- **Home**: [Main README](../README.md)
