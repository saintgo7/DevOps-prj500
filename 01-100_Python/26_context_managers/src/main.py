#!/usr/bin/env python3
"""Program 26: Context Managers - Master resource management with context managers."""

from contextlib import contextmanager, closing, suppress, redirect_stdout, ExitStack
import io
from typing import Any, Optional


def demonstrate_basic_context_manager() -> dict[str, Any]:
    """Demonstrate basic context manager usage."""

    class FileManager:
        """Simple file context manager."""

        def __init__(self, filename: str, mode: str):
            self.filename = filename
            self.mode = mode
            self.file = None

        def __enter__(self):
            """Open file and return handle."""
            self.file = open(self.filename, self.mode)
            return self.file

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Close file, even if exception occurred."""
            if self.file:
                self.file.close()
            return False  # Don't suppress exceptions

    # Create test file
    filename = "/tmp/test_context.txt"
    with FileManager(filename, 'w') as f:
        f.write("Hello from context manager")

    # Read back
    with FileManager(filename, 'r') as f:
        content = f.read()

    return {
        "content": content,
        "note": "__enter__ and __exit__ define context manager protocol",
    }


def demonstrate_exception_handling() -> dict[str, Any]:
    """Demonstrate exception handling in context managers."""

    class ErrorHandler:
        """Context manager that handles exceptions."""

        def __init__(self, suppress_errors: bool = False):
            self.suppress_errors = suppress_errors
            self.error = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Handle exceptions."""
            if exc_type is not None:
                self.error = f"{exc_type.__name__}: {exc_val}"
                return self.suppress_errors  # True suppresses exception
            return False

    # Without suppression
    try:
        with ErrorHandler(suppress_errors=False) as handler:
            raise ValueError("Test error")
    except ValueError:
        error_raised = True
    else:
        error_raised = False

    # With suppression
    with ErrorHandler(suppress_errors=True) as handler:
        raise ValueError("Suppressed error")
    error_suppressed = handler.error

    return {
        "error_raised": error_raised,
        "suppressed_error": error_suppressed,
        "note": "__exit__ returning True suppresses exceptions",
    }


def demonstrate_contextlib_decorator() -> dict[str, Any]:
    """Demonstrate @contextmanager decorator."""

    @contextmanager
    def managed_resource(name: str):
        """Context manager using generator."""
        # Setup
        resource = f"Resource-{name}"
        print(f"Acquiring {resource}")

        try:
            yield resource  # Provide resource to with block
        finally:
            # Cleanup (always runs)
            print(f"Releasing {resource}")

    results = []

    # Use context manager
    with managed_resource("A") as res:
        results.append(f"Using {res}")

    return {
        "results": results,
        "note": "@contextmanager turns generator into context manager",
    }


def demonstrate_multiple_contexts() -> dict[str, Any]:
    """Demonstrate managing multiple contexts."""

    @contextmanager
    def counter(name: str):
        """Simple counting context."""
        print(f"Enter {name}")
        yield name
        print(f"Exit {name}")

    # Nested with statements
    with counter("Outer"):
        with counter("Middle"):
            with counter("Inner"):
                result = "All contexts active"

    # Multiple contexts in one with (Python 3.1+)
    with counter("First"), counter("Second"):
        result2 = "Multiple contexts"

    return {
        "nested_result": result,
        "multiple_result": result2,
        "note": "Can nest or chain multiple context managers",
    }


def demonstrate_closing() -> dict[str, Any]:
    """Demonstrate contextlib.closing for objects with close()."""

    class Connection:
        """Mock connection object."""

        def __init__(self, name: str):
            self.name = name
            self.closed = False

        def close(self):
            """Close connection."""
            self.closed = True

        def query(self) -> str:
            """Execute query."""
            return f"Result from {self.name}"

    # Use closing to auto-close
    conn = Connection("Database")
    with closing(conn) as c:
        result = c.query()

    return {
        "result": result,
        "connection_closed": conn.closed,
        "note": "closing() calls close() on exit for any object",
    }


def demonstrate_suppress() -> dict[str, Any]:
    """Demonstrate contextlib.suppress for ignoring exceptions."""

    results = {}

    # Without suppress
    try:
        int("not a number")
        results["without_suppress"] = "Success"
    except ValueError:
        results["without_suppress"] = "Caught ValueError"

    # With suppress
    with suppress(ValueError):
        int("also not a number")
        results["with_suppress"] = "No error raised"

    results["with_suppress"] = results.get("with_suppress", "Suppressed")

    # Suppress multiple exception types
    with suppress(ValueError, TypeError, KeyError):
        data = {}
        value = data["missing_key"]

    results["multiple_suppressed"] = "KeyError suppressed"

    return {
        **results,
        "note": "suppress() silently ignores specified exceptions",
    }


