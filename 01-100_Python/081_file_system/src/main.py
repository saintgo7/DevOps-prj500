#!/usr/bin/env python3
"""
Program 81: File System Operations
Demonstrates file operations, directory traversal, and file metadata.
"""

import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import stat


def create_sample_files(base_dir: Path) -> None:
    """Create sample files for demonstration."""
    (base_dir / "file1.txt").write_text("Sample content in file 1")
    (base_dir / "file2.txt").write_text("Sample content in file 2")
    (base_dir / "subdir").mkdir(exist_ok=True)
    (base_dir / "subdir" / "nested.txt").write_text("Nested file content")
    (base_dir / ".hidden").write_text("Hidden file")


def read_file_operations(file_path: Path) -> None:
    """Demonstrate various file reading operations."""
    print("\n" + "=" * 60)
    print("FILE READING OPERATIONS")
    print("=" * 60)

    # Read entire file
    content = file_path.read_text()
    print(f"\n1. Read entire file ({file_path.name}):")
    print(f"   Content: {content[:50]}...")

    # Read with traditional open
    with open(file_path, 'r') as f:
        lines = f.readlines()
    print(f"\n2. Read lines: {len(lines)} lines")

    # Read line by line
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()
    print(f"   First line: {first_line}")

    # Read bytes
    binary_content = file_path.read_bytes()
    print(f"\n3. Read as bytes: {len(binary_content)} bytes")


def write_file_operations(base_dir: Path) -> None:
    """Demonstrate various file writing operations."""
    print("\n" + "=" * 60)
    print("FILE WRITING OPERATIONS")
    print("=" * 60)

    # Write text
    write_file = base_dir / "write_test.txt"
    write_file.write_text("Line 1\nLine 2\nLine 3")
    print(f"\n1. Wrote text file: {write_file.name}")

    # Append to file
    with open(write_file, 'a') as f:
        f.write("\nAppended line 4")
    print("2. Appended to file")

    # Write binary
    binary_file = base_dir / "binary_test.bin"
    binary_file.write_bytes(b'\x00\x01\x02\x03')
    print(f"3. Wrote binary file: {binary_file.name}")


def get_file_metadata(file_path: Path) -> Dict[str, Any]:
    """Get comprehensive file metadata."""
    stats = file_path.stat()

    return {
        'name': file_path.name,
        'size': stats.st_size,
        'mode': oct(stats.st_mode),
        'created': datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'accessed': datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
        'is_file': file_path.is_file(),
        'is_dir': file_path.is_dir(),
        'is_symlink': file_path.is_symlink(),
        'owner': stats.st_uid,
        'group': stats.st_gid,
    }


def display_file_metadata(base_dir: Path) -> None:
    """Display metadata for all files in directory."""
    print("\n" + "=" * 60)
    print("FILE METADATA")
    print("=" * 60)

    for file_path in sorted(base_dir.glob('*')):
        if file_path.is_file():
            metadata = get_file_metadata(file_path)
            print(f"\n{metadata['name']}:")
            print(f"  Size: {metadata['size']} bytes")
            print(f"  Modified: {metadata['modified']}")
            print(f"  Mode: {metadata['mode']}")


def traverse_directory_recursive(directory: Path, max_depth: int = 3) -> List[Path]:
    """Recursively traverse directory and return all files."""
    files = []

    def _traverse(path: Path, depth: int = 0):
        if depth > max_depth:
            return

        try:
            for item in path.iterdir():
                if item.is_file():
                    files.append(item)
                elif item.is_dir() and not item.name.startswith('.'):
                    _traverse(item, depth + 1)
        except PermissionError:
            pass

    _traverse(directory)
    return files


