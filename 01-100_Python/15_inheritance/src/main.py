#!/usr/bin/env python3
"""Program 15: Inheritance - Master inheritance and class hierarchies."""

from typing import List, Any, Optional
from abc import ABC, abstractmethod


def demonstrate_basic_inheritance() -> dict[str, Any]:
    """Demonstrate basic inheritance."""
    class Animal:
        """Base class for animals."""

        def __init__(self, name: str):
            self.name = name

        def speak(self) -> str:
            return "Some sound"

        def info(self) -> str:
            return f"I am {self.name}"

    class Dog(Animal):
        """Dog inherits from Animal."""

        def speak(self) -> str:
            return "Woof!"

        def fetch(self) -> str:
            return f"{self.name} is fetching the ball"

    class Cat(Animal):
        """Cat inherits from Animal."""

        def speak(self) -> str:
            return "Meow!"

        def scratch(self) -> str:
            return f"{self.name} is scratching"

    dog = Dog("Buddy")
    cat = Cat("Whiskers")

    return {
        "dog_name": dog.name,
        "dog_speak": dog.speak(),
        "dog_info": dog.info(),
        "dog_fetch": dog.fetch(),
        "cat_speak": cat.speak(),
        "cat_scratch": cat.scratch(),
        "dog_is_animal": isinstance(dog, Animal),
        "dog_is_dog": isinstance(dog, Dog),
    }


def demonstrate_super() -> dict[str, Any]:
    """Demonstrate super() function."""
    class Person:
        """Base Person class."""

        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def introduce(self) -> str:
            return f"I'm {self.name}, {self.age} years old"

    class Student(Person):
        """Student extends Person."""

        def __init__(self, name: str, age: int, student_id: str):
            super().__init__(name, age)  # Call parent __init__
            self.student_id = student_id

        def introduce(self) -> str:
            parent_intro = super().introduce()
            return f"{parent_intro}, Student ID: {self.student_id}"

    class GraduateStudent(Student):
        """GraduateStudent extends Student."""

        def __init__(self, name: str, age: int, student_id: str, research_area: str):
            super().__init__(name, age, student_id)
            self.research_area = research_area

        def introduce(self) -> str:
            parent_intro = super().introduce()
            return f"{parent_intro}, Research: {self.research_area}"

    student = Student("Alice", 20, "S12345")
    grad = GraduateStudent("Bob", 25, "G67890", "AI")

    return {
        "student_intro": student.introduce(),
        "grad_intro": grad.introduce(),
        "student_id": student.student_id,
        "research_area": grad.research_area,
    }


def demonstrate_multiple_inheritance() -> dict[str, Any]:
    """Demonstrate multiple inheritance."""
    class Flyer:
        """Mixin for flying ability."""

        def fly(self) -> str:
            return "Flying in the air"

    class Swimmer:
        """Mixin for swimming ability."""

        def swim(self) -> str:
            return "Swimming in water"

    class Duck(Flyer, Swimmer):
        """Duck can both fly and swim."""

        def __init__(self, name: str):
            self.name = name

        def quack(self) -> str:
            return f"{self.name} says quack!"

    class Penguin(Swimmer):
        """Penguin can only swim."""

        def __init__(self, name: str):
            self.name = name

    duck = Duck("Donald")
    penguin = Penguin("Pingu")

    return {
        "duck_fly": duck.fly(),
        "duck_swim": duck.swim(),
        "duck_quack": duck.quack(),
        "penguin_swim": penguin.swim(),
        "penguin_can_fly": hasattr(penguin, 'fly'),
        "mro": [cls.__name__ for cls in Duck.__mro__],
    }


def demonstrate_method_resolution_order() -> dict[str, Any]:
    """Demonstrate Method Resolution Order (MRO)."""
    class A:
        def method(self) -> str:
            return "A"

    class B(A):
        def method(self) -> str:
            return "B"

    class C(A):
        def method(self) -> str:
            return "C"

    class D(B, C):
        pass

    class E(B, C):
        def method(self) -> str:
            return f"E -> {super().method()}"

    d = D()
    e = E()

    return {
        "d_method": d.method(),
        "e_method": e.method(),
        "d_mro": [cls.__name__ for cls in D.__mro__],
        "e_mro": [cls.__name__ for cls in E.__mro__],
    }


def demonstrate_abstract_classes() -> dict[str, Any]:
    """Demonstrate abstract base classes."""
    class Shape(ABC):
        """Abstract base class for shapes."""

        def __init__(self, name: str):
            self.name = name

        @abstractmethod
        def area(self) -> float:
            """Calculate area - must be implemented by subclasses."""
            pass

        @abstractmethod
        def perimeter(self) -> float:
            """Calculate perimeter - must be implemented by subclasses."""
            pass

        def description(self) -> str:
            """Concrete method available to all subclasses."""
            return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

    class Rectangle(Shape):
        """Rectangle implementation."""

        def __init__(self, width: float, height: float):
            super().__init__("Rectangle")
            self.width = width
            self.height = height

        def area(self) -> float:
            return self.width * self.height

        def perimeter(self) -> float:
            return 2 * (self.width + self.height)

    class Circle(Shape):
        """Circle implementation."""

        def __init__(self, radius: float):
            super().__init__("Circle")
            self.radius = radius

        def area(self) -> float:
            return 3.14159 * self.radius ** 2

        def perimeter(self) -> float:
            return 2 * 3.14159 * self.radius

    rect = Rectangle(5, 3)
    circle = Circle(4)

    # Cannot instantiate abstract class
    can_instantiate_shape = False
    try:
        shape = Shape("test")
    except TypeError:
        can_instantiate_shape = False

    return {
        "rectangle_desc": rect.description(),
        "circle_desc": circle.description(),
        "can_instantiate_abc": can_instantiate_shape,
        "rect_is_shape": isinstance(rect, Shape),
    }


