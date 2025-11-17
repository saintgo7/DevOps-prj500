#!/usr/bin/env python3
"""Program 09: Dictionaries - Master key-value mappings in Python."""

from typing import Dict, Any, List, Optional


def demonstrate_dict_creation() -> dict[str, Any]:
    """Demonstrate various ways to create dictionaries."""
    empty_dict = {}
    basic_dict = {"name": "Alice", "age": 25, "city": "NYC"}
    dict_constructor = dict(name="Bob", age=30, city="LA")
    from_tuples = dict([("a", 1), ("b", 2), ("c", 3)])
    dict_comprehension = {x: x**2 for x in range(5)}
    fromkeys = dict.fromkeys(["a", "b", "c"], 0)
    nested = {
        "person1": {"name": "Alice", "age": 25},
        "person2": {"name": "Bob", "age": 30}
    }

    return {
        "empty": empty_dict,
        "basic": basic_dict,
        "constructor": dict_constructor,
        "from_tuples": from_tuples,
        "comprehension": dict_comprehension,
        "fromkeys": fromkeys,
        "nested": nested,
    }


def demonstrate_accessing_elements() -> dict[str, Any]:
    """Demonstrate accessing dictionary elements."""
    person = {"name": "Alice", "age": 25, "city": "NYC"}

    # Access with []
    name = person["name"]

    # Access with get()
    age = person.get("age")
    country = person.get("country", "USA")  # default value

    # Keys, values, items
    keys = list(person.keys())
    values = list(person.values())
    items = list(person.items())

    # Check key existence
    has_name = "name" in person
    has_country = "country" in person

    return {
        "name_bracket": name,
        "age_get": age,
        "country_default": country,
        "keys": keys,
        "values": values,
        "items": items,
        "has_name": has_name,
        "has_country": has_country,
    }


def demonstrate_dict_methods() -> dict[str, Any]:
    """Demonstrate dictionary methods."""
    # Update
    dict1 = {"a": 1, "b": 2}
    dict1.update({"c": 3, "d": 4})
    dict1.update(e=5, f=6)

    # Pop
    dict2 = {"a": 1, "b": 2, "c": 3}
    popped = dict2.pop("b")
    popped_default = dict2.pop("z", "not found")

    # Popitem (removes last inserted)
    dict3 = {"a": 1, "b": 2, "c": 3}
    last_item = dict3.popitem()

    # Setdefault
    dict4 = {"a": 1, "b": 2}
    val1 = dict4.setdefault("a", 99)  # key exists
    val2 = dict4.setdefault("c", 3)   # key doesn't exist

    # Clear
    dict5 = {"a": 1, "b": 2}
    dict5.clear()

    # Copy
    dict6 = {"a": 1, "b": 2}
    dict6_copy = dict6.copy()

    return {
        "update": dict1,
        "pop": {"dict": dict2, "popped": popped, "default": popped_default},
        "popitem": {"dict": dict3, "item": last_item},
        "setdefault": {"dict": dict4, "val1": val1, "val2": val2},
        "clear": dict5,
        "copy": {"original": dict6, "copy": dict6_copy, "are_equal": dict6 == dict6_copy, "are_same": dict6 is dict6_copy},
    }


def demonstrate_dict_operations() -> dict[str, Any]:
    """Demonstrate dictionary operations."""
    # Merge (Python 3.9+)
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    merged = dict1 | dict2

    # Update with |=
    dict3 = {"a": 1, "b": 2}
    dict3 |= {"c": 3, "d": 4}

    # Length
    length = len(dict1)

    # Delete key
    dict4 = {"a": 1, "b": 2, "c": 3}
    del dict4["b"]

    # Iteration
    person = {"name": "Alice", "age": 25, "city": "NYC"}
    keys_list = [k for k in person]
    values_list = [v for v in person.values()]
    items_list = [(k, v) for k, v in person.items()]

    return {
        "merge": merged,
        "update_merge": dict3,
        "length": length,
        "delete": dict4,
        "iterate_keys": keys_list,
        "iterate_values": values_list,
        "iterate_items": items_list,
    }


