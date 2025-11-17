#!/usr/bin/env python3
"""Program 17: Modules - Master Python modules and imports."""

import sys
import os
import math
import random
import datetime
from typing import Any, List
import json
from collections import defaultdict, Counter
from itertools import combinations, permutations


def demonstrate_standard_library() -> dict[str, Any]:
    """Demonstrate standard library modules."""
    # Math module
    math_results = {
        "pi": math.pi,
        "sqrt_16": math.sqrt(16),
        "ceil_4_3": math.ceil(4.3),
        "floor_4_8": math.floor(4.8),
    }

    # Random module
    random.seed(42)  # For reproducibility
    random_results = {
        "randint": random.randint(1, 100),
        "choice": random.choice(["apple", "banana", "cherry"]),
        "random_float": random.random(),
    }

    # Datetime module
    now = datetime.datetime.now()
    datetime_results = {
        "current_year": now.year,
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
        "iso_format": now.isoformat(),
    }

    return {
        "math": math_results,
        "random": random_results,
        "datetime": datetime_results,
    }


def demonstrate_import_styles() -> dict[str, Any]:
    """Demonstrate different import styles."""
    # Standard import
    import string
    ascii_letters = string.ascii_lowercase[:5]

    # From import
    from string import ascii_uppercase
    uppercase = ascii_uppercase[:5]

    # Import as (alias)
    import statistics as stats
    mean_val = stats.mean([1, 2, 3, 4, 5])

    # Multiple imports
    from operator import add, mul, sub
    add_result = add(5, 3)
    mul_result = mul(5, 3)

    # Import all (generally not recommended)
    # from math import *  # Not shown due to best practices

    return {
        "lowercase": ascii_letters,
        "uppercase": uppercase,
        "mean": mean_val,
        "add": add_result,
        "multiply": mul_result,
        "note": "Prefer explicit imports over 'import *'",
    }


def demonstrate_module_attributes() -> dict[str, Any]:
    """Demonstrate module attributes."""
    # Module name
    module_name = __name__

    # Module file path
    module_file = __file__

    # Module docstring
    module_doc = __doc__[:50] if __doc__ else None

    # sys module attributes
    python_version = sys.version.split()[0]
    platform = sys.platform
    path_count = len(sys.path)

    return {
        "module_name": module_name,
        "module_file": os.path.basename(module_file),
        "module_doc": module_doc,
        "python_version": python_version,
        "platform": platform,
        "path_entries": path_count,
    }


def demonstrate_collections() -> dict[str, Any]:
    """Demonstrate collections module."""
    # defaultdict
    dd = defaultdict(int)
    for char in "hello world":
        dd[char] += 1

    # Counter
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    counter = Counter(words)
    most_common = counter.most_common(2)

    # namedtuple
    from collections import namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)

    # deque (double-ended queue)
    from collections import deque
    dq = deque([1, 2, 3])
    dq.appendleft(0)
    dq.append(4)

    return {
        "defaultdict": dict(dd),
        "counter": dict(counter),
        "most_common": most_common,
        "point": f"Point(x={p.x}, y={p.y})",
        "deque": list(dq),
    }


def demonstrate_itertools() -> dict[str, Any]:
    """Demonstrate itertools module."""
    # combinations
    items = [1, 2, 3, 4]
    combs = list(combinations(items, 2))

    # permutations
    perms = list(permutations([1, 2, 3], 2))

    # chain
    from itertools import chain
    chained = list(chain([1, 2], [3, 4], [5, 6]))

    # cycle (limited to avoid infinite loop)
    from itertools import cycle, islice
    cycled = list(islice(cycle([1, 2, 3]), 7))

    # repeat
    from itertools import repeat
    repeated = list(repeat(5, 3))

    # product
    from itertools import product
    prod = list(product([1, 2], ['a', 'b']))

    return {
        "combinations": combs[:5],
        "permutations": perms[:5],
        "chain": chained,
        "cycle": cycled,
        "repeat": repeated,
        "product": prod,
    }


