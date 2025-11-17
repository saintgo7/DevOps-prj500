# Program 76: Graph Traversal Algorithms

Comprehensive implementation of graph traversal techniques (DFS and BFS).

## Description

This program demonstrates graph traversal algorithms including Depth-First Search (DFS) and Breadth-First Search (BFS) with various applications. Both recursive and iterative implementations are covered.

## Learning Objectives

- Master DFS and BFS algorithms
- Understand traversal order and properties
- Learn applications of traversals
- Implement recursive and iterative versions
- Apply traversals to graph problems

## Features

- **Depth-First Search (DFS)**:
  - Recursive implementation
  - Iterative with stack
  - All paths finding
  - Cycle detection
- **Breadth-First Search (BFS)**:
  - Queue-based implementation
  - Level-order traversal
  - Shortest path (unweighted)
  - Bipartite check
- **Applications**:
  - Connected components
  - Topological sort (DFS)
  - Shortest path (BFS)
  - Cycle detection
  - Path finding

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/76_graph_traversal
python src/main.py
```

## Key Concepts

### Time Complexity

**Both DFS and BFS:**
- **Time**: O(V + E) where V = vertices, E = edges
- **Space**: O(V) for visited set and queue/stack

### Space Complexity

**DFS (Recursive):**
- O(V) for recursion stack in worst case (linear graph)
- O(h) average case where h is height

**DFS (Iterative):**
- O(V) for explicit stack

**BFS:**
- O(V) for queue (worst case all vertices in queue)

### Algorithm Characteristics

**Depth-First Search:**
- Explores as deep as possible before backtracking
- Uses stack (implicit via recursion or explicit)
- Good for: Path finding, cycle detection, topological sort
- Memory efficient for deep graphs

**Breadth-First Search:**
- Explores neighbors level by level
- Uses queue
- Good for: Shortest path, level-order, nearest neighbor
- Finds shortest path in unweighted graphs

### Applications Comparison

| Application | DFS | BFS | Best Choice |
|-------------|-----|-----|-------------|
| Shortest path (unweighted) | ❌ | ✅ | BFS |
| Path exists | ✅ | ✅ | Either |
| Connected components | ✅ | ✅ | Either |
| Cycle detection | ✅ | ✅ | DFS simpler |
| Topological sort | ✅ | ❌ | DFS |
| Bipartite check | ✅ | ✅ | BFS simpler |

## Best Practices

1. **Use visited set**: Prevent revisiting nodes
2. **Handle disconnected graphs**: Loop through all vertices
3. **Choose right traversal**: DFS for memory, BFS for shortest path
4. **Use deque for BFS**: O(1) append and pop
5. **Implement iterative DFS**: Avoid stack overflow
6. **Mark visited before adding to queue**: Prevent duplicates
7. **Consider bidirectional BFS**: For shortest path optimization

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Empty graph
# - Single vertex
# - Disconnected graph
# - Cyclic graph
# - Tree structure
# - Complete graph
# - Path finding scenarios
```

## Navigation

- **Previous**: [Program 75 - Backtracking](../75_backtracking/README.md)
- **Next**: [Program 77 - Shortest Path](../77_shortest_path/README.md)
- **Home**: [Main README](../README.md)
