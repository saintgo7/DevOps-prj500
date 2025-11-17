# Program 22: Async/Await Advanced

Advanced asynchronous programming patterns using async/await syntax.

## Learning Objectives

- Master advanced asyncio patterns (gather, wait, as_completed)
- Implement asyncio synchronization primitives (Lock, Semaphore, Event, Queue)
- Use shield() to protect tasks from cancellation
- Handle exceptions in concurrent operations
- Implement structured concurrency with TaskGroup (Python 3.11+)

## Features

- Advanced gather() with return_exceptions
- asyncio.wait() with FIRST_COMPLETED, ALL_COMPLETED
- as_completed() for processing results as they arrive
- Semaphore for concurrency limiting
- Lock for mutual exclusion
- Event for task signaling
- Queue for producer-consumer patterns
- Shield for cancellation protection
- Timeout context managers
- TaskGroup for structured concurrency

## Usage

Run the program:
```bash
python src/main.py
```

Run tests:
```bash
pytest tests/
```

## Key Concepts

### 1. Gather with Exception Handling

```python
async def gather_with_errors():
    """Gather with return_exceptions=True."""
    results = await asyncio.gather(
        task("A", 0.05),
        task("B", 0.03, should_fail=True),
        task("C", 0.04),
        return_exceptions=True
    )
    return results  # Contains both results and exceptions
```

### 2. Semaphore for Concurrency Control

```python
async def limited_concurrency():
    """Limit concurrent tasks with semaphore."""
    sem = asyncio.Semaphore(2)  # Max 2 concurrent

    async def worker(sem, name):
        async with sem:
            await asyncio.sleep(0.1)
            return f"{name} completed"

    tasks = [worker(sem, f"Worker-{i}") for i in range(5)]
    results = await asyncio.gather(*tasks)
```

### 3. Queue for Producer-Consumer

```python
async def producer_consumer():
    """Use queue for async producer-consumer."""
    queue = asyncio.Queue(maxsize=5)

    async def producer(queue, items):
        for i in range(items):
            await queue.put(f"Item-{i}")
        await queue.put(None)  # Sentinel

    async def consumer(queue):
        while True:
            item = await queue.get()
            if item is None:
                break
            # Process item
```

### 4. Shield for Cancellation Protection

```python
async def with_shield():
    """Protect task with shield."""
    task = asyncio.create_task(important_task())
    shielded = asyncio.shield(task)

    try:
        shielded.cancel()
        await shielded
    except asyncio.CancelledError:
        # Shield was cancelled, but task continues
        result = await task  # Can still get result
```

## Best Practices

1. **Handle exceptions in gather()** - Use return_exceptions=True to collect errors
2. **Use Semaphore wisely** - Limit concurrent resource access (DB connections, API calls)
3. **Prefer Queue over direct communication** - Decouple producers and consumers
4. **Shield critical operations** - Protect important tasks from cancellation
5. **Use TaskGroup** - Leverage structured concurrency in Python 3.11+
6. **Lock for shared state** - Prevent race conditions in async code

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/ -k "test_semaphore"
```

## Navigation

- Previous: [Program 21 - Asyncio Basics](../21_asyncio_basics/README.md)
- Next: [Program 23 - Multithreading](../23_multithreading/README.md)
- [Back to Main](../../README.md)
