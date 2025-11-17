#!/usr/bin/env python3
"""Program 29: Type Hints - Master advanced type annotations and static typing."""

from typing import (
    Any, Union, Optional, List, Dict, Tuple, Set, Callable,
    TypeVar, Generic, Protocol, Literal, Final, cast, overload
)
from collections.abc import Sequence, Iterable, Mapping
from dataclasses import dataclass


def demonstrate_basic_types() -> dict[str, Any]:
    """Demonstrate basic type hints."""

    def greet(name: str, age: int) -> str:
        """Function with basic type hints."""
        return f"{name} is {age} years old"

    def calculate(x: float, y: float) -> float:
        """Numeric type hints."""
        return x + y

    def is_valid(flag: bool) -> bool:
        """Boolean type hints."""
        return not flag

    return {
        "greet": greet("Alice", 30),
        "calculate": calculate(3.14, 2.86),
        "is_valid": is_valid(False),
        "note": "Basic types: int, str, float, bool",
    }


def demonstrate_collection_types() -> dict[str, Any]:
    """Demonstrate collection type hints."""

    def process_list(items: List[int]) -> int:
        """List of integers."""
        return sum(items)

    def process_dict(data: Dict[str, int]) -> List[str]:
        """Dictionary with string keys, int values."""
        return list(data.keys())

    def process_tuple(coords: Tuple[float, float, float]) -> float:
        """Fixed-size tuple."""
        return sum(coords)

    def process_set(unique: Set[str]) -> int:
        """Set of strings."""
        return len(unique)

    return {
        "list_sum": process_list([1, 2, 3, 4, 5]),
        "dict_keys": process_dict({"a": 1, "b": 2}),
        "tuple_sum": process_tuple((1.5, 2.5, 3.0)),
        "set_len": process_set({"a", "b", "c"}),
        "note": "Collection types: List, Dict, Tuple, Set",
    }


def demonstrate_optional_union() -> dict[str, Any]:
    """Demonstrate Optional and Union types."""

    def find_user(user_id: int) -> Optional[str]:
        """Return username or None."""
        users = {1: "Alice", 2: "Bob"}
        return users.get(user_id)

    def process_value(value: Union[int, str]) -> str:
        """Accept int or str."""
        if isinstance(value, int):
            return f"Number: {value}"
        return f"String: {value}"

    # New syntax (Python 3.10+)
    def modern_optional(value: str | None) -> str:
        """Using | for union types."""
        return value or "default"

    return {
        "found_user": find_user(1),
        "missing_user": find_user(999),
        "process_int": process_value(42),
        "process_str": process_value("hello"),
        "modern": modern_optional(None),
        "note": "Optional[T] = Union[T, None] = T | None",
    }


def demonstrate_callable_types() -> dict[str, Any]:
    """Demonstrate Callable type hints."""

    def execute(func: Callable[[int, int], int], a: int, b: int) -> int:
        """Execute a function with two int args returning int."""
        return func(a, b)

    def add(x: int, y: int) -> int:
        return x + y

    def multiply(x: int, y: int) -> int:
        return x * y

    # Higher order function
    def make_multiplier(factor: int) -> Callable[[int], int]:
        """Return a function that multiplies by factor."""

        def multiplier(x: int) -> int:
            return x * factor

        return multiplier

    times_three = make_multiplier(3)

    return {
        "execute_add": execute(add, 5, 3),
        "execute_multiply": execute(multiply, 5, 3),
        "multiplier_result": times_three(7),
        "note": "Callable[[arg_types], return_type] for function types",
    }


def demonstrate_type_variables() -> dict[str, Any]:
    """Demonstrate TypeVar for generic types."""

    T = TypeVar('T')

    def first(items: List[T]) -> Optional[T]:
        """Return first item of any type."""
        return items[0] if items else None

    def reverse(items: List[T]) -> List[T]:
        """Reverse list of any type."""
        return items[::-1]

    # Constrained TypeVar
    NumberType = TypeVar('NumberType', int, float)

    def add_numbers(a: NumberType, b: NumberType) -> NumberType:
        """Add numbers (int or float only)."""
        return a + b  # type: ignore

    return {
        "first_int": first([1, 2, 3]),
        "first_str": first(["a", "b", "c"]),
        "reverse_int": reverse([1, 2, 3]),
        "add_result": add_numbers(5, 3),
        "note": "TypeVar enables generic type parameters",
    }


def demonstrate_generic_classes() -> dict[str, Any]:
    """Demonstrate Generic classes."""

    T = TypeVar('T')

    class Stack(Generic[T]):
        """Generic stack implementation."""

        def __init__(self):
            self._items: List[T] = []

        def push(self, item: T) -> None:
            self._items.append(item)

        def pop(self) -> Optional[T]:
            return self._items.pop() if self._items else None

        def peek(self) -> Optional[T]:
            return self._items[-1] if self._items else None

    # Type-specific stacks
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)

    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")

    return {
        "int_pop": int_stack.pop(),
        "str_pop": str_stack.pop(),
        "note": "Generic[T] creates generic classes",
    }


