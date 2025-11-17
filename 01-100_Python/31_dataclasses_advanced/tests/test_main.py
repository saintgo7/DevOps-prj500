"""
Unit tests for 31_dataclasses_advanced program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_dataclass,
    demonstrate_default_values,
    demonstrate_post_init,
    demonstrate_frozen,
    demonstrate_ordering,
    demonstrate_field_options,
    demonstrate_init_var,
    demonstrate_class_variables,
    demonstrate_helper_functions,
    demonstrate_inheritance,
    main
)


class TestBasicDataclass:
    """Test cases for demonstrate_basic_dataclass()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_dataclass()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_dataclass()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_dataclass()
        assert len(result) > 0

class TestDefaultValues:
    """Test cases for demonstrate_default_values()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_default_values()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_default_values()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_default_values()
        assert len(result) > 0

class TestPostInit:
    """Test cases for demonstrate_post_init()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_post_init()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_post_init()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_post_init()
        assert len(result) > 0

class TestFrozen:
    """Test cases for demonstrate_frozen()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_frozen()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_frozen()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_frozen()
        assert len(result) > 0

class TestOrdering:
    """Test cases for demonstrate_ordering()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_ordering()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_ordering()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_ordering()
        assert len(result) > 0

class TestFieldOptions:
    """Test cases for demonstrate_field_options()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_field_options()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_field_options()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_field_options()
        assert len(result) > 0

class TestInitVar:
    """Test cases for demonstrate_init_var()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_init_var()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_init_var()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_init_var()
        assert len(result) > 0

class TestClassVariables:
    """Test cases for demonstrate_class_variables()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_class_variables()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_class_variables()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_class_variables()
        assert len(result) > 0

class TestHelperFunctions:
    """Test cases for demonstrate_helper_functions()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_helper_functions()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_helper_functions()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_helper_functions()
        assert len(result) > 0

class TestInheritance:
    """Test cases for demonstrate_inheritance()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_inheritance()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_inheritance()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_inheritance()
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
        assert "Program 31" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
