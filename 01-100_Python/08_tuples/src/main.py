#!/usr/bin/env python3
"""Program 08: Tuples - Master immutable sequences in Python."""

from typing import Tuple, Any, List


def demonstrate_tuple_creation() -> dict[str, Any]:
    """Demonstrate various ways to create tuples."""
    empty_tuple = ()
    single = (1,)  # Note the comma
    numbers = (1, 2, 3, 4, 5)
    mixed = (1, "hello", 3.14, True, None)
    nested = ((1, 2), (3, 4), (5, 6))
    without_parens = 1, 2, 3
    from_list = tuple([1, 2, 3, 4, 5])
    from_string = tuple("hello")

    return {
        "empty": empty_tuple,
        "single": single,
        "numbers": numbers,
        "mixed_types": mixed,
        "nested": nested,
        "without_parens": without_parens,
        "from_list": from_list,
        "from_string": from_string,
    }


def demonstrate_indexing_slicing() -> dict[str, Any]:
    """Demonstrate tuple indexing and slicing."""
    numbers = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)

    return {
        "first": numbers[0],
        "last": numbers[-1],
        "third": numbers[2],
        "slice_2_5": numbers[2:5],
        "slice_start": numbers[:3],
        "slice_end": numbers[7:],
        "slice_step": numbers[::2],
        "reverse": numbers[::-1],
        "negative_slice": numbers[-3:],
    }


def demonstrate_tuple_methods() -> dict[str, Any]:
    """Demonstrate tuple methods."""
    numbers = (1, 2, 3, 2, 4, 2, 5)

    # Count
    count_2 = numbers.count(2)
    count_5 = numbers.count(5)
    count_10 = numbers.count(10)

    # Index
    index_2 = numbers.index(2)
    index_5 = numbers.index(5)

    return {
        "tuple": numbers,
        "count_2": count_2,
        "count_5": count_5,
        "count_10": count_10,
        "index_2": index_2,
        "index_5": index_5,
    }


def demonstrate_tuple_operations() -> dict[str, Any]:
    """Demonstrate tuple operations."""
    # Concatenation
    tuple1 = (1, 2, 3)
    tuple2 = (4, 5, 6)
    concatenated = tuple1 + tuple2

    # Repetition
    repeated = (1, 2) * 3

    # Membership
    numbers = (1, 2, 3, 4, 5)
    has_3 = 3 in numbers
    has_10 = 10 in numbers

    # Length
    length = len(numbers)

    # Min/Max/Sum
    min_val = min(numbers)
    max_val = max(numbers)
    sum_val = sum(numbers)

    # Comparison
    t1 = (1, 2, 3)
    t2 = (1, 2, 4)
    t3 = (1, 2, 3)

    return {
        "concatenation": concatenated,
        "repetition": repeated,
        "membership": {"has_3": has_3, "has_10": has_10},
        "length": length,
        "min": min_val,
        "max": max_val,
        "sum": sum_val,
        "comparison": {"t1_lt_t2": t1 < t2, "t1_eq_t3": t1 == t3},
    }


def demonstrate_tuple_unpacking() -> dict[str, Any]:
    """Demonstrate tuple unpacking."""
    # Basic unpacking
    point = (10, 20)
    x, y = point

    # Multiple assignment
    a, b, c = 1, 2, 3

    # Swap values
    x1, y1 = 5, 10
    x1, y1 = y1, x1

    # Extended unpacking
    numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    first, second, *rest = numbers
    first2, *middle, last = numbers

    # Nested unpacking
    nested = ((1, 2), (3, 4))
    (a1, b1), (c1, d1) = nested

    # Function returns
    def get_stats() -> Tuple[int, int, float]:
        nums = [1, 2, 3, 4, 5]
        return min(nums), max(nums), sum(nums) / len(nums)

    minimum, maximum, average = get_stats()

    return {
        "basic": {"x": x, "y": y},
        "multiple": {"a": a, "b": b, "c": c},
        "swapped": {"x": x1, "y": y1},
        "extended": {"first": first, "second": second, "rest": rest},
        "extended2": {"first": first2, "middle": middle, "last": last},
        "nested": {"a": a1, "b": b1, "c": c1, "d": d1},
        "function_return": {"min": minimum, "max": maximum, "avg": average},
    }


