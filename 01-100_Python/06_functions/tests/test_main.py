"""
Unit tests for 06_functions program.

These tests verify:
- Function definitions and usage
- Parameter handling (default, *args, **kwargs)
- Return values
- Recursive functions
- Lambda functions
- Closures
- Edge cases
"""

import sys
from pathlib import Path
from typing import Callable

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    greet,
    add,
    calculate_stats,
    power,
    print_args,
    print_kwargs,
    fibonacci,
    outer_function,
    lambda_double,
    main,
)


class TestGreetFunction:
    """Test cases for the greet() function."""

    def test_greet_default(self):
        """Test greeting with default parameter."""
        result = greet()
        assert result == "Hello, World!"

    def test_greet_with_name(self):
        """Test greeting with specific name."""
        result = greet("Python")
        assert result == "Hello, Python!"

    def test_greet_empty_string(self):
        """Test greeting with empty string."""
        result = greet("")
        assert result == "Hello, !"

    def test_greet_special_characters(self):
        """Test greeting with special characters."""
        result = greet("Test-123!")
        assert result == "Hello, Test-123!!"


class TestAddFunction:
    """Test cases for the add() function."""

    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        assert add(5, 3) == 8
        assert add(10, 20) == 30

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add(-5, -3) == -8
        assert add(-10, 5) == -5

    def test_add_zeros(self):
        """Test adding with zeros."""
        assert add(0, 0) == 0
        assert add(5, 0) == 5
        assert add(0, 5) == 5

    def test_add_large_numbers(self):
        """Test adding large numbers."""
        assert add(1000000, 2000000) == 3000000


class TestCalculateStats:
    """Test cases for the calculate_stats() function."""

    def test_basic_stats(self):
        """Test basic statistics calculation."""
        result = calculate_stats([1, 2, 3, 4, 5])
        assert result["sum"] == 15
        assert result["avg"] == 3.0
        assert result["min"] == 1
        assert result["max"] == 5

    def test_single_element(self):
        """Test with single element list."""
        result = calculate_stats([42])
        assert result["sum"] == 42
        assert result["avg"] == 42.0
        assert result["min"] == 42
        assert result["max"] == 42

    def test_empty_list(self):
        """Test with empty list."""
        result = calculate_stats([])
        assert result["sum"] == 0
        assert result["avg"] == 0
        assert result["min"] == 0
        assert result["max"] == 0

    def test_negative_numbers(self):
        """Test with negative numbers."""
        result = calculate_stats([-5, -3, -1])
        assert result["sum"] == -9
        assert result["avg"] == -3.0
        assert result["min"] == -5
        assert result["max"] == -1

    def test_mixed_numbers(self):
        """Test with mixed positive and negative numbers."""
        result = calculate_stats([-10, 0, 10])
        assert result["sum"] == 0
        assert result["avg"] == 0.0
        assert result["min"] == -10
        assert result["max"] == 10


class TestPowerFunction:
    """Test cases for the power() function."""

    def test_power_default_exponent(self):
        """Test power with default exponent (2)."""
        assert power(3) == 9
        assert power(5) == 25

    def test_power_custom_exponent(self):
        """Test power with custom exponent."""
        assert power(2, 3) == 8
        assert power(3, 3) == 27
        assert power(5, 0) == 1

    def test_power_zero_base(self):
        """Test power with zero base."""
        assert power(0) == 0
        assert power(0, 5) == 0

    def test_power_negative_base(self):
        """Test power with negative base."""
        assert power(-2, 2) == 4
        assert power(-2, 3) == -8


class TestPrintArgs:
    """Test cases for the print_args() function."""

    def test_no_arguments(self):
        """Test with no arguments."""
        result = print_args()
        assert result == []

    def test_single_argument(self):
        """Test with single argument."""
        result = print_args(1)
        assert result == [1]

    def test_multiple_arguments(self):
        """Test with multiple arguments."""
        result = print_args(1, 2, 3)
        assert result == [1, 2, 3]

    def test_mixed_types(self):
        """Test with mixed argument types."""
        result = print_args(1, "hello", 3.14, True, None)
        assert result == [1, "hello", 3.14, True, None]


class TestPrintKwargs:
    """Test cases for the print_kwargs() function."""

    def test_no_kwargs(self):
        """Test with no keyword arguments."""
        result = print_kwargs()
        assert result == {}

    def test_single_kwarg(self):
        """Test with single keyword argument."""
        result = print_kwargs(a=1)
        assert result == {"a": 1}

    def test_multiple_kwargs(self):
        """Test with multiple keyword arguments."""
        result = print_kwargs(a=1, b=2, c=3)
        assert result == {"a": 1, "b": 2, "c": 3}

    def test_mixed_value_types(self):
        """Test with mixed value types."""
        result = print_kwargs(num=42, text="hello", flag=True)
        assert result == {"num": 42, "text": "hello", "flag": True}


