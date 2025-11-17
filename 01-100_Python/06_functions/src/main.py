#!/usr/bin/env python3
"""Program 06: Functions - Master function definitions and usage."""

from typing import Any, Optional, List, Tuple


def greet(name: str = "World") -> str:
    """Basic function with default parameter."""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Function with multiple parameters."""
    return a + b


def calculate_stats(numbers: List[int]) -> dict[str, float]:
    """Function returning multiple values via dict."""
    return {
        "sum": sum(numbers),
        "avg": sum(numbers) / len(numbers) if numbers else 0,
        "min": min(numbers) if numbers else 0,
        "max": max(numbers) if numbers else 0,
    }


def power(base: int, exp: int = 2) -> int:
    """Function with default parameter."""
    return base ** exp


def print_args(*args) -> List[Any]:
    """Function with *args (variable positional arguments)."""
    return list(args)


def print_kwargs(**kwargs) -> dict[str, Any]:
    """Function with **kwargs (variable keyword arguments)."""
    return kwargs


def fibonacci(n: int) -> int:
    """Recursive function."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def outer_function(x: int) -> callable:
    """Nested function (closure)."""
    def inner_function(y: int) -> int:
        return x + y
    return inner_function


lambda_double = lambda x: x * 2  # Lambda function


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 06: Functions")
    print("=" * 60)
    
    print(f"\nBasic function: {greet()}")
    print(f"With parameter: {greet('Python')}")
    print(f"Add: {add(5, 3)}")
    print(f"Power: {power(3)} = {power(3, 2)}")
    print(f"Stats: {calculate_stats([1, 2, 3, 4, 5])}")
    print(f"*args: {print_args(1, 2, 3)}")
    print(f"**kwargs: {print_kwargs(a=1, b=2)}")
    print(f"Fibonacci(7): {fibonacci(7)}")
    print(f"Lambda: {lambda_double(5)}")
    
    add_ten = outer_function(10)
    print(f"Closure: {add_ten(5)}")
    
    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
