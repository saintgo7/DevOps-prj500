# Program 184: IPC Pipes

## Description
Explores inter-process communication using pipes, including anonymous pipes for parent-child communication and named pipes (FIFOs) for unrelated processes.

## Learning Objectives
- Create and use anonymous pipes
- Implement parent-child communication
- Work with named pipes (FIFOs)
- Handle pipe blocking behavior
- Implement bidirectional communication

## Features
- Anonymous pipe creation
- Pipe reading and writing
- Named pipe (FIFO) usage
- Pipe capacity and buffering
- Nonblocking pipes
- Pipe error handling

## Compilation
```bash
g++ -std=c++17 main.cpp -o ipc_pipes
./ipc_pipes
```

## Key Concepts
```cpp
int pipefd[2];
pipe(pipefd);  // pipefd[0] = read, pipefd[1] = write

if (fork() == 0) {
    close(pipefd[1]);
    read(pipefd[0], buffer, sizeof(buffer));
} else {
    close(pipefd[0]);
    write(pipefd[1], "Hello", 5);
}

// Named pipe
mkfifo("/tmp/myfifo", 0666);
```

## Best Practices
1. Close unused pipe ends
2. Handle pipe capacity limits
3. Check for broken pipes (SIGPIPE)
4. Use select/poll for multiple pipes
5. Clean up named pipes when done

## Navigation
- **Previous**: [183 - Process Management](/home/user/DevOps-prj500/101-200_CPP/183_process_management/README.md)
- **Next**: [185 - Shared Memory](/home/user/DevOps-prj500/101-200_CPP/185_shared_memory/README.md)
