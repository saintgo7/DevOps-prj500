"""
Unit tests for 34_logging program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_logging,
    demonstrate_logger_hierarchy,
    demonstrate_formatters,
    demonstrate_handlers,
    demonstrate_filters,
    demonstrate_configuration,
    demonstrate_contextual_logging,
    demonstrate_exception_logging,
    demonstrate_rotating_file_handler,
    demonstrate_logger_adapter,
    main
)


class TestBasicLogging:
    """Test cases for demonstrate_basic_logging()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_logging()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_logging()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_logging()
        assert len(result) > 0

class TestLoggerHierarchy:
    """Test cases for demonstrate_logger_hierarchy()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_logger_hierarchy()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_logger_hierarchy()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_logger_hierarchy()
        assert len(result) > 0

class TestFormatters:
    """Test cases for demonstrate_formatters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_formatters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_formatters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_formatters()
        assert len(result) > 0

class TestHandlers:
    """Test cases for demonstrate_handlers()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_handlers()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_handlers()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_handlers()
        assert len(result) > 0

class TestFilters:
    """Test cases for demonstrate_filters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_filters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_filters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_filters()
        assert len(result) > 0

class TestConfiguration:
    """Test cases for demonstrate_configuration()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_configuration()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_configuration()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_configuration()
        assert len(result) > 0

class TestContextualLogging:
    """Test cases for demonstrate_contextual_logging()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_contextual_logging()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_contextual_logging()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_contextual_logging()
        assert len(result) > 0

class TestExceptionLogging:
    """Test cases for demonstrate_exception_logging()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_exception_logging()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_exception_logging()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_exception_logging()
        assert len(result) > 0

class TestRotatingFileHandler:
    """Test cases for demonstrate_rotating_file_handler()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_rotating_file_handler()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_rotating_file_handler()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_rotating_file_handler()
        assert len(result) > 0

class TestLoggerAdapter:
    """Test cases for demonstrate_logger_adapter()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_logger_adapter()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_logger_adapter()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_logger_adapter()
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
        assert "Program 34" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
