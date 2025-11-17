# Program 186: Signal Handling

## Description
Explores POSIX signal handling for asynchronous event notification, including signal handlers, signal masks, and signal-safe programming.

## Learning Objectives
- Install signal handlers
- Use signal masks
- Implement safe signal handlers
- Work with real-time signals
- Handle common signals (SIGINT, SIGTERM, etc.)

## Features
- signal() and sigaction()
- Signal handler implementation
- Signal masks (sigprocmask)
- Signal sets (sigemptyset, sigaddset)
- Real-time signals
- Signal safety

## Compilation
```bash
g++ -std=c++17 main.cpp -o signal_handling
./signal_handling
```

## Key Concepts
```cpp
void signal_handler(int signum) {
    // Signal-safe operations only!
    write(STDOUT_FILENO, "Caught signal\n", 14);
}

struct sigaction sa;
sa.sa_handler = signal_handler;
sigemptyset(&sa.sa_mask);
sa.sa_flags = 0;
sigaction(SIGINT, &sa, nullptr);
```

## Best Practices
1. Use sigaction() instead of signal()
2. Keep signal handlers simple
3. Only use async-signal-safe functions
4. Set SA_RESTART flag for system calls
5. Block signals during critical sections

## Navigation
- **Previous**: [185 - Shared Memory](/home/user/DevOps-prj500/101-200_CPP/185_shared_memory/README.md)
- **Next**: [187 - Daemon Processes](/home/user/DevOps-prj500/101-200_CPP/187_daemon_processes/README.md)
