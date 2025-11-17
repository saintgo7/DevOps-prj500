# Program 77: Shortest Path Algorithms

Implementation of shortest path algorithms for weighted and unweighted graphs.

## Description

This program demonstrates shortest path algorithms including Dijkstra's algorithm, Bellman-Ford algorithm, Floyd-Warshall algorithm, and A* search. Covers both single-source and all-pairs shortest path problems.

## Learning Objectives

- Master shortest path algorithms
- Understand algorithm trade-offs
- Handle negative weights
- Learn all-pairs shortest path
- Apply heuristic search (A*)

## Features

- **Dijkstra's Algorithm**: Single-source, non-negative weights
- **Bellman-Ford**: Single-source, handles negative weights
- **Floyd-Warshall**: All-pairs shortest path
- **A* Search**: Heuristic-guided search
- **BFS**: Unweighted shortest path
- **Applications**:
  - GPS navigation
  - Network routing
  - Game pathfinding
  - Flight connections

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/77_shortest_path
python src/main.py
```

## Key Concepts

### Time Complexity

| Algorithm | Time | Space | Negative Weights | All-Pairs |
|-----------|------|-------|------------------|-----------|
| BFS | O(V+E) | O(V) | No | No |
| Dijkstra (heap) | O((V+E) log V) | O(V) | No | No |
| Dijkstra (array) | O(V²) | O(V) | No | No |
| Bellman-Ford | O(VE) | O(V) | Yes | No |
| Floyd-Warshall | O(V³) | O(V²) | Yes | Yes |
| A* | O(E) | O(V) | No | No |

### Algorithm Characteristics

**Dijkstra's Algorithm:**
- Greedy approach
- Uses priority queue
- Guarantees shortest path for non-negative weights
- Cannot handle negative weights
- Efficient for sparse graphs

**Bellman-Ford:**
- Dynamic programming approach
- Detects negative cycles
- Handles negative weights
- Slower than Dijkstra
- Simple implementation

**Floyd-Warshall:**
- Dynamic programming
- Finds shortest paths between all pairs
- Simple implementation
- Works with negative weights (no negative cycles)
- O(V³) makes it impractical for large graphs

**A* Search:**
- Heuristic-guided
- Optimal if heuristic is admissible
- Faster than Dijkstra with good heuristic
- Used in games and navigation

### Dijkstra's Algorithm Steps

1. Initialize distances to infinity (except source = 0)
2. Add source to priority queue
3. While queue not empty:
   - Extract node with minimum distance
   - For each neighbor, try to relax edge
   - Update distance if shorter path found
   - Add to queue if distance updated

## Best Practices

1. **Use Dijkstra for non-negative weights**: Optimal choice
2. **Implement with min-heap**: O((V+E) log V) performance
3. **Use Bellman-Ford for negative weights**: Only when necessary
4. **Use Floyd-Warshall for small dense graphs**: All-pairs
5. **Use A* for grid-based problems**: With good heuristic
6. **Reconstruct path**: Keep track of predecessors
7. **Check for negative cycles**: Important for correctness

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Simple paths
# - Multiple paths (verify shortest)
# - Disconnected nodes
# - Negative weights
# - Negative cycles
# - Large graphs (performance)
# - Compare algorithm results
```

## Navigation

- **Previous**: [Program 76 - Graph Traversal](../76_graph_traversal/README.md)
- **Next**: [Program 78 - Tree Traversal](../78_tree_traversal/README.md)
- **Home**: [Main README](../README.md)
