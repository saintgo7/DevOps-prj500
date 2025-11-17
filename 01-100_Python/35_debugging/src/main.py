#!/usr/bin/env python3
"""Program 35: Debugging - Master debugging techniques and tools."""

import sys
import traceback
import inspect
from typing import Any, List
import pdb


def demonstrate_print_debugging() -> dict[str, Any]:
    """Demonstrate print-based debugging."""

    def calculate_sum(numbers: List[int]) -> int:
        """Calculate sum with debug prints."""
        print(f"DEBUG: Input numbers: {numbers}")
        total = 0
        for i, num in enumerate(numbers):
            total += num
            print(f"DEBUG: Step {i}: total = {total}")
        print(f"DEBUG: Final total: {total}")
        return total

    # Capture the concept (actual prints go to stdout)
    result = calculate_sum([1, 2, 3, 4, 5])

    return {
        "result": result,
        "note": "Print debugging is simple but clutters output",
    }


def demonstrate_assert_debugging() -> dict[str, Any]:
    """Demonstrate debugging with assertions."""

    def divide(a: int, b: int) -> float:
        """Divide with assertions."""
        assert b != 0, "Divisor cannot be zero"
        assert isinstance(a, (int, float)), "Dividend must be numeric"
        assert isinstance(b, (int, float)), "Divisor must be numeric"
        return a / b

    result = divide(10, 2)

    # Test assertion
    error_caught = False
    try:
        divide(10, 0)
    except AssertionError as e:
        error_caught = True
        error_msg = str(e)

    return {
        "valid_result": result,
        "assertion_triggered": error_caught,
        "note": "Assertions catch bugs early in development",
    }


def demonstrate_traceback_inspection() -> dict[str, Any]:
    """Demonstrate traceback inspection."""

    def level_3():
        """Third level function."""
        raise ValueError("Something went wrong at level 3")

    def level_2():
        """Second level function."""
        level_3()

    def level_1():
        """First level function."""
        level_2()

    # Capture traceback
    try:
        level_1()
    except ValueError:
        tb_lines = traceback.format_exc().split('\n')
        tb_info = {
            "total_lines": len(tb_lines),
            "has_level_1": any("level_1" in line for line in tb_lines),
            "has_level_2": any("level_2" in line for line in tb_lines),
            "has_level_3": any("level_3" in line for line in tb_lines),
        }

    return {
        **tb_info,
        "note": "Tracebacks show call stack when exception occurs",
    }


def demonstrate_traceback_extraction() -> dict[str, Any]:
    """Demonstrate extracting traceback information."""

    def buggy_function():
        """Function that raises exception."""
        x = 10
        y = 0
        return x / y

    try:
        buggy_function()
    except ZeroDivisionError:
        exc_type, exc_value, exc_tb = sys.exc_info()

        # Extract traceback information
        tb_info = []
        for frame_summary in traceback.extract_tb(exc_tb):
            tb_info.append({
                "filename": frame_summary.filename.split('/')[-1],
                "line": frame_summary.lineno,
                "function": frame_summary.name,
            })

    return {
        "exception_type": exc_type.__name__,
        "exception_value": str(exc_value),
        "traceback_frames": len(tb_info),
        "note": "sys.exc_info() provides exception details",
    }


def demonstrate_inspect_module() -> dict[str, Any]:
    """Demonstrate inspect module for introspection."""

    def example_function(a: int, b: str = "default") -> str:
        """Example function for inspection."""
        local_var = f"{a}:{b}"
        return local_var

    # Get function signature
    sig = inspect.signature(example_function)
    params = list(sig.parameters.keys())

    # Get source code
    source = inspect.getsource(example_function)
    source_lines = len(source.split('\n'))

    # Check if it's a function
    is_func = inspect.isfunction(example_function)

    # Get current frame info
    frame = inspect.currentframe()
    frame_info = {
        "function": frame.f_code.co_name if frame else "unknown",
        "line": frame.f_lineno if frame else 0,
    }

    return {
        "parameters": params,
        "source_lines": source_lines,
        "is_function": is_func,
        "current_frame": frame_info["function"],
        "note": "inspect module provides runtime introspection",
    }


def demonstrate_stack_inspection() -> dict[str, Any]:
    """Demonstrate inspecting call stack."""

    def get_call_stack() -> List[str]:
        """Get call stack information."""
        stack = inspect.stack()
        return [f"{frame.function}:{frame.lineno}" for frame in stack[:5]]

    def inner_function():
        """Inner function."""
        return get_call_stack()

    def outer_function():
        """Outer function."""
        return inner_function()

    stack_info = outer_function()

    return {
        "stack_depth": len(stack_info),
        "stack_sample": stack_info[:3],
        "note": "inspect.stack() shows current call stack",
    }


