# Program 84: Subprocess Management

Running external commands and managing subprocesses using subprocess module.

## Description

This program demonstrates subprocess management for running shell commands, capturing output, handling errors, and managing process pipelines. Essential for system automation and shell integration.

## Learning Objectives

- Master subprocess module
- Run external commands safely
- Capture and process output
- Handle process errors
- Create command pipelines
- Understand security considerations

## Features

- **Command Execution**: run(), Popen(), call()
- **Output Capture**: stdout, stderr handling
- **Input/Output**: Pipe data to/from processes
- **Error Handling**: Return codes, exceptions
- **Timeouts**: Prevent hanging processes
- **Shell Commands**: Direct shell execution
- **Process Pipelines**: Chain commands
- **Environment Variables**: Custom environment

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/084_subprocess
python src/main.py
```

## Key Concepts

### subprocess.run() (Recommended)

```python
import subprocess

# Simple command
result = subprocess.run(['ls', '-la'],
                       capture_output=True,
                       text=True)

print(result.stdout)
print(result.returncode)
```

### Capturing Output

```python
# Capture stdout and stderr
result = subprocess.run(['command'],
                       capture_output=True,
                       text=True)

# Combine stderr with stdout
result = subprocess.run(['command'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
```

### Error Handling

```python
# Raise exception on failure
result = subprocess.run(['command'],
                       check=True,  # Raises CalledProcessError
                       capture_output=True)

# Check return code manually
if result.returncode != 0:
    print(f"Error: {result.stderr}")
```

### Timeouts

```python
try:
    result = subprocess.run(['command'],
                           timeout=5,  # seconds
                           capture_output=True)
except subprocess.TimeoutExpired:
    print("Command timed out")
```

### Shell vs Direct Execution

**Direct (Safer):**
```python
subprocess.run(['ls', '-la'])  # List as arguments
```

**Shell (Dangerous if user input):**
```python
subprocess.run('ls -la', shell=True)  # String command
```

## Best Practices

1. **Use run() for most cases**: Simplest and safest
2. **Avoid shell=True**: Security risk with user input
3. **Pass arguments as list**: Prevents injection
4. **Set timeout**: Prevent hanging processes
5. **Use check=True**: Raise exception on error
6. **Capture output properly**: Use capture_output=True
7. **Handle encoding**: Use text=True or specify encoding
8. **Clean up resources**: Popen objects need close()

## Testing

```bash
# Run tests
pytest tests/

# Test scenarios
# - Successful command execution
# - Command failure (non-zero exit)
# - Timeout handling
# - Output capture
# - Error output
# - Environment variables
# - Working directory change
```

## Navigation

- **Previous**: [Program 83 - Process Management](../083_process_management/README.md)
- **Next**: [Program 85 - Signals](../085_signals/README.md)
- **Home**: [Main README](../README.md)