def demonstrate_redirect_stdout() -> dict[str, Any]:
    """Demonstrate redirect_stdout for capturing output."""

    def noisy_function():
        """Function that prints."""
        print("Line 1")
        print("Line 2")
        print("Line 3")

    # Capture stdout
    output = io.StringIO()
    with redirect_stdout(output):
        noisy_function()

    captured = output.getvalue()

    return {
        "captured_output": captured.strip(),
        "line_count": len(captured.strip().split('\n')),
        "note": "redirect_stdout captures print statements",
    }


def demonstrate_exitstack() -> dict[str, Any]:
    """Demonstrate ExitStack for dynamic context management."""

    @contextmanager
    def resource(name: str):
        """Simple resource."""
        yield f"Resource-{name}"

    # Dynamic number of contexts
    def use_multiple_resources(count: int) -> list:
        """Use variable number of resources."""
        resources = []
        with ExitStack() as stack:
            for i in range(count):
                res = stack.enter_context(resource(str(i)))
                resources.append(res)
            return resources

    results = use_multiple_resources(3)

    # ExitStack for conditional contexts
    def conditional_contexts(use_resource_a: bool, use_resource_b: bool):
        """Conditionally enter contexts."""
        with ExitStack() as stack:
            res = []
            if use_resource_a:
                res.append(stack.enter_context(resource("A")))
            if use_resource_b:
                res.append(stack.enter_context(resource("B")))
            return res

    cond_results = conditional_contexts(True, False)

    return {
        "dynamic_resources": results,
        "conditional_resources": cond_results,
        "note": "ExitStack manages variable number of contexts",
    }


def demonstrate_reusable_context() -> dict[str, Any]:
    """Demonstrate reusable context managers."""

    class ReusableContext:
        """Context manager that can be used multiple times."""

        def __init__(self, name: str):
            self.name = name
            self.enter_count = 0
            self.exit_count = 0

        def __enter__(self):
            self.enter_count += 1
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.exit_count += 1
            return False

    # Create once, use multiple times
    ctx = ReusableContext("Reusable")

    with ctx:
        pass

    with ctx:
        pass

    with ctx:
        pass

    return {
        "enter_count": ctx.enter_count,
        "exit_count": ctx.exit_count,
        "note": "Context managers can be reusable if designed properly",
    }


def demonstrate_practical_examples() -> dict[str, Any]:
    """Demonstrate practical context manager use cases."""

    # 1. Timing context
    import time

    @contextmanager
    def timer(name: str):
        """Time execution of code block."""
        start = time.time()
        yield
        elapsed = time.time() - start
        print(f"{name} took {elapsed:.4f}s")

    # 2. Temporary attribute change
    @contextmanager
    def temporary_attr(obj, attr: str, value):
        """Temporarily change object attribute."""
        original = getattr(obj, attr)
        setattr(obj, attr, value)
        try:
            yield
        finally:
            setattr(obj, attr, original)

    class Config:
        debug = False

    config = Config()
    original_debug = config.debug

    with temporary_attr(config, 'debug', True):
        during_context = config.debug

    after_context = config.debug

    # 3. Database transaction (simulated)
    @contextmanager
    def transaction():
        """Simulate database transaction."""
        print("BEGIN TRANSACTION")
        try:
            yield
            print("COMMIT")
        except Exception:
            print("ROLLBACK")
            raise

    return {
        "original_debug": original_debug,
        "during_context": during_context,
        "after_context": after_context,
        "note": "Context managers perfect for setup/cleanup patterns",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 26: Context Managers")
    print("=" * 60)

    print("\n1. Basic Context Manager:")
    basic = demonstrate_basic_context_manager()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Exception Handling:")
    exceptions = demonstrate_exception_handling()
    for key, value in exceptions.items():
        print(f"   {key}: {value}")

    print("\n3. @contextmanager Decorator:")
    decorator = demonstrate_contextlib_decorator()
    for key, value in decorator.items():
        print(f"   {key}: {value}")

    print("\n4. Multiple Contexts:")
    multiple = demonstrate_multiple_contexts()
    for key, value in multiple.items():
        print(f"   {key}: {value}")

    print("\n5. Closing:")
    closing_demo = demonstrate_closing()
    for key, value in closing_demo.items():
        print(f"   {key}: {value}")

    print("\n6. Suppress:")
    suppress_demo = demonstrate_suppress()
    for key, value in suppress_demo.items():
        print(f"   {key}: {value}")

    print("\n7. Redirect Stdout:")
    redirect = demonstrate_redirect_stdout()
    for key, value in redirect.items():
        print(f"   {key}: {value}")

    print("\n8. ExitStack:")
    exitstack = demonstrate_exitstack()
    for key, value in exitstack.items():
        print(f"   {key}: {value}")

    print("\n9. Reusable Context:")
    reusable = demonstrate_reusable_context()
    for key, value in reusable.items():
        print(f"   {key}: {value}")

    print("\n10. Practical Examples:")
    practical = demonstrate_practical_examples()
    for key, value in practical.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
