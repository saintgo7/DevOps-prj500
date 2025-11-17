"""
Unit tests for 20_generators program.

These tests verify:
- Basic generators
- Yield vs return
- Generator expressions
- Infinite generators
- Generator pipelines
- send() method
- close() method
- Generator delegation (yield from)
- Practical generators
- Memory efficiency
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_generator,
    demonstrate_yield_vs_return,
    demonstrate_generator_expressions,
    demonstrate_infinite_generators,
    demonstrate_generator_pipeline,
    demonstrate_send_method,
    demonstrate_generator_close,
    demonstrate_generator_delegation,
    demonstrate_practical_generators,
    demonstrate_memory_efficiency,
    main,
)


class TestBasicGenerator:
    """Test cases for demonstrate_basic_generator()."""

    def test_generator_output(self):
        """Test basic generator output."""
        result = demonstrate_basic_generator()
        assert result["numbers"] == [1, 2, 3, 4, 5]

    def test_generator_exhaustion(self):
        """Test generator exhaustion."""
        result = demonstrate_basic_generator()
        assert result["after_exhausted"] == []


class TestYieldVsReturn:
    """Test cases for demonstrate_yield_vs_return()."""

    def test_list_vs_generator(self):
        """Test list vs generator results."""
        result = demonstrate_yield_vs_return()
        assert result["list_result"] == result["generator_result"]
        assert result["are_equal"] is True


class TestGeneratorExpressions:
    """Test cases for demonstrate_generator_expressions()."""

    def test_list_comprehension(self):
        """Test list comprehension."""
        result = demonstrate_generator_expressions()
        assert result["list_comp"] == result["gen_exp"]

    def test_first_five(self):
        """Test first five from large generator."""
        result = demonstrate_generator_expressions()
        assert result["first_five_large"] == [0, 1, 2, 3, 4]

    def test_chained_generators(self):
        """Test chained generators."""
        result = demonstrate_generator_expressions()
        assert all(x % 2 == 0 for x in result["chained_result"])


class TestInfiniteGenerators:
    """Test cases for demonstrate_infinite_generators()."""

    def test_counter(self):
        """Test infinite counter."""
        result = demonstrate_infinite_generators()
        assert result["counter"] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_fibonacci(self):
        """Test infinite fibonacci."""
        result = demonstrate_infinite_generators()
        assert result["fibonacci"] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


class TestGeneratorPipeline:
    """Test cases for demonstrate_generator_pipeline()."""

    def test_pipeline_result(self):
        """Test generator pipeline."""
        result = demonstrate_generator_pipeline()
        assert len(result["result"]) == 5
        # Should be squares of even numbers
        assert all(x % 4 == 0 for x in result["result"])


class TestSendMethod:
    """Test cases for demonstrate_send_method()."""

    def test_running_average(self):
        """Test running average with send()."""
        result = demonstrate_send_method()
        assert result["after_10"] == 10.0
        assert result["after_20"] == 15.0
        assert result["after_30"] == 20.0


class TestGeneratorClose:
    """Test cases for demonstrate_generator_close()."""

    def test_items_retrieved(self):
        """Test items retrieved before close."""
        result = demonstrate_generator_close()
        assert len(result["items_retrieved"]) == 2

    def test_close_properly(self):
        """Test generator closes properly."""
        result = demonstrate_generator_close()
        assert result["closed_properly"] is True


class TestGeneratorDelegation:
    """Test cases for demonstrate_generator_delegation()."""

    def test_yield_from(self):
        """Test yield from delegation."""
        result = demonstrate_generator_delegation()
        assert result["old_style"] == result["new_style"]
        assert result["are_equal"] is True


class TestPracticalGenerators:
    """Test cases for demonstrate_practical_generators()."""

    def test_batching(self):
        """Test batch processing."""
        result = demonstrate_practical_generators()
        assert result["batch_count"] == 4
        assert len(result["batches"][0]) == 5

    def test_tree_traversal(self):
        """Test tree traversal."""
        result = demonstrate_practical_generators()
        assert result["tree_traversal"] == [1, 2, 4, 5, 3]


class TestMemoryEfficiency:
    """Test cases for demonstrate_memory_efficiency()."""

    def test_memory_savings(self):
        """Test memory efficiency."""
        result = demonstrate_memory_efficiency()
        assert result["gen_size_bytes"] < result["list_size_bytes"]
        assert result["memory_saved"] > 0

    def test_sums_equal(self):
        """Test that sums are equal."""
        result = demonstrate_memory_efficiency()
        assert result["sums_equal"] is True


class TestMainFunction:
    """Test cases for the main() function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    def test_main_output(self, capsys):
        """Test that main produces expected output."""
        main()
        captured = capsys.readouterr()

        assert "Program 20: Generators" in captured.out


class TestIntegration:
    """Integration tests for generators."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_basic_generator,
            demonstrate_yield_vs_return,
            demonstrate_generator_expressions,
            demonstrate_infinite_generators,
            demonstrate_generator_pipeline,
            demonstrate_send_method,
            demonstrate_generator_close,
            demonstrate_generator_delegation,
            demonstrate_practical_generators,
            demonstrate_memory_efficiency,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
