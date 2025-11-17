"""
Unit tests for 60_api_documentation program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_openapi_basics,
    demonstrate_schema_documentation,
    demonstrate_endpoint_documentation,
    demonstrate_response_models,
    demonstrate_custom_docs,
    demonstrate_advanced_documentation,
    main
)


class TestOpenapiBasics:
    """Test cases for demonstrate_openapi_basics()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_openapi_basics()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_openapi_basics()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_openapi_basics()
        assert len(result) > 0

class TestSchemaDocumentation:
    """Test cases for demonstrate_schema_documentation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_schema_documentation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_schema_documentation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_schema_documentation()
        assert len(result) > 0

class TestEndpointDocumentation:
    """Test cases for demonstrate_endpoint_documentation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_endpoint_documentation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_endpoint_documentation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_endpoint_documentation()
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

class TestCustomDocs:
    """Test cases for demonstrate_custom_docs()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_custom_docs()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_custom_docs()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_custom_docs()
        assert len(result) > 0

class TestAdvancedDocumentation:
    """Test cases for demonstrate_advanced_documentation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_advanced_documentation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_advanced_documentation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_advanced_documentation()
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
        assert "Program 60" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