def demonstrate_protocols() -> dict[str, Any]:
    """Demonstrate Protocol for structural subtyping."""

    class Drawable(Protocol):
        """Protocol for drawable objects."""

        def draw(self) -> str:
            ...

    class Circle:
        """Circle implements Drawable protocol."""

        def draw(self) -> str:
            return "Drawing circle"

    class Square:
        """Square implements Drawable protocol."""

        def draw(self) -> str:
            return "Drawing square"

    def render(shape: Drawable) -> str:
        """Render any drawable shape."""
        return shape.draw()

    circle = Circle()
    square = Square()

    return {
        "render_circle": render(circle),
        "render_square": render(square),
        "note": "Protocol enables structural (duck) typing",
    }


def demonstrate_literal_types() -> dict[str, Any]:
    """Demonstrate Literal types."""

    def set_mode(mode: Literal["read", "write", "append"]) -> str:
        """Accept only specific string values."""
        return f"Mode set to {mode}"

    def get_coordinate(axis: Literal["x", "y", "z"]) -> int:
        """Accept only x, y, or z."""
        coords = {"x": 10, "y": 20, "z": 30}
        return coords[axis]

    # Type checker would error on invalid literals
    # set_mode("invalid")  # Error!

    return {
        "mode": set_mode("read"),
        "coordinate": get_coordinate("y"),
        "note": "Literal restricts to specific values",
    }


def demonstrate_final() -> dict[str, Any]:
    """Demonstrate Final type."""

    MAX_SIZE: Final = 100
    API_KEY: Final[str] = "secret-key"

    class Config:
        """Configuration class."""
        DATABASE: Final[str] = "postgres"

    # Type checker would warn about reassignment
    # MAX_SIZE = 200  # Error!
    # Config.DATABASE = "mysql"  # Error!

    return {
        "max_size": MAX_SIZE,
        "api_key_type": type(API_KEY).__name__,
        "database": Config.DATABASE,
        "note": "Final indicates value should not be reassigned",
    }


def demonstrate_advanced_patterns() -> dict[str, Any]:
    """Demonstrate advanced type hint patterns."""

    # Type aliases
    UserId = int
    UserName = str
    UserData = Dict[str, Union[str, int]]

    def get_user(user_id: UserId) -> UserData:
        """Use type aliases for clarity."""
        return {"id": user_id, "name": "Alice", "age": 30}

    # Nested generics
    Matrix = List[List[float]]

    def transpose(matrix: Matrix) -> Matrix:
        """Transpose a matrix."""
        return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

    # Multiple type variables
    K = TypeVar('K')
    V = TypeVar('V')

    def invert_dict(d: Dict[K, V]) -> Dict[V, K]:
        """Invert dictionary keys and values."""
        return {v: k for k, v in d.items()}

    return {
        "user": get_user(123),
        "transposed": transpose([[1, 2], [3, 4]]),
        "inverted": invert_dict({"a": 1, "b": 2}),
        "note": "Type aliases and nested generics improve code clarity",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 29: Type Hints")
    print("=" * 60)

    print("\n1. Basic Types:")
    basic = demonstrate_basic_types()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Collection Types:")
    collections = demonstrate_collection_types()
    for key, value in collections.items():
        print(f"   {key}: {value}")

    print("\n3. Optional and Union:")
    optional = demonstrate_optional_union()
    for key, value in optional.items():
        print(f"   {key}: {value}")

    print("\n4. Callable Types:")
    callable_demo = demonstrate_callable_types()
    for key, value in callable_demo.items():
        print(f"   {key}: {value}")

    print("\n5. TypeVar (Generics):")
    typevar = demonstrate_type_variables()
    for key, value in typevar.items():
        print(f"   {key}: {value}")

    print("\n6. Generic Classes:")
    generic = demonstrate_generic_classes()
    for key, value in generic.items():
        print(f"   {key}: {value}")

    print("\n7. Protocols:")
    protocols = demonstrate_protocols()
    for key, value in protocols.items():
        print(f"   {key}: {value}")

    print("\n8. Literal Types:")
    literal = demonstrate_literal_types()
    for key, value in literal.items():
        print(f"   {key}: {value}")

    print("\n9. Final Types:")
    final = demonstrate_final()
    for key, value in final.items():
        print(f"   {key}: {value}")

    print("\n10. Advanced Patterns:")
    advanced = demonstrate_advanced_patterns()
    for key, value in advanced.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
