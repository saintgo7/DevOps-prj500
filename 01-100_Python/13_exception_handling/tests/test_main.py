"""
Unit tests for 13_exception_handling program.

These tests verify:
- Basic exception handling
- Multiple exception types
- Exception hierarchy
- Else and finally clauses
- Raising exceptions
- Custom exceptions
- Context managers
- Exception chaining
- Assertions
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_exceptions,
    demonstrate_multiple_exceptions,
    demonstrate_exception_hierarchy,
    demonstrate_else_finally,
    demonstrate_raising_exceptions,
    demonstrate_custom_exceptions,
    demonstrate_context_managers,
    demonstrate_exception_chaining,
    demonstrate_assertions,
    main,
)


class TestBasicExceptions:
    """Test cases for demonstrate_basic_exceptions()."""

    def test_successful_division(self):
        """Test successful division."""
        result = demonstrate_basic_exceptions()
        assert result["division_success"]["result"] == 5.0
        assert result["division_success"]["success"] is True

    def test_zero_division_error(self):
        """Test zero division error handling."""
        result = demonstrate_basic_exceptions()
        assert "Error" in result["division_error"]

    def test_multiple_operations(self):
        """Test multiple operations with error handling."""
        result = demonstrate_basic_exceptions()
        results = result["multiple_operations"]
        assert results[0] == 5.0
        assert results[1] == "Error"
        assert results[2] == 2.0


class TestMultipleExceptions:
    """Test cases for demonstrate_multiple_exceptions()."""

    def test_value_error_handling(self):
        """Test ValueError handling."""
        result = demonstrate_multiple_exceptions()
        assert "ValueError" in result["value_error"]

    def test_zero_division_handling(self):
        """Test ZeroDivisionError handling."""
        result = demonstrate_multiple_exceptions()
        assert "ZeroDivisionError" in result["zero_division"]

    def test_index_error_handling(self):
        """Test IndexError handling."""
        result = demonstrate_multiple_exceptions()
        assert "IndexError" in result["index_error"]

    def test_successful_operation(self):
        """Test successful operation."""
        result = demonstrate_multiple_exceptions()
        assert "Success" in result["success"]


class TestExceptionHierarchy:
    """Test cases for demonstrate_exception_hierarchy()."""

    def test_specific_zero_division(self):
        """Test specific ZeroDivisionError caught."""
        result = demonstrate_exception_hierarchy()
        assert "ZeroDivisionError" in result["specific_zero"]

    def test_specific_value_error(self):
        """Test specific ValueError caught."""
        result = demonstrate_exception_hierarchy()
        assert "ValueError" in result["specific_value"]

    def test_arithmetic_error_base(self):
        """Test ArithmeticError base class."""
        result = demonstrate_exception_hierarchy()
        assert "ArithmeticError" in result["arithmetic_error"]


class TestElseFinally:
    """Test cases for demonstrate_else_finally()."""

    def test_successful_division_with_else(self):
        """Test successful division triggers else clause."""
        result = demonstrate_else_finally()
        success_case = result["success_case"]
        assert success_case["result"] == 5.0
        assert "else executed" in success_case["log"]
        assert "Finally always executes" in success_case["log"]

    def test_error_division_no_else(self):
        """Test error case skips else clause."""
        result = demonstrate_else_finally()
        error_case = result["error_case"]
        assert error_case["result"] is None
        assert "Error occurred" in error_case["log"]
        assert "Finally always executes" in error_case["log"]

    def test_file_operation_cleanup(self):
        """Test finally clause for cleanup."""
        result = demonstrate_else_finally()
        file_op = result["file_operation"]
        assert "File not found" in file_op["log"]
        assert "No file to close" in file_op["log"]


class TestRaisingExceptions:
    """Test cases for demonstrate_raising_exceptions()."""

    def test_valid_age(self):
        """Test valid age."""
        result = demonstrate_raising_exceptions()
        assert "Valid age: 25" in result["valid_age"]

    def test_negative_age(self):
        """Test negative age raises error."""
        result = demonstrate_raising_exceptions()
        assert "Error" in result["negative_age"]
        assert "negative" in result["negative_age"].lower()

    def test_convert_exception(self):
        """Test exception conversion."""
        result = demonstrate_raising_exceptions()
        assert "Error" in result["convert_error"]


class TestCustomExceptions:
    """Test cases for demonstrate_custom_exceptions()."""

    def test_valid_email(self):
        """Test valid email."""
        result = demonstrate_custom_exceptions()
        assert "Valid email" in result["valid_email"]

    def test_invalid_email(self):
        """Test invalid email raises custom exception."""
        result = demonstrate_custom_exceptions()
        assert "Error" in result["invalid_email"]

    def test_user_found(self):
        """Test user found."""
        result = demonstrate_custom_exceptions()
        assert result["user_found"] == "Alice"

    def test_user_not_found(self):
        """Test user not found raises custom exception."""
        result = demonstrate_custom_exceptions()
        assert "Error" in result["user_not_found"]
        assert "999" in result["user_not_found"]


class TestContextManagers:
    """Test cases for demonstrate_context_managers()."""

    def test_file_write_success(self):
        """Test file write with context manager."""
        result = demonstrate_context_managers()
        assert result["file_write"] == "Success"

    def test_error_logger(self):
        """Test custom error logger context manager."""
        result = demonstrate_context_managers()
        errors = result["error_logger"]
        assert len(errors) == 1
        assert "ValueError" in errors[0]


class TestExceptionChaining:
    """Test cases for demonstrate_exception_chaining()."""

    def test_explicit_chaining(self):
        """Test explicit exception chaining."""
        result = demonstrate_exception_chaining()
        assert "TypeError" in result["explicit_chain"]
        assert "ValueError" in result["explicit_chain"]


class TestAssertions:
    """Test cases for demonstrate_assertions()."""

    def test_valid_list(self):
        """Test valid list."""
        result = demonstrate_assertions()
        assert result["valid_list"] == 3.0

    def test_empty_list_assertion(self):
        """Test empty list triggers assertion."""
        result = demonstrate_assertions()
        assert "AssertionError" in result["empty_list"]


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

        assert "Program 13: Exception Handling" in captured.out
        assert "Basic Exceptions:" in captured.out


class TestIntegration:
    """Integration tests for exception handling."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_basic_exceptions,
            demonstrate_multiple_exceptions,
            demonstrate_exception_hierarchy,
            demonstrate_else_finally,
            demonstrate_raising_exceptions,
            demonstrate_custom_exceptions,
            demonstrate_context_managers,
            demonstrate_exception_chaining,
            demonstrate_assertions,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
