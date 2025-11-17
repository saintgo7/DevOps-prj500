# Program 23: Multithreading

Master concurrent execution with threads for I/O-bound tasks.

## Learning Objectives

- Understand threads and the threading module
- Implement thread synchronization with Lock, RLock, Semaphore
- Use Event and Condition for thread coordination
- Implement thread pools with Queue
- Master thread-local storage and daemon threads

## Features

- Basic Thread creation and management
- Thread subclassing for custom behavior
- Daemon vs non-daemon threads
- Lock for mutual exclusion
- RLock for reentrant locking
- Semaphore for resource limiting
- Event for signaling
- Condition for complex synchronization
- Thread pool pattern with Queue
- Thread-local storage

## Usage

Run the program:
```bash
python src/main.py
```

## Key Concepts

### 1. Basic Threading

```python
def worker(name, count):
    """Worker function."""
    for i in range(count):
        time.sleep(0.01)
        results.append(f"{name}-{i}")

# Create and start threads
thread1 = threading.Thread(target=worker, args=("Thread-1", 3))
thread2 = threading.Thread(target=worker, args=("Thread-2", 3))

thread1.start()
thread2.start()

# Wait for completion
thread1.join()
thread2.join()
```

### 2. Thread Synchronization with Lock

```python
counter = {"value": 0}
lock = threading.Lock()

def increment_with_lock(iterations):
    """Increment counter safely."""
    for _ in range(iterations):
        with lock:  # Acquire lock
            current = counter["value"]
            time.sleep(0.0001)
            counter["value"] = current + 1
```

### 3. Semaphore for Resource Limiting

```python
semaphore = threading.Semaphore(2)  # Max 2 concurrent

def worker(name):
    """Worker with semaphore."""
    with semaphore:
        # Only 2 threads can be here at once
        time.sleep(0.1)
```

### 4. Thread Pool with Queue

```python
def worker(queue, results):
    """Worker thread processing queue items."""
    while True:
        item = queue.get()
        if item is None:
            break
        result = item ** 2
        results.append(result)
        queue.task_done()

# Create thread pool
queue = Queue()
threads = []
for _ in range(3):
    t = threading.Thread(target=worker, args=(queue, results))
    t.start()
    threads.append(t)

# Add tasks
for i in range(10):
    queue.put(i)

# Wait for completion
queue.join()
```

## Best Practices

1. **Use Lock for shared data** - Always protect shared resources with locks
2. **Prefer context managers** - Use `with lock:` instead of manual acquire/release
3. **Avoid deadlocks** - Acquire locks in consistent order
4. **Use daemon for background** - Set daemon=True for background threads
5. **Thread pool for multiple tasks** - Use Queue-based pools for work distribution
6. **Be aware of GIL** - Python's GIL limits CPU-bound threading benefits

## Testing

```bash
pytest tests/
```

## Navigation

- Previous: [Program 22 - Async/Await](../22_async_await/README.md)
- Next: [Program 24 - Multiprocessing](../24_multiprocessing/README.md)
- [Back to Main](../../README.md)
