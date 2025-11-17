#!/usr/bin/env python3
"""Program 21: Asyncio Basics - Master asynchronous programming fundamentals."""

import asyncio
import time
from typing import Any, List


def demonstrate_basic_coroutine() -> dict[str, Any]:
    """Demonstrate basic coroutine definition and execution."""

    async def simple_coroutine() -> str:
        """A simple coroutine that returns a greeting."""
        return "Hello from coroutine!"

    async def delayed_greeting(name: str, delay: float) -> str:
        """Coroutine with async sleep."""
        await asyncio.sleep(delay)
        return f"Hello, {name}!"

    # Run single coroutine
    result1 = asyncio.run(simple_coroutine())

    # Run coroutine with delay
    start = time.time()
    result2 = asyncio.run(delayed_greeting("Alice", 0.1))
    elapsed = time.time() - start

    return {
        "simple_result": result1,
        "delayed_result": result2,
        "time_elapsed": f"{elapsed:.2f}s",
        "note": "async def creates coroutine, await suspends execution",
    }


def demonstrate_multiple_coroutines() -> dict[str, Any]:
    """Demonstrate running multiple coroutines concurrently."""

    async def task_worker(name: str, delay: float) -> str:
        """Simulate async task with delay."""
        await asyncio.sleep(delay)
        return f"Task {name} completed after {delay}s"

    async def run_concurrent():
        """Run multiple tasks concurrently."""
        # Create tasks
        task1 = asyncio.create_task(task_worker("A", 0.2))
        task2 = asyncio.create_task(task_worker("B", 0.1))
        task3 = asyncio.create_task(task_worker("C", 0.15))

        # Wait for all tasks
        results = await asyncio.gather(task1, task2, task3)
        return results

    start = time.time()
    results = asyncio.run(run_concurrent())
    elapsed = time.time() - start

    return {
        "results": results,
        "total_time": f"{elapsed:.2f}s",
        "note": "Tasks run concurrently, not sequentially (0.2s not 0.45s)",
    }


def demonstrate_await_keyword() -> dict[str, Any]:
    """Demonstrate await keyword usage."""

    async def fetch_data(source: str, delay: float) -> dict:
        """Simulate fetching data from source."""
        await asyncio.sleep(delay)
        return {"source": source, "data": f"Data from {source}"}

    async def process_data(data: dict) -> dict:
        """Simulate processing data."""
        await asyncio.sleep(0.05)
        return {**data, "processed": True}

    async def fetch_and_process():
        """Chain async operations."""
        # Sequential await calls
        raw_data = await fetch_data("API", 0.1)
        processed = await process_data(raw_data)
        return processed

    result = asyncio.run(fetch_and_process())

    return {
        "result": result,
        "note": "await pauses coroutine until awaited operation completes",
    }


def demonstrate_create_task() -> dict[str, Any]:
    """Demonstrate creating and managing tasks."""

    async def counter(name: str, count: int) -> List[str]:
        """Count asynchronously."""
        results = []
        for i in range(count):
            await asyncio.sleep(0.01)
            results.append(f"{name}: {i}")
        return results

    async def run_tasks():
        """Create and run multiple tasks."""
        # Create tasks
        task1 = asyncio.create_task(counter("Task-1", 3))
        task2 = asyncio.create_task(counter("Task-2", 3))

        # Tasks start immediately when created
        # Wait for completion
        result1 = await task1
        result2 = await task2

        return result1 + result2

    results = asyncio.run(run_tasks())

    return {
        "results": results,
        "task_count": 2,
        "note": "create_task() schedules coroutine for execution immediately",
    }


def demonstrate_gather() -> dict[str, Any]:
    """Demonstrate asyncio.gather for concurrent execution."""

    async def download(url: str, size: int) -> dict:
        """Simulate file download."""
        await asyncio.sleep(size * 0.01)
        return {"url": url, "size": size, "status": "completed"}

    async def download_all():
        """Download multiple files concurrently."""
        urls = [
            ("file1.txt", 5),
            ("file2.txt", 3),
            ("file3.txt", 4),
        ]

        # gather runs all coroutines concurrently
        results = await asyncio.gather(
            *[download(url, size) for url, size in urls]
        )
        return results

    start = time.time()
    results = asyncio.run(download_all())
    elapsed = time.time() - start

    return {
        "downloads": results,
        "total_time": f"{elapsed:.2f}s",
        "note": "gather() runs coroutines concurrently and returns results",
    }


def demonstrate_wait_for() -> dict[str, Any]:
    """Demonstrate asyncio.wait_for with timeout."""

    async def slow_operation() -> str:
        """Operation that takes too long."""
        await asyncio.sleep(2.0)
        return "Completed"

    async def fast_operation() -> str:
        """Quick operation."""
        await asyncio.sleep(0.05)
        return "Completed quickly"

    async def run_with_timeout():
        """Run operations with timeout."""
        results = {}

        # This will succeed
        try:
            result = await asyncio.wait_for(fast_operation(), timeout=1.0)
            results["fast"] = result
        except asyncio.TimeoutError:
            results["fast"] = "Timeout"

        # This will timeout
        try:
            result = await asyncio.wait_for(slow_operation(), timeout=0.1)
            results["slow"] = result
        except asyncio.TimeoutError:
            results["slow"] = "Timeout"

        return results

    results = asyncio.run(run_with_timeout())

    return {
        "results": results,
        "note": "wait_for() raises TimeoutError if operation exceeds timeout",
    }


