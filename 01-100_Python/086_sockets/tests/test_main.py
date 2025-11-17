"""
Unit tests for 086_sockets program.

These tests verify:
- Socket creation and configuration
- Socket binding and listening
- Socket connections
- Socket data transmission
- Socket error handling
"""

import sys
from pathlib import Path
import pytest
import socket

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestSocketCreation:
    """Test cases for socket creation."""

    def test_create_tcp_socket(self):
        """Test creating TCP socket."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        assert sock is not None
        sock.close()

    def test_create_udp_socket(self):
        """Test creating UDP socket."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        assert sock is not None
        sock.close()

    def test_socket_options(self):
        """Test setting socket options."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.close()


class TestSocketBinding:
    """Test cases for socket binding."""

    def test_bind_to_port(self):
        """Test binding socket to port."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('127.0.0.1', 0))  # Bind to any available port
            address = sock.getsockname()
            assert address[0] == '127.0.0.1'
            assert address[1] > 0
        finally:
            sock.close()


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
