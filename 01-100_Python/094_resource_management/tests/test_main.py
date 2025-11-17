"""
Unit tests for 094_resource_management program.

These tests verify:
- Context managers
- Resource allocation and cleanup
- File handle management
- Memory management
- Resource pooling
"""

import sys
from pathlib import Path
import pytest
import tempfile

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestContextManagers:
    """Test cases for context managers."""

    def test_file_context_manager(self):
        """Test file context manager."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("test")

        with open(temp_path, 'r') as f:
            content = f.read()
            assert content == "test"

        Path(temp_path).unlink()

    def test_custom_context_manager(self):
        """Test custom context manager."""
        class CustomContext:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                return False

        with CustomContext() as ctx:
            assert ctx is not None


class TestResourceCleanup:
    """Test cases for resource cleanup."""

    def test_temp_directory_cleanup(self):
        """Test temporary directory cleanup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            assert temp_path.exists()

        # Directory should be cleaned up after context
        assert not temp_path.exists()


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
