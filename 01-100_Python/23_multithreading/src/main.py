#!/usr/bin/env python3
"""Program 23: Multithreading - Master concurrent execution with threads."""

import threading
import time
from typing import Any, List
from queue import Queue
import random


def demonstrate_basic_thread() -> dict[str, Any]:
    """Demonstrate basic thread creation and execution."""

    results = []

    def worker(name: str, count: int):
        """Simple worker function."""
        for i in range(count):
            time.sleep(0.01)
            results.append(f"{name}-{i}")

    # Create threads
    thread1 = threading.Thread(target=worker, args=("Thread-1", 3))
    thread2 = threading.Thread(target=worker, args=("Thread-2", 3))

    # Start threads
    start = time.time()
    thread1.start()
    thread2.start()

    # Wait for completion
    thread1.join()
    thread2.join()
    elapsed = time.time() - start

    return {
        "results": sorted(results),
        "time": f"{elapsed:.2f}s",
        "note": "Threads run concurrently, sharing memory space",
    }


def demonstrate_thread_class() -> dict[str, Any]:
    """Demonstrate Thread subclassing."""

    class WorkerThread(threading.Thread):
        """Custom thread class."""

        def __init__(self, name: str, data: List[int]):
            super().__init__()
            self.name = name
            self.data = data
            self.result = 0

        def run(self):
            """Override run method."""
            self.result = sum(self.data)
            time.sleep(0.05)

    # Create thread instances
    thread1 = WorkerThread("Summer-1", [1, 2, 3, 4, 5])
    thread2 = WorkerThread("Summer-2", [10, 20, 30])

    # Start and wait
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    return {
        "thread1_result": thread1.result,
        "thread2_result": thread2.result,
        "note": "Subclass Thread and override run() for custom behavior",
    }


def demonstrate_daemon_threads() -> dict[str, Any]:
    """Demonstrate daemon vs non-daemon threads."""

    results = {"daemon_count": 0, "regular_count": 0}

    def daemon_worker():
        """Daemon thread - exits when main program exits."""
        for i in range(100):
            results["daemon_count"] = i
            time.sleep(0.01)

    def regular_worker():
        """Regular thread - blocks program exit."""
        for i in range(5):
            results["regular_count"] = i
            time.sleep(0.01)

    # Create daemon thread
    daemon = threading.Thread(target=daemon_worker)
    daemon.daemon = True  # Set as daemon
    daemon.start()

    # Create regular thread
    regular = threading.Thread(target=regular_worker)
    regular.start()

    # Wait for regular (daemon may not complete)
    regular.join()

    return {
        "daemon_count": results["daemon_count"],
        "regular_count": results["regular_count"],
        "note": "Daemon threads don't block program exit, regular threads do",
    }


def demonstrate_thread_lock() -> dict[str, Any]:
    """Demonstrate thread synchronization with Lock."""

    counter = {"value": 0}
    lock = threading.Lock()

    def increment_with_lock(name: str, iterations: int):
        """Increment counter with lock."""
        for _ in range(iterations):
            with lock:  # Acquire lock
                current = counter["value"]
                time.sleep(0.0001)  # Simulate work
                counter["value"] = current + 1

    # Create threads
    threads = [
        threading.Thread(target=increment_with_lock, args=(f"T{i}", 100))
        for i in range(3)
    ]

    # Run threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return {
        "final_count": counter["value"],
        "expected": 300,
        "note": "Lock ensures atomic access to shared resources",
    }


def demonstrate_rlock() -> dict[str, Any]:
    """Demonstrate RLock for reentrant locking."""

    rlock = threading.RLock()
    results = []

    def recursive_function(n: int):
        """Function that acquires lock recursively."""
        with rlock:
            if n > 0:
                results.append(n)
                recursive_function(n - 1)

    thread = threading.Thread(target=recursive_function, args=(5,))
    thread.start()
    thread.join()

    return {
        "results": results,
        "note": "RLock can be acquired multiple times by same thread",
    }


def demonstrate_semaphore() -> dict[str, Any]:
    """Demonstrate Semaphore for limiting concurrent access."""

    semaphore = threading.Semaphore(2)  # Max 2 concurrent
    active_count = []
    max_concurrent = [0]

    def worker(name: str):
        """Worker with semaphore."""
        with semaphore:
            active_count.append(name)
            max_concurrent[0] = max(max_concurrent[0], len(active_count))
            time.sleep(0.1)
            active_count.remove(name)

    # Create 5 threads but only 2 can run at once
    threads = [
        threading.Thread(target=worker, args=(f"Worker-{i}",))
        for i in range(5)
    ]

    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.time() - start

    return {
        "max_concurrent": max_concurrent[0],
        "time": f"{elapsed:.2f}s",
        "note": "Semaphore limits concurrent access to resource",
    }


