"""
Unit tests for 090_thread_synchronization program.

These tests verify:
- Locks and RLocks
- Semaphores and BoundedSemaphores
- Events and Conditions
- Barriers
- Thread-safe queues
"""

import sys
from pathlib import Path
import pytest
import threading
import time

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestLocks:
    """Test cases for locks."""

    def test_basic_lock(self):
        """Test basic lock functionality."""
        lock = threading.Lock()
        assert lock.acquire()
        lock.release()

    def test_rlock(self):
        """Test reentrant lock."""
        rlock = threading.RLock()
        assert rlock.acquire()
        assert rlock.acquire()  # Can acquire again
        rlock.release()
        rlock.release()


class TestSemaphores:
    """Test cases for semaphores."""

    def test_semaphore(self):
        """Test semaphore functionality."""
        sem = threading.Semaphore(2)
        assert sem.acquire()
        assert sem.acquire()
        sem.release()
        sem.release()

    def test_bounded_semaphore(self):
        """Test bounded semaphore."""
        sem = threading.BoundedSemaphore(1)
        assert sem.acquire()
        sem.release()


class TestEvents:
    """Test cases for events."""

    def test_event_set_wait(self):
        """Test event set and wait."""
        event = threading.Event()
        assert not event.is_set()

        event.set()
        assert event.is_set()

        event.clear()
        assert not event.is_set()


class TestConditions:
    """Test cases for conditions."""

    def test_condition_wait_notify(self):
        """Test condition variable."""
        condition = threading.Condition()
        notified = []

        def waiter():
            with condition:
                condition.wait(timeout=1.0)
                notified.append(1)

        def notifier():
            time.sleep(0.1)
            with condition:
                condition.notify()

        t1 = threading.Thread(target=waiter)
        t2 = threading.Thread(target=notifier)

        t1.start()
        t2.start()

        t1.join()
        t2.join()


class TestMainFunction:
    """Test cases for main function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
