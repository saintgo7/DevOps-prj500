#!/usr/bin/env python3
"""
Program 91: Advanced Asyncio
Demonstrates advanced asyncio patterns and protocols.
"""

import asyncio
import time
from typing import List, Any, Coroutine
from dataclasses import dataclass
import random


@dataclass
class TaskResult:
    """Store async task result."""
    task_id: int
    result: Any
    duration: float


async def demonstrate_async_basics() -> None:
    """Demonstrate async/await basics."""
    print("\n" + "=" * 60)
    print("ASYNC/AWAIT BASICS")
    print("=" * 60)

    async def simple_coroutine(n: int) -> int:
        """Simple coroutine."""
        await asyncio.sleep(0.1)
        return n * 2

    print("\n1. Coroutine definition:")
    print("   async def function(): ...")

    print("\n2. Awaiting coroutine:")
    result = await simple_coroutine(5)
    print(f"   Result: {result}")

    print("\n3. Multiple concurrent tasks:")
    results = await asyncio.gather(
        simple_coroutine(1),
        simple_coroutine(2),
        simple_coroutine(3)
    )
    print(f"   Results: {results}")


async def demonstrate_task_creation() -> None:
    """Demonstrate task creation and management."""
    print("\n" + "=" * 60)
    print("TASK CREATION")
    print("=" * 60)

    async def worker(task_id: int) -> str:
        """Worker coroutine."""
        await asyncio.sleep(0.1)
        return f"Task {task_id} completed"

    print("\n1. Creating tasks:")

    # Create tasks
    task1 = asyncio.create_task(worker(1))
    task2 = asyncio.create_task(worker(2))
    task3 = asyncio.create_task(worker(3))

    print("   Tasks created (running in background)")

    # Wait for tasks
    results = await asyncio.gather(task1, task2, task3)

    print(f"\n2. Results: {results}")


async def demonstrate_task_cancellation() -> None:
    """Demonstrate task cancellation."""
    print("\n" + "=" * 60)
    print("TASK CANCELLATION")
    print("=" * 60)

    async def long_running_task():
        """Long running task that can be cancelled."""
        try:
            print("   [Task] Starting...")
            await asyncio.sleep(5)
            print("   [Task] Completed")
        except asyncio.CancelledError:
            print("   [Task] Cancelled!")
            raise

    print("\n1. Starting task:")
    task = asyncio.create_task(long_running_task())

    print("2. Waiting briefly...")
    await asyncio.sleep(0.1)

    print("3. Cancelling task:")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("   ✓ Task cancellation handled")


async def demonstrate_timeouts() -> None:
    """Demonstrate timeout handling."""
    print("\n" + "=" * 60)
    print("TIMEOUT HANDLING")
    print("=" * 60)

    async def slow_operation():
        """Slow operation."""
        await asyncio.sleep(2)
        return "Done"

    print("\n1. Using wait_for with timeout:")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=0.5)
        print(f"   Result: {result}")
    except asyncio.TimeoutError:
        print("   ✓ Operation timed out")

    print("\n2. Using timeout context manager:")
    try:
        async with asyncio.timeout(0.5):
            await asyncio.sleep(2)
    except asyncio.TimeoutError:
        print("   ✓ Context manager timeout")


async def demonstrate_gather_vs_wait() -> None:
    """Demonstrate gather vs wait."""
    print("\n" + "=" * 60)
    print("GATHER vs WAIT")
    print("=" * 60)

    async def task(n: int) -> int:
        """Simple task."""
        await asyncio.sleep(0.1)
        return n

    print("\n1. asyncio.gather():")
    print("   - Returns results in order")
    print("   - Cancels all if one fails")

    results = await asyncio.gather(task(1), task(2), task(3))
    print(f"   Results: {results}")

    print("\n2. asyncio.wait():")
    print("   - Returns (done, pending) sets")
    print("   - More control over completion")

    tasks = [asyncio.create_task(task(i)) for i in range(1, 4)]
    done, pending = await asyncio.wait(tasks)

    results = [t.result() for t in done]
    print(f"   Done: {len(done)}, Pending: {len(pending)}")
    print(f"   Results: {sorted(results)}")


