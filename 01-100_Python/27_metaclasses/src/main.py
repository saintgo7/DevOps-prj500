#!/usr/bin/env python3
"""Program 27: Metaclasses - Master class creation and customization."""

from typing import Any


def demonstrate_type_function() -> dict[str, Any]:
    """Demonstrate type() as a metaclass."""

    # type() with one argument returns the type
    example_int = type(42)
    example_str = type("hello")

    # type() with three arguments creates a class
    # type(name, bases, dict)
    DynamicClass = type(
        'DynamicClass',
        (object,),
        {
            'attribute': 42,
            'method': lambda self: "Hello from dynamic class"
        }
    )

    instance = DynamicClass()

    return {
        "int_type": example_int.__name__,
        "str_type": example_str.__name__,
        "dynamic_attribute": instance.attribute,
        "dynamic_method": instance.method(),
        "note": "type() is the default metaclass for creating classes",
    }


def demonstrate_basic_metaclass() -> dict[str, Any]:
    """Demonstrate basic metaclass definition."""

    class SimpleMeta(type):
        """Simple metaclass that adds a class attribute."""

        def __new__(mcs, name, bases, dct):
            """Create new class with additional attribute."""
            dct['added_by_metaclass'] = True
            dct['class_id'] = id(name)
            return super().__new__(mcs, name, bases, dct)

    class MyClass(metaclass=SimpleMeta):
        """Class using custom metaclass."""
        original_attr = "original"

    return {
        "has_original": hasattr(MyClass, 'original_attr'),
        "has_added": hasattr(MyClass, 'added_by_metaclass'),
        "added_value": MyClass.added_by_metaclass,
        "note": "Metaclass __new__ called when class is created",
    }


def demonstrate_metaclass_init() -> dict[str, Any]:
    """Demonstrate metaclass __init__ method."""

    class InitMeta(type):
        """Metaclass with __init__."""

        def __init__(cls, name, bases, dct):
            """Initialize the class after creation."""
            super().__init__(name, bases, dct)
            cls.instances = []
            cls.creation_order = len(InitMeta.__subclasses__())

        def __call__(cls, *args, **kwargs):
            """Called when creating instance of the class."""
            instance = super().__call__(*args, **kwargs)
            cls.instances.append(instance)
            return instance

    class Tracked(metaclass=InitMeta):
        """Class that tracks its instances."""
        pass

    # Create instances
    obj1 = Tracked()
    obj2 = Tracked()
    obj3 = Tracked()

    return {
        "instance_count": len(Tracked.instances),
        "all_tracked": all(isinstance(obj, Tracked) for obj in Tracked.instances),
        "note": "Metaclass __call__ intercepts instance creation",
    }


def demonstrate_singleton_metaclass() -> dict[str, Any]:
    """Demonstrate Singleton pattern with metaclass."""

    class SingletonMeta(type):
        """Metaclass that creates singleton classes."""

        _instances = {}

        def __call__(cls, *args, **kwargs):
            """Return existing instance or create new one."""
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]

    class Database(metaclass=SingletonMeta):
        """Singleton database connection."""

        def __init__(self):
            self.connection = "Connected"

    # Create multiple "instances"
    db1 = Database()
    db2 = Database()
    db3 = Database()

    return {
        "same_instance": db1 is db2 is db3,
        "id_db1": id(db1),
        "id_db2": id(db2),
        "note": "Singleton metaclass ensures only one instance exists",
    }


def demonstrate_attribute_validation() -> dict[str, Any]:
    """Demonstrate metaclass for attribute validation."""

    class ValidatedMeta(type):
        """Metaclass that validates class attributes."""

        def __new__(mcs, name, bases, dct):
            """Validate attributes before class creation."""
            # Check for required class attributes
            if name != 'BaseModel':  # Skip for base class
                if 'required_field' not in dct:
                    dct['validation_error'] = "Missing required_field"
                else:
                    dct['validation_error'] = None

            return super().__new__(mcs, name, bases, dct)

    class BaseModel(metaclass=ValidatedMeta):
        """Base model class."""
        pass

    class ValidModel(BaseModel):
        """Model with required field."""
        required_field = "present"

    class InvalidModel(BaseModel):
        """Model without required field."""
        pass

    return {
        "valid_error": ValidModel.validation_error,
        "invalid_error": InvalidModel.validation_error,
        "note": "Metaclass can validate class definition",
    }


def demonstrate_method_registration() -> dict[str, Any]:
    """Demonstrate automatic method registration with metaclass."""

    class RegistryMeta(type):
        """Metaclass that registers methods."""

        def __new__(mcs, name, bases, dct):
            """Register methods with specific prefix."""
            cls = super().__new__(mcs, name, bases, dct)

            # Find and register methods
            handlers = {}
            for key, value in dct.items():
                if key.startswith('handle_') and callable(value):
                    event_name = key[7:]  # Remove 'handle_' prefix
                    handlers[event_name] = value

            cls._handlers = handlers
            return cls

    class EventProcessor(metaclass=RegistryMeta):
        """Process events with registered handlers."""

        def handle_click(self):
            return "Click handled"

        def handle_submit(self):
            return "Submit handled"

        def handle_cancel(self):
            return "Cancel handled"

        def other_method(self):
            return "Not a handler"

    return {
        "registered_handlers": list(EventProcessor._handlers.keys()),
        "handler_count": len(EventProcessor._handlers),
        "note": "Metaclass can auto-register methods by naming convention",
    }


