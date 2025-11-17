# 20_generators

## Description

Master Python generators - functions that yield values lazily for memory-efficient iteration. Learn generator functions, generator expressions, infinite generators, generator pipelines, send() method, yield from, and practical applications for large datasets and streaming.

This is Program #20 in the 500 Programs Collection.

## Learning Objectives

- Understand lazy evaluation with generators
- Create generator functions with yield
- Use generator expressions
- Build infinite generators
- Create generator pipelines
- Use send() for bidirectional communication
- Apply yield from for delegation
- Optimize memory usage with generators
- Handle large datasets efficiently

## Features

- Basic generator functions
- yield vs return comparison
- Generator expressions
- Infinite generators
- Generator pipelines
- send() method for coroutines
- close() for cleanup
- yield from delegation
- Practical generator patterns
- Memory efficiency demonstrations

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Generator

```python
def count_up_to(n):
    """Generate numbers from 1 to n."""
    count = 1
    while count <= n:
        yield count  # Yield, not return!
        count += 1

# Create generator
gen = count_up_to(5)

# Consume
for num in gen:
    print(num)  # 1, 2, 3, 4, 5

# Or convert to list
numbers = list(count_up_to(5))
```

### 2. Yield vs Return

```python
# Regular function - returns entire list
def get_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result  # All at once

# Generator function - yields one at a time
def get_generator(n):
    for i in range(n):
        yield i ** 2  # One at a time

# Memory efficient!
gen = get_generator(1000000)  # Doesn't compute yet
first = next(gen)  # Computes only first value
```

### 3. Generator Expressions

```python
# List comprehension (eager)
squares_list = [x**2 for x in range(10)]

# Generator expression (lazy)
squares_gen = (x**2 for x in range(10))  # Note: ()

# Memory efficient for large datasets
large_gen = (x for x in range(1_000_000))
first_five = list(islice(large_gen, 5))

# Chaining generators
numbers = (x for x in range(20))
evens = (x for x in numbers if x % 2 == 0)
squares = (x ** 2 for x in evens)
```

### 4. Infinite Generators

```python
def infinite_counter(start=0):
    """Generate infinite sequence."""
    count = start
    while True:  # Infinite!
        yield count
        count += 1

def fibonacci():
    """Infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Use with islice to limit
from itertools import islice
first_ten = list(islice(fibonacci(), 10))
```

### 5. Generator Pipeline

```python
def read_data():
    """Stage 1: Generate data."""
    for i in range(1, 21):
        yield i

def filter_even(numbers):
    """Stage 2: Filter."""
    for num in numbers:
        if num % 2 == 0:
            yield num

def square(numbers):
    """Stage 3: Transform."""
    for num in numbers:
        yield num ** 2

def limit(numbers, n):
    """Stage 4: Limit."""
    for i, num in enumerate(numbers):
        if i >= n:
            break
        yield num

# Build pipeline (lazy!)
pipeline = limit(square(filter_even(read_data())), 5)
result = list(pipeline)  # [4, 16, 36, 64, 100]
```

### 6. Generator send() Method

```python
def running_average():
    """Calculate running average (coroutine)."""
    total = 0.0
    count = 0
    average = 0.0

    while True:
        value = yield average  # Receive value
        if value is not None:
            total += value
            count += 1
            average = total / count

avg = running_average()
next(avg)  # Prime the generator

avg.send(10)  # Send value, get average
avg.send(20)
avg.send(30)
```

### 7. Generator close()

```python
def managed_resource():
    """Generator with cleanup."""
    print("Opening resource")
    try:
        for i in range(5):
            yield f"Item {i}"
    finally:
        print("Closing resource")

gen = managed_resource()
next(gen)
next(gen)
gen.close()  # Triggers finally block
```

### 8. yield from (Delegation)

```python
def gen1():
    yield 1
    yield 2
    yield 3

def gen2():
    yield 4
    yield 5
    yield 6

# Without yield from
def combined_old():
    for value in gen1():
        yield value
    for value in gen2():
        yield value

# With yield from (cleaner)
def combined_new():
    yield from gen1()
    yield from gen2()
```

### 9. Practical Patterns

```python
# File processing (memory efficient)
def read_large_file(filename):
    """Process file line by line."""
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Batch processing
def batch_data(data, batch_size):
    """Split into batches."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

# Tree traversal
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def traverse(node):
    """Traverse tree lazily."""
    yield node.value
    for child in node.children:
        yield from traverse(child)
```

### 10. Memory Efficiency

```python
import sys

# List uses memory for all items
def squares_list(n):
    return [x**2 for x in range(n)]

# Generator uses minimal memory
def squares_gen(n):
    for x in range(n):
        yield x**2

n = 1000
list_obj = squares_list(n)
gen_obj = squares_gen(n)

# Check sizes
list_size = sys.getsizeof(list_obj)  # Large
gen_size = sys.getsizeof(gen_obj)    # Small
```

## Best Practices

1. **Use for Memory-Intensive Operations**
2. **Prefer Generator Expressions for Simple Cases**
3. **Build Pipelines for Data Processing**
4. **Remember Generators Are One-Time Use**
5. **Use islice() to Limit Infinite Generators**

## When to Use Generators

**DO use for:**
- Large datasets
- Streaming data
- Infinite sequences
- Pipeline processing
- Memory-constrained environments

**DON'T use when:**
- Need random access
- Need to iterate multiple times
- Dataset is small
- Need len()

## Common Patterns

```python
# Lazy file reading
def read_logs(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Infinite sequence
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Data transformation pipeline
numbers = (x for x in range(100))
evens = (x for x in numbers if x % 2 == 0)
squares = (x**2 for x in evens)
```

## Testing

```bash
python src/main.py
```

---

**Program**: 20 of 500
**Difficulty**: ⭐⭐⭐ Intermediate/Advanced
**Category**: Python Advanced
**Estimated Time**: 60-90 minutes

[← Previous (19)](../19_decorators/) | [Back to Index](../../docs/INDEX.md) | [Next (21) →](../21_context_managers/)
