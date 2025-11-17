# Program 188: System Calls

## Description
Explores essential POSIX system calls for file operations, process control, and system interaction, providing low-level system programming capabilities.

## Learning Objectives
- Use file system calls (open, read, write, close)
- Implement process system calls
- Work with file descriptors
- Handle system call errors
- Understand errno

## Features
- File operations (open, read, write, close)
- File descriptor manipulation
- Process control system calls
- Error handling with errno
- System call wrappers
- Performance considerations

## Compilation
```bash
g++ -std=c++17 main.cpp -o system_calls
./system_calls
```

## Key Concepts
```cpp
int fd = open("file.txt", O_RDONLY);
if (fd == -1) {
    perror("open");
    return 1;
}

char buffer[1024];
ssize_t bytes = read(fd, buffer, sizeof(buffer));

write(STDOUT_FILENO, buffer, bytes);
close(fd);
```

## Best Practices
1. Always check system call return values
2. Use perror or strerror for error messages
3. Close file descriptors when done
4. Handle EINTR for interrupted calls
5. Use appropriate error handling

## Navigation
- **Previous**: [187 - Daemon Processes](/home/user/DevOps-prj500/101-200_CPP/187_daemon_processes/README.md)
- **Next**: [189 - Memory Mapped Files](/home/user/DevOps-prj500/101-200_CPP/189_memory_mapped_files/README.md)
