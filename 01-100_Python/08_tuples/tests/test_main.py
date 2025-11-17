"""
Unit tests for 08_tuples program.

These tests verify:
- Tuple creation methods
- Indexing and slicing operations
- Tuple methods (count, index)
- Tuple operations
- Tuple unpacking
- Immutability
- Nested tuples
- Tuple vs list comparison
- Edge cases
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_tuple_creation,
    demonstrate_indexing_slicing,
    demonstrate_tuple_methods,
    demonstrate_tuple_operations,
    demonstrate_tuple_unpacking,
    demonstrate_immutability,
    demonstrate_nested_tuples,
    demonstrate_tuple_vs_list,
    main,
)


class TestTupleCreation:
    """Test cases for demonstrate_tuple_creation()."""

    def test_tuple_creation_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_tuple_creation()
        assert isinstance(result, dict)

    def test_empty_tuple(self):
        """Test empty tuple creation."""
        result = demonstrate_tuple_creation()
        assert result["empty"] == ()
        assert isinstance(result["empty"], tuple)

    def test_single_element_tuple(self):
        """Test single element tuple (with comma)."""
        result = demonstrate_tuple_creation()
        assert result["single"] == (1,)
        assert len(result["single"]) == 1

    def test_numbers_tuple(self):
        """Test numbers tuple creation."""
        result = demonstrate_tuple_creation()
        assert result["numbers"] == (1, 2, 3, 4, 5)

    def test_mixed_types_tuple(self):
        """Test mixed types tuple."""
        result = demonstrate_tuple_creation()
        mixed = result["mixed_types"]
        assert len(mixed) == 5
        assert isinstance(mixed, tuple)

    def test_nested_tuple(self):
        """Test nested tuple creation."""
        result = demonstrate_tuple_creation()
        assert result["nested"] == ((1, 2), (3, 4), (5, 6))

    def test_tuple_without_parentheses(self):
        """Test tuple creation without parentheses."""
        result = demonstrate_tuple_creation()
        assert result["without_parens"] == (1, 2, 3)
        assert isinstance(result["without_parens"], tuple)

    def test_tuple_from_list(self):
        """Test tuple from list conversion."""
        result = demonstrate_tuple_creation()
        assert result["from_list"] == (1, 2, 3, 4, 5)

    def test_tuple_from_string(self):
        """Test tuple from string conversion."""
        result = demonstrate_tuple_creation()
        assert result["from_string"] == ('h', 'e', 'l', 'l', 'o')


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
        assert result["slice_2_5"] == (30, 40, 50)

    def test_slicing_start(self):
        """Test slicing from start."""
        result = demonstrate_indexing_slicing()
        assert result["slice_start"] == (10, 20, 30)

    def test_slicing_end(self):
        """Test slicing to end."""
        result = demonstrate_indexing_slicing()
        assert result["slice_end"] == (80, 90, 100)

    def test_slicing_step(self):
        """Test slicing with step."""
        result = demonstrate_indexing_slicing()
        assert result["slice_step"] == (10, 30, 50, 70, 90)

    def test_reverse_slice(self):
        """Test reverse slicing."""
        result = demonstrate_indexing_slicing()
        assert result["reverse"] == (100, 90, 80, 70, 60, 50, 40, 30, 20, 10)

    def test_negative_slice(self):
        """Test negative indexing slice."""
        result = demonstrate_indexing_slicing()
        assert result["negative_slice"] == (80, 90, 100)


class TestTupleMethods:
    """Test cases for demonstrate_tuple_methods()."""

    def test_count_method_multiple(self):
        """Test count method with multiple occurrences."""
        result = demonstrate_tuple_methods()
        assert result["count_2"] == 3

    def test_count_method_single(self):
        """Test count method with single occurrence."""
        result = demonstrate_tuple_methods()
        assert result["count_5"] == 1

    def test_count_method_zero(self):
        """Test count method with zero occurrences."""
        result = demonstrate_tuple_methods()
        assert result["count_10"] == 0

    def test_index_method_first_occurrence(self):
        """Test index method finds first occurrence."""
        result = demonstrate_tuple_methods()
        assert result["index_2"] == 0

    def test_index_method_unique_element(self):
        """Test index method with unique element."""
        result = demonstrate_tuple_methods()
        assert result["index_5"] == 6


class TestTupleOperations:
    """Test cases for demonstrate_tuple_operations()."""

    def test_concatenation(self):
        """Test tuple concatenation."""
        result = demonstrate_tuple_operations()
        assert result["concatenation"] == (1, 2, 3, 4, 5, 6)
        assert isinstance(result["concatenation"], tuple)

    def test_repetition(self):
        """Test tuple repetition."""
        result = demonstrate_tuple_operations()
        assert result["repetition"] == (1, 2, 1, 2, 1, 2)

    def test_membership_true(self):
        """Test membership operator (present)."""
        result = demonstrate_tuple_operations()
        assert result["membership"]["has_3"] is True

    def test_membership_false(self):
        """Test membership operator (absent)."""
        result = demonstrate_tuple_operations()
        assert result["membership"]["has_10"] is False

    def test_length(self):
        """Test length operation."""
        result = demonstrate_tuple_operations()
        assert result["length"] == 5

    def test_min_operation(self):
        """Test min operation."""
        result = demonstrate_tuple_operations()
        assert result["min"] == 1

    def test_max_operation(self):
        """Test max operation."""
        result = demonstrate_tuple_operations()
        assert result["max"] == 5

    def test_sum_operation(self):
        """Test sum operation."""
        result = demonstrate_tuple_operations()
        assert result["sum"] == 15

    def test_comparison_less_than(self):
        """Test tuple comparison (less than)."""
        result = demonstrate_tuple_operations()
        assert result["comparison"]["t1_lt_t2"] is True

    def test_comparison_equality(self):
        """Test tuple comparison (equality)."""
        result = demonstrate_tuple_operations()
        assert result["comparison"]["t1_eq_t3"] is True


class TestTupleUnpacking:
    """Test cases for demonstrate_tuple_unpacking()."""

    def test_basic_unpacking(self):
        """Test basic tuple unpacking."""
        result = demonstrate_tuple_unpacking()
        assert result["basic"]["x"] == 10
        assert result["basic"]["y"] == 20

    def test_multiple_assignment(self):
        """Test multiple assignment unpacking."""
        result = demonstrate_tuple_unpacking()
        assert result["multiple"]["a"] == 1
        assert result["multiple"]["b"] == 2
        assert result["multiple"]["c"] == 3

    def test_swapping_values(self):
        """Test value swapping with unpacking."""
        result = demonstrate_tuple_unpacking()
        # After swap: x1 was 5, y1 was 10, now x1=10, y1=5
        assert result["swapped"]["x"] == 10
        assert result["swapped"]["y"] == 5

    def test_extended_unpacking_rest(self):
        """Test extended unpacking with *rest."""
        result = demonstrate_tuple_unpacking()
        assert result["extended"]["first"] == 1
        assert result["extended"]["second"] == 2
        assert result["extended"]["rest"] == [3, 4, 5, 6, 7, 8, 9, 10]

    def test_extended_unpacking_middle(self):
        """Test extended unpacking with middle elements."""
        result = demonstrate_tuple_unpacking()
        assert result["extended2"]["first"] == 1
        assert result["extended2"]["last"] == 10
        assert len(result["extended2"]["middle"]) == 8

    def test_nested_unpacking(self):
        """Test nested tuple unpacking."""
        result = demonstrate_tuple_unpacking()
        assert result["nested"]["a"] == 1
        assert result["nested"]["b"] == 2
        assert result["nested"]["c"] == 3
        assert result["nested"]["d"] == 4

    def test_function_return_unpacking(self):
        """Test unpacking function return values."""
        result = demonstrate_tuple_unpacking()
        assert result["function_return"]["min"] == 1
        assert result["function_return"]["max"] == 5
        assert result["function_return"]["avg"] == 3.0


class TestImmutability:
    """Test cases for demonstrate_immutability()."""

    def test_tuple_immutability(self):
        """Test that tuples are immutable."""
        result = demonstrate_immutability()
        assert result["original_tuple"] == (1, 2, 3, 4, 5)

    def test_mutable_objects_in_tuple(self):
        """Test modifying mutable objects inside tuple."""
        result = demonstrate_immutability()
        # List inside tuple was modified
        assert 99 in result["mixed_after_modify"][0]

    def test_creating_new_tuple(self):
        """Test creating new tuple from modified list."""
        result = demonstrate_immutability()
        assert result["new_tuple"] == (1, 2, 3, 4, 5, 6)


class TestNestedTuples:
    """Test cases for demonstrate_nested_tuples()."""

    def test_original_matrix(self):
        """Test original matrix structure."""
        result = demonstrate_nested_tuples()
        assert result["original"] == ((1, 2, 3), (4, 5, 6), (7, 8, 9))

    def test_first_row_access(self):
        """Test accessing first row."""
        result = demonstrate_nested_tuples()
        assert result["first_row"] == (1, 2, 3)

    def test_element_access(self):
        """Test accessing specific element."""
        result = demonstrate_nested_tuples()
        assert result["element_2_2"] == 5

    def test_modified_tuple(self):
        """Test creating modified version of tuple."""
        result = demonstrate_nested_tuples()
        assert result["modified"][0][0] == 99
        # Original should be unchanged
        assert result["original"][0][0] == 1

    def test_flattened_tuple(self):
        """Test tuple flattening."""
        result = demonstrate_nested_tuples()
        assert result["flattened"] == (1, 2, 3, 4, 5, 6, 7, 8, 9)


class TestTupleVsList:
    """Test cases for demonstrate_tuple_vs_list()."""

    def test_memory_comparison(self):
        """Test memory efficiency of tuples."""
        result = demonstrate_tuple_vs_list()
        assert result["tuple_size_bytes"] < result["list_size_bytes"]
        assert result["memory_diff"] > 0

    def test_tuple_as_dict_key(self):
        """Test using tuple as dictionary key."""
        result = demonstrate_tuple_vs_list()
        assert result["tuple_as_key"] == {(1, 2): "value"}

    def test_hashability_note(self):
        """Test hashability information."""
        result = demonstrate_tuple_vs_list()
        assert "hashable" in result["hashable"].lower()

    def test_use_cases(self):
        """Test use cases information."""
        result = demonstrate_tuple_vs_list()
        assert "tuple" in result["use_cases"]
        assert "list" in result["use_cases"]


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

        assert "Program 08: Tuples" in captured.out
        assert "Tuple Creation:" in captured.out
        assert "Indexing and Slicing:" in captured.out
        assert "Tuple Methods:" in captured.out
        assert "Tuple Operations:" in captured.out
        assert "Tuple Unpacking:" in captured.out
        assert "Immutability:" in captured.out
        assert "Nested Tuples:" in captured.out
        assert "Tuple vs List:" in captured.out


class TestIntegration:
    """Integration tests for tuple operations."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_tuple_creation,
            demonstrate_indexing_slicing,
            demonstrate_tuple_methods,
            demonstrate_tuple_operations,
            demonstrate_tuple_unpacking,
            demonstrate_immutability,
            demonstrate_nested_tuples,
            demonstrate_tuple_vs_list,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"

    def test_tuple_immutability_verification(self):
        """Verify tuple immutability cannot be bypassed."""
        test_tuple = (1, 2, 3)

        with pytest.raises(TypeError):
            test_tuple[0] = 99


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_tuple_operations(self):
        """Test operations on empty tuples."""
        result = demonstrate_tuple_creation()
        empty = result["empty"]

        assert len(empty) == 0
        assert empty + (1,) == (1,)
        assert empty * 5 == ()

    def test_single_element_tuple_operations(self):
        """Test operations on single element tuple."""
        result = demonstrate_tuple_creation()
        single = result["single"]

        assert len(single) == 1
        assert single[0] == 1
        assert single * 3 == (1, 1, 1)

    def test_tuple_hashable_as_set_element(self):
        """Test that tuples can be set elements."""
        tuple_set = {(1, 2), (3, 4), (5, 6)}
        assert len(tuple_set) == 3
        assert (1, 2) in tuple_set


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
