"""
Unit tests for 29_type_hints program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_types,
    demonstrate_collection_types,
    demonstrate_optional_union,
    demonstrate_callable_types,
    demonstrate_type_variables,
    demonstrate_generic_classes,
    demonstrate_protocols,
    demonstrate_literal_types,
    demonstrate_final,
    demonstrate_advanced_patterns,
    main
)


class TestBasicTypes:
    """Test cases for demonstrate_basic_types()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_types()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_types()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_types()
        assert len(result) > 0

class TestCollectionTypes:
    """Test cases for demonstrate_collection_types()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_collection_types()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_collection_types()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_collection_types()
        assert len(result) > 0

class TestOptionalUnion:
    """Test cases for demonstrate_optional_union()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_optional_union()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_optional_union()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_optional_union()
        assert len(result) > 0

class TestCallableTypes:
    """Test cases for demonstrate_callable_types()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_callable_types()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_callable_types()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_callable_types()
        assert len(result) > 0

class TestTypeVariables:
    """Test cases for demonstrate_type_variables()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_type_variables()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_type_variables()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_type_variables()
        assert len(result) > 0

class TestGenericClasses:
    """Test cases for demonstrate_generic_classes()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_generic_classes()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_generic_classes()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_generic_classes()
        assert len(result) > 0

class TestProtocols:
    """Test cases for demonstrate_protocols()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_protocols()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_protocols()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_protocols()
        assert len(result) > 0

class TestLiteralTypes:
    """Test cases for demonstrate_literal_types()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_literal_types()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_literal_types()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_literal_types()
        assert len(result) > 0

class TestFinal:
    """Test cases for demonstrate_final()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_final()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_final()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_final()
        assert len(result) > 0

class TestAdvancedPatterns:
    """Test cases for demonstrate_advanced_patterns()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_advanced_patterns()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_advanced_patterns()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_advanced_patterns()
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
        assert "Program 29" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
