# Program 192: Asynchronous I/O

## Description
Explores asynchronous I/O operations using POSIX AIO and modern async patterns for non-blocking file and network operations.

## Learning Objectives
- Use POSIX AIO for async file operations
- Implement completion callbacks
- Handle AIO errors and results
- Compare sync vs async I/O
- Apply async patterns effectively

## Features
- POSIX AIO basics
- Async read/write operations
- Completion notification
- AIO control blocks
- Error handling
- Performance benefits

## Compilation
```bash
g++ -std=c++17 main.cpp -o async_io -lrt
./async_io
```

## Key Concepts
```cpp
struct aiocb cb;
memset(&cb, 0, sizeof(cb));
cb.aio_fildes = fd;
cb.aio_buf = buffer;
cb.aio_nbytes = size;

aio_read(&cb);

// Check completion
while (aio_error(&cb) == EINPROGRESS) { /* wait */ }
ssize_t ret = aio_return(&cb);
```

## Best Practices
1. Use async I/O for I/O-bound applications
2. Handle completion notifications properly
3. Manage AIO control blocks carefully
4. Consider using higher-level libraries
5. Profile to ensure performance gain

## Navigation
- **Previous**: [191 - Epoll Select](/home/user/DevOps-prj500/101-200_CPP/191_epoll_select/README.md)
- **Next**: [193 - Performance Profiling](/home/user/DevOps-prj500/101-200_CPP/193_performance_profiling/README.md)
