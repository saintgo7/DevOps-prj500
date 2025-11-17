#!/usr/bin/env python3
"""Program 28: Descriptors - Master attribute access control with descriptors."""

from typing import Any, Optional
from weakref import WeakKeyDictionary


def demonstrate_basic_descriptor() -> dict[str, Any]:
    """Demonstrate basic descriptor protocol."""

    class Descriptor:
        """Simple descriptor."""

        def __init__(self, name: str):
            self.name = name

        def __get__(self, instance, owner):
            """Get attribute value."""
            if instance is None:
                return self
            return f"Getting {self.name}"

        def __set__(self, instance, value):
            """Set attribute value."""
            print(f"Setting {self.name} to {value}")

        def __delete__(self, instance):
            """Delete attribute."""
            print(f"Deleting {self.name}")

    class MyClass:
        """Class using descriptor."""
        attr = Descriptor("attr")

    obj = MyClass()
    get_result = obj.attr
    obj.attr = "new value"

    return {
        "get_result": get_result,
        "note": "__get__, __set__, __delete__ define descriptor protocol",
    }


def demonstrate_data_vs_non_data() -> dict[str, Any]:
    """Demonstrate data vs non-data descriptors."""

    class DataDescriptor:
        """Data descriptor (has __get__ and __set__)."""

        def __get__(self, instance, owner):
            return "data descriptor"

        def __set__(self, instance, value):
            pass

    class NonDataDescriptor:
        """Non-data descriptor (only __get__)."""

        def __get__(self, instance, owner):
            return "non-data descriptor"

    class MyClass:
        data = DataDescriptor()
        non_data = NonDataDescriptor()

    obj = MyClass()

    # Data descriptor overrides instance __dict__
    obj.__dict__['data'] = "instance value"
    data_result = obj.data  # Returns descriptor value

    # Non-data descriptor can be overridden by instance
    obj.__dict__['non_data'] = "instance value"
    non_data_result = obj.non_data  # Returns instance value

    return {
        "data_descriptor": data_result,
        "non_data_descriptor": non_data_result,
        "note": "Data descriptors override instance dict, non-data don't",
    }


def demonstrate_validated_attribute() -> dict[str, Any]:
    """Demonstrate descriptor for attribute validation."""

    class ValidatedString:
        """Descriptor that validates string length."""

        def __init__(self, min_length: int, max_length: int):
            self.min_length = min_length
            self.max_length = max_length
            self.data = WeakKeyDictionary()

        def __get__(self, instance, owner):
            if instance is None:
                return self
            return self.data.get(instance, "")

        def __set__(self, instance, value: str):
            if not isinstance(value, str):
                raise TypeError("Value must be a string")
            if len(value) < self.min_length:
                raise ValueError(f"String too short (min {self.min_length})")
            if len(value) > self.max_length:
                raise ValueError(f"String too long (max {self.max_length})")
            self.data[instance] = value

    class Person:
        """Person with validated name."""
        name = ValidatedString(2, 50)

    person = Person()
    person.name = "Alice"
    valid_name = person.name

    # Test validation
    try:
        person.name = "X"
        error = None
    except ValueError as e:
        error = str(e)

    return {
        "valid_name": valid_name,
        "validation_error": error,
        "note": "Descriptors enable attribute validation",
    }


