# Program 181: Socket Programming

## Description
Introduces socket programming in C++ for network communication, covering TCP/IP sockets, client-server architecture, and basic network operations.

## Learning Objectives
- Create and configure sockets
- Implement TCP client-server communication
- Handle socket connections and data transfer
- Use non-blocking I/O
- Implement basic error handling for network operations

## Features
- Socket creation and binding
- TCP server implementation
- TCP client implementation
- Send and receive operations
- Connection management
- Error handling

## Compilation
```bash
g++ -std=c++17 main.cpp -o socket_programming
./socket_programming
```

## Key Concepts
```cpp
// Server
int server_fd = socket(AF_INET, SOCK_STREAM, 0);
bind(server_fd, (struct sockaddr*)&address, sizeof(address));
listen(server_fd, 3);
int client_socket = accept(server_fd, ...);

// Client
int sock = socket(AF_INET, SOCK_STREAM, 0);
connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
send(sock, message, strlen(message), 0);
```

## Best Practices
1. Always check socket operation return values
2. Close sockets properly to avoid leaks
3. Handle partial sends/receives
4. Use select/poll for multiple connections
5. Implement proper error handling

## Navigation
- **Previous**: [180 - Chrono](/home/user/DevOps-prj500/101-200_CPP/180_chrono/README.md)
- **Next**: [182 - Network Protocols](/home/user/DevOps-prj500/101-200_CPP/182_network_protocols/README.md)
