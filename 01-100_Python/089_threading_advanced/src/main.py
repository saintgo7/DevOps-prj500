#!/usr/bin/env python3
"""
Program 89: Advanced Threading
Demonstrates thread pools, locks, conditions, and semaphores.
"""

import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Any
from dataclasses import dataclass
import random


@dataclass
class TaskResult:
    """Store task execution result."""
    task_id: int
    result: Any
    duration: float


# Shared resources
shared_counter = 0
counter_lock = threading.Lock()


def demonstrate_thread_pool() -> None:
    """Demonstrate thread pool executor."""
    print("\n" + "=" * 60)
    print("THREAD POOL EXECUTOR")
    print("=" * 60)

    def worker_task(task_id: int) -> TaskResult:
        """Simulate work."""
        start = time.time()
        time.sleep(0.1)
        duration = time.time() - start
        return TaskResult(task_id, f"Result {task_id}", duration)

    print("\n1. Creating thread pool with 3 workers:")
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks
        futures = [executor.submit(worker_task, i) for i in range(5)]

        print("2. Submitted 5 tasks")

        # Collect results
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"   Task {result.task_id} completed in {result.duration:.3f}s")

    print(f"3. All tasks completed: {len(results)} results")


def demonstrate_locks() -> None:
    """Demonstrate lock usage."""
    print("\n" + "=" * 60)
    print("LOCKS (Mutex)")
    print("=" * 60)

    global shared_counter
    shared_counter = 0

    def increment_with_lock(n: int):
        """Increment counter with lock."""
        global shared_counter
        for _ in range(n):
            with counter_lock:
                shared_counter += 1

    def increment_without_lock(n: int):
        """Increment counter without lock (unsafe)."""
        global shared_counter
        for _ in range(n):
            shared_counter += 1

    # Without lock (race condition)
    print("\n1. Without lock (race condition):")
    shared_counter = 0
    threads = [threading.Thread(target=increment_without_lock, args=(1000,)) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"   Expected: 3000, Got: {shared_counter}")

    # With lock (safe)
    print("\n2. With lock (thread-safe):")
    shared_counter = 0
    threads = [threading.Thread(target=increment_with_lock, args=(1000,)) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"   Expected: 3000, Got: {shared_counter}")


def demonstrate_rlock() -> None:
    """Demonstrate reentrant lock."""
    print("\n" + "=" * 60)
    print("REENTRANT LOCK (RLock)")
    print("=" * 60)

    rlock = threading.RLock()

    def recursive_function(n: int):
        """Function that acquires lock recursively."""
        with rlock:
            if n > 0:
                print(f"   Level {n}")
                recursive_function(n - 1)

    print("\n1. RLock allows recursive acquisition:")
    print("   (Same thread can acquire multiple times)")

    recursive_function(3)

    print("\n2. Regular Lock would deadlock here!")


def demonstrate_semaphore() -> None:
    """Demonstrate semaphore usage."""
    print("\n" + "=" * 60)
    print("SEMAPHORE")
    print("=" * 60)

    # Semaphore with 2 permits
    semaphore = threading.Semaphore(2)

    def worker(worker_id: int):
        """Worker that uses semaphore."""
        print(f"   Worker {worker_id} waiting...")
        with semaphore:
            print(f"   Worker {worker_id} acquired semaphore")
            time.sleep(0.2)
            print(f"   Worker {worker_id} releasing semaphore")

    print("\n1. Semaphore with 2 permits:")
    print("   (Only 2 threads can acquire at once)")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]

    print("\n2. Starting 4 workers:")
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\n3. All workers completed")


