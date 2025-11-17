# Program 187: Daemon Processes

## Description
Demonstrates daemon process creation and management, showing how to write background services that run independently of controlling terminals.

## Learning Objectives
- Create daemon processes
- Detach from controlling terminal
- Handle daemon lifecycle
- Implement logging for daemons
- Manage daemon PID files

## Features
- Daemon creation steps
- Session and process group management
- File descriptor handling
- Working directory management
- PID file creation
- Daemon logging

## Compilation
```bash
g++ -std=c++17 main.cpp -o daemon_processes
./daemon_processes
```

## Key Concepts
```cpp
// Daemonize process
pid_t pid = fork();
if (pid > 0) exit(0);  // Parent exits

setsid();  // Create new session

pid = fork();
if (pid > 0) exit(0);  // First child exits

umask(0);
chdir("/");

// Close standard file descriptors
close(STDIN_FILENO);
close(STDOUT_FILENO);
close(STDERR_FILENO);
```

## Best Practices
1. Double-fork to avoid zombies
2. Close all file descriptors
3. Set appropriate umask
4. Change to root directory
5. Create PID file for management
6. Implement logging properly

## Navigation
- **Previous**: [186 - Signal Handling](/home/user/DevOps-prj500/101-200_CPP/186_signal_handling/README.md)
- **Next**: [188 - System Calls](/home/user/DevOps-prj500/101-200_CPP/188_system_calls/README.md)
