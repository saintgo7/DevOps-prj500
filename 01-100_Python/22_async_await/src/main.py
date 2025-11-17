#!/usr/bin/env python3
"""Program 22: Async/Await - Advanced asynchronous programming patterns."""

import asyncio
import time
from typing import Any, List, Optional


def demonstrate_gather_advanced() -> dict[str, Any]:
    """Demonstrate advanced asyncio.gather patterns."""

    async def task(name: str, delay: float, should_fail: bool = False) -> str:
        """Task that may succeed or fail."""
        await asyncio.sleep(delay)
        if should_fail:
            raise ValueError(f"Task {name} failed")
        return f"Task {name} success"

    async def gather_return_exceptions():
        """Gather with return_exceptions=True."""
        results = await asyncio.gather(
            task("A", 0.05),
            task("B", 0.03, should_fail=True),
            task("C", 0.04),
            return_exceptions=True
        )
        return results

    async def gather_fail_fast():
        """Gather that fails fast (default behavior)."""
        try:
            results = await asyncio.gather(
                task("A", 0.05),
                task("B", 0.03, should_fail=True),
                task("C", 0.04),
            )
            return results
        except ValueError as e:
            return f"Failed: {e}"

    results_with_exceptions = asyncio.run(gather_return_exceptions())
    fail_fast = asyncio.run(gather_fail_fast())

    return {
        "with_exceptions": [str(r) for r in results_with_exceptions],
        "fail_fast": fail_fast,
        "note": "return_exceptions=True collects errors, default raises first",
    }


def demonstrate_wait() -> dict[str, Any]:
    """Demonstrate asyncio.wait for fine-grained control."""

    async def task(name: str, delay: float) -> str:
        """Simple async task."""
        await asyncio.sleep(delay)
        return f"{name} done"

    async def wait_first_completed():
        """Wait for first task to complete."""
        tasks = {
            asyncio.create_task(task("Slow", 0.3)),
            asyncio.create_task(task("Medium", 0.15)),
            asyncio.create_task(task("Fast", 0.05)),
        }

        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel pending tasks
        for t in pending:
            t.cancel()

        completed = [t.result() for t in done]
        return {
            "completed": completed,
            "pending_count": len(pending),
        }

    async def wait_with_timeout():
        """Wait with timeout."""
        tasks = {
            asyncio.create_task(task("T1", 0.05)),
            asyncio.create_task(task("T2", 0.5)),
        }

        done, pending = await asyncio.wait(tasks, timeout=0.1)

        # Cancel pending
        for t in pending:
            t.cancel()

        return {
            "done_count": len(done),
            "pending_count": len(pending),
        }

    first = asyncio.run(wait_first_completed())
    timeout = asyncio.run(wait_with_timeout())

    return {
        "first_completed": first,
        "with_timeout": timeout,
        "note": "wait() offers FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED",
    }


def demonstrate_as_completed() -> dict[str, Any]:
    """Demonstrate asyncio.as_completed for processing results as they arrive."""

    async def fetch(item: str, delay: float) -> dict:
        """Fetch item with delay."""
        await asyncio.sleep(delay)
        return {"item": item, "delay": delay}

    async def process_as_completed():
        """Process results as they complete."""
        tasks = [
            fetch("Item-A", 0.15),
            fetch("Item-B", 0.05),
            fetch("Item-C", 0.10),
            fetch("Item-D", 0.03),
        ]

        results = []
        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)

        return results

    results = asyncio.run(process_as_completed())

    return {
        "results": results,
        "order": "Completed in order of finishing, not submission",
        "note": "as_completed yields coroutines as they finish",
    }


def demonstrate_semaphore() -> dict[str, Any]:
    """Demonstrate asyncio.Semaphore for concurrency control."""

    async def worker(sem: asyncio.Semaphore, name: str, delay: float) -> str:
        """Worker with semaphore."""
        async with sem:
            await asyncio.sleep(delay)
            return f"{name} completed"

    async def limited_concurrency():
        """Limit concurrent tasks with semaphore."""
        # Only allow 2 concurrent tasks
        sem = asyncio.Semaphore(2)

        tasks = [
            worker(sem, f"Worker-{i}", 0.1)
            for i in range(5)
        ]

        start = time.time()
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start

        return {
            "results": results,
            "time": f"{elapsed:.2f}s",
            "note": "With 2 concurrent, 5 tasks take ~0.3s not ~0.1s",
        }

    result = asyncio.run(limited_concurrency())

    return result


