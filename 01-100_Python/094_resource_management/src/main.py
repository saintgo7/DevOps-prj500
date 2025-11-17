#!/usr/bin/env python3
"""
Program 94: Resource Management
Demonstrates resource limits, cleanup, and context managers.
"""

import os
import sys
import tempfile
import resource
from pathlib import Path
from typing import Any, Optional
from contextlib import contextmanager, ExitStack, suppress
import atexit
import weakref
import gc


def demonstrate_context_managers() -> None:
    """Demonstrate context managers for resource management."""
    print("\n" + "=" * 60)
    print("CONTEXT MANAGERS")
    print("=" * 60)

    print("\n1. Basic context manager (file):")
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        temp_path = f.name
        f.write("Temporary content")
        print(f"   File created: {temp_path}")
    print("   File handle automatically closed")

    # Cleanup
    os.unlink(temp_path)

    print("\n2. Multiple resources:")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        with open(tmpdir / 'file1.txt', 'w') as f1:
            with open(tmpdir / 'file2.txt', 'w') as f2:
                f1.write("File 1")
                f2.write("File 2")
                print("   Multiple files opened")
    print("   All resources cleaned up")


def demonstrate_custom_context_manager() -> None:
    """Demonstrate custom context manager."""
    print("\n" + "=" * 60)
    print("CUSTOM CONTEXT MANAGER")
    print("=" * 60)

    class ManagedResource:
        """Custom context manager."""

        def __init__(self, name: str):
            self.name = name

        def __enter__(self):
            """Acquire resource."""
            print(f"   [Enter] Acquiring {self.name}")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Release resource."""
            print(f"   [Exit] Releasing {self.name}")
            if exc_type:
                print(f"   [Exit] Exception: {exc_type.__name__}")
            return False  # Don't suppress exceptions

    print("\n1. Using custom context manager:")
    with ManagedResource("Database Connection"):
        print("   Using resource...")

    print("\n2. With exception:")
    try:
        with ManagedResource("File Handle"):
            print("   Using resource...")
            raise ValueError("Simulated error")
    except ValueError:
        print("   Exception handled, resource still cleaned up")


def demonstrate_contextmanager_decorator() -> None:
    """Demonstrate @contextmanager decorator."""
    print("\n" + "=" * 60)
    print("@CONTEXTMANAGER DECORATOR")
    print("=" * 60)

    @contextmanager
    def managed_file(filename: str):
        """Context manager using decorator."""
        print(f"   Opening {filename}")
        f = open(filename, 'w')
        try:
            yield f
        finally:
            print(f"   Closing {filename}")
            f.close()

    print("\n1. Using @contextmanager:")
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    with managed_file(tmp_path) as f:
        f.write("Test content")

    os.unlink(tmp_path)
    print("   File cleaned up")


def demonstrate_exitstack() -> None:
    """Demonstrate ExitStack for dynamic context managers."""
    print("\n" + "=" * 60)
    print("EXIT STACK")
    print("=" * 60)

    print("\n1. Managing multiple resources dynamically:")

    with ExitStack() as stack:
        # Create temporary directory
        tmpdir = stack.enter_context(tempfile.TemporaryDirectory())
        tmpdir = Path(tmpdir)

        # Create multiple files
        files = []
        for i in range(3):
            f = stack.enter_context(open(tmpdir / f'file{i}.txt', 'w'))
            files.append(f)
            f.write(f"Content {i}")

        print(f"   Created {len(files)} files")

    print("   All resources automatically cleaned up")


def demonstrate_suppress() -> None:
    """Demonstrate contextlib.suppress."""
    print("\n" + "=" * 60)
    print("SUPPRESS CONTEXT MANAGER")
    print("=" * 60)

    print("\n1. Suppressing exceptions:")

    with suppress(FileNotFoundError):
        os.remove('nonexistent_file.txt')
    print("   FileNotFoundError suppressed")

    print("\n2. Multiple exception types:")
    with suppress(FileNotFoundError, PermissionError):
        os.remove('another_nonexistent.txt')
    print("   Multiple exceptions can be suppressed")


def demonstrate_resource_limits() -> None:
    """Demonstrate resource limits."""
    print("\n" + "=" * 60)
    print("RESOURCE LIMITS")
    print("=" * 60)

    print("\n1. Current resource limits:")

    try:
        # Get soft and hard limits
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        print(f"   Max open files:")
        print(f"     Soft limit: {soft}")
        print(f"     Hard limit: {hard}")

        # Memory limit
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        print(f"   Virtual memory:")
        if soft == resource.RLIM_INFINITY:
            print(f"     Soft limit: Unlimited")
        else:
            print(f"     Soft limit: {soft / (1024**2):.0f} MB")

        if hard == resource.RLIM_INFINITY:
            print(f"     Hard limit: Unlimited")
        else:
            print(f"     Hard limit: {hard / (1024**2):.0f} MB")

    except (ValueError, OSError) as e:
        print(f"   Resource limits not available: {e}")

    print("\n2. Resource usage:")
    try:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        print(f"   User time: {usage.ru_utime:.2f}s")
        print(f"   System time: {usage.ru_stime:.2f}s")
        print(f"   Max RSS: {usage.ru_maxrss / 1024:.2f} MB")
    except Exception as e:
        print(f"   Usage info not available: {e}")


def demonstrate_atexit() -> None:
    """Demonstrate atexit for cleanup."""
    print("\n" + "=" * 60)
    print("ATEXIT MODULE")
    print("=" * 60)

    cleanup_called = []

    def cleanup_handler():
        """Cleanup handler."""
        cleanup_called.append(True)
        print("   [atexit] Cleanup handler called")

    print("\n1. Registering cleanup handler:")
    atexit.register(cleanup_handler)
    print("   Handler registered")

    print("\n2. Handler will be called at program exit")
    print("   (Multiple handlers executed in LIFO order)")


def demonstrate_weakref() -> None:
    """Demonstrate weak references for memory management."""
    print("\n" + "=" * 60)
    print("WEAK REFERENCES")
    print("=" * 60)

    class Resource:
        """Sample resource class."""
        def __init__(self, name: str):
            self.name = name
            print(f"   [Resource] Created: {name}")

        def __del__(self):
            print(f"   [Resource] Destroyed: {self.name}")

    print("\n1. Strong reference (normal):")
    obj = Resource("strong")
    print("   Object referenced")
    del obj
    gc.collect()

    print("\n2. Weak reference:")
    obj = Resource("weak")
    weak = weakref.ref(obj)
    print(f"   Weak reference created: {weak() is not None}")

    del obj
    gc.collect()
    print(f"   After del: {weak() is None}")


def demonstrate_file_resource_management() -> None:
    """Demonstrate file resource management best practices."""
    print("\n" + "=" * 60)
    print("FILE RESOURCE MANAGEMENT")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        print("\n1. Using context manager (recommended):")
        with open(tmpdir / 'file1.txt', 'w') as f:
            f.write("Content")
        print("   ✓ File automatically closed")

        print("\n2. Using try/finally (old style):")
        f = open(tmpdir / 'file2.txt', 'w')
        try:
            f.write("Content")
        finally:
            f.close()
        print("   ✓ File closed in finally block")


def demonstrate_database_resource() -> None:
    """Demonstrate database-like resource management pattern."""
    print("\n" + "=" * 60)
    print("DATABASE CONNECTION PATTERN")
    print("=" * 60)

    class DatabaseConnection:
        """Simulated database connection."""

        def __init__(self, host: str):
            self.host = host
            self.connected = False

        def connect(self):
            """Connect to database."""
            print(f"   [DB] Connecting to {self.host}")
            self.connected = True

        def disconnect(self):
            """Disconnect from database."""
            if self.connected:
                print(f"   [DB] Disconnecting from {self.host}")
                self.connected = False

        def __enter__(self):
            """Enter context."""
            self.connect()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Exit context."""
            self.disconnect()
            return False

    print("\n1. Using database connection:")
    with DatabaseConnection("localhost:5432") as db:
        print("   [DB] Executing queries...")

    print("   ✓ Connection automatically closed")


