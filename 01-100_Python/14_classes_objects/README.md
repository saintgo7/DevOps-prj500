# 14_classes_objects

## Description

Master Object-Oriented Programming (OOP) in Python with comprehensive demonstrations of classes, objects, methods, attributes, properties, special methods, and advanced OOP concepts. Classes are fundamental to organizing code and modeling real-world entities.

This is Program #14 in the 500 Programs Collection.

## Learning Objectives

- Define classes and create objects (instances)
- Understand class vs instance attributes
- Use instance, class, and static methods
- Implement special (magic/dunder) methods
- Create properties with getters and setters
- Understand encapsulation and private attributes
- Use composition over inheritance
- Work with dataclasses (Python 3.7+)

## Features

- Basic class definitions and instantiation
- Class and instance attributes
- Instance, class, and static methods
- Special methods (__init__, __str__, __repr__, __len__, __eq__, etc.)
- Properties and property decorators
- Private attributes and name mangling
- Class composition pattern
- Dataclasses for data-focused classes

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Class Definition

```python
class Person:
    """A simple Person class."""

    def __init__(self, name: str, age: int):
        self.name = name  # Instance attribute
        self.age = age

    def greet(self) -> str:
        """Instance method."""
        return f"Hello, I'm {self.name}"

    def have_birthday(self) -> None:
        """Modify instance attribute."""
        self.age += 1

# Create instances
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# Access attributes
print(person1.name)  # Alice

# Call methods
greeting = person1.greet()
person1.have_birthday()
```

### 2. Class vs Instance Attributes

```python
class Counter:
    # Class attribute (shared by all instances)
    total_count = 0

    def __init__(self, name: str):
        self.name = name  # Instance attribute (unique to each instance)
        self.count = 0
        Counter.total_count += 1

    def increment(self):
        self.count += 1

c1 = Counter("Counter1")
c2 = Counter("Counter2")

c1.increment()  # Affects only c1.count
print(c1.count)  # 1
print(c2.count)  # 0
print(Counter.total_count)  # 2 (shared)
```

### 3. Instance, Class, and Static Methods

```python
class Calculator:
    precision = 2  # Class attribute

    def __init__(self, name: str):
        self.name = name

    # Instance method (has access to self)
    def add(self, a: float, b: float) -> float:
        """Instance method can access instance and class attributes."""
        result = a + b
        return round(result, self.precision)

    # Class method (has access to cls)
    @classmethod
    def set_precision(cls, precision: int) -> None:
        """Class method modifies class attribute."""
        cls.precision = precision

    @classmethod
    def create_scientific(cls) -> 'Calculator':
        """Factory method."""
        calc = cls("Scientific")
        calc.precision = 4
        return calc

    # Static method (no access to self or cls)
    @staticmethod
    def is_even(num: int) -> bool:
        """Static method - utility function."""
        return num % 2 == 0

# Usage
calc = Calculator("Basic")
calc.add(10.5, 20.3)  # Instance method

Calculator.set_precision(3)  # Class method

Calculator.is_even(4)  # Static method
```

### 4. Special Methods (Magic Methods)

```python
class Book:
    def __init__(self, title: str, pages: int):
        self.title = title
        self.pages = pages

    def __str__(self) -> str:
        """String for users (str())."""
        return f"'{self.title}' ({self.pages} pages)"

    def __repr__(self) -> str:
        """String for developers (repr())."""
        return f"Book(title='{self.title}', pages={self.pages})"

    def __len__(self) -> int:
        """Support len() function."""
        return self.pages

    def __eq__(self, other) -> bool:
        """Support == comparison."""
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title and self.pages == other.pages

    def __lt__(self, other: 'Book') -> bool:
        """Support < comparison."""
        return self.pages < other.pages

    def __add__(self, other: 'Book') -> int:
        """Support + operator."""
        return self.pages + other.pages

book1 = Book("Python Basics", 300)
book2 = Book("Advanced Python", 500)

print(str(book1))  # Calls __str__
print(repr(book1))  # Calls __repr__
print(len(book1))  # Calls __len__
print(book1 == book2)  # Calls __eq__
print(book1 < book2)  # Calls __lt__
print(book1 + book2)  # Calls __add__
```

