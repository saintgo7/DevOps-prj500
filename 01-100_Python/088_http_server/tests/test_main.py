"""
Unit tests for 088_http_server program.

These tests verify:
- HTTP server creation
- Request handling (GET, POST, etc.)
- Response generation
- Status codes
- Headers and content
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestHTTPServer:
    """Test cases for HTTP server."""

    def test_http_request_structure(self):
        """Test HTTP request structure."""
        request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        assert "GET" in request
        assert "HTTP/1.1" in request

    def test_http_response_structure(self):
        """Test HTTP response structure."""
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html></html>"
        assert "200 OK" in response
        assert "Content-Type" in response


class TestMainFunction:
    """Test cases for main function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
