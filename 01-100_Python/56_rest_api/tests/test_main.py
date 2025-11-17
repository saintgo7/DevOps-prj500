"""
Unit tests for 56_rest_api program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_complete_api,
    demonstrate_error_handling,
    demonstrate_filtering_sorting,
    demonstrate_api_testing,
    main
)


class TestCompleteApi:
    """Test cases for demonstrate_complete_api()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_complete_api()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_complete_api()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_complete_api()
        assert len(result) > 0

class TestErrorHandling:
    """Test cases for demonstrate_error_handling()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_error_handling()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_error_handling()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_error_handling()
        assert len(result) > 0

class TestFilteringSorting:
    """Test cases for demonstrate_filtering_sorting()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_filtering_sorting()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_filtering_sorting()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_filtering_sorting()
        assert len(result) > 0

class TestApiTesting:
    """Test cases for demonstrate_api_testing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_api_testing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_api_testing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_api_testing()
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
        assert "Program 56" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