def demonstrate_bounded_semaphore() -> None:
    """Demonstrate bounded semaphore."""
    print("\n" + "=" * 60)
    print("BOUNDED SEMAPHORE")
    print("=" * 60)

    print("\n1. BoundedSemaphore vs Semaphore:")
    print("   - BoundedSemaphore: Prevents release() beyond initial value")
    print("   - Semaphore: Allows unlimited release()")

    bounded_sem = threading.BoundedSemaphore(2)

    print("\n2. Example usage:")
    bounded_sem.acquire()
    print("   Acquired once")
    bounded_sem.release()
    print("   Released once")

    try:
        bounded_sem.release()
        bounded_sem.release()  # This would raise ValueError
    except ValueError as e:
        print(f"   ✓ Prevented over-release: {e}")


def demonstrate_condition() -> None:
    """Demonstrate condition variable."""
    print("\n" + "=" * 60)
    print("CONDITION VARIABLE")
    print("=" * 60)

    condition = threading.Condition()
    data_ready = False

    def producer():
        """Producer that signals when data is ready."""
        nonlocal data_ready
        time.sleep(0.2)
        with condition:
            data_ready = True
            print("   [Producer] Data ready, notifying...")
            condition.notify()

    def consumer():
        """Consumer that waits for data."""
        with condition:
            print("   [Consumer] Waiting for data...")
            condition.wait()
            print("   [Consumer] Data received!")

    print("\n1. Producer-Consumer pattern:")

    consumer_thread = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)

    consumer_thread.start()
    time.sleep(0.1)
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()

    print("\n2. Condition completed")


def demonstrate_event() -> None:
    """Demonstrate event synchronization."""
    print("\n" + "=" * 60)
    print("EVENT SYNCHRONIZATION")
    print("=" * 60)

    event = threading.Event()

    def waiter(worker_id: int):
        """Wait for event."""
        print(f"   Worker {worker_id} waiting for event...")
        event.wait()
        print(f"   Worker {worker_id} proceeding!")

    def setter():
        """Set event after delay."""
        time.sleep(0.3)
        print("   [Setter] Setting event...")
        event.set()

    print("\n1. Starting 3 waiters:")
    threads = [threading.Thread(target=waiter, args=(i,)) for i in range(3)]
    setter_thread = threading.Thread(target=setter)

    for t in threads:
        t.start()

    setter_thread.start()

    for t in threads:
        t.join()
    setter_thread.join()

    print("\n2. Event is set: {}".format(event.is_set()))


def demonstrate_barrier() -> None:
    """Demonstrate barrier synchronization."""
    print("\n" + "=" * 60)
    print("BARRIER SYNCHRONIZATION")
    print("=" * 60)

    barrier = threading.Barrier(3)

    def worker(worker_id: int):
        """Worker that waits at barrier."""
        print(f"   Worker {worker_id} doing work...")
        time.sleep(random.uniform(0.1, 0.3))
        print(f"   Worker {worker_id} waiting at barrier...")
        barrier.wait()
        print(f"   Worker {worker_id} passed barrier!")

    print("\n1. Barrier for 3 threads:")
    print("   (All threads wait until all arrive)")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\n2. All threads passed barrier")


def demonstrate_thread_local() -> None:
    """Demonstrate thread-local storage."""
    print("\n" + "=" * 60)
    print("THREAD-LOCAL STORAGE")
    print("=" * 60)

    thread_local = threading.local()

    def worker(worker_id: int):
        """Worker with thread-local data."""
        thread_local.data = f"Data for thread {worker_id}"
        time.sleep(0.1)
        print(f"   Thread {worker_id}: {thread_local.data}")

    print("\n1. Each thread has its own data:")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\n2. Thread-local data is isolated")


def demonstrate_timer() -> None:
    """Demonstrate timer threads."""
    print("\n" + "=" * 60)
    print("TIMER THREADS")
    print("=" * 60)

    def delayed_task():
        """Task to run after delay."""
        print("   [Timer] Task executed!")

    print("\n1. Starting timer (0.5 seconds):")
    timer = threading.Timer(0.5, delayed_task)
    timer.start()

    print("2. Waiting for timer...")
    timer.join()

    print("\n3. Timer completed")


