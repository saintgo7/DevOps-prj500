"""
Unit tests for 55_api_design program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_rest_principles,
    demonstrate_resource_naming,
    demonstrate_http_methods,
    demonstrate_status_codes,
    demonstrate_versioning,
    demonstrate_pagination,
    demonstrate_error_responses,
    main
)


class TestRestPrinciples:
    """Test cases for demonstrate_rest_principles()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_rest_principles()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_rest_principles()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_rest_principles()
        assert len(result) > 0

class TestResourceNaming:
    """Test cases for demonstrate_resource_naming()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_resource_naming()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_resource_naming()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_resource_naming()
        assert len(result) > 0

class TestHttpMethods:
    """Test cases for demonstrate_http_methods()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_http_methods()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_http_methods()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_http_methods()
        assert len(result) > 0

class TestStatusCodes:
    """Test cases for demonstrate_status_codes()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_status_codes()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_status_codes()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_status_codes()
        assert len(result) > 0

class TestVersioning:
    """Test cases for demonstrate_versioning()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_versioning()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_versioning()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_versioning()
        assert len(result) > 0

class TestPagination:
    """Test cases for demonstrate_pagination()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_pagination()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_pagination()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_pagination()
        assert len(result) > 0

class TestErrorResponses:
    """Test cases for demonstrate_error_responses()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_error_responses()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_error_responses()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_error_responses()
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
        assert "Program 55" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