def demonstrate_typed_attribute() -> dict[str, Any]:
    """Demonstrate descriptor for type checking."""

    class TypedAttribute:
        """Descriptor that enforces type."""

        def __init__(self, name: str, expected_type: type):
            self.name = name
            self.expected_type = expected_type
            self.data = WeakKeyDictionary()

        def __get__(self, instance, owner):
            if instance is None:
                return self
            return self.data.get(instance)

        def __set__(self, instance, value):
            if not isinstance(value, self.expected_type):
                raise TypeError(
                    f"{self.name} must be {self.expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
            self.data[instance] = value

    class Product:
        """Product with typed attributes."""
        name = TypedAttribute("name", str)
        price = TypedAttribute("price", (int, float))
        quantity = TypedAttribute("quantity", int)

    product = Product()
    product.name = "Widget"
    product.price = 19.99
    product.quantity = 100

    # Test type enforcement
    try:
        product.quantity = "not a number"
        type_error = None
    except TypeError as e:
        type_error = str(e)

    return {
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "type_error": type_error[:30] + "...",
        "note": "Descriptors can enforce type constraints",
    }


def demonstrate_lazy_property() -> dict[str, Any]:
    """Demonstrate lazy evaluation with descriptor."""

    class LazyProperty:
        """Descriptor that computes value only once."""

        def __init__(self, function):
            self.function = function
            self.name = function.__name__
            self.data = WeakKeyDictionary()

        def __get__(self, instance, owner):
            if instance is None:
                return self

            # Check if already computed
            if instance not in self.data:
                # Compute and cache
                self.data[instance] = self.function(instance)

            return self.data[instance]

    class DataProcessor:
        """Process data lazily."""

        def __init__(self, items: list):
            self.items = items
            self.compute_count = 0

        @LazyProperty
        def expensive_sum(self):
            """Expensive computation done once."""
            self.compute_count += 1
            return sum(self.items)

        @LazyProperty
        def expensive_average(self):
            """Another expensive computation."""
            self.compute_count += 1
            return sum(self.items) / len(self.items) if self.items else 0

    processor = DataProcessor([1, 2, 3, 4, 5])

    # First access computes
    sum1 = processor.expensive_sum
    count_after_first = processor.compute_count

    # Second access uses cache
    sum2 = processor.expensive_sum
    count_after_second = processor.compute_count

    return {
        "sum_result": sum1,
        "computed_once": count_after_first,
        "not_computed_again": count_after_second,
        "note": "Lazy descriptors compute expensive values only once",
    }


def demonstrate_property_implementation() -> dict[str, Any]:
    """Demonstrate how property() is implemented as a descriptor."""

    class Property:
        """Custom property implementation."""

        def __init__(self, fget=None, fset=None, fdel=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel

        def __get__(self, instance, owner):
            if instance is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(instance)

        def __set__(self, instance, value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.fset(instance, value)

        def __delete__(self, instance):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(instance)

    class Temperature:
        """Temperature with custom property."""

        def __init__(self):
            self._celsius = 0

        def get_celsius(self):
            return self._celsius

        def set_celsius(self, value):
            if value < -273.15:
                raise ValueError("Temperature below absolute zero!")
            self._celsius = value

        celsius = Property(get_celsius, set_celsius)

    temp = Temperature()
    temp.celsius = 25
    result = temp.celsius

    return {
        "temperature": result,
        "note": "property() is implemented as a descriptor",
    }


def demonstrate_method_descriptor() -> dict[str, Any]:
    """Demonstrate how methods work as descriptors."""

    class Method:
        """Simple method descriptor."""

        def __init__(self, func):
            self.func = func

        def __get__(self, instance, owner):
            """Return bound method when accessed through instance."""
            if instance is None:
                return self.func

            # Create bound method
            def bound_method(*args, **kwargs):
                return self.func(instance, *args, **kwargs)

            return bound_method

    class MyClass:
        """Class with method descriptor."""

        @Method
        def greet(self, name):
            return f"Hello, {name}!"

    obj = MyClass()
    result = obj.greet("World")

    return {
        "result": result,
        "note": "Methods are descriptors that return bound methods",
    }


def demonstrate_class_method_descriptor() -> dict[str, Any]:
    """Demonstrate classmethod implementation with descriptor."""

    class ClassMethod:
        """Custom classmethod implementation."""

        def __init__(self, func):
            self.func = func

        def __get__(self, instance, owner):
            """Always bind to class, not instance."""

            def bound_class_method(*args, **kwargs):
                return self.func(owner, *args, **kwargs)

            return bound_class_method

    class Counter:
        """Counter with class method."""
        count = 0

        @ClassMethod
        def increment(cls):
            cls.count += 1
            return cls.count

    # Call on class
    result1 = Counter.increment()
    result2 = Counter.increment()

    # Call on instance (still binds to class)
    obj = Counter()
    result3 = obj.increment()

    return {
        "results": [result1, result2, result3],
        "final_count": Counter.count,
        "note": "classmethod descriptor binds to class, not instance",
    }


def demonstrate_static_method_descriptor() -> dict[str, Any]:
    """Demonstrate staticmethod implementation with descriptor."""

    class StaticMethod:
        """Custom staticmethod implementation."""

        def __init__(self, func):
            self.func = func

        def __get__(self, instance, owner):
            """Return function unchanged (no binding)."""
            return self.func

    class Utility:
        """Utility class with static method."""

        @StaticMethod
        def add(x, y):
            return x + y

    # Call on class
    result1 = Utility.add(5, 3)

    # Call on instance
    obj = Utility()
    result2 = obj.add(10, 7)

    return {
        "class_call": result1,
        "instance_call": result2,
        "note": "staticmethod descriptor returns function without binding",
    }


def demonstrate_descriptor_storage_strategies() -> dict[str, Any]:
    """Demonstrate different storage strategies for descriptors."""

    # Strategy 1: WeakKeyDictionary (preferred)
    class WeakDictStrategy:
        def __init__(self):
            self.data = WeakKeyDictionary()

        def __get__(self, instance, owner):
            if instance is None:
                return self
            return self.data.get(instance, "default")

        def __set__(self, instance, value):
            self.data[instance] = value

    # Strategy 2: Instance __dict__ (name mangling)
    class InstanceDictStrategy:
        def __init__(self, name):
            self.name = f"_{name}"

        def __get__(self, instance, owner):
            if instance is None:
                return self
            return getattr(instance, self.name, "default")

        def __set__(self, instance, value):
            setattr(instance, self.name, value)

    class Example:
        weak = WeakDictStrategy()
        inst = InstanceDictStrategy("inst")

    obj = Example()
    obj.weak = "weak value"
    obj.inst = "inst value"

    return {
        "weak_storage": "WeakKeyDictionary",
        "inst_storage": "Instance __dict__",
        "weak_value": obj.weak,
        "inst_value": obj.inst,
        "note": "Descriptors can use various storage strategies",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 28: Descriptors")
    print("=" * 60)

    print("\n1. Basic Descriptor:")
    basic = demonstrate_basic_descriptor()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Data vs Non-Data Descriptors:")
    data_nondata = demonstrate_data_vs_non_data()
    for key, value in data_nondata.items():
        print(f"   {key}: {value}")

    print("\n3. Validated Attribute:")
    validated = demonstrate_validated_attribute()
    for key, value in validated.items():
        print(f"   {key}: {value}")

    print("\n4. Typed Attribute:")
    typed = demonstrate_typed_attribute()
    for key, value in typed.items():
        print(f"   {key}: {value}")

    print("\n5. Lazy Property:")
    lazy = demonstrate_lazy_property()
    for key, value in lazy.items():
        print(f"   {key}: {value}")

    print("\n6. Property Implementation:")
    prop = demonstrate_property_implementation()
    for key, value in prop.items():
        print(f"   {key}: {value}")

    print("\n7. Method Descriptor:")
    method = demonstrate_method_descriptor()
    for key, value in method.items():
        print(f"   {key}: {value}")

    print("\n8. ClassMethod Descriptor:")
    classmethod_demo = demonstrate_class_method_descriptor()
    for key, value in classmethod_demo.items():
        print(f"   {key}: {value}")

    print("\n9. StaticMethod Descriptor:")
    staticmethod_demo = demonstrate_static_method_descriptor()
    for key, value in staticmethod_demo.items():
        print(f"   {key}: {value}")

    print("\n10. Storage Strategies:")
    storage = demonstrate_descriptor_storage_strategies()
    for key, value in storage.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
