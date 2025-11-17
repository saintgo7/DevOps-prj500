#!/usr/bin/env python3
"""
Program 87: TCP/UDP Protocols
Demonstrates TCP and UDP protocols with practical examples.
"""

import socket
import threading
import time
from typing import Tuple
from dataclasses import dataclass


@dataclass
class MessageStats:
    """Store message statistics."""
    sent: int = 0
    received: int = 0
    errors: int = 0


def demonstrate_tcp_vs_udp() -> None:
    """Demonstrate differences between TCP and UDP."""
    print("\n" + "=" * 60)
    print("TCP vs UDP")
    print("=" * 60)

    print("\n1. TCP (Transmission Control Protocol):")
    print("   ✓ Connection-oriented")
    print("   ✓ Reliable delivery")
    print("   ✓ Ordered data")
    print("   ✓ Error checking")
    print("   ✓ Flow control")
    print("   - Higher overhead")

    print("\n2. UDP (User Datagram Protocol):")
    print("   ✓ Connectionless")
    print("   ✓ Fast")
    print("   ✓ Low overhead")
    print("   - No delivery guarantee")
    print("   - No order guarantee")
    print("   - No error recovery")

    print("\n3. Use cases:")
    print("   TCP: Web, Email, File transfer")
    print("   UDP: Video streaming, Gaming, DNS")


def tcp_server(host: str, port: int, stop_event: threading.Event) -> None:
    """TCP server implementation."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.settimeout(1.0)
        server_sock.bind((host, port))
        server_sock.listen(5)

        print(f"[TCP Server] Listening on {host}:{port}")

        while not stop_event.is_set():
            try:
                client_sock, addr = server_sock.accept()
                print(f"[TCP Server] Connection from {addr}")

                with client_sock:
                    data = client_sock.recv(1024)
                    if data:
                        message = data.decode('utf-8')
                        print(f"[TCP Server] Received: {message}")

                        # Send response
                        response = f"TCP Echo: {message}"
                        client_sock.sendall(response.encode('utf-8'))

                break  # Exit after one connection for demo

            except socket.timeout:
                continue
            except Exception as e:
                print(f"[TCP Server] Error: {e}")
                break


def tcp_client(host: str, port: int, message: str) -> None:
    """TCP client implementation."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            sock.connect((host, port))
            print(f"[TCP Client] Connected to {host}:{port}")

            # Send data
            sock.sendall(message.encode('utf-8'))
            print(f"[TCP Client] Sent: {message}")

            # Receive response
            data = sock.recv(1024)
            response = data.decode('utf-8')
            print(f"[TCP Client] Received: {response}")

    except Exception as e:
        print(f"[TCP Client] Error: {e}")


def demonstrate_tcp_communication() -> None:
    """Demonstrate TCP communication."""
    print("\n" + "=" * 60)
    print("TCP COMMUNICATION")
    print("=" * 60)

    host = '127.0.0.1'
    port = 10001
    stop_event = threading.Event()

    print("\n1. Starting TCP server...")
    server_thread = threading.Thread(
        target=tcp_server,
        args=(host, port, stop_event),
        daemon=True
    )
    server_thread.start()
    time.sleep(0.5)

    print("\n2. Connecting TCP client...")
    tcp_client(host, port, "Hello TCP!")

    stop_event.set()
    server_thread.join(timeout=2)
    print("\n3. TCP communication completed")


def udp_server(host: str, port: int, stop_event: threading.Event) -> None:
    """UDP server implementation."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.settimeout(1.0)
        server_sock.bind((host, port))

        print(f"[UDP Server] Listening on {host}:{port}")

        while not stop_event.is_set():
            try:
                data, addr = server_sock.recvfrom(1024)
                message = data.decode('utf-8')
                print(f"[UDP Server] Received from {addr}: {message}")

                # Send response
                response = f"UDP Echo: {message}"
                server_sock.sendto(response.encode('utf-8'), addr)

                break  # Exit after one message for demo

            except socket.timeout:
                continue
            except Exception as e:
                print(f"[UDP Server] Error: {e}")
                break


def udp_client(host: str, port: int, message: str) -> None:
    """UDP client implementation."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2.0)

            # Send data (no connection needed)
            sock.sendto(message.encode('utf-8'), (host, port))
            print(f"[UDP Client] Sent to {host}:{port}: {message}")

            # Receive response
            data, addr = sock.recvfrom(1024)
            response = data.decode('utf-8')
            print(f"[UDP Client] Received from {addr}: {response}")

    except Exception as e:
        print(f"[UDP Client] Error: {e}")


