#!/usr/bin/env python3
"""Program 31: Advanced Dataclasses - Master dataclass features and customization."""

from dataclasses import dataclass, field, asdict, astuple, replace, fields
from dataclasses import FrozenInstanceError, InitVar
from typing import Any, List, ClassVar
import json


def demonstrate_basic_dataclass() -> dict[str, Any]:
    """Demonstrate basic dataclass usage."""

    @dataclass
    class Person:
        """Simple dataclass."""
        name: str
        age: int
        email: str

    person = Person("Alice", 30, "alice@example.com")

    # Auto-generated methods
    person2 = Person("Alice", 30, "alice@example.com")
    person3 = Person("Bob", 25, "bob@example.com")

    return {
        "repr": repr(person),
        "equal": person == person2,
        "not_equal": person != person3,
        "note": "dataclass auto-generates __init__, __repr__, __eq__",
    }


def demonstrate_default_values() -> dict[str, Any]:
    """Demonstrate default values and field()."""

    @dataclass
    class Product:
        """Product with default values."""
        name: str
        price: float
        quantity: int = 1
        tags: List[str] = field(default_factory=list)
        discount: float = 0.0

    # With defaults
    product1 = Product("Widget", 19.99)

    # Override defaults
    product2 = Product("Gadget", 29.99, quantity=5, tags=["new", "sale"])

    return {
        "product1": asdict(product1),
        "product2": asdict(product2),
        "note": "Use field(default_factory=...) for mutable defaults",
    }


def demonstrate_post_init() -> dict[str, Any]:
    """Demonstrate __post_init__ for custom initialization."""

    @dataclass
    class Rectangle:
        """Rectangle with computed area."""
        width: float
        height: float
        area: float = field(init=False)

        def __post_init__(self):
            """Compute area after initialization."""
            self.area = self.width * self.height

    @dataclass
    class Person:
        """Person with full name."""
        first_name: str
        last_name: str
        full_name: str = field(init=False)

        def __post_init__(self):
            """Compute full name."""
            self.full_name = f"{self.first_name} {self.last_name}"

    rect = Rectangle(5.0, 3.0)
    person = Person("John", "Doe")

    return {
        "rectangle_area": rect.area,
        "person_full_name": person.full_name,
        "note": "__post_init__ called after __init__ for custom logic",
    }


def demonstrate_frozen() -> dict[str, Any]:
    """Demonstrate frozen (immutable) dataclasses."""

    @dataclass(frozen=True)
    class Point:
        """Immutable point."""
        x: float
        y: float

    point = Point(3.0, 4.0)

    # Try to modify (will raise FrozenInstanceError)
    error_raised = False
    try:
        point.x = 5.0  # type: ignore
    except FrozenInstanceError:
        error_raised = True

    # Can be used as dict key
    point_dict = {point: "origin"}

    return {
        "point": asdict(point),
        "immutable": error_raised,
        "hashable": hash(point) is not None,
        "note": "frozen=True makes dataclass immutable and hashable",
    }


def demonstrate_ordering() -> dict[str, Any]:
    """Demonstrate ordering with order=True."""

    @dataclass(order=True)
    class Score:
        """Score that can be compared."""
        value: int
        player: str = field(compare=False)

    scores = [
        Score(85, "Alice"),
        Score(92, "Bob"),
        Score(78, "Charlie"),
        Score(95, "David"),
    ]

    sorted_scores = sorted(scores)

    return {
        "original": [s.value for s in scores],
        "sorted": [s.value for s in sorted_scores],
        "max": max(scores).value,
        "note": "order=True generates comparison methods",
    }


def demonstrate_field_options() -> dict[str, Any]:
    """Demonstrate field() options."""

    @dataclass
    class Config:
        """Configuration with field options."""
        # Regular field
        name: str

        # Field with default
        debug: bool = False

        # Field excluded from init
        timestamp: float = field(init=False, default=0.0)

        # Field excluded from repr
        secret: str = field(repr=False, default="hidden")

        # Field excluded from comparison
        metadata: dict = field(compare=False, default_factory=dict)

        # Field with metadata
        version: str = field(metadata={"format": "semver"}, default="1.0.0")

    config = Config("MyApp")
    config2 = Config("MyApp", metadata={"key": "value"})

    return {
        "repr": repr(config),
        "equal": config == config2,
        "field_metadata": fields(Config)[5].metadata,
        "note": "field() has init, repr, compare, hash, metadata options",
    }


