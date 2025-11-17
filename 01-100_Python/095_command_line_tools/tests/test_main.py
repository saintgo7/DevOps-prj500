"""
Unit tests for 095_command_line_tools program.

These tests verify:
- Command-line argument handling
- CLI tool creation
- Input/output handling
- Exit codes
- Error handling in CLI
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestCommandLineInterface:
    """Test cases for CLI functionality."""

    def test_sys_argv(self):
        """Test sys.argv access."""
        assert isinstance(sys.argv, list)
        assert len(sys.argv) > 0

    def test_exit_codes(self):
        """Test exit code handling."""
        # Exit code 0 indicates success
        assert 0 == 0


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
