# 12_file_io

## Description

Master file input/output operations in Python with comprehensive demonstrations of reading, writing, file modes, JSON/CSV handling, pathlib, and context managers. File I/O is essential for data persistence, configuration management, and data processing.

This is Program #12 in the 500 Programs Collection.

## Learning Objectives

- Read and write text files effectively
- Understand different file opening modes
- Use file object methods (read, readline, readlines, write, writelines)
- Work with JSON and CSV files
- Use pathlib for modern path handling
- Implement context managers for safe file operations
- Perform file system operations
- Apply file I/O best practices

## Features

- Basic file operations (read, write, append)
- All file opening modes (r, w, a, r+, w+, rb, wb)
- File methods (read, readline, readlines, write, writelines, seek, tell)
- JSON operations (load, dump, loads, dumps)
- CSV operations (reader, writer, DictReader, DictWriter)
- pathlib for object-oriented path handling
- Context managers for automatic file closing
- File system operations (rename, copy, delete, check existence)

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic File Operations

```python
# Write to file
with open("file.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("Python File I/O\n")

# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read lines as list
with open("file.txt", "r") as f:
    lines = f.readlines()  # ['Hello, World!\n', 'Python File I/O\n']

# Read line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Append to file
with open("file.txt", "a") as f:
    f.write("Appended line\n")
```

### 2. File Opening Modes

```python
# Text modes
"r"   # Read (default)
"w"   # Write (truncates existing file)
"a"   # Append
"r+"  # Read and write
"w+"  # Write and read (truncates)
"a+"  # Append and read

# Binary modes
"rb"  # Read binary
"wb"  # Write binary
"ab"  # Append binary
"rb+" # Read and write binary

# Example
with open("file.bin", "wb") as f:
    f.write(b"Binary data")

with open("file.bin", "rb") as f:
    data = f.read()
```

### 3. File Object Methods

```python
with open("file.txt", "w") as f:
    # write()
    f.write("Line 1\n")

    # writelines()
    f.writelines(["Line 2\n", "Line 3\n"])

with open("file.txt", "r") as f:
    # read(size) - read up to size bytes
    chunk = f.read(10)

    # readline() - read single line
    line = f.readline()

    # readlines() - read all lines as list
    lines = f.readlines()

    # tell() - current position
    position = f.tell()

    # seek(offset, whence) - move to position
    f.seek(0)  # Beginning
    f.seek(0, 2)  # End
```

### 4. JSON Operations

```python
import json

data = {
    "name": "Alice",
    "age": 25,
    "hobbies": ["reading", "coding"]
}

# Write JSON to file
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read JSON from file
with open("data.json", "r") as f:
    loaded = json.load(f)

# JSON string operations
json_string = json.dumps(data, indent=2)
parsed = json.loads(json_string)
```

### 5. CSV Operations

```python
import csv

# Write CSV
headers = ["name", "age", "city"]
rows = [
    ["Alice", 25, "NYC"],
    ["Bob", 30, "LA"],
]

with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

# Read CSV
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# DictReader and DictWriter
dict_data = [
    {"name": "Alice", "age": 25, "city": "NYC"},
    {"name": "Bob", "age": 30, "city": "LA"},
]

with open("data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows(dict_data)

with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

### 6. Pathlib (Modern Approach)

```python
from pathlib import Path

# Create Path object
path = Path("file.txt")

# Write
path.write_text("Hello from pathlib!")

# Read
content = path.read_text()

# Path properties
absolute = path.absolute()
name = path.name
stem = path.stem  # Filename without extension
suffix = path.suffix  # Extension
parent = path.parent

# Check existence
exists = path.exists()
is_file = path.is_file()
is_dir = path.is_dir()

# Create directories
dir_path = Path("new_dir")
dir_path.mkdir(exist_ok=True)

# Nested directories
nested = Path("parent/child")
nested.mkdir(parents=True, exist_ok=True)

# List directory
for file in Path(".").glob("*.txt"):
    print(file)

# Delete
path.unlink()  # Delete file
dir_path.rmdir()  # Delete empty directory
```

### 7. Context Managers

```python
# Basic context manager (automatically closes file)
with open("file.txt", "w") as f:
    f.write("Context manager")
