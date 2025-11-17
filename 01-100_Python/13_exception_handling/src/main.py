#!/usr/bin/env python3
"""Program 13: Exception Handling - Master error handling in Python."""

from typing import Any, Optional, List
import sys


def demonstrate_basic_exceptions() -> dict[str, Any]:
    """Demonstrate basic exception handling."""
    # Try-except
    try:
        result = 10 / 2
        success = True
        error = None
    except ZeroDivisionError as e:
        result = None
        success = False
        error = str(e)

    # Catching ZeroDivisionError
    try:
        bad_result = 10 / 0
    except ZeroDivisionError as e:
        bad_result = f"Error: {e}"

    # Multiple operations
    results = []
    for divisor in [2, 0, 5]:
        try:
            results.append(10 / divisor)
        except ZeroDivisionError:
            results.append("Error")

    return {
        "division_success": {"result": result, "success": success},
        "division_error": bad_result,
        "multiple_operations": results,
    }


def demonstrate_multiple_exceptions() -> dict[str, Any]:
    """Demonstrate handling multiple exception types."""
    def safe_operation(value: str, index: int) -> str:
        try:
            # Could raise ValueError
            num = int(value)
            # Could raise ZeroDivisionError
            result = 100 / num
            # Could raise IndexError
            data = [1, 2, 3]
            item = data[index]
            return f"Success: {result}, {item}"
        except ValueError as e:
            return f"ValueError: {e}"
        except ZeroDivisionError as e:
            return f"ZeroDivisionError: {e}"
        except IndexError as e:
            return f"IndexError: {e}"

    # Multiple exception types in one except
    def safe_convert(value: str) -> str:
        try:
            num = int(value)
            result = 100 / num
            return f"Result: {result}"
        except (ValueError, ZeroDivisionError) as e:
            return f"Error: {type(e).__name__} - {e}"

    return {
        "value_error": safe_operation("abc", 0),
        "zero_division": safe_operation("0", 0),
        "index_error": safe_operation("5", 10),
        "success": safe_operation("5", 1),
        "combined_value": safe_convert("abc"),
        "combined_zero": safe_convert("0"),
    }


def demonstrate_exception_hierarchy() -> dict[str, Any]:
    """Demonstrate exception hierarchy."""
    def catch_specific_first(value: str) -> str:
        try:
            num = int(value)
            result = 100 / num
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Caught ZeroDivisionError (specific)"
        except ValueError:
            return "Caught ValueError (specific)"
        except Exception as e:
            return f"Caught general Exception: {type(e).__name__}"

    # Catching base exceptions
    def catch_arithmetic(divisor: int) -> str:
        try:
            return str(100 / divisor)
        except ArithmeticError:  # Base class for ZeroDivisionError
            return "Caught ArithmeticError"

    return {
        "specific_zero": catch_specific_first("0"),
        "specific_value": catch_specific_first("abc"),
        "arithmetic_error": catch_arithmetic(0),
    }


def demonstrate_else_finally() -> dict[str, Any]:
    """Demonstrate else and finally clauses."""
    # Else clause (runs if no exception)
    def divide_with_else(a: int, b: int) -> dict:
        log = []
        try:
            result = a / b
            log.append("Division attempted")
        except ZeroDivisionError:
            log.append("Error occurred")
            result = None
        else:
            log.append("No error - else executed")
        finally:
            log.append("Finally always executes")

        return {"result": result, "log": log}

    # Finally with file operations
    def safe_file_operation() -> dict:
        log = []
        file_handle = None
        try:
            file_handle = open("nonexistent.txt", "r")
            content = file_handle.read()
            log.append("File read successfully")
        except FileNotFoundError:
            log.append("File not found")
            content = None
        finally:
            if file_handle:
                file_handle.close()
                log.append("File closed")
            else:
                log.append("No file to close")

        return {"content": content, "log": log}

    return {
        "success_case": divide_with_else(10, 2),
        "error_case": divide_with_else(10, 0),
        "file_operation": safe_file_operation(),
    }


def demonstrate_raising_exceptions() -> dict[str, Any]:
    """Demonstrate raising exceptions."""
    def validate_age(age: int) -> str:
        if age < 0:
            raise ValueError("Age cannot be negative")
        if age > 150:
            raise ValueError("Age seems unrealistic")
        return f"Valid age: {age}"

    # Re-raising exceptions
    def process_with_reraise(value: str) -> str:
        try:
            num = int(value)
            if num < 0:
                raise ValueError("Negative numbers not allowed")
            return f"Processed: {num}"
        except ValueError:
            print("Logging error before re-raising")
            raise  # Re-raise the same exception

    # Custom error message when re-raising
    def convert_exception(value: str) -> str:
        try:
            return str(100 / int(value))
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero") from None

    results = {}

    # Test validate_age
    try:
        results["valid_age"] = validate_age(25)
    except ValueError as e:
        results["valid_age"] = f"Error: {e}"

    try:
        results["negative_age"] = validate_age(-5)
    except ValueError as e:
        results["negative_age"] = f"Error: {e}"

    # Test convert_exception
    try:
        results["convert_error"] = convert_exception("0")
    except ValueError as e:
        results["convert_error"] = f"Error: {e}"

    return results


