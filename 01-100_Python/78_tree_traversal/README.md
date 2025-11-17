# Program 78: Tree Traversal Algorithms

Comprehensive coverage of tree traversal techniques and algorithms.

## Description

This program demonstrates all tree traversal methods including depth-first (inorder, preorder, postorder) and breadth-first (level-order) traversals. Covers both recursive and iterative implementations with applications.

## Learning Objectives

- Master all tree traversal orders
- Implement recursive and iterative versions
- Understand traversal properties
- Apply traversals to tree problems
- Learn Morris traversal for O(1) space

## Features

- **Depth-First Traversals**:
  - Inorder (Left-Root-Right)
  - Preorder (Root-Left-Right)
  - Postorder (Left-Right-Root)
- **Breadth-First Traversal**:
  - Level-order (top to bottom)
  - Zigzag level-order
  - Vertical order
- **Implementations**:
  - Recursive (all traversals)
  - Iterative using stack (DFS)
  - Iterative using queue (BFS)
  - Morris traversal (O(1) space)
- **Applications**:
  - Expression tree evaluation
  - Serialization/deserialization
  - Tree views (left, right, top, bottom)

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/78_tree_traversal
python src/main.py
```

## Key Concepts

### Time Complexity

All traversals visit each node exactly once:
- **Time**: O(n) for n nodes
- **Space (recursive)**: O(h) where h is tree height
- **Space (iterative)**: O(h) for stack/queue
- **Space (Morris)**: O(1) - no extra data structure

### Traversal Orders

**Inorder (Left-Root-Right):**
- For BST: Visits nodes in sorted order
- Use cases: Get sorted values from BST

**Preorder (Root-Left-Right):**
- Root visited before children
- Use cases: Copy tree, prefix expression

**Postorder (Left-Right-Root):**
- Root visited after children
- Use cases: Delete tree, postfix expression, tree height

**Level-order (BFS):**
- Visit nodes level by level
- Use cases: Level-based problems, shortest path in unweighted tree

### Traversal Characteristics

| Traversal | Order | Stack Needed | Queue Needed | Applications |
|-----------|-------|--------------|--------------|--------------|
| Inorder | L-Root-R | Yes (implicit/explicit) | No | BST sorted order |
| Preorder | Root-L-R | Yes | No | Copy tree, serialize |
| Postorder | L-R-Root | Yes | No | Delete tree, calculate |
| Level-order | Top-bottom | No | Yes | Level problems |

### Morris Traversal

Space-optimized traversal using threaded binary trees:
- Creates temporary links to successor
- Restores tree structure
- O(1) space complexity
- O(n) time with constant factor increase

## Best Practices

1. **Use recursion for simplicity**: Natural for trees
2. **Implement iterative for production**: Avoid stack overflow
3. **Choose traversal based on problem**: Each has specific uses
4. **Use level-order for level-based problems**: BFS pattern
5. **Consider Morris for memory-constrained**: O(1) space
6. **Check for null nodes**: Prevent null pointer errors
7. **Test with various tree shapes**: Balanced, skewed, complete

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Empty tree
# - Single node
# - Balanced tree
# - Skewed tree (left and right)
# - Complete binary tree
# - Verify traversal order
# - Compare recursive vs iterative
```

## Navigation

- **Previous**: [Program 77 - Shortest Path](../77_shortest_path/README.md)
- **Next**: [Program 79 - Complexity Analysis](../79_complexity_analysis/README.md)
- **Home**: [Main README](../README.md)
