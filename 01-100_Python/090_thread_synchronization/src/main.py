#!/usr/bin/env python3
"""
Program 90: Thread Synchronization
Demonstrates race conditions, deadlocks, and their solutions.
"""

import threading
import time
import random
from typing import List
from dataclasses import dataclass


@dataclass
class BankAccount:
    """Simple bank account for synchronization demos."""
    balance: int = 0
    lock: threading.Lock = None

    def __post_init__(self):
        if self.lock is None:
            self.lock = threading.Lock()


def demonstrate_race_condition() -> None:
    """Demonstrate race condition problem."""
    print("\n" + "=" * 60)
    print("RACE CONDITION")
    print("=" * 60)

    counter = {'value': 0}

    def increment_unsafe(n: int):
        """Increment counter without synchronization."""
        for _ in range(n):
            temp = counter['value']
            time.sleep(0.00001)  # Simulate work
            counter['value'] = temp + 1

    print("\n1. Race condition occurs when:")
    print("   - Multiple threads access shared data")
    print("   - At least one modifies the data")
    print("   - No synchronization")

    print("\n2. Running without synchronization:")
    threads = [threading.Thread(target=increment_unsafe, args=(100,)) for _ in range(3)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"   Expected: 300")
    print(f"   Got: {counter['value']}")
    print(f"   Lost updates: {300 - counter['value']}")


def demonstrate_race_condition_solution() -> None:
    """Demonstrate race condition solution with locks."""
    print("\n" + "=" * 60)
    print("RACE CONDITION SOLUTION")
    print("=" * 60)

    counter = {'value': 0}
    lock = threading.Lock()

    def increment_safe(n: int):
        """Increment counter with lock."""
        for _ in range(n):
            with lock:
                temp = counter['value']
                time.sleep(0.00001)
                counter['value'] = temp + 1

    print("\n1. Solution: Use locks")
    print("   with lock:")
    print("       # Critical section")

    print("\n2. Running with synchronization:")
    threads = [threading.Thread(target=increment_safe, args=(100,)) for _ in range(3)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"   Expected: 300")
    print(f"   Got: {counter['value']}")
    print(f"   ✓ All updates preserved")


def demonstrate_deadlock() -> None:
    """Demonstrate deadlock situation."""
    print("\n" + "=" * 60)
    print("DEADLOCK")
    print("=" * 60)

    print("\n1. Deadlock occurs when:")
    print("   - Thread A holds lock1, waits for lock2")
    print("   - Thread B holds lock2, waits for lock1")
    print("   - Neither can proceed")

    lock1 = threading.Lock()
    lock2 = threading.Lock()
    deadlock_occurred = False

    def thread_a():
        """Thread A that may cause deadlock."""
        nonlocal deadlock_occurred
        lock1.acquire()
        print("   [Thread A] Acquired lock1")
        time.sleep(0.1)
        if lock2.acquire(timeout=0.5):
            print("   [Thread A] Acquired lock2")
            lock2.release()
        else:
            print("   [Thread A] Timeout waiting for lock2 (deadlock prevented)")
            deadlock_occurred = True
        lock1.release()

    def thread_b():
        """Thread B that may cause deadlock."""
        nonlocal deadlock_occurred
        lock2.acquire()
        print("   [Thread B] Acquired lock2")
        time.sleep(0.1)
        if lock1.acquire(timeout=0.5):
            print("   [Thread B] Acquired lock1")
            lock1.release()
        else:
            print("   [Thread B] Timeout waiting for lock1 (deadlock prevented)")
            deadlock_occurred = True
        lock2.release()

    print("\n2. Simulating potential deadlock:")
    t1 = threading.Thread(target=thread_a)
    t2 = threading.Thread(target=thread_b)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    if deadlock_occurred:
        print("\n3. Deadlock would have occurred (prevented by timeout)")


