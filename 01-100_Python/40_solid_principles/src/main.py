#!/usr/bin/env python3
"""Program 40: SOLID Principles - Master object-oriented design principles."""

from typing import Any, List, Protocol
from abc import ABC, abstractmethod


def demonstrate_single_responsibility() -> dict[str, Any]:
    """Demonstrate Single Responsibility Principle (SRP)."""

    # BAD: Multiple responsibilities
    class UserBad:
        def __init__(self, name: str, email: str):
            self.name = name
            self.email = email

        def save_to_database(self):
            # Database logic
            pass

        def send_email(self):
            # Email logic
            pass

        def generate_report(self):
            # Reporting logic
            pass

    # GOOD: Single responsibility
    class User:
        """Only responsible for user data."""

        def __init__(self, name: str, email: str):
            self.name = name
            self.email = email

    class UserRepository:
        """Only responsible for database operations."""

        def save(self, user: User):
            return f"Saved {user.name} to database"

    class EmailService:
        """Only responsible for email operations."""

        def send(self, user: User, message: str):
            return f"Sent email to {user.email}"

    class ReportGenerator:
        """Only responsible for generating reports."""

        def generate(self, user: User):
            return f"Generated report for {user.name}"

    # Use separated classes
    user = User("Alice", "alice@example.com")
    repo = UserRepository()
    email = EmailService()
    report = ReportGenerator()

    return {
        "saved": repo.save(user),
        "emailed": email.send(user, "Welcome!"),
        "reported": report.generate(user),
        "note": "SRP: A class should have only one reason to change",
    }


def demonstrate_open_closed() -> dict[str, Any]:
    """Demonstrate Open/Closed Principle (OCP)."""

    # GOOD: Open for extension, closed for modification
    class Discount(ABC):
        """Base discount class."""

        @abstractmethod
        def calculate(self, price: float) -> float:
            pass

    class NoDiscount(Discount):
        """No discount."""

        def calculate(self, price: float) -> float:
            return price

    class PercentageDiscount(Discount):
        """Percentage-based discount."""

        def __init__(self, percentage: float):
            self.percentage = percentage

        def calculate(self, price: float) -> float:
            return price * (1 - self.percentage / 100)

    class FixedDiscount(Discount):
        """Fixed amount discount."""

        def __init__(self, amount: float):
            self.amount = amount

        def calculate(self, price: float) -> float:
            return max(0, price - self.amount)

    class PriceCalculator:
        """Calculator using discount strategy."""

        def calculate_price(self, price: float, discount: Discount) -> float:
            return discount.calculate(price)

    # Use different discounts without modifying PriceCalculator
    calc = PriceCalculator()
    price = 100.0

    no_discount = calc.calculate_price(price, NoDiscount())
    percent_discount = calc.calculate_price(price, PercentageDiscount(10))
    fixed_discount = calc.calculate_price(price, FixedDiscount(15))

    return {
        "no_discount": no_discount,
        "10_percent": percent_discount,
        "15_fixed": fixed_discount,
        "note": "OCP: Open for extension, closed for modification",
    }


def demonstrate_liskov_substitution() -> dict[str, Any]:
    """Demonstrate Liskov Substitution Principle (LSP)."""

    # GOOD: Subtypes can replace base type
    class Bird:
        """Base bird class."""

        def __init__(self, name: str):
            self.name = name

        def eat(self) -> str:
            return f"{self.name} is eating"

    class FlyingBird(Bird):
        """Bird that can fly."""

        def fly(self) -> str:
            return f"{self.name} is flying"

    class Sparrow(FlyingBird):
        """Sparrow can fly."""

        def fly(self) -> str:
            return f"{self.name} (sparrow) is flying"

    class Penguin(Bird):
        """Penguin cannot fly - doesn't inherit FlyingBird."""

        def swim(self) -> str:
            return f"{self.name} (penguin) is swimming"

    # Functions work with base types
    def feed_bird(bird: Bird) -> str:
        """Works with any Bird."""
        return bird.eat()

    def make_bird_fly(bird: FlyingBird) -> str:
        """Only works with flying birds."""
        return bird.fly()

    sparrow = Sparrow("Tweety")
    penguin = Penguin("Pingu")

    return {
        "sparrow_eat": feed_bird(sparrow),
        "penguin_eat": feed_bird(penguin),
        "sparrow_fly": make_bird_fly(sparrow),
        "penguin_swim": penguin.swim(),
        "note": "LSP: Subtypes must be substitutable for their base types",
    }


