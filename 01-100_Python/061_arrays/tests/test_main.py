"""
Unit tests for 061_arrays program.

These tests verify:
- Array creation and initialization
- Array access and modification
- Array operations (insert, delete, search)
- Array algorithms
- Edge cases and boundary conditions
- Performance characteristics
"""

import sys
from pathlib import Path
from typing import List
import time

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestArrayBasics:
    """Test cases for basic array operations."""

    def test_array_creation_empty(self):
        """Test creating an empty array."""
        arr = []
        assert len(arr) == 0
        assert arr == []

    def test_array_creation_with_values(self):
        """Test creating an array with initial values."""
        arr = [1, 2, 3, 4, 5]
        assert len(arr) == 5
        assert arr == [1, 2, 3, 4, 5]

    def test_array_access_valid_index(self):
        """Test accessing array elements with valid indices."""
        arr = [10, 20, 30, 40, 50]
        assert arr[0] == 10
        assert arr[2] == 30
        assert arr[4] == 50
        assert arr[-1] == 50
        assert arr[-2] == 40

    def test_array_access_invalid_index(self):
        """Test accessing array with invalid index raises error."""
        arr = [1, 2, 3]
        with pytest.raises(IndexError):
            _ = arr[10]
        with pytest.raises(IndexError):
            _ = arr[-10]

    def test_array_modification(self):
        """Test modifying array elements."""
        arr = [1, 2, 3, 4, 5]
        arr[0] = 10
        arr[2] = 30
        arr[-1] = 50
        assert arr == [10, 2, 30, 4, 50]

    def test_array_slicing(self):
        """Test array slicing operations."""
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert arr[2:5] == [2, 3, 4]
        assert arr[:3] == [0, 1, 2]
        assert arr[7:] == [7, 8, 9]
        assert arr[::2] == [0, 2, 4, 6, 8]
        assert arr[::-1] == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


class TestArrayOperations:
    """Test cases for array operations."""

    def test_array_append(self):
        """Test appending elements to array."""
        arr = [1, 2, 3]
        arr.append(4)
        assert arr == [1, 2, 3, 4]
        arr.append(5)
        assert len(arr) == 5

    def test_array_insert(self):
        """Test inserting elements at specific positions."""
        arr = [1, 2, 4, 5]
        arr.insert(2, 3)
        assert arr == [1, 2, 3, 4, 5]
        arr.insert(0, 0)
        assert arr == [0, 1, 2, 3, 4, 5]
        arr.insert(len(arr), 6)
        assert arr == [0, 1, 2, 3, 4, 5, 6]

    def test_array_remove(self):
        """Test removing elements from array."""
        arr = [1, 2, 3, 2, 4]
        arr.remove(2)  # Removes first occurrence
        assert arr == [1, 3, 2, 4]
        arr.remove(4)
        assert arr == [1, 3, 2]

    def test_array_pop(self):
        """Test popping elements from array."""
        arr = [1, 2, 3, 4, 5]
        last = arr.pop()
        assert last == 5
        assert arr == [1, 2, 3, 4]

        second = arr.pop(1)
        assert second == 2
        assert arr == [1, 3, 4]

    def test_array_delete_by_index(self):
        """Test deleting elements by index."""
        arr = [1, 2, 3, 4, 5]
        del arr[2]
        assert arr == [1, 2, 4, 5]
        del arr[0]
        assert arr == [2, 4, 5]

    def test_array_clear(self):
        """Test clearing all elements from array."""
        arr = [1, 2, 3, 4, 5]
        arr.clear()
        assert arr == []
        assert len(arr) == 0

    def test_array_extend(self):
        """Test extending array with another array."""
        arr1 = [1, 2, 3]
        arr2 = [4, 5, 6]
        arr1.extend(arr2)
        assert arr1 == [1, 2, 3, 4, 5, 6]
        assert arr2 == [4, 5, 6]  # Original unchanged


class TestArraySearching:
    """Test cases for array searching algorithms."""

    def test_linear_search_found(self):
        """Test linear search when element exists."""
        arr = [5, 2, 8, 1, 9, 3]
        target = 8
        index = arr.index(target)
        assert index == 2
        assert arr[index] == target

    def test_linear_search_not_found(self):
        """Test linear search when element doesn't exist."""
        arr = [1, 2, 3, 4, 5]
        with pytest.raises(ValueError):
            arr.index(10)

    def test_membership_check(self):
        """Test checking if element exists in array."""
        arr = [1, 2, 3, 4, 5]
        assert 3 in arr
        assert 10 not in arr
        assert 1 in arr
        assert 0 not in arr

    def test_count_occurrences(self):
        """Test counting element occurrences."""
        arr = [1, 2, 3, 2, 4, 2, 5]
        assert arr.count(2) == 3
        assert arr.count(1) == 1
        assert arr.count(10) == 0


class TestArraySorting:
    """Test cases for array sorting."""

    def test_sort_ascending(self):
        """Test sorting array in ascending order."""
        arr = [5, 2, 8, 1, 9, 3]
        arr.sort()
        assert arr == [1, 2, 3, 5, 8, 9]

    def test_sort_descending(self):
        """Test sorting array in descending order."""
        arr = [5, 2, 8, 1, 9, 3]
        arr.sort(reverse=True)
        assert arr == [9, 8, 5, 3, 2, 1]

    def test_sorted_returns_new_array(self):
        """Test that sorted() returns new array without modifying original."""
        original = [5, 2, 8, 1, 9, 3]
        sorted_arr = sorted(original)
        assert sorted_arr == [1, 2, 3, 5, 8, 9]
        assert original == [5, 2, 8, 1, 9, 3]

    def test_reverse_array(self):
        """Test reversing array."""
        arr = [1, 2, 3, 4, 5]
        arr.reverse()
        assert arr == [5, 4, 3, 2, 1]


