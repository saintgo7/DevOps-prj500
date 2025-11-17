"""
Unit tests for 47_fastapi_routing program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_path_parameters,
    demonstrate_query_parameters,
    demonstrate_request_body,
    demonstrate_field_validation,
    demonstrate_form_data,
    demonstrate_api_router,
    demonstrate_dependencies_in_routing,
    main
)


class TestPathParameters:
    """Test cases for demonstrate_path_parameters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_path_parameters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_path_parameters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_path_parameters()
        assert len(result) > 0

class TestQueryParameters:
    """Test cases for demonstrate_query_parameters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_query_parameters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_query_parameters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_query_parameters()
        assert len(result) > 0

class TestRequestBody:
    """Test cases for demonstrate_request_body()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_request_body()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_request_body()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_request_body()
        assert len(result) > 0

class TestFieldValidation:
    """Test cases for demonstrate_field_validation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_field_validation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_field_validation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_field_validation()
        assert len(result) > 0

class TestFormData:
    """Test cases for demonstrate_form_data()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_form_data()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_form_data()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_form_data()
        assert len(result) > 0

class TestApiRouter:
    """Test cases for demonstrate_api_router()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_api_router()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_api_router()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_api_router()
        assert len(result) > 0

class TestDependenciesInRouting:
    """Test cases for demonstrate_dependencies_in_routing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_dependencies_in_routing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_dependencies_in_routing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_dependencies_in_routing()
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
        assert "Program 47" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
