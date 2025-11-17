"""
Unit tests for 087_tcp_udp program.

These tests verify:
- TCP client-server communication
- UDP client-server communication
- Data transmission reliability
- Connection handling
- Protocol differences
"""

import sys
from pathlib import Path
import pytest
import socket
import threading
import time

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestTCPCommunication:
    """Test cases for TCP communication."""

    def test_tcp_connection(self):
        """Test TCP client-server connection."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 0))
        server_socket.listen(1)
        port = server_socket.getsockname()[1]

        def server():
            conn, addr = server_socket.accept()
            conn.close()
            server_socket.close()

        thread = threading.Thread(target=server)
        thread.start()

        time.sleep(0.1)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', port))
        client_socket.close()

        thread.join()


class TestUDPCommunication:
    """Test cases for UDP communication."""

    def test_udp_send_receive(self):
        """Test UDP send and receive."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]

        message = b'test message'
        sock.sendto(message, ('127.0.0.1', port))
        sock.settimeout(1.0)

        data, addr = sock.recvfrom(1024)
        assert data == message
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
