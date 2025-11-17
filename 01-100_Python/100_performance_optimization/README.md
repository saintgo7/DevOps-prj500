# Program 100: Performance Optimization

Comprehensive guide to profiling, benchmarking, and optimizing Python code.

## Description

This program demonstrates performance optimization techniques including profiling, benchmarking, algorithm optimization, memory management, and Python-specific optimizations. The final program completing the 100 Python programs series!

## Learning Objectives

- Master profiling tools
- Benchmark code effectively
- Optimize algorithms
- Improve memory usage
- Use Python optimization techniques
- Understand performance trade-offs

## Features

- **Profiling**: cProfile, line_profiler, memory_profiler
- **Benchmarking**: timeit, performance measurement
- **Algorithm Optimization**: Time complexity improvements
- **Caching**: @lru_cache, custom caches
- **Generators**: Memory-efficient iteration
- **String Optimization**: join vs concatenation
- **Loop Optimization**: List comprehensions, built-ins
- **Data Structure Choice**: List vs set vs dict

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/100_performance_optimization
python src/main.py --benchmark
```

## Key Concepts

### Profiling

```python
import cProfile
import pstats

# Profile code
profiler = cProfile.Profile()
profiler.enable()

# Code to profile
slow_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Benchmarking

```python
import timeit

# Benchmark function
time = timeit.timeit(
    'sum(range(1000))',
    number=10000
)

# Compare implementations
time1 = timeit.timeit(lambda: method1(), number=1000)
time2 = timeit.timeit(lambda: method2(), number=1000)
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # Cached after first call
    return compute(n)

# Check cache stats
expensive_function.cache_info()
```

### Generators vs Lists

```python
# List - all in memory
def create_list(n):
    return [i * i for i in range(n)]

# Generator - one at a time
def create_generator(n):
    for i in range(n):
        yield i * i

# Memory efficient
for value in create_generator(1000000):
    process(value)
```

### String Optimization

```python
# Slow - creates many strings
result = ''
for s in strings:
    result += s

# Fast - single operation
result = ''.join(strings)

# F-strings fastest for formatting
name, age = "Alice", 30
s = f"Name: {name}, Age: {age}"
```

### Loop Optimization

```python
# Slow - repeated lookups
result = []
for i in data:
    result.append(i * 2)

# Fast - list comprehension
result = [i * 2 for i in data]

# Faster - built-in functions
result = list(map(lambda x: x * 2, data))

# Fastest for sum
total = sum(data)  # Don't write manual loop
```

### Data Structure Choice

```python
# List - O(n) membership test
if item in my_list:
    pass

# Set - O(1) membership test
if item in my_set:
    pass

# Use right structure for operation
data = list(range(10000))
data_set = set(data)

# Slow: O(n) for each lookup
for item in search_items:
    if item in data:
        found.append(item)

# Fast: O(1) for each lookup
for item in search_items:
    if item in data_set:
        found.append(item)
```

## Best Practices

1. **Profile before optimizing**: Find real bottlenecks
2. **Use right algorithm**: O(n log n) vs O(n²)
3. **Cache expensive operations**: Memoization
4. **Use generators**: For large data
5. **Leverage built-ins**: They're optimized C code
6. **Choose right data structure**: Set for membership
7. **Minimize function calls**: In hot loops
8. **Use local variables**: Faster than global

## Testing

```bash
# Run tests
pytest tests/

# Profile script
python -m cProfile -o profile.stats src/main.py
python -m pstats profile.stats

# Benchmark
python src/main.py --benchmark

# Memory profiling
python -m memory_profiler src/main.py

# Test scenarios
# - Compare naive vs optimized
# - Memory usage comparison
# - Scaling with input size
# - Cache effectiveness
```

## Congratulations!

You've completed all 100 Python programs! This comprehensive journey covered:

1-20: **Fundamentals** - Basics to control flow
21-40: **Data Structures** - Strings to comprehensions
41-60: **Functions & Modules** - Functions to packaging
61-80: **Algorithms** - Data structures to problem solving
81-100: **System Programming** - Files to optimization

## Navigation

- **Previous**: [Program 99 - Deployment](../099_deployment/README.md)
- **Home**: [Main README](../README.md)
- **Start Again**: [Program 01 - Hello World](../01_hello_world/README.md)