def demonstrate_lock() -> dict[str, Any]:
    """Demonstrate asyncio.Lock for mutual exclusion."""

    async def increment_counter(lock: asyncio.Lock, counter: List[int], name: str):
        """Increment shared counter with lock."""
        for _ in range(3):
            async with lock:
                # Critical section
                current = counter[0]
                await asyncio.sleep(0.01)  # Simulate work
                counter[0] = current + 1
        return f"{name} done"

    async def with_lock():
        """Use lock for synchronization."""
        lock = asyncio.Lock()
        counter = [0]

        await asyncio.gather(
            increment_counter(lock, counter, "Task-1"),
            increment_counter(lock, counter, "Task-2"),
            increment_counter(lock, counter, "Task-3"),
        )

        return counter[0]

    async def without_lock():
        """Without lock - race condition."""
        counter = [0]

        async def unsafe_increment(name: str):
            for _ in range(3):
                current = counter[0]
                await asyncio.sleep(0.01)
                counter[0] = current + 1

        await asyncio.gather(
            unsafe_increment("Task-1"),
            unsafe_increment("Task-2"),
            unsafe_increment("Task-3"),
        )

        return counter[0]

    safe = asyncio.run(with_lock())
    unsafe = asyncio.run(without_lock())

    return {
        "with_lock": safe,
        "without_lock": unsafe,
        "expected": 9,
        "note": "Lock prevents race conditions in async code",
    }


def demonstrate_event() -> dict[str, Any]:
    """Demonstrate asyncio.Event for signaling."""

    async def waiter(event: asyncio.Event, name: str) -> str:
        """Wait for event to be set."""
        await event.wait()
        return f"{name} received signal"

    async def setter(event: asyncio.Event, delay: float):
        """Set event after delay."""
        await asyncio.sleep(delay)
        event.set()

    async def use_event():
        """Coordinate tasks with event."""
        event = asyncio.Event()

        # Create waiters
        waiters = [
            asyncio.create_task(waiter(event, f"Waiter-{i}"))
            for i in range(3)
        ]

        # Create setter
        setter_task = asyncio.create_task(setter(event, 0.1))

        # Wait for all
        await setter_task
        results = await asyncio.gather(*waiters)

        return results

    results = asyncio.run(use_event())

    return {
        "results": results,
        "note": "Event allows one or more tasks to wait for signal",
    }


def demonstrate_queue() -> dict[str, Any]:
    """Demonstrate asyncio.Queue for producer-consumer pattern."""

    async def producer(queue: asyncio.Queue, items: int):
        """Produce items."""
        for i in range(items):
            await asyncio.sleep(0.02)
            await queue.put(f"Item-{i}")
        await queue.put(None)  # Sentinel

    async def consumer(queue: asyncio.Queue, name: str) -> List[str]:
        """Consume items."""
        consumed = []
        while True:
            item = await queue.get()
            if item is None:
                await queue.put(None)  # Re-add for other consumers
                break
            consumed.append(f"{name} got {item}")
            await asyncio.sleep(0.01)
        return consumed

    async def producer_consumer():
        """Run producer-consumer pattern."""
        queue = asyncio.Queue(maxsize=5)

        # Start producer and consumers
        prod = asyncio.create_task(producer(queue, 6))
        cons1 = asyncio.create_task(consumer(queue, "Consumer-1"))
        cons2 = asyncio.create_task(consumer(queue, "Consumer-2"))

        # Wait for completion
        await prod
        results = await asyncio.gather(cons1, cons2)

        return [item for sublist in results for item in sublist]

    results = asyncio.run(producer_consumer())

    return {
        "results": results,
        "total_consumed": len(results),
        "note": "Queue enables async producer-consumer patterns",
    }