def demonstrate_dict_comprehensions() -> dict[str, Any]:
    """Demonstrate dictionary comprehensions."""
    # Basic comprehension
    squares = {x: x**2 for x in range(6)}

    # With condition
    even_squares = {x: x**2 for x in range(10) if x % 2 == 0}

    # From two lists
    keys = ["a", "b", "c"]
    values = [1, 2, 3]
    combined = {k: v for k, v in zip(keys, values)}

    # Swap keys and values
    original = {"a": 1, "b": 2, "c": 3}
    swapped = {v: k for k, v in original.items()}

    # Conditional values
    numbers = {x: "even" if x % 2 == 0 else "odd" for x in range(6)}

    # Nested dict comprehension
    matrix_dict = {i: {j: i * j for j in range(1, 4)} for i in range(1, 4)}

    return {
        "squares": squares,
        "even_squares": even_squares,
        "combined": combined,
        "swapped": swapped,
        "conditional": numbers,
        "nested": matrix_dict,
    }


def demonstrate_nested_dicts() -> dict[str, Any]:
    """Demonstrate nested dictionary operations."""
    database = {
        "users": {
            "alice": {"age": 25, "city": "NYC"},
            "bob": {"age": 30, "city": "LA"}
        },
        "posts": {
            "post1": {"title": "Hello", "author": "alice"},
            "post2": {"title": "World", "author": "bob"}
        }
    }

    # Access nested values
    alice_age = database["users"]["alice"]["age"]
    post1_title = database["posts"]["post1"]["title"]

    # Safe nested access with get()
    bob_country = database.get("users", {}).get("bob", {}).get("country", "Unknown")

    # Modify nested values
    database_copy = {
        "users": {k: v.copy() for k, v in database["users"].items()},
        "posts": {k: v.copy() for k, v in database["posts"].items()}
    }
    database_copy["users"]["alice"]["age"] = 26

    return {
        "database": database,
        "alice_age": alice_age,
        "post1_title": post1_title,
        "bob_country": bob_country,
        "modified": database_copy,
    }


def demonstrate_defaultdict() -> dict[str, Any]:
    """Demonstrate defaultdict from collections."""
    from collections import defaultdict

    # Default int
    counts = defaultdict(int)
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    for word in words:
        counts[word] += 1

    # Default list
    groups = defaultdict(list)
    data = [("fruit", "apple"), ("veg", "carrot"), ("fruit", "banana"), ("veg", "spinach")]
    for category, item in data:
        groups[category].append(item)

    # Default dict
    nested = defaultdict(dict)
    nested["user1"]["name"] = "Alice"
    nested["user1"]["age"] = 25

    return {
        "counts": dict(counts),
        "groups": dict(groups),
        "nested": dict(nested),
    }


def demonstrate_counter() -> dict[str, Any]:
    """Demonstrate Counter from collections."""
    from collections import Counter

    # Count elements
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    counter = Counter(numbers)

    # Most common
    most_common = counter.most_common(2)

    # From string
    letter_count = Counter("hello world")

    # Operations
    c1 = Counter(["a", "b", "c", "a"])
    c2 = Counter(["a", "b", "d"])
    addition = c1 + c2
    subtraction = c1 - c2
    intersection = c1 & c2
    union = c1 | c2

    return {
        "counter": dict(counter),
        "most_common": most_common,
        "letters": dict(letter_count),
        "addition": dict(addition),
        "subtraction": dict(subtraction),
        "intersection": dict(intersection),
        "union": dict(union),
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 09: Dictionaries")
    print("=" * 60)

    print("\n1. Dictionary Creation:")
    creation = demonstrate_dict_creation()
    for key, value in creation.items():
        print(f"   {key}: {value}")

    print("\n2. Accessing Elements:")
    accessing = demonstrate_accessing_elements()
    for key, value in accessing.items():
        print(f"   {key}: {value}")

    print("\n3. Dictionary Methods:")
    methods = demonstrate_dict_methods()
    for key, value in methods.items():
        print(f"   {key}: {value}")

    print("\n4. Dictionary Operations:")
    operations = demonstrate_dict_operations()
    for key, value in operations.items():
        print(f"   {key}: {value}")

    print("\n5. Dictionary Comprehensions:")
    comprehensions = demonstrate_dict_comprehensions()
    for key, value in comprehensions.items():
        print(f"   {key}: {value}")

    print("\n6. Nested Dictionaries:")
    nested = demonstrate_nested_dicts()
    for key, value in nested.items():
        print(f"   {key}: {value}")

    print("\n7. DefaultDict:")
    defaultdict_demo = demonstrate_defaultdict()
    for key, value in defaultdict_demo.items():
        print(f"   {key}: {value}")

    print("\n8. Counter:")
    counter_demo = demonstrate_counter()
    for key, value in counter_demo.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
