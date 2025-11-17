"""
Unit tests for 35_debugging program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_print_debugging,
    demonstrate_assert_debugging,
    demonstrate_traceback_inspection,
    demonstrate_traceback_extraction,
    demonstrate_inspect_module,
    demonstrate_stack_inspection,
    demonstrate_locals_globals,
    demonstrate_custom_exception_hook,
    demonstrate_debugging_decorators,
    demonstrate_object_inspection,
    main
)


class TestPrintDebugging:
    """Test cases for demonstrate_print_debugging()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_print_debugging()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_print_debugging()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_print_debugging()
        assert len(result) > 0

class TestAssertDebugging:
    """Test cases for demonstrate_assert_debugging()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_assert_debugging()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_assert_debugging()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_assert_debugging()
        assert len(result) > 0

class TestTracebackInspection:
    """Test cases for demonstrate_traceback_inspection()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_traceback_inspection()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_traceback_inspection()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_traceback_inspection()
        assert len(result) > 0

class TestTracebackExtraction:
    """Test cases for demonstrate_traceback_extraction()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_traceback_extraction()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_traceback_extraction()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_traceback_extraction()
        assert len(result) > 0

class TestInspectModule:
    """Test cases for demonstrate_inspect_module()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_inspect_module()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_inspect_module()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_inspect_module()
        assert len(result) > 0

class TestStackInspection:
    """Test cases for demonstrate_stack_inspection()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_stack_inspection()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_stack_inspection()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_stack_inspection()
        assert len(result) > 0

class TestLocalsGlobals:
    """Test cases for demonstrate_locals_globals()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_locals_globals()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_locals_globals()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_locals_globals()
        assert len(result) > 0

class TestCustomExceptionHook:
    """Test cases for demonstrate_custom_exception_hook()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_custom_exception_hook()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_custom_exception_hook()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_custom_exception_hook()
        assert len(result) > 0

class TestDebuggingDecorators:
    """Test cases for demonstrate_debugging_decorators()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_debugging_decorators()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_debugging_decorators()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_debugging_decorators()
        assert len(result) > 0

class TestObjectInspection:
    """Test cases for demonstrate_object_inspection()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_object_inspection()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_object_inspection()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_object_inspection()
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
        assert "Program 35" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
