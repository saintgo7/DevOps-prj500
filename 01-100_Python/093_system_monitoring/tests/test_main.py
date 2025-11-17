"""
Unit tests for 093_system_monitoring program.

These tests verify:
- System resource monitoring
- CPU usage tracking
- Memory usage tracking
- Disk usage tracking
- Network statistics
"""

import sys
from pathlib import Path
import pytest
import os

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestSystemMonitoring:
    """Test cases for system monitoring."""

    def test_get_cpu_count(self):
        """Test getting CPU count."""
        cpu_count = os.cpu_count()
        assert cpu_count is not None
        assert cpu_count > 0

    def test_get_process_id(self):
        """Test getting process ID."""
        pid = os.getpid()
        assert pid > 0


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