class TestFibonacci:
    """Test cases for the fibonacci() function."""

    def test_fibonacci_base_cases(self):
        """Test Fibonacci base cases."""
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_fibonacci_sequence(self):
        """Test Fibonacci sequence values."""
        assert fibonacci(2) == 1
        assert fibonacci(3) == 2
        assert fibonacci(4) == 3
        assert fibonacci(5) == 5
        assert fibonacci(6) == 8
        assert fibonacci(7) == 13

    def test_fibonacci_larger_values(self):
        """Test larger Fibonacci values."""
        assert fibonacci(10) == 55
        assert fibonacci(15) == 610


class TestOuterFunction:
    """Test cases for the outer_function() closure."""

    def test_closure_basic(self):
        """Test basic closure functionality."""
        add_five = outer_function(5)
        assert add_five(3) == 8
        assert add_five(10) == 15

    def test_closure_different_values(self):
        """Test closure with different outer values."""
        add_ten = outer_function(10)
        add_twenty = outer_function(20)

        assert add_ten(5) == 15
        assert add_twenty(5) == 25

    def test_closure_returns_callable(self):
        """Test that outer_function returns a callable."""
        inner = outer_function(1)
        assert callable(inner)

    def test_closure_negative_values(self):
        """Test closure with negative values."""
        add_neg = outer_function(-5)
        assert add_neg(10) == 5
        assert add_neg(-3) == -8


class TestLambdaDouble:
    """Test cases for the lambda_double function."""

    def test_lambda_positive_numbers(self):
        """Test lambda with positive numbers."""
        assert lambda_double(5) == 10
        assert lambda_double(3) == 6

    def test_lambda_zero(self):
        """Test lambda with zero."""
        assert lambda_double(0) == 0

    def test_lambda_negative_numbers(self):
        """Test lambda with negative numbers."""
        assert lambda_double(-5) == -10

    def test_lambda_float_numbers(self):
        """Test lambda with float numbers."""
        assert lambda_double(2.5) == 5.0


class TestMainFunction:
    """Test cases for the main() function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    def test_main_output(self, capsys):
        """Test that main produces expected output."""
        main()
        captured = capsys.readouterr()

        assert "Program 06: Functions" in captured.out
        assert "Basic function:" in captured.out
        assert "Add:" in captured.out
        assert "Power:" in captured.out
        assert "Stats:" in captured.out
        assert "*args:" in captured.out
        assert "**kwargs:" in captured.out
        assert "Fibonacci(7):" in captured.out
        assert "Lambda:" in captured.out
        assert "Closure:" in captured.out

    def test_main_shows_results(self, capsys):
        """Test that main shows correct results."""
        main()
        captured = capsys.readouterr()

        # Check for expected values
        assert "13" in captured.out  # Fibonacci(7)
        assert "10" in captured.out  # lambda_double(5)
        assert "15" in captured.out  # closure result


class TestIntegration:
    """Integration tests for the complete program."""

    def test_all_functions_work_together(self):
        """Test that all functions can be used together."""
        # Test basic functions
        greeting = greet("Test")
        sum_result = add(5, 3)
        stats = calculate_stats([1, 2, 3, 4, 5])

        # Test advanced functions
        fib = fibonacci(5)
        closure = outer_function(10)
        closure_result = closure(5)

        # Verify all results are correct
        assert greeting == "Hello, Test!"
        assert sum_result == 8
        assert stats["avg"] == 3.0
        assert fib == 5
        assert closure_result == 15

    def test_function_composition(self):
        """Test composing functions together."""
        # Use one function's output as another's input
        numbers = list(range(1, 6))
        stats = calculate_stats(numbers)
        result = power(int(stats["avg"]), 2)

        assert result == 9  # avg is 3, 3^2 is 9


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_power_with_one(self):
        """Test power with base 1."""
        assert power(1, 100) == 1
        assert power(1, 0) == 1

    def test_fibonacci_performance(self):
        """Test that fibonacci doesn't take too long for reasonable inputs."""
        import time
        start = time.time()
        result = fibonacci(20)
        elapsed = time.time() - start

        assert result == 6765
        assert elapsed < 1.0  # Should complete in less than 1 second

    def test_args_and_kwargs_together(self):
        """Test that *args and **kwargs can work in combination."""
        # While not demonstrated in main functions, good to verify understanding
        args_result = print_args(1, 2, 3)
        kwargs_result = print_kwargs(a=1, b=2)

        assert len(args_result) == 3
        assert len(kwargs_result) == 2


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
