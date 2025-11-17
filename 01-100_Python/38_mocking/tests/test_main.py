"""
Unit tests for 38_mocking program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_mock,
    demonstrate_magic_mock,
    demonstrate_return_value_side_effect,
    demonstrate_assert_methods,
    demonstrate_call_tracking,
    demonstrate_patch_decorator,
    demonstrate_patch_multiple,
    demonstrate_spec_autospec,
    demonstrate_property_mock,
    demonstrate_practical_mocking,
    main
)


class TestBasicMock:
    """Test cases for demonstrate_basic_mock()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_mock()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_mock()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_mock()
        assert len(result) > 0

class TestMagicMock:
    """Test cases for demonstrate_magic_mock()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_magic_mock()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_magic_mock()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_magic_mock()
        assert len(result) > 0

class TestReturnValueSideEffect:
    """Test cases for demonstrate_return_value_side_effect()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_return_value_side_effect()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_return_value_side_effect()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_return_value_side_effect()
        assert len(result) > 0

class TestAssertMethods:
    """Test cases for demonstrate_assert_methods()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_assert_methods()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_assert_methods()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_assert_methods()
        assert len(result) > 0

class TestCallTracking:
    """Test cases for demonstrate_call_tracking()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_call_tracking()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_call_tracking()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_call_tracking()
        assert len(result) > 0

class TestPatchDecorator:
    """Test cases for demonstrate_patch_decorator()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_patch_decorator()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_patch_decorator()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_patch_decorator()
        assert len(result) > 0

class TestPatchMultiple:
    """Test cases for demonstrate_patch_multiple()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_patch_multiple()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_patch_multiple()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_patch_multiple()
        assert len(result) > 0

class TestSpecAutospec:
    """Test cases for demonstrate_spec_autospec()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_spec_autospec()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_spec_autospec()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_spec_autospec()
        assert len(result) > 0

class TestPropertyMock:
    """Test cases for demonstrate_property_mock()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_property_mock()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_property_mock()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_property_mock()
        assert len(result) > 0

class TestPracticalMocking:
    """Test cases for demonstrate_practical_mocking()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_practical_mocking()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_practical_mocking()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_practical_mocking()
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
        assert "Program 38" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