def demonstrate_locals_globals() -> dict[str, Any]:
    """Demonstrate inspecting locals and globals."""

    global_var = "I am global"

    def example_function():
        """Function with local variables."""
        local_var1 = "I am local"
        local_var2 = 42

        # Get local variables
        local_vars = locals()

        # Get global variables (sample)
        global_vars = {k: v for k, v in globals().items()
                       if not k.startswith('__')}

        return {
            "local_count": len(local_vars),
            "has_local_var1": "local_var1" in local_vars,
            "global_sample_count": len(list(global_vars.keys())[:5]),
        }

    result = example_function()

    return {
        **result,
        "note": "locals() and globals() access variable scopes",
    }


def demonstrate_custom_exception_hook() -> dict[str, Any]:
    """Demonstrate custom exception hook."""

    exceptions_caught = []

    def custom_excepthook(exc_type, exc_value, exc_traceback):
        """Custom exception handler."""
        exceptions_caught.append({
            "type": exc_type.__name__,
            "value": str(exc_value),
        })

    # Save original
    original_hook = sys.excepthook

    # Install custom hook (for demonstration, not actually using)
    # sys.excepthook = custom_excepthook

    # Simulate exception handling
    try:
        raise ValueError("Test exception")
    except ValueError as e:
        custom_excepthook(type(e), e, None)

    return {
        "exceptions_caught": exceptions_caught,
        "note": "sys.excepthook handles uncaught exceptions",
    }


def demonstrate_debugging_decorators() -> dict[str, Any]:
    """Demonstrate debugging decorators."""

    def trace_calls(func):
        """Decorator that traces function calls."""

        def wrapper(*args, **kwargs):
            print(f"TRACE: Calling {func.__name__}")
            print(f"TRACE: Args: {args}, Kwargs: {kwargs}")
            result = func(*args, **kwargs)
            print(f"TRACE: {func.__name__} returned {result}")
            return result

        return wrapper

    def debug_on_error(func):
        """Decorator that prints debug info on error."""

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"ERROR in {func.__name__}: {e}")
                print(f"Args: {args}, Kwargs: {kwargs}")
                traceback.print_exc()
                raise

        return wrapper

    @trace_calls
    def add(a, b):
        return a + b

    result = add(5, 3)

    return {
        "result": result,
        "note": "Decorators can add debugging instrumentation",
    }


def demonstrate_object_inspection() -> dict[str, Any]:
    """Demonstrate inspecting object attributes."""

    class MyClass:
        """Example class."""
        class_var = "class level"

        def __init__(self):
            self.instance_var = "instance level"

        def method(self):
            """Example method."""
            return "method result"

    obj = MyClass()

    # Get all attributes
    all_attrs = dir(obj)

    # Filter to non-special attributes
    custom_attrs = [attr for attr in dir(obj) if not attr.startswith('_')]

    # Get attribute values
    attr_values = {attr: getattr(obj, attr) for attr in custom_attrs
                   if not callable(getattr(obj, attr))}

    # Get methods
    methods = [attr for attr in custom_attrs
               if callable(getattr(obj, attr))]

    return {
        "total_attributes": len(all_attrs),
        "custom_attributes": custom_attrs,
        "attribute_values": attr_values,
        "methods": methods,
        "note": "dir() and getattr() inspect object attributes",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 35: Debugging")
    print("=" * 60)

    print("\n1. Print Debugging:")
    print_debug = demonstrate_print_debugging()
    for key, value in print_debug.items():
        print(f"   {key}: {value}")

    print("\n2. Assert Debugging:")
    assert_debug = demonstrate_assert_debugging()
    for key, value in assert_debug.items():
        print(f"   {key}: {value}")

    print("\n3. Traceback Inspection:")
    tb_inspect = demonstrate_traceback_inspection()
    for key, value in tb_inspect.items():
        print(f"   {key}: {value}")

    print("\n4. Traceback Extraction:")
    tb_extract = demonstrate_traceback_extraction()
    for key, value in tb_extract.items():
        print(f"   {key}: {value}")

    print("\n5. Inspect Module:")
    inspect_demo = demonstrate_inspect_module()
    for key, value in inspect_demo.items():
        print(f"   {key}: {value}")

    print("\n6. Stack Inspection:")
    stack = demonstrate_stack_inspection()
    for key, value in stack.items():
        print(f"   {key}: {value}")

    print("\n7. Locals and Globals:")
    scopes = demonstrate_locals_globals()
    for key, value in scopes.items():
        print(f"   {key}: {value}")

    print("\n8. Custom Exception Hook:")
    hook = demonstrate_custom_exception_hook()
    for key, value in hook.items():
        print(f"   {key}: {value}")

    print("\n9. Debugging Decorators:")
    decorators = demonstrate_debugging_decorators()
    for key, value in decorators.items():
        print(f"   {key}: {value}")

    print("\n10. Object Inspection:")
    obj_inspect = demonstrate_object_inspection()
    for key, value in obj_inspect.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
