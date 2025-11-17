# Program 92: Event Loops

Deep dive into asyncio event loops, protocols, and low-level async APIs.

## Description

This program explores event loop internals including callbacks, futures, protocols, and transports. Understanding these fundamentals enables building custom async frameworks and debugging async code.

## Learning Objectives

- Understand event loop architecture
- Master callbacks and futures
- Learn protocols and transports
- Practice low-level async APIs
- Implement custom async patterns
- Debug event loop issues

## Features

- **Event Loop Basics**: Get, run, close loops
- **Callbacks**: call_soon, call_later, call_at
- **Futures**: Low-level result containers
- **Tasks**: High-level coroutine wrappers
- **Protocols**: Callback-based network code
- **Transports**: Abstract communication channels
- **Async Iteration**: Custom async iterators
- **Async Context**: Custom context managers

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/092_event_loops
python src/main.py
```

## Key Concepts

### Event Loop Operations

```python
import asyncio

# Get event loop
loop = asyncio.get_event_loop()

# Schedule callback
loop.call_soon(callback, *args)
loop.call_later(delay, callback, *args)
loop.call_at(when, callback, *args)

# Run coroutine
loop.run_until_complete(coroutine())

# Run forever
loop.run_forever()
```

### Futures

```python
# Low-level result container
future = loop.create_future()

# Set result (from another callback)
future.set_result("value")

# Get result (blocks until set)
result = await future
```

### Protocols and Transports

```python
class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)

    def connection_lost(self, exc):
        pass

# Create server
server = await loop.create_server(
    EchoProtocol,
    'localhost', 8888
)
```

### Running in Executor

```python
import concurrent.futures

# Run blocking code in thread pool
loop = asyncio.get_event_loop()
with concurrent.futures.ThreadPoolExecutor() as pool:
    result = await loop.run_in_executor(
        pool,
        blocking_function,
        *args
    )
```

### Event Loop Policies

```python
# Get/set event loop policy
policy = asyncio.get_event_loop_policy()
asyncio.set_event_loop_policy(policy)

# Use uvloop for better performance
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```

## Best Practices

1. **Use asyncio.run() for simple cases**: Manages loop lifecycle
2. **Get loop once**: Avoid repeated get_event_loop() calls
3. **Close loops properly**: Prevent resource leaks
4. **Use high-level APIs when possible**: Tasks over futures
5. **Run blocking code in executor**: Don't block event loop
6. **Set loop debug mode**: asyncio.get_event_loop().set_debug(True)
7. **Consider uvloop**: Drop-in replacement, 2-4x faster
8. **Monitor slow callbacks**: Debug mode tracks these

## Testing

```bash
# Run tests
pytest tests/

# Enable debug mode
PYTHONASYNCIODEBUG=1 python src/main.py

# Test scenarios
# - Callback scheduling
# - Future completion
# - Protocol implementation
# - Executor usage
# - Loop lifecycle
# - Performance benchmarks
```

## Navigation

- **Previous**: [Program 91 - Asyncio Advanced](../091_asyncio_advanced/README.md)
- **Next**: [Program 93 - System Monitoring](../093_system_monitoring/README.md)
- **Home**: [Main README](../README.md)
