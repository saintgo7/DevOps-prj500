# Program 191: Epoll and Select

## Description
Demonstrates I/O multiplexing with select, poll, and epoll for handling multiple file descriptors efficiently, essential for scalable network servers.

## Learning Objectives
- Use select() for I/O multiplexing
- Implement poll() for better scalability
- Master epoll for high-performance servers
- Compare different multiplexing mechanisms
- Build scalable event loops

## Features
- select() demonstration
- poll() usage
- epoll API (Linux-specific)
- Event loop implementation
- Performance comparison
- Timeout handling

## Compilation
```bash
g++ -std=c++17 main.cpp -o epoll_select
./epoll_select
```

## Key Concepts
```cpp
// select
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(sock, &readfds);
select(sock + 1, &readfds, nullptr, nullptr, &timeout);

// epoll (Linux)
int epoll_fd = epoll_create1(0);
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, sock, &event);
epoll_wait(epoll_fd, events, MAX_EVENTS, timeout);
```

## Best Practices
1. Use epoll on Linux for scalability
2. Handle edge-triggered events carefully
3. Set appropriate timeouts
4. Check for error conditions
5. Profile for performance bottlenecks

## Navigation
- **Previous**: [190 - POSIX Threads](/home/user/DevOps-prj500/101-200_CPP/190_posix_threads/README.md)
- **Next**: [192 - Async IO](/home/user/DevOps-prj500/101-200_CPP/192_async_io/README.md)
