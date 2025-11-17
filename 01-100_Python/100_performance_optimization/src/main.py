#!/usr/bin/env python3
"""
Program 100: Performance Optimization
Demonstrates optimization techniques and benchmarking.
"""

import time
import timeit
import sys
from typing import List, Callable, Any
from functools import lru_cache, wraps
import itertools


def time_function(func: Callable) -> Callable:
    """Decorator to time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"   {func.__name__}: {(end - start) * 1000:.3f} ms")
        return result
    return wrapper


def demonstrate_profiling() -> None:
    """Demonstrate profiling techniques."""
    print("\n" + "=" * 60)
    print("PROFILING")
    print("=" * 60)

    print("\n1. Using time module:")

    @time_function
    def slow_function():
        """Simulate slow function."""
        total = 0
        for i in range(100000):
            total += i
        return total

    result = slow_function()

    print("\n2. Using timeit for micro-benchmarks:")
    time_taken = timeit.timeit(
        'sum(range(100000))',
        number=10
    )
    print(f"   timeit: {time_taken * 1000:.3f} ms")

    print("\n3. Profiling tools:")
    print("   - cProfile: Built-in profiler")
    print("   - line_profiler: Line-by-line profiling")
    print("   - memory_profiler: Memory usage")


def demonstrate_algorithm_optimization() -> None:
    """Demonstrate algorithm optimization."""
    print("\n" + "=" * 60)
    print("ALGORITHM OPTIMIZATION")
    print("=" * 60)

    data = list(range(1000))

    print("\n1. List comprehension vs loop:")

    @time_function
    def using_loop():
        result = []
        for i in data:
            if i % 2 == 0:
                result.append(i * 2)
        return result

    @time_function
    def using_comprehension():
        return [i * 2 for i in data if i % 2 == 0]

    using_loop()
    using_comprehension()

    print("\n2. Use appropriate data structures:")
    print("   - List: Sequential access")
    print("   - Set: Membership testing")
    print("   - Dict: Key-value lookups")
    print("   - Deque: Queue operations")


def demonstrate_caching() -> None:
    """Demonstrate caching for performance."""
    print("\n" + "=" * 60)
    print("CACHING")
    print("=" * 60)

    print("\n1. Without caching:")

    call_count = {'count': 0}

    def fibonacci_slow(n: int) -> int:
        """Fibonacci without caching."""
        call_count['count'] += 1
        if n < 2:
            return n
        return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)

    call_count['count'] = 0
    start = time.perf_counter()
    result = fibonacci_slow(20)
    end = time.perf_counter()
    print(f"   Time: {(end - start) * 1000:.3f} ms")
    print(f"   Calls: {call_count['count']}")

    print("\n2. With @lru_cache:")

    @lru_cache(maxsize=None)
    def fibonacci_fast(n: int) -> int:
        """Fibonacci with caching."""
        if n < 2:
            return n
        return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)

    fibonacci_fast.cache_clear()
    start = time.perf_counter()
    result = fibonacci_fast(20)
    end = time.perf_counter()
    info = fibonacci_fast.cache_info()
    print(f"   Time: {(end - start) * 1000:.3f} ms")
    print(f"   Cache hits: {info.hits}, misses: {info.misses}")


def demonstrate_generator_optimization() -> None:
    """Demonstrate generators for memory efficiency."""
    print("\n" + "=" * 60)
    print("GENERATOR OPTIMIZATION")
    print("=" * 60)

    print("\n1. List vs Generator:")

    def create_list(n: int) -> List[int]:
        """Create list (all in memory)."""
        return [i * i for i in range(n)]

    def create_generator(n: int):
        """Create generator (lazy evaluation)."""
        for i in range(n):
            yield i * i

    n = 10000

    # List
    start = time.perf_counter()
    list_result = create_list(n)
    list_memory = sys.getsizeof(list_result)
    end = time.perf_counter()
    print(f"   List: {(end - start) * 1000:.3f} ms, {list_memory} bytes")

    # Generator
    start = time.perf_counter()
    gen_result = create_generator(n)
    gen_memory = sys.getsizeof(gen_result)
    end = time.perf_counter()
    print(f"   Generator: {(end - start) * 1000:.3f} ms, {gen_memory} bytes")

    print(f"\n2. Memory saved: {list_memory - gen_memory} bytes")


def demonstrate_string_optimization() -> None:
    """Demonstrate string optimization."""
    print("\n" + "=" * 60)
    print("STRING OPTIMIZATION")
    print("=" * 60)

    parts = ['part'] * 1000

    print("\n1. String concatenation:")

    @time_function
    def concat_with_plus():
        result = ''
        for part in parts:
            result += part
        return result

    @time_function
    def concat_with_join():
        return ''.join(parts)

    concat_with_plus()
    concat_with_join()

    print("\n2. String formatting:")

    name, age = "Alice", 30

    @time_function
    def format_percent():
        return "Name: %s, Age: %d" % (name, age)

    @time_function
    def format_method():
        return "Name: {}, Age: {}".format(name, age)

    @time_function
    def format_fstring():
        return f"Name: {name}, Age: {age}"

    format_percent()
    format_method()
    format_fstring()


def demonstrate_loop_optimization() -> None:
    """Demonstrate loop optimization."""
    print("\n" + "=" * 60)
    print("LOOP OPTIMIZATION")
    print("=" * 60)

    data = list(range(10000))

    print("\n1. Avoid repeated attribute lookups:")

    @time_function
    def lookup_in_loop():
        result = []
        for i in data:
            result.append(i * 2)
        return result

    @time_function
    def cached_lookup():
        result = []
        append = result.append  # Cache method
        for i in data:
            append(i * 2)
        return result

    lookup_in_loop()
    cached_lookup()

    print("\n2. Use built-in functions:")

    @time_function
    def manual_sum():
        total = 0
        for i in data:
            total += i
        return total

    @time_function
    def builtin_sum():
        return sum(data)

    manual_sum()
    builtin_sum()


def demonstrate_comprehension_optimization() -> None:
    """Demonstrate comprehension optimization."""
    print("\n" + "=" * 60)
    print("COMPREHENSION OPTIMIZATION")
    print("=" * 60)

    data = range(1000)

    print("\n1. List vs Set vs Dict comprehension:")

    @time_function
    def list_comp():
        return [i * 2 for i in data]

    @time_function
    def set_comp():
        return {i * 2 for i in data}

    @time_function
    def dict_comp():
        return {i: i * 2 for i in data}

    list_comp()
    set_comp()
    dict_comp()


def demonstrate_function_call_optimization() -> None:
    """Demonstrate function call optimization."""
    print("\n" + "=" * 60)
    print("FUNCTION CALL OPTIMIZATION")
    print("=" * 60)

    print("\n1. Reduce function calls:")

    data = list(range(1000))

    @time_function
    def many_calls():
        def double(x):
            return x * 2
        return [double(i) for i in data]

    @time_function
    def inline():
        return [i * 2 for i in data]

    many_calls()
    inline()


def demonstrate_data_structure_choice() -> None:
    """Demonstrate choosing right data structure."""
    print("\n" + "=" * 60)
    print("DATA STRUCTURE CHOICE")
    print("=" * 60)

    data = list(range(10000))
    search_items = [100, 5000, 9999]

    print("\n1. Membership testing:")

    @time_function
    def test_in_list():
        data_list = data
        return [item in data_list for item in search_items]

    @time_function
    def test_in_set():
        data_set = set(data)
        return [item in data_set for item in search_items]

    test_in_list()
    test_in_set()

    print("\n2. Time complexity:")
    print("   List membership: O(n)")
    print("   Set membership: O(1)")
    print("   Dict lookup: O(1)")


def demonstrate_lazy_evaluation() -> None:
    """Demonstrate lazy evaluation."""
    print("\n" + "=" * 60)
    print("LAZY EVALUATION")
    print("=" * 60)

    print("\n1. Using itertools:")

    @time_function
    def eager_filtering():
        data = list(range(100000))
        filtered = [x for x in data if x % 2 == 0]
        doubled = [x * 2 for x in filtered]
        return list(itertools.islice(doubled, 10))

    @time_function
    def lazy_filtering():
        data = range(100000)
        filtered = (x for x in data if x % 2 == 0)
        doubled = (x * 2 for x in filtered)
        return list(itertools.islice(doubled, 10))

    eager_filtering()
    lazy_filtering()


def demonstrate_memory_optimization() -> None:
    """Demonstrate memory optimization."""
    print("\n" + "=" * 60)
    print("MEMORY OPTIMIZATION")
    print("=" * 60)

    print("\n1. Using __slots__:")

    class WithoutSlots:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class WithSlots:
        __slots__ = ['x', 'y']

        def __init__(self, x, y):
            self.x = x
            self.y = y

    obj1 = WithoutSlots(1, 2)
    obj2 = WithSlots(1, 2)

    print(f"   Without __slots__: {sys.getsizeof(obj1)} bytes")
    print(f"   With __slots__: {sys.getsizeof(obj2)} bytes")

    print("\n2. Memory tips:")
    print("   - Use generators for large datasets")
    print("   - Delete large objects when done")
    print("   - Use __slots__ for many instances")
    print("   - Profile memory usage")


def demonstrate_best_practices() -> None:
    """Demonstrate optimization best practices."""
    print("\n" + "=" * 60)
    print("OPTIMIZATION BEST PRACTICES")
    print("=" * 60)

    print("\n1. Profile first:")
    print("   ✓ Measure before optimizing")
    print("   ✓ Find actual bottlenecks")
    print("   ✓ Focus on hot paths")
    print("   ✓ Use profiling tools")

    print("\n2. Algorithm over micro-optimizations:")
    print("   ✓ O(n log n) vs O(n²) matters more")
    print("   ✓ Choose right data structure")
    print("   ✓ Cache expensive operations")
    print("   ✓ Avoid premature optimization")

    print("\n3. Common optimizations:")
    print("   ✓ Use list comprehensions")
    print("   ✓ Use built-in functions")
    print("   ✓ Cache frequently used values")
    print("   ✓ Use generators for large data")
    print("   ✓ Avoid global lookups in loops")

    print("\n4. Memory vs Speed:")
    print("   ✓ Cache trades memory for speed")
    print("   ✓ Generators trade speed for memory")
    print("   ✓ Profile both metrics")
    print("   ✓ Optimize for your bottleneck")


def demonstrate_benchmarking() -> None:
    """Demonstrate proper benchmarking."""
    print("\n" + "=" * 60)
    print("BENCHMARKING")
    print("=" * 60)

    print("\n1. Using timeit:")

    # Benchmark multiple runs
    result = timeit.repeat(
        'sum(range(1000))',
        repeat=3,
        number=1000
    )

    print(f"   Min: {min(result) * 1000:.3f} ms")
    print(f"   Max: {max(result) * 1000:.3f} ms")
    print(f"   Avg: {sum(result) / len(result) * 1000:.3f} ms")

    print("\n2. Benchmarking tips:")
    print("   ✓ Run multiple iterations")
    print("   ✓ Discard outliers")
    print("   ✓ Test in production-like environment")
    print("   ✓ Compare relative performance")


def main() -> None:
    """Main function demonstrating performance optimization."""
    print("=" * 60)
    print("PYTHON PERFORMANCE OPTIMIZATION")
    print("=" * 60)

    demonstrate_profiling()
    demonstrate_algorithm_optimization()
    demonstrate_caching()
    demonstrate_generator_optimization()
    demonstrate_string_optimization()
    demonstrate_loop_optimization()
    demonstrate_comprehension_optimization()
    demonstrate_function_call_optimization()
    demonstrate_data_structure_choice()
    demonstrate_lazy_evaluation()
    demonstrate_memory_optimization()
    demonstrate_benchmarking()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("CONGRATULATIONS!")
    print("All 100 Python programs completed!")
    print("=" * 60)
    print("\nKey takeaways:")
    print("1. Profile before optimizing")
    print("2. Algorithm choice matters most")
    print("3. Use appropriate data structures")
    print("4. Leverage Python's built-ins")
    print("5. Balance readability and performance")


if __name__ == "__main__":
    main()
