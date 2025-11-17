#!/usr/bin/env python3
"""Program 19: Decorators - Master function and class decorators."""

import time
import functools
from typing import Any, Callable, TypeVar, cast


def demonstrate_basic_decorator() -> dict[str, Any]:
    """Demonstrate basic decorator concepts."""

    def simple_decorator(func: Callable) -> Callable:
        """Simple decorator that prints before and after function call."""
        def wrapper(*args, **kwargs):
            print(f"Before calling {func.__name__}")
            result = func(*args, **kwargs)
            print(f"After calling {func.__name__}")
            return result
        return wrapper

    @simple_decorator
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    # Capture output
    result = greet("Alice")

    return {
        "decorated_result": result,
        "note": "Decorator wraps function with additional behavior",
    }


def demonstrate_decorator_with_arguments() -> dict[str, Any]:
    """Demonstrate decorators that take arguments."""

    def repeat(times: int):
        """Decorator that repeats function execution."""
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                results = []
                for _ in range(times):
                    results.append(func(*args, **kwargs))
                return results
            return wrapper
        return decorator

    @repeat(times=3)
    def say_hello() -> str:
        return "Hello!"

    results = say_hello()

    return {
        "repeat_3_times": results,
        "count": len(results),
        "note": "Decorator factory pattern for parameterized decorators",
    }


def demonstrate_functools_wraps() -> dict[str, Any]:
    """Demonstrate @functools.wraps for preserving metadata."""

    # Without @wraps
    def bad_decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            """Wrapper docstring."""
            return func(*args, **kwargs)
        return wrapper

    # With @wraps
    def good_decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper docstring."""
            return func(*args, **kwargs)
        return wrapper

    @bad_decorator
    def bad_func() -> str:
        """Original docstring for bad_func."""
        return "bad"

    @good_decorator
    def good_func() -> str:
        """Original docstring for good_func."""
        return "good"

    return {
        "bad_func_name": bad_func.__name__,
        "bad_func_doc": bad_func.__doc__,
        "good_func_name": good_func.__name__,
        "good_func_doc": good_func.__doc__,
        "recommendation": "Always use @functools.wraps",
    }


def demonstrate_timing_decorator() -> dict[str, Any]:
    """Demonstrate practical timing decorator."""

    def timing_decorator(func: Callable) -> Callable:
        """Measure function execution time."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end - start:.4f} seconds")
            return result
        return wrapper

    @timing_decorator
    def slow_function() -> int:
        """Simulate slow function."""
        time.sleep(0.1)
        return 42

    result = slow_function()

    return {
        "result": result,
        "note": "Timing decorator useful for performance monitoring",
    }


def demonstrate_caching_decorator() -> dict[str, Any]:
    """Demonstrate caching with decorators."""

    # Manual cache decorator
    def memoize(func: Callable) -> Callable:
        """Cache function results."""
        cache = {}

        @functools.wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]

        wrapper.cache = cache  # Expose cache for inspection
        return wrapper

    @memoize
    def fibonacci(n: int) -> int:
        """Calculate fibonacci number."""
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    result1 = fibonacci(10)
    cache_size1 = len(fibonacci.cache)

    # Using functools.lru_cache
    @functools.lru_cache(maxsize=128)
    def fibonacci_lru(n: int) -> int:
        """Calculate fibonacci with LRU cache."""
        if n < 2:
            return n
        return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

    result2 = fibonacci_lru(10)
    cache_info = fibonacci_lru.cache_info()

    return {
        "manual_cache_result": result1,
        "manual_cache_size": cache_size1,
        "lru_cache_result": result2,
        "lru_hits": cache_info.hits,
        "lru_misses": cache_info.misses,
    }


