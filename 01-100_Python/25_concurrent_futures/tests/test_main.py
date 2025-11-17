"""
Unit tests for 25_concurrent_futures program.

These tests verify:
- ThreadPoolExecutor basics
- ProcessPoolExecutor for CPU-bound tasks
- Executor map method
- as_completed for processing results
- Future object methods
- wait() function with different conditions
- Future callbacks
- Timeout handling
- Exception handling in futures
- Context manager best practices
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_thread_pool_executor,
    demonstrate_process_pool_executor,
    demonstrate_map,
    demonstrate_as_completed,
    demonstrate_future_methods,
    demonstrate_wait,
    demonstrate_callbacks,
    demonstrate_timeout,
    demonstrate_exception_handling,
    demonstrate_context_manager,
    main,
)


class TestThreadPoolExecutor:
    """Test cases for demonstrate_thread_pool_executor()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_thread_pool_executor()
        assert isinstance(result, dict)

    def test_all_tasks_completed(self):
        """Test that all tasks completed."""
        result = demonstrate_thread_pool_executor()
        assert len(result["results"]) == 3

    def test_results_content(self):
        """Test results contain completion messages."""
        result = demonstrate_thread_pool_executor()
        for r in result["results"]:
            assert "completed" in r


class TestProcessPoolExecutor:
    """Test cases for demonstrate_process_pool_executor()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_process_pool_executor()
        assert isinstance(result, dict)

    def test_task_count(self):
        """Test correct number of tasks."""
        result = demonstrate_process_pool_executor()
        assert result["task_count"] == 5

    def test_all_results_equal(self):
        """Test all results are equal (same calculation)."""
        result = demonstrate_process_pool_executor()
        assert result["all_equal"] is True


class TestMap:
    """Test cases for demonstrate_map()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_map()
        assert isinstance(result, dict)

    def test_thread_results(self):
        """Test thread pool map results."""
        result = demonstrate_map()
        expected = [i**2 for i in range(10)]
        assert result["thread_results"] == expected

    def test_process_results(self):
        """Test process pool map results."""
        result = demonstrate_map()
        expected = [i**2 for i in range(10)]
        assert result["process_results"] == expected


class TestAsCompleted:
    """Test cases for demonstrate_as_completed()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_as_completed()
        assert isinstance(result, dict)

    def test_all_results_collected(self):
        """Test that all results were collected."""
        result = demonstrate_as_completed()
        assert len(result["results"]) == 4

    def test_first_completed_first(self):
        """Test that fastest task completed first."""
        result = demonstrate_as_completed()
        # Task with 0.03s delay should finish first
        assert result["results"][0]["url"] == "file4.txt"


class TestFutureMethods:
    """Test cases for demonstrate_future_methods()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_future_methods()
        assert isinstance(result, dict)

    def test_has_result(self):
        """Test that future returned result."""
        result = demonstrate_future_methods()
        assert "Completed" in result["result"]

    def test_done_after_result(self):
        """Test that future is done after getting result."""
        result = demonstrate_future_methods()
        assert result["done_after_result"] is True


class TestWait:
    """Test cases for demonstrate_wait()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_wait()
        assert isinstance(result, dict)

    def test_first_completed(self):
        """Test that first task completed."""
        result = demonstrate_wait()
        assert "done" in result["first_completed"]

    def test_pending_count(self):
        """Test pending count."""
        result = demonstrate_wait()
        assert result["pending_when_first_done"] == 3


class TestCallbacks:
    """Test cases for demonstrate_callbacks()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_callbacks()
        assert isinstance(result, dict)

    def test_callbacks_called(self):
        """Test that callbacks were called."""
        result = demonstrate_callbacks()
        assert len(result["callbacks"]) == 2


class TestTimeout:
    """Test cases for demonstrate_timeout()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_timeout()
        assert isinstance(result, dict)

    def test_timeout_occurred(self):
        """Test that timeout occurred."""
        result = demonstrate_timeout()
        assert result["result"] == "Timeout"


class TestExceptionHandling:
    """Test cases for demonstrate_exception_handling()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_exception_handling()
        assert isinstance(result, dict)

    def test_has_successes(self):
        """Test that some tasks succeeded."""
        result = demonstrate_exception_handling()
        assert len(result["successes"]) == 4  # 0, 1, 2, 4 (not 3)

    def test_has_errors(self):
        """Test that one task failed."""
        result = demonstrate_exception_handling()
        assert len(result["errors"]) == 1


class TestContextManager:
    """Test cases for demonstrate_context_manager()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_context_manager()
        assert isinstance(result, dict)

    def test_with_context(self):
        """Test context manager results."""
        result = demonstrate_context_manager()
        expected = [i * 2 for i in range(5)]
        assert result["with_context"] == expected

    def test_manual_shutdown(self):
        """Test manual shutdown results."""
        result = demonstrate_context_manager()
        expected = [i * 2 for i in range(5)]
        assert result["manual_shutdown"] == expected


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
        assert "Program 25" in captured.out
        assert "Concurrent Futures" in captured.out


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
