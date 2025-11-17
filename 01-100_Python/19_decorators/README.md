# 19_decorators

## Description

Master Python decorators - powerful tools for modifying function and class behavior. Learn function decorators, decorators with arguments, @functools.wraps, class decorators, @property, @staticmethod, @classmethod, and practical decorator patterns.

This is Program #19 in the 500 Programs Collection.

## Learning Objectives

- Understand decorator concepts and syntax
- Create function decorators
- Use decorators with arguments
- Apply @functools.wraps for metadata preservation
- Build practical decorators (timing, caching, validation)
- Stack multiple decorators
- Use class-based decorators
- Master built-in decorators (@property, @staticmethod, @classmethod)

## Features

- Basic function decorators
- Decorators with arguments
- @functools.wraps usage
- Timing decorator
- Caching decorator (manual and @lru_cache)
- Validation decorator
- Multiple decorator stacking
- Class-based decorators
- @property decorator
- @staticmethod and @classmethod

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Decorator

```python
def simple_decorator(func):
    """Wrap function with additional behavior."""
    def wrapper(*args, **kwargs):
        print(f"Before {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After {func.__name__}")
        return result
    return wrapper

@simple_decorator
def greet(name):
    return f"Hello, {name}!"

# Same as: greet = simple_decorator(greet)
```

### 2. Decorator with Arguments

```python
def repeat(times):
    """Decorator factory."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    return "Hello!"

# say_hello() returns ["Hello!", "Hello!", "Hello!"]
```

### 3. @functools.wraps

```python
import functools

def good_decorator(func):
    @functools.wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_function():
    """Original docstring."""
    pass

# Metadata preserved
print(my_function.__name__)  # "my_function"
print(my_function.__doc__)   # "Original docstring."
```

### 4. Timing Decorator

```python
import time
import functools

def timing_decorator(func):
    """Measure execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.4f}s")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    return 42
```

### 5. Caching Decorator

```python
# Manual cache
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Built-in LRU cache
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)
```

### 6. Validation Decorator

```python
def validate_positive(func):
    """Validate all arguments are positive."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"Argument must be positive: {arg}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def divide(a, b):
    return a / b
```

### 7. Multiple Decorators

```python
@decorator1
@decorator2
@decorator3
def my_function():
    pass

# Equivalent to:
# my_function = decorator1(decorator2(decorator3(my_function)))
# Applied bottom to top
```

### 8. Class-Based Decorator

```python
class CountCalls:
    """Decorator that counts function calls."""
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    return "Hello!"

say_hello()
print(say_hello.count)  # 1
```

### 9. @property Decorator

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """Getter."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter with validation."""
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self):
        """Computed property."""
        return 3.14159 * self._radius ** 2

circle = Circle(5)
circle.radius = 10  # Uses setter
print(circle.area)  # Uses getter
```

### 10. @staticmethod and @classmethod

```python
class MathOps:
    class_var = "MathOps"

    def __init__(self, name):
        self.name = name

    # Instance method
    def instance_method(self, x):
        return f"{self.name}: {x}"

    # Static method (no self or cls)
    @staticmethod
    def add(a, b):
        return a + b

    # Class method (has cls)
    @classmethod
    def multiply_by_two(cls, x):
        return f"{cls.class_var}: {x * 2}"

    @classmethod
    def create(cls, name):
        """Factory method."""
        return cls(name)

# Usage
MathOps.add(5, 3)  # No instance needed
MathOps.multiply_by_two(5)
instance = MathOps.create("Calculator")
```

## Best Practices

1. **Always Use @functools.wraps**
2. **Keep Decorators Simple**
3. **Use Descriptive Names**
4. **Document Side Effects**
5. **Consider Performance Impact**

## Common Use Cases

- **Logging**: Log function calls
- **Timing**: Measure performance
- **Caching**: Memoize results
- **Validation**: Check inputs
- **Authentication**: Verify permissions
- **Rate Limiting**: Control call frequency

## Testing

```bash
python src/main.py
```

---

**Program**: 19 of 500
**Difficulty**: ⭐⭐⭐ Intermediate/Advanced
**Category**: Python Advanced
**Estimated Time**: 60-90 minutes

[← Previous (18)](../18_packages/) | [Back to Index](../../docs/INDEX.md) | [Next (20) →](../20_generators/)
