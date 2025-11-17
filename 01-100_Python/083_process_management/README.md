# Program 83: Process Management

Process creation, monitoring, and management using Python's multiprocessing and psutil.

## Description

This program demonstrates process management including creating child processes, inter-process communication, process pools, and monitoring system processes. Essential for parallel processing and system administration.

## Learning Objectives

- Understand processes vs threads
- Master multiprocessing module
- Learn inter-process communication
- Practice process pools
- Monitor system processes with psutil

## Features

- **Process Creation**: Fork, spawn, forkserver methods
- **Process Pools**: Parallel task execution
- **IPC Mechanisms**:
  - Pipes
  - Queues
  - Shared memory
  - Manager objects
- **Process Monitoring**: CPU, memory, status
- **Process Control**: Start, stop, kill, wait
- **Process Synchronization**: Locks, semaphores, events
- **System Processes**: List, filter, terminate

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/083_process_management
python src/main.py
```

## Key Concepts

### Process vs Thread

**Process:**
- Separate memory space
- Heavy weight
- True parallelism (GIL doesn't apply)
- IPC needed for communication
- Better for CPU-bound tasks

**Thread:**
- Shared memory space
- Light weight
- Concurrent but not parallel (GIL)
- Shared variables for communication
- Better for I/O-bound tasks

### Multiprocessing Basics

```python
from multiprocessing import Process

def worker(name):
    print(f"Worker {name}")

p = Process(target=worker, args=('A',))
p.start()
p.join()
```

### Process Pool

```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool(4) as pool:
    results = pool.map(square, range(10))
```

### Inter-Process Communication

**Queue:**
```python
from multiprocessing import Queue

q = Queue()
q.put(42)
value = q.get()
```

**Pipe:**
```python
from multiprocessing import Pipe

parent_conn, child_conn = Pipe()
parent_conn.send([1, 2, 3])
child_conn.recv()
```

**Shared Memory:**
```python
from multiprocessing import Value, Array

counter = Value('i', 0)
arr = Array('i', range(10))
```

## Best Practices

1. **Use Pool for parallel tasks**: Simpler than manual processes
2. **Close pools properly**: Use context manager
3. **Use Queue for IPC**: Thread-safe communication
4. **Handle process termination**: Join or terminate
5. **Set start method explicitly**: 'spawn' for portability
6. **Avoid shared state**: Use message passing
7. **Limit pool size**: Don't create too many processes
8. **Use Manager for complex objects**: Shared lists, dicts

## Testing

```bash
# Run tests
pytest tests/

# Test scenarios
# - Process creation and termination
# - Pool execution
# - Inter-process communication
# - Process synchronization
# - Error handling
# - Performance with different pool sizes
```

## Navigation

- **Previous**: [Program 82 - Path Operations](../082_path_operations/README.md)
- **Next**: [Program 84 - Subprocess](../084_subprocess/README.md)
- **Home**: [Main README](../README.md)