def demonstrate_interface_segregation() -> dict[str, Any]:
    """Demonstrate Interface Segregation Principle (ISP)."""

    # GOOD: Segregated interfaces
    class Printer(Protocol):
        """Print interface."""

        def print_document(self, doc: str) -> str:
            ...

    class Scanner(Protocol):
        """Scan interface."""

        def scan_document(self) -> str:
            ...

    class Fax(Protocol):
        """Fax interface."""

        def send_fax(self, doc: str) -> str:
            ...

    class SimplePrinter:
        """Only implements printing."""

        def print_document(self, doc: str) -> str:
            return f"Printing: {doc}"

    class MultiFunctionDevice:
        """Implements all interfaces."""

        def print_document(self, doc: str) -> str:
            return f"Printing: {doc}"

        def scan_document(self) -> str:
            return "Scanning document"

        def send_fax(self, doc: str) -> str:
            return f"Faxing: {doc}"

    # Use specific interfaces
    simple = SimplePrinter()
    multi = MultiFunctionDevice()

    return {
        "simple_print": simple.print_document("test.pdf"),
        "multi_print": multi.print_document("test.pdf"),
        "multi_scan": multi.scan_document(),
        "multi_fax": multi.send_fax("test.pdf"),
        "note": "ISP: No client should depend on methods it doesn't use",
    }


def demonstrate_dependency_inversion() -> dict[str, Any]:
    """Demonstrate Dependency Inversion Principle (DIP)."""

    # GOOD: Depend on abstractions
    class MessageSender(Protocol):
        """Abstract message sender."""

        def send(self, message: str) -> str:
            ...

    class EmailSender:
        """Concrete email implementation."""

        def send(self, message: str) -> str:
            return f"Email sent: {message}"

    class SMSSender:
        """Concrete SMS implementation."""

        def send(self, message: str) -> str:
            return f"SMS sent: {message}"

    class SlackSender:
        """Concrete Slack implementation."""

        def send(self, message: str) -> str:
            return f"Slack sent: {message}"

    class Notification:
        """High-level module depending on abstraction."""

        def __init__(self, sender: MessageSender):
            self.sender = sender

        def notify(self, message: str) -> str:
            return self.sender.send(message)

    # Inject different implementations
    email_notif = Notification(EmailSender())
    sms_notif = Notification(SMSSender())
    slack_notif = Notification(SlackSender())

    return {
        "email": email_notif.notify("Hello via Email"),
        "sms": sms_notif.notify("Hello via SMS"),
        "slack": slack_notif.notify("Hello via Slack"),
        "note": "DIP: Depend on abstractions, not concrete implementations",
    }


def demonstrate_srp_violation() -> dict[str, Any]:
    """Demonstrate SRP violation and fix."""

    # Violation example
    violation_code = """
class Employee:
    # Too many responsibilities!
    def calculate_pay(self): ...      # Finance
    def save_to_database(self): ...   # Persistence
    def generate_report(self): ...    # Reporting
    def send_email(self): ...         # Communication
"""

    # Fixed version
    fixed_code = """
class Employee:
    # Only employee data
    def __init__(self, name, hours, rate):
        self.name = name
        self.hours = hours
        self.rate = rate

class PayCalculator:
    def calculate(self, employee): ...

class EmployeeRepository:
    def save(self, employee): ...

class ReportGenerator:
    def generate(self, employee): ...

class EmailService:
    def send(self, employee): ...
"""

    return {
        "violation_count": 4,
        "classes_after_fix": 5,
        "note": "Each class has one responsibility",
    }


def demonstrate_ocp_extension() -> dict[str, Any]:
    """Demonstrate extending without modification."""

    class Shape(ABC):
        """Base shape - closed for modification."""

        @abstractmethod
        def area(self) -> float:
            pass

    class Rectangle(Shape):
        """Extended shape."""

        def __init__(self, width: float, height: float):
            self.width = width
            self.height = height

        def area(self) -> float:
            return self.width * self.height

    class Circle(Shape):
        """Another extension."""

        def __init__(self, radius: float):
            self.radius = radius

        def area(self) -> float:
            return 3.14159 * self.radius ** 2

    class Triangle(Shape):
        """New extension - Shape class unchanged."""

        def __init__(self, base: float, height: float):
            self.base = base
            self.height = height

        def area(self) -> float:
            return 0.5 * self.base * self.height

    class AreaCalculator:
        """Uses shapes - doesn't need modification."""

        def total_area(self, shapes: List[Shape]) -> float:
            return sum(shape.area() for shape in shapes)

    shapes = [
        Rectangle(5, 4),
        Circle(3),
        Triangle(6, 4),
    ]

    calc = AreaCalculator()
    total = calc.total_area(shapes)

    return {
        "rectangle_area": shapes[0].area(),
        "circle_area": shapes[1].area(),
        "triangle_area": shapes[2].area(),
        "total_area": total,
        "note": "New shapes added without modifying existing code",
    }


