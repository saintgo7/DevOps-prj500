# Program 62: Linked Lists

Implementation of singly and doubly linked list data structures with comprehensive operations.

## Description

This program demonstrates linked list implementations including singly linked lists, doubly linked lists, and circular linked lists. Linked lists are dynamic data structures that store elements in nodes connected by pointers.

## Learning Objectives

- Understand linked list structure and types
- Implement node-based data structures
- Master pointer manipulation
- Learn trade-offs vs arrays
- Practice linked list algorithms

## Features

- **Singly Linked List**: Nodes with single forward pointer
- **Doubly Linked List**: Nodes with forward and backward pointers
- **Circular Linked List**: Last node points to first
- **Basic Operations**: Insert, delete, search, traverse
- **Advanced Operations**: Reverse, detect cycles, merge lists
- **Middle Element**: Find middle in single pass
- **Cycle Detection**: Floyd's cycle-finding algorithm

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/62_linked_lists
python src/main.py
```

## Key Concepts

### Time Complexity

- **Access**: O(n) - Must traverse from head
- **Search**: O(n) - Linear traversal
- **Insertion at head**: O(1) - Direct pointer update
- **Insertion at tail**: O(n) for singly, O(1) for doubly (with tail pointer)
- **Deletion at head**: O(1) - Update head pointer
- **Deletion (known node)**: O(1) for doubly, O(n) for singly

### Space Complexity

- **Storage**: O(n) - n nodes plus pointers
- **Extra space per node**: O(1) for singly, O(1) for doubly (2 pointers)

### Advantages over Arrays

- Dynamic size (no pre-allocation)
- Efficient insertion/deletion at beginning
- No wasted memory from pre-allocation

### Disadvantages vs Arrays

- No random access (must traverse)
- Extra memory for pointers
- Poor cache locality

## Best Practices

1. **Always check for None**: Prevent null pointer errors
2. **Use dummy head node**: Simplifies edge cases
3. **Update pointers carefully**: Draw diagrams for complex operations
4. **Clean up nodes**: Set pointers to None to help garbage collection
5. **Consider doubly linked for bidirectional traversal**
6. **Use tail pointer for O(1) append operations**
7. **Implement __str__ for debugging**

## Testing

```bash
# Run tests
pytest tests/

# Test edge cases
# - Empty list
# - Single element
# - Operations at head/tail/middle
```

## Navigation

- **Previous**: [Program 61 - Arrays](../61_arrays/README.md)
- **Next**: [Program 63 - Stacks](../63_stacks/README.md)
- **Home**: [Main README](../README.md)
