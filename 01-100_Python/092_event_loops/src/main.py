#!/usr/bin/env python3
"""
Program 92: Event Loops
Demonstrates event loop internals and custom protocols.
"""

import asyncio
import time
from typing import Optional
import socket


def demonstrate_event_loop_basics() -> None:
    """Demonstrate event loop basics."""
    print("\n" + "=" * 60)
    print("EVENT LOOP BASICS")
    print("=" * 60)

    print("\n1. Event loop concept:")
    print("   - Manages and executes async tasks")
    print("   - Schedules callbacks")
    print("   - Performs network I/O")
    print("   - Runs subprocesses")

    print("\n2. Event loop lifecycle:")
    print("   create -> run tasks -> close")


async def demonstrate_get_event_loop() -> None:
    """Demonstrate getting event loop."""
    print("\n" + "=" * 60)
    print("GETTING EVENT LOOP")
    print("=" * 60)

    # Get current event loop
    loop = asyncio.get_event_loop()

    print(f"\n1. Current event loop: {type(loop).__name__}")
    print(f"   Running: {loop.is_running()}")
    print(f"   Closed: {loop.is_closed()}")

    print("\n2. Event loop methods:")
    print("   - run_until_complete()")
    print("   - run_forever()")
    print("   - stop()")
    print("   - close()")


async def demonstrate_call_soon() -> None:
    """Demonstrate call_soon."""
    print("\n" + "=" * 60)
    print("CALL_SOON")
    print("=" * 60)

    def callback(message: str):
        """Simple callback."""
        print(f"   Callback: {message}")

    print("\n1. Scheduling callbacks with call_soon:")

    loop = asyncio.get_event_loop()

    loop.call_soon(callback, "First")
    loop.call_soon(callback, "Second")
    loop.call_soon(callback, "Third")

    print("   Callbacks scheduled")

    await asyncio.sleep(0.1)

    print("\n2. Callbacks executed in order")


async def demonstrate_call_later() -> None:
    """Demonstrate call_later."""
    print("\n" + "=" * 60)
    print("CALL_LATER")
    print("=" * 60)

    def callback(message: str):
        """Delayed callback."""
        print(f"   Delayed callback: {message}")

    print("\n1. Scheduling delayed callbacks:")

    loop = asyncio.get_event_loop()

    # Schedule callbacks with delays
    loop.call_later(0.2, callback, "After 0.2s")
    loop.call_later(0.1, callback, "After 0.1s")

    print("   Callbacks scheduled")

    await asyncio.sleep(0.3)

    print("\n2. All callbacks executed")


async def demonstrate_call_at() -> None:
    """Demonstrate call_at."""
    print("\n" + "=" * 60)
    print("CALL_AT")
    print("=" * 60)

    def callback():
        """Timed callback."""
        print("   Callback executed at specific time")

    print("\n1. Scheduling callback at specific time:")

    loop = asyncio.get_event_loop()

    # Schedule at specific time
    when = loop.time() + 0.2
    loop.call_at(when, callback)

    print(f"   Scheduled for {when:.3f}")

    await asyncio.sleep(0.3)


async def demonstrate_futures() -> None:
    """Demonstrate futures in event loop."""
    print("\n" + "=" * 60)
    print("FUTURES")
    print("=" * 60)

    print("\n1. Future represents eventual result:")

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def set_result():
        """Set future result."""
        future.set_result("Result value")
        print("   Future result set")

    loop.call_later(0.2, set_result)

    print("   Waiting for future...")
    result = await future
    print(f"   Got result: {result}")


async def demonstrate_task_scheduling() -> None:
    """Demonstrate task scheduling."""
    print("\n" + "=" * 60)
    print("TASK SCHEDULING")
    print("=" * 60)

    async def task(task_id: int):
        """Simple task."""
        print(f"   Task {task_id} running")
        await asyncio.sleep(0.1)
        return f"Result {task_id}"

    print("\n1. Creating and scheduling tasks:")

    # Create tasks
    task1 = asyncio.create_task(task(1))
    task2 = asyncio.create_task(task(2))

    print("   Tasks created and scheduled")

    # Get current task
    current = asyncio.current_task()
    print(f"\n2. Current task: {current.get_name()}")

    # Get all tasks
    all_tasks = asyncio.all_tasks()
    print(f"3. Total tasks: {len(all_tasks)}")

    # Wait for tasks
    await task1
    await task2


