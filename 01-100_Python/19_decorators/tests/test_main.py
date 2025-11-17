"""
Unit tests for 19_decorators program.

These tests verify:
- Basic decorators
- Decorators with arguments
- functools.wraps
- Timing decorators
- Caching decorators
- Validation decorators
- Multiple decorators
- Class decorators
- Property decorators
- Static and class methods
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_decorator,
    demonstrate_decorator_with_arguments,
    demonstrate_functools_wraps,
    demonstrate_timing_decorator,
    demonstrate_caching_decorator,
    demonstrate_validation_decorator,
    demonstrate_multiple_decorators,
    demonstrate_class_decorator,
    demonstrate_property_decorator,
    demonstrate_staticmethod_classmethod,
    main,
)


class TestBasicDecorator:
    """Test cases for demonstrate_basic_decorator()."""

    def test_decorator_result(self):
        """Test basic decorator result."""
        result = demonstrate_basic_decorator()
        assert result["decorated_result"] == "Hello, Alice!"


class TestDecoratorWithArguments:
    """Test cases for demonstrate_decorator_with_arguments()."""

    def test_repeat_count(self):
        """Test repeat decorator."""
        result = demonstrate_decorator_with_arguments()
        assert result["count"] == 3
        assert len(result["repeat_3_times"]) == 3
        assert all(r == "Hello!" for r in result["repeat_3_times"])


class TestFunctoolsWraps:
    """Test cases for demonstrate_functools_wraps()."""

    def test_bad_decorator_metadata(self):
        """Test decorator without @wraps."""
        result = demonstrate_functools_wraps()
        assert result["bad_func_name"] == "wrapper"

    def test_good_decorator_metadata(self):
        """Test decorator with @wraps."""
        result = demonstrate_functools_wraps()
        assert result["good_func_name"] == "good_func"
        assert "Original docstring" in result["good_func_doc"]


class TestTimingDecorator:
    """Test cases for demonstrate_timing_decorator()."""

    def test_timing_result(self):
        """Test timing decorator result."""
        result = demonstrate_timing_decorator()
        assert result["result"] == 42


class TestCachingDecorator:
    """Test cases for demonstrate_caching_decorator()."""

    def test_manual_cache(self):
        """Test manual cache decorator."""
        result = demonstrate_caching_decorator()
        assert result["manual_cache_result"] == 55
        assert result["manual_cache_size"] >= 1

    def test_lru_cache(self):
        """Test LRU cache."""
        result = demonstrate_caching_decorator()
        assert result["lru_cache_result"] == 55
        assert result["lru_hits"] >= 0
        assert result["lru_misses"] >= 0


class TestValidationDecorator:
    """Test cases for demonstrate_validation_decorator()."""

    def test_valid_input(self):
        """Test validation with valid input."""
        result = demonstrate_validation_decorator()
        assert result["valid_result"] == 5.0

    def test_invalid_input(self):
        """Test validation with invalid input."""
        result = demonstrate_validation_decorator()
        assert result["validation_works"] is True


class TestMultipleDecorators:
    """Test cases for demonstrate_multiple_decorators()."""

    def test_stacked_decorators(self):
        """Test stacked decorators."""
        result = demonstrate_multiple_decorators()
        assert result["result"] == "HELLO ALICE!!!"


class TestClassDecorator:
    """Test cases for demonstrate_class_decorator()."""

    def test_call_counting(self):
        """Test class-based decorator counting."""
        result = demonstrate_class_decorator()
        assert result["call_count"] == 3
        assert result["final_count"] == 4


class TestPropertyDecorator:
    """Test cases for demonstrate_property_decorator()."""

    def test_initial_area(self):
        """Test initial area calculation."""
        result = demonstrate_property_decorator()
        assert "78.5" in result["initial_area"]

    def test_area_after_radius_change(self):
        """Test area after radius change."""
        result = demonstrate_property_decorator()
        assert "314.1" in result["new_area"]

    def test_diameter_property(self):
        """Test diameter property."""
        result = demonstrate_property_decorator()
        assert result["diameter_radius"] == 10.0


class TestStaticmethodClassmethod:
    """Test cases for demonstrate_staticmethod_classmethod()."""

    def test_static_method(self):
        """Test static method."""
        result = demonstrate_staticmethod_classmethod()
        assert result["static_method"] == 8

    def test_class_method(self):
        """Test class method."""
        result = demonstrate_staticmethod_classmethod()
        assert "MathOps" in result["class_method"]
        assert "10" in result["class_method"]

    def test_factory_method(self):
        """Test factory class method."""
        result = demonstrate_staticmethod_classmethod()
        assert "Calculator" in result["factory_instance"]


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

        assert "Program 19: Decorators" in captured.out


class TestIntegration:
    """Integration tests for decorators."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_basic_decorator,
            demonstrate_decorator_with_arguments,
            demonstrate_functools_wraps,
            demonstrate_timing_decorator,
            demonstrate_caching_decorator,
            demonstrate_validation_decorator,
            demonstrate_multiple_decorators,
            demonstrate_class_decorator,
            demonstrate_property_decorator,
            demonstrate_staticmethod_classmethod,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
