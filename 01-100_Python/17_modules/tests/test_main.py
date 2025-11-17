"""
Unit tests for 17_modules program.

These tests verify:
- Standard library usage
- Import styles
- Module attributes
- Collections module
- Itertools module
- Pathlib module
- Functools module
- OS and sys modules
- JSON module
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_standard_library,
    demonstrate_import_styles,
    demonstrate_module_attributes,
    demonstrate_collections,
    demonstrate_itertools,
    demonstrate_pathlib_module,
    demonstrate_functools,
    demonstrate_os_sys,
    demonstrate_json_module,
    main,
)


class TestStandardLibrary:
    """Test cases for demonstrate_standard_library()."""

    def test_math_operations(self):
        """Test math module operations."""
        result = demonstrate_standard_library()
        math_results = result["math"]
        assert math_results["pi"] > 3.14
        assert math_results["sqrt_16"] == 4.0

    def test_random_operations(self):
        """Test random module operations."""
        result = demonstrate_standard_library()
        random_results = result["random"]
        assert isinstance(random_results["randint"], int)

    def test_datetime_operations(self):
        """Test datetime module operations."""
        result = demonstrate_standard_library()
        datetime_results = result["datetime"]
        assert datetime_results["current_year"] >= 2024


class TestImportStyles:
    """Test cases for demonstrate_import_styles()."""

    def test_standard_import(self):
        """Test standard import."""
        result = demonstrate_import_styles()
        assert len(result["lowercase"]) == 5

    def test_from_import(self):
        """Test from import."""
        result = demonstrate_import_styles()
        assert len(result["uppercase"]) == 5

    def test_import_as(self):
        """Test import as."""
        result = demonstrate_import_styles()
        assert result["mean"] == 3.0

    def test_multiple_imports(self):
        """Test multiple imports."""
        result = demonstrate_import_styles()
        assert result["add"] == 8
        assert result["multiply"] == 15


class TestModuleAttributes:
    """Test cases for demonstrate_module_attributes()."""

    def test_module_name(self):
        """Test module name."""
        result = demonstrate_module_attributes()
        assert result["module_name"] == "__main__"

    def test_module_file(self):
        """Test module file."""
        result = demonstrate_module_attributes()
        assert "main.py" in result["module_file"]

    def test_python_version(self):
        """Test Python version."""
        result = demonstrate_module_attributes()
        assert result["python_version"].startswith("3.")


class TestCollections:
    """Test cases for demonstrate_collections()."""

    def test_defaultdict(self):
        """Test defaultdict."""
        result = demonstrate_collections()
        dd = result["defaultdict"]
        assert dd["l"] == 3

    def test_counter(self):
        """Test Counter."""
        result = demonstrate_collections()
        counter = result["counter"]
        assert counter["apple"] == 3

    def test_most_common(self):
        """Test most_common."""
        result = demonstrate_collections()
        most_common = result["most_common"]
        assert most_common[0][0] == "apple"

    def test_deque(self):
        """Test deque."""
        result = demonstrate_collections()
        deque_result = result["deque"]
        assert deque_result[0] == 0
        assert deque_result[-1] == 4


class TestItertools:
    """Test cases for demonstrate_itertools()."""

    def test_combinations(self):
        """Test combinations."""
        result = demonstrate_itertools()
        combs = result["combinations"]
        assert (1, 2) in combs

    def test_permutations(self):
        """Test permutations."""
        result = demonstrate_itertools()
        perms = result["permutations"]
        assert (1, 2) in perms

    def test_chain(self):
        """Test chain."""
        result = demonstrate_itertools()
        chained = result["chain"]
        assert chained == [1, 2, 3, 4, 5, 6]

    def test_product(self):
        """Test product."""
        result = demonstrate_itertools()
        prod = result["product"]
        assert (1, 'a') in prod


class TestPathlibModule:
    """Test cases for demonstrate_pathlib_module()."""

    def test_path_properties(self):
        """Test path properties."""
        result = demonstrate_pathlib_module()
        assert result["current_name"] == "main.py"
        assert result["suffix"] == ".py"

    def test_file_operations(self):
        """Test file operations."""
        result = demonstrate_pathlib_module()
        assert result["file_content"] == "Hello from pathlib!"


class TestFunctools:
    """Test cases for demonstrate_functools()."""

    def test_reduce(self):
        """Test reduce."""
        result = demonstrate_functools()
        assert result["reduce_product"] == 120

    def test_partial(self):
        """Test partial."""
        result = demonstrate_functools()
        assert result["square_5"] == 25
        assert result["cube_3"] == 27

    def test_lru_cache(self):
        """Test lru_cache."""
        result = demonstrate_functools()
        assert result["fibonacci_10"] == 55
        assert result["cache_hits"] >= 0


class TestOsSys:
    """Test cases for demonstrate_os_sys()."""

    def test_current_directory(self):
        """Test current directory."""
        result = demonstrate_os_sys()
        assert isinstance(result["current_dir"], str)

    def test_directory_operations(self):
        """Test directory operations."""
        result = demonstrate_os_sys()
        assert result["dir_created"] is True


class TestJsonModule:
    """Test cases for demonstrate_json_module()."""

    def test_json_operations(self):
        """Test JSON operations."""
        result = demonstrate_json_module()
        assert result["parsed_equal"] is True
        assert result["loaded_equal"] is True

    def test_json_structure(self):
        """Test JSON structure."""
        result = demonstrate_json_module()
        original = result["original"]
        assert original["name"] == "Alice"


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

        assert "Program 17: Modules" in captured.out


class TestIntegration:
    """Integration tests for modules."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_standard_library,
            demonstrate_import_styles,
            demonstrate_module_attributes,
            demonstrate_collections,
            demonstrate_itertools,
            demonstrate_pathlib_module,
            demonstrate_functools,
            demonstrate_os_sys,
            demonstrate_json_module,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
