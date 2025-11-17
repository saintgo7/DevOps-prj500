#!/usr/bin/env python3
"""Program 39: Design Patterns - Master classic and modern design patterns."""

from typing import Any, List, Protocol
from abc import ABC, abstractmethod


def demonstrate_singleton() -> dict[str, Any]:
    """Demonstrate Singleton pattern."""

    class Singleton:
        """Singleton implementation."""
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.initialized = False
            return cls._instance

        def __init__(self):
            if not self.initialized:
                self.value = 0
                self.initialized = True

    # Create instances
    s1 = Singleton()
    s2 = Singleton()
    s3 = Singleton()

    # Modify one
    s1.value = 42

    return {
        "same_instance": s1 is s2 is s3,
        "shared_value": s2.value,
        "id_s1": id(s1),
        "id_s2": id(s2),
        "note": "Singleton ensures only one instance exists",
    }


def demonstrate_factory() -> dict[str, Any]:
    """Demonstrate Factory pattern."""

    class Animal(ABC):
        @abstractmethod
        def speak(self) -> str:
            pass

    class Dog(Animal):
        def speak(self) -> str:
            return "Woof!"

    class Cat(Animal):
        def speak(self) -> str:
            return "Meow!"

    class Bird(Animal):
        def speak(self) -> str:
            return "Tweet!"

    class AnimalFactory:
        """Factory for creating animals."""

        @staticmethod
        def create_animal(animal_type: str) -> Animal:
            """Create animal based on type."""
            animals = {
                "dog": Dog,
                "cat": Cat,
                "bird": Bird,
            }
            animal_class = animals.get(animal_type.lower())
            if not animal_class:
                raise ValueError(f"Unknown animal: {animal_type}")
            return animal_class()

    # Create animals using factory
    dog = AnimalFactory.create_animal("dog")
    cat = AnimalFactory.create_animal("cat")
    bird = AnimalFactory.create_animal("bird")

    return {
        "dog_sound": dog.speak(),
        "cat_sound": cat.speak(),
        "bird_sound": bird.speak(),
        "note": "Factory encapsulates object creation logic",
    }


def demonstrate_observer() -> dict[str, Any]:
    """Demonstrate Observer pattern."""

    class Observer(ABC):
        @abstractmethod
        def update(self, message: str) -> None:
            pass

    class ConcreteObserver(Observer):
        def __init__(self, name: str):
            self.name = name
            self.messages = []

        def update(self, message: str) -> None:
            self.messages.append(message)

    class Subject:
        """Subject that notifies observers."""

        def __init__(self):
            self._observers: List[Observer] = []

        def attach(self, observer: Observer) -> None:
            self._observers.append(observer)

        def detach(self, observer: Observer) -> None:
            self._observers.remove(observer)

        def notify(self, message: str) -> None:
            for observer in self._observers:
                observer.update(message)

    # Create subject and observers
    subject = Subject()
    obs1 = ConcreteObserver("Observer1")
    obs2 = ConcreteObserver("Observer2")

    subject.attach(obs1)
    subject.attach(obs2)

    # Notify observers
    subject.notify("Event 1")
    subject.notify("Event 2")

    return {
        "obs1_messages": obs1.messages,
        "obs2_messages": obs2.messages,
        "observer_count": len(subject._observers),
        "note": "Observer enables one-to-many dependency",
    }


