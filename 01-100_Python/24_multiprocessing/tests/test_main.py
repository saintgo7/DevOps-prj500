"""
Unit tests for 24_multiprocessing program.

These tests verify:
- Basic process creation and execution
- Process subclassing
- Process pool for parallel map
- Pool apply methods
- Shared memory with Value and Array
- Manager for sharing complex structures
- Queue for inter-process communication
- Pipe for two-way communication
- Lock for process synchronization
- Pool context manager and callbacks
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_process,
    demonstrate_process_class,
    demonstrate_pool,
    demonstrate_pool_apply,
    demonstrate_shared_memory,
    demonstrate_manager,
    demonstrate_queue,
    demonstrate_pipe,
    demonstrate_lock,
    demonstrate_pool_context,
    main,
)


class TestBasicProcess:
    """Test cases for demonstrate_basic_process()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_process()
        assert isinstance(result, dict)

    def test_main_pid(self):
        """Test that main PID is recorded."""
        result = demonstrate_basic_process()
        assert "main_pid" in result
        assert result["main_pid"] > 0

    def test_process_results(self):
        """Test that processes produced results."""
        result = demonstrate_basic_process()
        assert len(result["results"]) == 3


class TestProcessClass:
    """Test cases for demonstrate_process_class()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_process_class()
        assert isinstance(result, dict)

    def test_results_count(self):
        """Test correct number of results."""
        result = demonstrate_process_class()
        assert len(result["results"]) == 2


class TestPool:
    """Test cases for demonstrate_pool()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_pool()
        assert isinstance(result, dict)

    def test_squares(self):
        """Test square calculations."""
        result = demonstrate_pool()
        expected = [i**2 for i in range(10)]
        assert result["squares"] == expected

    def test_cubes(self):
        """Test cube calculations."""
        result = demonstrate_pool()
        expected = [i**3 for i in range(10)]
        assert result["cubes"] == expected


class TestPoolApply:
    """Test cases for demonstrate_pool_apply()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_pool_apply()
        assert isinstance(result, dict)

    def test_apply_result(self):
        """Test apply result."""
        result = demonstrate_pool_apply()
        assert result["apply_result"] == 5 * 3 + 5  # 20

    def test_apply_async_result(self):
        """Test apply_async result."""
        result = demonstrate_pool_apply()
        assert result["apply_async_result"] == 4 * 2 + 4  # 12

    def test_starmap_results(self):
        """Test starmap results."""
        result = demonstrate_pool_apply()
        expected = [1*2+1, 3*4+3, 5*6+5]
        assert result["starmap_results"] == expected


class TestSharedMemory:
    """Test cases for demonstrate_shared_memory()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_shared_memory()
        assert isinstance(result, dict)

    def test_shared_value(self):
        """Test shared value incremented correctly."""
        result = demonstrate_shared_memory()
        assert result["shared_value"] == 5

    def test_shared_array(self):
        """Test shared array incremented correctly."""
        result = demonstrate_shared_memory()
        assert result["shared_array"] == [5, 5, 5]


class TestManager:
    """Test cases for demonstrate_manager()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_manager()
        assert isinstance(result, dict)

    def test_shared_dict(self):
        """Test shared dictionary."""
        result = demonstrate_manager()
        assert len(result["shared_dict"]) == 3

    def test_shared_list(self):
        """Test shared list."""
        result = demonstrate_manager()
        assert len(result["shared_list"]) == 3


class TestQueue:
    """Test cases for demonstrate_queue()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_queue()
        assert isinstance(result, dict)

    def test_all_items_consumed(self):
        """Test that all items were consumed."""
        result = demonstrate_queue()
        assert len(result["results"]) == 5


class TestPipe:
    """Test cases for demonstrate_pipe()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_pipe()
        assert isinstance(result, dict)

    def test_data_sent(self):
        """Test data was sent."""
        result = demonstrate_pipe()
        assert result["sent"] == "hello from parent"

    def test_data_received(self):
        """Test data was received and processed."""
        result = demonstrate_pipe()
        assert result["received"] == "HELLO FROM PARENT"


class TestLock:
    """Test cases for demonstrate_lock()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_lock()
        assert isinstance(result, dict)

    def test_lock_ensures_correctness(self):
        """Test that lock ensures correct count."""
        result = demonstrate_lock()
        assert result["final_value"] == 30

    def test_expected_value(self):
        """Test expected value."""
        result = demonstrate_lock()
        assert result["expected"] == 30


class TestPoolContext:
    """Test cases for demonstrate_pool_context()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_pool_context()
        assert isinstance(result, dict)

    def test_has_successes(self):
        """Test that some tasks succeeded."""
        result = demonstrate_pool_context()
        assert len(result["successes"]) > 0

    def test_has_errors(self):
        """Test that one task failed."""
        result = demonstrate_pool_context()
        assert len(result["errors"]) >= 1


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
        assert "Program 24" in captured.out
        assert "Multiprocessing" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
