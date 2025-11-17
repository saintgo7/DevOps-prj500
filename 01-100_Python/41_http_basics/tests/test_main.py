"""
Unit tests for 41_http_basics program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_http_methods,
    demonstrate_status_codes,
    demonstrate_common_headers,
    demonstrate_http_request,
    demonstrate_http_response,
    demonstrate_content_negotiation,
    main
)


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

class TestCommonHeaders:
    """Test cases for demonstrate_common_headers()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_common_headers()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_common_headers()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_common_headers()
        assert len(result) > 0

class TestHttpRequest:
    """Test cases for demonstrate_http_request()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_http_request()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_http_request()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_http_request()
        assert len(result) > 0

class TestHttpResponse:
    """Test cases for demonstrate_http_response()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_http_response()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_http_response()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_http_response()
        assert len(result) > 0

class TestContentNegotiation:
    """Test cases for demonstrate_content_negotiation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_content_negotiation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_content_negotiation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_content_negotiation()
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
        assert "Program 41" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
