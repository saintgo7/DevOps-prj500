# Program 21: Asyncio Basics

Master asynchronous programming fundamentals with Python's asyncio library.

## Learning Objectives

- Understand coroutines and the async/await syntax
- Master asyncio.run(), create_task(), and gather() for concurrent execution
- Learn task creation, cancellation, and timeout handling
- Implement async context managers and async iterators
- Chain and coordinate multiple asynchronous operations

## Features

- Basic coroutine definition and execution
- Concurrent task execution with create_task() and gather()
- Timeout handling with wait_for()
- Task cancellation with CancelledError
- Async context managers (__aenter__, __aexit__)
- Async iteration (__aiter__, __anext__)
- Coroutine chaining for sequential async operations
- Practical demonstrations of all asyncio fundamentals

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

### 1. Basic Coroutine

```python
async def simple_coroutine():
    """Define a coroutine with async def."""
    return "Hello from coroutine!"

# Run the coroutine
result = asyncio.run(simple_coroutine())
```

### 2. Concurrent Execution

```python
async def run_concurrent():
    """Run multiple tasks concurrently."""
    task1 = asyncio.create_task(worker("A", 0.2))
    task2 = asyncio.create_task(worker("B", 0.1))

    # Wait for all tasks
    results = await asyncio.gather(task1, task2)
    return results
```

### 3. Timeout Handling

```python
async def with_timeout():
    """Run operation with timeout."""
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
    except asyncio.TimeoutError:
        result = "Timeout"
    return result
```

### 4. Async Context Manager

```python
class AsyncResource:
    async def __aenter__(self):
        await asyncio.sleep(0.01)
        return "Resource acquired"

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.01)
        return False

async def use_resource():
    async with AsyncResource() as resource:
        return f"Using {resource}"
```

## Best Practices

1. **Use asyncio.run()** - Always use asyncio.run() as entry point, not loop.run_until_complete()
2. **Create tasks early** - Use create_task() immediately to start concurrent execution
3. **Gather for collections** - Use gather() to run multiple coroutines concurrently
4. **Handle cancellation** - Always handle CancelledError in long-running tasks
5. **Avoid blocking calls** - Never use time.sleep() or blocking I/O in async functions
6. **Use timeouts** - Protect against hung operations with wait_for()

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/ -k "test_basic_coroutine"
```

## Navigation

- Previous: [Program 20 - Generators](../20_generators/README.md)
- Next: [Program 22 - Async/Await](../22_async_await/README.md)
- [Back to Main](../../README.md)
