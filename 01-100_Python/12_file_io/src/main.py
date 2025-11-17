#!/usr/bin/env python3
"""Program 12: File I/O - Master file operations in Python."""

import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any


def demonstrate_basic_file_operations() -> dict[str, Any]:
    """Demonstrate basic file read/write operations."""
    # Write to file
    with open("temp_basic.txt", "w") as f:
        f.write("Hello, World!\n")
        f.write("Python File I/O\n")

    # Read entire file
    with open("temp_basic.txt", "r") as f:
        content = f.read()

    # Read lines
    with open("temp_basic.txt", "r") as f:
        lines = f.readlines()

    # Read line by line
    line_by_line = []
    with open("temp_basic.txt", "r") as f:
        for line in f:
            line_by_line.append(line.strip())

    # Append to file
    with open("temp_basic.txt", "a") as f:
        f.write("Appended line\n")

    # Read after append
    with open("temp_basic.txt", "r") as f:
        final_content = f.read()

    # Cleanup
    os.remove("temp_basic.txt")

    return {
        "initial_content": content,
        "lines": lines,
        "line_by_line": line_by_line,
        "after_append": final_content,
    }


def demonstrate_file_modes() -> dict[str, Any]:
    """Demonstrate different file opening modes."""
    # Write mode (w) - creates or truncates
    with open("temp_modes.txt", "w") as f:
        f.write("Write mode")

    # Read mode (r) - default mode
    with open("temp_modes.txt", "r") as f:
        read_content = f.read()

    # Append mode (a) - adds to end
    with open("temp_modes.txt", "a") as f:
        f.write("\nAppend mode")

    # Read and write mode (r+)
    with open("temp_modes.txt", "r+") as f:
        content = f.read()
        f.write("\nRead+ mode")

    # Write and read mode (w+) - truncates first
    with open("temp_modes_w.txt", "w+") as f:
        f.write("Write+ mode")
        f.seek(0)  # Go back to start
        w_plus_content = f.read()

    # Binary mode
    with open("temp_binary.bin", "wb") as f:
        f.write(b"Binary data")

    with open("temp_binary.bin", "rb") as f:
        binary_content = f.read()

    # Cleanup
    os.remove("temp_modes.txt")
    os.remove("temp_modes_w.txt")
    os.remove("temp_binary.bin")

    return {
        "write_mode": read_content,
        "after_append": content,
        "write_plus": w_plus_content,
        "binary": binary_content,
    }


def demonstrate_file_methods() -> dict[str, Any]:
    """Demonstrate file object methods."""
    with open("temp_methods.txt", "w") as f:
        f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

    # read(size)
    with open("temp_methods.txt", "r") as f:
        chunk1 = f.read(10)
        chunk2 = f.read(10)
        position = f.tell()

    # readline()
    with open("temp_methods.txt", "r") as f:
        line1 = f.readline()
        line2 = f.readline()

    # seek()
    with open("temp_methods.txt", "r") as f:
        f.seek(0)  # Beginning
        from_start = f.read(10)
        f.seek(0, 2)  # End
        file_size = f.tell()

    # writelines()
    lines = ["First\n", "Second\n", "Third\n"]
    with open("temp_writelines.txt", "w") as f:
        f.writelines(lines)

    with open("temp_writelines.txt", "r") as f:
        writelines_result = f.read()

    # Cleanup
    os.remove("temp_methods.txt")
    os.remove("temp_writelines.txt")

    return {
        "chunk1": chunk1,
        "chunk2": chunk2,
        "position_after_chunks": position,
        "readline1": line1.strip(),
        "readline2": line2.strip(),
        "file_size": file_size,
        "writelines": writelines_result,
    }


def demonstrate_json_operations() -> dict[str, Any]:
    """Demonstrate JSON file operations."""
    # Write JSON
    data = {
        "name": "Alice",
        "age": 25,
        "city": "NYC",
        "hobbies": ["reading", "coding", "gaming"]
    }

    with open("temp_data.json", "w") as f:
        json.dump(data, f, indent=2)

    # Read JSON
    with open("temp_data.json", "r") as f:
        loaded_data = json.load(f)

    # JSON strings
    json_string = json.dumps(data, indent=2)
    from_string = json.loads(json_string)

    # Cleanup
    os.remove("temp_data.json")

    return {
        "original": data,
        "loaded": loaded_data,
        "are_equal": data == loaded_data,
        "json_string": json_string,
    }


