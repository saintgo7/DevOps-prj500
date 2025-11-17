# Program 87: TCP and UDP Protocols

Advanced TCP and UDP programming with protocol implementation.

## Description

This program demonstrates advanced TCP and UDP protocol usage including connection management, data streaming, error handling, and protocol design patterns. Builds on socket fundamentals for real-world network applications.

## Learning Objectives

- Master TCP connection lifecycle
- Understand UDP datagram handling
- Implement custom protocols
- Learn flow control and buffering
- Handle network errors gracefully
- Practice protocol design

## Features

- **TCP Features**:
  - Connection management
  - Streaming data
  - Flow control
  - Error recovery
  - Keep-alive
- **UDP Features**:
  - Datagram handling
  - No connection overhead
  - Broadcast/multicast
  - Packet loss handling
- **Protocol Design**: Custom message formats
- **Error Handling**: Timeouts, retries, recovery
- **Performance**: Buffering, batching

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/087_tcp_udp
python src/main.py
```

## Key Concepts

### TCP Connection Lifecycle

1. **Server**: socket() → bind() → listen() → accept()
2. **Client**: socket() → connect()
3. **Communication**: send() / recv()
4. **Teardown**: close()

### TCP Three-Way Handshake

1. Client sends SYN
2. Server sends SYN-ACK
3. Client sends ACK
4. Connection established

### UDP Characteristics

- **Connectionless**: No handshake
- **Unreliable**: Packets may be lost, duplicated, reordered
- **Fast**: No connection overhead
- **Message-based**: Maintains message boundaries

### Handling Partial Sends/Receives

```python
def send_all(sock, data):
    """Send all data, handling partial sends."""
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

def recv_all(sock, size):
    """Receive exact amount of data."""
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise RuntimeError("Socket connection broken")
        data += chunk
    return data
```

### Protocol Design Pattern

```python
# Message format: [4-byte length][payload]
def send_message(sock, message):
    data = message.encode('utf-8')
    length = len(data)
    sock.sendall(length.to_bytes(4, 'big') + data)

def recv_message(sock):
    length_bytes = recv_all(sock, 4)
    length = int.from_bytes(length_bytes, 'big')
    return recv_all(sock, length).decode('utf-8')
```

### When to Use TCP vs UDP

**Use TCP for:**
- Reliable data transfer
- File transfers
- Web applications (HTTP/HTTPS)
- Email (SMTP)
- Remote shell (SSH)

**Use UDP for:**
- Real-time applications
- Video/audio streaming
- Online gaming
- DNS queries
- IoT sensors

## Best Practices

1. **TCP:**
   - Handle partial sends/receives
   - Implement proper timeouts
   - Use keepalive for long connections
   - Buffer data appropriately
2. **UDP:**
   - Keep messages small (< MTU)
   - Implement own reliability if needed
   - Handle out-of-order delivery
   - Consider packet loss
3. **Both:**
   - Validate all input
   - Use length-prefixed messages
   - Implement version negotiation
   - Log network events

## Testing

```bash
# Run tests
pytest tests/

# Performance testing
# - Throughput measurement
# - Latency testing
# - Packet loss simulation (UDP)
# - Connection stress testing

# Test scenarios
# - Normal operation
# - Network errors
# - Partial data
# - Concurrent connections
# - Large data transfers
```

## Navigation

- **Previous**: [Program 86 - Sockets](../086_sockets/README.md)
- **Next**: [Program 88 - HTTP Server](../088_http_server/README.md)
- **Home**: [Main README](../README.md)