def demonstrate_directory_traversal(base_dir: Path) -> None:
    """Demonstrate different directory traversal methods."""
    print("\n" + "=" * 60)
    print("DIRECTORY TRAVERSAL")
    print("=" * 60)

    # Method 1: os.walk
    print("\n1. Using os.walk():")
    for root, dirs, files in os.walk(base_dir):
        level = root.replace(str(base_dir), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{Path(root).name}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

    # Method 2: Path.rglob
    print("\n2. Using Path.rglob():")
    for item in sorted(base_dir.rglob('*.txt')):
        rel_path = item.relative_to(base_dir)
        print(f"   {rel_path}")

    # Method 3: Custom recursive
    print("\n3. Using custom recursive function:")
    all_files = traverse_directory_recursive(base_dir)
    for file in all_files[:5]:  # Show first 5
        print(f"   {file.name}")


def demonstrate_file_operations(base_dir: Path) -> None:
    """Demonstrate various file operations."""
    print("\n" + "=" * 60)
    print("FILE OPERATIONS")
    print("=" * 60)

    # Copy file
    src_file = base_dir / "file1.txt"
    dst_file = base_dir / "file1_copy.txt"
    shutil.copy2(src_file, dst_file)
    print(f"\n1. Copied: {src_file.name} -> {dst_file.name}")

    # Move/Rename file
    old_name = base_dir / "file1_copy.txt"
    new_name = base_dir / "file1_renamed.txt"
    old_name.rename(new_name)
    print(f"2. Renamed: {old_name.name} -> {new_name.name}")

    # Check file existence
    print(f"\n3. File existence checks:")
    print(f"   {src_file.name} exists: {src_file.exists()}")
    print(f"   nonexistent.txt exists: {(base_dir / 'nonexistent.txt').exists()}")

    # Get file size
    size = src_file.stat().st_size
    print(f"\n4. File size: {src_file.name} = {size} bytes")

    # Change permissions
    test_file = base_dir / "permissions_test.txt"
    test_file.write_text("Test content")
    test_file.chmod(0o644)
    print(f"\n5. Set permissions: {test_file.name} = 0o644")


def demonstrate_directory_operations(base_dir: Path) -> None:
    """Demonstrate directory operations."""
    print("\n" + "=" * 60)
    print("DIRECTORY OPERATIONS")
    print("=" * 60)

    # Create directory
    new_dir = base_dir / "new_directory"
    new_dir.mkdir(exist_ok=True)
    print(f"\n1. Created directory: {new_dir.name}")

    # Create nested directories
    nested_dir = base_dir / "level1" / "level2" / "level3"
    nested_dir.mkdir(parents=True, exist_ok=True)
    print(f"2. Created nested directories: level1/level2/level3")

    # List directory contents
    print(f"\n3. Contents of {base_dir.name}:")
    for item in sorted(base_dir.iterdir()):
        prefix = "📁" if item.is_dir() else "📄"
        print(f"   {prefix} {item.name}")

    # Check if directory is empty
    empty_check = list(new_dir.iterdir())
    print(f"\n4. Is '{new_dir.name}' empty? {len(empty_check) == 0}")

    # Remove directory
    if new_dir.exists():
        new_dir.rmdir()
        print(f"5. Removed directory: {new_dir.name}")


def demonstrate_temp_files() -> None:
    """Demonstrate temporary file operations."""
    print("\n" + "=" * 60)
    print("TEMPORARY FILES")
    print("=" * 60)

    # Temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp:
        temp.write("Temporary content")
        temp_path = temp.name
    print(f"\n1. Created temp file: {temp_path}")
    print(f"   Exists: {os.path.exists(temp_path)}")
    os.unlink(temp_path)

    # Temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n2. Created temp directory: {temp_dir}")
        temp_file = Path(temp_dir) / "test.txt"
        temp_file.write_text("Test")
        print(f"   Created file in temp dir: {temp_file.exists()}")


def demonstrate_safe_operations(base_dir: Path) -> None:
    """Demonstrate safe file operations with error handling."""
    print("\n" + "=" * 60)
    print("SAFE FILE OPERATIONS")
    print("=" * 60)

    # Safe read
    try:
        nonexistent = base_dir / "nonexistent.txt"
        content = nonexistent.read_text()
    except FileNotFoundError:
        print("\n1. ✓ Caught FileNotFoundError for nonexistent file")

    # Safe write with context manager
    try:
        safe_file = base_dir / "safe_write.txt"
        with open(safe_file, 'w') as f:
            f.write("Safely written content")
        print("2. ✓ Safely wrote file with context manager")
    except IOError as e:
        print(f"   Error writing file: {e}")

    # Safe permission check
    try:
        test_file = base_dir / "file1.txt"
        if os.access(test_file, os.R_OK):
            print("3. ✓ File is readable")
        if os.access(test_file, os.W_OK):
            print("   ✓ File is writable")
    except Exception as e:
        print(f"   Error checking permissions: {e}")


def main() -> None:
    """Main function demonstrating file system operations."""
    print("=" * 60)
    print("PYTHON FILE SYSTEM OPERATIONS")
    print("=" * 60)

    # Create temporary workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        print(f"\nWorking directory: {base_dir}")

        # Create sample files
        create_sample_files(base_dir)

        # Demonstrate all operations
        read_file_operations(base_dir / "file1.txt")
        write_file_operations(base_dir)
        display_file_metadata(base_dir)
        demonstrate_directory_traversal(base_dir)
        demonstrate_file_operations(base_dir)
        demonstrate_directory_operations(base_dir)
        demonstrate_temp_files()
        demonstrate_safe_operations(base_dir)

    print("\n" + "=" * 60)
    print("All file system operations completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
