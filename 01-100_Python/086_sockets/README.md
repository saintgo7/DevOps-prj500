# Program 86: Socket Programming

Network programming with sockets for client-server communication.

## Description

This program demonstrates socket programming basics including creating TCP and UDP sockets, client-server communication, connection handling, and network protocols. Foundation for network applications.

## Learning Objectives

- Understand socket fundamentals
- Implement TCP and UDP clients/servers
- Master socket operations
- Learn network protocols
- Handle connection errors
- Practice non-blocking I/O

## Features

- **TCP Sockets**: Reliable, connection-oriented
- **UDP Sockets**: Unreliable, connectionless
- **Client-Server**: Request-response patterns
- **Socket Operations**: bind, listen, accept, connect, send, recv
- **Multiple Clients**: Handle concurrent connections
- **Non-blocking Sockets**: Async I/O
- **Socket Options**: SO_REUSEADDR, SO_KEEPALIVE
- **Error Handling**: Network errors and timeouts

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/086_sockets
python src/main.py
```

## Key Concepts

### TCP Server

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(5)

while True:
    client, addr = server.accept()
    print(f"Connected: {addr}")
    data = client.recv(1024)
    client.send(b"Response")
    client.close()
```

### TCP Client

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))
client.send(b"Request")
response = client.recv(1024)
client.close()
```

### UDP Server

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 8080))

while True:
    data, addr = server.recvfrom(1024)
    server.sendto(b"Response", addr)
```

### Socket Options

```python
# Reuse address (avoid "Address already in use")
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set timeout
server.settimeout(5.0)

# Get socket options
server.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
```

### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | No guarantee |
| Ordering | Ordered | No ordering |
| Speed | Slower | Faster |
| Overhead | Higher | Lower |
| Use Cases | HTTP, FTP, SSH | DNS, Streaming, Gaming |

## Best Practices

1. **Use context managers**: Ensure socket cleanup
2. **Set SO_REUSEADDR**: For development/testing
3. **Set timeouts**: Prevent hanging
4. **Handle partial sends/receives**: Loop until complete
5. **Use select/poll for multiple clients**: Efficient I/O
6. **Validate input**: Don't trust network data
7. **Use proper encoding**: UTF-8 for text
8. **Close sockets properly**: Avoid resource leaks

## Testing

```bash
# Run tests
pytest tests/

# Manual testing
# Terminal 1 - Server
python src/main.py --server

# Terminal 2 - Client
python src/main.py --client

# Test scenarios
# - Basic communication
# - Multiple clients
# - Connection timeout
# - Large data transfer
# - Error conditions
```

## Navigation

- **Previous**: [Program 85 - Signals](../085_signals/README.md)
- **Next**: [Program 87 - TCP/UDP](../087_tcp_udp/README.md)
- **Home**: [Main README](../README.md)