async def demonstrate_as_completed() -> None:
    """Demonstrate as_completed pattern."""
    print("\n" + "=" * 60)
    print("AS_COMPLETED PATTERN")
    print("=" * 60)

    async def task(task_id: int) -> TaskResult:
        """Task with random duration."""
        start = time.time()
        duration = random.uniform(0.1, 0.3)
        await asyncio.sleep(duration)
        return TaskResult(task_id, f"Result {task_id}", time.time() - start)

    print("\n1. Processing tasks as they complete:")

    tasks = [task(i) for i in range(5)]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"   Task {result.task_id} done ({result.duration:.3f}s)")


async def demonstrate_semaphore() -> None:
    """Demonstrate asyncio semaphore."""
    print("\n" + "=" * 60)
    print("ASYNCIO SEMAPHORE")
    print("=" * 60)

    semaphore = asyncio.Semaphore(2)

    async def worker(worker_id: int):
        """Worker that uses semaphore."""
        print(f"   Worker {worker_id} waiting...")
        async with semaphore:
            print(f"   Worker {worker_id} acquired semaphore")
            await asyncio.sleep(0.2)
            print(f"   Worker {worker_id} releasing")

    print("\n1. Semaphore with 2 permits:")
    print("   (Only 2 coroutines can run simultaneously)")

    tasks = [worker(i) for i in range(4)]
    await asyncio.gather(*tasks)

    print("\n2. All workers completed")


async def demonstrate_lock() -> None:
    """Demonstrate asyncio lock."""
    print("\n" + "=" * 60)
    print("ASYNCIO LOCK")
    print("=" * 60)

    lock = asyncio.Lock()
    counter = 0

    async def increment():
        """Increment shared counter."""
        nonlocal counter
        async with lock:
            temp = counter
            await asyncio.sleep(0.01)
            counter = temp + 1

    print("\n1. Using lock for synchronization:")

    tasks = [increment() for _ in range(10)]
    await asyncio.gather(*tasks)

    print(f"   Counter: {counter}")
    print("   ✓ All increments preserved")


async def demonstrate_event() -> None:
    """Demonstrate asyncio event."""
    print("\n" + "=" * 60)
    print("ASYNCIO EVENT")
    print("=" * 60)

    event = asyncio.Event()

    async def waiter(waiter_id: int):
        """Wait for event."""
        print(f"   Waiter {waiter_id} waiting...")
        await event.wait()
        print(f"   Waiter {waiter_id} proceeding!")

    async def setter():
        """Set event after delay."""
        await asyncio.sleep(0.3)
        print("   [Setter] Setting event...")
        event.set()

    print("\n1. Starting waiters:")

    tasks = [waiter(i) for i in range(3)]
    tasks.append(setter())

    await asyncio.gather(*tasks)

    print("\n2. All waiters notified")


async def demonstrate_queue() -> None:
    """Demonstrate asyncio queue."""
    print("\n" + "=" * 60)
    print("ASYNCIO QUEUE")
    print("=" * 60)

    queue = asyncio.Queue(maxsize=5)

    async def producer():
        """Producer coroutine."""
        for i in range(5):
            await queue.put(f"Item {i}")
            print(f"   [Producer] Added Item {i}")
            await asyncio.sleep(0.1)

    async def consumer():
        """Consumer coroutine."""
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=0.5)
                print(f"   [Consumer] Processing {item}")
                queue.task_done()
            except asyncio.TimeoutError:
                break

    print("\n1. Producer-Consumer with async queue:")

    await asyncio.gather(producer(), consumer())

    print("\n2. Queue processing completed")


async def demonstrate_streaming() -> None:
    """Demonstrate async streaming patterns."""
    print("\n" + "=" * 60)
    print("ASYNC STREAMING")
    print("=" * 60)

    async def data_generator():
        """Generate data asynchronously."""
        for i in range(5):
            await asyncio.sleep(0.1)
            yield i

    print("\n1. Async generator:")
    async for value in data_generator():
        print(f"   Received: {value}")

    print("\n2. Stream processing completed")


