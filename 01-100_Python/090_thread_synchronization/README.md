# Program 90: Thread Synchronization

Thread synchronization primitives and patterns for concurrent programming.

## Description

This program demonstrates thread synchronization mechanisms including locks, semaphores, events, barriers, and conditions. Essential for coordinating multiple threads and preventing race conditions.

## Learning Objectives

- Master thread synchronization primitives
- Understand race conditions and deadlocks
- Learn thread coordination patterns
- Practice producer-consumer pattern
- Implement thread-safe data structures
- Handle synchronization pitfalls

## Features

- **Locks**: Mutual exclusion (Lock, RLock)
- **Semaphores**: Counting and bounded semaphores
- **Events**: Signal between threads
- **Barriers**: Synchronize at checkpoint
- **Conditions**: Wait for specific condition
- **Thread-safe Queue**: Producer-consumer pattern
- **Atomic Operations**: Thread-safe counters
- **Deadlock Prevention**: Strategies and patterns

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/090_thread_synchronization
python src/main.py
```

## Key Concepts

### Lock (Mutex)

```python
from threading import Lock

lock = Lock()

with lock:
    # Critical section
    # Only one thread at a time
    shared_resource += 1
```

### RLock (Reentrant Lock)

```python
from threading import RLock

lock = RLock()

def recursive_function():
    with lock:
        # Can acquire same lock multiple times
        recursive_function()
```

### Semaphore

```python
from threading import Semaphore

# Allow up to 3 threads
semaphore = Semaphore(3)

with semaphore:
    # Up to 3 threads can be here
    access_limited_resource()
```

### Event

```python
from threading import Event

event = Event()

# Wait for event
event.wait()  # Blocks until set

# Signal event
event.set()   # Wake all waiting threads
event.clear() # Reset event
```

### Condition

```python
from threading import Condition

condition = Condition()

# Producer
with condition:
    produce_item()
    condition.notify()  # Wake one waiting thread

# Consumer
with condition:
    while not item_available():
        condition.wait()  # Release lock and wait
    consume_item()
```

### Barrier

```python
from threading import Barrier

barrier = Barrier(3)  # Wait for 3 threads

def worker():
    # Phase 1
    do_work()
    barrier.wait()  # Wait for all threads
    # Phase 2
    do_more_work()
```

### Producer-Consumer Pattern

```python
from queue import Queue
from threading import Thread

queue = Queue(maxsize=10)

def producer():
    for i in range(100):
        queue.put(i)  # Blocks if full

def consumer():
    while True:
        item = queue.get()  # Blocks if empty
        process(item)
        queue.task_done()
```

## Best Practices

1. **Use context managers**: Automatic lock release
2. **Minimize critical sections**: Hold locks briefly
3. **Avoid nested locks**: Prevent deadlocks
4. **Use Queue for communication**: Thread-safe
5. **Use Events for signaling**: Clean coordination
6. **Prefer higher-level constructs**: Queue over Lock
7. **Test concurrent code**: Race conditions are subtle
8. **Document locking strategy**: Make it clear

## Testing

```bash
# Run tests
pytest tests/

# Stress testing
python src/main.py --stress

# Test scenarios
# - Race conditions
# - Deadlock detection
# - Starvation
# - Lock ordering
# - Performance under contention
# - Producer-consumer balance
```

## Navigation

- **Previous**: [Program 89 - Threading Advanced](../089_threading_advanced/README.md)
- **Next**: [Program 91 - Asyncio Advanced](../091_asyncio_advanced/README.md)
- **Home**: [Main README](../README.md)
