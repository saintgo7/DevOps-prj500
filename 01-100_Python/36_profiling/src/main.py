#!/usr/bin/env python3
"""Program 36: Profiling - Master performance analysis and optimization."""

import time
import timeit
import cProfile
import pstats
import io
import sys
from typing import Any, List
from functools import wraps


def demonstrate_timeit_basic() -> dict[str, Any]:
    """Demonstrate basic timing with timeit."""

    # Time a simple operation
    time1 = timeit.timeit("x = 1 + 1", number=1000000)

    # Time list comprehension vs loop
    setup = "data = range(100)"
    list_comp = timeit.timeit("[x**2 for x in data]", setup=setup, number=10000)
    loop = timeit.timeit("""
result = []
for x in data:
    result.append(x**2)
""", setup=setup, number=10000)

    return {
        "simple_op": f"{time1:.6f}s",
        "list_comp": f"{list_comp:.6f}s",
        "loop": f"{loop:.6f}s",
        "faster": "list_comp" if list_comp < loop else "loop",
        "note": "timeit.timeit() measures execution time accurately",
    }


def demonstrate_time_decorator() -> dict[str, Any]:
    """Demonstrate timing decorator."""

    times = {}

    def timing_decorator(func):
        """Decorator that times function execution."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            times[func.__name__] = elapsed
            return result

        return wrapper

    @timing_decorator
    def slow_function():
        """Simulate slow operation."""
        time.sleep(0.1)
        return sum(range(1000))

    @timing_decorator
    def fast_function():
        """Quick operation."""
        return sum(range(100))

    result1 = slow_function()
    result2 = fast_function()

    return {
        "slow_time": f"{times['slow_function']:.3f}s",
        "fast_time": f"{times['fast_function']:.3f}s",
        "note": "Decorators enable reusable timing instrumentation",
    }


def demonstrate_cprofile_basic() -> dict[str, Any]:
    """Demonstrate basic cProfile usage."""

    def fibonacci(n: int) -> int:
        """Compute fibonacci (inefficient)."""
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    def compute():
        """Function to profile."""
        return fibonacci(15)

    # Profile the function
    profiler = cProfile.Profile()
    profiler.enable()
    result = compute()
    profiler.disable()

    # Get statistics
    stats_stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stats_stream)
    stats.sort_stats('cumulative')
    stats.print_stats(5)

    output = stats_stream.getvalue()
    line_count = len([l for l in output.split('\n') if l.strip()])

    return {
        "result": result,
        "stats_lines": line_count,
        "note": "cProfile provides detailed function call statistics",
    }


def demonstrate_profile_analysis() -> dict[str, Any]:
    """Demonstrate analyzing profile statistics."""

    def slow_operation():
        """Slow operation."""
        total = 0
        for i in range(100000):
            total += i ** 2
        return total

    def medium_operation():
        """Medium speed operation."""
        return sum(i ** 2 for i in range(10000))

    def fast_operation():
        """Fast operation."""
        return sum(range(1000))

    def main_function():
        """Main function calling others."""
        slow_operation()
        medium_operation()
        fast_operation()

    # Profile
    profiler = cProfile.Profile()
    profiler.enable()
    main_function()
    profiler.disable()

    # Analyze
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')

    # Get function counts
    func_count = len(stats.stats)

    return {
        "functions_called": func_count,
        "note": "Stats can be sorted by time, calls, cumulative time",
    }


def demonstrate_memory_profiling() -> dict[str, Any]:
    """Demonstrate basic memory profiling concepts."""

    def create_large_list():
        """Create large list."""
        return [i for i in range(1000000)]

    def create_generator():
        """Create generator (memory efficient)."""
        return (i for i in range(1000000))

    # Measure list size
    large_list = create_large_list()
    list_size = sys.getsizeof(large_list)

    # Measure generator size
    gen = create_generator()
    gen_size = sys.getsizeof(gen)

    return {
        "list_size_bytes": list_size,
        "generator_size_bytes": gen_size,
        "memory_saved": list_size - gen_size,
        "note": "Generators use significantly less memory",
    }


def demonstrate_line_profiling_concept() -> dict[str, Any]:
    """Demonstrate line-by-line profiling concept."""

    def process_data(data: List[int]) -> dict:
        """Process data line by line."""
        # Line 1: Initialize
        result = {"sum": 0, "squares": [], "evens": []}

        # Line 2: Sum all
        result["sum"] = sum(data)

        # Line 3: Square all
        result["squares"] = [x ** 2 for x in data]

        # Line 4: Filter evens
        result["evens"] = [x for x in data if x % 2 == 0]

        return result

    # Time each operation separately
    data = list(range(10000))

    start = time.perf_counter()
    sum_result = sum(data)
    sum_time = time.perf_counter() - start

    start = time.perf_counter()
    squares = [x ** 2 for x in data]
    squares_time = time.perf_counter() - start

    start = time.perf_counter()
    evens = [x for x in data if x % 2 == 0]
    evens_time = time.perf_counter() - start

    return {
        "sum_time": f"{sum_time:.6f}s",
        "squares_time": f"{squares_time:.6f}s",
        "evens_time": f"{evens_time:.6f}s",
        "note": "Line profiling identifies hotspots in functions",
    }


def demonstrate_algorithm_comparison() -> dict[str, Any]:
    """Demonstrate comparing algorithm performance."""

    # Linear search
    def linear_search(arr: List[int], target: int) -> int:
        for i, val in enumerate(arr):
            if val == target:
                return i
        return -1

    # Binary search (requires sorted array)
    def binary_search(arr: List[int], target: int) -> int:
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    # Time comparisons
    data = list(range(10000))
    target = 9999

    linear_time = timeit.timeit(
        lambda: linear_search(data, target),
        number=100
    )

    binary_time = timeit.timeit(
        lambda: binary_search(data, target),
        number=100
    )

    return {
        "linear_time": f"{linear_time:.6f}s",
        "binary_time": f"{binary_time:.6f}s",
        "speedup": f"{linear_time / binary_time:.1f}x",
        "note": "Profiling helps choose better algorithms",
    }


def demonstrate_caching_performance() -> dict[str, Any]:
    """Demonstrate performance impact of caching."""

    # Without cache
    def fibonacci_no_cache(n: int) -> int:
        if n <= 1:
            return n
        return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)

    # With cache
    cache = {}

    def fibonacci_cached(n: int) -> int:
        if n in cache:
            return cache[n]
        if n <= 1:
            return n
        result = fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
        cache[n] = result
        return result

    # Time both
    n = 20

    no_cache_time = timeit.timeit(
        lambda: fibonacci_no_cache(n),
        number=1
    )

    cached_time = timeit.timeit(
        lambda: fibonacci_cached(n),
        number=1
    )

    return {
        "without_cache": f"{no_cache_time:.6f}s",
        "with_cache": f"{cached_time:.6f}s",
        "speedup": f"{no_cache_time / cached_time:.0f}x",
        "note": "Caching dramatically improves performance",
    }


def demonstrate_datastructure_performance() -> dict[str, Any]:
    """Demonstrate performance of different data structures."""

    n = 10000

    # List append
    list_time = timeit.timeit("""