def demonstrate_shield() -> dict[str, Any]:
    """Demonstrate asyncio.shield to protect from cancellation."""

    async def important_task() -> str:
        """Task that should not be cancelled."""
        await asyncio.sleep(0.2)
        return "Important work completed"

    async def with_shield():
        """Protect task with shield."""
        task = asyncio.create_task(important_task())
        shielded = asyncio.shield(task)

        try:
            # Try to cancel after short delay
            await asyncio.sleep(0.05)
            shielded.cancel()
            result = await shielded
        except asyncio.CancelledError:
            # Shield was cancelled, but task continues
            result = await task  # Can still get result

        return result

    result = asyncio.run(with_shield())

    return {
        "result": result,
        "note": "shield() protects inner task from cancellation",
    }


def demonstrate_timeout() -> dict[str, Any]:
    """Demonstrate async timeout context manager."""

    async def operation(duration: float) -> str:
        """Operation with variable duration."""
        await asyncio.sleep(duration)
        return f"Completed in {duration}s"

    async def with_timeout():
        """Use timeout context manager."""
        results = {}

        # This succeeds
        try:
            async with asyncio.timeout(0.5):
                results["fast"] = await operation(0.1)
        except asyncio.TimeoutError:
            results["fast"] = "Timeout"

        # This times out (Python 3.11+)
        try:
            async with asyncio.timeout(0.1):
                results["slow"] = await operation(0.5)
        except (asyncio.TimeoutError, AttributeError):
            results["slow"] = "Timeout"

        return results

    results = asyncio.run(with_timeout())

    return {
        "results": results,
        "note": "async with timeout() provides cleaner timeout handling (3.11+)",
    }


def demonstrate_task_groups() -> dict[str, Any]:
    """Demonstrate TaskGroup for structured concurrency."""

    async def task(name: str, delay: float) -> str:
        """Simple task."""
        await asyncio.sleep(delay)
        return f"{name} done"

    async def with_task_group():
        """Use TaskGroup (Python 3.11+)."""
        try:
            # Try TaskGroup if available
            async with asyncio.TaskGroup() as tg:
                task1 = tg.create_task(task("A", 0.05))
                task2 = tg.create_task(task("B", 0.03))
                task3 = tg.create_task(task("C", 0.04))

            return {
                "results": [task1.result(), task2.result(), task3.result()],
                "note": "TaskGroup ensures all tasks complete or all are cancelled",
            }
        except AttributeError:
            # Fallback for older Python
            results = await asyncio.gather(
                task("A", 0.05),
                task("B", 0.03),
                task("C", 0.04),
            )
            return {
                "results": results,
                "note": "TaskGroup not available, using gather (Python < 3.11)",
            }

    result = asyncio.run(with_task_group())

    return result


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 22: Async/Await Advanced")
    print("=" * 60)

    print("\n1. Gather Advanced:")
    gather = demonstrate_gather_advanced()
    for key, value in gather.items():
        print(f"   {key}: {value}")

    print("\n2. Asyncio Wait:")
    wait = demonstrate_wait()
    for key, value in wait.items():
        print(f"   {key}: {value}")

    print("\n3. As Completed:")
    completed = demonstrate_as_completed()
    for key, value in completed.items():
        print(f"   {key}: {value}")

    print("\n4. Semaphore (Concurrency Limit):")
    sem = demonstrate_semaphore()
    for key, value in sem.items():
        print(f"   {key}: {value}")

    print("\n5. Lock (Mutual Exclusion):")
    lock = demonstrate_lock()
    for key, value in lock.items():
        print(f"   {key}: {value}")

    print("\n6. Event (Signaling):")
    event = demonstrate_event()
    for key, value in event.items():
        print(f"   {key}: {value}")

    print("\n7. Queue (Producer-Consumer):")
    queue = demonstrate_queue()
    for key, value in queue.items():
        print(f"   {key}: {value}")

    print("\n8. Shield (Cancellation Protection):")
    shield = demonstrate_shield()
    for key, value in shield.items():
        print(f"   {key}: {value}")

    print("\n9. Timeout Context:")
    timeout = demonstrate_timeout()
    for key, value in timeout.items():
        print(f"   {key}: {value}")

    print("\n10. Task Groups:")
    groups = demonstrate_task_groups()
    for key, value in groups.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