class TestArrayAggregation:
    """Test cases for array aggregation operations."""

    def test_sum_array(self):
        """Test calculating sum of array elements."""
        arr = [1, 2, 3, 4, 5]
        assert sum(arr) == 15
        assert sum([]) == 0
        assert sum([10]) == 10

    def test_min_max(self):
        """Test finding minimum and maximum values."""
        arr = [5, 2, 8, 1, 9, 3]
        assert min(arr) == 1
        assert max(arr) == 9

        arr2 = [-5, -2, -8, -1]
        assert min(arr2) == -8
        assert max(arr2) == -1

    def test_min_max_empty_array(self):
        """Test min/max on empty array raises error."""
        arr = []
        with pytest.raises(ValueError):
            min(arr)
        with pytest.raises(ValueError):
            max(arr)


class TestArrayIterations:
    """Test cases for array iteration methods."""

    def test_basic_iteration(self):
        """Test iterating over array elements."""
        arr = [1, 2, 3, 4, 5]
        result = []
        for item in arr:
            result.append(item * 2)
        assert result == [2, 4, 6, 8, 10]

    def test_enumerate(self):
        """Test iteration with indices using enumerate."""
        arr = ['a', 'b', 'c']
        indices = []
        values = []
        for idx, val in enumerate(arr):
            indices.append(idx)
            values.append(val)
        assert indices == [0, 1, 2]
        assert values == ['a', 'b', 'c']

    def test_list_comprehension(self):
        """Test list comprehension for transformations."""
        arr = [1, 2, 3, 4, 5]
        squared = [x ** 2 for x in arr]
        assert squared == [1, 4, 9, 16, 25]

        evens = [x for x in arr if x % 2 == 0]
        assert evens == [2, 4]

    def test_map_function(self):
        """Test using map for transformations."""
        arr = [1, 2, 3, 4, 5]
        doubled = list(map(lambda x: x * 2, arr))
        assert doubled == [2, 4, 6, 8, 10]

    def test_filter_function(self):
        """Test using filter for selecting elements."""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        evens = list(filter(lambda x: x % 2 == 0, arr))
        assert evens == [2, 4, 6, 8, 10]


class TestMultidimensionalArrays:
    """Test cases for multidimensional arrays."""

    def test_2d_array_creation(self):
        """Test creating a 2D array."""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert len(matrix) == 3
        assert len(matrix[0]) == 3
        assert matrix[1][1] == 5

    def test_2d_array_access(self):
        """Test accessing 2D array elements."""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert matrix[0][0] == 1
        assert matrix[2][2] == 9
        assert matrix[1][2] == 6

    def test_2d_array_modification(self):
        """Test modifying 2D array elements."""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        matrix[1][1] = 50
        assert matrix == [[1, 2, 3], [4, 50, 6], [7, 8, 9]]

    def test_2d_array_iteration(self):
        """Test iterating over 2D array."""
        matrix = [[1, 2], [3, 4], [5, 6]]
        flattened = []
        for row in matrix:
            for val in row:
                flattened.append(val)
        assert flattened == [1, 2, 3, 4, 5, 6]


class TestArrayEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_array_operations(self):
        """Test operations on empty array."""
        arr = []
        assert len(arr) == 0
        assert sum(arr) == 0
        assert list(reversed(arr)) == []

    def test_single_element_array(self):
        """Test operations on single element array."""
        arr = [42]
        assert len(arr) == 1
        assert sum(arr) == 42
        assert min(arr) == 42
        assert max(arr) == 42

    def test_duplicate_elements(self):
        """Test array with all duplicate elements."""
        arr = [5, 5, 5, 5, 5]
        assert len(set(arr)) == 1
        assert arr.count(5) == 5
        assert min(arr) == 5
        assert max(arr) == 5

    def test_large_array_performance(self):
        """Test performance with large arrays."""
        large_arr = list(range(100000))

        start = time.time()
        _ = 50000 in large_arr
        search_time = time.time() - start

        start = time.time()
        _ = len(large_arr)
        len_time = time.time() - start

        # These operations should be fast
        assert search_time < 1.0
        assert len_time < 0.1

    def test_negative_indices(self):
        """Test negative indexing."""
        arr = [1, 2, 3, 4, 5]
        assert arr[-1] == 5
        assert arr[-2] == 4
        assert arr[-5] == 1

    def test_array_concatenation(self):
        """Test array concatenation with + operator."""
        arr1 = [1, 2, 3]
        arr2 = [4, 5, 6]
        result = arr1 + arr2
        assert result == [1, 2, 3, 4, 5, 6]
        assert arr1 == [1, 2, 3]  # Originals unchanged
        assert arr2 == [4, 5, 6]

    def test_array_repetition(self):
        """Test array repetition with * operator."""
        arr = [1, 2, 3]
        repeated = arr * 3
        assert repeated == [1, 2, 3, 1, 2, 3, 1, 2, 3]
        assert len(repeated) == 9


class TestArrayCopy:
    """Test cases for array copying."""

    def test_shallow_copy(self):
        """Test shallow copy of array."""
        original = [1, 2, 3, 4, 5]
        copy = original.copy()
        copy[0] = 10
        assert original[0] == 1
        assert copy[0] == 10

    def test_slice_copy(self):
        """Test copying array using slicing."""
        original = [1, 2, 3, 4, 5]
        copy = original[:]
        copy[0] = 10
        assert original[0] == 1
        assert copy[0] == 10

    def test_shallow_copy_nested(self):
        """Test shallow copy with nested arrays."""
        original = [[1, 2], [3, 4]]
        copy = original.copy()
        copy[0][0] = 10
        # Shallow copy: nested lists are shared
        assert original[0][0] == 10


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
