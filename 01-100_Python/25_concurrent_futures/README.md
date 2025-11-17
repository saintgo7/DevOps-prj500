# Program 25: Concurrent Futures

High-level interface for concurrent execution with ThreadPoolExecutor and ProcessPoolExecutor.

## Learning Objectives

- Master ThreadPoolExecutor and ProcessPoolExecutor
- Use submit(), map(), and as_completed()
- Handle Future objects and their methods
- Implement callbacks and exception handling
- Understand wait() with different completion strategies

## Features

- ThreadPoolExecutor for I/O-bound tasks
- ProcessPoolExecutor for CPU-bound tasks
- Future objects with done(), running(), result(), cancel()
- as_completed() for processing results as they finish
- wait() with FIRST_COMPLETED, ALL_COMPLETED
- Callbacks with add_done_callback()
- Timeout handling
- Exception handling in futures
- Context manager support

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. ThreadPoolExecutor

```python
def task(name, duration):
    time.sleep(duration)
    return f"{name} completed"

with ThreadPoolExecutor(max_workers=3) as executor:
    future1 = executor.submit(task, "Task-1", 0.1)
    future2 = executor.submit(task, "Task-2", 0.05)

    results = [future1.result(), future2.result()]
```

### 2. Map for Batch Processing

```python
def square(x):
    return x ** 2

with ThreadPoolExecutor(max_workers=4) as executor:
    numbers = list(range(10))
    results = list(executor.map(square, numbers))
```

### 3. As Completed

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(download, url): url for url in urls}

    for future in as_completed(futures):
        result = future.result()
        # Process result as soon as it's ready
```

### 4. Callbacks

```python
def callback(future):
    result = future.result()
    print(f"Callback: {result}")

with ThreadPoolExecutor() as executor:
    future = executor.submit(task, 5)
    future.add_done_callback(callback)
```

## Best Practices

1. **Use context manager** - Ensures proper cleanup with `with` statement
2. **Choose right executor** - ThreadPool for I/O, ProcessPool for CPU
3. **Handle exceptions** - Always wrap future.result() in try/except
4. **Use as_completed** - Process results as they arrive for better responsiveness
5. **Set timeouts** - Protect against hung operations
6. **Limit workers** - Don't create too many threads/processes

## Testing

```bash
pytest tests/
```

## Navigation

- Previous: [Program 24 - Multiprocessing](../24_multiprocessing/README.md)
- Next: [Program 26 - Context Managers](../26_context_managers/README.md)
- [Back to Main](../../README.md)
