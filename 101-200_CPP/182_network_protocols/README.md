# Program 182: Network Protocols

## Description
Explores network protocols including UDP, TCP features, HTTP basics, and protocol implementation patterns in C++.

## Learning Objectives
- Understand TCP vs UDP differences
- Implement UDP communication
- Work with protocol headers
- Handle network byte order
- Parse simple protocols

## Features
- UDP socket implementation
- TCP features demonstration
- Protocol message formatting
- Endianness handling (htons, ntohs)
- Basic HTTP request/response

## Compilation
```bash
g++ -std=c++17 main.cpp -o network_protocols
./network_protocols
```

## Key Concepts
```cpp
// UDP socket
int sock = socket(AF_INET, SOCK_DGRAM, 0);
sendto(sock, buffer, len, 0, (struct sockaddr*)&addr, sizeof(addr));
recvfrom(sock, buffer, len, 0, (struct sockaddr*)&addr, &addr_len);

// Byte order
uint16_t port = htons(8080);
uint32_t ip = htonl(INADDR_ANY);
```

## Best Practices
1. Choose appropriate protocol (TCP/UDP)
2. Handle byte order conversions
3. Implement protocol state machines
4. Validate incoming data
5. Use timeouts for network operations

## Navigation
- **Previous**: [181 - Socket Programming](/home/user/DevOps-prj500/101-200_CPP/181_socket_programming/README.md)
- **Next**: [183 - Process Management](/home/user/DevOps-prj500/101-200_CPP/183_process_management/README.md)
