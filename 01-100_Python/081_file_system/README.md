# Program 81: File System Operations

Comprehensive file system operations using Python's pathlib and os modules.

## Description

This program demonstrates file system manipulation including file and directory operations, path handling, file metadata, permissions, and file system traversal. Essential for system programming and automation tasks.

## Learning Objectives

- Master file and directory operations
- Learn path manipulation with pathlib
- Understand file permissions and metadata
- Practice file system traversal
- Handle cross-platform path issues

## Features

- **File Operations**: Create, read, write, delete, copy, move
- **Directory Operations**: Create, remove, list, walk
- **Path Manipulation**: Join, split, normalize, resolve
- **File Metadata**: Size, modification time, permissions
- **File Permissions**: chmod, chown operations
- **Symbolic Links**: Create and resolve symlinks
- **Temporary Files**: Create temp files and directories
- **Cross-platform**: Handle Windows/Unix path differences

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/081_file_system
python src/main.py
```

## Key Concepts

### Pathlib vs os.path

**Use pathlib (modern approach):**
```python
from pathlib import Path

path = Path('/home/user/file.txt')
path.exists()
path.is_file()
path.read_text()
```

**os.path (legacy but still useful):**
```python
import os

os.path.exists('/home/user/file.txt')
os.path.isfile('/home/user/file.txt')
```

### Common Operations

**File Operations:**
- `Path.read_text()` / `Path.write_text()` - Read/write text
- `Path.read_bytes()` / `Path.write_bytes()` - Read/write bytes
- `Path.unlink()` - Delete file
- `shutil.copy()` - Copy file
- `shutil.move()` - Move file

**Directory Operations:**
- `Path.mkdir(parents=True)` - Create directory
- `Path.rmdir()` - Remove empty directory
- `shutil.rmtree()` - Remove directory tree
- `Path.iterdir()` - List directory contents
- `Path.glob('*.txt')` - Pattern matching

### File Permissions (Unix)

- **Read (r)**: 4
- **Write (w)**: 2
- **Execute (x)**: 1
- **Combination**: chmod 755 = rwxr-xr-x

## Best Practices

1. **Use pathlib for new code**: More Pythonic and powerful
2. **Use context managers**: Ensure files are closed properly
3. **Check existence before operations**: Prevent errors
4. **Handle permissions errors**: Use try-except
5. **Use tempfile for temporary files**: Automatic cleanup
6. **Be careful with recursive delete**: Double-check paths
7. **Use absolute paths**: Avoid ambiguity
8. **Handle cross-platform paths**: Use Path objects

## Testing

```bash
# Run tests
pytest tests/

# Test with different scenarios
# - File operations (create, read, write, delete)
# - Directory traversal
# - Permission handling
# - Symbolic links
# - Edge cases (missing files, permissions)
```

## Navigation

- **Previous**: [Program 80 - Problem Solving](../80_problem_solving/README.md)
- **Next**: [Program 82 - Path Operations](../082_path_operations/README.md)
- **Home**: [Main README](../README.md)