def demonstrate_task_cancellation() -> dict[str, Any]:
    """Demonstrate task cancellation."""

    async def long_task(name: str) -> str:
        """Long running task."""
        try:
            for i in range(10):
                await asyncio.sleep(0.1)
            return f"{name} completed"
        except asyncio.CancelledError:
            return f"{name} was cancelled"

    async def run_with_cancellation():
        """Create and cancel a task."""
        task = asyncio.create_task(long_task("Worker"))

        # Let it run briefly
        await asyncio.sleep(0.15)

        # Cancel the task
        task.cancel()

        # Wait for task to handle cancellation
        try:
            result = await task
        except asyncio.CancelledError:
            result = "Task cancelled via exception"

        return result

    result = asyncio.run(run_with_cancellation())

    return {
        "result": result,
        "note": "task.cancel() requests cancellation, raises CancelledError",
    }


def demonstrate_async_context_manager() -> dict[str, Any]:
    """Demonstrate async context managers."""

    class AsyncResource:
        """Async context manager example."""

        async def __aenter__(self):
            """Async enter."""
            await asyncio.sleep(0.01)
            return "Resource acquired"

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            """Async exit."""
            await asyncio.sleep(0.01)
            return False

    async def use_resource():
        """Use async context manager."""
        async with AsyncResource() as resource:
            return f"Using {resource}"

    result = asyncio.run(use_resource())

    return {
        "result": result,
        "note": "async with for async context managers (__aenter__, __aexit__)",
    }


def demonstrate_async_iteration() -> dict[str, Any]:
    """Demonstrate async iteration."""

    class AsyncRange:
        """Async iterator example."""

        def __init__(self, start: int, stop: int):
            self.start = start
            self.stop = stop
            self.current = start

        def __aiter__(self):
            """Return async iterator."""
            return self

        async def __anext__(self):
            """Get next value asynchronously."""
            if self.current >= self.stop:
                raise StopAsyncIteration

            await asyncio.sleep(0.01)
            value = self.current
            self.current += 1
            return value

    async def iterate_async():
        """Iterate using async for."""
        results = []
        async for num in AsyncRange(0, 5):
            results.append(num)
        return results

    results = asyncio.run(iterate_async())

    return {
        "results": results,
        "note": "async for iterates over async iterators (__aiter__, __anext__)",
    }


def demonstrate_coroutine_chaining() -> dict[str, Any]:
    """Demonstrate chaining coroutines."""

    async def step1(value: int) -> int:
        """First step."""
        await asyncio.sleep(0.01)
        return value * 2

    async def step2(value: int) -> int:
        """Second step."""
        await asyncio.sleep(0.01)
        return value + 10

    async def step3(value: int) -> int:
        """Third step."""
        await asyncio.sleep(0.01)
        return value ** 2

    async def pipeline(initial: int) -> dict:
        """Chain multiple async operations."""
        result1 = await step1(initial)
        result2 = await step2(result1)
        result3 = await step3(result2)

        return {
            "initial": initial,
            "after_step1": result1,
            "after_step2": result2,
            "final": result3,
        }

    result = asyncio.run(pipeline(5))

    return {
        "pipeline": result,
        "note": "Coroutines can be chained with await for sequential operations",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 21: Asyncio Basics")
    print("=" * 60)

    print("\n1. Basic Coroutine:")
    basic = demonstrate_basic_coroutine()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Multiple Coroutines:")
    multiple = demonstrate_multiple_coroutines()
    for key, value in multiple.items():
        print(f"   {key}: {value}")

    print("\n3. Await Keyword:")
    await_demo = demonstrate_await_keyword()
    for key, value in await_demo.items():
        print(f"   {key}: {value}")

    print("\n4. Create Task:")
    task = demonstrate_create_task()
    for key, value in task.items():
        print(f"   {key}: {value}")

    print("\n5. Asyncio Gather:")
    gather = demonstrate_gather()
    for key, value in gather.items():
        print(f"   {key}: {value}")

    print("\n6. Wait For (Timeout):")
    wait = demonstrate_wait_for()
    for key, value in wait.items():
        print(f"   {key}: {value}")

    print("\n7. Task Cancellation:")
    cancel = demonstrate_task_cancellation()
    for key, value in cancel.items():
        print(f"   {key}: {value}")

    print("\n8. Async Context Manager:")
    context = demonstrate_async_context_manager()
    for key, value in context.items():
        print(f"   {key}: {value}")

    print("\n9. Async Iteration:")
    iteration = demonstrate_async_iteration()
    for key, value in iteration.items():
        print(f"   {key}: {value}")

    print("\n10. Coroutine Chaining:")
    chaining = demonstrate_coroutine_chaining()
    for key, value in chaining.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
