# Program 72: Advanced Recursion

Deep dive into recursive problem-solving with optimization techniques.

## Description

This program explores advanced recursion concepts including tail recursion, memoization, recursive backtracking, and converting recursion to iteration. Covers complex recursive problems and optimization strategies.

## Learning Objectives

- Master recursive thinking and problem decomposition
- Understand recursion tree and call stack
- Learn memoization and dynamic programming
- Practice tail recursion optimization
- Convert between recursive and iterative solutions

## Features

- **Recursion Fundamentals**: Base case, recursive case
- **Tail Recursion**: Last operation is recursive call
- **Memoization**: Cache results to avoid recomputation
- **Backtracking**: Explore all possibilities
- **Tree Recursion**: Multiple recursive calls
- **Mutual Recursion**: Functions calling each other
- **Recursion to Iteration**: Using stacks
- **Complex Problems**: Tower of Hanoi, N-Queens, permutations

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/72_recursion_advanced
python src/main.py
```

## Key Concepts

### Time Complexity

**Without Memoization:**
- **Fibonacci**: O(2^n) - Exponential
- **Factorial**: O(n) - Linear
- **Tower of Hanoi**: O(2^n) - Exponential

**With Memoization:**
- **Fibonacci**: O(n) - Each subproblem solved once
- **Many DP problems**: O(n) to O(n²)

### Space Complexity

- **Recursion depth**: O(d) where d is maximum depth
- **Memoization**: O(n) for cache storage
- **Tail recursion (optimized)**: O(1) - Reuses stack frame

### Recursion Patterns

**Direct Recursion:**
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

**Tail Recursion:**
```python
def factorial_tail(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)
```

**Memoization:**
```python
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Best Practices

1. **Always define base case**: Prevent infinite recursion
2. **Use memoization for overlapping subproblems**: Massive speedup
3. **Consider iterative alternative**: For simple recursions
4. **Use lru_cache decorator**: Built-in memoization
5. **Limit recursion depth**: Python has default limit (usually 1000)
6. **Use tail recursion when possible**: Some languages optimize this
7. **Draw recursion tree**: Visualize problem decomposition

## Testing

```bash
# Run tests
pytest tests/

# Test with different inputs
# - Base cases
# - Small values
# - Large values (check stack depth)
# - Edge cases

# Increase recursion limit if needed
# sys.setrecursionlimit(10000)
```

## Navigation

- **Previous**: [Program 71 - Searching Algorithms](../71_searching_algorithms/README.md)
- **Next**: [Program 73 - Dynamic Programming](../73_dynamic_programming/README.md)
- **Home**: [Main README](../README.md)
