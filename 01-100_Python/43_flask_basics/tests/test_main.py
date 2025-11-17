"""
Unit tests for 43_flask_basics program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_app,
    demonstrate_routes,
    demonstrate_request_methods,
    demonstrate_request_object,
    demonstrate_response_object,
    demonstrate_json_api,
    demonstrate_error_handling,
    demonstrate_application_context,
    main
)


class TestBasicApp:
    """Test cases for demonstrate_basic_app()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_app()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_app()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_app()
        assert len(result) > 0

class TestRoutes:
    """Test cases for demonstrate_routes()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_routes()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_routes()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_routes()
        assert len(result) > 0

class TestRequestMethods:
    """Test cases for demonstrate_request_methods()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_request_methods()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_request_methods()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_request_methods()
        assert len(result) > 0

class TestRequestObject:
    """Test cases for demonstrate_request_object()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_request_object()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_request_object()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_request_object()
        assert len(result) > 0

class TestResponseObject:
    """Test cases for demonstrate_response_object()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_response_object()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_response_object()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_response_object()
        assert len(result) > 0

class TestJsonApi:
    """Test cases for demonstrate_json_api()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_json_api()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_json_api()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_json_api()
        assert len(result) > 0

class TestErrorHandling:
    """Test cases for demonstrate_error_handling()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_error_handling()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_error_handling()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_error_handling()
        assert len(result) > 0

class TestApplicationContext:
    """Test cases for demonstrate_application_context()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_application_context()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_application_context()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_application_context()
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
        assert "Program 43" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
