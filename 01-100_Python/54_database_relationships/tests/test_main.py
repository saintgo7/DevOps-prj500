"""
Unit tests for 54_database_relationships program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_one_to_many,
    demonstrate_many_to_many,
    demonstrate_one_to_one,
    demonstrate_relationship_configuration,
    demonstrate_joins,
    demonstrate_complex_relationships,
    demonstrate_relationship_loading_strategies,
    main
)


class TestOneToMany:
    """Test cases for demonstrate_one_to_many()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_one_to_many()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_one_to_many()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_one_to_many()
        assert len(result) > 0

class TestManyToMany:
    """Test cases for demonstrate_many_to_many()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_many_to_many()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_many_to_many()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_many_to_many()
        assert len(result) > 0

class TestOneToOne:
    """Test cases for demonstrate_one_to_one()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_one_to_one()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_one_to_one()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_one_to_one()
        assert len(result) > 0

class TestRelationshipConfiguration:
    """Test cases for demonstrate_relationship_configuration()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_relationship_configuration()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_relationship_configuration()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_relationship_configuration()
        assert len(result) > 0

class TestJoins:
    """Test cases for demonstrate_joins()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_joins()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_joins()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_joins()
        assert len(result) > 0

class TestComplexRelationships:
    """Test cases for demonstrate_complex_relationships()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_complex_relationships()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_complex_relationships()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_complex_relationships()
        assert len(result) > 0

class TestRelationshipLoadingStrategies:
    """Test cases for demonstrate_relationship_loading_strategies()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_relationship_loading_strategies()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_relationship_loading_strategies()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_relationship_loading_strategies()
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
        assert "Program 54" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