def demonstrate_udp_communication() -> None:
    """Demonstrate UDP communication."""
    print("\n" + "=" * 60)
    print("UDP COMMUNICATION")
    print("=" * 60)

    host = '127.0.0.1'
    port = 10002
    stop_event = threading.Event()

    print("\n1. Starting UDP server...")
    server_thread = threading.Thread(
        target=udp_server,
        args=(host, port, stop_event),
        daemon=True
    )
    server_thread.start()
    time.sleep(0.5)

    print("\n2. Sending UDP message...")
    udp_client(host, port, "Hello UDP!")

    stop_event.set()
    server_thread.join(timeout=2)
    print("\n3. UDP communication completed")


def demonstrate_tcp_features() -> None:
    """Demonstrate TCP-specific features."""
    print("\n" + "=" * 60)
    print("TCP FEATURES")
    print("=" * 60)

    print("\n1. Three-way handshake:")
    print("   Client -> SYN -> Server")
    print("   Server -> SYN-ACK -> Client")
    print("   Client -> ACK -> Server")

    print("\n2. Connection state:")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)

    addr = sock.getsockname()
    print(f"   Listening on port {addr[1]}")
    print("   State: LISTEN")

    sock.close()

    print("\n3. Flow control:")
    print("   - TCP uses sliding window")
    print("   - Prevents overwhelming receiver")
    print("   - Dynamic window sizing")


def demonstrate_udp_features() -> None:
    """Demonstrate UDP-specific features."""
    print("\n" + "=" * 60)
    print("UDP FEATURES")
    print("=" * 60)

    print("\n1. Connectionless:")
    print("   - No handshake")
    print("   - No state maintained")
    print("   - Each packet independent")

    print("\n2. Packet structure:")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('127.0.0.1', 0))
        addr = sock.getsockname()
        print(f"   Bound to port {addr[1]}")
        print("   - Source port: 2 bytes")
        print("   - Dest port: 2 bytes")
        print("   - Length: 2 bytes")
        print("   - Checksum: 2 bytes")

    print("\n3. Broadcasting:")
    print("   - UDP supports broadcast")
    print("   - TCP does not")
    print("   - Useful for discovery")


def demonstrate_tcp_streaming() -> None:
    """Demonstrate TCP data streaming."""
    print("\n" + "=" * 60)
    print("TCP DATA STREAMING")
    print("=" * 60)

    print("\n1. TCP provides byte stream:")
    print("   - No message boundaries")
    print("   - Data arrives as stream")
    print("   - Application must delimit")

    print("\n2. Handling strategies:")
    print("   - Fixed-length messages")
    print("   - Delimiter-based (e.g., \\n)")
    print("   - Length-prefixed")

    print("\n3. Example: Length-prefixed")
    message = b"Hello, World!"
    length = len(message).to_bytes(4, 'big')
    packet = length + message
    print(f"   Length: {len(message)} bytes")
    print(f"   Packet: {len(packet)} bytes")


def demonstrate_udp_datagrams() -> None:
    """Demonstrate UDP datagram handling."""
    print("\n" + "=" * 60)
    print("UDP DATAGRAMS")
    print("=" * 60)

    print("\n1. Message boundaries:")
    print("   - Each send = one datagram")
    print("   - Each recv = one datagram")
    print("   - Boundaries preserved")

    print("\n2. Maximum size:")
    print("   - Theoretical: 65,507 bytes")
    print("   - Practical: 512-8192 bytes")
    print("   - MTU considerations")

    print("\n3. Fragmentation:")
    print("   - Large datagrams fragmented")
    print("   - By IP layer")
    print("   - Can cause packet loss")


def demonstrate_performance_comparison() -> None:
    """Demonstrate performance characteristics."""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)

    print("\n1. Latency:")
    print("   TCP: Higher (connection setup)")
    print("   UDP: Lower (no setup)")

    print("\n2. Throughput:")
    print("   TCP: Higher (flow control)")
    print("   UDP: Variable (no control)")

    print("\n3. Overhead:")
    print("   TCP header: 20-60 bytes")
    print("   UDP header: 8 bytes")

    print("\n4. CPU usage:")
    print("   TCP: Higher (more processing)")
    print("   UDP: Lower (minimal processing)")


