#!/usr/bin/env python3
"""Program 30: Protocols - Master structural subtyping and runtime protocols."""

from typing import Protocol, runtime_checkable, Any, Iterator
from abc import ABC, abstractmethod


def demonstrate_basic_protocol() -> dict[str, Any]:
    """Demonstrate basic Protocol definition."""

    class Closeable(Protocol):
        """Protocol for objects that can be closed."""

        def close(self) -> None:
            """Close the resource."""
            ...

    class File:
        """File implements Closeable protocol."""

        def __init__(self, name: str):
            self.name = name
            self.closed = False

        def close(self) -> None:
            self.closed = True

    class Connection:
        """Connection also implements Closeable protocol."""

        def __init__(self):
            self.active = True

        def close(self) -> None:
            self.active = False

    def cleanup(resource: Closeable) -> str:
        """Clean up any closeable resource."""
        resource.close()
        return "Resource closed"

    file = File("test.txt")
    conn = Connection()

    return {
        "file_result": cleanup(file),
        "file_closed": file.closed,
        "conn_result": cleanup(conn),
        "conn_active": conn.active,
        "note": "Protocol enables structural (duck) typing",
    }


def demonstrate_runtime_checkable() -> dict[str, Any]:
    """Demonstrate @runtime_checkable decorator."""

    @runtime_checkable
    class Drawable(Protocol):
        """Runtime checkable drawing protocol."""

        def draw(self) -> str:
            ...

    class Circle:
        """Implements Drawable."""

        def draw(self) -> str:
            return "Circle drawn"

    class Rectangle:
        """Implements Drawable."""

        def draw(self) -> str:
            return "Rectangle drawn"

    class NotDrawable:
        """Does not implement Drawable."""

        def paint(self) -> str:
            return "Painted"

    circle = Circle()
    rect = Rectangle()
    other = NotDrawable()

    return {
        "circle_is_drawable": isinstance(circle, Drawable),
        "rect_is_drawable": isinstance(rect, Drawable),
        "other_is_drawable": isinstance(other, Drawable),
        "note": "@runtime_checkable enables isinstance() checks",
    }


def demonstrate_protocol_vs_abc() -> dict[str, Any]:
    """Demonstrate difference between Protocol and ABC."""

    # ABC approach - nominal typing
    class ShapeABC(ABC):
        """Abstract base class."""

        @abstractmethod
        def area(self) -> float:
            pass

    class SquareABC(ShapeABC):
        """Must explicitly inherit."""

        def __init__(self, side: float):
            self.side = side

        def area(self) -> float:
            return self.side ** 2

    # Protocol approach - structural typing
    class ShapeProtocol(Protocol):
        """Protocol definition."""

        def area(self) -> float:
            ...

    class CircleImplicit:
        """Implicitly satisfies protocol without inheritance."""

        def __init__(self, radius: float):
            self.radius = radius

        def area(self) -> float:
            return 3.14159 * self.radius ** 2

    def calculate_area_abc(shape: ShapeABC) -> float:
        """Requires explicit inheritance."""
        return shape.area()

    def calculate_area_protocol(shape: ShapeProtocol) -> float:
        """Works with any object having area() method."""
        return shape.area()

    square = SquareABC(5)
    circle = CircleImplicit(3)

    return {
        "abc_area": calculate_area_abc(square),
        "protocol_area": calculate_area_protocol(circle),
        "protocol_works_with_square": calculate_area_protocol(square),
        "note": "Protocol = structural, ABC = nominal typing",
    }


def demonstrate_multiple_methods() -> dict[str, Any]:
    """Demonstrate Protocol with multiple methods."""

    class Serializable(Protocol):
        """Protocol for serializable objects."""

        def to_dict(self) -> dict:
            ...

        def from_dict(self, data: dict) -> None:
            ...

    class User:
        """User implements Serializable."""

        def __init__(self, name: str = "", age: int = 0):
            self.name = name
            self.age = age

        def to_dict(self) -> dict:
            return {"name": self.name, "age": self.age}

        def from_dict(self, data: dict) -> None:
            self.name = data["name"]
            self.age = data["age"]

    def save(obj: Serializable) -> dict:
        """Save any serializable object."""
        return obj.to_dict()

    def load(obj: Serializable, data: dict) -> None:
        """Load into any serializable object."""
        obj.from_dict(data)

    user = User("Alice", 30)
    data = save(user)

    new_user = User()
    load(new_user, data)

    return {
        "saved_data": data,
        "loaded_name": new_user.name,
        "loaded_age": new_user.age,
        "note": "Protocols can define multiple methods",
    }


def demonstrate_generic_protocol() -> dict[str, Any]:
    """Demonstrate generic Protocol."""

    from typing import TypeVar

    T = TypeVar('T')

    class Container(Protocol[T]):
        """Generic container protocol."""

        def add(self, item: T) -> None:
            ...

        def get(self) -> T:
            ...

    class IntBox:
        """Container for integers."""

        def __init__(self):
            self.value: int = 0

        def add(self, item: int) -> None:
            self.value = item

        def get(self) -> int:
            return self.value

    class StrBox:
        """Container for strings."""

        def __init__(self):
            self.value: str = ""

        def add(self, item: str) -> None:
            self.value = item

        def get(self) -> str:
            return self.value

    def use_container(container: Container[T], item: T) -> T:
        """Use any container."""
        container.add(item)
        return container.get()

    int_box = IntBox()
    str_box = StrBox()

    return {
        "int_result": use_container(int_box, 42),
        "str_result": use_container(str_box, "hello"),
        "note": "Protocols can be generic with TypeVar",
    }


