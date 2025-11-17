"""
Unit tests for 44_flask_routing program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_url_parameters,
    demonstrate_query_strings,
    demonstrate_custom_converters,
    demonstrate_http_methods,
    demonstrate_url_building,
    demonstrate_blueprints,
    demonstrate_route_decorators,
    main
)


class TestUrlParameters:
    """Test cases for demonstrate_url_parameters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_url_parameters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_url_parameters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_url_parameters()
        assert len(result) > 0

class TestQueryStrings:
    """Test cases for demonstrate_query_strings()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_query_strings()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_query_strings()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_query_strings()
        assert len(result) > 0

class TestCustomConverters:
    """Test cases for demonstrate_custom_converters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_custom_converters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_custom_converters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_custom_converters()
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

class TestUrlBuilding:
    """Test cases for demonstrate_url_building()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_url_building()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_url_building()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_url_building()
        assert len(result) > 0

class TestBlueprints:
    """Test cases for demonstrate_blueprints()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_blueprints()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_blueprints()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_blueprints()
        assert len(result) > 0

class TestRouteDecorators:
    """Test cases for demonstrate_route_decorators()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_route_decorators()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_route_decorators()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_route_decorators()
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
        assert "Program 44" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
