#!/usr/bin/env python3
"""Program 25: Concurrent Futures - High-level concurrent execution interface."""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait
from concurrent.futures import FIRST_COMPLETED, ALL_COMPLETED, Future
import time
from typing import Any, List


def demonstrate_thread_pool_executor() -> dict[str, Any]:
    """Demonstrate ThreadPoolExecutor basics."""

    def task(name: str, duration: float) -> str:
        """Simple task with delay."""
        time.sleep(duration)
        return f"{name} completed in {duration}s"

    # Create thread pool
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks
        future1 = executor.submit(task, "Task-1", 0.1)
        future2 = executor.submit(task, "Task-2", 0.05)
        future3 = executor.submit(task, "Task-3", 0.08)

        # Get results
        results = [future1.result(), future2.result(), future3.result()]

    return {
        "results": results,
        "note": "ThreadPoolExecutor for I/O-bound tasks",
    }


def demonstrate_process_pool_executor() -> dict[str, Any]:
    """Demonstrate ProcessPoolExecutor for CPU-bound tasks."""

    def cpu_intensive(n: int) -> int:
        """CPU-intensive calculation."""
        result = 0
        for i in range(n):
            result += i ** 2
        return result

    # Create process pool
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Submit tasks
        futures = [executor.submit(cpu_intensive, 100000) for _ in range(5)]

        # Collect results
        results = [f.result() for f in futures]

    return {
        "task_count": len(results),
        "first_result": results[0],
        "all_equal": all(r == results[0] for r in results),
        "note": "ProcessPoolExecutor for CPU-bound tasks",
    }


def demonstrate_map() -> dict[str, Any]:
    """Demonstrate executor.map() method."""

    def square(x: int) -> int:
        """Square a number."""
        time.sleep(0.01)
        return x ** 2

    numbers = list(range(10))

    # ThreadPoolExecutor with map
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(square, numbers))

    # ProcessPoolExecutor with map
    with ProcessPoolExecutor(max_workers=2) as executor:
        process_results = list(executor.map(square, numbers))

    return {
        "thread_results": results,
        "process_results": process_results,
        "note": "map() returns results in order of input",
    }


def demonstrate_as_completed() -> dict[str, Any]:
    """Demonstrate as_completed for processing results as they finish."""

    def download(url: str, delay: float) -> dict:
        """Simulate download."""
        time.sleep(delay)
        return {"url": url, "delay": delay, "status": "success"}

    urls = [
        ("file1.txt", 0.15),
        ("file2.txt", 0.05),
        ("file3.txt", 0.10),
        ("file4.txt", 0.03),
    ]

    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all tasks
        futures = {
            executor.submit(download, url, delay): url
            for url, delay in urls
        }

        # Process as they complete
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    return {
        "results": results,
        "order": "Completed order, not submission order",
        "note": "as_completed yields futures as they finish",
    }


def demonstrate_future_methods() -> dict[str, Any]:
    """Demonstrate Future object methods."""

    def slow_task(duration: float) -> str:
        """Task with variable duration."""
        time.sleep(duration)
        return f"Completed after {duration}s"

    executor = ThreadPoolExecutor(max_workers=2)

    # Submit task
    future = executor.submit(slow_task, 0.1)

    # Check status
    results = {
        "running_immediately": future.running(),
        "done_immediately": future.done(),
    }

    # Wait and check again
    time.sleep(0.05)
    results["running_after_delay"] = future.running()

    # Get result (blocks until complete)
    results["result"] = future.result()
    results["done_after_result"] = future.done()

    executor.shutdown()

    return {
        **results,
        "note": "Future provides done(), running(), result(), cancel()",
    }


def demonstrate_wait() -> dict[str, Any]:
    """Demonstrate wait() function with different return conditions."""

    def task(name: str, duration: float) -> str:
        """Simple task."""
        time.sleep(duration)
        return f"{name} done"

    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks
        futures = {
            executor.submit(task, f"Task-{i}", delay)
            for i, delay in enumerate([0.2, 0.1, 0.15, 0.05])
        }

        # Wait for first to complete
        done, pending = wait(futures, return_when=FIRST_COMPLETED)

        first_result = list(done)[0].result()
        pending_count = len(pending)

        # Cancel pending
        for f in pending:
            f.cancel()

    return {
        "first_completed": first_result,
        "pending_when_first_done": pending_count,
        "note": "wait() with FIRST_COMPLETED, ALL_COMPLETED, FIRST_EXCEPTION",
    }


