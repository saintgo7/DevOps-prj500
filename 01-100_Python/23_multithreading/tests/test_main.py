"""
Unit tests for 23_multithreading program.

These tests verify:
- Basic thread creation and execution
- Thread subclassing
- Daemon vs non-daemon threads
- Thread lock for synchronization
- RLock for reentrant locking
- Semaphore for limiting concurrent access
- Event for thread signaling
- Condition for complex synchronization
- Thread pool with Queue
- Thread-local storage
"""

import sys
from pathlib import Path
import pytest
import threading

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_thread,
    demonstrate_thread_class,
    demonstrate_daemon_threads,
    demonstrate_thread_lock,
    demonstrate_rlock,
    demonstrate_semaphore,
    demonstrate_event,
    demonstrate_condition,
    demonstrate_thread_pool,
    demonstrate_thread_local,
    main,
)


class TestBasicThread:
    """Test cases for demonstrate_basic_thread()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_thread()
        assert isinstance(result, dict)

    def test_results_created(self):
        """Test that threads produced results."""
        result = demonstrate_basic_thread()
        assert len(result["results"]) == 6  # 2 threads * 3 iterations

    def test_concurrent_execution(self):
        """Test that threads ran concurrently."""
        result = demonstrate_basic_thread()
        time_str = result["time"]
        time_val = float(time_str.replace("s", ""))
        # Should be ~0.03s concurrent, not ~0.06s sequential
        assert time_val < 0.08


class TestThreadClass:
    """Test cases for demonstrate_thread_class()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_thread_class()
        assert isinstance(result, dict)

    def test_thread1_sum(self):
        """Test thread 1 calculation."""
        result = demonstrate_thread_class()
        assert result["thread1_result"] == 15  # sum(1,2,3,4,5)

    def test_thread2_sum(self):
        """Test thread 2 calculation."""
        result = demonstrate_thread_class()
        assert result["thread2_result"] == 60  # sum(10,20,30)


class TestDaemonThreads:
    """Test cases for demonstrate_daemon_threads()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_daemon_threads()
        assert isinstance(result, dict)

    def test_regular_count(self):
        """Test that regular thread completed fully."""
        result = demonstrate_daemon_threads()
        assert result["regular_count"] == 4  # 0-4

    def test_daemon_may_not_complete(self):
        """Test that daemon thread may not complete."""
        result = demonstrate_daemon_threads()
        # Daemon may have been interrupted
        assert result["daemon_count"] >= 0


class TestThreadLock:
    """Test cases for demonstrate_thread_lock()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_thread_lock()
        assert isinstance(result, dict)

    def test_lock_ensures_correctness(self):
        """Test that lock ensures correct count."""
        result = demonstrate_thread_lock()
        assert result["final_count"] == 300

    def test_expected_value(self):
        """Test expected value is documented."""
        result = demonstrate_thread_lock()
        assert result["expected"] == 300


class TestRLock:
    """Test cases for demonstrate_rlock()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_rlock()
        assert isinstance(result, dict)

    def test_recursive_results(self):
        """Test recursive function results."""
        result = demonstrate_rlock()
        assert result["results"] == [5, 4, 3, 2, 1]


class TestSemaphore:
    """Test cases for demonstrate_semaphore()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_semaphore()
        assert isinstance(result, dict)

    def test_max_concurrent(self):
        """Test that semaphore limits concurrency."""
        result = demonstrate_semaphore()
        # Semaphore(2) means max 2 concurrent
        assert result["max_concurrent"] <= 2

    def test_timing(self):
        """Test that execution time reflects limited concurrency."""
        result = demonstrate_semaphore()
        time_str = result["time"]
        time_val = float(time_str.replace("s", ""))
        # 5 workers, 2 concurrent, 0.1s each -> ~0.3s minimum
        assert time_val >= 0.20


class TestEvent:
    """Test cases for demonstrate_event()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_event()
        assert isinstance(result, dict)

    def test_events_recorded(self):
        """Test that events were recorded."""
        result = demonstrate_event()
        assert result["total_events"] >= 7  # 3 waiting + 1 set + 3 proceeding


class TestCondition:
    """Test cases for demonstrate_condition()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_condition()
        assert isinstance(result, dict)

    def test_all_items_consumed(self):
        """Test that all items were consumed."""
        result = demonstrate_condition()
        assert len(result["consumed"]) == 5


class TestThreadPool:
    """Test cases for demonstrate_thread_pool()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_thread_pool()
        assert isinstance(result, dict)

    def test_all_tasks_processed(self):
        """Test that all tasks were processed."""
        result = demonstrate_thread_pool()
        assert len(result["results"]) == 10

    def test_correct_calculations(self):
        """Test that calculations are correct."""
        result = demonstrate_thread_pool()
        # 0^2, 1^2, 2^2, ..., 9^2
        expected = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
        assert result["results"] == expected

    def test_worker_count(self):
        """Test worker count."""
        result = demonstrate_thread_pool()
        assert result["workers"] == 3

    def test_task_count(self):
        """Test task count."""
        result = demonstrate_thread_pool()
        assert result["tasks"] == 10


class TestThreadLocal:
    """Test cases for demonstrate_thread_local()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_thread_local()
        assert isinstance(result, dict)

    def test_all_threads_completed(self):
        """Test that all threads completed."""
        result = demonstrate_thread_local()
        assert len(result["results"]) == 5

    def test_thread_isolation(self):
        """Test that each thread has its own value."""
        result = demonstrate_thread_local()
        # Each thread should have its own value: 0, 10, 20, 30, 40
        expected_values = {0, 10, 20, 30, 40}
        actual_values = set(result["results"].values())
        assert actual_values == expected_values


class TestMainFunction:
    """Test cases for the main() function."""

    def test_main_runs_without_error(self, capsys):
        """Test that main() executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    def test_main_produces_output(self, capsys):
        """Test that main() produces output."""
        main()
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_main_header(self, capsys):
        """Test that main() prints header."""
        main()
        captured = capsys.readouterr()
        assert "Program 23" in captured.out
        assert "Multithreading" in captured.out

    def test_main_all_demonstrations(self, capsys):
        """Test that main() runs all demonstrations."""
        main()
        captured = capsys.readouterr()
        demonstrations = [
            "Basic Thread",
            "Thread Class",
            "Daemon Threads",
            "Thread Lock",
            "RLock",
            "Semaphore",
            "Event",
            "Condition",
            "Thread Pool",
            "Thread Local",
        ]
        for demo in demonstrations:
            assert demo in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_thread_safety(self):
        """Test that thread lock ensures thread safety."""
        # Run multiple times to check for race conditions
        for _ in range(5):
            result = demonstrate_thread_lock()
            assert result["final_count"] == 300

    def test_multiple_executions(self):
        """Test that functions can be called multiple times."""
        result1 = demonstrate_basic_thread()
        result2 = demonstrate_basic_thread()
        assert len(result1["results"]) == len(result2["results"])


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
