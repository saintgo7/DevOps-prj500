# Program 30: Protocols

Master structural subtyping and runtime protocols in Python.

## Learning Objectives

- Understand Protocol for structural typing
- Use @runtime_checkable for isinstance() checks
- Differentiate Protocol vs ABC (nominal typing)
- Implement generic protocols
- Use built-in protocols (Iterator, Sized, Comparable)

## Features

- Basic Protocol definition
- @runtime_checkable decorator
- Protocol vs ABC comparison
- Multiple method protocols
- Generic protocols with TypeVar
- Iterator protocol
- Comparable protocol
- Context manager protocol
- Sized protocol
- Protocol composition

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Protocol

```python
from typing import Protocol

class Closeable(Protocol):
    def close(self) -> None:
        ...

def cleanup(resource: Closeable) -> None:
    resource.close()
```

### 2. Runtime Checkable

```python
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str:
        ...

class Circle:
    def draw(self) -> str:
        return "Circle"

print(isinstance(Circle(), Drawable))  # True
```

### 3. Generic Protocol

```python
T = TypeVar('T')

class Container(Protocol[T]):
    def add(self, item: T) -> None:
        ...

    def get(self) -> T:
        ...
```

## Best Practices

1. **Prefer Protocol over ABC** - More Pythonic, supports duck typing
2. **Use @runtime_checkable sparingly** - Type checking at runtime has overhead
3. **Keep protocols focused** - Single responsibility principle
4. **Compose protocols** - Combine multiple protocols via inheritance
5. **Document protocol requirements** - Clear docstrings for protocol methods

## Testing

```bash
pytest tests/
```

## Navigation

- Previous: [Program 29 - Type Hints](../29_type_hints/README.md)
- Next: [Program 31 - Dataclasses Advanced](../31_dataclasses_advanced/README.md)
- [Back to Main](../../README.md)
