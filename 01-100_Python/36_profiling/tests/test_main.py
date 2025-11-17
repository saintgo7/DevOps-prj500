"""
Unit tests for 36_profiling program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_timeit_basic,
    demonstrate_time_decorator,
    demonstrate_cprofile_basic,
    demonstrate_profile_analysis,
    demonstrate_memory_profiling,
    demonstrate_line_profiling_concept,
    demonstrate_algorithm_comparison,
    demonstrate_caching_performance,
    demonstrate_datastructure_performance,
    demonstrate_optimization_techniques,
    main
)


class TestTimeitBasic:
    """Test cases for demonstrate_timeit_basic()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_timeit_basic()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_timeit_basic()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_timeit_basic()
        assert len(result) > 0

class TestTimeDecorator:
    """Test cases for demonstrate_time_decorator()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_time_decorator()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_time_decorator()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_time_decorator()
        assert len(result) > 0

class TestCprofileBasic:
    """Test cases for demonstrate_cprofile_basic()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_cprofile_basic()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_cprofile_basic()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_cprofile_basic()
        assert len(result) > 0

class TestProfileAnalysis:
    """Test cases for demonstrate_profile_analysis()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_profile_analysis()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_profile_analysis()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_profile_analysis()
        assert len(result) > 0

class TestMemoryProfiling:
    """Test cases for demonstrate_memory_profiling()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_memory_profiling()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_memory_profiling()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_memory_profiling()
        assert len(result) > 0

class TestLineProfilingConcept:
    """Test cases for demonstrate_line_profiling_concept()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_line_profiling_concept()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_line_profiling_concept()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_line_profiling_concept()
        assert len(result) > 0

class TestAlgorithmComparison:
    """Test cases for demonstrate_algorithm_comparison()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_algorithm_comparison()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_algorithm_comparison()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_algorithm_comparison()
        assert len(result) > 0

class TestCachingPerformance:
    """Test cases for demonstrate_caching_performance()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_caching_performance()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_caching_performance()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_caching_performance()
        assert len(result) > 0

class TestDatastructurePerformance:
    """Test cases for demonstrate_datastructure_performance()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_datastructure_performance()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_datastructure_performance()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_datastructure_performance()
        assert len(result) > 0

class TestOptimizationTechniques:
    """Test cases for demonstrate_optimization_techniques()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_optimization_techniques()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_optimization_techniques()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_optimization_techniques()
        assert len(result) > 0


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
        assert "Program 36" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