def demonstrate_lsp_violation() -> dict[str, Any]:
    """Demonstrate LSP violation and fix."""

    # Violation: Square violates LSP
    class Rectangle:
        def __init__(self, width: float, height: float):
            self.width = width
            self.height = height

        def set_width(self, width: float):
            self.width = width

        def set_height(self, height: float):
            self.height = height

        def area(self) -> float:
            return self.width * self.height

    # This violates LSP
    class SquareBad(Rectangle):
        def set_width(self, width: float):
            self.width = width
            self.height = width  # Breaks expectations

        def set_height(self, height: float):
            self.width = height  # Breaks expectations
            self.height = height

    # Better: Separate classes
    class Shape(ABC):
        @abstractmethod
        def area(self) -> float:
            pass

    class RectangleGood(Shape):
        def __init__(self, width: float, height: float):
            self.width = width
            self.height = height

        def area(self) -> float:
            return self.width * self.height

    class SquareGood(Shape):
        def __init__(self, side: float):
            self.side = side

        def area(self) -> float:
            return self.side ** 2

    rect = RectangleGood(5, 4)
    square = SquareGood(4)

    return {
        "rectangle_area": rect.area(),
        "square_area": square.area(),
        "note": "Square and Rectangle are separate, preserving LSP",
    }


def demonstrate_isp_benefits() -> dict[str, Any]:
    """Demonstrate ISP benefits."""

    # Specific interfaces
    class Readable(Protocol):
        def read(self) -> str: ...

    class Writable(Protocol):
        def write(self, data: str) -> str: ...

    class Closeable(Protocol):
        def close(self) -> str: ...

    class ReadOnlyFile:
        """Only implements what it needs."""

        def read(self) -> str:
            return "Reading data"

        def close(self) -> str:
            return "Closed"

    class ReadWriteFile:
        """Implements multiple interfaces."""

        def read(self) -> str:
            return "Reading data"

        def write(self, data: str) -> str:
            return f"Writing: {data}"

        def close(self) -> str:
            return "Closed"

    # Functions use specific interfaces
    def read_data(readable: Readable) -> str:
        return readable.read()

    def write_data(writable: Writable, data: str) -> str:
        return writable.write(data)

    ro_file = ReadOnlyFile()
    rw_file = ReadWriteFile()

    return {
        "ro_read": read_data(ro_file),
        "rw_read": read_data(rw_file),
        "rw_write": write_data(rw_file, "test"),
        "note": "Interfaces are small and focused",
    }


def demonstrate_all_principles() -> dict[str, Any]:
    """Demonstrate all SOLID principles working together."""

    principles_summary = {
        "S": "Single Responsibility - One reason to change",
        "O": "Open/Closed - Open for extension, closed for modification",
        "L": "Liskov Substitution - Subtypes must be substitutable",
        "I": "Interface Segregation - Many specific interfaces over one general",
        "D": "Dependency Inversion - Depend on abstractions, not concretions",
    }

    benefits = [
        "More maintainable code",
        "Easier to test",
        "More flexible and extensible",
        "Reduced coupling",
        "Better code organization",
    ]

    return {
        "principles": principles_summary,
        "benefits": benefits,
        "note": "SOLID principles lead to better OO design",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 40: SOLID Principles")
    print("=" * 60)

    print("\n1. Single Responsibility Principle (SRP):")
    srp = demonstrate_single_responsibility()
    for key, value in srp.items():
        print(f"   {key}: {value}")

    print("\n2. Open/Closed Principle (OCP):")
    ocp = demonstrate_open_closed()
    for key, value in ocp.items():
        print(f"   {key}: {value}")

    print("\n3. Liskov Substitution Principle (LSP):")
    lsp = demonstrate_liskov_substitution()
    for key, value in lsp.items():
        print(f"   {key}: {value}")

    print("\n4. Interface Segregation Principle (ISP):")
    isp = demonstrate_interface_segregation()
    for key, value in isp.items():
        print(f"   {key}: {value}")

    print("\n5. Dependency Inversion Principle (DIP):")
    dip = demonstrate_dependency_inversion()
    for key, value in dip.items():
        print(f"   {key}: {value}")

    print("\n6. SRP Violation and Fix:")
    srp_fix = demonstrate_srp_violation()
    for key, value in srp_fix.items():
        print(f"   {key}: {value}")

    print("\n7. OCP Extension Example:")
    ocp_ext = demonstrate_ocp_extension()
    for key, value in ocp_ext.items():
        print(f"   {key}: {value}")

    print("\n8. LSP Violation and Fix:")
    lsp_fix = demonstrate_lsp_violation()
    for key, value in lsp_fix.items():
        print(f"   {key}: {value}")

    print("\n9. ISP Benefits:")
    isp_benefits = demonstrate_isp_benefits()
    for key, value in isp_benefits.items():
        print(f"   {key}: {value}")

    print("\n10. All SOLID Principles:")
    all_solid = demonstrate_all_principles()
    for key, value in all_solid.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
