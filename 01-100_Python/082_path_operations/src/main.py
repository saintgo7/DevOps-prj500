#!/usr/bin/env python3
"""
Program 82: Path Operations
Demonstrates pathlib, path manipulation, and file finding.
"""

from pathlib import Path, PurePath
import os
import glob
import tempfile
from typing import List, Iterator
import fnmatch


def demonstrate_path_creation() -> None:
    """Demonstrate different ways to create paths."""
    print("\n" + "=" * 60)
    print("PATH CREATION")
    print("=" * 60)

    # Create paths
    p1 = Path('/home/user/documents')
    p2 = Path.home() / 'documents'
    p3 = Path('.')  # Current directory
    p4 = Path.cwd()  # Current working directory

    print(f"\n1. Absolute path: {p1}")
    print(f"2. Home-relative path: {p2}")
    print(f"3. Current directory: {p3}")
    print(f"4. Working directory: {p4}")

    # Path from parts
    p5 = Path('home', 'user', 'documents', 'file.txt')
    print(f"\n5. Path from parts: {p5}")

    # Joining paths
    base = Path('/home/user')
    full_path = base / 'documents' / 'file.txt'
    print(f"6. Joined path: {full_path}")


def demonstrate_path_properties() -> None:
    """Demonstrate path properties and attributes."""
    print("\n" + "=" * 60)
    print("PATH PROPERTIES")
    print("=" * 60)

    path = Path('/home/user/documents/project/data/file.tar.gz')

    print(f"\nOriginal path: {path}")
    print(f"\n1. Components:")
    print(f"   name: {path.name}")
    print(f"   stem: {path.stem}")
    print(f"   suffix: {path.suffix}")
    print(f"   suffixes: {path.suffixes}")
    print(f"   parent: {path.parent}")
    print(f"   parents: {list(path.parents)}")
    print(f"   parts: {path.parts}")
    print(f"   anchor: {path.anchor}")

    print(f"\n2. Queries:")
    print(f"   is_absolute: {path.is_absolute()}")
    print(f"   is_relative: {not path.is_absolute()}")

    # Real path properties
    real_path = Path(__file__)
    print(f"\n3. Real file properties ({real_path.name}):")
    print(f"   absolute: {real_path.absolute()}")
    print(f"   exists: {real_path.exists()}")
    print(f"   is_file: {real_path.is_file()}")
    print(f"   is_dir: {real_path.is_dir()}")


def demonstrate_path_manipulation() -> None:
    """Demonstrate path manipulation operations."""
    print("\n" + "=" * 60)
    print("PATH MANIPULATION")
    print("=" * 60)

    path = Path('/home/user/documents/file.txt')

    print(f"\nOriginal: {path}")

    # Change name
    new_name = path.with_name('newfile.txt')
    print(f"\n1. with_name: {new_name}")

    # Change suffix
    new_suffix = path.with_suffix('.md')
    print(f"2. with_suffix: {new_suffix}")

    # Change stem
    new_stem = path.with_stem('newfile')
    print(f"3. with_stem: {new_stem}")

    # Join paths
    joined = path.parent / 'subfolder' / 'newfile.txt'
    print(f"4. Joined: {joined}")

    # Relative paths
    base = Path('/home/user')
    relative = Path('/home/user/documents/project/file.txt')
    try:
        rel_to = relative.relative_to(base)
        print(f"\n5. Relative to {base}: {rel_to}")
    except ValueError:
        print("   Path is not relative to base")


def demonstrate_path_resolution() -> None:
    """Demonstrate path resolution and normalization."""
    print("\n" + "=" * 60)
    print("PATH RESOLUTION")
    print("=" * 60)

    # Resolve dots
    path1 = Path('./documents/../documents/./file.txt')
    print(f"\n1. Original: {path1}")
    print(f"   Resolved: {path1.resolve()}")

    # Absolute vs relative
    path2 = Path('relative/path/file.txt')
    print(f"\n2. Relative: {path2}")
    print(f"   Absolute: {path2.absolute()}")

    # Expanduser
    path3 = Path('~/documents/file.txt')
    print(f"\n3. With tilde: {path3}")
    print(f"   Expanded: {path3.expanduser()}")

    # Normalize path
    path4 = Path('/home//user/./documents/../documents/file.txt')
    print(f"\n4. Messy path: {path4}")
    print(f"   Normalized: {Path(os.path.normpath(path4))}")