def demonstrate_iterator_protocol() -> dict[str, Any]:
    """Demonstrate built-in iterator protocol."""

    class Countdown:
        """Custom iterator."""

        def __init__(self, start: int):
            self.current = start

        def __iter__(self) -> Iterator[int]:
            return self

        def __next__(self) -> int:
            if self.current <= 0:
                raise StopIteration
            self.current -= 1
            return self.current + 1

    def consume_iterator(it: Iterator[int]) -> list[int]:
        """Consume any iterator."""
        return list(it)

    countdown = Countdown(5)
    result = consume_iterator(countdown)

    return {
        "countdown": result,
        "note": "Iterator is a built-in Protocol",
    }


def demonstrate_comparable_protocol() -> dict[str, Any]:
    """Demonstrate comparable protocol."""

    from typing import TypeVar

    T = TypeVar('T')

    class Comparable(Protocol):
        """Protocol for comparable objects."""

        def __lt__(self, other: Any) -> bool:
            ...

        def __gt__(self, other: Any) -> bool:
            ...

    class Score:
        """Score that can be compared."""

        def __init__(self, value: int):
            self.value = value

        def __lt__(self, other: 'Score') -> bool:
            return self.value < other.value

        def __gt__(self, other: 'Score') -> bool:
            return self.value > other.value

    def find_max(items: list[Comparable]) -> Comparable:
        """Find maximum of comparable items."""
        if not items:
            raise ValueError("Empty list")
        max_item = items[0]
        for item in items[1:]:
            if item > max_item:  # type: ignore
                max_item = item
        return max_item

    scores = [Score(85), Score(92), Score(78), Score(95)]
    max_score = find_max(scores)  # type: ignore

    return {
        "max_score": max_score.value,  # type: ignore
        "note": "Comparable protocol enables ordering operations",
    }


def demonstrate_context_manager_protocol() -> dict[str, Any]:
    """Demonstrate context manager protocol."""

    class ManagedResource:
        """Implements context manager protocol."""

        def __init__(self, name: str):
            self.name = name
            self.entered = False
            self.exited = False

        def __enter__(self) -> 'ManagedResource':
            self.entered = True
            return self

        def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
            self.exited = True
            return False

    def use_context_manager(cm):
        """Use any context manager."""
        with cm as resource:
            return f"Using {resource.name}"

    resource = ManagedResource("Database")
    result = use_context_manager(resource)

    return {
        "result": result,
        "entered": resource.entered,
        "exited": resource.exited,
        "note": "Context manager is a structural protocol",
    }


def demonstrate_sized_protocol() -> dict[str, Any]:
    """Demonstrate Sized protocol."""

    from typing import Sized

    class CustomCollection:
        """Collection with length."""

        def __init__(self, items: list):
            self.items = items

        def __len__(self) -> int:
            return len(self.items)

    def get_size(obj: Sized) -> int:
        """Get size of any sized object."""
        return len(obj)

    collection = CustomCollection([1, 2, 3, 4, 5])

    return {
        "collection_size": get_size(collection),
        "list_size": get_size([1, 2, 3]),
        "str_size": get_size("hello"),
        "note": "Sized protocol requires __len__ method",
    }


def demonstrate_protocol_composition() -> dict[str, Any]:
    """Demonstrate composing multiple protocols."""

    class Readable(Protocol):
        """Protocol for readable objects."""

        def read(self) -> str:
            ...

    class Writable(Protocol):
        """Protocol for writable objects."""

        def write(self, data: str) -> None:
            ...

    class ReadWritable(Readable, Writable, Protocol):
        """Combined protocol."""
        pass

    class FileHandle:
        """Implements both protocols."""

        def __init__(self):
            self.content = ""

        def read(self) -> str:
            return self.content

        def write(self, data: str) -> None:
            self.content = data

    def copy_data(source: Readable, dest: Writable) -> None:
        """Copy from readable to writable."""
        data = source.read()
        dest.write(data)

    def mirror(rw: ReadWritable) -> str:
        """Use object that is both readable and writable."""
        data = rw.read()
        rw.write(data + data)
        return rw.read()

    handle = FileHandle()
    handle.write("test")
    result = mirror(handle)

    return {
        "result": result,
        "note": "Protocols can be composed via inheritance",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 30: Protocols")
    print("=" * 60)

    print("\n1. Basic Protocol:")
    basic = demonstrate_basic_protocol()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Runtime Checkable:")
    runtime = demonstrate_runtime_checkable()
    for key, value in runtime.items():
        print(f"   {key}: {value}")

    print("\n3. Protocol vs ABC:")
    comparison = demonstrate_protocol_vs_abc()
    for key, value in comparison.items():
        print(f"   {key}: {value}")

    print("\n4. Multiple Methods:")
    multiple = demonstrate_multiple_methods()
    for key, value in multiple.items():
        print(f"   {key}: {value}")

    print("\n5. Generic Protocol:")
    generic = demonstrate_generic_protocol()
    for key, value in generic.items():
        print(f"   {key}: {value}")

    print("\n6. Iterator Protocol:")
    iterator = demonstrate_iterator_protocol()
    for key, value in iterator.items():
        print(f"   {key}: {value}")

    print("\n7. Comparable Protocol:")
    comparable = demonstrate_comparable_protocol()
    for key, value in comparable.items():
        print(f"   {key}: {value}")

    print("\n8. Context Manager Protocol:")
    context = demonstrate_context_manager_protocol()
    for key, value in context.items():
        print(f"   {key}: {value}")

    print("\n9. Sized Protocol:")
    sized = demonstrate_sized_protocol()
    for key, value in sized.items():
        print(f"   {key}: {value}")

    print("\n10. Protocol Composition:")
    composition = demonstrate_protocol_composition()
    for key, value in composition.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
