# Program 89: Advanced Threading

Advanced threading concepts including thread pools, futures, and concurrent execution patterns.

## Description

This program demonstrates advanced threading techniques including ThreadPoolExecutor, concurrent.futures, thread-safe patterns, and performance optimization. Covers modern Python threading approaches.

## Learning Objectives

- Master ThreadPoolExecutor
- Understand concurrent.futures
- Learn thread pool patterns
- Practice thread-safe code
- Optimize thread performance
- Handle threading pitfalls

## Features

- **ThreadPoolExecutor**: Manage thread pools
- **Futures**: Asynchronous result handling
- **Thread Pools**: Reusable worker threads
- **Task Submission**: submit() and map() methods
- **Result Retrieval**: as_completed(), wait()
- **Exception Handling**: Propagate exceptions from threads
- **Context Managers**: Proper pool cleanup
- **Performance**: Optimal thread count

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/089_threading_advanced
python src/main.py
```

## Key Concepts

### ThreadPoolExecutor Basics

```python
from concurrent.futures import ThreadPoolExecutor

def task(n):
    return n * n

with ThreadPoolExecutor(max_workers=4) as executor:
    # Submit single task
    future = executor.submit(task, 5)
    result = future.result()

    # Submit multiple tasks
    futures = [executor.submit(task, i) for i in range(10)]

    # Map function over iterable
    results = executor.map(task, range(10))
```

### Processing Results

```python
from concurrent.futures import as_completed

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task, i) for i in range(10)]

    # Process as they complete
    for future in as_completed(futures):
        result = future.result()
        print(result)
```

### Exception Handling

```python
def task_with_error(n):
    if n == 5:
        raise ValueError("Error!")
    return n * n

with ThreadPoolExecutor() as executor:
    future = executor.submit(task_with_error, 5)
    try:
        result = future.result()  # Exception raised here
    except ValueError as e:
        print(f"Task failed: {e}")
```

### Optimal Thread Count

**I/O-bound tasks:**
- More threads = better (up to a point)
- Typical: 20-100 threads

**CPU-bound tasks:**
- Use ProcessPoolExecutor instead
- ThreadPoolExecutor limited by GIL

**Formula:**
- I/O-bound: threads = 2 * CPU_count
- CPU-bound: processes = CPU_count

### Thread Safety Patterns

```python
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.value += 1
```

## Best Practices

1. **Use ThreadPoolExecutor**: Better than raw threads
2. **Use context manager**: Ensures cleanup
3. **Set appropriate worker count**: Based on task type
4. **Handle exceptions**: Check future.result()
5. **Use as_completed**: Process results as ready
6. **Avoid shared state**: Use thread-safe structures
7. **Profile before optimizing**: Measure actual benefit
8. **Consider asyncio**: For I/O-bound tasks

## Testing

```bash
# Run tests
pytest tests/

# Performance testing
python src/main.py --benchmark

# Test scenarios
# - Task execution
# - Exception propagation
# - Thread pool shutdown
# - Concurrent modification
# - Resource cleanup
# - Performance scaling
```

## Navigation

- **Previous**: [Program 88 - HTTP Server](../088_http_server/README.md)
- **Next**: [Program 90 - Thread Synchronization](../090_thread_synchronization/README.md)
- **Home**: [Main README](../README.md)
