"""
Unit tests for 26_context_managers program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_context_manager,
    demonstrate_exception_handling,
    demonstrate_contextlib_decorator,
    demonstrate_multiple_contexts,
    demonstrate_closing,
    demonstrate_suppress,
    demonstrate_redirect_stdout,
    demonstrate_exitstack,
    demonstrate_reusable_context,
    demonstrate_practical_examples,
    main
)


class TestBasicContextManager:
    """Test cases for demonstrate_basic_context_manager()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_context_manager()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_context_manager()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_context_manager()
        assert len(result) > 0

class TestExceptionHandling:
    """Test cases for demonstrate_exception_handling()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_exception_handling()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_exception_handling()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_exception_handling()
        assert len(result) > 0

class TestContextlibDecorator:
    """Test cases for demonstrate_contextlib_decorator()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_contextlib_decorator()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_contextlib_decorator()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_contextlib_decorator()
        assert len(result) > 0

class TestMultipleContexts:
    """Test cases for demonstrate_multiple_contexts()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_multiple_contexts()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_multiple_contexts()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_multiple_contexts()
        assert len(result) > 0

class TestClosing:
    """Test cases for demonstrate_closing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_closing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_closing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_closing()
        assert len(result) > 0

class TestSuppress:
    """Test cases for demonstrate_suppress()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_suppress()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_suppress()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_suppress()
        assert len(result) > 0

class TestRedirectStdout:
    """Test cases for demonstrate_redirect_stdout()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_redirect_stdout()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_redirect_stdout()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_redirect_stdout()
        assert len(result) > 0

class TestExitstack:
    """Test cases for demonstrate_exitstack()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_exitstack()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_exitstack()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_exitstack()
        assert len(result) > 0

class TestReusableContext:
    """Test cases for demonstrate_reusable_context()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_reusable_context()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_reusable_context()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_reusable_context()
        assert len(result) > 0

class TestPracticalExamples:
    """Test cases for demonstrate_practical_examples()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_practical_examples()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_practical_examples()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_practical_examples()
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
        assert "Program 26" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
