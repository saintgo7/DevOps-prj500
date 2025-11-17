# Program 71: Searching Algorithms

Implementation and analysis of various searching algorithms and techniques.

## Description

This program demonstrates different searching algorithms including linear search, binary search, interpolation search, and jump search. Each algorithm is optimized for different data characteristics and use cases.

## Learning Objectives

- Understand searching algorithm principles
- Analyze time and space complexity
- Learn when to use each algorithm
- Master binary search and variants
- Apply searching to real problems

## Features

- **Linear Search**: Sequential scanning
- **Binary Search**: Divide and conquer on sorted data
- **Interpolation Search**: Probe position based on value
- **Jump Search**: Block-based searching
- **Exponential Search**: Find range then binary search
- **Ternary Search**: Three-way divide
- **Search in Rotated Array**: Modified binary search
- **Search 2D Matrix**: Row and column search

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/71_searching_algorithms
python src/main.py
```

## Key Concepts

### Time Complexity

| Algorithm | Best | Average | Worst | Space | Requirements |
|-----------|------|---------|-------|-------|--------------|
| Linear Search | O(1) | O(n) | O(n) | O(1) | None |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) | Sorted |
| Interpolation | O(1) | O(log log n) | O(n) | O(1) | Sorted, uniform |
| Jump Search | O(1) | O(√n) | O(√n) | O(1) | Sorted |
| Exponential | O(1) | O(log n) | O(log n) | O(1) | Sorted |

### Algorithm Details

**Linear Search:**
- Simplest search algorithm
- Works on unsorted data
- Best for small datasets or when data rarely searched

**Binary Search:**
- Most common efficient search
- Requires sorted data
- Halves search space each iteration
- Can be recursive or iterative

**Interpolation Search:**
- Better than binary for uniformly distributed data
- Calculates probable position
- Degrades to linear search in worst case

**Jump Search:**
- Optimal jump size is √n
- Better than linear, worse than binary
- Good for systems where backward movement is costly

## Best Practices

1. **Use binary search for sorted data**: O(log n) is very efficient
2. **Implement iterative binary search**: Avoid stack overhead
3. **Handle edge cases**: Empty array, single element
4. **Check bounds carefully**: Prevent index errors
5. **Use bisect module in Python**: Optimized binary search
6. **Consider data distribution**: Interpolation for uniform data
7. **Verify sorted prerequisite**: Binary search variants need sorted data

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Empty array
# - Single element
# - Element at start/middle/end
# - Element not present
# - Duplicate elements
# - Large datasets
# - Edge values
```

## Navigation

- **Previous**: [Program 70 - Sorting Algorithms](../70_sorting_algorithms/README.md)
- **Next**: [Program 72 - Advanced Recursion](../72_recursion_advanced/README.md)
- **Home**: [Main README](../README.md)
