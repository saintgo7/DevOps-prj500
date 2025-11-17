# Program 24: Multiprocessing

Master parallel processing with multiple processes for CPU-bound tasks.

## Learning Objectives

- Understand processes and the multiprocessing module
- Use Process, Pool for parallel execution
- Implement inter-process communication with Queue, Pipe
- Share data with Value, Array, and Manager
- Master process synchronization with Lock

## Features

- Basic Process creation and management
- Process subclassing
- Process Pool for parallel map operations
- Shared memory with Value and Array
- Manager for complex shared structures
- Queue for inter-process communication
- Pipe for two-way communication
- Lock for process synchronization
- Pool with callbacks

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Process

```python
def worker(name, queue):
    """Worker function in separate process."""
    pid = os.getpid()
    queue.put({"name": name, "pid": pid})

# Create process
queue = mp.Queue()
p = mp.Process(target=worker, args=("Process-1", queue))
p.start()
p.join()

result = queue.get()
```

### 2. Process Pool

```python
def square(x):
    return x ** 2

# Use pool to parallelize
with mp.Pool(processes=4) as pool:
    numbers = list(range(10))
    results = pool.map(square, numbers)
```

### 3. Shared Memory

```python
# Create shared memory
shared_value = mp.Value('i', 0)  # Shared integer
shared_array = mp.Array('i', [0, 0, 0])  # Shared array

def increment(shared_val):
    with shared_val.get_lock():
        shared_val.value += 1
```

### 4. Manager for Complex Structures

```python
with mp.Manager() as manager:
    shared_dict = manager.dict()
    shared_list = manager.list()

    # Pass to processes
    processes = []
    for i in range(3):
        p = mp.Process(target=worker, args=(shared_dict, shared_list))
        processes.append(p)
        p.start()
```

## Best Practices

1. **Use Pool for multiple tasks** - Simpler than managing processes manually
2. **Protect shared memory** - Always use locks with Value/Array
3. **Prefer Manager for complex data** - Easier than manual serialization
4. **Use Queue for communication** - Safer than Pipe for multiple processes
5. **Guard with if __name__ == '__main__'** - Required on Windows
6. **Choose right tool** - Multiprocessing for CPU-bound, Threading for I/O-bound

## Testing

```bash
pytest tests/
```

## Navigation

- Previous: [Program 23 - Multithreading](../23_multithreading/README.md)
- Next: [Program 25 - Concurrent Futures](../25_concurrent_futures/README.md)
- [Back to Main](../../README.md)
