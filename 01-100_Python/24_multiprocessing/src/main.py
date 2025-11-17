#!/usr/bin/env python3
"""Program 24: Multiprocessing - Master parallel processing with multiple processes."""

import multiprocessing as mp
import time
import os
from typing import Any, List


def demonstrate_basic_process() -> dict[str, Any]:
    """Demonstrate basic process creation and execution."""

    results = mp.Queue()

    def worker(name: str, queue: mp.Queue):
        """Worker function running in separate process."""
        pid = os.getpid()
        queue.put({"name": name, "pid": pid, "message": f"{name} completed"})

    # Create processes
    processes = []
    for i in range(3):
        p = mp.Process(target=worker, args=(f"Process-{i}", results))
        processes.append(p)
        p.start()

    # Wait for all processes
    for p in processes:
        p.join()

    # Collect results
    process_results = []
    while not results.empty():
        process_results.append(results.get())

    return {
        "main_pid": os.getpid(),
        "results": process_results,
        "note": "Each process has separate memory space and PID",
    }


def demonstrate_process_class() -> dict[str, Any]:
    """Demonstrate Process subclassing."""

    class WorkerProcess(mp.Process):
        """Custom process class."""

        def __init__(self, name: str, data: List[int], queue: mp.Queue):
            super().__init__()
            self.name = name
            self.data = data
            self.queue = queue

        def run(self):
            """Override run method."""
            result = sum(self.data)
            self.queue.put({"name": self.name, "sum": result})

    # Create shared queue
    queue = mp.Queue()

    # Create processes
    p1 = WorkerProcess("Summer-1", [1, 2, 3, 4, 5], queue)
    p2 = WorkerProcess("Summer-2", [10, 20, 30], queue)

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    results = []
    while not queue.empty():
        results.append(queue.get())

    return {
        "results": results,
        "note": "Subclass Process and override run() for custom behavior",
    }


def demonstrate_pool() -> dict[str, Any]:
    """Demonstrate Process Pool for parallel map operations."""

    def square(x: int) -> int:
        """Square a number."""
        time.sleep(0.01)
        return x ** 2

    def cube(x: int) -> int:
        """Cube a number."""
        return x ** 3

    # Create pool
    with mp.Pool(processes=4) as pool:
        # Map function across data
        numbers = list(range(10))
        squares = pool.map(square, numbers)

        # Map async
        cubes_async = pool.map_async(cube, numbers)
        cubes = cubes_async.get()

    return {
        "squares": squares,
        "cubes": cubes,
        "note": "Pool.map() distributes work across processes",
    }


def demonstrate_pool_apply() -> dict[str, Any]:
    """Demonstrate Pool apply methods."""

    def process_data(x: int, y: int) -> int:
        """Process with multiple arguments."""
        return x * y + x

    with mp.Pool(processes=2) as pool:
        # apply - single task, blocking
        result1 = pool.apply(process_data, (5, 3))

        # apply_async - single task, non-blocking
        async_result = pool.apply_async(process_data, (4, 2))
        result2 = async_result.get()

        # starmap - multiple args per task
        tasks = [(1, 2), (3, 4), (5, 6)]
        results = pool.starmap(process_data, tasks)

    return {
        "apply_result": result1,
        "apply_async_result": result2,
        "starmap_results": results,
        "note": "apply/apply_async for single tasks, starmap for multiple args",
    }


def demonstrate_shared_memory() -> dict[str, Any]:
    """Demonstrate shared memory with Value and Array."""

    def increment_value(shared_val: mp.Value, shared_arr: mp.Array):
        """Increment shared value and array."""
        with shared_val.get_lock():
            shared_val.value += 1

        with shared_arr.get_lock():
            for i in range(len(shared_arr)):
                shared_arr[i] += 1

    # Create shared memory
    shared_value = mp.Value('i', 0)  # Shared integer
    shared_array = mp.Array('i', [0, 0, 0])  # Shared array

    # Create processes
    processes = []
    for _ in range(5):
        p = mp.Process(target=increment_value, args=(shared_value, shared_array))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return {
        "shared_value": shared_value.value,
        "shared_array": list(shared_array),
        "note": "Value and Array provide shared memory with locks",
    }


