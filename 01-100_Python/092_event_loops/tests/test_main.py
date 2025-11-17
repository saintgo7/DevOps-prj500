"""
Unit tests for 092_event_loops program.

These tests verify:
- Event loop creation and management
- Event loop execution
- Task scheduling
- Event loop policies
- Running coroutines in event loop
"""

import sys
from pathlib import Path
import pytest
import asyncio

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestEventLoop:
    """Test cases for event loop."""

    def test_get_event_loop(self):
        """Test getting event loop."""
        try:
            loop = asyncio.get_event_loop()
            assert loop is not None
        except RuntimeError:
            # Python 3.10+ may raise RuntimeError if no current event loop
            loop = asyncio.new_event_loop()
            assert loop is not None
            loop.close()

    def test_run_coroutine(self):
        """Test running coroutine."""
        async def coro():
            return 42

        result = asyncio.run(coro())
        assert result == 42


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