async def demonstrate_custom_protocol() -> None:
    """Demonstrate custom protocol."""
    print("\n" + "=" * 60)
    print("CUSTOM PROTOCOL")
    print("=" * 60)

    class EchoProtocol(asyncio.Protocol):
        """Simple echo protocol."""

        def connection_made(self, transport):
            """Called when connection is made."""
            peername = transport.get_extra_info('peername')
            print(f'   [Server] Connection from {peername}')
            self.transport = transport

        def data_received(self, data):
            """Called when data is received."""
            message = data.decode()
            print(f'   [Server] Received: {message}')

            # Echo back
            self.transport.write(data)

        def connection_lost(self, exc):
            """Called when connection is lost."""
            print('   [Server] Connection closed')

    print("\n1. Protocol lifecycle:")
    print("   connection_made -> data_received -> connection_lost")

    print("\n2. Protocol methods:")
    print("   - connection_made(transport)")
    print("   - data_received(data)")
    print("   - eof_received()")
    print("   - connection_lost(exc)")


async def demonstrate_transport() -> None:
    """Demonstrate transport concepts."""
    print("\n" + "=" * 60)
    print("TRANSPORT")
    print("=" * 60)

    print("\n1. Transport abstraction:")
    print("   - Represents communication channel")
    print("   - Used by protocols")
    print("   - Handles actual I/O")

    print("\n2. Transport methods:")
    print("   - write(data)")
    print("   - writelines(list_of_data)")
    print("   - close()")
    print("   - abort()")
    print("   - get_extra_info(name)")

    print("\n3. Transport types:")
    print("   - ReadTransport")
    print("   - WriteTransport")
    print("   - Transport (read + write)")
    print("   - DatagramTransport")
    print("   - SubprocessTransport")


async def demonstrate_low_level_apis() -> None:
    """Demonstrate low-level async APIs."""
    print("\n" + "=" * 60)
    print("LOW-LEVEL APIs")
    print("=" * 60)

    print("\n1. Loop.run_in_executor():")
    print("   - Run blocking code in thread/process pool")

    import concurrent.futures

    def blocking_task():
        """Blocking task."""
        time.sleep(0.1)
        return "Blocking result"

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_task)
        print(f"   Result: {result}")

    print("\n2. Loop.create_server():")
    print("   - Create TCP server")

    print("\n3. Loop.create_connection():")
    print("   - Create TCP client")


async def demonstrate_async_iteration() -> None:
    """Demonstrate async iteration protocol."""
    print("\n" + "=" * 60)
    print("ASYNC ITERATION")
    print("=" * 60)

    class AsyncRange:
        """Async iterator example."""

        def __init__(self, n):
            self.n = n
            self.i = 0

        def __aiter__(self):
            """Return async iterator."""
            return self

        async def __anext__(self):
            """Get next item asynchronously."""
            if self.i >= self.n:
                raise StopAsyncIteration
            await asyncio.sleep(0.05)
            self.i += 1
            return self.i

    print("\n1. Custom async iterator:")

    async for i in AsyncRange(5):
        print(f"   Value: {i}")

    print("\n2. Async iteration completed")


async def demonstrate_async_context() -> None:
    """Demonstrate async context managers."""
    print("\n" + "=" * 60)
    print("ASYNC CONTEXT MANAGERS")
    print("=" * 60)

    class AsyncResource:
        """Async context manager example."""

        async def __aenter__(self):
            """Async enter."""
            print("   [Resource] Acquiring...")
            await asyncio.sleep(0.1)
            print("   [Resource] Acquired")
            return self

        async def __aexit__(self, exc_type, exc, tb):
            """Async exit."""
            print("   [Resource] Releasing...")
            await asyncio.sleep(0.1)
            print("   [Resource] Released")

    print("\n1. Using async context manager:")

    async with AsyncResource():
        print("   [Resource] Using resource")

    print("\n2. Resource automatically cleaned up")