def demonstrate_polymorphism() -> dict[str, Any]:
    """Demonstrate polymorphism through inheritance."""
    class Vehicle:
        """Base vehicle class."""

        def __init__(self, brand: str):
            self.brand = brand

        def start(self) -> str:
            return f"{self.brand} is starting"

        def move(self) -> str:
            return "Moving"

    class Car(Vehicle):
        """Car implementation."""

        def move(self) -> str:
            return f"{self.brand} is driving on the road"

    class Boat(Vehicle):
        """Boat implementation."""

        def move(self) -> str:
            return f"{self.brand} is sailing on water"

    class Plane(Vehicle):
        """Plane implementation."""

        def move(self) -> str:
            return f"{self.brand} is flying in the sky"

    # Polymorphism in action
    vehicles: List[Vehicle] = [
        Car("Toyota"),
        Boat("Yamaha"),
        Plane("Boeing")
    ]

    movements = [vehicle.move() for vehicle in vehicles]

    return {
        "car_move": movements[0],
        "boat_move": movements[1],
        "plane_move": movements[2],
        "all_are_vehicles": all(isinstance(v, Vehicle) for v in vehicles),
    }


def demonstrate_composition_vs_inheritance() -> dict[str, Any]:
    """Demonstrate composition vs inheritance."""
    # Using inheritance
    class EmployeeWithInheritance:
        """Employee using inheritance."""

        def __init__(self, name: str):
            self.name = name

    class ManagerWithInheritance(EmployeeWithInheritance):
        """Manager inherits from Employee."""

        def __init__(self, name: str, department: str):
            super().__init__(name)
            self.department = department

    # Using composition
    class Employee:
        """Simple Employee class."""

        def __init__(self, name: str):
            self.name = name

    class Department:
        """Department class."""

        def __init__(self, name: str):
            self.name = name

    class ManagerWithComposition:
        """Manager using composition."""

        def __init__(self, name: str, department_name: str):
            self.employee = Employee(name)  # Composition
            self.department = Department(department_name)  # Composition

        @property
        def name(self) -> str:
            return self.employee.name

    manager_inherit = ManagerWithInheritance("Alice", "IT")
    manager_compose = ManagerWithComposition("Bob", "HR")

    return {
        "inheritance_name": manager_inherit.name,
        "inheritance_dept": manager_inherit.department,
        "composition_name": manager_compose.name,
        "composition_dept": manager_compose.department.name,
        "recommendation": "Prefer composition for 'has-a' relationships",
    }


def demonstrate_mixins() -> dict[str, Any]:
    """Demonstrate mixin pattern."""
    class JSONMixin:
        """Mixin to add JSON serialization."""

        def to_json(self) -> str:
            import json
            return json.dumps(self.__dict__)

    class LogMixin:
        """Mixin to add logging capability."""

        def log(self, message: str) -> str:
            return f"[{self.__class__.__name__}] {message}"

    class User(JSONMixin, LogMixin):
        """User class with mixins."""

        def __init__(self, username: str, email: str):
            self.username = username
            self.email = email

    user = User("alice", "alice@example.com")
    json_repr = user.to_json()
    log_message = user.log("User created")

    return {
        "json_output": json_repr,
        "log_output": log_message,
        "has_to_json": hasattr(user, 'to_json'),
        "has_log": hasattr(user, 'log'),
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 15: Inheritance")
    print("=" * 60)

    print("\n1. Basic Inheritance:")
    basic = demonstrate_basic_inheritance()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Super():")
    super_demo = demonstrate_super()
    for key, value in super_demo.items():
        print(f"   {key}: {value}")

    print("\n3. Multiple Inheritance:")
    multiple = demonstrate_multiple_inheritance()
    for key, value in multiple.items():
        print(f"   {key}: {value}")

    print("\n4. Method Resolution Order:")
    mro = demonstrate_method_resolution_order()
    for key, value in mro.items():
        print(f"   {key}: {value}")

    print("\n5. Abstract Classes:")
    abstract = demonstrate_abstract_classes()
    for key, value in abstract.items():
        print(f"   {key}: {value}")

    print("\n6. Polymorphism:")
    polymorphism = demonstrate_polymorphism()
    for key, value in polymorphism.items():
        print(f"   {key}: {value}")

    print("\n7. Composition vs Inheritance:")
    comparison = demonstrate_composition_vs_inheritance()
    for key, value in comparison.items():
        print(f"   {key}: {value}")

    print("\n8. Mixins:")
    mixins = demonstrate_mixins()
    for key, value in mixins.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
