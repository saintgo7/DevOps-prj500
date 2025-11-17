#!/usr/bin/env python3
"""Program 20: Generators - Master lazy evaluation and generator patterns."""

import sys
from typing import Iterator, Generator, Any
from itertools import islice


def demonstrate_basic_generator() -> dict[str, Any]:
    """Demonstrate basic generator function."""

    def count_up_to(n: int) -> Generator[int, None, None]:
        """Generate numbers from 1 to n."""
        count = 1
        while count <= n:
            yield count
            count += 1

    # Create generator
    gen = count_up_to(5)

    # Consume generator
    numbers = list(gen)

    # Generator exhausted after first use
    numbers_again = list(gen)

    return {
        "numbers": numbers,
        "after_exhausted": numbers_again,
        "note": "Generators produce values lazily, one at a time",
    }


def demonstrate_yield_vs_return() -> dict[str, Any]:
    """Demonstrate difference between yield and return."""

    # Regular function with return
    def get_list(n: int) -> list[int]:
        """Return entire list at once."""
        result = []
        for i in range(n):
            result.append(i ** 2)
        return result

    # Generator with yield
    def get_generator(n: int) -> Generator[int, None, None]:
        """Yield values one at a time."""
        for i in range(n):
            yield i ** 2

    # Memory comparison
    list_result = get_list(5)
    gen_result = get_generator(5)

    # Generator doesn't compute all values upfront
    gen_list = list(gen_result)

    return {
        "list_result": list_result,
        "generator_result": gen_list,
        "are_equal": list_result == gen_list,
        "key_difference": "Generator computes on-demand, saves memory",
    }


def demonstrate_generator_expressions() -> dict[str, Any]:
    """Demonstrate generator expressions."""

    # List comprehension (eager)
    list_comp = [x ** 2 for x in range(10)]

    # Generator expression (lazy)
    gen_exp = (x ** 2 for x in range(10))

    # Generator expression doesn't compute until needed
    gen_list = list(gen_exp)

    # Memory efficient for large datasets
    large_gen = (x for x in range(1_000_000))
    first_five = list(islice(large_gen, 5))

    # Chaining generators
    numbers = (x for x in range(20))
    evens = (x for x in numbers if x % 2 == 0)
    squares = (x ** 2 for x in evens)
    result = list(squares)

    return {
        "list_comp": list_comp,
        "gen_exp": gen_list,
        "first_five_large": first_five,
        "chained_result": result,
        "syntax": "() for generator, [] for list",
    }


def demonstrate_infinite_generators() -> dict[str, Any]:
    """Demonstrate infinite generators."""

    def infinite_counter(start: int = 0) -> Generator[int, None, None]:
        """Generate infinite sequence of numbers."""
        count = start
        while True:
            yield count
            count += 1

    def fibonacci() -> Generator[int, None, None]:
        """Generate infinite Fibonacci sequence."""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    # Take first 10 from infinite counter
    counter = infinite_counter(1)
    first_ten = list(islice(counter, 10))

    # Take first 10 Fibonacci numbers
    fib = fibonacci()
    fib_ten = list(islice(fib, 10))

    return {
        "counter": first_ten,
        "fibonacci": fib_ten,
        "note": "Infinite generators possible due to lazy evaluation",
    }


def demonstrate_generator_pipeline() -> dict[str, Any]:
    """Demonstrate generator pipeline pattern."""

    def read_data() -> Generator[int, None, None]:
        """Simulate reading data."""
        for i in range(1, 21):
            yield i

    def filter_even(numbers: Generator[int, None, None]) -> Generator[int, None, None]:
        """Filter even numbers."""
        for num in numbers:
            if num % 2 == 0:
                yield num

    def square(numbers: Generator[int, None, None]) -> Generator[int, None, None]:
        """Square each number."""
        for num in numbers:
            yield num ** 2

    def limit(numbers: Generator[int, None, None], n: int) -> Generator[int, None, None]:
        """Limit to first n items."""
        for i, num in enumerate(numbers):
            if i >= n:
                break
            yield num

    # Build pipeline
    pipeline = limit(square(filter_even(read_data())), 5)
    result = list(pipeline)

    return {
        "result": result,
        "note": "Pipelines process data lazily, memory efficient",
        "pattern": "read -> filter -> transform -> limit",
    }


def demonstrate_send_method() -> dict[str, Any]:
    """Demonstrate generator.send() method."""

    def running_average() -> Generator[float, float, None]:
        """Calculate running average."""
        total = 0.0
        count = 0
        average = 0.0

        while True:
            value = yield average
            if value is not None:
                total += value
                count += 1
                average = total / count

    avg = running_average()
    next(avg)  # Prime the generator

    avg1 = avg.send(10)
    avg2 = avg.send(20)
    avg3 = avg.send(30)

    return {
        "after_10": avg1,
        "after_20": avg2,
        "after_30": avg3,
        "note": "send() allows bi-directional communication",
    }


