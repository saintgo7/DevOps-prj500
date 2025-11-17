# Program 65: Hash Tables

Comprehensive implementation of hash tables with collision resolution strategies.

## Description

This program demonstrates hash table (hash map) implementation with various hashing functions and collision resolution techniques. Hash tables provide O(1) average-case lookup, insert, and delete operations.

## Learning Objectives

- Understand hashing principles
- Implement hash functions
- Master collision resolution techniques
- Learn load factor and resizing
- Apply hash tables to problems

## Features

- **Hash Functions**: Division, multiplication, universal hashing
- **Collision Resolution**:
  - Chaining (linked lists)
  - Open addressing (linear, quadratic, double hashing)
- **Dynamic Resizing**: Maintain load factor
- **Python dict Implementation**: Understanding internals
- **HashSet**: Set operations using hashing
- **Caching**: LRU cache implementation
- **Applications**: Word frequency, anagrams, duplicates

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/65_hash_tables
python src/main.py
```

## Key Concepts

### Time Complexity

**Average Case:**
- **Insert**: O(1)
- **Delete**: O(1)
- **Search**: O(1)

**Worst Case (many collisions):**
- **Insert**: O(n)
- **Delete**: O(n)
- **Search**: O(n)

### Space Complexity

- **Storage**: O(n) for n key-value pairs
- **Chaining**: O(n + m) where m is table size
- **Load Factor**: α = n/m (keep < 0.7 for performance)

### Hash Function Properties

1. **Deterministic**: Same input → same output
2. **Uniform Distribution**: Minimize collisions
3. **Fast Computation**: O(1) time
4. **Avalanche Effect**: Small change → different hash

### Collision Resolution

**Chaining:**
- Each bucket contains linked list
- Simple to implement
- Can exceed load factor
- Better for high load factors

**Open Addressing:**
- All elements in table
- Better cache performance
- Requires good probing
- Performance degrades at high load factors

## Best Practices

1. **Use Python dict for most cases**: Highly optimized
2. **Choose good hash function**: Minimize collisions
3. **Monitor load factor**: Resize when > 0.7
4. **Use immutable keys**: Prevent hash changes
5. **Implement __hash__ and __eq__**: For custom objects
6. **Consider OrderedDict**: When order matters
7. **Use defaultdict**: For counting/grouping

## Testing

```bash
# Run tests
pytest tests/

# Test cases
# - Basic operations
# - Collision handling
# - Resizing behavior
# - Custom hash functions
# - Edge cases (empty, single element)
```

## Navigation

- **Previous**: [Program 64 - Queues](../64_queues/README.md)
- **Next**: [Program 66 - Binary Trees](../66_binary_trees/README.md)
- **Home**: [Main README](../README.md)
