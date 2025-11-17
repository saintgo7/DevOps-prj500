# Program 29: Type Hints

Master advanced type annotations and static typing in Python.

## Learning Objectives

- Use basic type hints (int, str, float, bool)
- Master collection types (List, Dict, Tuple, Set)
- Implement Optional and Union types
- Create generic types with TypeVar and Generic
- Use Protocol for structural subtyping

## Features

- Basic type annotations
- Collection type hints
- Optional and Union types
- Callable type hints
- TypeVar for generics
- Generic classes
- Protocol for duck typing
- Literal types for specific values
- Final for constants
- Type aliases and nested generics

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Types

```python
def greet(name: str, age: int) -> str:
    return f"{name} is {age} years old"
```

### 2. Collections

```python
def process_list(items: List[int]) -> int:
    return sum(items)

def process_dict(data: Dict[str, int]) -> List[str]:
    return list(data.keys())
```

### 3. Generic Types

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self):
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> Optional[T]:
        return self._items.pop() if self._items else None
```

### 4. Protocol

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str:
        ...

def render(shape: Drawable) -> str:
    return shape.draw()
```

## Best Practices

1. **Add type hints gradually** - Don't need to type everything at once
2. **Use mypy for checking** - Run static type checker regularly
3. **Prefer Protocol over ABC** - More flexible, duck typing friendly
4. **Type aliases for clarity** - UserId = int makes code more readable
5. **Use Optional explicitly** - Better than implicit None
6. **Generic for reusable code** - Type-safe containers and functions

## Testing

```bash
# Type check
mypy src/

# Run tests
pytest tests/
```

## Navigation

- Previous: [Program 28 - Descriptors](../28_descriptors/README.md)
- Next: [Program 30 - Protocols](../30_protocols/README.md)
- [Back to Main](../../README.md)