def demonstrate_event() -> dict[str, Any]:
    """Demonstrate Event for thread signaling."""

    event = threading.Event()
    results = []

    def waiter(name: str):
        """Wait for event."""
        results.append(f"{name} waiting")
        event.wait()  # Block until event is set
        results.append(f"{name} proceeding")

    def setter():
        """Set event after delay."""
        time.sleep(0.1)
        results.append("Event set")
        event.set()

    # Create waiters
    waiters = [
        threading.Thread(target=waiter, args=(f"Waiter-{i}",))
        for i in range(3)
    ]
    setter_thread = threading.Thread(target=setter)

    # Start all threads
    for w in waiters:
        w.start()
    setter_thread.start()

    # Wait for completion
    for w in waiters:
        w.join()
    setter_thread.join()

    return {
        "results": results[:5],  # First 5 results
        "total_events": len(results),
        "note": "Event allows threads to wait for a signal",
    }


def demonstrate_condition() -> dict[str, Any]:
    """Demonstrate Condition for complex synchronization."""

    condition = threading.Condition()
    buffer = []
    MAX_SIZE = 3

    def producer():
        """Produce items."""
        for i in range(5):
            with condition:
                while len(buffer) >= MAX_SIZE:
                    condition.wait()  # Wait for space
                buffer.append(f"Item-{i}")
                condition.notify()  # Notify consumer
            time.sleep(0.02)

    def consumer():
        """Consume items."""
        consumed = []
        for _ in range(5):
            with condition:
                while not buffer:
                    condition.wait()  # Wait for items
                item = buffer.pop(0)
                consumed.append(item)
                condition.notify()  # Notify producer
            time.sleep(0.03)
        return consumed

    prod = threading.Thread(target=producer)
    cons_result = []

    def consumer_wrapper():
        cons_result.extend(consumer())

    cons = threading.Thread(target=consumer_wrapper)

    prod.start()
    cons.start()
    prod.join()
    cons.join()

    return {
        "consumed": cons_result,
        "note": "Condition provides wait/notify for complex coordination",
    }


def demonstrate_thread_pool() -> dict[str, Any]:
    """Demonstrate thread pool pattern with Queue."""

    def worker(queue: Queue, results: List):
        """Worker thread processing queue items."""
        while True:
            item = queue.get()
            if item is None:
                break
            # Process item
            result = item ** 2
            results.append(result)
            queue.task_done()

    # Create queue and results
    queue = Queue()
    results = []

    # Create thread pool
    threads = []
    for _ in range(3):
        t = threading.Thread(target=worker, args=(queue, results))
        t.start()
        threads.append(t)

    # Add tasks
    for i in range(10):
        queue.put(i)

    # Wait for all tasks
    queue.join()

    # Stop workers
    for _ in threads:
        queue.put(None)
    for t in threads:
        t.join()

    return {
        "results": sorted(results),
        "workers": 3,
        "tasks": 10,
        "note": "Queue enables thread pool pattern for work distribution",
    }


def demonstrate_thread_local() -> dict[str, Any]:
    """Demonstrate thread-local storage."""

    thread_local = threading.local()
    results = {}

    def worker(name: str, value: int):
        """Each thread has its own copy of data."""
        thread_local.data = value
        time.sleep(0.01)  # Simulate work
        # Each thread sees only its own value
        results[name] = thread_local.data

    threads = [
        threading.Thread(target=worker, args=(f"Thread-{i}", i * 10))
        for i in range(5)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return {
        "results": results,
        "note": "thread.local() provides separate storage per thread",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 23: Multithreading")
    print("=" * 60)

    print("\n1. Basic Thread:")
    basic = demonstrate_basic_thread()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Thread Class:")
    thread_class = demonstrate_thread_class()
    for key, value in thread_class.items():
        print(f"   {key}: {value}")

    print("\n3. Daemon Threads:")
    daemon = demonstrate_daemon_threads()
    for key, value in daemon.items():
        print(f"   {key}: {value}")

    print("\n4. Thread Lock:")
    lock = demonstrate_thread_lock()
    for key, value in lock.items():
        print(f"   {key}: {value}")

    print("\n5. RLock (Reentrant):")
    rlock = demonstrate_rlock()
    for key, value in rlock.items():
        print(f"   {key}: {value}")

    print("\n6. Semaphore:")
    sem = demonstrate_semaphore()
    for key, value in sem.items():
        print(f"   {key}: {value}")

    print("\n7. Event:")
    event = demonstrate_event()
    for key, value in event.items():
        print(f"   {key}: {value}")

    print("\n8. Condition:")
    condition = demonstrate_condition()
    for key, value in condition.items():
        print(f"   {key}: {value}")

    print("\n9. Thread Pool with Queue:")
    pool = demonstrate_thread_pool()
    for key, value in pool.items():
        print(f"   {key}: {value}")

    print("\n10. Thread Local Storage:")
    local = demonstrate_thread_local()
    for key, value in local.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