def demonstrate_init_var() -> dict[str, Any]:
    """Demonstrate InitVar for init-only variables."""

    @dataclass
    class DatabaseConnection:
        """Database connection with initialization logic."""
        host: str
        port: int
        database: str = field(init=False)
        connection_string: str = field(init=False)
        timeout: InitVar[int] = 30

        def __post_init__(self, timeout: int):
            """Build connection string using InitVar."""
            self.database = "mydb"
            self.connection_string = (
                f"{self.host}:{self.port}/{self.database}?timeout={timeout}"
            )

    conn = DatabaseConnection("localhost", 5432, timeout=60)

    return {
        "connection_string": conn.connection_string,
        "has_timeout_attr": hasattr(conn, 'timeout'),
        "note": "InitVar passes values to __post_init__ without storing",
    }


def demonstrate_class_variables() -> dict[str, Any]:
    """Demonstrate ClassVar in dataclasses."""

    @dataclass
    class Counter:
        """Counter with class-level count."""
        name: str
        count: ClassVar[int] = 0

        def __post_init__(self):
            Counter.count += 1

    c1 = Counter("first")
    c2 = Counter("second")
    c3 = Counter("third")

    return {
        "instance_count": Counter.count,
        "c1_has_count": hasattr(c1, 'count'),
        "class_var": Counter.count,
        "note": "ClassVar not included in __init__ or instance attributes",
    }


def demonstrate_helper_functions() -> dict[str, Any]:
    """Demonstrate dataclass helper functions."""

    @dataclass
    class Book:
        """Book dataclass."""
        title: str
        author: str
        year: int
        isbn: str

    book = Book("Python Tricks", "Dan Bader", 2017, "978-1775093305")

    # asdict - convert to dictionary
    book_dict = asdict(book)

    # astuple - convert to tuple
    book_tuple = astuple(book)

    # replace - create modified copy
    updated_book = replace(book, year=2018)

    # fields - get field information
    field_names = [f.name for f in fields(Book)]

    return {
        "as_dict": book_dict,
        "as_tuple": book_tuple,
        "replaced_year": updated_book.year,
        "field_names": field_names,
        "note": "asdict, astuple, replace, fields are helper functions",
    }


def demonstrate_inheritance() -> dict[str, Any]:
    """Demonstrate dataclass inheritance."""

    @dataclass
    class Animal:
        """Base animal class."""
        name: str
        age: int

    @dataclass
    class Dog(Animal):
        """Dog extends Animal."""
        breed: str
        is_trained: bool = False

    @dataclass
    class Cat(Animal):
        """Cat extends Animal."""
        indoor: bool = True
        lives: int = 9

    dog = Dog("Buddy", 3, "Labrador", is_trained=True)
    cat = Cat("Whiskers", 2)

    return {
        "dog": asdict(dog),
        "cat": asdict(cat),
        "dog_name": dog.name,
        "cat_lives": cat.lives,
        "note": "Dataclasses support inheritance",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 31: Advanced Dataclasses")
    print("=" * 60)

    print("\n1. Basic Dataclass:")
    basic = demonstrate_basic_dataclass()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Default Values:")
    defaults = demonstrate_default_values()
    for key, value in defaults.items():
        print(f"   {key}: {value}")

    print("\n3. Post Init:")
    post_init = demonstrate_post_init()
    for key, value in post_init.items():
        print(f"   {key}: {value}")

    print("\n4. Frozen (Immutable):")
    frozen = demonstrate_frozen()
    for key, value in frozen.items():
        print(f"   {key}: {value}")

    print("\n5. Ordering:")
    ordering = demonstrate_ordering()
    for key, value in ordering.items():
        print(f"   {key}: {value}")

    print("\n6. Field Options:")
    field_opts = demonstrate_field_options()
    for key, value in field_opts.items():
        print(f"   {key}: {value}")

    print("\n7. InitVar:")
    init_var = demonstrate_init_var()
    for key, value in init_var.items():
        print(f"   {key}: {value}")

    print("\n8. ClassVar:")
    class_var = demonstrate_class_variables()
    for key, value in class_var.items():
        print(f"   {key}: {value}")

    print("\n9. Helper Functions:")
    helpers = demonstrate_helper_functions()
    for key, value in helpers.items():
        print(f"   {key}: {value}")

    print("\n10. Inheritance:")
    inheritance = demonstrate_inheritance()
    for key, value in inheritance.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