def demonstrate_validation_decorator() -> dict[str, Any]:
    """Demonstrate validation decorator."""

    def validate_positive(func: Callable) -> Callable:
        """Validate that all arguments are positive."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (int, float)) and arg <= 0:
                    raise ValueError(f"Argument must be positive, got {arg}")
            return func(*args, **kwargs)
        return wrapper

    @validate_positive
    def divide(a: float, b: float) -> float:
        """Divide two numbers."""
        return a / b

    # Test valid input
    valid_result = divide(10, 2)

    # Test invalid input
    error_caught = False
    try:
        invalid_result = divide(10, -2)
    except ValueError:
        error_caught = True

    return {
        "valid_result": valid_result,
        "validation_works": error_caught,
        "note": "Decorators great for cross-cutting concerns",
    }


def demonstrate_multiple_decorators() -> dict[str, Any]:
    """Demonstrate stacking multiple decorators."""

    def uppercase(func: Callable) -> Callable:
        """Convert result to uppercase."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper

    def exclaim(func: Callable) -> Callable:
        """Add exclamation marks."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{result}!!!"
        return wrapper

    # Order matters: bottom to top execution
    @exclaim
    @uppercase
    def greet(name: str) -> str:
        return f"hello {name}"

    result = greet("alice")

    return {
        "result": result,
        "order": "Decorators applied bottom-to-top",
        "execution": "exclaim(uppercase(greet))",
    }


def demonstrate_class_decorator() -> dict[str, Any]:
    """Demonstrate class-based decorators."""

    class CountCalls:
        """Decorator class that counts function calls."""

        def __init__(self, func: Callable):
            functools.update_wrapper(self, func)
            self.func = func
            self.count = 0

        def __call__(self, *args, **kwargs):
            self.count += 1
            return self.func(*args, **kwargs)

    @CountCalls
    def say_hello() -> str:
        return "Hello!"

    # Call multiple times
    say_hello()
    say_hello()
    say_hello()

    return {
        "call_count": say_hello.count,
        "last_result": say_hello(),
        "final_count": say_hello.count,
        "note": "Class decorators maintain state via instance",
    }


def demonstrate_property_decorator() -> dict[str, Any]:
    """Demonstrate @property decorator."""

    class Circle:
        """Circle class with property decorators."""

        def __init__(self, radius: float):
            self._radius = radius

        @property
        def radius(self) -> float:
            """Get radius."""
            return self._radius

        @radius.setter
        def radius(self, value: float) -> None:
            """Set radius with validation."""
            if value <= 0:
                raise ValueError("Radius must be positive")
            self._radius = value

        @property
        def area(self) -> float:
            """Calculate area (read-only)."""
            return 3.14159 * self._radius ** 2

        @property
        def diameter(self) -> float:
            """Get diameter."""
            return self._radius * 2

        @diameter.setter
        def diameter(self, value: float) -> None:
            """Set diameter."""
            self.radius = value / 2

    circle = Circle(5)
    initial_area = circle.area

    circle.radius = 10
    new_area = circle.area

    circle.diameter = 20
    diameter_radius = circle.radius

    return {
        "initial_area": f"{initial_area:.2f}",
        "new_area": f"{new_area:.2f}",
        "diameter_radius": diameter_radius,
        "note": "@property makes methods look like attributes",
    }


def demonstrate_staticmethod_classmethod() -> dict[str, Any]:
    """Demonstrate @staticmethod and @classmethod."""

    class MathOperations:
        """Class demonstrating different method types."""

        class_variable = "MathOps"

        def __init__(self, name: str):
            self.name = name

        # Instance method (has access to self)
        def instance_method(self, x: int) -> str:
            return f"{self.name}: {x}"

        # Static method (no access to self or cls)
        @staticmethod
        def add(a: int, b: int) -> int:
            """Static method - utility function."""
            return a + b

        # Class method (has access to cls)
        @classmethod
        def multiply_by_two(cls, x: int) -> str:
            """Class method - can access class variables."""
            return f"{cls.class_variable}: {x * 2}"

        @classmethod
        def create(cls, name: str) -> 'MathOperations':
            """Factory method."""
            return cls(name)

    # Use static method (no instance needed)
    static_result = MathOperations.add(5, 3)

    # Use class method (no instance needed)
    class_result = MathOperations.multiply_by_two(5)

    # Use factory class method
    instance = MathOperations.create("Calculator")
    instance_result = instance.instance_method(10)

    return {
        "static_method": static_result,
        "class_method": class_result,
        "factory_instance": instance_result,
        "note": "@staticmethod: utility, @classmethod: factory/alternative constructors",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 19: Decorators")
    print("=" * 60)

    print("\n1. Basic Decorator:")
    basic = demonstrate_basic_decorator()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Decorator with Arguments:")
    args_dec = demonstrate_decorator_with_arguments()
    for key, value in args_dec.items():
        print(f"   {key}: {value}")

    print("\n3. functools.wraps:")
    wraps = demonstrate_functools_wraps()
    for key, value in wraps.items():
        print(f"   {key}: {value}")

    print("\n4. Timing Decorator:")
    timing = demonstrate_timing_decorator()
    for key, value in timing.items():
        print(f"   {key}: {value}")

    print("\n5. Caching Decorator:")
    caching = demonstrate_caching_decorator()
    for key, value in caching.items():
        print(f"   {key}: {value}")

    print("\n6. Validation Decorator:")
    validation = demonstrate_validation_decorator()
    for key, value in validation.items():
        print(f"   {key}: {value}")

    print("\n7. Multiple Decorators:")
    multiple = demonstrate_multiple_decorators()
    for key, value in multiple.items():
        print(f"   {key}: {value}")

    print("\n8. Class Decorator:")
    class_dec = demonstrate_class_decorator()
    for key, value in class_dec.items():
        print(f"   {key}: {value}")

    print("\n9. Property Decorator:")
    prop = demonstrate_property_decorator()
    for key, value in prop.items():
        print(f"   {key}: {value}")

    print("\n10. Static and Class Methods:")
    methods = demonstrate_staticmethod_classmethod()
    for key, value in methods.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
