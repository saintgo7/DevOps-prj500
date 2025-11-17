"""
Unit tests for 21_asyncio_basics program.

These tests verify:
- Basic coroutine functionality
- Multiple coroutines execution
- Await keyword usage
- Task creation and management
- Asyncio gather operations
- Timeout handling
- Task cancellation
- Async context managers
- Async iteration
- Coroutine chaining
"""

import sys
from pathlib import Path
import asyncio
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_coroutine,
    demonstrate_multiple_coroutines,
    demonstrate_await_keyword,
    demonstrate_create_task,
    demonstrate_gather,
    demonstrate_wait_for,
    demonstrate_task_cancellation,
    demonstrate_async_context_manager,
    demonstrate_async_iteration,
    demonstrate_coroutine_chaining,
    main,
)


class TestBasicCoroutine:
    """Test cases for demonstrate_basic_coroutine()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_coroutine()
        assert isinstance(result, dict)

    def test_simple_result(self):
        """Test simple coroutine result."""
        result = demonstrate_basic_coroutine()
        assert result["simple_result"] == "Hello from coroutine!"

    def test_delayed_result(self):
        """Test delayed greeting result."""
        result = demonstrate_basic_coroutine()
        assert result["delayed_result"] == "Hello, Alice!"

    def test_time_elapsed(self):
        """Test that time elapsed is tracked."""
        result = demonstrate_basic_coroutine()
        assert "time_elapsed" in result
        assert "s" in result["time_elapsed"]

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_coroutine()
        assert "note" in result
        assert "async def" in result["note"]


class TestMultipleCoroutines:
    """Test cases for demonstrate_multiple_coroutines()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_multiple_coroutines()
        assert isinstance(result, dict)

    def test_results_list(self):
        """Test that results is a list."""
        result = demonstrate_multiple_coroutines()
        assert isinstance(result["results"], list)
        assert len(result["results"]) == 3

    def test_concurrent_execution(self):
        """Test that tasks run concurrently."""
        result = demonstrate_multiple_coroutines()
        # All three tasks should complete in ~0.2s, not 0.45s
        time_str = result["total_time"]
        time_val = float(time_str.replace("s", ""))
        assert time_val < 0.35  # Allow some overhead

    def test_all_tasks_completed(self):
        """Test that all tasks completed successfully."""
        result = demonstrate_multiple_coroutines()
        assert all("completed" in r for r in result["results"])


class TestAwaitKeyword:
    """Test cases for demonstrate_await_keyword()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_await_keyword()
        assert isinstance(result, dict)

    def test_result_structure(self):
        """Test result has correct structure."""
        result = demonstrate_await_keyword()
        assert "result" in result
        assert isinstance(result["result"], dict)

    def test_data_fetched(self):
        """Test that data was fetched."""
        result = demonstrate_await_keyword()
        data = result["result"]
        assert data["source"] == "API"
        assert "data" in data

    def test_data_processed(self):
        """Test that data was processed."""
        result = demonstrate_await_keyword()
        data = result["result"]
        assert data["processed"] is True


class TestCreateTask:
    """Test cases for demonstrate_create_task()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_create_task()
        assert isinstance(result, dict)

    def test_results_list(self):
        """Test that results is a list."""
        result = demonstrate_create_task()
        assert isinstance(result["results"], list)

    def test_task_count(self):
        """Test correct number of tasks."""
        result = demonstrate_create_task()
        assert result["task_count"] == 2

    def test_counter_results(self):
        """Test that counter tasks produced results."""
        result = demonstrate_create_task()
        # 2 tasks, 3 counts each = 6 results
        assert len(result["results"]) == 6


