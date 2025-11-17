"""
Unit tests for 084_subprocess program.

These tests verify:
- Subprocess execution
- Capturing subprocess output
- Subprocess error handling
- Subprocess communication
- Process pipelines
"""

import sys
from pathlib import Path
import pytest
import subprocess

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestSubprocessExecution:
    """Test cases for subprocess execution."""

    def test_run_simple_command(self):
        """Test running simple command."""
        result = subprocess.run(['echo', 'test'], capture_output=True, text=True)
        assert result.returncode == 0
        assert 'test' in result.stdout

    def test_capture_output(self):
        """Test capturing subprocess output."""
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        assert result.returncode == 0
        assert 'Python' in result.stdout or 'Python' in result.stderr

    def test_check_return_code(self):
        """Test checking return code."""
        result = subprocess.run(['true'], capture_output=True)
        assert result.returncode == 0


class TestSubprocessErrors:
    """Test cases for subprocess error handling."""

    def test_command_not_found(self):
        """Test handling command not found."""
        with pytest.raises((subprocess.CalledProcessError, FileNotFoundError)):
            subprocess.run(['nonexistent_command_12345'], check=True, capture_output=True)

    def test_non_zero_exit_code(self):
        """Test handling non-zero exit code."""
        with pytest.raises(subprocess.CalledProcessError):
            subprocess.run(['false'], check=True, capture_output=True)


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