def demonstrate_strategy() -> dict[str, Any]:
    """Demonstrate Strategy pattern."""

    class SortStrategy(ABC):
        @abstractmethod
        def sort(self, data: List[int]) -> List[int]:
            pass

    class BubbleSort(SortStrategy):
        def sort(self, data: List[int]) -> List[int]:
            arr = data.copy()
            n = len(arr)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return arr

    class QuickSort(SortStrategy):
        def sort(self, data: List[int]) -> List[int]:
            if len(data) <= 1:
                return data
            pivot = data[len(data) // 2]
            left = [x for x in data if x < pivot]
            middle = [x for x in data if x == pivot]
            right = [x for x in data if x > pivot]
            return self.sort(left) + middle + self.sort(right)

    class Sorter:
        """Context that uses strategy."""

        def __init__(self, strategy: SortStrategy):
            self.strategy = strategy

        def sort(self, data: List[int]) -> List[int]:
            return self.strategy.sort(data)

    # Use different strategies
    data = [64, 34, 25, 12, 22, 11, 90]

    bubble_sorter = Sorter(BubbleSort())
    quick_sorter = Sorter(QuickSort())

    bubble_result = bubble_sorter.sort(data)
    quick_result = quick_sorter.sort(data)

    return {
        "bubble_sort": bubble_result,
        "quick_sort": quick_result,
        "results_equal": bubble_result == quick_result,
        "note": "Strategy enables selecting algorithm at runtime",
    }


def demonstrate_decorator_pattern() -> dict[str, Any]:
    """Demonstrate Decorator pattern (not Python decorator)."""

    class Component(ABC):
        @abstractmethod
        def operation(self) -> str:
            pass

    class ConcreteComponent(Component):
        def operation(self) -> str:
            return "ConcreteComponent"

    class Decorator(Component):
        def __init__(self, component: Component):
            self._component = component

        def operation(self) -> str:
            return self._component.operation()

    class BorderDecorator(Decorator):
        def operation(self) -> str:
            return f"[{self._component.operation()}]"

    class ColorDecorator(Decorator):
        def __init__(self, component: Component, color: str):
            super().__init__(component)
            self.color = color

        def operation(self) -> str:
            return f"{self.color}({self._component.operation()})"

    # Build decorated component
    component = ConcreteComponent()
    bordered = BorderDecorator(component)
    colored_bordered = ColorDecorator(bordered, "Red")

    return {
        "plain": component.operation(),
        "bordered": bordered.operation(),
        "colored_bordered": colored_bordered.operation(),
        "note": "Decorator adds behavior without modifying original",
    }


def demonstrate_adapter() -> dict[str, Any]:
    """Demonstrate Adapter pattern."""

    class EuropeanPlug:
        """European power plug."""

        def provide_power(self) -> str:
            return "220V European power"

    class AmericanSocket:
        """American power socket."""

        def connect(self, plug: 'AmericanPlug') -> str:
            return plug.get_power()

    class AmericanPlug:
        """American power plug."""

        def get_power(self) -> str:
            return "110V American power"

    class PlugAdapter(AmericanPlug):
        """Adapter for European plug."""

        def __init__(self, european_plug: EuropeanPlug):
            self.european_plug = european_plug

        def get_power(self) -> str:
            power = self.european_plug.provide_power()
            # Convert to American format
            return f"Converted from {power}"

    # Use adapter
    european_plug = EuropeanPlug()
    adapter = PlugAdapter(european_plug)
    socket = AmericanSocket()

    result = socket.connect(adapter)

    return {
        "result": result,
        "note": "Adapter converts one interface to another",
    }


def demonstrate_command() -> dict[str, Any]:
    """Demonstrate Command pattern."""

    class Command(ABC):
        @abstractmethod
        def execute(self) -> str:
            pass

        @abstractmethod
        def undo(self) -> str:
            pass

    class Light:
        """Receiver."""

        def __init__(self):
            self.is_on = False

        def turn_on(self) -> str:
            self.is_on = True
            return "Light is ON"

        def turn_off(self) -> str:
            self.is_on = False
            return "Light is OFF"

    class LightOnCommand(Command):
        def __init__(self, light: Light):
            self.light = light

        def execute(self) -> str:
            return self.light.turn_on()

        def undo(self) -> str:
            return self.light.turn_off()

    class LightOffCommand(Command):
        def __init__(self, light: Light):
            self.light = light

        def execute(self) -> str:
            return self.light.turn_off()

        def undo(self) -> str:
            return self.light.turn_on()

    class RemoteControl:
        """Invoker."""

        def __init__(self):
            self.command: Command = None
            self.history: List[Command] = []

        def set_command(self, command: Command):
            self.command = command

        def press_button(self) -> str:
            result = self.command.execute()
            self.history.append(self.command)
            return result

        def press_undo(self) -> str:
            if self.history:
                command = self.history.pop()
                return command.undo()
            return "Nothing to undo"

    # Use command pattern
    light = Light()
    on_command = LightOnCommand(light)
    off_command = LightOffCommand(light)

    remote = RemoteControl()

    remote.set_command(on_command)
    result1 = remote.press_button()

    remote.set_command(off_command)
    result2 = remote.press_button()

    result3 = remote.press_undo()

    return {
        "turn_on": result1,
        "turn_off": result2,
        "undo": result3,
        "final_state": light.is_on,
        "note": "Command encapsulates actions as objects",
    }


def demonstrate_builder() -> dict[str, Any]:
    """Demonstrate Builder pattern."""

    class Pizza:
        """Product."""

        def __init__(self):
            self.size = None
            self.cheese = False
            self.pepperoni = False
            self.mushrooms = False

        def __str__(self):
            return f"Pizza(size={self.size}, cheese={self.cheese}, pepperoni={self.pepperoni}, mushrooms={self.mushrooms})"

    class PizzaBuilder:
        """Builder."""

        def __init__(self):
            self.pizza = Pizza()

        def set_size(self, size: str) -> 'PizzaBuilder':
            self.pizza.size = size
            return self

        def add_cheese(self) -> 'PizzaBuilder':
            self.pizza.cheese = True
            return self

        def add_pepperoni(self) -> 'PizzaBuilder':
            self.pizza.pepperoni = True
            return self

        def add_mushrooms(self) -> 'PizzaBuilder':
            self.pizza.mushrooms = True
            return self

        def build(self) -> Pizza:
            return self.pizza

    # Build pizza
    pizza = (PizzaBuilder()
             .set_size("Large")
             .add_cheese()
             .add_pepperoni()
             .build())

    return {
        "size": pizza.size,
        "has_cheese": pizza.cheese,
        "has_pepperoni": pizza.pepperoni,
        "has_mushrooms": pizza.mushrooms,
        "note": "Builder constructs complex objects step by step",
    }


def demonstrate_template_method() -> dict[str, Any]:
    """Demonstrate Template Method pattern."""

    class DataProcessor(ABC):
        """Template method pattern."""

        def process(self) -> List[str]:
            """Template method."""
            steps = []
            steps.append(self.read_data())
            steps.append(self.process_data())
            steps.append(self.save_data())
            return steps

        @abstractmethod
        def read_data(self) -> str:
            pass

        @abstractmethod
        def process_data(self) -> str:
            pass

        @abstractmethod
        def save_data(self) -> str:
            pass

    class CSVProcessor(DataProcessor):
        def read_data(self) -> str:
            return "Reading CSV file"

        def process_data(self) -> str:
            return "Processing CSV data"

        def save_data(self) -> str:
            return "Saving to CSV"

    class JSONProcessor(DataProcessor):
        def read_data(self) -> str:
            return "Reading JSON file"

        def process_data(self) -> str:
            return "Processing JSON data"

        def save_data(self) -> str:
            return "Saving to JSON"

    csv_processor = CSVProcessor()
    json_processor = JSONProcessor()

    return {
        "csv_steps": csv_processor.process(),
        "json_steps": json_processor.process(),
        "note": "Template Method defines algorithm skeleton in base class",
    }


def demonstrate_dependency_injection() -> dict[str, Any]:
    """Demonstrate Dependency Injection pattern."""

    class Database(Protocol):
        """Database interface."""

        def query(self, sql: str) -> List[dict]:
            ...

    class MySQLDatabase:
        """MySQL implementation."""

        def query(self, sql: str) -> List[dict]:
            return [{"id": 1, "name": "MySQL result"}]

    class PostgreSQLDatabase:
        """PostgreSQL implementation."""

        def query(self, sql: str) -> List[dict]:
            return [{"id": 1, "name": "PostgreSQL result"}]

    class UserRepository:
        """Repository with dependency injection."""

        def __init__(self, database: Database):
            self.database = database

        def get_users(self) -> List[dict]:
            return self.database.query("SELECT * FROM users")

    # Inject different databases
    mysql_repo = UserRepository(MySQLDatabase())
    postgres_repo = UserRepository(PostgreSQLDatabase())

    mysql_result = mysql_repo.get_users()
    postgres_result = postgres_repo.get_users()

    return {
        "mysql_source": mysql_result[0]["name"],
        "postgres_source": postgres_result[0]["name"],
        "note": "DI decouples classes from their dependencies",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 39: Design Patterns")
    print("=" * 60)

    print("\n1. Singleton:")
    singleton = demonstrate_singleton()
    for key, value in singleton.items():
        print(f"   {key}: {value}")

    print("\n2. Factory:")
    factory = demonstrate_factory()
    for key, value in factory.items():
        print(f"   {key}: {value}")

    print("\n3. Observer:")
    observer = demonstrate_observer()
    for key, value in observer.items():
        print(f"   {key}: {value}")

    print("\n4. Strategy:")
    strategy = demonstrate_strategy()
    for key, value in strategy.items():
        print(f"   {key}: {value}")

    print("\n5. Decorator Pattern:")
    decorator = demonstrate_decorator_pattern()
    for key, value in decorator.items():
        print(f"   {key}: {value}")

    print("\n6. Adapter:")
    adapter = demonstrate_adapter()
    for key, value in adapter.items():
        print(f"   {key}: {value}")

    print("\n7. Command:")
    command = demonstrate_command()
    for key, value in command.items():
        print(f"   {key}: {value}")

    print("\n8. Builder:")
    builder = demonstrate_builder()
    for key, value in builder.items():
        print(f"   {key}: {value}")

    print("\n9. Template Method:")
    template = demonstrate_template_method()
    for key, value in template.items():
        print(f"   {key}: {value}")

    print("\n10. Dependency Injection:")
    di = demonstrate_dependency_injection()
    for key, value in di.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
