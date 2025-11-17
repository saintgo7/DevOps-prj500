# Program 85: Signal Handling

Unix signal handling for process communication and graceful shutdown.

## Description

This program demonstrates signal handling in Python using the signal module. Covers handling interrupts, graceful shutdown, custom signal handlers, and inter-process signaling for Unix-like systems.

## Learning Objectives

- Understand Unix signals
- Implement signal handlers
- Practice graceful shutdown
- Learn signal types and uses
- Handle cleanup on termination

## Features

- **Common Signals**: SIGINT, SIGTERM, SIGHUP, SIGUSR1/2
- **Signal Handlers**: Register custom handlers
- **Graceful Shutdown**: Clean up resources
- **Signal Blocking**: Prevent signal delivery
- **Signal Masking**: Control signal handling
- **Alarm Signals**: SIGALRM for timeouts
- **Child Process Signals**: SIGCHLD handling
- **Signal Sending**: Send signals between processes

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/085_signals
python src/main.py
```

## Key Concepts

### Common Signals

| Signal | Number | Default Action | Catchable | Description |
|--------|--------|----------------|-----------|-------------|
| SIGINT | 2 | Terminate | Yes | Interrupt (Ctrl+C) |
| SIGTERM | 15 | Terminate | Yes | Termination request |
| SIGKILL | 9 | Terminate | No | Force kill |
| SIGHUP | 1 | Terminate | Yes | Hangup |
| SIGALRM | 14 | Terminate | Yes | Alarm clock |
| SIGUSR1 | 10 | Terminate | Yes | User-defined |
| SIGUSR2 | 12 | Terminate | Yes | User-defined |
| SIGCHLD | 17 | Ignore | Yes | Child stopped/terminated |

### Signal Handler

```python
import signal
import sys

def signal_handler(sig, frame):
    print(f'Received signal {sig}')
    # Clean up resources
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

### Graceful Shutdown Pattern

```python
import signal
import time

shutdown_flag = False

def shutdown_handler(sig, frame):
    global shutdown_flag
    shutdown_flag = True
    print("Shutting down gracefully...")

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

while not shutdown_flag:
    # Main work
    time.sleep(1)

# Cleanup
print("Cleanup completed")
```

### Sending Signals

```python
import os
import signal

# Send signal to process
os.kill(pid, signal.SIGTERM)

# Send to process group
os.killpg(pgid, signal.SIGTERM)
```

## Best Practices

1. **Handle SIGINT and SIGTERM**: For graceful shutdown
2. **Use flags for shutdown**: Don't exit directly in handler
3. **Keep handlers short**: Minimal work in signal context
4. **Restore default handlers**: When appropriate
5. **Use signal.alarm() for timeouts**: Simple timer mechanism
6. **Don't use print() in handlers**: Not signal-safe
7. **Test signal handling**: Verify cleanup works
8. **Document signal behavior**: What each handler does

## Testing

```bash
# Run tests
pytest tests/

# Manual testing
python src/main.py &
PID=$!

# Send signals
kill -SIGINT $PID   # Interrupt
kill -SIGTERM $PID  # Terminate
kill -SIGHUP $PID   # Hangup
kill -SIGUSR1 $PID  # User signal

# Force kill (uncatchable)
kill -SIGKILL $PID
```

## Navigation

- **Previous**: [Program 84 - Subprocess](../084_subprocess/README.md)
- **Next**: [Program 86 - Sockets](../086_sockets/README.md)
- **Home**: [Main README](../README.md)
