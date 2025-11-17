# Program 74: Greedy Algorithms

Implementation of greedy algorithm patterns and classic problems.

## Description

This program demonstrates greedy algorithms that make locally optimal choices at each step. Covers activity selection, Huffman coding, minimum spanning trees, and other optimization problems solvable by greedy approach.

## Learning Objectives

- Understand greedy choice property
- Learn when greedy approach works
- Prove correctness of greedy algorithms
- Compare greedy vs dynamic programming
- Apply greedy to optimization problems

## Features

- **Classic Problems**:
  - Activity selection
  - Fractional knapsack
  - Huffman coding
  - Job sequencing
  - Minimum spanning tree (Kruskal's, Prim's)
  - Dijkstra's shortest path
  - Coin change (greedy version)
- **Interval Scheduling**: Maximize non-overlapping activities
- **Graph Algorithms**: MST, shortest path
- **Optimization**: Task scheduling, resource allocation

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/74_greedy_algorithms
python src/main.py
```

## Key Concepts

### Time Complexity

| Problem | Time | Space | Approach |
|---------|------|-------|----------|
| Activity Selection | O(n log n) | O(1) | Sort by end time |
| Fractional Knapsack | O(n log n) | O(1) | Sort by value/weight |
| Huffman Coding | O(n log n) | O(n) | Priority queue |
| Kruskal's MST | O(E log E) | O(V) | Sort edges |
| Prim's MST | O(E log V) | O(V) | Priority queue |
| Dijkstra's | O((V+E) log V) | O(V) | Priority queue |

### Greedy Choice Property

An algorithm has the greedy choice property if:
- A globally optimal solution can be arrived at by making locally optimal (greedy) choices
- The choice made at each step is never reconsidered

### When Greedy Works

Greedy algorithms work when problem has:
1. **Greedy choice property**: Local optimum leads to global optimum
2. **Optimal substructure**: Optimal solution contains optimal subsolutions

### Greedy vs Dynamic Programming

**Use Greedy when:**
- Greedy choice property holds
- Simpler and more efficient
- Examples: MST, Dijkstra's

**Use DP when:**
- Need to consider all possibilities
- Overlapping subproblems
- Examples: 0/1 knapsack, LCS

## Best Practices

1. **Prove correctness**: Greedy doesn't always work
2. **Sort data first**: Many greedy algorithms need sorted input
3. **Use priority queue**: For maintaining greedy choice
4. **Consider exchange argument**: Prove greedy stays ahead
5. **Check problem constraints**: Ensure greedy applies
6. **Test counterexamples**: Verify algorithm correctness
7. **Document greedy choice**: Make strategy clear

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Small examples (manual verification)
# - Edge cases (empty, single element)
# - Cases where greedy fails (for comparison)
# - Large inputs (performance)
# - Known optimal solutions
```

## Navigation

- **Previous**: [Program 73 - Dynamic Programming](../73_dynamic_programming/README.md)
- **Next**: [Program 75 - Backtracking](../75_backtracking/README.md)
- **Home**: [Main README](../README.md)
