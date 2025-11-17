# Program 82: Path Operations

Advanced path manipulation and resolution using pathlib.

## Description

This program focuses on path operations including path construction, normalization, resolution, relative paths, and cross-platform compatibility. Essential for building robust file system applications.

## Learning Objectives

- Master pathlib Path operations
- Understand absolute vs relative paths
- Learn path normalization and resolution
- Handle cross-platform path issues
- Practice path manipulation patterns

## Features

- **Path Construction**: Build paths from components
- **Path Resolution**: Resolve relative and symbolic links
- **Path Normalization**: Remove redundant separators
- **Path Comparison**: Check path relationships
- **Path Components**: Extract parts (name, stem, suffix, parent)
- **Relative Paths**: Convert between absolute and relative
- **Glob Patterns**: Find files matching patterns
- **Cross-platform**: Handle Windows/Unix differences

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/082_path_operations
python src/main.py
```

## Key Concepts

### Path Components

```python
path = Path('/home/user/documents/file.txt')

path.name          # 'file.txt'
path.stem          # 'file'
path.suffix        # '.txt'
path.parent        # '/home/user/documents'
path.parents[0]    # '/home/user/documents'
path.parents[1]    # '/home/user'
path.anchor        # '/'
```

### Path Operations

**Construction:**
```python
Path('/home') / 'user' / 'file.txt'
Path.home() / 'documents'
Path.cwd() / 'relative' / 'path'
```

**Resolution:**
```python
path.resolve()           # Absolute path
path.absolute()          # Absolute (may contain ..)
path.expanduser()        # Expand ~
```

**Comparison:**
```python
path.is_absolute()
path.is_relative_to(other)
path.relative_to(other)
path.samefile(other)
```

### Glob Patterns

```python
Path.glob('*.txt')        # All .txt files
Path.glob('**/*.py')      # All .py files recursively
Path.rglob('*.md')        # Recursive glob shorthand
```

### Cross-platform Considerations

- Use `Path` objects - automatic separator handling
- Avoid hardcoded separators ('/' or '\\')
- Use `Path.home()` and `Path.cwd()` for base paths
- Test on target platforms

## Best Practices

1. **Use Path objects throughout**: Don't mix strings and Path
2. **Use / operator for joining**: More readable than joinpath
3. **Resolve paths early**: Convert to absolute paths
4. **Use relative_to for comparing**: Check path relationships
5. **Use glob for pattern matching**: More efficient than manual
6. **Handle WindowsPath vs PosixPath**: Use Path for portability
7. **Cache resolved paths**: If used repeatedly
8. **Validate paths**: Check exists(), is_file(), is_dir()

## Testing

```bash
# Run tests
pytest tests/

# Test scenarios
# - Path construction
# - Absolute/relative conversion
# - Path component extraction
# - Glob pattern matching
# - Cross-platform compatibility
# - Symbolic link resolution
```

## Navigation

- **Previous**: [Program 81 - File System](../081_file_system/README.md)
- **Next**: [Program 83 - Process Management](../083_process_management/README.md)
- **Home**: [Main README](../README.md)
