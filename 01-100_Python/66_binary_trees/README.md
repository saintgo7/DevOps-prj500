# Program 66: Binary Trees

Implementation of binary tree data structure with traversal algorithms and operations.

## Description

This program demonstrates binary tree implementation including node structure, tree construction, various traversal methods (inorder, preorder, postorder, level-order), and common tree operations.

## Learning Objectives

- Understand tree terminology and properties
- Implement binary tree structure
- Master tree traversal algorithms
- Learn recursive and iterative approaches
- Apply trees to problem-solving

## Features

- **Tree Construction**: Build trees from arrays, lists
- **Traversals**:
  - Inorder (Left-Root-Right)
  - Preorder (Root-Left-Right)
  - Postorder (Left-Right-Root)
  - Level-order (BFS)
- **Tree Properties**: Height, depth, size, balanced check
- **Path Operations**: Root-to-leaf paths, path sum
- **Tree Modification**: Insert, delete nodes
- **Views**: Left view, right view, top view
- **Serialization**: Convert tree to/from string

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/66_binary_trees
python src/main.py
```

## Key Concepts

### Time Complexity

**Traversals:**
- **All traversals**: O(n) - Visit each node once

**Operations:**
- **Search**: O(n) - May need to check all nodes
- **Insert**: O(n) - Find position
- **Height**: O(n) - Check all paths
- **Balanced check**: O(n) - Check all nodes

### Space Complexity

**Storage:**
- **Nodes**: O(n) for n nodes

**Traversal:**
- **Recursive**: O(h) stack space (h = height)
- **Iterative**: O(h) for queue/stack
- **Level-order**: O(w) where w is max width

### Tree Properties

- **Height**: Longest path from root to leaf
- **Depth**: Distance from root to node
- **Level**: Depth + 1
- **Complete**: All levels filled except possibly last
- **Perfect**: All levels completely filled
- **Balanced**: Height difference ≤ 1 for all nodes

## Best Practices

1. **Use recursion for traversals**: Natural and clean
2. **Check for None/null**: Prevent errors
3. **Use queue for level-order**: BFS pattern
4. **Draw tree diagrams**: Visualize structure
5. **Test with balanced and skewed trees**
6. **Consider iterative for large trees**: Avoid stack overflow
7. **Use parent pointers when needed**: For upward traversal

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Empty tree
# - Single node
# - Balanced tree
# - Skewed tree (left/right)
# - All traversal orders
# - Edge cases
```

## Navigation

- **Previous**: [Program 65 - Hash Tables](../65_hash_tables/README.md)
- **Next**: [Program 67 - Binary Search Trees](../67_binary_search_trees/README.md)
- **Home**: [Main README](../README.md)
