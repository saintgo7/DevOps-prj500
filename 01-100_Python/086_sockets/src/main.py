#!/usr/bin/env python3
"""
Program 86: Socket Programming
Demonstrates socket programming basics, client/server communication.
"""

import socket
import threading
import time
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class SocketInfo:
    """Store socket information."""
    family: str
    type: str
    protocol: int
    local_address: Optional[Tuple[str, int]]
    remote_address: Optional[Tuple[str, int]]


def demonstrate_socket_basics() -> None:
    """Demonstrate basic socket concepts."""
    print("\n" + "=" * 60)
    print("SOCKET BASICS")
    print("=" * 60)

    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("\n1. Socket creation:")
    print(f"   Family: AF_INET (IPv4)")
    print(f"   Type: SOCK_STREAM (TCP)")
    print(f"   File descriptor: {sock.fileno()}")

    print("\n2. Socket families:")
    print(f"   AF_INET: IPv4 = {socket.AF_INET}")
    print(f"   AF_INET6: IPv6 = {socket.AF_INET6}")
    print(f"   AF_UNIX: Unix domain = {socket.AF_UNIX}")

    print("\n3. Socket types:")
    print(f"   SOCK_STREAM: TCP = {socket.SOCK_STREAM}")
    print(f"   SOCK_DGRAM: UDP = {socket.SOCK_DGRAM}")

    sock.close()
    print("\n4. Socket closed")


def demonstrate_hostname_resolution() -> None:
    """Demonstrate hostname and IP resolution."""
    print("\n" + "=" * 60)
    print("HOSTNAME RESOLUTION")
    print("=" * 60)

    # Get hostname
    hostname = socket.gethostname()
    print(f"\n1. Local hostname: {hostname}")

    # Get IP address
    try:
        ip = socket.gethostbyname(hostname)
        print(f"   IP address: {ip}")
    except socket.gaierror:
        print("   Could not resolve hostname")

    # Resolve external hostname
    print("\n2. Resolving external hostname:")
    try:
        ip = socket.gethostbyname('localhost')
        print(f"   localhost -> {ip}")
    except socket.gaierror as e:
        print(f"   Error: {e}")

    # Get FQDN
    fqdn = socket.getfqdn()
    print(f"\n3. Fully qualified domain name: {fqdn}")

    # Get address info
    print("\n4. Address info for localhost:")
    try:
        addr_info = socket.getaddrinfo('localhost', 8000, socket.AF_INET, socket.SOCK_STREAM)
        for info in addr_info[:3]:
            print(f"   {info[4]}")
    except socket.gaierror as e:
        print(f"   Error: {e}")


def run_echo_server(host: str, port: int, stop_event: threading.Event) -> None:
    """Simple echo server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # Set socket options
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.settimeout(1.0)  # Timeout for accept

        # Bind and listen
        server_sock.bind((host, port))
        server_sock.listen(1)
        print(f"[Server] Listening on {host}:{port}")

        while not stop_event.is_set():
            try:
                # Accept connection
                client_sock, client_addr = server_sock.accept()
                print(f"[Server] Connection from {client_addr}")

                with client_sock:
                    # Receive data
                    data = client_sock.recv(1024)
                    if data:
                        message = data.decode('utf-8')
                        print(f"[Server] Received: {message}")

                        # Echo back
                        client_sock.sendall(data)
                        print(f"[Server] Echoed back")

                break  # Exit after one connection for demo

            except socket.timeout:
                continue
            except Exception as e:
                print(f"[Server] Error: {e}")
                break


def run_echo_client(host: str, port: int, message: str) -> None:
    """Simple echo client."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
            # Connect to server
            client_sock.connect((host, port))
            print(f"[Client] Connected to {host}:{port}")

            # Send data
            client_sock.sendall(message.encode('utf-8'))
            print(f"[Client] Sent: {message}")

            # Receive echo
            data = client_sock.recv(1024)
            echo = data.decode('utf-8')
            print(f"[Client] Received echo: {echo}")

    except ConnectionRefusedError:
        print("[Client] Connection refused")
    except Exception as e:
        print(f"[Client] Error: {e}")


def demonstrate_client_server() -> None:
    """Demonstrate simple client-server communication."""
    print("\n" + "=" * 60)
    print("CLIENT-SERVER COMMUNICATION")
    print("=" * 60)

    host = '127.0.0.1'
    port = 9999
    stop_event = threading.Event()

    print("\n1. Starting echo server in background...")

    # Start server in thread
    server_thread = threading.Thread(
        target=run_echo_server,
        args=(host, port, stop_event),
        daemon=True
    )
    server_thread.start()
    time.sleep(0.5)  # Give server time to start

    print("\n2. Connecting client...")
    run_echo_client(host, port, "Hello, Socket!")

    # Cleanup
    stop_event.set()
    server_thread.join(timeout=2)
    print("\n3. Server stopped")


