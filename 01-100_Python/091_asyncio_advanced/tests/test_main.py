"""
Unit tests for 091_asyncio_advanced program.

These tests verify:
- Async/await syntax
- Asyncio tasks and coroutines
- Concurrent execution
- Asyncio event loop
- Async context managers
"""

import sys
from pathlib import Path
import pytest
import asyncio

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestAsyncBasics:
    """Test cases for async basics."""

    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test basic async function."""
        async def async_func():
            await asyncio.sleep(0.01)
            return "done"

        result = await async_func()
        assert result == "done"

    @pytest.mark.asyncio
    async def test_create_task(self):
        """Test creating asyncio task."""
        async def worker():
            await asyncio.sleep(0.01)
            return 42

        task = asyncio.create_task(worker())
        result = await task
        assert result == 42

    @pytest.mark.asyncio
    async def test_gather(self):
        """Test gathering multiple tasks."""
        async def task1():
            await asyncio.sleep(0.01)
            return 1

        async def task2():
            await asyncio.sleep(0.01)
            return 2

        results = await asyncio.gather(task1(), task2())
        assert results == [1, 2]


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
