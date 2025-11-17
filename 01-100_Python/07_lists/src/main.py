#!/usr/bin/env python3
"""Program 07: Lists - Master Python list operations and methods."""

from typing import List, Any, Optional


def demonstrate_list_creation() -> dict[str, Any]:
    """Demonstrate various ways to create lists."""
    empty_list = []
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True, None]
    nested = [[1, 2], [3, 4], [5, 6]]
    range_list = list(range(1, 6))
    repeated = [0] * 5
    comprehension = [x * 2 for x in range(5)]

    return {
        "empty": empty_list,
        "numbers": numbers,
        "mixed_types": mixed,
        "nested": nested,
        "from_range": range_list,
        "repeated": repeated,
        "comprehension": comprehension,
    }


def demonstrate_indexing_slicing() -> dict[str, Any]:
    """Demonstrate list indexing and slicing."""
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

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


def demonstrate_list_methods() -> dict[str, Any]:
    """Demonstrate common list methods."""
    # Append
    lst1 = [1, 2, 3]
    lst1.append(4)

    # Extend
    lst2 = [1, 2, 3]
    lst2.extend([4, 5, 6])

    # Insert
    lst3 = [1, 2, 4]
    lst3.insert(2, 3)

    # Remove
    lst4 = [1, 2, 3, 2]
    lst4.remove(2)

    # Pop
    lst5 = [1, 2, 3, 4]
    popped = lst5.pop()
    popped_index = lst5.pop(1)

    # Index
    lst6 = [10, 20, 30, 20]
    index = lst6.index(20)

    # Count
    lst7 = [1, 2, 2, 3, 2, 4]
    count = lst7.count(2)

    # Sort
    lst8 = [3, 1, 4, 1, 5, 9, 2, 6]
    lst8.sort()
    lst9 = [3, 1, 4, 1, 5, 9, 2, 6]
    lst9.sort(reverse=True)

    # Reverse
    lst10 = [1, 2, 3, 4, 5]
    lst10.reverse()

    # Clear
    lst11 = [1, 2, 3]
    lst11.clear()

    # Copy
    lst12 = [1, 2, 3]
    lst12_copy = lst12.copy()

    return {
        "append": lst1,
        "extend": lst2,
        "insert": lst3,
        "remove": lst4,
        "pop": {"list": lst5, "popped": popped, "popped_index": popped_index},
        "index": index,
        "count": count,
        "sort_asc": lst8,
        "sort_desc": lst9,
        "reverse": lst10,
        "clear": lst11,
        "copy": {"original": lst12, "copy": lst12_copy, "are_equal": lst12 == lst12_copy, "are_same": lst12 is lst12_copy},
    }


def demonstrate_list_operations() -> dict[str, Any]:
    """Demonstrate list operations."""
    # Concatenation
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    concatenated = list1 + list2

    # Repetition
    repeated = [1, 2] * 3

    # Membership
    numbers = [1, 2, 3, 4, 5]
    has_3 = 3 in numbers
    has_10 = 10 in numbers

    # Length
    length = len(numbers)

    # Min/Max/Sum
    min_val = min(numbers)
    max_val = max(numbers)
    sum_val = sum(numbers)

    # Iteration
    doubled = [x * 2 for x in numbers]

    return {
        "concatenation": concatenated,
        "repetition": repeated,
        "membership": {"has_3": has_3, "has_10": has_10},
        "length": length,
        "min": min_val,
        "max": max_val,
        "sum": sum_val,
        "doubled": doubled,
    }


def demonstrate_list_comprehensions() -> dict[str, Any]:
    """Demonstrate list comprehensions."""
    # Basic comprehension
    squares = [x**2 for x in range(10)]

    # With condition
    evens = [x for x in range(20) if x % 2 == 0]

    # With if-else
    even_odd = ["even" if x % 2 == 0 else "odd" for x in range(10)]

    # Nested comprehension
    matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]

    # Flatten nested list
    nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [item for sublist in nested for item in sublist]

    # String manipulation
    words = ["hello", "world", "python"]
    uppercase = [word.upper() for word in words]

    return {
        "squares": squares,
        "evens": evens,
        "even_odd": even_odd,
        "matrix": matrix,
        "flattened": flattened,
        "uppercase": uppercase,
    }


def demonstrate_nested_lists() -> dict[str, Any]:
    """Demonstrate nested list operations."""
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    # Access elements
    first_row = matrix[0]
    element_2_2 = matrix[1][1]

    # Modify elements
    matrix_copy = [row[:] for row in matrix]
    matrix_copy[0][0] = 99

    # Transpose
    transposed = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    # Flatten
    flattened = [item for row in matrix for item in row]

    return {
        "original": matrix,
        "first_row": first_row,
        "element_2_2": element_2_2,
        "modified": matrix_copy,
        "transposed": transposed,
        "flattened": flattened,
    }


def demonstrate_list_patterns() -> dict[str, Any]:
    """Demonstrate common list patterns."""
    # Filter
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = list(filter(lambda x: x % 2 == 0, numbers))

    # Map
    doubled = list(map(lambda x: x * 2, numbers))

    # Zip
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    zipped = list(zip(names, ages))

    # Enumerate
    enumerated = list(enumerate(names))

    # Sorted (non-mutating)
    unsorted = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_asc = sorted(unsorted)
    sorted_desc = sorted(unsorted, reverse=True)

    # Reversed
    reversed_list = list(reversed(numbers))

    # Any/All
    has_even = any(x % 2 == 0 for x in numbers)
    all_positive = all(x > 0 for x in numbers)

    return {
        "filter_evens": evens,
        "map_doubled": doubled,
        "zip": zipped,
        "enumerate": enumerated,
        "sorted_asc": sorted_asc,
        "sorted_desc": sorted_desc,
        "reversed": reversed_list,
        "has_even": has_even,
        "all_positive": all_positive,
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 07: Lists")
    print("=" * 60)

    print("\n1. List Creation:")
    creation = demonstrate_list_creation()
    for key, value in creation.items():
        print(f"   {key}: {value}")

    print("\n2. Indexing and Slicing:")
    indexing = demonstrate_indexing_slicing()
    for key, value in indexing.items():
        print(f"   {key}: {value}")

    print("\n3. List Methods:")
    methods = demonstrate_list_methods()
    for key, value in methods.items():
        print(f"   {key}: {value}")

    print("\n4. List Operations:")
    operations = demonstrate_list_operations()
    for key, value in operations.items():
        print(f"   {key}: {value}")

    print("\n5. List Comprehensions:")
    comprehensions = demonstrate_list_comprehensions()
    for key, value in comprehensions.items():
        print(f"   {key}: {value}")

    print("\n6. Nested Lists:")
    nested = demonstrate_nested_lists()
    for key, value in nested.items():
        print(f"   {key}: {value}")

    print("\n7. Common Patterns:")
    patterns = demonstrate_list_patterns()
    for key, value in patterns.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
