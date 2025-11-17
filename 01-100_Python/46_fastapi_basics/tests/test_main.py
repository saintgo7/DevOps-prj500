"""
Unit tests for 46_fastapi_basics program.

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
    demonstrate_path_operations,
    demonstrate_request_body,
    demonstrate_response_models,
    demonstrate_status_codes,
    demonstrate_async_operations,
    demonstrate_dependencies,
    demonstrate_documentation,
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

class TestPathOperations:
    """Test cases for demonstrate_path_operations()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_path_operations()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_path_operations()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_path_operations()
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

class TestResponseModels:
    """Test cases for demonstrate_response_models()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_response_models()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_response_models()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_response_models()
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

class TestAsyncOperations:
    """Test cases for demonstrate_async_operations()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_async_operations()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_async_operations()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_async_operations()
        assert len(result) > 0

class TestDependencies:
    """Test cases for demonstrate_dependencies()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_dependencies()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_dependencies()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_dependencies()
        assert len(result) > 0

class TestDocumentation:
    """Test cases for demonstrate_documentation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_documentation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_documentation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_documentation()
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
        assert "Program 46" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
