"""Unit tests for 05_loops program."""

import sys
from pathlib import Path
import pytest

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_for_loops,
    demonstrate_range_function,
    demonstrate_while_loops,
    demonstrate_loop_control,
    demonstrate_nested_loops,
    demonstrate_loop_else,
    demonstrate_enumerate_zip,
    demonstrate_list_comprehensions,
    demonstrate_common_patterns,
    fibonacci_sequence,
    main,
)


class TestBasicForLoops:
    def test_sum_list(self):
        result = demonstrate_basic_for_loops()
        assert result["sum_list"] == 15

    def test_letters(self):
        result = demonstrate_basic_for_loops()
        assert result["letters"] == ['P', 'y', 't', 'h', 'o', 'n']


class TestRangeFunction:
    def test_range_5(self):
        result = demonstrate_range_function()
        assert result["range_5"] == [0, 1, 2, 3, 4]

    def test_countdown(self):
        result = demonstrate_range_function()
        assert result["countdown"] == list(range(10, 0, -1))


class TestWhileLoops:
    def test_while_sum(self):
        result = demonstrate_while_loops()
        assert result["while_sum"] == 10

    def test_factorial(self):
        result = demonstrate_while_loops()
        assert result["factorial_5"] == 120


class TestLoopControl:
    def test_break(self):
        result = demonstrate_loop_control()
        assert result["break_at_5"] == [0, 1, 2, 3, 4]

    def test_continue(self):
        result = demonstrate_loop_control()
        assert result["odd_numbers"] == [1, 3, 5, 7, 9]


class TestNestedLoops:
    def test_mult_table(self):
        result = demonstrate_nested_loops()
        assert result["mult_table_3x3"] == [[1,2,3], [2,4,6], [3,6,9]]

    def test_flattened(self):
        result = demonstrate_nested_loops()
        assert result["flattened_matrix"] == list(range(1, 10))


class TestFibonacci:
    def test_fib_10(self):
        result = fibonacci_sequence(10)
        assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_fib_0(self):
        assert fibonacci_sequence(0) == []

    def test_fib_1(self):
        assert fibonacci_sequence(1) == [0]


class TestMain:
    def test_main_executes(self):
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