# File automatically closed here

# Multiple files
with open("input.txt", "r") as f_in, open("output.txt", "w") as f_out:
    content = f_in.read()
    f_out.write(content.upper())

# Manual file handling (NOT recommended)
f = open("file.txt", "w")
try:
    f.write("Data")
finally:
    f.close()  # Must close manually
```

### 8. File System Operations

```python
import os
import shutil
from pathlib import Path

# Check existence
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("directory")

# File info
size = os.path.getsize("file.txt")
modified_time = os.path.getmtime("file.txt")

# Rename
os.rename("old.txt", "new.txt")

# Copy
shutil.copy2("source.txt", "dest.txt")

# Delete
os.remove("file.txt")

# List directory
files = os.listdir(".")
```

## Best Practices

1. **Always Use Context Managers**
   ```python
   # Good
   with open("file.txt", "r") as f:
       content = f.read()

   # Bad - file might not close if exception occurs
   f = open("file.txt", "r")
   content = f.read()
   f.close()
   ```

2. **Use pathlib for Path Operations**
   ```python
   # Good - modern, cross-platform
   from pathlib import Path
   path = Path("data") / "file.txt"

   # Older approach
   import os
   path = os.path.join("data", "file.txt")
   ```

3. **Specify Encoding for Text Files**
   ```python
   # Good
   with open("file.txt", "r", encoding="utf-8") as f:
       content = f.read()

   # Can cause issues with non-ASCII characters
   with open("file.txt", "r") as f:
       content = f.read()
   ```

4. **Use newline='' for CSV Files**
   ```python
   # Good
   with open("data.csv", "w", newline="") as f:
       writer = csv.writer(f)

   # Can cause extra blank lines on Windows
   with open("data.csv", "w") as f:
       writer = csv.writer(f)
   ```

5. **Check File Existence Before Operations**
   ```python
   from pathlib import Path

   path = Path("file.txt")
   if path.exists():
       content = path.read_text()
   ```

6. **Use JSON for Configuration**
   ```python
   # Good for configuration files
   config = {
       "host": "localhost",
       "port": 8080,
       "debug": True
   }
   with open("config.json", "w") as f:
       json.dump(config, f, indent=2)
   ```

## Common Patterns

### 1. Read Large Files Line by Line

```python
# Memory efficient
with open("large_file.txt", "r") as f:
    for line in f:
        process(line.strip())
```

### 2. Read File into List

```python
with open("file.txt", "r") as f:
    lines = [line.strip() for line in f]
```

### 3. Write List to File

```python
lines = ["line1", "line2", "line3"]
with open("file.txt", "w") as f:
    f.write("\n".join(lines))
```

### 4. Copy File Contents

```python
with open("source.txt", "r") as f_in, open("dest.txt", "w") as f_out:
    f_out.write(f_in.read())
```

### 5. Process JSON Configuration

```python
def load_config(filename):
    with open(filename, "r") as f:
        return json.load(f)

config = load_config("config.json")
```

## File Modes Quick Reference

| Mode | Read | Write | Create | Truncate | Position |
|------|------|-------|--------|----------|----------|
| r    | ✓    |       |        |          | Start    |
| w    |      | ✓     | ✓      | ✓        | Start    |
| a    |      | ✓     | ✓      |          | End      |
| r+   | ✓    | ✓     |        |          | Start    |
| w+   | ✓    | ✓     | ✓      | ✓        | Start    |
| a+   | ✓    | ✓     | ✓      |          | End      |

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

## Common Pitfalls

1. **Forgetting to Close Files** - Use context managers
2. **Not Specifying Encoding** - Especially for non-ASCII text
3. **Modifying File While Reading** - Can cause unexpected behavior
4. **Not Handling File Not Found** - Use try-except or check existence
5. **Using Wrong newline Mode for CSV** - Use `newline=''`

---

**Program**: 12 of 500
**Difficulty**: ⭐⭐ Beginner/Intermediate
**Category**: Python Basics / File I/O
**Estimated Time**: 45-60 minutes

[← Previous (11)](../11_string_methods/) | [Back to Index](../../docs/INDEX.md) | [Next (13) →](../13_exception_handling/)
