# Program 63: Stack Data Structure

Implementation of stack (LIFO) data structure with applications and algorithms.

## Description

This program demonstrates stack implementation using both lists and linked lists. Stacks follow Last-In-First-Out (LIFO) principle and are fundamental to many algorithms including expression evaluation, backtracking, and function calls.

## Learning Objectives

- Understand LIFO (Last-In-First-Out) principle
- Implement stack using different approaches
- Apply stacks to real-world problems
- Master stack-based algorithms
- Learn when to use stacks

## Features

- **List-based Stack**: Using Python lists
- **Linked-list Stack**: Using custom nodes
- **Core Operations**: push, pop, peek, isEmpty
- **Expression Evaluation**: Infix, prefix, postfix
- **Balanced Parentheses**: Check matching brackets
- **Function Call Stack**: Understand recursion
- **Undo/Redo**: Implement using stacks
- **Backtracking**: Maze solving, puzzles

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/63_stacks
python src/main.py
```

## Key Concepts

### Time Complexity

- **Push**: O(1) - Add to top
- **Pop**: O(1) - Remove from top
- **Peek**: O(1) - View top element
- **Search**: O(n) - Must check each element
- **isEmpty**: O(1) - Check size

### Space Complexity

- **Storage**: O(n) where n is number of elements
- **Operations**: O(1) additional space

### Common Applications

1. **Expression Evaluation**: Convert and evaluate expressions
2. **Parentheses Matching**: Validate nested brackets
3. **Function Calls**: Call stack in programming
4. **Undo/Redo**: Command pattern implementation
5. **Browser History**: Back button functionality
6. **DFS**: Depth-first search traversal
7. **Backtracking**: Solving puzzles and games

## Best Practices

1. **Check for underflow**: Don't pop from empty stack
2. **Check for overflow**: In fixed-size implementations
3. **Use clear naming**: push/pop are conventional
4. **Consider deque for better performance**: `collections.deque`
5. **Implement using list for simplicity**: For most cases
6. **Add size/capacity tracking**: Know stack state
7. **Thread safety**: Use locks for concurrent access

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Empty stack operations
# - Push/pop sequences
# - Expression evaluation
# - Parentheses matching
```

## Navigation

- **Previous**: [Program 62 - Linked Lists](../62_linked_lists/README.md)
- **Next**: [Program 64 - Queues](../64_queues/README.md)
- **Home**: [Main README](../README.md)
