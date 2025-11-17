#!/usr/bin/env python3
"""Program 16: Polymorphism - Master polymorphic behavior in Python."""

from typing import List, Any, Protocol
from abc import ABC, abstractmethod


def demonstrate_duck_typing() -> dict[str, Any]:
    """Demonstrate duck typing - 'If it walks like a duck...'"""

    class Dog:
        def speak(self) -> str:
            return "Woof!"

    class Cat:
        def speak(self) -> str:
            return "Meow!"

    class Robot:
        def speak(self) -> str:
            return "Beep boop!"

    # No common base class, but all have speak() method
    def make_it_speak(thing) -> str:
        return thing.speak()

    animals = [Dog(), Cat(), Robot()]
    sounds = [make_it_speak(animal) for animal in animals]

    return {
        "dog_sound": sounds[0],
        "cat_sound": sounds[1],
        "robot_sound": sounds[2],
        "note": "Duck typing: no inheritance needed, just matching interface",
    }


def demonstrate_method_overriding() -> dict[str, Any]:
    """Demonstrate method overriding."""

    class Animal:
        def make_sound(self) -> str:
            return "Generic animal sound"

        def move(self) -> str:
            return "Moving"

    class Dog(Animal):
        def make_sound(self) -> str:
            return "Woof!"

        def move(self) -> str:
            return "Running on four legs"

    class Bird(Animal):
        def make_sound(self) -> str:
            return "Chirp!"

        def move(self) -> str:
            return "Flying with wings"

    # Polymorphic behavior
    animals: List[Animal] = [Animal(), Dog(), Bird()]
    sounds = [animal.make_sound() for animal in animals]
    movements = [animal.move() for animal in animals]

    return {
        "generic_sound": sounds[0],
        "dog_sound": sounds[1],
        "bird_sound": sounds[2],
        "dog_move": movements[1],
        "bird_move": movements[2],
    }


def demonstrate_operator_overloading() -> dict[str, Any]:
    """Demonstrate operator overloading for polymorphism."""

    class Vector:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def __add__(self, other: 'Vector') -> 'Vector':
            return Vector(self.x + other.x, self.y + other.y)

        def __sub__(self, other: 'Vector') -> 'Vector':
            return Vector(self.x - other.x, self.y - other.y)

        def __mul__(self, scalar: float) -> 'Vector':
            return Vector(self.x * scalar, self.y * scalar)

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Vector):
                return NotImplemented
            return self.x == other.x and self.y == other.y

        def __str__(self) -> str:
            return f"Vector({self.x}, {self.y})"

        def __repr__(self) -> str:
            return f"Vector(x={self.x}, y={self.y})"

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)

    v_add = v1 + v2
    v_sub = v2 - v1
    v_mul = v1 * 3
    v_eq = v1 == Vector(1, 2)

    return {
        "v1": str(v1),
        "v2": str(v2),
        "addition": str(v_add),
        "subtraction": str(v_sub),
        "multiplication": str(v_mul),
        "equality": v_eq,
    }


def demonstrate_protocol_polymorphism() -> dict[str, Any]:
    """Demonstrate Protocol-based polymorphism (Python 3.8+)."""

    class Drawable(Protocol):
        """Protocol defining drawable interface."""
        def draw(self) -> str:
            ...

    class Circle:
        def __init__(self, radius: float):
            self.radius = radius

        def draw(self) -> str:
            return f"Drawing circle with radius {self.radius}"

    class Square:
        def __init__(self, side: float):
            self.side = side

        def draw(self) -> str:
            return f"Drawing square with side {self.side}"

    class Triangle:
        def __init__(self, base: float, height: float):
            self.base = base
            self.height = height

        def draw(self) -> str:
            return f"Drawing triangle with base {self.base} and height {self.height}"

    # Works with any object that has draw() method
    def render(shape: Drawable) -> str:
        return shape.draw()

    shapes = [Circle(5), Square(4), Triangle(3, 6)]
    drawings = [render(shape) for shape in shapes]

    return {
        "circle": drawings[0],
        "square": drawings[1],
        "triangle": drawings[2],
        "note": "Protocol allows structural subtyping",
    }


def demonstrate_abstract_polymorphism() -> dict[str, Any]:
    """Demonstrate polymorphism with abstract base classes."""

    class PaymentMethod(ABC):
        """Abstract payment method."""

        @abstractmethod
        def process_payment(self, amount: float) -> str:
            pass

        @abstractmethod
        def get_fee(self, amount: float) -> float:
            pass

    class CreditCard(PaymentMethod):
        def process_payment(self, amount: float) -> str:
            return f"Processing ${amount:.2f} via Credit Card"

        def get_fee(self, amount: float) -> float:
            return amount * 0.03  # 3% fee

    class PayPal(PaymentMethod):
        def process_payment(self, amount: float) -> str:
            return f"Processing ${amount:.2f} via PayPal"

        def get_fee(self, amount: float) -> float:
            return amount * 0.025  # 2.5% fee

    class BankTransfer(PaymentMethod):
        def process_payment(self, amount: float) -> str:
            return f"Processing ${amount:.2f} via Bank Transfer"

        def get_fee(self, amount: float) -> float:
            return 1.0  # Flat fee

    def process_transaction(payment: PaymentMethod, amount: float) -> dict:
        fee = payment.get_fee(amount)
        total = amount + fee
        message = payment.process_payment(total)
        return {"message": message, "fee": fee, "total": total}

    methods = [CreditCard(), PayPal(), BankTransfer()]
    transactions = [process_transaction(method, 100) for method in methods]

    return {
        "credit_card": transactions[0],
        "paypal": transactions[1],
        "bank_transfer": transactions[2],
    }


