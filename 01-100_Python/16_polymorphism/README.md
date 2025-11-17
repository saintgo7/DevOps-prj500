# 16_polymorphism

## Description

Master polymorphism - the ability of different objects to respond to the same method call in different ways. Learn duck typing, method overriding, operator overloading, protocols, abstract polymorphism, and SOLID principles (Liskov Substitution, Interface Segregation).

This is Program #16 in the 500 Programs Collection.

## Learning Objectives

- Understand duck typing (Python's implicit polymorphism)
- Implement method overriding
- Use operator overloading for custom behavior
- Work with Protocol classes (structural subtyping)
- Apply abstract polymorphism with ABC
- Understand function polymorphism
- Apply SOLID principles (LSP, ISP)
- Build flexible, extensible code

## Features

- Duck typing demonstrations
- Method overriding patterns
- Operator overloading (__add__, __sub__, __mul__, __eq__, etc.)
- Protocol-based polymorphism (Python 3.8+)
- Abstract base class polymorphism
- Function polymorphism (len, iter, etc.)
- Interface Segregation Principle
- Liskov Substitution Principle

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Duck Typing

```python
# "If it walks like a duck and quacks like a duck, it's a duck"

class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:
    def speak(self):
        return "Beep boop!"

# No common base class needed!
def make_it_speak(thing):
    return thing.speak()

# All work with same function
animals = [Dog(), Cat(), Robot()]
for animal in animals:
    print(make_it_speak(animal))
```

### 2. Method Overriding

```python
class Animal:
    def make_sound(self):
        return "Generic sound"

    def move(self):
        return "Moving"

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

    def move(self):
        return "Running on four legs"

# Polymorphic behavior
animals = [Animal(), Dog()]
for animal in animals:
    print(animal.make_sound())  # Different output
```

### 3. Operator Overloading

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """v1 + v2"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """v1 - v2"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """v * 3"""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        """v1 == v2"""
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2  # Calls __add__
v4 = v1 * 3   # Calls __mul__
```

### 4. Protocol Polymorphism

```python
from typing import Protocol

class Drawable(Protocol):
    """Protocol defining drawable interface."""
    def draw(self) -> str:
        ...

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def draw(self):
        return f"Drawing circle with radius {self.radius}"

class Square:
    def __init__(self, side):
        self.side = side

    def draw(self):
        return f"Drawing square with side {self.side}"

def render(shape: Drawable):
    """Works with any object that has draw() method."""
    return shape.draw()

# No explicit inheritance needed
shapes = [Circle(5), Square(4)]
for shape in shapes:
    print(render(shape))
```

### 5. Abstract Polymorphism

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

class CreditCard(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount} via Credit Card"

class PayPal(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount} via PayPal"

def process_transaction(payment: PaymentMethod, amount: float):
    """Works with any PaymentMethod."""
    return payment.process_payment(amount)

methods = [CreditCard(), PayPal()]
for method in methods:
    print(process_transaction(method, 100))
```

### 6. Function Polymorphism

```python
# Built-in functions work polymorphically

len("hello")    # 5 (string)
len([1, 2, 3])  # 3 (list)
len({"a": 1})   # 1 (dict)

# Custom class
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __len__(self):
        return len(self.songs)

playlist = Playlist(["Song1", "Song2", "Song3"])
len(playlist)  # 3
```

### 7. Interface Segregation Principle

```python
from abc import ABC, abstractmethod

# Split into small, focused interfaces

class Printer(ABC):
    @abstractmethod
    def print_document(self, doc):
        pass

class Scanner(ABC):
    @abstractmethod
    def scan_document(self):
        pass

# Simple printer only implements printing
class SimplePrinter(Printer):
    def print_document(self, doc):
        return f"Printing: {doc}"

# Multi-function device implements both
class MultiFunctionDevice(Printer, Scanner):
    def print_document(self, doc):
        return f"MFD Printing: {doc}"

    def scan_document(self):
        return "MFD Scanning"
```

### 8. Liskov Substitution Principle

```python
# Child classes should be substitutable for parent

class Bird:
    def move(self):
        return "Moving"

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class WalkingBird(Bird):
    def move(self):
        return "Walking"

def make_bird_move(bird: Bird):
    """Works with any Bird subclass."""
    return bird.move()

# Both work correctly
sparrow = FlyingBird()
penguin = WalkingBird()
make_bird_move(sparrow)  # "Flying"
make_bird_move(penguin)  # "Walking"
```

## Best Practices

1. **Use Duck Typing (Pythonic)**
2. **Define Clear Interfaces**
3. **Keep Methods Consistent**
4. **Use Protocols for Structural Typing**
5. **Follow SOLID Principles**
6. **Document Expected Behavior**

## Testing

```bash
python src/main.py
```

---

**Program**: 16 of 500
**Difficulty**: ⭐⭐⭐ Intermediate/Advanced
**Category**: Object-Oriented Programming
**Estimated Time**: 60-75 minutes

[← Previous (15)](../15_inheritance/) | [Back to Index](../../docs/INDEX.md) | [Next (17) →](../17_modules/)