def demonstrate_csv_operations() -> dict[str, Any]:
    """Demonstrate CSV file operations."""
    # Write CSV
    headers = ["name", "age", "city"]
    rows = [
        ["Alice", 25, "NYC"],
        ["Bob", 30, "LA"],
        ["Charlie", 35, "Chicago"]
    ]

    with open("temp_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    # Read CSV
    read_rows = []
    with open("temp_data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            read_rows.append(row)

    # DictReader and DictWriter
    dict_data = [
        {"name": "Alice", "age": 25, "city": "NYC"},
        {"name": "Bob", "age": 30, "city": "LA"},
    ]

    with open("temp_dict.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
        writer.writeheader()
        writer.writerows(dict_data)

    read_dict_data = []
    with open("temp_dict.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            read_dict_data.append(dict(row))

    # Cleanup
    os.remove("temp_data.csv")
    os.remove("temp_dict.csv")

    return {
        "written_rows": rows,
        "read_rows": read_rows[1:],  # Skip header
        "dict_data": dict_data,
        "read_dict_data": read_dict_data,
    }


def demonstrate_pathlib() -> dict[str, Any]:
    """Demonstrate pathlib operations."""
    # Create Path objects
    path = Path("temp_pathlib.txt")

    # Write using pathlib
    path.write_text("Hello from pathlib!")

    # Read using pathlib
    content = path.read_text()

    # Path operations
    absolute = path.absolute()
    name = path.name
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    exists = path.exists()

    # Create directories
    dir_path = Path("temp_dir")
    dir_path.mkdir(exist_ok=True)

    # Create nested directories
    nested_path = Path("temp_parent/temp_child")
    nested_path.mkdir(parents=True, exist_ok=True)

    # List directory
    files = list(Path(".").glob("temp_*.txt"))

    # Cleanup
    path.unlink()
    nested_path.rmdir()
    Path("temp_parent").rmdir()
    dir_path.rmdir()

    return {
        "content": content,
        "name": name,
        "stem": stem,
        "suffix": suffix,
        "exists_before_delete": exists,
        "found_files": [f.name for f in files],
    }


def demonstrate_context_managers() -> dict[str, Any]:
    """Demonstrate context managers for file operations."""
    # Basic context manager
    with open("temp_context.txt", "w") as f:
        f.write("Context manager ensures file is closed")
        is_closed_inside = f.closed

    # File is automatically closed
    is_closed_outside = f.closed

    # Multiple files
    with open("temp_file1.txt", "w") as f1, open("temp_file2.txt", "w") as f2:
        f1.write("File 1")
        f2.write("File 2")

    # Read both files
    with open("temp_file1.txt", "r") as f1, open("temp_file2.txt", "r") as f2:
        content1 = f1.read()
        content2 = f2.read()

    # Cleanup
    os.remove("temp_context.txt")
    os.remove("temp_file1.txt")
    os.remove("temp_file2.txt")

    return {
        "closed_inside": is_closed_inside,
        "closed_outside": is_closed_outside,
        "file1_content": content1,
        "file2_content": content2,
    }


def demonstrate_file_system_operations() -> dict[str, Any]:
    """Demonstrate file system operations."""
    # Create file
    Path("temp_fs.txt").write_text("Test content")

    # Check existence
    exists = os.path.exists("temp_fs.txt")
    is_file = os.path.isfile("temp_fs.txt")
    is_dir = os.path.isdir("temp_fs.txt")

    # File info
    file_size = os.path.getsize("temp_fs.txt")
    modified_time = os.path.getmtime("temp_fs.txt")

    # Rename
    os.rename("temp_fs.txt", "temp_renamed.txt")
    renamed_exists = os.path.exists("temp_renamed.txt")

    # Copy (using pathlib)
    from shutil import copy2
    copy2("temp_renamed.txt", "temp_copy.txt")

    # List directory
    temp_files = [f for f in os.listdir(".") if f.startswith("temp_")]

    # Cleanup
    os.remove("temp_renamed.txt")
    os.remove("temp_copy.txt")

    return {
        "exists": exists,
        "is_file": is_file,
        "is_dir": is_dir,
        "file_size": file_size,
        "renamed_exists": renamed_exists,
        "temp_files_found": len(temp_files),
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 12: File I/O")
    print("=" * 60)

    print("\n1. Basic File Operations:")
    basic = demonstrate_basic_file_operations()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. File Modes:")
    modes = demonstrate_file_modes()
    for key, value in modes.items():
        print(f"   {key}: {value}")

    print("\n3. File Methods:")
    methods = demonstrate_file_methods()
    for key, value in methods.items():
        print(f"   {key}: {value}")

    print("\n4. JSON Operations:")
    json_ops = demonstrate_json_operations()
    for key, value in json_ops.items():
        if key != "json_string":
            print(f"   {key}: {value}")

    print("\n5. CSV Operations:")
    csv_ops = demonstrate_csv_operations()
    for key, value in csv_ops.items():
        print(f"   {key}: {value}")

    print("\n6. Pathlib:")
    pathlib_ops = demonstrate_pathlib()
    for key, value in pathlib_ops.items():
        print(f"   {key}: {value}")

    print("\n7. Context Managers:")
    context = demonstrate_context_managers()
    for key, value in context.items():
        print(f"   {key}: {value}")

    print("\n8. File System Operations:")
    fs_ops = demonstrate_file_system_operations()
    for key, value in fs_ops.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