class TestGather:
    """Test cases for demonstrate_gather()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_gather()
        assert isinstance(result, dict)

    def test_downloads_completed(self):
        """Test that all downloads completed."""
        result = demonstrate_gather()
        assert len(result["downloads"]) == 3

    def test_download_structure(self):
        """Test download result structure."""
        result = demonstrate_gather()
        for download in result["downloads"]:
            assert "url" in download
            assert "size" in download
            assert "status" in download
            assert download["status"] == "completed"

    def test_concurrent_timing(self):
        """Test that downloads ran concurrently."""
        result = demonstrate_gather()
        time_str = result["total_time"]
        time_val = float(time_str.replace("s", ""))
        # Should take ~0.05s (max), not 0.12s (sum)
        assert time_val < 0.10


class TestWaitFor:
    """Test cases for demonstrate_wait_for()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_wait_for()
        assert isinstance(result, dict)

    def test_fast_operation_succeeds(self):
        """Test that fast operation completes."""
        result = demonstrate_wait_for()
        assert result["results"]["fast"] != "Timeout"

    def test_slow_operation_times_out(self):
        """Test that slow operation times out."""
        result = demonstrate_wait_for()
        assert result["results"]["slow"] == "Timeout"


class TestTaskCancellation:
    """Test cases for demonstrate_task_cancellation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_task_cancellation()
        assert isinstance(result, dict)

    def test_task_was_cancelled(self):
        """Test that task was successfully cancelled."""
        result = demonstrate_task_cancellation()
        assert "cancelled" in result["result"].lower()


class TestAsyncContextManager:
    """Test cases for demonstrate_async_context_manager()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_async_context_manager()
        assert isinstance(result, dict)

    def test_resource_acquired(self):
        """Test that resource was acquired."""
        result = demonstrate_async_context_manager()
        assert "Resource acquired" in result["result"]


class TestAsyncIteration:
    """Test cases for demonstrate_async_iteration()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_async_iteration()
        assert isinstance(result, dict)

    def test_iteration_results(self):
        """Test async iteration results."""
        result = demonstrate_async_iteration()
        assert result["results"] == [0, 1, 2, 3, 4]


class TestCoroutineChaining:
    """Test cases for demonstrate_coroutine_chaining()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_coroutine_chaining()
        assert isinstance(result, dict)

    def test_pipeline_structure(self):
        """Test pipeline result structure."""
        result = demonstrate_coroutine_chaining()
        pipeline = result["pipeline"]
        assert "initial" in pipeline
        assert "after_step1" in pipeline
        assert "after_step2" in pipeline
        assert "final" in pipeline

    def test_pipeline_computation(self):
        """Test pipeline computations."""
        result = demonstrate_coroutine_chaining()
        pipeline = result["pipeline"]
        # 5 -> step1 (*2) -> 10 -> step2 (+10) -> 20 -> step3 (**2) -> 400
        assert pipeline["initial"] == 5
        assert pipeline["after_step1"] == 10
        assert pipeline["after_step2"] == 20
        assert pipeline["final"] == 400


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
        assert "Program 21" in captured.out
        assert "Asyncio Basics" in captured.out

    def test_main_all_demonstrations(self, capsys):
        """Test that main() runs all demonstrations."""
        main()
        captured = capsys.readouterr()
        demonstrations = [
            "Basic Coroutine",
            "Multiple Coroutines",
            "Await Keyword",
            "Create Task",
            "Asyncio Gather",
            "Wait For",
            "Task Cancellation",
            "Async Context Manager",
            "Async Iteration",
            "Coroutine Chaining",
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

    def test_functions_are_synchronous(self):
        """Test that demonstrate functions are synchronous wrappers."""
        # These functions should be callable without await
        result = demonstrate_basic_coroutine()
        assert isinstance(result, dict)

    def test_multiple_executions(self):
        """Test that functions can be called multiple times."""
        result1 = demonstrate_basic_coroutine()
        result2 = demonstrate_basic_coroutine()
        assert result1["simple_result"] == result2["simple_result"]

    def test_concurrent_demonstrations(self):
        """Test running multiple demonstrations."""
        results = [
            demonstrate_basic_coroutine(),
            demonstrate_multiple_coroutines(),
            demonstrate_await_keyword(),
        ]
        assert len(results) == 3
        assert all(isinstance(r, dict) for r in results)


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
