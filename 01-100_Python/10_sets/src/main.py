#!/usr/bin/env python3
"""Program 10: Sets - Master unordered collections of unique elements."""

from typing import Set, Any, List


def demonstrate_set_creation() -> dict[str, Any]:
    """Demonstrate various ways to create sets."""
    empty_set = set()  # Note: {} creates empty dict, not set
    numbers = {1, 2, 3, 4, 5}
    from_list = set([1, 2, 2, 3, 3, 3, 4, 5])  # Duplicates removed
    from_string = set("hello")  # Unique characters
    from_tuple = set((1, 2, 3, 2, 1))
    set_comprehension = {x**2 for x in range(6)}
    mixed_types = {1, "hello", 3.14, True}

    return {
        "empty": empty_set,
        "numbers": numbers,
        "from_list_deduped": from_list,
        "from_string": from_string,
        "from_tuple": from_tuple,
        "comprehension": set_comprehension,
        "mixed_types": mixed_types,
    }


def demonstrate_set_methods() -> dict[str, Any]:
    """Demonstrate set methods."""
    # Add
    set1 = {1, 2, 3}
    set1.add(4)
    set1.add(2)  # No effect, already exists

    # Update (add multiple)
    set2 = {1, 2, 3}
    set2.update([4, 5, 6])
    set2.update({7, 8}, [9, 10])

    # Remove (raises KeyError if not found)
    set3 = {1, 2, 3, 4, 5}
    set3.remove(3)

    # Discard (no error if not found)
    set4 = {1, 2, 3, 4, 5}
    set4.discard(3)
    set4.discard(99)  # No error

    # Pop (removes and returns arbitrary element)
    set5 = {1, 2, 3, 4, 5}
    popped = set5.pop()

    # Clear
    set6 = {1, 2, 3}
    set6.clear()

    # Copy
    set7 = {1, 2, 3}
    set7_copy = set7.copy()

    return {
        "add": set1,
        "update": set2,
        "remove": set3,
        "discard": set4,
        "pop": {"set": set5, "popped": popped},
        "clear": set6,
        "copy": {"original": set7, "copy": set7_copy},
    }


def demonstrate_set_operations() -> dict[str, Any]:
    """Demonstrate mathematical set operations."""
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}

    # Union (elements in either set)
    union1 = set_a | set_b
    union2 = set_a.union(set_b)

    # Intersection (elements in both sets)
    intersection1 = set_a & set_b
    intersection2 = set_a.intersection(set_b)

    # Difference (elements in first but not second)
    difference1 = set_a - set_b
    difference2 = set_a.difference(set_b)

    # Symmetric difference (elements in either but not both)
    sym_diff1 = set_a ^ set_b
    sym_diff2 = set_a.symmetric_difference(set_b)

    # Multiple sets
    set_c = {3, 4, 5, 6}
    multi_union = set_a.union(set_b, set_c)
    multi_intersection = set_a.intersection(set_b, set_c)

    return {
        "set_a": set_a,
        "set_b": set_b,
        "union": union1,
        "intersection": intersection1,
        "difference_a_b": difference1,
        "difference_b_a": set_b - set_a,
        "symmetric_difference": sym_diff1,
        "multi_union": multi_union,
        "multi_intersection": multi_intersection,
    }


def demonstrate_set_comparisons() -> dict[str, Any]:
    """Demonstrate set comparison operations."""
    set_a = {1, 2, 3}
    set_b = {1, 2, 3, 4, 5}
    set_c = {1, 2, 3}
    set_d = {4, 5, 6}

    # Subset
    is_subset = set_a <= set_b  # or set_a.issubset(set_b)
    is_proper_subset = set_a < set_b

    # Superset
    is_superset = set_b >= set_a  # or set_b.issuperset(set_a)
    is_proper_superset = set_b > set_a

    # Equality
    is_equal = set_a == set_c

    # Disjoint (no common elements)
    is_disjoint = set_a.isdisjoint(set_d)

    return {
        "set_a": set_a,
        "set_b": set_b,
        "set_c": set_c,
        "set_d": set_d,
        "a_subset_of_b": is_subset,
        "a_proper_subset_of_b": is_proper_subset,
        "b_superset_of_a": is_superset,
        "b_proper_superset_of_a": is_proper_superset,
        "a_equals_c": is_equal,
        "a_disjoint_d": is_disjoint,
    }