### 5. Properties

```python
class Temperature:
    def __init__(self, celsius: float = 0):
        self._celsius = celsius  # "Private" attribute

    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set temperature with validation."""
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set temperature via Fahrenheit."""
        self.celsius = (value - 32) * 5/9

temp = Temperature(0)
temp.celsius = 100  # Calls setter
print(temp.fahrenheit)  # Calls getter
temp.fahrenheit = 212  # Calls setter
print(temp.celsius)  # 100.0
```

### 6. Private Attributes

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self.__balance = balance  # Name mangling (private)

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        return self.__balance

account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.get_balance())  # 1500

# Cannot access directly
# print(account.__balance)  # AttributeError

# But can access via name mangling (not recommended)
print(account._BankAccount__balance)  # 1500
```

### 7. Composition

```python
class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def start(self) -> str:
        return f"Engine started ({self.horsepower} HP)"

class Car:
    """Car uses composition (has-an Engine)."""

    def __init__(self, brand: str, horsepower: int):
        self.brand = brand
        self.engine = Engine(horsepower)  # Composition

    def start(self) -> str:
        return f"{self.brand}: {self.engine.start()}"

car = Car("Toyota", 150)
print(car.start())  # Toyota: Engine started (150 HP)
```

### 8. Dataclasses

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    """Student dataclass with auto-generated methods."""
    name: str
    age: int
    grades: List[int] = field(default_factory=list)

    def average_grade(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

# Auto-generated __init__, __repr__, __eq__, etc.
student = Student("Alice", 20, [85, 90, 88])
print(student)  # Student(name='Alice', age=20, grades=[85, 90, 88])
print(student.average_grade())  # 87.66...
```

## Best Practices

1. **Use __init__ for Initialization**
   ```python
   class Person:
       def __init__(self, name, age):
           self.name = name
           self.age = age
   ```

2. **Use Properties for Computed Attributes**
   ```python
   @property
   def full_name(self):
       return f"{self.first_name} {self.last_name}"
   ```

3. **Prefer Composition Over Inheritance**
   ```python
   # Good - composition
   class Car:
       def __init__(self):
           self.engine = Engine()

   # Sometimes necessary but use carefully
   class SportsCar(Car):
       pass
   ```

4. **Use @classmethod for Alternative Constructors**
   ```python
   @classmethod
   def from_string(cls, data_string):
       # Parse and create instance
       return cls(...)
   ```

5. **Implement __repr__ for Debugging**
   ```python
   def __repr__(self):
       return f"Person(name='{self.name}', age={self.age})"
   ```

6. **Use Dataclasses for Data-Heavy Classes**
   ```python
   from dataclasses import dataclass

   @dataclass
   class Point:
       x: float
       y: float
   ```

## Common Special Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `__init__` | Constructor | `obj = Class()` |
| `__str__` | User-friendly string | `str(obj)` |
| `__repr__` | Developer string | `repr(obj)` |
| `__len__` | Length | `len(obj)` |
| `__eq__` | Equality | `obj1 == obj2` |
| `__lt__` | Less than | `obj1 < obj2` |
| `__add__` | Addition | `obj1 + obj2` |
| `__getitem__` | Indexing | `obj[key]` |
| `__call__` | Callable | `obj()` |

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

---

**Program**: 14 of 500
**Difficulty**: ⭐⭐ Intermediate
**Category**: Object-Oriented Programming
**Estimated Time**: 60-90 minutes

[← Previous (13)](../13_exception_handling/) | [Back to Index](../../docs/INDEX.md) | [Next (15) →](../15_inheritance/)