def demonstrate_error_handling() -> None:
    """Demonstrate error handling for both protocols."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)

    print("\n1. TCP errors:")
    print("   - Connection refused")
    print("   - Connection reset")
    print("   - Connection timeout")
    print("   - Broken pipe")

    print("\n2. UDP errors:")
    print("   - Port unreachable (ICMP)")
    print("   - Network unreachable")
    print("   - No errors for lost packets")

    print("\n3. Handling strategies:")

    # TCP example
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        sock.connect(('127.0.0.1', 9999))
    except (ConnectionRefusedError, socket.timeout) as e:
        print(f"   ✓ TCP: Caught {type(e).__name__}")
    finally:
        sock.close()

    # UDP example
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.1)
        sock.sendto(b"test", ('127.0.0.1', 9999))
        sock.recvfrom(1024)
    except socket.timeout:
        print("   ✓ UDP: Timeout (no response)")
    finally:
        sock.close()


def demonstrate_use_cases() -> None:
    """Demonstrate appropriate use cases."""
    print("\n" + "=" * 60)
    print("USE CASES")
    print("=" * 60)

    print("\n1. Choose TCP for:")
    print("   ✓ File transfers")
    print("   ✓ Email (SMTP, IMAP)")
    print("   ✓ Web (HTTP/HTTPS)")
    print("   ✓ SSH/Remote login")
    print("   ✓ Database connections")

    print("\n2. Choose UDP for:")
    print("   ✓ Video/Audio streaming")
    print("   ✓ Online gaming")
    print("   ✓ DNS queries")
    print("   ✓ VoIP")
    print("   ✓ IoT sensor data")

    print("\n3. Decision factors:")
    print("   - Reliability required?")
    print("   - Order important?")
    print("   - Latency critical?")
    print("   - Bandwidth constrained?")


def demonstrate_socket_buffer_sizes() -> None:
    """Demonstrate socket buffer configuration."""
    print("\n" + "=" * 60)
    print("SOCKET BUFFERS")
    print("=" * 60)

    # TCP socket
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("\n1. TCP socket buffers:")

    # Get default buffer sizes
    send_buf = tcp_sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    recv_buf = tcp_sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(f"   Send buffer: {send_buf} bytes")
    print(f"   Recv buffer: {recv_buf} bytes")

    # Set custom buffer sizes
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    print("   Set to 64 KB")

    tcp_sock.close()

    # UDP socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("\n2. UDP socket buffers:")

    send_buf = udp_sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    recv_buf = udp_sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(f"   Send buffer: {send_buf} bytes")
    print(f"   Recv buffer: {recv_buf} bytes")

    udp_sock.close()


def demonstrate_multicast() -> None:
    """Demonstrate UDP multicast basics."""
    print("\n" + "=" * 60)
    print("UDP MULTICAST")
    print("=" * 60)

    print("\n1. Multicast addresses:")
    print("   Range: 224.0.0.0 to 239.255.255.255")
    print("   Example: 224.0.0.1 (all hosts)")

    print("\n2. Multicast features:")
    print("   - One-to-many communication")
    print("   - Efficient bandwidth usage")
    print("   - Group management (IGMP)")

    print("\n3. Common uses:")
    print("   - Video conferencing")
    print("   - Stock tickers")
    print("   - Service discovery")


def main() -> None:
    """Main function demonstrating TCP/UDP protocols."""
    print("=" * 60)
    print("PYTHON TCP/UDP PROTOCOLS")
    print("=" * 60)

    demonstrate_tcp_vs_udp()
    demonstrate_tcp_communication()
    demonstrate_udp_communication()
    demonstrate_tcp_features()
    demonstrate_udp_features()
    demonstrate_tcp_streaming()
    demonstrate_udp_datagrams()
    demonstrate_performance_comparison()
    demonstrate_error_handling()
    demonstrate_socket_buffer_sizes()
    demonstrate_multicast()
    demonstrate_use_cases()

    print("\n" + "=" * 60)
    print("All TCP/UDP demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
