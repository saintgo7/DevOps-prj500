# Program 183: Process Management

## Description
Demonstrates process creation and management using fork(), exec(), wait(), and related POSIX system calls for multi-process programming.

## Learning Objectives
- Create child processes with fork()
- Execute programs with exec family
- Wait for child processes
- Handle process exit status
- Implement process synchronization

## Features
- fork() for process creation
- exec() family functions
- wait() and waitpid()
- Process exit status
- Zombie and orphan processes
- Process environment

## Compilation
```bash
g++ -std=c++17 main.cpp -o process_management
./process_management
```

## Key Concepts
```cpp
pid_t pid = fork();
if (pid == 0) {
    // Child process
    execl("/bin/ls", "ls", "-l", nullptr);
} else {
    // Parent process
    int status;
    waitpid(pid, &status, 0);
}
```

## Best Practices
1. Always check fork() return value
2. Handle child process exit status
3. Avoid zombie processes with wait()
4. Use exec carefully to avoid security issues
5. Implement proper error handling

## Navigation
- **Previous**: [182 - Network Protocols](/home/user/DevOps-prj500/101-200_CPP/182_network_protocols/README.md)
- **Next**: [184 - IPC Pipes](/home/user/DevOps-prj500/101-200_CPP/184_ipc_pipes/README.md)
