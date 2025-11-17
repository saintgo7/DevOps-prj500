# Program 79: Algorithm Complexity Analysis

Comprehensive guide to analyzing time and space complexity of algorithms.

## Description

This program teaches Big O notation, complexity analysis techniques, and demonstrates how to analyze various algorithms. Includes practical examples of complexity measurement and optimization strategies.

## Learning Objectives

- Master Big O notation
- Analyze time complexity of algorithms
- Understand space complexity
- Learn amortized analysis
- Practice complexity proofs
- Identify optimization opportunities

## Features

- **Big O Notation**: O(1), O(log n), O(n), O(n log n), O(n²), O(2^n)
- **Time Complexity Analysis**: Loop analysis, recursion
- **Space Complexity**: Memory usage analysis
- **Recurrence Relations**: Master theorem, substitution
- **Amortized Analysis**: Average cost over sequence
- **Best/Average/Worst Case**: Different scenarios
- **Practical Examples**: Real algorithm analysis
- **Optimization Techniques**: Improve complexity

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/79_complexity_analysis
python src/main.py
```

## Key Concepts

### Big O Notation

Describes upper bound on growth rate:

**Constant - O(1):**
- Array access: arr[i]
- Hash table lookup (average)
- Push/pop on stack

**Logarithmic - O(log n):**
- Binary search
- Balanced tree operations
- Finding power of number

**Linear - O(n):**
- Array traversal
- Linear search
- Finding min/max

**Linearithmic - O(n log n):**
- Merge sort
- Quick sort (average)
- Heap sort

**Quadratic - O(n²):**
- Bubble sort
- Nested loops
- Insertion sort

**Exponential - O(2^n):**
- Fibonacci (naive)
- Subset generation
- Backtracking (worst case)

**Factorial - O(n!):**
- Permutations
- Traveling salesman (brute force)

### Analyzing Loops

```python
# O(n) - single loop
for i in range(n):
    # O(1) operation

# O(n²) - nested loops
for i in range(n):
    for j in range(n):
        # O(1) operation

# O(n log n) - loop with division
for i in range(n):
    j = i
    while j > 0:
        j = j // 2  # O(log n)
```

### Analyzing Recursion

Use recurrence relations:

**T(n) = T(n-1) + O(1)** → O(n) - Linear recursion

**T(n) = T(n-1) + T(n-2) + O(1)** → O(2^n) - Fibonacci

**T(n) = 2T(n/2) + O(n)** → O(n log n) - Merge sort

### Space Complexity

- **Auxiliary space**: Extra space used by algorithm
- **Total space**: Input + auxiliary space
- Consider: variables, data structures, recursion stack

### Amortized Analysis

Average cost per operation over sequence:
- **Dynamic array**: O(1) amortized append
- **Disjoint set union**: O(α(n)) amortized

## Best Practices

1. **Focus on worst case**: Usually most important
2. **Drop constants**: O(2n) = O(n)
3. **Drop lower terms**: O(n² + n) = O(n²)
4. **Consider both time and space**: Trade-offs
5. **Use recurrence relations**: For recursive algorithms
6. **Benchmark real performance**: Big O is asymptotic
7. **Optimize the bottleneck**: Focus on highest complexity

## Testing

```bash
# Run tests
pytest tests/

# Benchmark different implementations
python src/main.py --benchmark

# Compare complexity classes
# - Measure actual runtime
# - Plot growth curves
# - Verify theoretical analysis
```

## Navigation

- **Previous**: [Program 78 - Tree Traversal](../78_tree_traversal/README.md)
- **Next**: [Program 80 - Problem Solving](../80_problem_solving/README.md)
- **Home**: [Main README](../README.md)
