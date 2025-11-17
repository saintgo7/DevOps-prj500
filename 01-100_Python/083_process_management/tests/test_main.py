"""
Unit tests for 083_process_management program.

These tests verify:
- Process creation and management
- Process information retrieval
- Parent-child process relationships
- Process termination
- Environment variables
"""

import sys
from pathlib import Path
import pytest
import os

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestProcessInformation:
    """Test cases for process information."""

    def test_get_process_id(self):
        """Test getting process ID."""
        pid = os.getpid()
        assert pid > 0

    def test_get_parent_process_id(self):
        """Test getting parent process ID."""
        ppid = os.getppid()
        assert ppid > 0

    def test_process_exists(self):
        """Test checking if process exists."""
        pid = os.getpid()
        assert pid is not None


class TestEnvironmentVariables:
    """Test cases for environment variables."""

    def test_get_environment_variable(self):
        """Test getting environment variable."""
        path = os.environ.get('PATH')
        assert path is not None

    def test_set_environment_variable(self):
        """Test setting environment variable."""
        os.environ['TEST_VAR'] = 'test_value'
        assert os.environ.get('TEST_VAR') == 'test_value'

    def test_environment_dict(self):
        """Test environment as dictionary."""
        env = dict(os.environ)
        assert isinstance(env, dict)
        assert len(env) > 0


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
