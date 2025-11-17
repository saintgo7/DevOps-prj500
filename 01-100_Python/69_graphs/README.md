# Program 69: Graph Data Structure

Comprehensive implementation of graph data structures and basic algorithms.

## Description

This program demonstrates graph representations (adjacency matrix, adjacency list, edge list) and fundamental graph concepts. Graphs are versatile data structures modeling relationships between entities.

## Learning Objectives

- Understand graph terminology and types
- Implement graph representations
- Learn graph traversal algorithms
- Master basic graph operations
- Apply graphs to real-world problems

## Features

- **Graph Representations**:
  - Adjacency Matrix
  - Adjacency List
  - Edge List
- **Graph Types**:
  - Directed/Undirected
  - Weighted/Unweighted
  - Cyclic/Acyclic
- **Basic Operations**: Add/remove vertices and edges
- **Degree Calculation**: In-degree, out-degree
- **Connectivity**: Check if graph is connected
- **Cycle Detection**: Find cycles in graph
- **Path Finding**: Check if path exists

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/69_graphs
python src/main.py
```

## Key Concepts

### Time Complexity

**Adjacency Matrix (V vertices, E edges):**
- **Add Edge**: O(1)
- **Remove Edge**: O(1)
- **Check Edge**: O(1)
- **Get Neighbors**: O(V)
- **Space**: O(V²)

**Adjacency List:**
- **Add Edge**: O(1)
- **Remove Edge**: O(degree)
- **Check Edge**: O(degree)
- **Get Neighbors**: O(degree)
- **Space**: O(V + E)

### Space Complexity

- **Adjacency Matrix**: O(V²)
- **Adjacency List**: O(V + E)
- **Edge List**: O(E)

### Graph Terminology

- **Vertex (Node)**: Graph element
- **Edge**: Connection between vertices
- **Degree**: Number of edges connected to vertex
- **Path**: Sequence of vertices connected by edges
- **Cycle**: Path that starts and ends at same vertex
- **Connected**: Path exists between any two vertices
- **Component**: Maximal connected subgraph

### Choosing Representation

**Adjacency Matrix:**
- Dense graphs (E ≈ V²)
- Need fast edge lookup
- Have enough memory

**Adjacency List:**
- Sparse graphs (E << V²)
- Need to iterate neighbors
- Memory efficient

## Best Practices

1. **Use adjacency list for sparse graphs**: Most real-world graphs
2. **Use dict for adjacency list in Python**: Flexible and efficient
3. **Consider networkx library**: Rich graph algorithms
4. **Store edge weights**: For weighted graphs
5. **Use sets for undirected graphs**: Prevent duplicate edges
6. **Implement __str__ for visualization**: Aid debugging
7. **Validate input**: Check for self-loops, duplicates

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Empty graph
# - Single vertex
# - Add/remove operations
# - Directed vs undirected
# - Cycle detection
# - Connectivity check
# - Various graph topologies
```

## Navigation

- **Previous**: [Program 68 - Heaps](../68_heaps/README.md)
- **Next**: [Program 70 - Sorting Algorithms](../70_sorting_algorithms/README.md)
- **Home**: [Main README](../README.md)
