# 06_functions

## Description

Master Python functions with comprehensive demonstrations of function definitions, parameters, return values, lambda functions, recursion, closures, and advanced function concepts. This program covers everything from basic function syntax to advanced patterns like *args, **kwargs, and nested functions.

This is Program #6 in the 500 Programs Collection.

## Learning Objectives

- Understand function definition and calling syntax
- Master different parameter types (positional, default, keyword)
- Work with variable arguments (*args and **kwargs)
- Learn recursive function patterns
- Understand closures and nested functions
- Use lambda functions effectively
- Return multiple values from functions
- Apply function best practices

## Features

- Basic function definitions with parameters and return values
- Default parameter values
- Multiple return values using dictionaries
- Variable positional arguments (*args)
- Variable keyword arguments (**kwargs)
- Recursive functions (Fibonacci example)
- Lambda functions for simple operations
- Nested functions and closures
- Comprehensive demonstrations with examples

## Usage

```bash
python src/main.py
```

## Example Output

```
============================================================
Program 06: Functions
============================================================

Basic function: Hello, World!
With parameter: Hello, Python!
Add: 8
Power: 9 = 9
Stats: {'sum': 15, 'avg': 3.0, 'min': 1, 'max': 5}
*args: [1, 2, 3]
**kwargs: {'a': 1, 'b': 2}
Fibonacci(7): 13
Lambda: 10
Closure: 15

============================================================
✅ Program completed!
============================================================
```

## Key Concepts

### 1. Basic Function Definition

```python
def greet(name: str = "World") -> str:
    """Function with default parameter."""
    return f"Hello, {name}!"
```

- Use `def` keyword to define functions
- Parameters can have default values
- Type hints improve code clarity
- `return` statement returns a value

### 2. Multiple Parameters

```python
def add(a: int, b: int) -> int:
    """Function with multiple parameters."""
    return a + b
```

### 3. Returning Multiple Values

```python
def calculate_stats(numbers: List[int]) -> dict[str, float]:
    """Return multiple values via dictionary."""
    return {
        "sum": sum(numbers),
        "avg": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }
```

### 4. Variable Arguments (*args)

```python
def print_args(*args) -> List[Any]:
    """Accept variable number of positional arguments."""
    return list(args)

# Usage: print_args(1, 2, 3, 4, 5)
```

### 5. Keyword Arguments (**kwargs)

```python
def print_kwargs(**kwargs) -> dict[str, Any]:
    """Accept variable number of keyword arguments."""
    return kwargs

# Usage: print_kwargs(name="Alice", age=25, city="NYC")
```

### 6. Recursive Functions

```python
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 7. Lambda Functions

```python
# Anonymous function for simple operations
lambda_double = lambda x: x * 2
result = lambda_double(5)  # 10
```

### 8. Closures (Nested Functions)

```python
def outer_function(x: int) -> callable:
    """Return inner function that remembers x."""
    def inner_function(y: int) -> int:
        return x + y
    return inner_function

add_ten = outer_function(10)
result = add_ten(5)  # 15
```

## Best Practices

1. **Use Descriptive Names**: Function names should clearly indicate what they do
   ```python
   def calculate_total_price(items):  # Good
   def calc(x):  # Bad
   ```

2. **Single Responsibility**: Each function should do one thing well
   ```python
   def validate_email(email):  # Good - single purpose
   def validate_and_send_email(email):  # Bad - two purposes
   ```

3. **Use Type Hints**: Makes code more readable and catches errors early
   ```python
   def greet(name: str) -> str:  # Good
   def greet(name):  # Less clear
   ```

4. **Document with Docstrings**: Explain what the function does
   ```python
   def calculate_area(radius: float) -> float:
       """Calculate circle area given radius."""
       return 3.14159 * radius ** 2
   ```

5. **Default Arguments**: Use mutable defaults carefully
   ```python
   # Good
   def create_list(items: List = None) -> List:
       if items is None:
           items = []
       return items

   # Bad - mutable default
   def create_list(items: List = []) -> List:
       return items
   ```

6. **Keep Functions Short**: Aim for 10-20 lines when possible

7. **Avoid Deep Nesting**: Keep it flat and readable

8. **Return Early**: Use guard clauses for cleaner code
   ```python
   def process(value):
       if not value:
           return None
       # Continue processing
   ```

## Testing

Run the program to see all function demonstrations:

```bash
# Run main program
python src/main.py

# Run with Python directly
python3 src/main.py
```

## Common Patterns

### Function as First-Class Objects

```python
# Functions can be assigned to variables
operation = add

# Functions can be passed as arguments
def apply_operation(func, a, b):
    return func(a, b)

result = apply_operation(add, 5, 3)
```

### Factory Functions

```python
def create_multiplier(factor):
    """Return function that multiplies by factor."""
    def multiply(x):
        return x * factor
    return multiply

double = create_multiplier(2)
triple = create_multiplier(3)
```

## Related Concepts

- **Decorators** (Program 19): Advanced function wrapping
- **Lambda Functions**: One-line anonymous functions
- **Generators** (Program 20): Functions that yield values
- **Methods**: Functions inside classes (Program 14)

---

**Program**: 06 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics
**Estimated Time**: 30-45 minutes

[← Previous (05)](../05_loops/) | [Back to Index](../../docs/INDEX.md) | [Next (07) →](../07_lists/)
