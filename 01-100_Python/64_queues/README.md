# Program 64: Queue Data Structure

Implementation of queue (FIFO) and related data structures including priority queues and deques.

## Description

This program demonstrates queue implementations following First-In-First-Out (FIFO) principle. Includes standard queues, circular queues, priority queues, and double-ended queues (deques).

## Learning Objectives

- Understand FIFO (First-In-First-Out) principle
- Implement various queue types
- Learn queue applications
- Master queue-based algorithms
- Compare queue implementations

## Features

- **Standard Queue**: Basic FIFO operations
- **Circular Queue**: Efficient fixed-size queue
- **Priority Queue**: Elements ordered by priority
- **Deque**: Double-ended queue (both ends)
- **Queue using Stacks**: Implementing queue with stacks
- **BFS Implementation**: Breadth-first search
- **Task Scheduling**: Job queue simulation
- **Producer-Consumer**: Multi-threading pattern

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/64_queues
python src/main.py
```

## Key Concepts

### Time Complexity

**Standard Queue:**
- **Enqueue**: O(1) - Add to rear
- **Dequeue**: O(1) - Remove from front
- **Peek**: O(1) - View front element
- **Search**: O(n) - Must check each element

**Priority Queue (Heap-based):**
- **Insert**: O(log n) - Maintain heap property
- **Extract Min/Max**: O(log n) - Remove and re-heapify
- **Peek**: O(1) - View top element

**Deque:**
- **Add/Remove Front**: O(1)
- **Add/Remove Rear**: O(1)

### Space Complexity

- **Storage**: O(n) for n elements
- **Circular Queue**: O(k) for fixed capacity k

### Common Applications

1. **BFS Traversal**: Level-order tree/graph traversal
2. **Task Scheduling**: Job queues, process scheduling
3. **Buffer Management**: IO buffers, print spooling
4. **Handling Requests**: Web servers, API rate limiting
5. **Cache Implementation**: LRU cache using queue
6. **Producer-Consumer**: Multi-threading coordination

## Best Practices

1. **Use collections.deque**: Optimized for queue operations
2. **Use queue.Queue for threading**: Thread-safe implementation
3. **Use heapq for priority queue**: Built-in heap implementation
4. **Check for empty before dequeue**: Prevent errors
5. **Consider circular buffer**: For fixed-size needs
6. **Add capacity limits**: Prevent unbounded growth
7. **Monitor queue size**: Detect bottlenecks

## Testing

```bash
# Run tests
pytest tests/

# Test scenarios
# - Enqueue/dequeue sequences
# - Empty queue handling
# - Priority ordering
# - Circular queue wraparound
# - Concurrent access
```

## Navigation

- **Previous**: [Program 63 - Stacks](../63_stacks/README.md)
- **Next**: [Program 65 - Hash Tables](../65_hash_tables/README.md)
- **Home**: [Main README](../README.md)
