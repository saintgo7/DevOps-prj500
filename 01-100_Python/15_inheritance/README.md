# 15_inheritance

## Description

Master inheritance in Python - a fundamental OOP concept that enables code reuse through parent-child class relationships. Learn single inheritance, multiple inheritance, method resolution order (MRO), abstract base classes, and when to use inheritance vs composition.

This is Program #15 in the 500 Programs Collection.

## Learning Objectives

- Understand single and multiple inheritance
- Use super() for parent class access
- Master Method Resolution Order (MRO)
- Create abstract base classes (ABC)
- Implement polymorphism through inheritance
- Understand composition vs inheritance
- Use mixins for shared functionality
- Apply inheritance best practices

## Features

- Basic single inheritance
- super() function usage
- Multiple inheritance patterns
- Method Resolution Order (MRO)
- Abstract Base Classes (ABC)
- Polymorphism demonstrations
- Composition vs inheritance comparison
- Mixin pattern implementation

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Inheritance

```python
class Animal:
    """Base class."""
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "Some sound"

class Dog(Animal):
    """Dog inherits from Animal."""
    def speak(self) -> str:
        """Override parent method."""
        return "Woof!"

dog = Dog("Buddy")
print(dog.name)  # Inherited attribute
print(dog.speak())  # Overridden method
isinstance(dog, Animal)  # True
isinstance(dog, Dog)  # True
```

### 2. Using super()

```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def introduce(self) -> str:
        return f"I'm {self.name}, {self.age} years old"

class Student(Person):
    def __init__(self, name: str, age: int, student_id: str):
        super().__init__(name, age)  # Call parent constructor
        self.student_id = student_id

    def introduce(self) -> str:
        parent_intro = super().introduce()  # Call parent method
        return f"{parent_intro}, Student ID: {self.student_id}"

student = Student("Alice", 20, "S12345")
print(student.introduce())
```

### 3. Multiple Inheritance

```python
class Flyer:
    def fly(self) -> str:
        return "Flying"

class Swimmer:
    def swim(self) -> str:
        return "Swimming"

class Duck(Flyer, Swimmer):
    """Duck inherits from both Flyer and Swimmer."""
    def __init__(self, name: str):
        self.name = name

    def quack(self) -> str:
        return f"{self.name} says quack!"

duck = Duck("Donald")
duck.fly()    # From Flyer
duck.swim()   # From Swimmer
duck.quack()  # Own method

# Check inheritance
Duck.__mro__  # Method Resolution Order
```

### 4. Method Resolution Order (MRO)

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

d = D()
d.method()  # Which one is called?

# Check MRO
D.__mro__  # (D, B, C, A, object)
# Python uses C3 linearization algorithm
```

### 5. Abstract Base Classes

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class."""

    @abstractmethod
    def area(self) -> float:
        """Must be implemented by subclasses."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Must be implemented by subclasses."""
        pass

    def description(self) -> str:
        """Concrete method available to all."""
        return f"Area: {self.area():.2f}"

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Cannot instantiate ABC
# shape = Shape()  # TypeError

# Can instantiate concrete class
rect = Rectangle(5, 3)
print(rect.area())  # 15.0
```

### 6. Polymorphism

```python
class Vehicle:
    def __init__(self, brand: str):
        self.brand = brand

    def move(self) -> str:
        return "Moving"

class Car(Vehicle):
    def move(self) -> str:
        return f"{self.brand} is driving"

class Boat(Vehicle):
    def move(self) -> str:
        return f"{self.brand} is sailing"

# Polymorphism in action
vehicles = [Car("Toyota"), Boat("Yamaha"), Car("Honda")]
for vehicle in vehicles:
    print(vehicle.move())  # Different behavior for each
```

### 7. Composition vs Inheritance

```python
# Using inheritance (is-a relationship)
class Manager(Employee):
    def __init__(self, name: str, department: str):
        super().__init__(name)
        self.department = department

# Using composition (has-a relationship)
class Manager:
    def __init__(self, name: str, department_name: str):
        self.employee = Employee(name)  # Composition
        self.department = Department(department_name)

# Prefer composition when:
# - No clear "is-a" relationship
# - Need flexibility to change behavior
# - Want to avoid deep inheritance hierarchies
```

### 8. Mixins

```python
class JSONMixin:
    """Mixin for JSON serialization."""
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

class LogMixin:
    """Mixin for logging."""
    def log(self, message: str) -> str:
        return f"[{self.__class__.__name__}] {message}"

class User(JSONMixin, LogMixin):
    """User class with mixin functionality."""
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

user = User("alice", "alice@example.com")
user.to_json()  # From JSONMixin
user.log("User created")  # From LogMixin
```

## Best Practices

1. **Keep Inheritance Hierarchies Shallow**
   - Max 2-3 levels deep
   - Deep hierarchies are hard to maintain

2. **Use ABC for Interfaces**
   ```python
   from abc import ABC, abstractmethod

   class Repository(ABC):
       @abstractmethod
       def save(self, data):
           pass
   ```

3. **Prefer Composition Over Inheritance**
   - "Has-a" relationships: use composition
   - "Is-a" relationships: use inheritance

4. **Use super() Properly**
   ```python
   def __init__(self, ...):
       super().__init__(...)  # Call parent
   ```

5. **Document Inheritance Relationships**
6. **Avoid Multiple Inheritance When Possible**
7. **Use Mixins for Cross-Cutting Concerns**

## Testing

```bash
python src/main.py
```

---

**Program**: 15 of 500
**Difficulty**: ⭐⭐ Intermediate
**Category**: Object-Oriented Programming
**Estimated Time**: 60-75 minutes

[← Previous (14)](../14_classes_objects/) | [Back to Index](../../docs/INDEX.md) | [Next (16) →](../16_polymorphism/)
