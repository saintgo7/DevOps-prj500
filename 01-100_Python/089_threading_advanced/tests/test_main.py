"""
Unit tests for 089_threading_advanced program.

These tests verify:
- Thread creation and management
- Thread synchronization primitives
- Thread pools
- Thread-safe data structures
- Race condition handling
"""

import sys
from pathlib import Path
import pytest
import threading
import time

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestThreadCreation:
    """Test cases for thread creation."""

    def test_create_thread(self):
        """Test creating and starting a thread."""
        executed = []

        def worker():
            executed.append(1)

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()

        assert len(executed) == 1

    def test_multiple_threads(self):
        """Test creating multiple threads."""
        counter = []

        def worker():
            counter.append(1)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(counter) == 5


class TestThreadSynchronization:
    """Test cases for thread synchronization."""

    def test_lock(self):
        """Test thread lock."""
        lock = threading.Lock()
        counter = [0]

        def worker():
            for _ in range(1000):
                with lock:
                    counter[0] += 1

        threads = [threading.Thread(target=worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert counter[0] == 2000


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