def demonstrate_custom_exceptions() -> dict[str, Any]:
    """Demonstrate custom exception classes."""
    # Define custom exceptions
    class InvalidEmailError(Exception):
        """Raised when email format is invalid."""
        pass

    class UserNotFoundError(Exception):
        """Raised when user is not found."""
        def __init__(self, user_id: int):
            self.user_id = user_id
            super().__init__(f"User with ID {user_id} not found")

    class ValidationError(Exception):
        """Base class for validation errors."""
        pass

    class PasswordTooShortError(ValidationError):
        """Raised when password is too short."""
        pass

    # Use custom exceptions
    def validate_email(email: str) -> str:
        if "@" not in email:
            raise InvalidEmailError(f"Invalid email: {email}")
        return f"Valid email: {email}"

    def get_user(user_id: int) -> str:
        users = {1: "Alice", 2: "Bob"}
        if user_id not in users:
            raise UserNotFoundError(user_id)
        return users[user_id]

    results = {}

    # Test custom exceptions
    try:
        results["valid_email"] = validate_email("test@example.com")
    except InvalidEmailError as e:
        results["valid_email"] = f"Error: {e}"

    try:
        results["invalid_email"] = validate_email("invalid")
    except InvalidEmailError as e:
        results["invalid_email"] = f"Error: {e}"

    try:
        results["user_found"] = get_user(1)
    except UserNotFoundError as e:
        results["user_found"] = f"Error: {e}"

    try:
        results["user_not_found"] = get_user(999)
    except UserNotFoundError as e:
        results["user_not_found"] = f"Error: {e}"

    return results


def demonstrate_context_managers() -> dict[str, Any]:
    """Demonstrate exception handling with context managers."""
    # Context managers automatically handle cleanup
    def safe_file_write() -> str:
        try:
            with open("temp_test.txt", "w") as f:
                f.write("Test content")
                # File is automatically closed even if exception occurs
            return "Success"
        except IOError as e:
            return f"Error: {e}"
        finally:
            # Cleanup
            import os
            if os.path.exists("temp_test.txt"):
                os.remove("temp_test.txt")

    # Custom context manager
    class ErrorLogger:
        def __enter__(self):
            self.errors = []
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                self.errors.append(f"{exc_type.__name__}: {exc_val}")
                # Return True to suppress exception
                return True

    def use_error_logger() -> list:
        with ErrorLogger() as logger:
            raise ValueError("Test error")
        return logger.errors

    return {
        "file_write": safe_file_write(),
        "error_logger": use_error_logger(),
    }


def demonstrate_exception_chaining() -> dict[str, Any]:
    """Demonstrate exception chaining."""
    def process_data(data: str) -> str:
        try:
            # First operation
            num = int(data)
        except ValueError as e:
            # Chain the exception
            raise TypeError("Data processing failed") from e

    def implicit_chaining(data: str) -> str:
        try:
            num = int(data)
            result = 100 / num
            return str(result)
        except ValueError:
            # This will cause another exception
            raise ZeroDivisionError("Cannot process invalid input")

    results = {}

    # Explicit chaining
    try:
        results["explicit_chain"] = process_data("abc")
    except TypeError as e:
        results["explicit_chain"] = f"{type(e).__name__}: {e}, Caused by: {type(e.__cause__).__name__}"

    return results


def demonstrate_assertions() -> dict[str, Any]:
    """Demonstrate assertions for debugging."""
    def calculate_average(numbers: List[int]) -> float:
        assert len(numbers) > 0, "List cannot be empty"
        assert all(isinstance(n, int) for n in numbers), "All elements must be integers"
        return sum(numbers) / len(numbers)

    results = {}

    # Successful assertion
    try:
        results["valid_list"] = calculate_average([1, 2, 3, 4, 5])
    except AssertionError as e:
        results["valid_list"] = f"AssertionError: {e}"

    # Failed assertion
    try:
        results["empty_list"] = calculate_average([])
    except AssertionError as e:
        results["empty_list"] = f"AssertionError: {e}"

    return results


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 13: Exception Handling")
    print("=" * 60)

    print("\n1. Basic Exceptions:")
    basic = demonstrate_basic_exceptions()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Multiple Exceptions:")
    multiple = demonstrate_multiple_exceptions()
    for key, value in multiple.items():
        print(f"   {key}: {value}")

    print("\n3. Exception Hierarchy:")
    hierarchy = demonstrate_exception_hierarchy()
    for key, value in hierarchy.items():
        print(f"   {key}: {value}")

    print("\n4. Else and Finally:")
    else_finally = demonstrate_else_finally()
    for key, value in else_finally.items():
        print(f"   {key}: {value}")

    print("\n5. Raising Exceptions:")
    raising = demonstrate_raising_exceptions()
    for key, value in raising.items():
        print(f"   {key}: {value}")

    print("\n6. Custom Exceptions:")
    custom = demonstrate_custom_exceptions()
    for key, value in custom.items():
        print(f"   {key}: {value}")

    print("\n7. Context Managers:")
    context = demonstrate_context_managers()
    for key, value in context.items():
        print(f"   {key}: {value}")

    print("\n8. Exception Chaining:")
    chaining = demonstrate_exception_chaining()
    for key, value in chaining.items():
        print(f"   {key}: {value}")

    print("\n9. Assertions:")
    assertions = demonstrate_assertions()
    for key, value in assertions.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
