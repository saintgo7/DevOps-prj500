"""
Unit tests for 30_protocols program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_protocol,
    demonstrate_runtime_checkable,
    demonstrate_protocol_vs_abc,
    demonstrate_multiple_methods,
    demonstrate_generic_protocol,
    demonstrate_iterator_protocol,
    demonstrate_comparable_protocol,
    demonstrate_context_manager_protocol,
    demonstrate_sized_protocol,
    demonstrate_protocol_composition,
    main
)


class TestBasicProtocol:
    """Test cases for demonstrate_basic_protocol()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_protocol()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_protocol()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_protocol()
        assert len(result) > 0

class TestRuntimeCheckable:
    """Test cases for demonstrate_runtime_checkable()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_runtime_checkable()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_runtime_checkable()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_runtime_checkable()
        assert len(result) > 0

class TestProtocolVsAbc:
    """Test cases for demonstrate_protocol_vs_abc()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_protocol_vs_abc()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_protocol_vs_abc()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_protocol_vs_abc()
        assert len(result) > 0

class TestMultipleMethods:
    """Test cases for demonstrate_multiple_methods()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_multiple_methods()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_multiple_methods()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_multiple_methods()
        assert len(result) > 0

class TestGenericProtocol:
    """Test cases for demonstrate_generic_protocol()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_generic_protocol()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_generic_protocol()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_generic_protocol()
        assert len(result) > 0

class TestIteratorProtocol:
    """Test cases for demonstrate_iterator_protocol()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_iterator_protocol()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_iterator_protocol()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_iterator_protocol()
        assert len(result) > 0

class TestComparableProtocol:
    """Test cases for demonstrate_comparable_protocol()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_comparable_protocol()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_comparable_protocol()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_comparable_protocol()
        assert len(result) > 0

class TestContextManagerProtocol:
    """Test cases for demonstrate_context_manager_protocol()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_context_manager_protocol()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_context_manager_protocol()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_context_manager_protocol()
        assert len(result) > 0

class TestSizedProtocol:
    """Test cases for demonstrate_sized_protocol()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_sized_protocol()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_sized_protocol()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_sized_protocol()
        assert len(result) > 0

class TestProtocolComposition:
    """Test cases for demonstrate_protocol_composition()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_protocol_composition()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_protocol_composition()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_protocol_composition()
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
        assert "Program 30" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
