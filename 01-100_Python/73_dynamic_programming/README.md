# Program 73: Dynamic Programming

Comprehensive coverage of dynamic programming patterns and problems.

## Description

This program demonstrates dynamic programming (DP) techniques for solving optimization problems. Covers both top-down (memoization) and bottom-up (tabulation) approaches with classic DP problems.

## Learning Objectives

- Understand optimal substructure and overlapping subproblems
- Master memoization vs tabulation approaches
- Identify DP problem patterns
- Learn state transition and recurrence relations
- Optimize space complexity in DP solutions

## Features

- **Classic Problems**:
  - Fibonacci sequence
  - Longest Common Subsequence (LCS)
  - Longest Increasing Subsequence (LIS)
  - 0/1 Knapsack problem
  - Coin change problem
  - Edit distance (Levenshtein)
  - Matrix chain multiplication
- **Approaches**: Top-down (memoization), Bottom-up (tabulation)
- **Space Optimization**: Reduce from O(n²) to O(n)
- **Path Reconstruction**: Trace back solution

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/73_dynamic_programming
python src/main.py
```

## Key Concepts

### Time Complexity

| Problem | Naive | DP | Space |
|---------|-------|-----|-------|
| Fibonacci | O(2^n) | O(n) | O(n) |
| LCS | O(2^n) | O(m×n) | O(m×n) |
| LIS | O(2^n) | O(n²) or O(n log n) | O(n) |
| Knapsack | O(2^n) | O(n×W) | O(n×W) |
| Coin Change | O(S^n) | O(n×S) | O(S) |
| Edit Distance | O(3^n) | O(m×n) | O(m×n) |

### DP Requirements

1. **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
2. **Overlapping Subproblems**: Same subproblems solved multiple times

### Approaches

**Top-Down (Memoization):**
- Start with original problem
- Recursively break down
- Cache results
- More intuitive
- Uses recursion stack

**Bottom-Up (Tabulation):**
- Start with smallest subproblems
- Build up to original problem
- Fill DP table
- Better space efficiency
- No recursion overhead

### DP Patterns

1. **Linear DP**: 1D array (Fibonacci, climbing stairs)
2. **2D DP**: 2D table (LCS, edit distance)
3. **Knapsack Pattern**: Include/exclude decisions
4. **Interval DP**: Process subarrays
5. **Tree DP**: DP on trees
6. **Digit DP**: Problems on digits

## Best Practices

1. **Identify the state**: What parameters define subproblem?
2. **Define recurrence relation**: How to compute state from smaller states?
3. **Determine base cases**: Smallest subproblems
4. **Decide on approach**: Top-down vs bottom-up
5. **Optimize space**: Often can reduce dimensions
6. **Reconstruct solution**: Keep track of decisions made
7. **Test with examples**: Verify recurrence is correct

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Small inputs (manually verify)
# - Known solutions
# - Edge cases (empty, single element)
# - Large inputs (performance)
# - Compare naive vs DP results
```

## Navigation

- **Previous**: [Program 72 - Advanced Recursion](../72_recursion_advanced/README.md)
- **Next**: [Program 74 - Greedy Algorithms](../74_greedy_algorithms/README.md)
- **Home**: [Main README](../README.md)
