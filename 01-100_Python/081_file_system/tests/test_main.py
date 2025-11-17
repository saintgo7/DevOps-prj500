"""
Unit tests for 081_file_system program.

These tests verify:
- File reading and writing operations
- Directory operations and traversal
- File metadata retrieval
- Temporary file/directory handling
- Safe file operations with error handling
"""

import sys
from pathlib import Path
import tempfile
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    create_sample_files,
    get_file_metadata,
    traverse_directory_recursive,
    main,
)


class TestFileOperations:
    """Test cases for file operations."""

    def test_create_sample_files(self):
        """Test creating sample files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            create_sample_files(base_dir)

            assert (base_dir / "file1.txt").exists()
            assert (base_dir / "file2.txt").exists()
            assert (base_dir / "subdir").exists()
            assert (base_dir / "subdir" / "nested.txt").exists()
            assert (base_dir / ".hidden").exists()

    def test_read_write_text_file(self):
        """Test reading and writing text files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.txt"
            content = "Test content\nLine 2"

            test_file.write_text(content)
            read_content = test_file.read_text()

            assert read_content == content

    def test_read_write_binary_file(self):
        """Test reading and writing binary files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.bin"
            binary_data = b'\x00\x01\x02\x03\xFF'

            test_file.write_bytes(binary_data)
            read_data = test_file.read_bytes()

            assert read_data == binary_data

    def test_append_to_file(self):
        """Test appending to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "append_test.txt"
            test_file.write_text("Line 1\n")

            with open(test_file, 'a') as f:
                f.write("Line 2\n")

            content = test_file.read_text()
            assert "Line 1" in content
            assert "Line 2" in content


class TestFileMetadata:
    """Test cases for file metadata operations."""

    def test_get_file_metadata(self):
        """Test retrieving file metadata."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "metadata_test.txt"
            test_file.write_text("Test content")

            metadata = get_file_metadata(test_file)

            assert metadata['name'] == 'metadata_test.txt'
            assert metadata['size'] > 0
            assert metadata['is_file'] is True
            assert metadata['is_dir'] is False
            assert 'created' in metadata
            assert 'modified' in metadata

    def test_file_stat_properties(self):
        """Test file stat properties."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "stat_test.txt"
            test_file.write_text("Content")

            stats = test_file.stat()

            assert stats.st_size > 0
            assert stats.st_mode > 0
            assert stats.st_mtime > 0


class TestDirectoryOperations:
    """Test cases for directory operations."""

    def test_create_directory(self):
        """Test creating directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            new_dir = base_dir / "new_directory"

            new_dir.mkdir()

            assert new_dir.exists()
            assert new_dir.is_dir()

    def test_create_nested_directories(self):
        """Test creating nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            nested_dir = base_dir / "level1" / "level2" / "level3"

            nested_dir.mkdir(parents=True)

            assert nested_dir.exists()
            assert nested_dir.is_dir()

    def test_list_directory_contents(self):
        """Test listing directory contents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / "file1.txt").write_text("File 1")
            (base_dir / "file2.txt").write_text("File 2")
            (base_dir / "subdir").mkdir()

            contents = list(base_dir.iterdir())

            assert len(contents) == 3

    def test_remove_empty_directory(self):
        """Test removing empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            test_dir = base_dir / "to_remove"
            test_dir.mkdir()

            test_dir.rmdir()

            assert not test_dir.exists()


class TestDirectoryTraversal:
    """Test cases for directory traversal."""

    def test_traverse_directory_recursive(self):
        """Test recursive directory traversal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            create_sample_files(base_dir)

            files = traverse_directory_recursive(base_dir)

            assert len(files) > 0
            assert all(f.is_file() for f in files)

    def test_glob_pattern_matching(self):
        """Test glob pattern matching."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / "file1.txt").write_text("Text")
            (base_dir / "file2.py").write_text("Python")
            (base_dir / "file3.txt").write_text("Text")

            txt_files = list(base_dir.glob("*.txt"))

            assert len(txt_files) == 2

    def test_rglob_recursive_pattern(self):
        """Test recursive glob pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / "file1.txt").write_text("Text")
            (base_dir / "subdir").mkdir()
            (base_dir / "subdir" / "file2.txt").write_text("Text")

            txt_files = list(base_dir.rglob("*.txt"))

            assert len(txt_files) == 2


class TestFileExistence:
    """Test cases for file existence checks."""

    def test_file_exists(self):
        """Test checking if file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            existing_file = Path(temp_dir) / "exists.txt"
            existing_file.write_text("Content")

            assert existing_file.exists()

    def test_file_not_exists(self):
        """Test checking if file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existing = Path(temp_dir) / "nonexistent.txt"

            assert not non_existing.exists()

    def test_is_file_vs_is_dir(self):
        """Test distinguishing between files and directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            test_file = base_dir / "file.txt"
            test_dir = base_dir / "directory"

            test_file.write_text("Content")
            test_dir.mkdir()

            assert test_file.is_file() and not test_file.is_dir()
            assert test_dir.is_dir() and not test_dir.is_file()


class TestFileCopyMove:
    """Test cases for file copy and move operations."""

    def test_copy_file(self):
        """Test copying files."""
        import shutil
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            src = base_dir / "source.txt"
            dst = base_dir / "destination.txt"

            src.write_text("Content")
            shutil.copy2(src, dst)

            assert dst.exists()
            assert src.read_text() == dst.read_text()

    def test_rename_file(self):
        """Test renaming files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            old_name = base_dir / "old.txt"
            new_name = base_dir / "new.txt"

            old_name.write_text("Content")
            old_name.rename(new_name)

            assert new_name.exists()
            assert not old_name.exists()


class TestErrorHandling:
    """Test cases for error handling."""

    def test_read_nonexistent_file(self):
        """Test reading non-existent file raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent = Path(temp_dir) / "nonexistent.txt"

            with pytest.raises(FileNotFoundError):
                nonexistent.read_text()

    def test_mkdir_existing_directory(self):
        """Test mkdir on existing directory with exist_ok."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "existing"
            test_dir.mkdir()

            # Should not raise error with exist_ok=True
            test_dir.mkdir(exist_ok=True)

            assert test_dir.exists()


class TestMainFunction:
    """Test cases for main function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    def test_main_output(self, capsys):
        """Test that main produces expected output."""
        main()
        captured = capsys.readouterr()

        assert "FILE SYSTEM OPERATIONS" in captured.out
        assert "FILE READING OPERATIONS" in captured.out
        assert "DIRECTORY OPERATIONS" in captured.out


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