def demonstrate_socket_options() -> None:
    """Demonstrate socket options."""
    print("\n" + "=" * 60)
    print("SOCKET OPTIONS")
    print("=" * 60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("\n1. Setting socket options:")

    # SO_REUSEADDR
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    reuse = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print(f"   SO_REUSEADDR: {reuse}")

    # SO_KEEPALIVE
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    keepalive = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    print(f"   SO_KEEPALIVE: {keepalive}")

    # Socket timeout
    sock.settimeout(5.0)
    timeout = sock.gettimeout()
    print(f"   Timeout: {timeout}s")

    # Blocking mode
    sock.setblocking(True)
    print(f"   Blocking mode: True")

    sock.close()


def demonstrate_non_blocking() -> None:
    """Demonstrate non-blocking sockets."""
    print("\n" + "=" * 60)
    print("NON-BLOCKING SOCKETS")
    print("=" * 60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("\n1. Setting non-blocking mode:")
    sock.setblocking(False)
    print("   Socket is now non-blocking")

    # Try to connect (will raise exception immediately if not ready)
    try:
        sock.connect(('127.0.0.1', 9999))
    except BlockingIOError:
        print("2. BlockingIOError raised (expected for non-blocking)")

    sock.close()


def demonstrate_socket_info() -> None:
    """Demonstrate getting socket information."""
    print("\n" + "=" * 60)
    print("SOCKET INFORMATION")
    print("=" * 60)

    # Create and bind socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 0))  # Bind to any available port

    print("\n1. Socket properties:")
    print(f"   Family: {sock.family}")
    print(f"   Type: {sock.type}")
    print(f"   Protocol: {sock.proto}")

    # Get bound address
    local_addr = sock.getsockname()
    print(f"\n2. Local address: {local_addr[0]}:{local_addr[1]}")

    sock.close()


def demonstrate_udp_socket() -> None:
    """Demonstrate UDP socket basics."""
    print("\n" + "=" * 60)
    print("UDP SOCKET BASICS")
    print("=" * 60)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("\n1. UDP socket created:")
    print(f"   Type: SOCK_DGRAM (UDP)")

    # Bind to address
    sock.bind(('127.0.0.1', 0))
    addr = sock.getsockname()
    print(f"   Bound to: {addr[0]}:{addr[1]}")

    print("\n2. UDP characteristics:")
    print("   - Connectionless")
    print("   - No guaranteed delivery")
    print("   - No order guarantee")
    print("   - Lower overhead than TCP")

    sock.close()


def demonstrate_socket_errors() -> None:
    """Demonstrate common socket errors."""
    print("\n" + "=" * 60)
    print("SOCKET ERROR HANDLING")
    print("=" * 60)

    print("\n1. Connection refused:")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect(('127.0.0.1', 9998))
    except ConnectionRefusedError:
        print("   ✓ Caught ConnectionRefusedError")
    finally:
        sock.close()

    print("\n2. Timeout error:")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        sock.connect(('10.255.255.1', 9999))
    except socket.timeout:
        print("   ✓ Caught socket.timeout")
    except OSError as e:
        print(f"   ✓ Caught OSError: {e}")
    finally:
        sock.close()

    print("\n3. Address already in use:")
    print("   (Prevented by SO_REUSEADDR)")


def demonstrate_socket_shutdown() -> None:
    """Demonstrate socket shutdown."""
    print("\n" + "=" * 60)
    print("SOCKET SHUTDOWN")
    print("=" * 60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 0))

    print("\n1. Shutdown methods:")
    print("   SHUT_RD: No more receives")
    print("   SHUT_WR: No more sends")
    print("   SHUT_RDWR: No more I/O")

    print("\n2. Socket lifecycle:")
    print("   create -> bind -> listen -> accept -> send/recv -> shutdown -> close")

    sock.close()


def demonstrate_socket_context_manager() -> None:
    """Demonstrate socket with context manager."""
    print("\n" + "=" * 60)
    print("SOCKET CONTEXT MANAGER")
    print("=" * 60)

    print("\n1. Using context manager (recommended):")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', 0))
        addr = sock.getsockname()
        print(f"   Socket created and bound to {addr[1]}")
    print("   Socket automatically closed")


def demonstrate_socket_pairs() -> None:
    """Demonstrate socket pairs for IPC."""
    print("\n" + "=" * 60)
    print("SOCKET PAIRS (IPC)")
    print("=" * 60)

    try:
        # Create connected socket pair
        sock1, sock2 = socket.socketpair()

        print("\n1. Created socket pair:")
        print("   Two connected sockets for IPC")

        # Send data through pair
        message = b"Hello through socket pair"
        sock1.send(message)
        print(f"\n2. Sent: {message.decode()}")

        received = sock2.recv(1024)
        print(f"3. Received: {received.decode()}")

        sock1.close()
        sock2.close()

    except AttributeError:
        print("\n1. socketpair() not available on this platform")


def demonstrate_best_practices() -> None:
    """Demonstrate socket programming best practices."""
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)

    print("\n1. Always use context managers:")
    print("   with socket.socket() as sock:")
    print("       # socket auto-closes")

    print("\n2. Set SO_REUSEADDR for servers:")
    print("   sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)")

    print("\n3. Use timeouts to prevent hanging:")
    print("   sock.settimeout(5.0)")

    print("\n4. Handle all socket exceptions:")
    print("   - ConnectionRefusedError")
    print("   - socket.timeout")
    print("   - OSError")

    print("\n5. Close sockets properly:")
    print("   sock.shutdown(socket.SHUT_RDWR)")
    print("   sock.close()")


def main() -> None:
    """Main function demonstrating socket programming."""
    print("=" * 60)
    print("PYTHON SOCKET PROGRAMMING")
    print("=" * 60)

    demonstrate_socket_basics()
    demonstrate_hostname_resolution()
    demonstrate_client_server()
    demonstrate_socket_options()
    demonstrate_non_blocking()
    demonstrate_socket_info()
    demonstrate_udp_socket()
    demonstrate_socket_errors()
    demonstrate_socket_shutdown()
    demonstrate_socket_context_manager()
    demonstrate_socket_pairs()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All socket programming demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
