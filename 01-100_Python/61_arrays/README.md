# Program 61: Array Operations

Comprehensive implementation of array data structure and operations in Python.

## Description

This program demonstrates array operations using Python lists, including element access, insertion, deletion, searching, and manipulation. Arrays are fundamental data structures that store elements in contiguous memory locations.

## Learning Objectives

- Understand array data structure fundamentals
- Master array indexing and slicing
- Learn time complexity of array operations
- Implement common array algorithms
- Practice array manipulation techniques

## Features

- **Element Access**: O(1) time complexity for index-based access
- **Array Creation**: Multiple initialization methods
- **Insertion/Deletion**: Add and remove elements
- **Searching**: Linear and binary search implementations
- **Sorting**: Various sorting algorithms
- **Array Manipulation**: Reverse, rotate, and transform arrays
- **Multi-dimensional Arrays**: 2D and 3D array operations

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/61_arrays
python src/main.py
```

## Key Concepts

### Time Complexity

- **Access**: O(1) - Direct index access
- **Search**: O(n) - Linear search (unsorted)
- **Search**: O(log n) - Binary search (sorted)
- **Insertion**: O(n) - May require shifting elements
- **Deletion**: O(n) - May require shifting elements
- **Append**: O(1) amortized - Add to end

### Space Complexity

- **Storage**: O(n) where n is number of elements
- **Most operations**: O(1) additional space

## Best Practices

1. **Use appropriate data structure**: Lists for dynamic arrays, array module for fixed types
2. **Pre-allocate size when known**: Improves performance
3. **Use list comprehensions**: More Pythonic and often faster
4. **Avoid repeated indexing**: Cache values in loops
5. **Consider numpy for numerical operations**: Much faster for large arrays
6. **Use generators for large data**: Saves memory
7. **Leverage built-in functions**: `sum()`, `min()`, `max()` are optimized

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Navigation

- **Previous**: [Program 60 - Modules](../60_modules/README.md)
- **Next**: [Program 62 - Linked Lists](../62_linked_lists/README.md)
- **Home**: [Main README](../README.md)