def demonstrate_manager() -> dict[str, Any]:
    """Demonstrate Manager for sharing complex data structures."""

    def worker(shared_dict: dict, shared_list: list, name: str):
        """Worker accessing shared structures."""
        shared_dict[name] = os.getpid()
        shared_list.append(f"{name} done")

    with mp.Manager() as manager:
        # Create shared structures
        shared_dict = manager.dict()
        shared_list = manager.list()

        # Create processes
        processes = []
        for i in range(3):
            p = mp.Process(
                target=worker,
                args=(shared_dict, shared_list, f"Worker-{i}")
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        return {
            "shared_dict": dict(shared_dict),
            "shared_list": list(shared_list),
            "note": "Manager provides shared dicts, lists, and more",
        }


def demonstrate_queue() -> dict[str, Any]:
    """Demonstrate Queue for inter-process communication."""

    def producer(queue: mp.Queue, items: int):
        """Produce items."""
        for i in range(items):
            queue.put(f"Item-{i}")
        queue.put(None)  # Sentinel

    def consumer(queue: mp.Queue, results: mp.Queue):
        """Consume items."""
        consumed = []
        while True:
            item = queue.get()
            if item is None:
                break
            consumed.append(f"Processed {item}")
        results.put(consumed)

    # Create queues
    work_queue = mp.Queue()
    result_queue = mp.Queue()

    # Create processes
    prod = mp.Process(target=producer, args=(work_queue, 5))
    cons = mp.Process(target=consumer, args=(work_queue, result_queue))

    prod.start()
    cons.start()
    prod.join()
    cons.join()

    results = result_queue.get()

    return {
        "results": results,
        "note": "Queue enables safe inter-process communication",
    }


def demonstrate_pipe() -> dict[str, Any]:
    """Demonstrate Pipe for two-way communication."""

    def worker(conn):
        """Worker using pipe connection."""
        # Receive data
        data = conn.recv()
        # Process and send back
        result = data.upper()
        conn.send(result)
        conn.close()

    # Create pipe
    parent_conn, child_conn = mp.Pipe()

    # Create process
    p = mp.Process(target=worker, args=(child_conn,))
    p.start()

    # Send data
    parent_conn.send("hello from parent")
    # Receive result
    result = parent_conn.recv()

    p.join()

    return {
        "sent": "hello from parent",
        "received": result,
        "note": "Pipe provides two-way communication channel",
    }


def demonstrate_lock() -> dict[str, Any]:
    """Demonstrate Lock for process synchronization."""

    def worker(lock: mp.Lock, shared_val: mp.Value, name: str):
        """Worker with lock."""
        for _ in range(10):
            with lock:
                current = shared_val.value
                time.sleep(0.001)
                shared_val.value = current + 1

    lock = mp.Lock()
    shared_value = mp.Value('i', 0)

    processes = []
    for i in range(3):
        p = mp.Process(target=worker, args=(lock, shared_value, f"P-{i}"))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return {
        "final_value": shared_value.value,
        "expected": 30,
        "note": "Lock prevents race conditions in multiprocessing",
    }


def demonstrate_pool_context() -> dict[str, Any]:
    """Demonstrate Pool context manager and callbacks."""

    results = {"success": [], "errors": []}

    def task(x: int) -> int:
        """Task that may fail."""
        if x == 5:
            raise ValueError("Invalid value")
        return x ** 2

    def success_callback(result):
        """Called on success."""
        results["success"].append(result)

    def error_callback(error):
        """Called on error."""
        results["errors"].append(str(error))

    with mp.Pool(processes=2) as pool:
        # Submit tasks with callbacks
        for i in range(8):
            pool.apply_async(
                task,
                (i,),
                callback=success_callback,
                error_callback=error_callback
            )
        pool.close()
        pool.join()

    return {
        "successes": sorted(results["success"]),
        "errors": results["errors"],
        "note": "Pool supports success and error callbacks",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 24: Multiprocessing")
    print("=" * 60)

    print("\n1. Basic Process:")
    basic = demonstrate_basic_process()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Process Class:")
    proc_class = demonstrate_process_class()
    for key, value in proc_class.items():
        print(f"   {key}: {value}")

    print("\n3. Process Pool:")
    pool = demonstrate_pool()
    for key, value in pool.items():
        print(f"   {key}: {value}")

    print("\n4. Pool Apply Methods:")
    apply = demonstrate_pool_apply()
    for key, value in apply.items():
        print(f"   {key}: {value}")

    print("\n5. Shared Memory (Value, Array):")
    shared = demonstrate_shared_memory()
    for key, value in shared.items():
        print(f"   {key}: {value}")

    print("\n6. Manager (Shared Structures):")
    manager = demonstrate_manager()
    for key, value in manager.items():
        print(f"   {key}: {value}")

    print("\n7. Queue (IPC):")
    queue = demonstrate_queue()
    for key, value in queue.items():
        print(f"   {key}: {value}")

    print("\n8. Pipe (Two-way Communication):")
    pipe = demonstrate_pipe()
    for key, value in pipe.items():
        print(f"   {key}: {value}")

    print("\n9. Lock (Synchronization):")
    lock = demonstrate_lock()
    for key, value in lock.items():
        print(f"   {key}: {value}")

    print("\n10. Pool with Callbacks:")
    callbacks = demonstrate_pool_context()
    for key, value in callbacks.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
