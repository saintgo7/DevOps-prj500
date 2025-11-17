"""
Unit tests for 07_lists program.

These tests verify:
- List creation methods
- Indexing and slicing operations
- List methods (append, extend, insert, remove, etc.)
- List operations (concatenation, repetition, membership)
- List comprehensions
- Nested lists
- Common list patterns
- Edge cases
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_list_creation,
    demonstrate_indexing_slicing,
    demonstrate_list_methods,
    demonstrate_list_operations,
    demonstrate_list_comprehensions,
    demonstrate_nested_lists,
    demonstrate_list_patterns,
    main,
)


class TestListCreation:
    """Test cases for demonstrate_list_creation()."""

    def test_list_creation_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_list_creation()
        assert isinstance(result, dict)

    def test_empty_list(self):
        """Test empty list creation."""
        result = demonstrate_list_creation()
        assert result["empty"] == []

    def test_numbers_list(self):
        """Test numbers list creation."""
        result = demonstrate_list_creation()
        assert result["numbers"] == [1, 2, 3, 4, 5]

    def test_mixed_types_list(self):
        """Test mixed types list."""
        result = demonstrate_list_creation()
        mixed = result["mixed_types"]
        assert len(mixed) == 5
        assert 1 in mixed
        assert "hello" in mixed
        assert 3.14 in mixed
        assert True in mixed
        assert None in mixed

    def test_nested_list(self):
        """Test nested list creation."""
        result = demonstrate_list_creation()
        assert result["nested"] == [[1, 2], [3, 4], [5, 6]]

    def test_range_list(self):
        """Test list from range."""
        result = demonstrate_list_creation()
        assert result["from_range"] == [1, 2, 3, 4, 5]

    def test_repeated_list(self):
        """Test repeated element list."""
        result = demonstrate_list_creation()
        assert result["repeated"] == [0, 0, 0, 0, 0]

    def test_comprehension_list(self):
        """Test list comprehension."""
        result = demonstrate_list_creation()
        assert result["comprehension"] == [0, 2, 4, 6, 8]


class TestIndexingSlicing:
    """Test cases for demonstrate_indexing_slicing()."""

    def test_indexing_first_element(self):
        """Test accessing first element."""
        result = demonstrate_indexing_slicing()
        assert result["first"] == 10

    def test_indexing_last_element(self):
        """Test accessing last element."""
        result = demonstrate_indexing_slicing()
        assert result["last"] == 100

    def test_indexing_third_element(self):
        """Test accessing third element."""
        result = demonstrate_indexing_slicing()
        assert result["third"] == 30

    def test_slicing_middle(self):
        """Test slicing middle elements."""
        result = demonstrate_indexing_slicing()
        assert result["slice_2_5"] == [30, 40, 50]

    def test_slicing_start(self):
        """Test slicing from start."""
        result = demonstrate_indexing_slicing()
        assert result["slice_start"] == [10, 20, 30]

    def test_slicing_end(self):
        """Test slicing to end."""
        result = demonstrate_indexing_slicing()
        assert result["slice_end"] == [80, 90, 100]

    def test_slicing_step(self):
        """Test slicing with step."""
        result = demonstrate_indexing_slicing()
        assert result["slice_step"] == [10, 30, 50, 70, 90]

    def test_reverse_slice(self):
        """Test reverse slicing."""
        result = demonstrate_indexing_slicing()
        assert result["reverse"] == [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

    def test_negative_slice(self):
        """Test negative indexing slice."""
        result = demonstrate_indexing_slicing()
        assert result["negative_slice"] == [80, 90, 100]


class TestListMethods:
    """Test cases for demonstrate_list_methods()."""

    def test_append_method(self):
        """Test append method."""
        result = demonstrate_list_methods()
        assert result["append"] == [1, 2, 3, 4]

    def test_extend_method(self):
        """Test extend method."""
        result = demonstrate_list_methods()
        assert result["extend"] == [1, 2, 3, 4, 5, 6]

    def test_insert_method(self):
        """Test insert method."""
        result = demonstrate_list_methods()
        assert result["insert"] == [1, 2, 3, 4]

    def test_remove_method(self):
        """Test remove method."""
        result = demonstrate_list_methods()
        assert result["remove"] == [1, 3, 2]

    def test_pop_method(self):
        """Test pop methods."""
        result = demonstrate_list_methods()
        assert result["pop"]["list"] == [1, 2]
        assert result["pop"]["popped"] == 4
        assert result["pop"]["popped_index"] == 2

    def test_index_method(self):
        """Test index method."""
        result = demonstrate_list_methods()
        assert result["index"] == 1

    def test_count_method(self):
        """Test count method."""
        result = demonstrate_list_methods()
        assert result["count"] == 3

    def test_sort_ascending(self):
        """Test sort ascending."""
        result = demonstrate_list_methods()
        assert result["sort_asc"] == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sort_descending(self):
        """Test sort descending."""
        result = demonstrate_list_methods()
        assert result["sort_desc"] == [9, 6, 5, 4, 3, 2, 1, 1]

    def test_reverse_method(self):
        """Test reverse method."""
        result = demonstrate_list_methods()
        assert result["reverse"] == [5, 4, 3, 2, 1]

    def test_clear_method(self):
        """Test clear method."""
        result = demonstrate_list_methods()
        assert result["clear"] == []

    def test_copy_method(self):
        """Test copy method."""
        result = demonstrate_list_methods()
        assert result["copy"]["original"] == [1, 2, 3]
        assert result["copy"]["copy"] == [1, 2, 3]
        assert result["copy"]["are_equal"] is True
        assert result["copy"]["are_same"] is False


class TestListOperations:
    """Test cases for demonstrate_list_operations()."""

    def test_concatenation(self):
        """Test list concatenation."""
        result = demonstrate_list_operations()
        assert result["concatenation"] == [1, 2, 3, 4, 5, 6]

    def test_repetition(self):
        """Test list repetition."""
        result = demonstrate_list_operations()
        assert result["repetition"] == [1, 2, 1, 2, 1, 2]

    def test_membership_true(self):
        """Test membership operator (present)."""
        result = demonstrate_list_operations()
        assert result["membership"]["has_3"] is True

    def test_membership_false(self):
        """Test membership operator (absent)."""
        result = demonstrate_list_operations()
        assert result["membership"]["has_10"] is False

    def test_length(self):
        """Test length operation."""
        result = demonstrate_list_operations()
        assert result["length"] == 5

    def test_min_operation(self):
        """Test min operation."""
        result = demonstrate_list_operations()
        assert result["min"] == 1

    def test_max_operation(self):
        """Test max operation."""
        result = demonstrate_list_operations()
        assert result["max"] == 5

    def test_sum_operation(self):
        """Test sum operation."""
        result = demonstrate_list_operations()
        assert result["sum"] == 15

    def test_doubled_list(self):
        """Test list comprehension doubling."""
        result = demonstrate_list_operations()
        assert result["doubled"] == [2, 4, 6, 8, 10]


class TestListComprehensions:
    """Test cases for demonstrate_list_comprehensions()."""

    def test_squares_comprehension(self):
        """Test basic squares comprehension."""
        result = demonstrate_list_comprehensions()
        assert result["squares"] == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    def test_evens_comprehension(self):
        """Test filtering even numbers."""
        result = demonstrate_list_comprehensions()
        assert result["evens"] == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    def test_even_odd_comprehension(self):
        """Test if-else comprehension."""
        result = demonstrate_list_comprehensions()
        expected = ["even", "odd", "even", "odd", "even", "odd", "even", "odd", "even", "odd"]
        assert result["even_odd"] == expected

    def test_matrix_comprehension(self):
        """Test nested comprehension for matrix."""
        result = demonstrate_list_comprehensions()
        assert result["matrix"] == [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

    def test_flattened_comprehension(self):
        """Test flattening nested lists."""
        result = demonstrate_list_comprehensions()
        assert result["flattened"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_uppercase_comprehension(self):
        """Test string manipulation comprehension."""
        result = demonstrate_list_comprehensions()
        assert result["uppercase"] == ["HELLO", "WORLD", "PYTHON"]


class TestNestedLists:
    """Test cases for demonstrate_nested_lists()."""

    def test_original_matrix(self):
        """Test original matrix structure."""
        result = demonstrate_nested_lists()
        assert result["original"] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_first_row_access(self):
        """Test accessing first row."""
        result = demonstrate_nested_lists()
        assert result["first_row"] == [1, 2, 3]

    def test_element_access(self):
        """Test accessing specific element."""
        result = demonstrate_nested_lists()
        assert result["element_2_2"] == 5

    def test_modified_matrix(self):
        """Test matrix modification."""
        result = demonstrate_nested_lists()
        assert result["modified"][0][0] == 99

    def test_transposed_matrix(self):
        """Test matrix transposition."""
        result = demonstrate_nested_lists()
        assert result["transposed"] == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    def test_flattened_matrix(self):
        """Test matrix flattening."""
        result = demonstrate_nested_lists()
        assert result["flattened"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]


class TestListPatterns:
    """Test cases for demonstrate_list_patterns()."""

    def test_filter_pattern(self):
        """Test filter pattern."""
        result = demonstrate_list_patterns()
        assert result["filter_evens"] == [2, 4, 6, 8, 10]

    def test_map_pattern(self):
        """Test map pattern."""
        result = demonstrate_list_patterns()
        assert result["map_doubled"] == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    def test_zip_pattern(self):
        """Test zip pattern."""
        result = demonstrate_list_patterns()
        assert result["zip"] == [("Alice", 25), ("Bob", 30), ("Charlie", 35)]

    def test_enumerate_pattern(self):
        """Test enumerate pattern."""
        result = demonstrate_list_patterns()
        assert result["enumerate"] == [(0, "Alice"), (1, "Bob"), (2, "Charlie")]

    def test_sorted_ascending(self):
        """Test sorted ascending."""
        result = demonstrate_list_patterns()
        assert result["sorted_asc"] == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sorted_descending(self):
        """Test sorted descending."""
        result = demonstrate_list_patterns()
        assert result["sorted_desc"] == [9, 6, 5, 4, 3, 2, 1, 1]

    def test_reversed_pattern(self):
        """Test reversed pattern."""
        result = demonstrate_list_patterns()
        assert result["reversed"] == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    def test_any_pattern(self):
        """Test any() pattern."""
        result = demonstrate_list_patterns()
        assert result["has_even"] is True

    def test_all_pattern(self):
        """Test all() pattern."""
        result = demonstrate_list_patterns()
        assert result["all_positive"] is True


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

        assert "Program 07: Lists" in captured.out
        assert "List Creation:" in captured.out
        assert "Indexing and Slicing:" in captured.out
        assert "List Methods:" in captured.out
        assert "List Operations:" in captured.out
        assert "List Comprehensions:" in captured.out
        assert "Nested Lists:" in captured.out
        assert "Common Patterns:" in captured.out


class TestIntegration:
    """Integration tests for list operations."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_list_creation,
            demonstrate_indexing_slicing,
            demonstrate_list_methods,
            demonstrate_list_operations,
            demonstrate_list_comprehensions,
            demonstrate_nested_lists,
            demonstrate_list_patterns,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"

    def test_list_mutation_vs_creation(self):
        """Test understanding of list mutation."""
        result = demonstrate_list_methods()

        # Verify methods that mutate lists
        assert isinstance(result["append"], list)
        assert isinstance(result["extend"], list)

        # Verify copy creates new list
        assert result["copy"]["are_same"] is False


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_list_operations(self):
        """Test operations on empty lists."""
        result = demonstrate_list_creation()
        empty = result["empty"]

        assert len(empty) == 0
        assert sum(empty) == 0
        assert empty + [1] == [1]

    def test_single_element_list(self):
        """Test operations on single element list."""
        single = [42]

        assert len(single) == 1
        assert single[0] == 42
        assert single[-1] == 42
        assert min(single) == 42
        assert max(single) == 42

    def test_list_comprehension_empty_result(self):
        """Test list comprehension with no matching elements."""
        result = [x for x in range(10) if x > 100]
        assert result == []


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
