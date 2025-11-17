# Program 94: Resource Management

Comprehensive resource management including context managers, cleanup, and resource limits.

## Description

This program demonstrates proper resource management using context managers, weak references, resource limits, and cleanup patterns. Essential for writing robust, leak-free applications.

## Learning Objectives

- Master context managers
- Understand resource lifecycles
- Learn cleanup patterns
- Practice weak references
- Set resource limits
- Prevent resource leaks

## Features

- **Context Managers**: with statement, __enter__/__exit__
- **Custom Context Managers**: @contextmanager decorator
- **ExitStack**: Dynamic context management
- **Resource Limits**: setrlimit, getrlimit
- **Weak References**: Avoid circular references
- **Cleanup Handlers**: atexit, weakref.finalize
- **Memory Management**: Garbage collection control
- **File Handles**: Proper file closure

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/094_resource_management
python src/main.py
```

## Key Concepts

### Context Managers

```python
# Built-in context manager
with open('file.txt', 'r') as f:
    data = f.read()
# File automatically closed

# Custom context manager
class Resource:
    def __enter__(self):
        print("Acquiring resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        return False  # Don't suppress exceptions

with Resource() as r:
    r.use()
```

### @contextmanager Decorator

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    # Setup
    resource = acquire()
    try:
        yield resource
    finally:
        # Cleanup
        release(resource)

with managed_resource() as r:
    use(r)
```

### ExitStack

```python
from contextlib import ExitStack

with ExitStack() as stack:
    # Dynamically enter contexts
    files = [stack.enter_context(open(f)) for f in filenames]

    # All files automatically closed
```

### Resource Limits

```python
import resource

# Get current limits
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)

# Set new limit
resource.setrlimit(resource.RLIMIT_NOFILE, (1024, hard))
```

### Weak References

```python
import weakref

class Resource:
    pass

obj = Resource()
weak_ref = weakref.ref(obj)

# Get object (returns None if collected)
obj = weak_ref()
```

### Cleanup Handlers

```python
import atexit

def cleanup():
    print("Cleaning up")

atexit.register(cleanup)

# Or with decorator
@atexit.register
def another_cleanup():
    print("More cleanup")
```

### Memory Management

```python
import gc

# Collect garbage
collected = gc.collect()

# Disable automatic collection
gc.disable()

# Get object count
stats = gc.get_count()
```

## Best Practices

1. **Always use context managers**: For file, network, database
2. **Implement __enter__/__exit__**: For custom resources
3. **Use ExitStack for dynamic resources**: Multiple files, connections
4. **Set resource limits**: Prevent resource exhaustion
5. **Use weak references**: Break circular references
6. **Register cleanup handlers**: atexit for final cleanup
7. **Explicit cleanup**: Don't rely solely on garbage collection
8. **Test resource cleanup**: Verify no leaks

## Testing

```bash
# Run tests
pytest tests/

# Check for resource leaks
python -m pytest tests/ --verbose

# Test scenarios
# - Context manager enter/exit
# - Exception handling in context
# - Resource limit enforcement
# - Memory leak detection
# - Cleanup handler execution
# - Circular reference handling
```

## Navigation

- **Previous**: [Program 93 - System Monitoring](../093_system_monitoring/README.md)
- **Next**: [Program 95 - Command Line Tools](../095_command_line_tools/README.md)
- **Home**: [Main README](../README.md)