def demonstrate_callbacks() -> dict[str, Any]:
    """Demonstrate future callbacks."""

    results = {"callbacks": []}

    def task(x: int) -> int:
        """Simple task."""
        time.sleep(0.05)
        return x ** 2

    def callback(future: Future):
        """Called when future completes."""
        result = future.result()
        results["callbacks"].append(f"Callback: {result}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit with callback
        future1 = executor.submit(task, 5)
        future1.add_done_callback(callback)

        future2 = executor.submit(task, 7)
        future2.add_done_callback(callback)

        # Wait for completion
        future1.result()
        future2.result()

    time.sleep(0.1)  # Allow callbacks to complete

    return {
        "callbacks": results["callbacks"],
        "note": "add_done_callback() registers function to call on completion",
    }


def demonstrate_timeout() -> dict[str, Any]:
    """Demonstrate timeout handling."""

    def slow_operation() -> str:
        """Very slow operation."""
        time.sleep(2.0)
        return "Completed"

    results = {}

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(slow_operation)

        # Try to get result with timeout
        try:
            result = future.result(timeout=0.1)
            results["result"] = result
        except TimeoutError:
            results["result"] = "Timeout"
            future.cancel()

        results["cancelled"] = future.cancelled()

    return {
        **results,
        "note": "result(timeout=x) raises TimeoutError if not done",
    }


def demonstrate_exception_handling() -> dict[str, Any]:
    """Demonstrate exception handling in futures."""

    def task_with_error(x: int) -> int:
        """Task that may raise exception."""
        if x == 3:
            raise ValueError(f"Invalid value: {x}")
        return x ** 2

    results = {"success": [], "errors": []}

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task_with_error, i) for i in range(5)]

        for future in as_completed(futures):
            try:
                result = future.result()
                results["success"].append(result)
            except ValueError as e:
                results["errors"].append(str(e))

    return {
        "successes": results["success"],
        "errors": results["errors"],
        "note": "Exceptions raised in tasks can be caught via result()",
    }


def demonstrate_context_manager() -> dict[str, Any]:
    """Demonstrate executor context manager best practices."""

    def task(x: int) -> int:
        """Simple task."""
        return x * 2

    # With context manager (recommended)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task, i) for i in range(5)]
        results_with = [f.result() for f in futures]
        # Automatically calls shutdown(wait=True)

    # Manual shutdown
    executor_manual = ProcessPoolExecutor(max_workers=2)
    futures = [executor_manual.submit(task, i) for i in range(5)]
    results_manual = [f.result() for f in futures]
    executor_manual.shutdown(wait=True)

    return {
        "with_context": results_with,
        "manual_shutdown": results_manual,
        "note": "Use 'with' for automatic cleanup, or call shutdown() manually",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 25: Concurrent Futures")
    print("=" * 60)

    print("\n1. ThreadPoolExecutor:")
    thread = demonstrate_thread_pool_executor()
    for key, value in thread.items():
        print(f"   {key}: {value}")

    print("\n2. ProcessPoolExecutor:")
    process = demonstrate_process_pool_executor()
    for key, value in process.items():
        print(f"   {key}: {value}")

    print("\n3. Executor Map:")
    map_demo = demonstrate_map()
    for key, value in map_demo.items():
        print(f"   {key}: {value}")

    print("\n4. As Completed:")
    completed = demonstrate_as_completed()
    for key, value in completed.items():
        print(f"   {key}: {value}")

    print("\n5. Future Methods:")
    future = demonstrate_future_methods()
    for key, value in future.items():
        print(f"   {key}: {value}")

    print("\n6. Wait Function:")
    wait_demo = demonstrate_wait()
    for key, value in wait_demo.items():
        print(f"   {key}: {value}")

    print("\n7. Callbacks:")
    callbacks = demonstrate_callbacks()
    for key, value in callbacks.items():
        print(f"   {key}: {value}")

    print("\n8. Timeout Handling:")
    timeout = demonstrate_timeout()
    for key, value in timeout.items():
        print(f"   {key}: {value}")

    print("\n9. Exception Handling:")
    exceptions = demonstrate_exception_handling()
    for key, value in exceptions.items():
        print(f"   {key}: {value}")

    print("\n10. Context Manager:")
    context = demonstrate_context_manager()
    for key, value in context.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