async def demonstrate_task_groups() -> None:
    """Demonstrate task groups (Python 3.11+)."""
    print("\n" + "=" * 60)
    print("TASK GROUPS")
    print("=" * 60)

    async def worker(worker_id: int) -> str:
        """Worker task."""
        await asyncio.sleep(0.1)
        return f"Worker {worker_id} done"

    print("\n1. Using task groups (structured concurrency):")

    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(worker(1))
            task2 = tg.create_task(worker(2))
            task3 = tg.create_task(worker(3))

        print(f"   Results: {task1.result()}, {task2.result()}, {task3.result()}")
    except AttributeError:
        print("   TaskGroup not available (Python < 3.11)")


async def demonstrate_subprocess() -> None:
    """Demonstrate async subprocess."""
    print("\n" + "=" * 60)
    print("ASYNC SUBPROCESS")
    print("=" * 60)

    print("\n1. Running subprocess asynchronously:")

    proc = await asyncio.create_subprocess_exec(
        'echo', 'Hello from async subprocess',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    print(f"   Output: {stdout.decode().strip()}")
    print(f"   Return code: {proc.returncode}")


async def demonstrate_exception_handling() -> None:
    """Demonstrate async exception handling."""
    print("\n" + "=" * 60)
    print("EXCEPTION HANDLING")
    print("=" * 60)

    async def failing_task():
        """Task that raises exception."""
        await asyncio.sleep(0.1)
        raise ValueError("Task failed!")

    print("\n1. Handling exceptions in gather:")

    try:
        await asyncio.gather(
            asyncio.sleep(0.1),
            failing_task(),
            return_exceptions=True
        )
    except Exception as e:
        print(f"   Caught: {e}")

    print("   ✓ return_exceptions=True prevents cancellation")


async def demonstrate_context_vars() -> None:
    """Demonstrate context variables."""
    print("\n" + "=" * 60)
    print("CONTEXT VARIABLES")
    print("=" * 60)

    from contextvars import ContextVar

    request_id: ContextVar[str] = ContextVar('request_id')

    async def worker(worker_id: int):
        """Worker with context-local data."""
        request_id.set(f"req-{worker_id}")
        await asyncio.sleep(0.1)
        print(f"   Worker {worker_id}: {request_id.get()}")

    print("\n1. Context variables are task-local:")

    tasks = [worker(i) for i in range(3)]
    await asyncio.gather(*tasks)

    print("\n2. Each task has isolated context")


async def demonstrate_performance_patterns() -> None:
    """Demonstrate performance patterns."""
    print("\n" + "=" * 60)
    print("PERFORMANCE PATTERNS")
    print("=" * 60)

    print("\n1. Batch processing:")
    print("   - Process items in batches")
    print("   - Limit concurrent tasks")

    print("\n2. Connection pooling:")
    print("   - Reuse connections")
    print("   - Use semaphores for limits")

    print("\n3. Caching:")
    print("   - Cache async results")
    print("   - Use functools.lru_cache")


async def demonstrate_best_practices() -> None:
    """Demonstrate asyncio best practices."""
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)

    print("\n1. Do's:")
    print("   ✓ Use asyncio.run() for main")
    print("   ✓ Use create_task() for background tasks")
    print("   ✓ Use timeouts for operations")
    print("   ✓ Handle cancellations properly")
    print("   ✓ Use async context managers")

    print("\n2. Don'ts:")
    print("   × Don't block the event loop")
    print("   × Don't use time.sleep()")
    print("   × Don't forget to await")
    print("   × Don't mix threads and asyncio carelessly")

    print("\n3. Performance:")
    print("   ✓ Use uvloop for better performance")
    print("   ✓ Batch operations when possible")
    print("   ✓ Use connection pooling")


async def main_async() -> None:
    """Main async function."""
    print("=" * 60)
    print("PYTHON ADVANCED ASYNCIO")
    print("=" * 60)

    await demonstrate_async_basics()
    await demonstrate_task_creation()
    await demonstrate_task_cancellation()
    await demonstrate_timeouts()
    await demonstrate_gather_vs_wait()
    await demonstrate_as_completed()
    await demonstrate_semaphore()
    await demonstrate_lock()
    await demonstrate_event()
    await demonstrate_queue()
    await demonstrate_streaming()
    await demonstrate_task_groups()
    await demonstrate_subprocess()
    await demonstrate_exception_handling()
    await demonstrate_context_vars()
    await demonstrate_performance_patterns()
    await demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All asyncio demonstrations completed!")
    print("=" * 60)


def main() -> None:
    """Main function."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