def demonstrate_pathlib_module() -> dict[str, Any]:
    """Demonstrate pathlib module."""
    from pathlib import Path

    # Current file path
    current = Path(__file__)

    # Path operations
    parent = current.parent
    name = current.name
    stem = current.stem
    suffix = current.suffix

    # Create temp directory
    temp_dir = Path("temp_module_demo")
    temp_dir.mkdir(exist_ok=True)

    # Create a file
    temp_file = temp_dir / "test.txt"
    temp_file.write_text("Hello from pathlib!")

    # Read file
    content = temp_file.read_text()

    # Cleanup
    temp_file.unlink()
    temp_dir.rmdir()

    return {
        "current_name": name,
        "stem": stem,
        "suffix": suffix,
        "parent_name": parent.name,
        "file_content": content,
    }


def demonstrate_functools() -> dict[str, Any]:
    """Demonstrate functools module."""
    from functools import reduce, partial, lru_cache, wraps

    # reduce
    numbers = [1, 2, 3, 4, 5]
    product = reduce(lambda x, y: x * y, numbers)

    # partial
    def power(base, exponent):
        return base ** exponent

    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)

    # lru_cache
    @lru_cache(maxsize=128)
    def fibonacci(n: int) -> int:
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    fib_10 = fibonacci(10)
    cache_info = fibonacci.cache_info()

    return {
        "reduce_product": product,
        "square_5": square(5),
        "cube_3": cube(3),
        "fibonacci_10": fib_10,
        "cache_hits": cache_info.hits,
        "cache_size": cache_info.currsize,
    }


def demonstrate_os_sys() -> dict[str, Any]:
    """Demonstrate os and sys modules."""
    # os module
    cwd = os.getcwd()
    env_path = os.environ.get('PATH', 'Not found')[:50]

    # Create and remove directory
    test_dir = "temp_os_test"
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
    dir_exists = os.path.exists(test_dir)
    os.rmdir(test_dir)

    # sys module
    args_count = len(sys.argv)
    recursion_limit = sys.getrecursionlimit()

    return {
        "current_dir": os.path.basename(cwd),
        "path_prefix": env_path + "...",
        "dir_created": dir_exists,
        "argv_count": args_count,
        "recursion_limit": recursion_limit,
    }


def demonstrate_json_module() -> dict[str, Any]:
    """Demonstrate json module."""
    # Python to JSON
    data = {
        "name": "Alice",
        "age": 25,
        "hobbies": ["reading", "coding"],
        "active": True,
    }

    json_string = json.dumps(data)
    json_pretty = json.dumps(data, indent=2)

    # JSON to Python
    parsed = json.loads(json_string)

    # Write to file
    temp_file = Path("temp_json.json")
    with temp_file.open("w") as f:
        json.dump(data, f)

    # Read from file
    with temp_file.open("r") as f:
        loaded = json.load(f)

    # Cleanup
    temp_file.unlink()

    return {
        "original": data,
        "json_compact": json_string,
        "parsed_equal": parsed == data,
        "loaded_equal": loaded == data,
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 17: Modules")
    print("=" * 60)

    print("\n1. Standard Library:")
    stdlib = demonstrate_standard_library()
    for key, value in stdlib.items():
        print(f"   {key}: {value}")

    print("\n2. Import Styles:")
    imports = demonstrate_import_styles()
    for key, value in imports.items():
        print(f"   {key}: {value}")

    print("\n3. Module Attributes:")
    attributes = demonstrate_module_attributes()
    for key, value in attributes.items():
        print(f"   {key}: {value}")

    print("\n4. Collections Module:")
    collections_demo = demonstrate_collections()
    for key, value in collections_demo.items():
        print(f"   {key}: {value}")

    print("\n5. Itertools Module:")
    itertools_demo = demonstrate_itertools()
    for key, value in itertools_demo.items():
        print(f"   {key}: {value}")

    print("\n6. Pathlib Module:")
    pathlib_demo = demonstrate_pathlib_module()
    for key, value in pathlib_demo.items():
        print(f"   {key}: {value}")

    print("\n7. Functools Module:")
    functools_demo = demonstrate_functools()
    for key, value in functools_demo.items():
        print(f"   {key}: {value}")

    print("\n8. OS and Sys Modules:")
    os_sys = demonstrate_os_sys()
    for key, value in os_sys.items():
        print(f"   {key}: {value}")

    print("\n9. JSON Module:")
    json_demo = demonstrate_json_module()
    for key, value in json_demo.items():
        if key != "json_compact":
            print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