def find_files_by_pattern(base_dir: Path, pattern: str) -> List[Path]:
    """Find files matching a pattern."""
    return list(base_dir.rglob(pattern))


def demonstrate_file_finding(base_dir: Path) -> None:
    """Demonstrate different file finding methods."""
    print("\n" + "=" * 60)
    print("FILE FINDING")
    print("=" * 60)

    # Create sample structure
    (base_dir / 'documents').mkdir()
    (base_dir / 'documents' / 'report.txt').write_text("Report")
    (base_dir / 'documents' / 'data.csv').write_text("Data")
    (base_dir / 'scripts').mkdir()
    (base_dir / 'scripts' / 'script.py').write_text("# Script")
    (base_dir / 'scripts' / 'config.json').write_text("{}")

    # Method 1: glob
    print("\n1. Using glob (*.txt):")
    for path in base_dir.glob('**/*.txt'):
        print(f"   {path.relative_to(base_dir)}")

    # Method 2: rglob (recursive)
    print("\n2. Using rglob (*.py):")
    for path in base_dir.rglob('*.py'):
        print(f"   {path.relative_to(base_dir)}")

    # Method 3: iterdir with filtering
    print("\n3. Using iterdir with filter:")
    for path in base_dir.rglob('*'):
        if path.is_file() and path.suffix in ['.json', '.csv']:
            print(f"   {path.relative_to(base_dir)}")

    # Method 4: fnmatch
    print("\n4. Using fnmatch (*.{txt,py}):")
    for path in base_dir.rglob('*'):
        if fnmatch.fnmatch(path.name, '*.txt') or fnmatch.fnmatch(path.name, '*.py'):
            print(f"   {path.relative_to(base_dir)}")


def demonstrate_path_comparison() -> None:
    """Demonstrate path comparison operations."""
    print("\n" + "=" * 60)
    print("PATH COMPARISON")
    print("=" * 60)

    path1 = Path('/home/user/documents')
    path2 = Path('/home/user/documents')
    path3 = Path('/home/user/Downloads')

    print(f"\npath1: {path1}")
    print(f"path2: {path2}")
    print(f"path3: {path3}")

    print(f"\n1. Equality:")
    print(f"   path1 == path2: {path1 == path2}")
    print(f"   path1 == path3: {path1 == path3}")

    print(f"\n2. String comparison:")
    print(f"   str(path1) == str(path2): {str(path1) == str(path2)}")

    print(f"\n3. Samefile (for existing files):")
    print("   (Only works for existing files)")


def demonstrate_path_traversal(base_dir: Path) -> None:
    """Demonstrate directory traversal with paths."""
    print("\n" + "=" * 60)
    print("PATH TRAVERSAL")
    print("=" * 60)

    # Create nested structure
    (base_dir / 'level1').mkdir()
    (base_dir / 'level1' / 'level2').mkdir()
    (base_dir / 'level1' / 'level2' / 'file.txt').write_text("Deep file")
    (base_dir / 'level1' / 'file1.txt').write_text("File 1")

    print(f"\n1. Iterating directory:")
    for item in sorted(base_dir.rglob('*')):
        if item.is_file():
            indent = '  ' * (len(item.relative_to(base_dir).parts) - 1)
            print(f"   {indent}{item.name}")

    print(f"\n2. Walking up the tree:")
    deep_file = base_dir / 'level1' / 'level2' / 'file.txt'
    current = deep_file
    while current != base_dir:
        print(f"   {current.name}")
        current = current.parent
    print(f"   {current.name}")