def demonstrate_cleanup_callbacks() -> None:
    """Demonstrate cleanup callbacks."""
    print("\n" + "=" * 60)
    print("CLEANUP CALLBACKS")
    print("=" * 60)

    cleanup_actions = []

    @contextmanager
    def tracked_resource(name: str):
        """Resource with cleanup tracking."""
        print(f"   Acquiring {name}")

        def cleanup():
            cleanup_actions.append(name)
            print(f"   Cleaning up {name}")

        try:
            yield name
        finally:
            cleanup()

    print("\n1. Resources with cleanup callbacks:")
    with ExitStack() as stack:
        stack.enter_context(tracked_resource("Resource1"))
        stack.enter_context(tracked_resource("Resource2"))
        stack.enter_context(tracked_resource("Resource3"))

    print(f"\n2. Cleanup order: {cleanup_actions}")
    print("   (LIFO - Last In, First Out)")


def demonstrate_memory_management() -> None:
    """Demonstrate memory management."""
    print("\n" + "=" * 60)
    print("MEMORY MANAGEMENT")
    print("=" * 60)

    print("\n1. Garbage collection:")
    print(f"   GC enabled: {gc.isenabled()}")
    print(f"   Collections: {gc.get_count()}")

    print("\n2. Manual collection:")
    before = gc.get_count()
    collected = gc.collect()
    after = gc.get_count()
    print(f"   Objects collected: {collected}")

    print("\n3. Memory management tips:")
    print("   ✓ Use context managers")
    print("   ✓ Delete large objects when done")
    print("   ✓ Use generators for large datasets")
    print("   ✓ Avoid circular references")


