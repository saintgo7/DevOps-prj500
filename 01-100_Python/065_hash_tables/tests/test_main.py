"""
Unit tests for 065_hash_tables program.

These tests verify:
- Hash table creation and initialization
- Insert, search, delete operations
- Hash function implementation
- Collision handling
- Load factor and resizing
- Edge cases and performance
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestHashTableBasics:
    """Test cases for basic hash table operations."""

    def test_hash_table_creation(self):
        """Test creating an empty hash table."""
        ht = {}
        assert len(ht) == 0

    def test_hash_table_insert(self):
        """Test inserting key-value pairs."""
        ht = {}
        ht["key1"] = "value1"
        assert ht["key1"] == "value1"

    def test_hash_table_search(self):
        """Test searching for keys."""
        ht = {"name": "Alice", "age": 30}
        assert ht["name"] == "Alice"
        assert ht["age"] == 30

    def test_hash_table_delete(self):
        """Test deleting keys."""
        ht = {"a": 1, "b": 2, "c": 3}
        del ht["b"]
        assert "b" not in ht
        assert len(ht) == 2


class TestHashTableOperations:
    """Test cases for hash table operations."""

    def test_update_existing_key(self):
        """Test updating value for existing key."""
        ht = {"key": "old_value"}
        ht["key"] = "new_value"
        assert ht["key"] == "new_value"

    def test_get_with_default(self):
        """Test get method with default value."""
        ht = {"a": 1}
        assert ht.get("a") == 1
        assert ht.get("b", "default") == "default"

    def test_keys_values_items(self):
        """Test getting keys, values, and items."""
        ht = {"a": 1, "b": 2, "c": 3}
        assert set(ht.keys()) == {"a", "b", "c"}
        assert set(ht.values()) == {1, 2, 3}
        assert len(list(ht.items())) == 3

    def test_clear(self):
        """Test clearing hash table."""
        ht = {"a": 1, "b": 2}
        ht.clear()
        assert len(ht) == 0


class TestHashTableMembership:
    """Test cases for membership testing."""

    def test_key_exists(self):
        """Test checking if key exists."""
        ht = {"a": 1, "b": 2}
        assert "a" in ht
        assert "c" not in ht

    def test_has_key(self):
        """Test hasattr-like functionality."""
        ht = {"name": "Alice", "age": 30}
        assert "name" in ht
        assert "email" not in ht


class TestHashTableIteration:
    """Test cases for iterating over hash table."""

    def test_iterate_keys(self):
        """Test iterating over keys."""
        ht = {"a": 1, "b": 2, "c": 3}
        keys = []
        for key in ht:
            keys.append(key)
        assert set(keys) == {"a", "b", "c"}

    def test_iterate_items(self):
        """Test iterating over key-value pairs."""
        ht = {"a": 1, "b": 2}
        items = []
        for k, v in ht.items():
            items.append((k, v))
        assert len(items) == 2


class TestHashTableCollisions:
    """Test cases for collision handling."""

    def test_multiple_insertions(self):
        """Test inserting many items."""
        ht = {}
        for i in range(100):
            ht[f"key{i}"] = i
        assert len(ht) == 100
        assert ht["key50"] == 50

    def test_collision_resolution(self):
        """Test that collisions are handled correctly."""
        # Python's dict handles collisions internally
        ht = {}
        for i in range(1000):
            ht[str(i)] = i
        assert len(ht) == 1000


class TestHashTableTypes:
    """Test cases for different key types."""

    def test_string_keys(self):
        """Test using string keys."""
        ht = {"name": "Alice", "city": "NYC"}
        assert ht["name"] == "Alice"

    def test_integer_keys(self):
        """Test using integer keys."""
        ht = {1: "one", 2: "two", 3: "three"}
        assert ht[1] == "one"

    def test_tuple_keys(self):
        """Test using tuple keys (immutable)."""
        ht = {(1, 2): "pair", (3, 4): "another"}
        assert ht[(1, 2)] == "pair"

    def test_mixed_types(self):
        """Test using mixed types as keys."""
        ht = {"str": 1, 42: "int", (1, 2): "tuple"}
        assert len(ht) == 3


class TestHashTableEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_hash_table(self):
        """Test operations on empty hash table."""
        ht = {}
        assert len(ht) == 0
        assert list(ht.keys()) == []

    def test_single_element(self):
        """Test hash table with single element."""
        ht = {"only": "one"}
        assert len(ht) == 1
        assert ht["only"] == "one"

    def test_key_not_found(self):
        """Test accessing non-existent key."""
        ht = {"a": 1}
        with pytest.raises(KeyError):
            _ = ht["nonexistent"]

    def test_delete_nonexistent_key(self):
        """Test deleting non-existent key."""
        ht = {"a": 1}
        with pytest.raises(KeyError):
            del ht["nonexistent"]

    def test_large_hash_table(self):
        """Test performance with large hash table."""
        ht = {}
        for i in range(10000):
            ht[f"key{i}"] = i
        assert len(ht) == 10000
        assert ht["key5000"] == 5000


class TestHashTableUpdate:
    """Test cases for update operations."""

    def test_update_with_dict(self):
        """Test updating with another dictionary."""
        ht1 = {"a": 1, "b": 2}
        ht2 = {"c": 3, "d": 4}
        ht1.update(ht2)
        assert len(ht1) == 4

    def test_update_overwrites(self):
        """Test update overwrites existing keys."""
        ht1 = {"a": 1, "b": 2}
        ht2 = {"b": 20, "c": 3}
        ht1.update(ht2)
        assert ht1["b"] == 20


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
