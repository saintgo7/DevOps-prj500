"""
Unit tests for 51_middleware program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_middleware,
    demonstrate_logging_middleware,
    demonstrate_cors_middleware,
    demonstrate_authentication_middleware,
    demonstrate_error_handling_middleware,
    demonstrate_rate_limiting_middleware,
    demonstrate_request_id_middleware,
    demonstrate_compression_middleware,
    demonstrate_middleware_order,
    main
)


class TestBasicMiddleware:
    """Test cases for demonstrate_basic_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_middleware()
        assert len(result) > 0

class TestLoggingMiddleware:
    """Test cases for demonstrate_logging_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_logging_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_logging_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_logging_middleware()
        assert len(result) > 0

class TestCorsMiddleware:
    """Test cases for demonstrate_cors_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_cors_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_cors_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_cors_middleware()
        assert len(result) > 0

class TestAuthenticationMiddleware:
    """Test cases for demonstrate_authentication_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_authentication_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_authentication_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_authentication_middleware()
        assert len(result) > 0

class TestErrorHandlingMiddleware:
    """Test cases for demonstrate_error_handling_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_error_handling_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_error_handling_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_error_handling_middleware()
        assert len(result) > 0

class TestRateLimitingMiddleware:
    """Test cases for demonstrate_rate_limiting_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_rate_limiting_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_rate_limiting_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_rate_limiting_middleware()
        assert len(result) > 0

class TestRequestIdMiddleware:
    """Test cases for demonstrate_request_id_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_request_id_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_request_id_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_request_id_middleware()
        assert len(result) > 0

class TestCompressionMiddleware:
    """Test cases for demonstrate_compression_middleware()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_compression_middleware()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_compression_middleware()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_compression_middleware()
        assert len(result) > 0

class TestMiddlewareOrder:
    """Test cases for demonstrate_middleware_order()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_middleware_order()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_middleware_order()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_middleware_order()
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
        assert "Program 51" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