def demonstrate_queue() -> None:
    """Demonstrate thread-safe queue."""
    print("\n" + "=" * 60)
    print("THREAD-SAFE QUEUE")
    print("=" * 60)

    task_queue = queue.Queue(maxsize=5)

    def producer(n: int):
        """Producer adds items to queue."""
        for i in range(n):
            task_queue.put(f"Item {i}")
            print(f"   [Producer] Added Item {i}")
            time.sleep(0.1)

    def consumer():
        """Consumer processes items from queue."""
        while True:
            try:
                item = task_queue.get(timeout=1)
                print(f"   [Consumer] Processing {item}")
                task_queue.task_done()
            except queue.Empty:
                break

    print("\n1. Producer-Consumer with Queue:")

    prod_thread = threading.Thread(target=producer, args=(5,))
    cons_thread = threading.Thread(target=consumer)

    prod_thread.start()
    time.sleep(0.05)
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

    print("\n2. Queue processing completed")


def demonstrate_priority_queue() -> None:
    """Demonstrate priority queue."""
    print("\n" + "=" * 60)
    print("PRIORITY QUEUE")
    print("=" * 60)

    pq = queue.PriorityQueue()

    print("\n1. Adding items with priorities:")
    items = [(3, "Low priority"), (1, "High priority"), (2, "Medium priority")]

    for priority, item in items:
        pq.put((priority, item))
        print(f"   Added: {item} (priority {priority})")

    print("\n2. Processing by priority:")
    while not pq.empty():
        priority, item = pq.get()
        print(f"   {item}")


def demonstrate_daemon_threads() -> None:
    """Demonstrate daemon threads."""
    print("\n" + "=" * 60)
    print("DAEMON THREADS")
    print("=" * 60)

    def daemon_worker():
        """Daemon thread worker."""
        print("   [Daemon] Started")
        time.sleep(0.5)
        print("   [Daemon] Still running...")

    print("\n1. Daemon vs Non-daemon:")
    print("   - Daemon: Exits when main exits")
    print("   - Non-daemon: Blocks main exit")

    print("\n2. Starting daemon thread:")
    daemon = threading.Thread(target=daemon_worker, daemon=True)
    daemon.start()

    time.sleep(0.2)
    print("3. Main thread ending (daemon may not complete)")


def demonstrate_thread_pool_map() -> None:
    """Demonstrate thread pool map."""
    print("\n" + "=" * 60)
    print("THREAD POOL MAP")
    print("=" * 60)

    def square(x: int) -> int:
        """Square a number."""
        time.sleep(0.1)
        return x * x

    print("\n1. Using map() with thread pool:")
    numbers = [1, 2, 3, 4, 5]

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(square, numbers))

    print(f"   Input: {numbers}")
    print(f"   Results: {results}")


def demonstrate_context_managers() -> None:
    """Demonstrate threading context managers."""
    print("\n" + "=" * 60)
    print("CONTEXT MANAGERS")
    print("=" * 60)

    lock = threading.Lock()

    print("\n1. Using locks with 'with' statement:")
    print("   with lock:")
    print("       # Critical section")
    print("       # Lock automatically released")

    print("\n2. Benefits:")
    print("   ✓ Automatic release")
    print("   ✓ Exception safe")
    print("   ✓ Clean code")


def main() -> None:
    """Main function demonstrating advanced threading."""
    print("=" * 60)
    print("PYTHON ADVANCED THREADING")
    print("=" * 60)

    demonstrate_thread_pool()
    demonstrate_locks()
    demonstrate_rlock()
    demonstrate_semaphore()
    demonstrate_bounded_semaphore()
    demonstrate_condition()
    demonstrate_event()
    demonstrate_barrier()
    demonstrate_thread_local()
    demonstrate_timer()
    demonstrate_queue()
    demonstrate_priority_queue()
    demonstrate_daemon_threads()
    demonstrate_thread_pool_map()
    demonstrate_context_managers()

    print("\n" + "=" * 60)
    print("All threading demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