def demonstrate_set_comprehensions() -> dict[str, Any]:
    """Demonstrate set comprehensions."""
    # Basic comprehension
    squares = {x**2 for x in range(10)}

    # With condition
    even_squares = {x**2 for x in range(10) if x % 2 == 0}

    # From string
    vowels = {char.lower() for char in "Hello World" if char.lower() in "aeiou"}

    # Mathematical sets
    multiples_3 = {x for x in range(1, 31) if x % 3 == 0}
    multiples_5 = {x for x in range(1, 31) if x % 5 == 0}
    multiples_3_or_5 = multiples_3 | multiples_5

    return {
        "squares": squares,
        "even_squares": even_squares,
        "vowels": vowels,
        "multiples_3": multiples_3,
        "multiples_5": multiples_5,
        "multiples_3_or_5": multiples_3_or_5,
    }


def demonstrate_frozenset() -> dict[str, Any]:
    """Demonstrate frozenset (immutable set)."""
    # Create frozenset
    frozen = frozenset([1, 2, 3, 4, 5])

    # Can be used as dict key or set element
    dict_with_frozen_key = {frozen: "value"}
    set_of_frozen = {frozenset([1, 2]), frozenset([3, 4])}

    # Supports all query operations
    frozen_a = frozenset([1, 2, 3])
    frozen_b = frozenset([3, 4, 5])
    union = frozen_a | frozen_b
    intersection = frozen_a & frozen_b

    # Cannot be modified (no add, remove, etc.)

    return {
        "frozen": frozen,
        "as_dict_key": dict_with_frozen_key,
        "set_of_frozensets": set_of_frozen,
        "union": union,
        "intersection": intersection,
        "is_immutable": "frozenset cannot be modified after creation",
    }


def demonstrate_set_use_cases() -> dict[str, Any]:
    """Demonstrate practical use cases for sets."""
    # Remove duplicates
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 5]
    unique = list(set(numbers))

    # Membership testing (faster than list)
    allowed_users = {"alice", "bob", "charlie"}
    is_allowed = "alice" in allowed_users

    # Find common elements
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]
    common = list(set(list1) & set(list2))

    # Find unique elements
    unique_to_list1 = list(set(list1) - set(list2))
    unique_to_list2 = list(set(list2) - set(list1))

    # Find all unique elements
    all_unique = list(set(list1) ^ set(list2))

    # Count unique words
    text = "hello world hello python world"
    unique_words = set(text.split())
    word_count = len(unique_words)

    return {
        "remove_duplicates": unique,
        "membership_test": is_allowed,
        "common_elements": common,
        "unique_to_list1": unique_to_list1,
        "unique_to_list2": unique_to_list2,
        "all_unique": all_unique,
        "unique_words": unique_words,
        "unique_word_count": word_count,
    }


def demonstrate_set_patterns() -> dict[str, Any]:
    """Demonstrate common set patterns."""
    # Filter duplicates while preserving order (Python 3.7+)
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    seen = set()
    unique_ordered = []
    for num in numbers:
        if num not in seen:
            seen.add(num)
            unique_ordered.append(num)

    # Set operations on multiple collections
    sets = [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]
    intersection_all = set.intersection(*sets)
    union_all = set.union(*sets)

    # Filtering with sets
    valid_ids = {1, 3, 5, 7, 9}
    data = [
        {"id": 1, "value": "a"},
        {"id": 2, "value": "b"},
        {"id": 3, "value": "c"},
        {"id": 4, "value": "d"},
        {"id": 5, "value": "e"},
    ]
    filtered = [item for item in data if item["id"] in valid_ids]

    return {
        "unique_ordered": unique_ordered,
        "intersection_all": intersection_all,
        "union_all": union_all,
        "filtered_data": filtered,
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 10: Sets")
    print("=" * 60)

    print("\n1. Set Creation:")
    creation = demonstrate_set_creation()
    for key, value in creation.items():
        print(f"   {key}: {value}")

    print("\n2. Set Methods:")
    methods = demonstrate_set_methods()
    for key, value in methods.items():
        print(f"   {key}: {value}")

    print("\n3. Set Operations:")
    operations = demonstrate_set_operations()
    for key, value in operations.items():
        print(f"   {key}: {value}")

    print("\n4. Set Comparisons:")
    comparisons = demonstrate_set_comparisons()
    for key, value in comparisons.items():
        print(f"   {key}: {value}")

    print("\n5. Set Comprehensions:")
    comprehensions = demonstrate_set_comprehensions()
    for key, value in comprehensions.items():
        print(f"   {key}: {value}")

    print("\n6. Frozenset:")
    frozenset_demo = demonstrate_frozenset()
    for key, value in frozenset_demo.items():
        print(f"   {key}: {value}")

    print("\n7. Use Cases:")
    use_cases = demonstrate_set_use_cases()
    for key, value in use_cases.items():
        print(f"   {key}: {value}")

    print("\n8. Common Patterns:")
    patterns = demonstrate_set_patterns()
    for key, value in patterns.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
