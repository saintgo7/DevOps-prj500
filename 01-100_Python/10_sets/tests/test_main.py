"""
Unit tests for 10_sets program.

These tests verify:
- Set creation methods
- Set methods (add, remove, discard, etc.)
- Set operations (union, intersection, difference)
- Set comparisons
- Set comprehensions
- Frozensets
- Practical set use cases
- Edge cases
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_set_creation,
    demonstrate_set_methods,
    demonstrate_set_operations,
    demonstrate_set_comparisons,
    demonstrate_set_comprehensions,
    demonstrate_frozenset,
    demonstrate_set_use_cases,
    demonstrate_set_patterns,
    main,
)


class TestSetCreation:
    """Test cases for demonstrate_set_creation()."""

    def test_empty_set(self):
        """Test empty set creation."""
        result = demonstrate_set_creation()
        assert result["empty"] == set()
        assert isinstance(result["empty"], set)

    def test_numbers_set(self):
        """Test numbers set creation."""
        result = demonstrate_set_creation()
        assert result["numbers"] == {1, 2, 3, 4, 5}

    def test_deduplication(self):
        """Test automatic deduplication."""
        result = demonstrate_set_creation()
        from_list = result["from_list_deduped"]
        assert len(from_list) == 4  # Duplicates removed
        assert from_list == {1, 2, 3, 4, 5}

    def test_from_string(self):
        """Test set from string."""
        result = demonstrate_set_creation()
        from_string = result["from_string"]
        assert 'h' in from_string
        assert 'e' in from_string
        assert 'l' in from_string
        assert 'o' in from_string

    def test_set_comprehension(self):
        """Test set comprehension."""
        result = demonstrate_set_creation()
        comp = result["comprehension"]
        assert 0 in comp
        assert 25 in comp


class TestSetMethods:
    """Test cases for demonstrate_set_methods()."""

    def test_add_method(self):
        """Test add() method."""
        result = demonstrate_set_methods()
        assert 4 in result["add"]
        assert len(result["add"]) == 4

    def test_update_method(self):
        """Test update() method."""
        result = demonstrate_set_methods()
        updated = result["update"]
        assert len(updated) == 10
        assert 10 in updated

    def test_remove_method(self):
        """Test remove() method."""
        result = demonstrate_set_methods()
        assert 3 not in result["remove"]

    def test_discard_method(self):
        """Test discard() method."""
        result = demonstrate_set_methods()
        assert 3 not in result["discard"]
        assert len(result["discard"]) == 4

    def test_pop_method(self):
        """Test pop() method."""
        result = demonstrate_set_methods()
        pop_result = result["pop"]
        assert len(pop_result["set"]) == 4
        assert isinstance(pop_result["popped"], int)

    def test_clear_method(self):
        """Test clear() method."""
        result = demonstrate_set_methods()
        assert result["clear"] == set()

    def test_copy_method(self):
        """Test copy() method."""
        result = demonstrate_set_methods()
        copy_result = result["copy"]
        assert copy_result["original"] == copy_result["copy"]


class TestSetOperations:
    """Test cases for demonstrate_set_operations()."""

    def test_union_operation(self):
        """Test union operation."""
        result = demonstrate_set_operations()
        union = result["union"]
        assert len(union) == 8
        assert 1 in union
        assert 8 in union

    def test_intersection_operation(self):
        """Test intersection operation."""
        result = demonstrate_set_operations()
        intersection = result["intersection"]
        assert intersection == {4, 5}

    def test_difference_operation(self):
        """Test difference operation."""
        result = demonstrate_set_operations()
        diff_a_b = result["difference_a_b"]
        diff_b_a = result["difference_b_a"]
        assert diff_a_b == {1, 2, 3}
        assert diff_b_a == {6, 7, 8}

    def test_symmetric_difference(self):
        """Test symmetric difference."""
        result = demonstrate_set_operations()
        sym_diff = result["symmetric_difference"]
        assert len(sym_diff) == 6
        assert 4 not in sym_diff
        assert 5 not in sym_diff

    def test_multi_union(self):
        """Test union of multiple sets."""
        result = demonstrate_set_operations()
        multi_union = result["multi_union"]
        assert len(multi_union) == 8

    def test_multi_intersection(self):
        """Test intersection of multiple sets."""
        result = demonstrate_set_operations()
        multi_inter = result["multi_intersection"]
        assert multi_inter == {4, 5}


class TestSetComparisons:
    """Test cases for demonstrate_set_comparisons()."""

    def test_subset(self):
        """Test subset comparison."""
        result = demonstrate_set_comparisons()
        assert result["a_subset_of_b"] is True

    def test_proper_subset(self):
        """Test proper subset comparison."""
        result = demonstrate_set_comparisons()
        assert result["a_proper_subset_of_b"] is True

    def test_superset(self):
        """Test superset comparison."""
        result = demonstrate_set_comparisons()
        assert result["b_superset_of_a"] is True

    def test_proper_superset(self):
        """Test proper superset comparison."""
        result = demonstrate_set_comparisons()
        assert result["b_proper_superset_of_a"] is True

    def test_equality(self):
        """Test set equality."""
        result = demonstrate_set_comparisons()
        assert result["a_equals_c"] is True

    def test_disjoint(self):
        """Test disjoint sets."""
        result = demonstrate_set_comparisons()
        assert result["a_disjoint_d"] is True


class TestSetComprehensions:
    """Test cases for demonstrate_set_comprehensions()."""

    def test_squares_comprehension(self):
        """Test basic set comprehension."""
        result = demonstrate_set_comprehensions()
        squares = result["squares"]
        assert 0 in squares
        assert 81 in squares

    def test_even_squares(self):
        """Test conditional comprehension."""
        result = demonstrate_set_comprehensions()
        even_squares = result["even_squares"]
        assert 0 in even_squares
        assert 64 in even_squares

    def test_vowels_comprehension(self):
        """Test string filtering comprehension."""
        result = demonstrate_set_comprehensions()
        vowels = result["vowels"]
        assert 'e' in vowels
        assert 'o' in vowels

    def test_multiples_comprehensions(self):
        """Test mathematical set comprehensions."""
        result = demonstrate_set_comprehensions()
        mult_3 = result["multiples_3"]
        mult_5 = result["multiples_5"]
        mult_3_or_5 = result["multiples_3_or_5"]

        assert 3 in mult_3
        assert 5 in mult_5
        assert 15 in mult_3_or_5


class TestFrozenset:
    """Test cases for demonstrate_frozenset()."""

    def test_frozenset_creation(self):
        """Test frozenset creation."""
        result = demonstrate_frozenset()
        frozen = result["frozen"]
        assert isinstance(frozen, frozenset)
        assert 1 in frozen

    def test_frozenset_as_dict_key(self):
        """Test frozenset as dictionary key."""
        result = demonstrate_frozenset()
        dict_key = result["as_dict_key"]
        assert isinstance(dict_key, dict)

    def test_frozenset_union(self):
        """Test frozenset union."""
        result = demonstrate_frozenset()
        union = result["union"]
        assert isinstance(union, frozenset)
        assert len(union) == 5

    def test_frozenset_intersection(self):
        """Test frozenset intersection."""
        result = demonstrate_frozenset()
        intersection = result["intersection"]
        assert intersection == frozenset([3])


class TestSetUseCases:
    """Test cases for demonstrate_set_use_cases()."""

    def test_remove_duplicates(self):
        """Test removing duplicates use case."""
        result = demonstrate_set_use_cases()
        unique = result["remove_duplicates"]
        assert len(unique) == 5
        assert 1 in unique

    def test_membership_testing(self):
        """Test membership testing use case."""
        result = demonstrate_set_use_cases()
        assert result["membership_test"] is True

    def test_common_elements(self):
        """Test finding common elements."""
        result = demonstrate_set_use_cases()
        common = result["common_elements"]
        assert 4 in common
        assert 5 in common

    def test_unique_elements(self):
        """Test finding unique elements."""
        result = demonstrate_set_use_cases()
        unique1 = result["unique_to_list1"]
        unique2 = result["unique_to_list2"]
        assert 1 in unique1
        assert 8 in unique2

    def test_all_unique(self):
        """Test finding all unique elements."""
        result = demonstrate_set_use_cases()
        all_unique = result["all_unique"]
        assert len(all_unique) == 6

    def test_unique_word_count(self):
        """Test counting unique words."""
        result = demonstrate_set_use_cases()
        assert result["unique_word_count"] == 3


class TestSetPatterns:
    """Test cases for demonstrate_set_patterns()."""

    def test_unique_ordered(self):
        """Test preserving order while removing duplicates."""
        result = demonstrate_set_patterns()
        unique_ordered = result["unique_ordered"]
        assert len(unique_ordered) == 7
        assert unique_ordered[0] == 3  # First occurrence preserved

    def test_intersection_all(self):
        """Test intersection of multiple sets."""
        result = demonstrate_set_patterns()
        intersection_all = result["intersection_all"]
        assert 3 in intersection_all

    def test_union_all(self):
        """Test union of multiple sets."""
        result = demonstrate_set_patterns()
        union_all = result["union_all"]
        assert len(union_all) == 5

    def test_filtered_data(self):
        """Test filtering with sets."""
        result = demonstrate_set_patterns()
        filtered = result["filtered_data"]
        assert len(filtered) == 3
        assert filtered[0]["id"] == 1


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

        assert "Program 10: Sets" in captured.out
        assert "Set Creation:" in captured.out
        assert "Set Methods:" in captured.out
        assert "Set Operations:" in captured.out
        assert "Set Comparisons:" in captured.out


class TestIntegration:
    """Integration tests for set operations."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_set_creation,
            demonstrate_set_methods,
            demonstrate_set_operations,
            demonstrate_set_comparisons,
            demonstrate_set_comprehensions,
            demonstrate_frozenset,
            demonstrate_set_use_cases,
            demonstrate_set_patterns,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_set_operations(self):
        """Test operations on empty sets."""
        empty = set()
        assert len(empty) == 0
        assert empty.union({1, 2}) == {1, 2}
        assert empty.intersection({1, 2}) == set()

    def test_set_with_single_element(self):
        """Test single element set."""
        single = {42}
        assert len(single) == 1
        assert 42 in single


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
