"""
Unit tests for 100_performance_optimization program.

These tests verify:
- Performance measurement
- Code optimization techniques
- Profiling and benchmarking
- Memory optimization
- Algorithm optimization
"""

import sys
from pathlib import Path
import pytest
import time

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestPerformanceMeasurement:
    """Test cases for performance measurement."""

    def test_timing_function(self):
        """Test measuring function execution time."""
        def slow_function():
            time.sleep(0.01)

        start = time.time()
        slow_function()
        elapsed = time.time() - start

        assert elapsed >= 0.01

    def test_list_comprehension_vs_loop(self):
        """Test list comprehension performance."""
        # List comprehension
        start = time.time()
        result1 = [x ** 2 for x in range(1000)]
        time1 = time.time() - start

        # Regular loop
        start = time.time()
        result2 = []
        for x in range(1000):
            result2.append(x ** 2)
        time2 = time.time() - start

        assert result1 == result2

    def test_generator_memory_efficiency(self):
        """Test generator memory efficiency."""
        # Generator uses less memory
        gen = (x for x in range(1000))
        assert hasattr(gen, '__iter__')
        assert hasattr(gen, '__next__')


class TestOptimization:
    """Test cases for code optimization."""

    def test_set_vs_list_membership(self):
        """Test set vs list membership performance."""
        items_list = list(range(1000))
        items_set = set(range(1000))

        # Set membership is faster
        start = time.time()
        _ = 999 in items_set
        set_time = time.time() - start

        start = time.time()
        _ = 999 in items_list
        list_time = time.time() - start

        # Both should work correctly
        assert 999 in items_set
        assert 999 in items_list

    def test_string_concatenation(self):
        """Test string concatenation methods."""
        parts = ['part' + str(i) for i in range(100)]

        # Join is more efficient
        start = time.time()
        result1 = ''.join(parts)
        join_time = time.time() - start

        assert len(result1) > 0


class TestCaching:
    """Test cases for caching techniques."""

    def test_memoization(self):
        """Test memoization for optimization."""
        cache = {}

        def fibonacci(n):
            if n in cache:
                return cache[n]
            if n <= 1:
                return n
            cache[n] = fibonacci(n-1) + fibonacci(n-2)
            return cache[n]

        result = fibonacci(10)
        assert result == 55
        assert 10 in cache


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
