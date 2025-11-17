#!/usr/bin/env python3
"""Program 14: Classes and Objects - Master Object-Oriented Programming basics."""

from typing import List, Optional, Any


def demonstrate_basic_class() -> dict[str, Any]:
    """Demonstrate basic class definition and usage."""
    class Person:
        """A simple Person class."""

        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def greet(self) -> str:
            return f"Hello, I'm {self.name} and I'm {self.age} years old."

        def have_birthday(self) -> None:
            self.age += 1

    # Create instances
    person1 = Person("Alice", 25)
    person2 = Person("Bob", 30)

    # Use methods
    greeting1 = person1.greet()
    person1.have_birthday()
    greeting_after = person1.greet()

    return {
        "person1_name": person1.name,
        "person2_name": person2.name,
        "greeting_before": greeting1,
        "greeting_after": greeting_after,
        "person1_age": person1.age,
    }


def demonstrate_class_attributes() -> dict[str, Any]:
    """Demonstrate class vs instance attributes."""
    class Counter:
        """Counter with both class and instance attributes."""

        # Class attribute (shared by all instances)
        total_count = 0

        def __init__(self, name: str):
            self.name = name
            # Instance attribute
            self.count = 0
            Counter.total_count += 1

        def increment(self) -> None:
            self.count += 1

    # Create instances
    c1 = Counter("Counter1")
    c2 = Counter("Counter2")

    c1.increment()
    c1.increment()
    c2.increment()

    return {
        "c1_count": c1.count,
        "c2_count": c2.count,
        "total_count": Counter.total_count,
        "shared_attribute": c1.total_count == c2.total_count,
    }


def demonstrate_methods() -> dict[str, Any]:
    """Demonstrate different types of methods."""
    class Calculator:
        """Calculator with instance, class, and static methods."""

        precision = 2

        def __init__(self, name: str):
            self.name = name
            self.history: List[str] = []

        # Instance method
        def add(self, a: float, b: float) -> float:
            result = round(a + b, self.precision)
            self.history.append(f"{a} + {b} = {result}")
            return result

        # Class method
        @classmethod
        def set_precision(cls, precision: int) -> None:
            cls.precision = precision

        @classmethod
        def create_scientific(cls) -> 'Calculator':
            calc = cls("Scientific")
            calc.precision = 4
            return calc

        # Static method
        @staticmethod
        def is_even(num: int) -> bool:
            return num % 2 == 0

    # Use different methods
    calc = Calculator("Basic")
    result1 = calc.add(10.5, 20.3)

    # Class method
    Calculator.set_precision(3)
    calc2 = Calculator("Advanced")
    result2 = calc2.add(10.5, 20.3)

    # Static method
    even_check = Calculator.is_even(4)

    return {
        "instance_method": result1,
        "after_class_method": result2,
        "static_method": even_check,
        "history": calc.history,
    }


def demonstrate_special_methods() -> dict[str, Any]:
    """Demonstrate special (magic/dunder) methods."""
    class Book:
        """Book class with special methods."""

        def __init__(self, title: str, pages: int):
            self.title = title
            self.pages = pages

        def __str__(self) -> str:
            """String representation for users."""
            return f"'{self.title}' ({self.pages} pages)"

        def __repr__(self) -> str:
            """String representation for developers."""
            return f"Book(title='{self.title}', pages={self.pages})"

        def __len__(self) -> int:
            """Support len() function."""
            return self.pages

        def __eq__(self, other: object) -> bool:
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
    book3 = Book("Python Basics", 300)

    return {
        "str": str(book1),
        "repr": repr(book1),
        "len": len(book1),
        "equality": book1 == book3,
        "not_equal": book1 == book2,
        "comparison": book1 < book2,
        "addition": book1 + book2,
    }


def demonstrate_properties() -> dict[str, Any]:
    """Demonstrate properties and encapsulation."""
    class Temperature:
        """Temperature class with property decorators."""

        def __init__(self, celsius: float = 0):
            self._celsius = celsius

        @property
        def celsius(self) -> float:
            """Get temperature in Celsius."""
            return self._celsius

        @celsius.setter
        def celsius(self, value: float) -> None:
            """Set temperature in Celsius."""
            if value < -273.15:
                raise ValueError("Temperature below absolute zero!")
            self._celsius = value

        @property
        def fahrenheit(self) -> float:
            """Get temperature in Fahrenheit."""
            return (self._celsius * 9/5) + 32

        @fahrenheit.setter
        def fahrenheit(self, value: float) -> None:
            """Set temperature in Fahrenheit."""
            self.celsius = (value - 32) * 5/9

    temp = Temperature(0)
    initial_c = temp.celsius
    initial_f = temp.fahrenheit

    temp.celsius = 100
    boiling_c = temp.celsius
    boiling_f = temp.fahrenheit

    temp.fahrenheit = 32
    freezing_c = temp.celsius

    # Test validation
    error_caught = False
    try:
        temp.celsius = -300
    except ValueError:
        error_caught = True

    return {
        "initial_celsius": initial_c,
        "initial_fahrenheit": initial_f,
        "boiling_celsius": boiling_c,
        "boiling_fahrenheit": boiling_f,
        "freezing_celsius": freezing_c,
        "validation_works": error_caught,
    }