def demonstrate_deadlock_prevention() -> None:
    """Demonstrate deadlock prevention strategies."""
    print("\n" + "=" * 60)
    print("DEADLOCK PREVENTION")
    print("=" * 60)

    print("\n1. Prevention strategies:")
    print("   ✓ Lock ordering")
    print("   ✓ Lock timeout")
    print("   ✓ Trylock")
    print("   ✓ Single lock")

    lock1 = threading.Lock()
    lock2 = threading.Lock()

    def thread_ordered_locks(lock_first, lock_second):
        """Acquire locks in consistent order."""
        with lock_first:
            print(f"   Thread acquired first lock")
            time.sleep(0.1)
            with lock_second:
                print(f"   Thread acquired second lock")

    print("\n2. Strategy: Lock ordering")
    print("   (Always acquire locks in same order)")

    t1 = threading.Thread(target=thread_ordered_locks, args=(lock1, lock2))
    t2 = threading.Thread(target=thread_ordered_locks, args=(lock1, lock2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("\n3. ✓ No deadlock with consistent ordering")


def demonstrate_livelock() -> None:
    """Demonstrate livelock situation."""
    print("\n" + "=" * 60)
    print("LIVELOCK")
    print("=" * 60)

    print("\n1. Livelock:")
    print("   - Threads keep changing state")
    print("   - No progress made")
    print("   - Different from deadlock (threads active)")

    print("\n2. Example scenario:")
    print("   Two people in hallway, both step aside,")
    print("   then both step same way again, repeatedly")

    attempts = {'count': 0}
    max_attempts = 5

    lock1 = threading.Lock()
    lock2 = threading.Lock()

    def polite_thread_a():
        """Thread that backs off politely."""
        while attempts['count'] < max_attempts:
            if lock1.acquire(blocking=False):
                print("   [Thread A] Got lock1")
                time.sleep(0.05)
                if lock2.acquire(blocking=False):
                    print("   [Thread A] Got both locks!")
                    lock2.release()
                    lock1.release()
                    return
                else:
                    print("   [Thread A] Can't get lock2, releasing lock1")
                    lock1.release()
                    attempts['count'] += 1
            time.sleep(0.1)

    def polite_thread_b():
        """Thread that backs off politely."""
        while attempts['count'] < max_attempts:
            if lock2.acquire(blocking=False):
                print("   [Thread B] Got lock2")
                time.sleep(0.05)
                if lock1.acquire(blocking=False):
                    print("   [Thread B] Got both locks!")
                    lock1.release()
                    lock2.release()
                    return
                else:
                    print("   [Thread B] Can't get lock1, releasing lock2")
                    lock2.release()
                    attempts['count'] += 1
            time.sleep(0.1)

    print("\n3. Simulating livelock:")
    t1 = threading.Thread(target=polite_thread_a)
    t2 = threading.Thread(target=polite_thread_b)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"\n4. Total retry attempts: {attempts['count']}")


def demonstrate_bank_transfer_race() -> None:
    """Demonstrate race condition in bank transfers."""
    print("\n" + "=" * 60)
    print("BANK TRANSFER RACE CONDITION")
    print("=" * 60)

    account_a = BankAccount(balance=1000)
    account_b = BankAccount(balance=1000)

    def transfer_unsafe(from_account: BankAccount, to_account: BankAccount, amount: int):
        """Unsafe transfer (race condition)."""
        if from_account.balance >= amount:
            time.sleep(0.001)  # Simulate processing
            from_account.balance -= amount
            to_account.balance += amount

    def transfer_safe(from_account: BankAccount, to_account: BankAccount, amount: int):
        """Safe transfer with locks."""
        # Always acquire locks in same order to prevent deadlock
        first_lock = from_account.lock if id(from_account) < id(to_account) else to_account.lock
        second_lock = to_account.lock if id(from_account) < id(to_account) else from_account.lock

        with first_lock:
            with second_lock:
                if from_account.balance >= amount:
                    time.sleep(0.001)
                    from_account.balance -= amount
                    to_account.balance += amount

    print("\n1. Without synchronization:")
    # Test unsafe transfers
    account_a.balance = 1000
    account_b.balance = 1000

    threads = [
        threading.Thread(target=transfer_unsafe, args=(account_a, account_b, 100))
        for _ in range(5)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"   Account A: ${account_a.balance}")
    print(f"   Account B: ${account_b.balance}")
    print(f"   Total: ${account_a.balance + account_b.balance} (should be $2000)")

    print("\n2. With synchronization:")
    account_a.balance = 1000
    account_b.balance = 1000

    threads = [
        threading.Thread(target=transfer_safe, args=(account_a, account_b, 100))
        for _ in range(5)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"   Account A: ${account_a.balance}")
    print(f"   Account B: ${account_b.balance}")
    print(f"   Total: ${account_a.balance + account_b.balance}")
    print("   ✓ Consistent state maintained")


def demonstrate_read_write_lock() -> None:
    """Demonstrate read-write lock pattern."""
    print("\n" + "=" * 60)
    print("READ-WRITE LOCK PATTERN")
    print("=" * 60)

    class ReadWriteLock:
        """Simple read-write lock implementation."""

        def __init__(self):
            self.readers = 0
            self.writers = 0
            self.read_ready = threading.Condition(threading.Lock())
            self.write_ready = threading.Condition(threading.Lock())

        def acquire_read(self):
            """Acquire read lock."""
            self.read_ready.acquire()
            while self.writers > 0:
                self.read_ready.wait()
            self.readers += 1
            self.read_ready.release()

        def release_read(self):
            """Release read lock."""
            self.read_ready.acquire()
            self.readers -= 1
            if self.readers == 0:
                self.read_ready.notifyAll()
            self.read_ready.release()

        def acquire_write(self):
            """Acquire write lock."""
            self.write_ready.acquire()
            while self.writers > 0 or self.readers > 0:
                self.write_ready.wait()
            self.writers += 1
            self.write_ready.release()

        def release_write(self):
            """Release write lock."""
            self.write_ready.acquire()
            self.writers -= 1
            self.write_ready.notifyAll()
            self.read_ready.acquire()
            self.read_ready.notifyAll()
            self.read_ready.release()
            self.write_ready.release()

    print("\n1. Read-Write lock allows:")
    print("   - Multiple readers simultaneously")
    print("   - Exclusive writer access")
    print("   - Better performance for read-heavy workloads")

    print("\n2. Use cases:")
    print("   - Database connections")
    print("   - Cache systems")
    print("   - Configuration data")


def demonstrate_atomic_operations() -> None:
    """Demonstrate atomic operations."""
    print("\n" + "=" * 60)
    print("ATOMIC OPERATIONS")
    print("=" * 60)

    print("\n1. Atomic operations:")
    print("   - Complete without interruption")
    print("   - No partial states visible")
    print("   - Thread-safe by nature")

    print("\n2. Python atomic operations:")
    print("   ✓ Reading/writing simple variables")
    print("   ✓ List append/pop")
    print("   ✓ dict.setdefault()")
    print("   - Most other ops need locks")

    print("\n3. Not atomic:")
    print("   × i += 1 (read, modify, write)")
    print("   × list[i] = value (needs lock)")
    print("   × Multiple operations")


def demonstrate_synchronization_best_practices() -> None:
    """Demonstrate synchronization best practices."""
    print("\n" + "=" * 60)
    print("SYNCHRONIZATION BEST PRACTICES")
    print("=" * 60)

    print("\n1. Lock granularity:")
    print("   ✓ Fine-grained: Better concurrency")
    print("   ✓ Coarse-grained: Simpler code")
    print("   → Balance based on contention")

    print("\n2. Critical sections:")
    print("   ✓ Keep them short")
    print("   ✓ Avoid I/O inside locks")
    print("   ✓ Don't call unknown code")
    print("   ✓ Don't acquire other locks")

    print("\n3. Lock ordering:")
    print("   ✓ Always acquire in same order")
    print("   ✓ Document the order")
    print("   ✓ Use lock hierarchies")

    print("\n4. Testing:")
    print("   ✓ Stress test with many threads")
    print("   ✓ Use thread sanitizers")
    print("   ✓ Add assertions")
    print("   ✓ Test on multiple cores")


def demonstrate_lock_free_data_structures() -> None:
    """Demonstrate lock-free concepts."""
    print("\n" + "=" * 60)
    print("LOCK-FREE DATA STRUCTURES")
    print("=" * 60)

    print("\n1. Lock-free characteristics:")
    print("   - No explicit locks")
    print("   - Use atomic operations")
    print("   - Compare-and-swap (CAS)")
    print("   - Better scalability")

    print("\n2. Python support:")
    print("   - Limited native support")
    print("   - Use queue.Queue (lock-free internally)")
    print("   - Use threading.local")

    print("\n3. Trade-offs:")
    print("   ✓ No deadlocks")
    print("   ✓ Better performance at scale")
    print("   - Complex to implement")
    print("   - Subtle bugs possible")


def demonstrate_thread_safety_levels() -> None:
    """Demonstrate different thread safety levels."""
    print("\n" + "=" * 60)
    print("THREAD SAFETY LEVELS")
    print("=" * 60)

    print("\n1. Thread-safe:")
    print("   - Can be used by multiple threads")
    print("   - No external synchronization needed")
    print("   - Example: queue.Queue")

    print("\n2. Thread-compatible:")
    print("   - Safe with external synchronization")
    print("   - Not safe without locks")
    print("   - Example: list, dict")

    print("\n3. Thread-hostile:")
    print("   - Cannot be made thread-safe")
    print("   - Must use separate instances")
    print("   - Rare in Python")


def main() -> None:
    """Main function demonstrating thread synchronization."""
    print("=" * 60)
    print("PYTHON THREAD SYNCHRONIZATION")
    print("=" * 60)

    demonstrate_race_condition()
    demonstrate_race_condition_solution()
    demonstrate_deadlock()
    demonstrate_deadlock_prevention()
    demonstrate_livelock()
    demonstrate_bank_transfer_race()
    demonstrate_read_write_lock()
    demonstrate_atomic_operations()
    demonstrate_synchronization_best_practices()
    demonstrate_lock_free_data_structures()
    demonstrate_thread_safety_levels()

    print("\n" + "=" * 60)
    print("All synchronization demonstrations completed!")
    print("=" * 60)
    print("\nKey takeaways:")
    print("- Always protect shared mutable state")
    print("- Use consistent lock ordering")
    print("- Keep critical sections short")
    print("- Test with multiple threads")


if __name__ == "__main__":
    main()
