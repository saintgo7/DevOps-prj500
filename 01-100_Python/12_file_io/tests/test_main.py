"""
Unit tests for 12_file_io program.

These tests verify:
- Basic file operations (read, write, append)
- File modes
- File methods
- JSON operations
- CSV operations
- Pathlib operations
- Context managers
- File system operations
- Edge cases
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_file_operations,
    demonstrate_file_modes,
    demonstrate_file_methods,
    demonstrate_json_operations,
    demonstrate_csv_operations,
    demonstrate_pathlib,
    demonstrate_context_managers,
    demonstrate_file_system_operations,
    main,
)


class TestBasicFileOperations:
    """Test cases for demonstrate_basic_file_operations()."""

    def test_basic_operations_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_file_operations()
        assert isinstance(result, dict)

    def test_initial_content(self):
        """Test initial file content."""
        result = demonstrate_basic_file_operations()
        assert "Hello, World!" in result["initial_content"]

    def test_lines_read(self):
        """Test reading lines."""
        result = demonstrate_basic_file_operations()
        assert len(result["lines"]) >= 2

    def test_line_by_line_reading(self):
        """Test line by line reading."""
        result = demonstrate_basic_file_operations()
        assert isinstance(result["line_by_line"], list)

    def test_append_operation(self):
        """Test append operation."""
        result = demonstrate_basic_file_operations()
        assert "Appended line" in result["after_append"]


class TestFileModes:
    """Test cases for demonstrate_file_modes()."""

    def test_write_mode(self):
        """Test write mode."""
        result = demonstrate_file_modes()
        assert result["write_mode"] == "Write mode"

    def test_append_mode(self):
        """Test append mode."""
        result = demonstrate_file_modes()
        assert "Append mode" in result["after_append"]

    def test_write_plus_mode(self):
        """Test write+ mode."""
        result = demonstrate_file_modes()
        assert result["write_plus"] == "Write+ mode"

    def test_binary_mode(self):
        """Test binary mode."""
        result = demonstrate_file_modes()
        assert isinstance(result["binary"], bytes)
        assert result["binary"] == b"Binary data"


class TestFileMethods:
    """Test cases for demonstrate_file_methods()."""

    def test_read_chunks(self):
        """Test reading in chunks."""
        result = demonstrate_file_methods()
        assert len(result["chunk1"]) == 10
        assert len(result["chunk2"]) == 10

    def test_tell_position(self):
        """Test tell() method."""
        result = demonstrate_file_methods()
        assert result["position_after_chunks"] == 20

    def test_readline(self):
        """Test readline() method."""
        result = demonstrate_file_methods()
        assert result["readline1"] == "Line 1"
        assert result["readline2"] == "Line 2"

    def test_file_size(self):
        """Test getting file size."""
        result = demonstrate_file_methods()
        assert result["file_size"] > 0

    def test_writelines(self):
        """Test writelines() method."""
        result = demonstrate_file_methods()
        assert "First" in result["writelines"]
        assert "Second" in result["writelines"]


class TestJsonOperations:
    """Test cases for demonstrate_json_operations()."""

    def test_json_dump_load(self):
        """Test JSON dump and load."""
        result = demonstrate_json_operations()
        assert result["loaded_equal"] is True

    def test_json_strings(self):
        """Test JSON string operations."""
        result = demonstrate_json_operations()
        assert result["parsed_equal"] is True

    def test_json_structure(self):
        """Test JSON data structure."""
        result = demonstrate_json_operations()
        original = result["original"]
        assert original["name"] == "Alice"
        assert original["age"] == 25


class TestCsvOperations:
    """Test cases for demonstrate_csv_operations()."""

    def test_csv_write_read(self):
        """Test CSV write and read."""
        result = demonstrate_csv_operations()
        written = result["written_rows"]
        read_data = result["read_rows"]
        assert len(read_data) == len(written)

    def test_dict_writer_reader(self):
        """Test DictWriter and DictReader."""
        result = demonstrate_csv_operations()
        dict_data = result["dict_data"]
        read_dict = result["read_dict_data"]
        assert len(dict_data) == len(read_dict)
        assert read_dict[0]["name"] == "Alice"


class TestPathlib:
    """Test cases for demonstrate_pathlib()."""

    def test_pathlib_write_read(self):
        """Test pathlib write and read."""
        result = demonstrate_pathlib()
        assert result["content"] == "Hello from pathlib!"

    def test_path_properties(self):
        """Test path properties."""
        result = demonstrate_pathlib()
        assert result["name"] == "temp_pathlib.txt"
        assert result["stem"] == "temp_pathlib"
        assert result["suffix"] == ".txt"


class TestContextManagers:
    """Test cases for demonstrate_context_managers()."""

    def test_file_auto_close(self):
        """Test automatic file closing."""
        result = demonstrate_context_managers()
        assert result["closed_inside"] is False
        assert result["closed_outside"] is True

    def test_multiple_files(self):
        """Test multiple files context."""
        result = demonstrate_context_managers()
        assert result["file1_content"] == "File 1"
        assert result["file2_content"] == "File 2"


class TestFileSystemOperations:
    """Test cases for demonstrate_file_system_operations()."""

    def test_existence_checks(self):
        """Test file existence checks."""
        result = demonstrate_file_system_operations()
        assert result["exists"] is True
        assert result["is_file"] is True
        assert result["is_dir"] is False

    def test_file_size(self):
        """Test file size retrieval."""
        result = demonstrate_file_system_operations()
        assert result["file_size"] > 0

    def test_rename_operation(self):
        """Test file rename."""
        result = demonstrate_file_system_operations()
        assert result["renamed_exists"] is True


class TestMainFunction:
    """Test cases for the main() function."""

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

        assert "Program 12: File I/O" in captured.out
        assert "Basic File Operations:" in captured.out
        assert "JSON Operations:" in captured.out


class TestIntegration:
    """Integration tests for file I/O operations."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_basic_file_operations,
            demonstrate_file_modes,
            demonstrate_file_methods,
            demonstrate_json_operations,
            demonstrate_csv_operations,
            demonstrate_pathlib,
            demonstrate_context_managers,
            demonstrate_file_system_operations,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_json_special_characters(self):
        """Test JSON with special characters."""
        import json
        data = {"special": "Hello\nWorld\t!"}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        assert parsed == data

    def test_pathlib_absolute_path(self):
        """Test pathlib absolute path."""
        path = Path("test.txt")
        absolute = path.absolute()
        assert absolute.is_absolute()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
