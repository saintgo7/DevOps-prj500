"""
Unit tests for 09_dictionaries program.

These tests verify:
- Dictionary creation methods
- Accessing elements
- Dictionary methods
- Dictionary operations
- Dictionary comprehensions
- Nested dictionaries
- defaultdict and Counter
- Edge cases
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_dict_creation,
    demonstrate_accessing_elements,
    demonstrate_dict_methods,
    demonstrate_dict_operations,
    demonstrate_dict_comprehensions,
    demonstrate_nested_dicts,
    demonstrate_defaultdict,
    demonstrate_counter,
    main,
)


class TestDictCreation:
    """Test cases for demonstrate_dict_creation()."""

    def test_empty_dict(self):
        """Test empty dictionary creation."""
        result = demonstrate_dict_creation()
        assert result["empty"] == {}

    def test_basic_dict(self):
        """Test basic dictionary creation."""
        result = demonstrate_dict_creation()
        basic = result["basic"]
        assert basic["name"] == "Alice"
        assert basic["age"] == 25
        assert basic["city"] == "NYC"

    def test_dict_constructor(self):
        """Test dict() constructor."""
        result = demonstrate_dict_creation()
        constructor = result["constructor"]
        assert constructor["name"] == "Bob"
        assert constructor["age"] == 30

    def test_dict_from_tuples(self):
        """Test dict creation from tuples."""
        result = demonstrate_dict_creation()
        assert result["from_tuples"] == {"a": 1, "b": 2, "c": 3}

    def test_dict_comprehension(self):
        """Test dictionary comprehension."""
        result = demonstrate_dict_creation()
        assert result["comprehension"] == {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

    def test_dict_fromkeys(self):
        """Test dict.fromkeys() method."""
        result = demonstrate_dict_creation()
        assert result["fromkeys"] == {"a": 0, "b": 0, "c": 0}

    def test_nested_dict(self):
        """Test nested dictionary creation."""
        result = demonstrate_dict_creation()
        nested = result["nested"]
        assert "person1" in nested
        assert "person2" in nested
        assert nested["person1"]["name"] == "Alice"


class TestAccessingElements:
    """Test cases for demonstrate_accessing_elements()."""

    def test_bracket_access(self):
        """Test accessing with [] operator."""
        result = demonstrate_accessing_elements()
        assert result["name_bracket"] == "Alice"

    def test_get_method(self):
        """Test get() method."""
        result = demonstrate_accessing_elements()
        assert result["age_get"] == 25

    def test_get_with_default(self):
        """Test get() with default value."""
        result = demonstrate_accessing_elements()
        assert result["country_default"] == "USA"

    def test_keys_method(self):
        """Test keys() method."""
        result = demonstrate_accessing_elements()
        keys = result["keys"]
        assert "name" in keys
        assert "age" in keys
        assert "city" in keys

    def test_values_method(self):
        """Test values() method."""
        result = demonstrate_accessing_elements()
        values = result["values"]
        assert "Alice" in values
        assert 25 in values

    def test_items_method(self):
        """Test items() method."""
        result = demonstrate_accessing_elements()
        items = result["items"]
        assert ("name", "Alice") in items

    def test_in_operator_present(self):
        """Test 'in' operator for existing key."""
        result = demonstrate_accessing_elements()
        assert result["has_name"] is True

    def test_in_operator_absent(self):
        """Test 'in' operator for non-existing key."""
        result = demonstrate_accessing_elements()
        assert result["has_country"] is False


class TestDictMethods:
    """Test cases for demonstrate_dict_methods()."""

    def test_update_method(self):
        """Test update() method."""
        result = demonstrate_dict_methods()
        updated = result["update"]
        assert len(updated) == 6
        assert updated["a"] == 1
        assert updated["f"] == 6

    def test_pop_method(self):
        """Test pop() method."""
        result = demonstrate_dict_methods()
        pop_result = result["pop"]
        assert pop_result["popped"] == 2
        assert "b" not in pop_result["dict"]

    def test_pop_default(self):
        """Test pop() with default value."""
        result = demonstrate_dict_methods()
        assert result["pop"]["default"] == "not found"

    def test_popitem_method(self):
        """Test popitem() method."""
        result = demonstrate_dict_methods()
        popitem_result = result["popitem"]
        assert popitem_result["item"] == ("c", 3)

    def test_setdefault_existing(self):
        """Test setdefault() with existing key."""
        result = demonstrate_dict_methods()
        assert result["setdefault"]["val1"] == 1

    def test_setdefault_new(self):
        """Test setdefault() with new key."""
        result = demonstrate_dict_methods()
        assert result["setdefault"]["val2"] == 3
        assert result["setdefault"]["dict"]["c"] == 3

    def test_clear_method(self):
        """Test clear() method."""
        result = demonstrate_dict_methods()
        assert result["clear"] == {}

    def test_copy_method(self):
        """Test copy() method."""
        result = demonstrate_dict_methods()
        copy_result = result["copy"]
        assert copy_result["are_equal"] is True
        assert copy_result["are_same"] is False


class TestDictOperations:
    """Test cases for demonstrate_dict_operations()."""

    def test_merge_operator(self):
        """Test merge with | operator."""
        result = demonstrate_dict_operations()
        merged = result["merge"]
        assert len(merged) == 4
        assert merged["a"] == 1
        assert merged["d"] == 4

    def test_update_merge_operator(self):
        """Test update with |= operator."""
        result = demonstrate_dict_operations()
        updated = result["update_merge"]
        assert len(updated) == 4

    def test_length(self):
        """Test len() function."""
        result = demonstrate_dict_operations()
        assert result["length"] == 2

    def test_delete_key(self):
        """Test del keyword."""
        result = demonstrate_dict_operations()
        deleted = result["delete"]
        assert "b" not in deleted
        assert len(deleted) == 2

    def test_iterate_keys(self):
        """Test iterating over keys."""
        result = demonstrate_dict_operations()
        keys = result["iterate_keys"]
        assert len(keys) == 3
        assert "name" in keys

    def test_iterate_values(self):
        """Test iterating over values."""
        result = demonstrate_dict_operations()
        values = result["iterate_values"]
        assert "Alice" in values

    def test_iterate_items(self):
        """Test iterating over items."""
        result = demonstrate_dict_operations()
        items = result["iterate_items"]
        assert len(items) == 3


class TestDictComprehensions:
    """Test cases for demonstrate_dict_comprehensions()."""

    def test_basic_comprehension(self):
        """Test basic dictionary comprehension."""
        result = demonstrate_dict_comprehensions()
        squares = result["squares"]
        assert squares[0] == 0
        assert squares[5] == 25

    def test_conditional_comprehension(self):
        """Test comprehension with condition."""
        result = demonstrate_dict_comprehensions()
        even_squares = result["even_squares"]
        assert 0 in even_squares
        assert 2 in even_squares
        assert 1 not in even_squares

    def test_combined_comprehension(self):
        """Test comprehension from two lists."""
        result = demonstrate_dict_comprehensions()
        combined = result["combined"]
        assert combined["a"] == 1
        assert combined["c"] == 3

    def test_swapped_comprehension(self):
        """Test swapping keys and values."""
        result = demonstrate_dict_comprehensions()
        swapped = result["swapped"]
        assert swapped[1] == "a"
        assert swapped[3] == "c"

    def test_conditional_values(self):
        """Test conditional values in comprehension."""
        result = demonstrate_dict_comprehensions()
        numbers = result["conditional"]
        assert numbers[0] == "even"
        assert numbers[1] == "odd"

    def test_nested_dict_comprehension(self):
        """Test nested dictionary comprehension."""
        result = demonstrate_dict_comprehensions()
        matrix = result["nested"]
        assert matrix[1][1] == 1
        assert matrix[2][3] == 6


class TestNestedDicts:
    """Test cases for demonstrate_nested_dicts()."""

    def test_access_nested_value(self):
        """Test accessing nested dictionary values."""
        result = demonstrate_nested_dicts()
        assert result["alice_age"] == 25
        assert result["post1_title"] == "Hello"

    def test_safe_nested_access(self):
        """Test safe nested access with get()."""
        result = demonstrate_nested_dicts()
        assert result["bob_country"] == "Unknown"

    def test_modified_nested_dict(self):
        """Test modifying nested dictionary."""
        result = demonstrate_nested_dicts()
        modified = result["modified"]
        assert modified["users"]["alice"]["age"] == 26
        # Original should have different age
        assert result["database"]["users"]["alice"]["age"] == 25


class TestDefaultdict:
    """Test cases for demonstrate_defaultdict()."""

    def test_defaultdict_int(self):
        """Test defaultdict with int."""
        result = demonstrate_defaultdict()
        counts = result["counts"]
        assert counts["l"] == 3
        assert counts["o"] == 2

    def test_defaultdict_list(self):
        """Test defaultdict with list."""
        result = demonstrate_defaultdict()
        groups = result["groups"]
        assert "fruit" in groups
        assert len(groups["fruit"]) == 2
        assert "apple" in groups["fruit"]

    def test_defaultdict_dict(self):
        """Test defaultdict with dict."""
        result = demonstrate_defaultdict()
        nested = result["nested"]
        assert nested["user1"]["name"] == "Alice"


class TestCounter:
    """Test cases for demonstrate_counter()."""

    def test_counter_basic(self):
        """Test basic Counter functionality."""
        result = demonstrate_counter()
        counter = result["counter"]
        assert counter[4] == 4
        assert counter[3] == 3

    def test_most_common(self):
        """Test most_common() method."""
        result = demonstrate_counter()
        most_common = result["most_common"]
        assert most_common[0] == (4, 4)

    def test_counter_from_string(self):
        """Test Counter with string."""
        result = demonstrate_counter()
        letter_count = result["letters"]
        assert letter_count["l"] == 3
        assert letter_count["o"] == 2

    def test_counter_addition(self):
        """Test Counter addition."""
        result = demonstrate_counter()
        addition = result["addition"]
        assert addition["a"] == 3

    def test_counter_subtraction(self):
        """Test Counter subtraction."""
        result = demonstrate_counter()
        subtraction = result["subtraction"]
        assert subtraction["a"] == 1

    def test_counter_intersection(self):
        """Test Counter intersection."""
        result = demonstrate_counter()
        intersection = result["intersection"]
        assert "a" in intersection
        assert "b" in intersection

    def test_counter_union(self):
        """Test Counter union."""
        result = demonstrate_counter()
        union = result["union"]
        assert union["a"] == 2


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

        assert "Program 09: Dictionaries" in captured.out
        assert "Dictionary Creation:" in captured.out
        assert "Accessing Elements:" in captured.out
        assert "Dictionary Methods:" in captured.out
        assert "Dictionary Operations:" in captured.out
        assert "Dictionary Comprehensions:" in captured.out
        assert "Nested Dictionaries:" in captured.out
        assert "DefaultDict:" in captured.out
        assert "Counter:" in captured.out


class TestIntegration:
    """Integration tests for dictionary operations."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_dict_creation,
            demonstrate_accessing_elements,
            demonstrate_dict_methods,
            demonstrate_dict_operations,
            demonstrate_dict_comprehensions,
            demonstrate_nested_dicts,
            demonstrate_defaultdict,
            demonstrate_counter,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_dict_operations(self):
        """Test operations on empty dictionaries."""
        empty = {}
        assert len(empty) == 0
        assert list(empty.keys()) == []
        assert list(empty.values()) == []
        assert empty.get("key", "default") == "default"

    def test_dict_key_types(self):
        """Test different key types."""
        test_dict = {
            "string": 1,
            42: "number",
            (1, 2): "tuple",
        }
        assert test_dict["string"] == 1
        assert test_dict[42] == "number"
        assert test_dict[(1, 2)] == "tuple"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
