"""
Unit tests for 22_async_await program.

These tests verify:
- Advanced gather patterns
- Asyncio wait operations
- As completed processing
- Semaphore for concurrency control
- Lock for mutual exclusion
- Event for signaling
- Queue for producer-consumer
- Shield for cancellation protection
- Timeout context managers
- Task groups (Python 3.11+)
"""

import sys
from pathlib import Path
import asyncio
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_gather_advanced,
    demonstrate_wait,
    demonstrate_as_completed,
    demonstrate_semaphore,
    demonstrate_lock,
    demonstrate_event,
    demonstrate_queue,
    demonstrate_shield,
    demonstrate_timeout,
    demonstrate_task_groups,
    main,
)


class TestGatherAdvanced:
    """Test cases for demonstrate_gather_advanced()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_gather_advanced()
        assert isinstance(result, dict)

    def test_with_exceptions(self):
        """Test gather with return_exceptions=True."""
        result = demonstrate_gather_advanced()
        assert "with_exceptions" in result
        assert isinstance(result["with_exceptions"], list)
        assert len(result["with_exceptions"]) == 3

    def test_exception_captured(self):
        """Test that exception was captured in results."""
        result = demonstrate_gather_advanced()
        exceptions = result["with_exceptions"]
        # One should be an error
        assert any("failed" in str(e).lower() for e in exceptions)

    def test_fail_fast(self):
        """Test gather with fail-fast behavior."""
        result = demonstrate_gather_advanced()
        assert "fail_fast" in result
        assert "Failed" in str(result["fail_fast"])


class TestWait:
    """Test cases for demonstrate_wait()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_wait()
        assert isinstance(result, dict)

    def test_first_completed(self):
        """Test FIRST_COMPLETED functionality."""
        result = demonstrate_wait()
        first = result["first_completed"]
        assert "completed" in first
        assert "pending_count" in first
        # Should have completed 1, pending 2
        assert first["pending_count"] == 2

    def test_with_timeout(self):
        """Test wait with timeout."""
        result = demonstrate_wait()
        timeout = result["with_timeout"]
        assert timeout["done_count"] >= 1
        assert "pending_count" in timeout


class TestAsCompleted:
    """Test cases for demonstrate_as_completed()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_as_completed()
        assert isinstance(result, dict)

    def test_results_list(self):
        """Test that all results are collected."""
        result = demonstrate_as_completed()
        assert len(result["results"]) == 4

    def test_completion_order(self):
        """Test that results are in completion order."""
        result = demonstrate_as_completed()
        # First result should be Item-D (delay 0.03)
        assert result["results"][0]["item"] == "Item-D"


class TestSemaphore:
    """Test cases for demonstrate_semaphore()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_semaphore()
        assert isinstance(result, dict)

    def test_concurrency_limited(self):
        """Test that semaphore limits concurrency."""
        result = demonstrate_semaphore()
        time_str = result["time"]
        time_val = float(time_str.replace("s", ""))
        # 5 tasks, 2 concurrent, 0.1s each -> ~0.3s minimum
        assert time_val >= 0.20

    def test_all_completed(self):
        """Test that all workers completed."""
        result = demonstrate_semaphore()
        assert len(result["results"]) == 5


class TestLock:
    """Test cases for demonstrate_lock()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_lock()
        assert isinstance(result, dict)

    def test_with_lock_correct(self):
        """Test that lock ensures correct count."""
        result = demonstrate_lock()
        assert result["with_lock"] == 9

    def test_without_lock_race_condition(self):
        """Test that without lock causes race condition."""
        result = demonstrate_lock()
        # Without lock, result may be less than 9
        assert result["without_lock"] <= 9

    def test_expected_value(self):
        """Test expected value is documented."""
        result = demonstrate_lock()
        assert result["expected"] == 9


class TestEvent:
    """Test cases for demonstrate_event()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_event()
        assert isinstance(result, dict)

    def test_all_waiters_received_signal(self):
        """Test that all waiters received the signal."""
        result = demonstrate_event()
        assert len(result["results"]) == 3

    def test_signal_content(self):
        """Test signal content."""
        result = demonstrate_event()
        for r in result["results"]:
            assert "received signal" in r


class TestQueue:
    """Test cases for demonstrate_queue()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_queue()
        assert isinstance(result, dict)

    def test_items_consumed(self):
        """Test that items were consumed."""
        result = demonstrate_queue()
        assert result["total_consumed"] == 6

    def test_consumer_pattern(self):
        """Test producer-consumer pattern."""
        result = demonstrate_queue()
        # Each result should have "got" in it
        assert all("got" in r for r in result["results"])


class TestShield:
    """Test cases for demonstrate_shield()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_shield()
        assert isinstance(result, dict)

    def test_task_completed(self):
        """Test that shielded task completed despite cancellation."""
        result = demonstrate_shield()
        assert "completed" in result["result"].lower()


class TestTimeout:
    """Test cases for demonstrate_timeout()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_timeout()
        assert isinstance(result, dict)

    def test_fast_operation_succeeds(self):
        """Test that fast operation completes."""
        result = demonstrate_timeout()
        assert result["results"]["fast"] != "Timeout"

    def test_slow_operation_times_out(self):
        """Test that slow operation times out."""
        result = demonstrate_timeout()
        assert result["results"]["slow"] == "Timeout"


class TestTaskGroups:
    """Test cases for demonstrate_task_groups()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_task_groups()
        assert isinstance(result, dict)

    def test_all_tasks_completed(self):
        """Test that all tasks completed."""
        result = demonstrate_task_groups()
        assert len(result["results"]) == 3

    def test_task_results(self):
        """Test task results."""
        result = demonstrate_task_groups()
        for r in result["results"]:
            assert "done" in r


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
        assert "Program 22" in captured.out
        assert "Async/Await" in captured.out

    def test_main_all_demonstrations(self, capsys):
        """Test that main() runs all demonstrations."""
        main()
        captured = capsys.readouterr()
        demonstrations = [
            "Gather Advanced",
            "Asyncio Wait",
            "As Completed",
            "Semaphore",
            "Lock",
            "Event",
            "Queue",
            "Shield",
            "Timeout",
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

    def test_multiple_executions(self):
        """Test that functions can be called multiple times."""
        result1 = demonstrate_lock()
        result2 = demonstrate_lock()
        # Both should have correct value with lock
        assert result1["with_lock"] == 9
        assert result2["with_lock"] == 9

    def test_synchronization_primitives(self):
        """Test that synchronization primitives work correctly."""
        results = [
            demonstrate_lock(),
            demonstrate_event(),
            demonstrate_semaphore(),
        ]
        assert all(isinstance(r, dict) for r in results)


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