def demonstrate_class_decoration() -> dict[str, Any]:
    """Demonstrate metaclass for automatic class decoration."""

    class DecoratorMeta(type):
        """Metaclass that decorates all methods."""

        def __new__(mcs, name, bases, dct):
            """Wrap all methods with logging."""

            def logged_method(method):
                """Wrapper that logs method calls."""

                def wrapper(*args, **kwargs):
                    result = method(*args, **kwargs)
                    return f"[LOGGED] {method.__name__}: {result}"

                return wrapper

            # Wrap all methods (except special methods)
            for key, value in dct.items():
                if callable(value) and not key.startswith('__'):
                    dct[key] = logged_method(value)

            return super().__new__(mcs, name, bases, dct)

    class Calculator(metaclass=DecoratorMeta):
        """Calculator with auto-logged methods."""

        def add(self, a, b):
            return a + b

        def multiply(self, a, b):
            return a * b

    calc = Calculator()

    return {
        "add_result": calc.add(2, 3),
        "multiply_result": calc.multiply(4, 5),
        "note": "Metaclass can automatically decorate methods",
    }


def demonstrate_abstract_enforcement() -> dict[str, Any]:
    """Demonstrate metaclass for enforcing abstract methods."""

    class AbstractMeta(type):
        """Metaclass that enforces abstract method implementation."""

        def __call__(cls, *args, **kwargs):
            """Check abstract methods before instantiation."""
            abstract_methods = getattr(cls, '_abstract_methods', set())

            # Check if all abstract methods are implemented
            for method in abstract_methods:
                if not hasattr(cls, method) or getattr(cls, method) is None:
                    return f"Error: {method} not implemented"

            return super().__call__(*args, **kwargs)

    class Shape(metaclass=AbstractMeta):
        """Abstract shape class."""
        _abstract_methods = {'area', 'perimeter'}

        def describe(self):
            return "I am a shape"

    class Rectangle(Shape):
        """Concrete rectangle."""

        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

        def perimeter(self):
            return 2 * (self.width + self.height)

    class IncompleteShape(Shape):
        """Shape without required methods."""

        def area(self):
            return 0
        # Missing perimeter!

    rect = Rectangle(5, 3)
    incomplete = IncompleteShape()

    return {
        "rectangle_type": type(rect).__name__,
        "incomplete_error": isinstance(incomplete, str),
        "note": "Metaclass can enforce abstract method implementation",
    }


def demonstrate_class_registry() -> dict[str, Any]:
    """Demonstrate automatic class registry with metaclass."""

    class RegistryMeta(type):
        """Metaclass that maintains registry of all subclasses."""

        registry = {}

        def __new__(mcs, name, bases, dct):
            """Register class on creation."""
            cls = super().__new__(mcs, name, bases, dct)

            # Register class by name
            if name != 'Plugin':  # Don't register base class
                mcs.registry[name] = cls

            return cls

    class Plugin(metaclass=RegistryMeta):
        """Base plugin class."""
        pass

    class AuthPlugin(Plugin):
        """Authentication plugin."""
        pass

    class LoggingPlugin(Plugin):
        """Logging plugin."""
        pass

    class CachePlugin(Plugin):
        """Caching plugin."""
        pass

    return {
        "registered_plugins": list(RegistryMeta.registry.keys()),
        "plugin_count": len(RegistryMeta.registry),
        "can_get_class": RegistryMeta.registry['AuthPlugin'].__name__,
        "note": "Metaclass can maintain registry of all subclasses",
    }


def demonstrate_inheritance_metaclass() -> dict[str, Any]:
    """Demonstrate metaclass inheritance."""

    class BaseMeta(type):
        """Base metaclass."""

        def __new__(mcs, name, bases, dct):
            dct['from_base_meta'] = True
            return super().__new__(mcs, name, bases, dct)

    class ExtendedMeta(BaseMeta):
        """Extended metaclass."""

        def __new__(mcs, name, bases, dct):
            dct['from_extended_meta'] = True
            return super().__new__(mcs, name, bases, dct)

    class MyClass(metaclass=ExtendedMeta):
        """Class using extended metaclass."""
        pass

    return {
        "has_base_attr": hasattr(MyClass, 'from_base_meta'),
        "has_extended_attr": hasattr(MyClass, 'from_extended_meta'),
        "base_value": MyClass.from_base_meta,
        "extended_value": MyClass.from_extended_meta,
        "note": "Metaclasses can inherit from other metaclasses",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 27: Metaclasses")
    print("=" * 60)

    print("\n1. Type Function:")
    type_demo = demonstrate_type_function()
    for key, value in type_demo.items():
        print(f"   {key}: {value}")

    print("\n2. Basic Metaclass:")
    basic = demonstrate_basic_metaclass()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n3. Metaclass __init__:")
    init = demonstrate_metaclass_init()
    for key, value in init.items():
        print(f"   {key}: {value}")

    print("\n4. Singleton Metaclass:")
    singleton = demonstrate_singleton_metaclass()
    for key, value in singleton.items():
        print(f"   {key}: {value}")

    print("\n5. Attribute Validation:")
    validation = demonstrate_attribute_validation()
    for key, value in validation.items():
        print(f"   {key}: {value}")

    print("\n6. Method Registration:")
    registration = demonstrate_method_registration()
    for key, value in registration.items():
        print(f"   {key}: {value}")

    print("\n7. Class Decoration:")
    decoration = demonstrate_class_decoration()
    for key, value in decoration.items():
        print(f"   {key}: {value}")

    print("\n8. Abstract Enforcement:")
    abstract = demonstrate_abstract_enforcement()
    for key, value in abstract.items():
        print(f"   {key}: {value}")

    print("\n9. Class Registry:")
    registry = demonstrate_class_registry()
    for key, value in registry.items():
        print(f"   {key}: {value}")

    print("\n10. Metaclass Inheritance:")
    inheritance = demonstrate_inheritance_metaclass()
    for key, value in inheritance.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