result = []
for i in range(1000):
    result.append(i)
""", number=n)

    # List extend
    extend_time = timeit.timeit("""
result = []
result.extend(range(1000))
""", number=n)

    # Set add
    set_time = timeit.timeit("""
result = set()
for i in range(1000):
    result.add(i)
""", number=n)

    # Dict set
    dict_time = timeit.timeit("""
result = {}
for i in range(1000):
    result[i] = i
""", number=n)

    return {
        "list_append": f"{list_time:.4f}s",
        "list_extend": f"{extend_time:.4f}s",
        "set_add": f"{set_time:.4f}s",
        "dict_set": f"{dict_time:.4f}s",
        "note": "Different data structures have different performance",
    }


def demonstrate_optimization_techniques() -> dict[str, Any]:
    """Demonstrate common optimization techniques."""

    # Technique 1: List comprehension vs append
    data = range(1000)

    append_time = timeit.timeit("""
result = []
for i in range(1000):
    result.append(i * 2)
""", number=1000)

    comp_time = timeit.timeit("""
result = [i * 2 for i in range(1000)]
""", number=1000)

    # Technique 2: Local variable vs global
    global_time = timeit.timeit("len([])", number=100000)
    local_time = timeit.timeit("""
local_len = len
local_len([])
""", number=100000)

    return {
        "append_vs_comp": f"{comp_time / append_time:.2f}x faster",
        "local_vs_global": f"{global_time / local_time:.2f}x",
        "techniques": ["comprehensions", "local vars", "caching", "generators"],
        "note": "Small optimizations add up in tight loops",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 36: Profiling")
    print("=" * 60)

    print("\n1. Timeit Basic:")
    timeit_demo = demonstrate_timeit_basic()
    for key, value in timeit_demo.items():
        print(f"   {key}: {value}")

    print("\n2. Timing Decorator:")
    decorator = demonstrate_time_decorator()
    for key, value in decorator.items():
        print(f"   {key}: {value}")

    print("\n3. cProfile Basic:")
    cprofile = demonstrate_cprofile_basic()
    for key, value in cprofile.items():
        print(f"   {key}: {value}")

    print("\n4. Profile Analysis:")
    analysis = demonstrate_profile_analysis()
    for key, value in analysis.items():
        print(f"   {key}: {value}")

    print("\n5. Memory Profiling:")
    memory = demonstrate_memory_profiling()
    for key, value in memory.items():
        print(f"   {key}: {value}")

    print("\n6. Line Profiling Concept:")
    line = demonstrate_line_profiling_concept()
    for key, value in line.items():
        print(f"   {key}: {value}")

    print("\n7. Algorithm Comparison:")
    algorithms = demonstrate_algorithm_comparison()
    for key, value in algorithms.items():
        print(f"   {key}: {value}")

    print("\n8. Caching Performance:")
    caching = demonstrate_caching_performance()
    for key, value in caching.items():
        print(f"   {key}: {value}")

    print("\n9. Data Structure Performance:")
    datastructures = demonstrate_datastructure_performance()
    for key, value in datastructures.items():
        print(f"   {key}: {value}")

    print("\n10. Optimization Techniques:")
    optimization = demonstrate_optimization_techniques()
    for key, value in optimization.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