async def demonstrate_event_loop_policies() -> None:
    """Demonstrate event loop policies."""
    print("\n" + "=" * 60)
    print("EVENT LOOP POLICIES")
    print("=" * 60)

    print("\n1. Event loop policy:")
    policy = asyncio.get_event_loop_policy()
    print(f"   Current policy: {type(policy).__name__}")

    print("\n2. Policy responsibilities:")
    print("   - Create new event loops")
    print("   - Manage default event loop")
    print("   - Per-thread event loop management")

    print("\n3. Custom policies:")
    print("   - uvloop: High-performance implementation")
    print("   - Custom policies for special needs")


async def demonstrate_coroutine_introspection() -> None:
    """Demonstrate coroutine introspection."""
    print("\n" + "=" * 60)
    print("COROUTINE INTROSPECTION")
    print("=" * 60)

    async def sample_coro():
        """Sample coroutine."""
        await asyncio.sleep(0.1)

    coro = sample_coro()

    print("\n1. Coroutine inspection:")
    print(f"   Type: {type(coro).__name__}")
    print(f"   Is coroutine: {asyncio.iscoroutine(coro)}")

    # Clean up
    await coro

    print("\n2. Task inspection:")
    task = asyncio.create_task(sample_coro())
    print(f"   Task name: {task.get_name()}")
    print(f"   Done: {task.done()}")

    await task


async def demonstrate_debug_mode() -> None:
    """Demonstrate debug mode."""
    print("\n" + "=" * 60)
    print("DEBUG MODE")
    print("=" * 60)

    print("\n1. Enable debug mode:")
    print("   - PYTHONASYNCIODEBUG=1")
    print("   - loop.set_debug(True)")

    loop = asyncio.get_event_loop()
    debug = loop.get_debug()
    print(f"\n2. Debug mode: {debug}")

    print("\n3. Debug features:")
    print("   - Detect unawaited coroutines")
    print("   - Track callback execution time")
    print("   - Log slow callbacks")


async def demonstrate_performance_tips() -> None:
    """Demonstrate performance tips."""
    print("\n" + "=" * 60)
    print("PERFORMANCE TIPS")
    print("=" * 60)

    print("\n1. Use uvloop:")
    print("   import uvloop")
    print("   uvloop.install()")

    print("\n2. Batch operations:")
    print("   - Reduce context switches")
    print("   - Group similar tasks")

    print("\n3. Use appropriate data structures:")
    print("   - asyncio.Queue for producer-consumer")
    print("   - asyncio.Lock for synchronization")

    print("\n4. Avoid blocking calls:")
    print("   - Use run_in_executor() for blocking code")
    print("   - Use async libraries")


async def demonstrate_best_practices() -> None:
    """Demonstrate event loop best practices."""
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)

    print("\n1. Event loop management:")
    print("   ✓ Use asyncio.run() for main")
    print("   ✓ One event loop per thread")
    print("   ✓ Close loops properly")

    print("\n2. Task management:")
    print("   ✓ Track long-running tasks")
    print("   ✓ Cancel properly")
    print("   ✓ Handle exceptions")

    print("\n3. Resource management:")
    print("   ✓ Use async context managers")
    print("   ✓ Clean up on exit")
    print("   ✓ Set timeouts")

    print("\n4. Debugging:")
    print("   ✓ Enable debug mode in development")
    print("   ✓ Use logging")
    print("   ✓ Monitor task queues")


async def main_async() -> None:
    """Main async function."""
    print("=" * 60)
    print("PYTHON EVENT LOOPS")
    print("=" * 60)

    await demonstrate_get_event_loop()
    await demonstrate_call_soon()
    await demonstrate_call_later()
    await demonstrate_call_at()
    await demonstrate_futures()
    await demonstrate_task_scheduling()
    await demonstrate_custom_protocol()
    await demonstrate_transport()
    await demonstrate_low_level_apis()
    await demonstrate_async_iteration()
    await demonstrate_async_context()
    await demonstrate_event_loop_policies()
    await demonstrate_coroutine_introspection()
    await demonstrate_debug_mode()
    await demonstrate_performance_tips()
    await demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All event loop demonstrations completed!")
    print("=" * 60)


def main() -> None:
    """Main function."""
    demonstrate_event_loop_basics()
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
