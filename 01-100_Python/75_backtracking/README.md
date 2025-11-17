# Program 75: Backtracking Algorithms

Implementation of backtracking for solving constraint satisfaction and combinatorial problems.

## Description

This program demonstrates backtracking technique for exploring all possible solutions by incrementally building candidates and abandoning them (backtracking) when they fail to satisfy constraints.

## Learning Objectives

- Understand backtracking paradigm
- Learn pruning and constraint propagation
- Master recursive exploration
- Solve classic constraint problems
- Optimize backtracking with heuristics

## Features

- **Classic Problems**:
  - N-Queens problem
  - Sudoku solver
  - Knight's tour
  - Hamiltonian path
  - Graph coloring
  - Subset sum
  - Permutations and combinations
  - Word search in grid
- **Constraint Satisfaction**: CSP framework
- **Pruning**: Early termination of invalid paths
- **Optimization**: Find best solution among many

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/75_backtracking
python src/main.py
```

## Key Concepts

### Time Complexity

| Problem | Worst Case | Typical | With Pruning |
|---------|-----------|---------|--------------|
| N-Queens | O(n!) | Better with pruning | O(n^n) reduced |
| Sudoku | O(9^m) | Polynomial with constraints | Much better |
| Permutations | O(n!) | O(n!) | O(n!) |
| Combinations | O(2^n) | O(2^n) | Can be reduced |
| Graph Coloring | O(m^n) | Depends on graph | With heuristics |

### Space Complexity

- **Recursion depth**: O(d) where d is depth of search tree
- **State storage**: O(n) for current solution
- **Total**: O(d × n) for recursion stack

### Backtracking Template

```python
def backtrack(state, solutions):
    if is_solution(state):
        solutions.append(copy(state))
        return

    for choice in get_choices(state):
        if is_valid(choice, state):
            make_choice(state, choice)
            backtrack(state, solutions)
            undo_choice(state, choice)  # Backtrack
```

### Key Techniques

**Pruning:**
- Eliminate branches that cannot lead to solution
- Check constraints early
- Significantly reduces search space

**Constraint Propagation:**
- Forward checking
- Arc consistency
- Reduces available choices

**Heuristics:**
- Most constrained variable first
- Least constraining value
- Fail-fast ordering

## Best Practices

1. **Check constraints early**: Prune invalid branches quickly
2. **Use efficient data structures**: Fast constraint checking
3. **Order choices intelligently**: Use heuristics
4. **Make/undo symmetric**: Clean backtracking
5. **Limit recursion depth**: Prevent stack overflow
6. **Keep track of visited states**: Avoid cycles
7. **Consider iterative deepening**: For depth-limited search

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Small instances (verify correctness)
# - Instances with no solution
# - Multiple solutions
# - Optimal solutions
# - Performance on large instances
```

## Navigation

- **Previous**: [Program 74 - Greedy Algorithms](../74_greedy_algorithms/README.md)
- **Next**: [Program 76 - Graph Traversal](../76_graph_traversal/README.md)
- **Home**: [Main README](../README.md)