def demonstrate_function_polymorphism() -> dict[str, Any]:
    """Demonstrate polymorphism with built-in functions."""

    # len() works with different types
    string_len = len("Hello")
    list_len = len([1, 2, 3, 4, 5])
    dict_len = len({"a": 1, "b": 2})

    # Custom class supporting len()
    class Playlist:
        def __init__(self, songs: List[str]):
            self.songs = songs

        def __len__(self) -> int:
            return len(self.songs)

    playlist = Playlist(["Song1", "Song2", "Song3"])
    playlist_len = len(playlist)

    # iter() and next() with different iterables
    list_iter = iter([1, 2, 3])
    first = next(list_iter)

    return {
        "string_len": string_len,
        "list_len": list_len,
        "dict_len": dict_len,
        "playlist_len": playlist_len,
        "iter_first": first,
        "note": "Built-in functions use polymorphism via magic methods",
    }


def demonstrate_interface_segregation() -> dict[str, Any]:
    """Demonstrate interface segregation principle."""

    class Printer(ABC):
        @abstractmethod
        def print_document(self, doc: str) -> str:
            pass

    class Scanner(ABC):
        @abstractmethod
        def scan_document(self) -> str:
            pass

    class Fax(ABC):
        @abstractmethod
        def fax_document(self, doc: str, number: str) -> str:
            pass

    # Simple printer only implements printing
    class SimplePrinter(Printer):
        def print_document(self, doc: str) -> str:
            return f"Printing: {doc}"

    # Multi-function device implements all interfaces
    class MultiFunctionDevice(Printer, Scanner, Fax):
        def print_document(self, doc: str) -> str:
            return f"MFD Printing: {doc}"

        def scan_document(self) -> str:
            return "MFD Scanning document"

        def fax_document(self, doc: str, number: str) -> str:
            return f"MFD Faxing {doc} to {number}"

    simple = SimplePrinter()
    mfd = MultiFunctionDevice()

    return {
        "simple_print": simple.print_document("Test"),
        "mfd_print": mfd.print_document("Test"),
        "mfd_scan": mfd.scan_document(),
        "mfd_fax": mfd.fax_document("Test", "555-1234"),
        "simple_can_scan": isinstance(simple, Scanner),
        "mfd_can_scan": isinstance(mfd, Scanner),
    }


def demonstrate_liskov_substitution() -> dict[str, Any]:
    """Demonstrate Liskov Substitution Principle."""

    class Bird:
        def move(self) -> str:
            return "Moving"

    class FlyingBird(Bird):
        def move(self) -> str:
            return "Flying"

        def fly(self) -> str:
            return "Soaring through the sky"

    class WalkingBird(Bird):
        def move(self) -> str:
            return "Walking"

        def walk(self) -> str:
            return "Walking on ground"

    # Good: Any Bird can be substituted
    def make_bird_move(bird: Bird) -> str:
        return bird.move()

    sparrow = FlyingBird()
    penguin = WalkingBird()

    # Both work with the same interface
    results = [make_bird_move(sparrow), make_bird_move(penguin)]

    return {
        "sparrow_move": results[0],
        "penguin_move": results[1],
        "sparrow_fly": sparrow.fly(),
        "penguin_walk": penguin.walk(),
        "note": "Child classes can replace parent without breaking code",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 16: Polymorphism")
    print("=" * 60)

    print("\n1. Duck Typing:")
    duck = demonstrate_duck_typing()
    for key, value in duck.items():
        print(f"   {key}: {value}")

    print("\n2. Method Overriding:")
    overriding = demonstrate_method_overriding()
    for key, value in overriding.items():
        print(f"   {key}: {value}")

    print("\n3. Operator Overloading:")
    operators = demonstrate_operator_overloading()
    for key, value in operators.items():
        print(f"   {key}: {value}")

    print("\n4. Protocol Polymorphism:")
    protocol = demonstrate_protocol_polymorphism()
    for key, value in protocol.items():
        print(f"   {key}: {value}")

    print("\n5. Abstract Polymorphism:")
    abstract = demonstrate_abstract_polymorphism()
    for key, value in abstract.items():
        print(f"   {key}: {value}")

    print("\n6. Function Polymorphism:")
    functions = demonstrate_function_polymorphism()
    for key, value in functions.items():
        print(f"   {key}: {value}")

    print("\n7. Interface Segregation:")
    segregation = demonstrate_interface_segregation()
    for key, value in segregation.items():
        print(f"   {key}: {value}")

    print("\n8. Liskov Substitution:")
    liskov = demonstrate_liskov_substitution()
    for key, value in liskov.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
