"""
Unit tests for 57_graphql_basics program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_graphql_vs_rest,
    demonstrate_schema_definition,
    demonstrate_queries,
    demonstrate_mutations,
    demonstrate_python_graphql,
    demonstrate_graphql_patterns,
    main
)


class TestGraphqlVsRest:
    """Test cases for demonstrate_graphql_vs_rest()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_graphql_vs_rest()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_graphql_vs_rest()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_graphql_vs_rest()
        assert len(result) > 0

class TestSchemaDefinition:
    """Test cases for demonstrate_schema_definition()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_schema_definition()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_schema_definition()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_schema_definition()
        assert len(result) > 0

class TestQueries:
    """Test cases for demonstrate_queries()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_queries()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_queries()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_queries()
        assert len(result) > 0

class TestMutations:
    """Test cases for demonstrate_mutations()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_mutations()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_mutations()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_mutations()
        assert len(result) > 0

class TestPythonGraphql:
    """Test cases for demonstrate_python_graphql()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_python_graphql()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_python_graphql()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_python_graphql()
        assert len(result) > 0

class TestGraphqlPatterns:
    """Test cases for demonstrate_graphql_patterns()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_graphql_patterns()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_graphql_patterns()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_graphql_patterns()
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
        assert "Program 57" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
