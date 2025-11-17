# Program 26: Context Managers

Master resource management with context managers using __enter__, __exit__, and @contextmanager.

## Learning Objectives

- Understand the context manager protocol (__enter__, __exit__)
- Use @contextmanager decorator for simple context managers
- Handle exceptions in context managers
- Implement contextlib utilities (closing, suppress, redirect_stdout)
- Master ExitStack for dynamic context management

## Features

- Basic context manager with __enter__/__exit__
- Exception handling and suppression
- @contextmanager decorator
- Multiple and nested contexts
- contextlib.closing for objects with close()
- contextlib.suppress for ignoring exceptions
- contextlib.redirect_stdout for capturing output
- ExitStack for dynamic and conditional contexts
- Reusable context managers
- Practical examples (timer, temporary attributes, transactions)

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Context Manager

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions

with FileManager('test.txt', 'w') as f:
    f.write("Hello")
```

### 2. @contextmanager Decorator

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    # Setup
    resource = f"Resource-{name}"
    print(f"Acquiring {resource}")
    try:
        yield resource  # Provide to with block
    finally:
        # Cleanup (always runs)
        print(f"Releasing {resource}")

with managed_resource("DB") as res:
    print(f"Using {res}")
```

### 3. ExitStack for Dynamic Contexts

```python
from contextlib import ExitStack

def use_multiple_resources(count):
    with ExitStack() as stack:
        resources = []
        for i in range(count):
            res = stack.enter_context(resource(str(i)))
            resources.append(res)
        return resources
```

### 4. Suppress for Exception Handling

```python
from contextlib import suppress

# Ignore specific exceptions
with suppress(FileNotFoundError):
    os.remove('nonexistent_file.txt')
```

## Best Practices

1. **Use context managers for resources** - Files, locks, connections, etc.
2. **Always clean up in __exit__** - Ensure resources are released
3. **Return False from __exit__** - Let exceptions propagate unless intentionally suppressing
4. **Use @contextmanager for simple cases** - Cleaner than class-based approach
5. **Leverage contextlib utilities** - closing, suppress, redirect_stdout
6. **ExitStack for dynamic resources** - When number of contexts varies

## Testing

```bash
pytest tests/
```

## Navigation

- Previous: [Program 25 - Concurrent Futures](../25_concurrent_futures/README.md)
- Next: [Program 27 - Metaclasses](../27_metaclasses/README.md)
- [Back to Main](../../README.md)