def demonstrate_immutability() -> dict[str, Any]:
    """Demonstrate tuple immutability."""
    # Tuples are immutable
    numbers = (1, 2, 3, 4, 5)

    # But mutable objects inside tuples can be modified
    mixed = ([1, 2, 3], [4, 5, 6])
    mixed[0].append(99)  # This works!

    # Converting to list, modifying, converting back
    numbers_list = list(numbers)
    numbers_list.append(6)
    new_tuple = tuple(numbers_list)

    return {
        "original_tuple": numbers,
        "mixed_after_modify": mixed,
        "new_tuple": new_tuple,
        "immutable_note": "Tuples cannot be modified directly",
    }


def demonstrate_nested_tuples() -> dict[str, Any]:
    """Demonstrate nested tuple operations."""
    matrix = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9)
    )

    # Access elements
    first_row = matrix[0]
    element_2_2 = matrix[1][1]

    # Convert to list for modification
    matrix_list = [list(row) for row in matrix]
    matrix_list[0][0] = 99
    matrix_modified = tuple(tuple(row) for row in matrix_list)

    # Flatten
    flattened = tuple(item for row in matrix for item in row)

    return {
        "original": matrix,
        "first_row": first_row,
        "element_2_2": element_2_2,
        "modified": matrix_modified,
        "flattened": flattened,
    }


def demonstrate_tuple_vs_list() -> dict[str, Any]:
    """Demonstrate differences between tuples and lists."""
    # Memory efficiency
    import sys
    lst = [1, 2, 3, 4, 5]
    tpl = (1, 2, 3, 4, 5)

    list_size = sys.getsizeof(lst)
    tuple_size = sys.getsizeof(tpl)

    # Hashable (can be used as dict keys)
    dict_with_tuple_key = {(1, 2): "value"}

    # Performance (tuples are faster to create)
    # Use case: return values, data integrity

    return {
        "list_size_bytes": list_size,
        "tuple_size_bytes": tuple_size,
        "memory_diff": list_size - tuple_size,
        "tuple_as_key": dict_with_tuple_key,
        "hashable": "Tuples are hashable, lists are not",
        "use_cases": {
            "tuple": "Immutable data, dict keys, function returns",
            "list": "Mutable collections, frequent modifications"
        }
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 08: Tuples")
    print("=" * 60)

    print("\n1. Tuple Creation:")
    creation = demonstrate_tuple_creation()
    for key, value in creation.items():
        print(f"   {key}: {value}")

    print("\n2. Indexing and Slicing:")
    indexing = demonstrate_indexing_slicing()
    for key, value in indexing.items():
        print(f"   {key}: {value}")

    print("\n3. Tuple Methods:")
    methods = demonstrate_tuple_methods()
    for key, value in methods.items():
        print(f"   {key}: {value}")

    print("\n4. Tuple Operations:")
    operations = demonstrate_tuple_operations()
    for key, value in operations.items():
        print(f"   {key}: {value}")

    print("\n5. Tuple Unpacking:")
    unpacking = demonstrate_tuple_unpacking()
    for key, value in unpacking.items():
        print(f"   {key}: {value}")

    print("\n6. Immutability:")
    immutability = demonstrate_immutability()
    for key, value in immutability.items():
        print(f"   {key}: {value}")

    print("\n7. Nested Tuples:")
    nested = demonstrate_nested_tuples()
    for key, value in nested.items():
        print(f"   {key}: {value}")

    print("\n8. Tuple vs List:")
    comparison = demonstrate_tuple_vs_list()
    for key, value in comparison.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