def demonstrate_generator_close() -> dict[str, Any]:
    """Demonstrate generator cleanup with close()."""

    def managed_resource() -> Generator[str, None, None]:
        """Generator with cleanup."""
        print("Opening resource")
        try:
            for i in range(5):
                yield f"Item {i}"
        finally:
            print("Closing resource")

    gen = managed_resource()
    items = [next(gen), next(gen)]

    # Close generator (triggers finally block)
    gen.close()

    # Try to use closed generator
    error_caught = False
    try:
        next(gen)
    except StopIteration:
        error_caught = True

    return {
        "items_retrieved": items,
        "closed_properly": error_caught,
        "note": "close() triggers finally block for cleanup",
    }


def demonstrate_generator_delegation() -> dict[str, Any]:
    """Demonstrate yield from for generator delegation."""

    def gen1() -> Generator[int, None, None]:
        """First generator."""
        yield 1
        yield 2
        yield 3

    def gen2() -> Generator[int, None, None]:
        """Second generator."""
        yield 4
        yield 5
        yield 6

    # Without yield from
    def combined_old() -> Generator[int, None, None]:
        """Combine generators the old way."""
        for value in gen1():
            yield value
        for value in gen2():
            yield value

    # With yield from (Python 3.3+)
    def combined_new() -> Generator[int, None, None]:
        """Combine generators with yield from."""
        yield from gen1()
        yield from gen2()

    old_result = list(combined_old())
    new_result = list(combined_new())

    return {
        "old_style": old_result,
        "new_style": new_result,
        "are_equal": old_result == new_result,
        "note": "'yield from' delegates to sub-generator",
    }


def demonstrate_practical_generators() -> dict[str, Any]:
    """Demonstrate practical generator use cases."""

    # File processing (memory efficient)
    def process_large_file(filename: str) -> Generator[str, None, None]:
        """Process file line by line without loading all in memory."""
        with open(filename) as f:
            for line in f:
                yield line.strip().upper()

    # Batch processing
    def batch_data(data: list, batch_size: int) -> Generator[list, None, None]:
        """Split data into batches."""
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]

    data = list(range(20))
    batches = list(batch_data(data, 5))

    # Tree traversal
    class Node:
        def __init__(self, value: int, children: list = None):
            self.value = value
            self.children = children or []

    def traverse(node: Node) -> Generator[int, None, None]:
        """Traverse tree and yield all values."""
        yield node.value
        for child in node.children:
            yield from traverse(child)

    tree = Node(1, [Node(2, [Node(4), Node(5)]), Node(3)])
    tree_values = list(traverse(tree))

    return {
        "batches": batches,
        "batch_count": len(batches),
        "tree_traversal": tree_values,
        "note": "Generators excellent for large data, streaming, trees",
    }


def demonstrate_memory_efficiency() -> dict[str, Any]:
    """Demonstrate memory efficiency of generators."""

    # List approach (uses memory for all items)
    def squares_list(n: int) -> list[int]:
        return [x ** 2 for x in range(n)]

    # Generator approach (uses minimal memory)
    def squares_gen(n: int) -> Generator[int, None, None]:
        for x in range(n):
            yield x ** 2

    # Memory size comparison
    n = 1000
    list_obj = squares_list(n)
    gen_obj = squares_gen(n)

    list_size = sys.getsizeof(list_obj)
    gen_size = sys.getsizeof(gen_obj)

    # Sum using generator (doesn't store all values)
    sum_gen = sum(squares_gen(n))
    sum_list = sum(list_obj)

    return {
        "list_size_bytes": list_size,
        "gen_size_bytes": gen_size,
        "memory_saved": list_size - gen_size,
        "sums_equal": sum_gen == sum_list,
        "note": f"Generator uses {gen_size/list_size*100:.1f}% of list memory",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 20: Generators")
    print("=" * 60)

    print("\n1. Basic Generator:")
    basic = demonstrate_basic_generator()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Yield vs Return:")
    yield_return = demonstrate_yield_vs_return()
    for key, value in yield_return.items():
        print(f"   {key}: {value}")

    print("\n3. Generator Expressions:")
    gen_exp = demonstrate_generator_expressions()
    for key, value in gen_exp.items():
        print(f"   {key}: {value}")

    print("\n4. Infinite Generators:")
    infinite = demonstrate_infinite_generators()
    for key, value in infinite.items():
        print(f"   {key}: {value}")

    print("\n5. Generator Pipeline:")
    pipeline = demonstrate_generator_pipeline()
    for key, value in pipeline.items():
        print(f"   {key}: {value}")

    print("\n6. Generator send():")
    send = demonstrate_send_method()
    for key, value in send.items():
        print(f"   {key}: {value}")

    print("\n7. Generator close():")
    close = demonstrate_generator_close()
    for key, value in close.items():
        print(f"   {key}: {value}")

    print("\n8. Generator Delegation (yield from):")
    delegation = demonstrate_generator_delegation()
    for key, value in delegation.items():
        print(f"   {key}: {value}")

    print("\n9. Practical Generators:")
    practical = demonstrate_practical_generators()
    for key, value in practical.items():
        print(f"   {key}: {value}")

    print("\n10. Memory Efficiency:")
    memory = demonstrate_memory_efficiency()
    for key, value in memory.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