def demonstrate_best_practices() -> None:
    """Demonstrate resource management best practices."""
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)

    print("\n1. Always use context managers:")
    print("   ✓ with open() for files")
    print("   ✓ with lock for threading")
    print("   ✓ with connection for databases")

    print("\n2. Cleanup order:")
    print("   ✓ Close resources in reverse order")
    print("   ✓ Use ExitStack for dynamic resources")
    print("   ✓ Register cleanup handlers with atexit")

    print("\n3. Error handling:")
    print("   ✓ Always cleanup even on exceptions")
    print("   ✓ Use try/finally if not using context managers")
    print("   ✓ Log cleanup errors")

    print("\n4. Memory management:")
    print("   ✓ Avoid circular references")
    print("   ✓ Use weak references when appropriate")
    print("   ✓ Delete large objects explicitly")
    print("   ✓ Use generators for large data")

    print("\n5. Resource limits:")
    print("   ✓ Check limits before opening many files")
    print("   ✓ Pool expensive resources")
    print("   ✓ Set appropriate timeouts")


def demonstrate_resource_pool() -> None:
    """Demonstrate resource pooling pattern."""
    print("\n" + "=" * 60)
    print("RESOURCE POOLING")
    print("=" * 60)

    class ResourcePool:
        """Simple resource pool."""

        def __init__(self, create_fn, max_size: int = 5):
            self.create_fn = create_fn
            self.max_size = max_size
            self.pool = []
            self.in_use = set()

        def acquire(self):
            """Acquire resource from pool."""
            if self.pool:
                resource = self.pool.pop()
                print(f"   Reusing pooled resource")
            elif len(self.in_use) < self.max_size:
                resource = self.create_fn()
                print(f"   Creating new resource")
            else:
                raise RuntimeError("Pool exhausted")

            self.in_use.add(id(resource))
            return resource

        def release(self, resource):
            """Return resource to pool."""
            self.in_use.discard(id(resource))
            self.pool.append(resource)
            print(f"   Returned resource to pool")

        @contextmanager
        def get_resource(self):
            """Get resource as context manager."""
            resource = self.acquire()
            try:
                yield resource
            finally:
                self.release(resource)

    print("\n1. Using resource pool:")

    def create_connection():
        """Simulate creating a connection."""
        return f"Connection-{id(object())}"

    pool = ResourcePool(create_connection, max_size=2)

    with pool.get_resource() as conn1:
        print(f"   Using: {conn1[:20]}...")

    with pool.get_resource() as conn2:
        print(f"   Using: {conn2[:20]}...")

    print("\n2. Pool statistics:")
    print(f"   Pooled: {len(pool.pool)}")
    print(f"   In use: {len(pool.in_use)}")


def main() -> None:
    """Main function demonstrating resource management."""
    print("=" * 60)
    print("PYTHON RESOURCE MANAGEMENT")
    print("=" * 60)

    demonstrate_context_managers()
    demonstrate_custom_context_manager()
    demonstrate_contextmanager_decorator()
    demonstrate_exitstack()
    demonstrate_suppress()
    demonstrate_resource_limits()
    demonstrate_atexit()
    demonstrate_weakref()
    demonstrate_file_resource_management()
    demonstrate_database_resource()
    demonstrate_cleanup_callbacks()
    demonstrate_memory_management()
    demonstrate_resource_pool()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All resource management demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
