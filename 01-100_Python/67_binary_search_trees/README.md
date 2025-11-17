# Program 67: Binary Search Trees (BST)

Implementation of Binary Search Tree with operations and balancing concepts.

## Description

This program demonstrates BST implementation where left subtree contains values less than root and right subtree contains values greater than root. Provides efficient searching, insertion, and deletion operations.

## Learning Objectives

- Understand BST property and invariants
- Implement BST operations efficiently
- Learn tree balancing importance
- Master successor/predecessor finding
- Compare with balanced trees (AVL, Red-Black)

## Features

- **BST Operations**: Insert, delete, search
- **Traversals**: Inorder gives sorted order
- **Min/Max**: Find minimum and maximum values
- **Successor/Predecessor**: Next/previous in order
- **Validation**: Check if tree is valid BST
- **Conversion**: Array to BST, BST to array
- **Range Queries**: Find elements in range
- **Kth Smallest/Largest**: Order statistics

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/67_binary_search_trees
python src/main.py
```

## Key Concepts

### Time Complexity

**Balanced BST:**
- **Search**: O(log n)
- **Insert**: O(log n)
- **Delete**: O(log n)
- **Min/Max**: O(log n)
- **Successor/Predecessor**: O(log n)

**Worst Case (Skewed):**
- **All operations**: O(n) - Degenerates to linked list

### Space Complexity

- **Storage**: O(n) for n nodes
- **Recursive operations**: O(h) stack space where h is height

### BST Property

For every node:
- All values in **left subtree < node value**
- All values in **right subtree > node value**
- Both subtrees are BSTs

### Operations

**Search:**
1. Compare with root
2. Go left if smaller, right if larger
3. Return when found or reach None

**Insert:**
1. Search for position
2. Insert as leaf node
3. Maintain BST property

**Delete:**
1. Find node to delete
2. Three cases:
   - Leaf: Simply remove
   - One child: Replace with child
   - Two children: Replace with inorder successor/predecessor

## Best Practices

1. **Keep tree balanced**: Use AVL or Red-Black for guaranteed O(log n)
2. **Validate BST property**: Especially after modifications
3. **Use inorder for sorted output**: Natural property
4. **Consider duplicate handling**: Allow or disallow
5. **Implement iterative search**: Avoid recursion overhead
6. **Cache tree statistics**: Size, height if needed often
7. **Use BST for ordered data**: Better than hash table for range queries

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Insert sequence (random, sorted, reverse)
# - Search existing and non-existing
# - Delete leaf, single child, two children
# - BST validation
# - Min/Max operations
# - Successor/Predecessor
```

## Navigation

- **Previous**: [Program 66 - Binary Trees](../66_binary_trees/README.md)
- **Next**: [Program 68 - Heaps](../68_heaps/README.md)
- **Home**: [Main README](../README.md)
