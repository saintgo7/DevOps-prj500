# Program 91: Advanced Asyncio

Advanced asynchronous programming with asyncio including tasks, coroutines, and async patterns.

## Description

This program demonstrates advanced asyncio concepts including task management, async context managers, async iterators, timeouts, and cancellation. Covers modern asynchronous programming patterns in Python.

## Learning Objectives

- Master asyncio task management
- Understand coroutines and awaitables
- Learn async context managers and iterators
- Practice cancellation and timeouts
- Implement concurrent async patterns
- Handle async exceptions

## Features

- **Async Functions**: Define coroutines with async/await
- **Task Management**: Create, cancel, gather tasks
- **Async Context Managers**: async with statement
- **Async Iterators**: async for loops
- **Timeouts**: wait_for() and timeout handling
- **Cancellation**: Cancel long-running tasks
- **Concurrent Execution**: gather(), wait(), as_completed()
- **Error Handling**: Exception propagation in tasks

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/091_asyncio_advanced
python src/main.py
```

## Key Concepts

### Coroutines and Tasks

```python
import asyncio

async def my_coroutine():
    await asyncio.sleep(1)
    return "result"

# Run coroutine
asyncio.run(my_coroutine())

# Create task
task = asyncio.create_task(my_coroutine())
result = await task
```

### Concurrent Execution

```python
# Wait for all tasks
results = await asyncio.gather(
    task1(),
    task2(),
    task3()
)

# Wait with timeout
try:
    result = await asyncio.wait_for(task(), timeout=5.0)
except asyncio.TimeoutError:
    print("Timeout!")
```

### Async Context Manager

```python
class AsyncResource:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

async with AsyncResource() as resource:
    await resource.use()
```

### Async Iterator

```python
class AsyncIterator:
    async def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(0.1)
        if self.done:
            raise StopAsyncIteration
        return self.next_value()

async for item in AsyncIterator():
    process(item)
```

### Task Cancellation

```python
task = asyncio.create_task(long_running())

# Cancel task
task.cancel()

try:
    await task
except asyncio.CancelledError:
    print("Task was cancelled")
```

### Error Handling

```python
async def task_with_error():
    raise ValueError("Error!")

try:
    results = await asyncio.gather(
        task1(),
        task_with_error(),
        task3(),
        return_exceptions=True  # Don't stop on first exception
    )
except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

1. **Use asyncio.run() for entry point**: Handles event loop
2. **Create tasks for concurrent execution**: Don't just await
3. **Set timeouts**: Prevent hanging operations
4. **Handle cancellation**: Clean up resources
5. **Use return_exceptions in gather**: Continue on errors
6. **Implement async context managers**: Proper cleanup
7. **Use asyncio libraries**: aiohttp, aiofiles, etc.
8. **Profile async code**: Find bottlenecks

## Testing

```bash
# Run tests
pytest tests/

# Async testing with pytest-asyncio
pytest --asyncio-mode=auto

# Test scenarios
# - Concurrent task execution
# - Timeout handling
# - Cancellation
# - Exception propagation
# - Resource cleanup
# - Performance comparison with sync code
```

## Navigation

- **Previous**: [Program 90 - Thread Synchronization](../090_thread_synchronization/README.md)
- **Next**: [Program 92 - Event Loops](../092_event_loops/README.md)
- **Home**: [Main README](../README.md)