def demonstrate_private_attributes() -> dict[str, Any]:
    """Demonstrate private attributes and name mangling."""
    class BankAccount:
        """Bank account with private balance."""

        def __init__(self, owner: str, initial_balance: float = 0):
            self.owner = owner
            self.__balance = initial_balance  # Private attribute

        def deposit(self, amount: float) -> None:
            if amount > 0:
                self.__balance += amount

        def withdraw(self, amount: float) -> bool:
            if amount > 0 and amount <= self.__balance:
                self.__balance -= amount
                return True
            return False

        def get_balance(self) -> float:
            return self.__balance

    account = BankAccount("Alice", 1000)
    initial = account.get_balance()

    account.deposit(500)
    after_deposit = account.get_balance()

    account.withdraw(200)
    after_withdraw = account.get_balance()

    # Try to access private attribute (won't work as expected)
    direct_access = hasattr(account, "__balance")
    mangled_access = hasattr(account, "_BankAccount__balance")

    return {
        "initial_balance": initial,
        "after_deposit": after_deposit,
        "after_withdraw": after_withdraw,
        "has_private_attr": direct_access,
        "has_mangled_attr": mangled_access,
    }


def demonstrate_class_composition() -> dict[str, Any]:
    """Demonstrate composition over inheritance."""
    class Engine:
        """Engine class."""

        def __init__(self, horsepower: int):
            self.horsepower = horsepower

        def start(self) -> str:
            return f"Engine started ({self.horsepower} HP)"

    class Car:
        """Car class using composition."""

        def __init__(self, brand: str, horsepower: int):
            self.brand = brand
            self.engine = Engine(horsepower)  # Composition

        def start(self) -> str:
            return f"{self.brand}: {self.engine.start()}"

    car = Car("Toyota", 150)
    start_message = car.start()
    horsepower = car.engine.horsepower

    return {
        "car_brand": car.brand,
        "engine_hp": horsepower,
        "start_message": start_message,
    }


def demonstrate_dataclasses() -> dict[str, Any]:
    """Demonstrate dataclasses (Python 3.7+)."""
    from dataclasses import dataclass, field
    from typing import List

    @dataclass
    class Student:
        """Student dataclass."""
        name: str
        age: int
        grades: List[int] = field(default_factory=list)

        def average_grade(self) -> float:
            if not self.grades:
                return 0.0
            return sum(self.grades) / len(self.grades)

    # Create instances
    student1 = Student("Alice", 20, [85, 90, 88])
    student2 = Student("Bob", 21)  # Default empty grades

    student2.grades.extend([92, 88, 95])

    avg1 = student1.average_grade()
    avg2 = student2.average_grade()

    return {
        "student1": str(student1),
        "student1_avg": avg1,
        "student2_avg": avg2,
        "auto_repr": "Dataclass provides __repr__ automatically",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 14: Classes and Objects")
    print("=" * 60)

    print("\n1. Basic Class:")
    basic = demonstrate_basic_class()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Class Attributes:")
    attributes = demonstrate_class_attributes()
    for key, value in attributes.items():
        print(f"   {key}: {value}")

    print("\n3. Methods:")
    methods = demonstrate_methods()
    for key, value in methods.items():
        print(f"   {key}: {value}")

    print("\n4. Special Methods:")
    special = demonstrate_special_methods()
    for key, value in special.items():
        print(f"   {key}: {value}")

    print("\n5. Properties:")
    properties = demonstrate_properties()
    for key, value in properties.items():
        print(f"   {key}: {value}")

    print("\n6. Private Attributes:")
    private = demonstrate_private_attributes()
    for key, value in private.items():
        print(f"   {key}: {value}")

    print("\n7. Composition:")
    composition = demonstrate_class_composition()
    for key, value in composition.items():
        print(f"   {key}: {value}")

    print("\n8. Dataclasses:")
    dataclasses_demo = demonstrate_dataclasses()
    for key, value in dataclasses_demo.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
