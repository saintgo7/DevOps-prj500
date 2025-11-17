"""
Unit tests for 37_testing_advanced program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_fixtures,
    demonstrate_parametrize,
    demonstrate_marks,
    demonstrate_fixtures_scope,
    demonstrate_fixture_parameters,
    demonstrate_conftest,
    demonstrate_monkeypatch,
    demonstrate_tmp_path,
    demonstrate_capsys,
    demonstrate_testing_best_practices,
    main
)


class TestFixtures:
    """Test cases for demonstrate_fixtures()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_fixtures()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_fixtures()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_fixtures()
        assert len(result) > 0

class TestParametrize:
    """Test cases for demonstrate_parametrize()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_parametrize()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_parametrize()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_parametrize()
        assert len(result) > 0

class TestMarks:
    """Test cases for demonstrate_marks()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_marks()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_marks()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_marks()
        assert len(result) > 0

class TestFixturesScope:
    """Test cases for demonstrate_fixtures_scope()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_fixtures_scope()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_fixtures_scope()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_fixtures_scope()
        assert len(result) > 0

class TestFixtureParameters:
    """Test cases for demonstrate_fixture_parameters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_fixture_parameters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_fixture_parameters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_fixture_parameters()
        assert len(result) > 0

class TestConftest:
    """Test cases for demonstrate_conftest()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_conftest()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_conftest()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_conftest()
        assert len(result) > 0

class TestMonkeypatch:
    """Test cases for demonstrate_monkeypatch()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_monkeypatch()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_monkeypatch()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_monkeypatch()
        assert len(result) > 0

class TestTmpPath:
    """Test cases for demonstrate_tmp_path()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_tmp_path()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_tmp_path()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_tmp_path()
        assert len(result) > 0

class TestCapsys:
    """Test cases for demonstrate_capsys()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_capsys()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_capsys()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_capsys()
        assert len(result) > 0

class TestTestingBestPractices:
    """Test cases for demonstrate_testing_best_practices()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_testing_best_practices()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_testing_best_practices()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_testing_best_practices()
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
        assert "Program 37" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