def demonstrate_pure_paths() -> None:
    """Demonstrate PurePath for path manipulation without filesystem access."""
    print("\n" + "=" * 60)
    print("PURE PATHS (No Filesystem Access)")
    print("=" * 60)

    # Pure paths don't access filesystem
    pure = PurePath('/home/user/documents/file.txt')

    print(f"\n1. PurePath properties:")
    print(f"   path: {pure}")
    print(f"   name: {pure.name}")
    print(f"   parent: {pure.parent}")
    print(f"   suffix: {pure.suffix}")

    # Platform-specific pure paths
    from pathlib import PurePosixPath, PureWindowsPath

    posix = PurePosixPath('/home/user/file.txt')
    windows = PureWindowsPath('C:/Users/user/file.txt')

    print(f"\n2. Platform-specific:")
    print(f"   POSIX: {posix}")
    print(f"   Windows: {windows}")

    # Path manipulation without filesystem
    new_path = pure.with_suffix('.md')
    print(f"\n3. Manipulation without filesystem:")
    print(f"   Original: {pure}")
    print(f"   Modified: {new_path}")


def demonstrate_advanced_patterns(base_dir: Path) -> None:
    """Demonstrate advanced path patterns and operations."""
    print("\n" + "=" * 60)
    print("ADVANCED PATH PATTERNS")
    print("=" * 60)

    # Create test files
    for i in range(3):
        (base_dir / f'file{i}.txt').write_text(f"Content {i}")
        (base_dir / f'data{i}.csv').write_text(f"Data {i}")

    # Pattern matching
    print("\n1. Multiple patterns:")
    patterns = ['*.txt', '*.csv']
    for pattern in patterns:
        files = list(base_dir.glob(pattern))
        print(f"   {pattern}: {len(files)} files")

    # Complex glob patterns
    print("\n2. Complex patterns:")
    (base_dir / 'test_file.txt').write_text("Test")
    (base_dir / 'test_data.txt').write_text("Test data")

    for path in base_dir.glob('test_*.txt'):
        print(f"   {path.name}")

    # Exclude patterns
    print("\n3. Filtered results:")
    all_files = list(base_dir.glob('*.txt'))
    filtered = [f for f in all_files if not f.name.startswith('test_')]
    print(f"   All .txt files: {len(all_files)}")
    print(f"   Filtered (no test_*): {len(filtered)}")


def demonstrate_path_utilities(base_dir: Path) -> None:
    """Demonstrate useful path utility functions."""
    print("\n" + "=" * 60)
    print("PATH UTILITIES")
    print("=" * 60)

    test_file = base_dir / 'test.txt'
    test_file.write_text("Test content")

    # File size
    size = test_file.stat().st_size
    print(f"\n1. File size: {size} bytes")

    # Extension checking
    extensions = ['.txt', '.py', '.md']
    print(f"\n2. Extension checking:")
    for ext in extensions:
        has_ext = test_file.suffix == ext
        print(f"   Has {ext}: {has_ext}")

    # Path building helper
    def build_path(*parts: str) -> Path:
        """Build path from parts safely."""
        return Path(*parts)

    built = build_path('home', 'user', 'documents', 'file.txt')
    print(f"\n3. Built path: {built}")

    # Safe path operations
    def safe_read(path: Path) -> str:
        """Safely read file with error handling."""
        try:
            return path.read_text()
        except FileNotFoundError:
            return ""
        except PermissionError:
            return ""

    content = safe_read(test_file)
    print(f"\n4. Safe read: {'Success' if content else 'Failed'}")


def main() -> None:
    """Main function demonstrating path operations."""
    print("=" * 60)
    print("PYTHON PATH OPERATIONS")
    print("=" * 60)

    # Path basics
    demonstrate_path_creation()
    demonstrate_path_properties()
    demonstrate_path_manipulation()
    demonstrate_path_resolution()
    demonstrate_pure_paths()
    demonstrate_path_comparison()

    # File finding operations
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        print(f"\nWorking directory: {base_dir}")

        demonstrate_file_finding(base_dir)
        demonstrate_path_traversal(base_dir)
        demonstrate_advanced_patterns(base_dir)
        demonstrate_path_utilities(base_dir)

    print("\n" + "=" * 60)
    print("All path operations completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
