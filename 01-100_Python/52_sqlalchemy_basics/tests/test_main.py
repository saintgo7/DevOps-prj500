"""
Unit tests for 52_sqlalchemy_basics program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_engine_creation,
    demonstrate_declarative_base,
    demonstrate_session_management,
    demonstrate_basic_queries,
    demonstrate_crud_operations,
    demonstrate_raw_sql,
    demonstrate_transactions,
    main
)


class TestEngineCreation:
    """Test cases for demonstrate_engine_creation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_engine_creation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_engine_creation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_engine_creation()
        assert len(result) > 0

class TestDeclarativeBase:
    """Test cases for demonstrate_declarative_base()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_declarative_base()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_declarative_base()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_declarative_base()
        assert len(result) > 0

class TestSessionManagement:
    """Test cases for demonstrate_session_management()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_session_management()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_session_management()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_session_management()
        assert len(result) > 0

class TestBasicQueries:
    """Test cases for demonstrate_basic_queries()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_queries()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_queries()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_queries()
        assert len(result) > 0

class TestCrudOperations:
    """Test cases for demonstrate_crud_operations()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_crud_operations()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_crud_operations()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_crud_operations()
        assert len(result) > 0

class TestRawSql:
    """Test cases for demonstrate_raw_sql()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_raw_sql()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_raw_sql()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_raw_sql()
        assert len(result) > 0

class TestTransactions:
    """Test cases for demonstrate_transactions()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_transactions()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_transactions()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_transactions()
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
        assert "Program 52" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
