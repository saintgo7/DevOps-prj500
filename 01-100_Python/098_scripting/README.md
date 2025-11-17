# Program 98: Shell Scripting with Python

Using Python as a shell scripting replacement with subprocess and system integration.

## Description

This program demonstrates using Python for system tasks traditionally done with shell scripts. Covers running commands, text processing, file operations, and building cross-platform automation scripts.

## Learning Objectives

- Replace shell scripts with Python
- Master subprocess module
- Handle command output
- Process text like grep/sed/awk
- Create portable scripts
- Integrate with system tools

## Features

- **Command Execution**: Run shell commands safely
- **Text Processing**: grep, sed, awk alternatives
- **File Operations**: Find, copy, move, delete
- **Process Management**: Background processes
- **Environment Variables**: Read and set
- **User Interaction**: Input, prompts, passwords
- **Archiving**: tar, zip operations
- **System Information**: Platform, paths, users

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/098_scripting
python src/main.py
```

## Key Concepts

### Running Commands

```python
import subprocess

# Simple command
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# With error checking
result = subprocess.run(['command'], check=True)

# Shell command (use carefully)
result = subprocess.run('ls | grep txt', shell=True, capture_output=True)
```

### Text Processing (grep alternative)

```python
# Find lines matching pattern
with open('log.txt') as f:
    errors = [line for line in f if 'ERROR' in line]

# With regex
import re
pattern = re.compile(r'ERROR: (\d+)')
for line in file:
    if match := pattern.search(line):
        error_code = match.group(1)
```

### File Operations (find alternative)

```python
from pathlib import Path

# Find all .txt files recursively
txt_files = Path('.').rglob('*.txt')

# Find files modified in last 24 hours
import time
day_ago = time.time() - 86400
recent = [f for f in Path('.').rglob('*')
          if f.stat().st_mtime > day_ago]
```

### Text Replacement (sed alternative)

```python
# Replace in file
content = Path('file.txt').read_text()
modified = content.replace('old', 'new')
Path('file.txt').write_text(modified)

# With regex
import re
modified = re.sub(r'pattern', 'replacement', content)
```

### Process Management

```python
# Start background process
proc = subprocess.Popen(['long-running-command'])

# Check if still running
if proc.poll() is None:
    print("Still running")

# Wait for completion
proc.wait()
```

### Environment Variables

```python
import os

# Read environment variable
home = os.environ.get('HOME')
user = os.getenv('USER', 'unknown')

# Set environment variable
os.environ['MY_VAR'] = 'value'

# Run command with custom env
env = os.environ.copy()
env['CUSTOM'] = 'value'
subprocess.run(['command'], env=env)
```

## Best Practices

1. **Use subprocess.run()**: Modern, safe API
2. **Avoid shell=True**: Security risk
3. **Pass lists not strings**: Prevent injection
4. **Use Path for files**: Cross-platform
5. **Check return codes**: Handle errors
6. **Set timeouts**: Prevent hanging
7. **Use text=True**: For string output
8. **Test on target platforms**: OS differences

## Testing

```bash
# Run tests
pytest tests/

# Test script
python src/main.py --dry-run

# Test scenarios
# - Command execution
# - Error handling
# - Text processing
# - File operations
# - Cross-platform compatibility
# - Edge cases
```

## Navigation

- **Previous**: [Program 97 - Automation](../097_automation/README.md)
- **Next**: [Program 99 - Deployment](../099_deployment/README.md)
- **Home**: [Main README](../README.md)
