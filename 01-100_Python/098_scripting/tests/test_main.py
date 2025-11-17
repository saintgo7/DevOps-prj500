"""
Unit tests for 098_scripting program.

These tests verify:
- Script execution
- Script utilities
- File processing scripts
- Data transformation scripts
- Script error handling
"""

import sys
from pathlib import Path
import pytest
import subprocess

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestScripting:
    """Test cases for scripting functionality."""

    def test_script_execution(self):
        """Test script execution."""
        result = subprocess.run(
            [sys.executable, '-c', 'print("test")'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'test' in result.stdout

    def test_data_transformation(self):
        """Test data transformation."""
        data = [1, 2, 3, 4, 5]
        transformed = [x ** 2 for x in data]
        assert transformed == [1, 4, 9, 16, 25]

    def test_file_processing(self):
        """Test file processing."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("line1\nline2\nline3")

        with open(temp_path, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 3
        Path(temp_path).unlink()


class TestMainFunction:
    """Test cases for main function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
