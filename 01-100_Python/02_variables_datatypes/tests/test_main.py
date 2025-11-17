"""
Unit tests for 02_variables_datatypes program.

These tests verify:
- Integer operations and representations
- Float operations and special values
- String operations and formatting
- Boolean logic and comparisons
- None type handling
- Type checking functionality
- Type conversion operations
- Multiple assignment patterns
"""

import math
import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_integers,
    demonstrate_floats,
    demonstrate_strings,
    demonstrate_booleans,
    demonstrate_none,
    demonstrate_type_checking,
    demonstrate_type_conversion,
    demonstrate_multiple_assignment,
    main,
)


class TestDemonstrateIntegers:
    """Test cases for demonstrate_integers()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_integers()
        assert isinstance(result, dict)

    def test_positive_integer(self):
        """Test positive integer value."""
        result = demonstrate_integers()
        assert result["positive"] == 42
        assert isinstance(result["positive"], int)

    def test_negative_integer(self):
        """Test negative integer value."""
        result = demonstrate_integers()
        assert result["negative"] == -17
        assert result["negative"] < 0

    def test_zero(self):
        """Test zero value."""
        result = demonstrate_integers()
        assert result["zero"] == 0

    def test_large_integer(self):
        """Test large integer with underscores."""
        result = demonstrate_integers()
        assert result["large"] == 1_000_000

    def test_binary_representation(self):
        """Test binary number representation."""
        result = demonstrate_integers()
        assert result["binary"] == 10  # 0b1010 = 10

    def test_octal_representation(self):
        """Test octal number representation."""
        result = demonstrate_integers()
        assert result["octal"] == 10  # 0o12 = 10

    def test_hexadecimal_representation(self):
        """Test hexadecimal number representation."""
        result = demonstrate_integers()
        assert result["hex"] == 10  # 0xA = 10

    def test_type_name(self):
        """Test type name is 'int'."""
        result = demonstrate_integers()
        assert result["type"] == "int"


class TestDemonstrateFloats:
    """Test cases for demonstrate_floats()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_floats()
        assert isinstance(result, dict)

    def test_simple_float(self):
        """Test simple float value."""
        result = demonstrate_floats()
        assert result["simple"] == 3.14
        assert isinstance(result["simple"], float)

    def test_negative_float(self):
        """Test negative float value."""
        result = demonstrate_floats()
        assert result["negative"] == -2.5
        assert result["negative"] < 0

    def test_scientific_notation(self):
        """Test scientific notation."""
        result = demonstrate_floats()
        assert result["scientific"] == 1500.0  # 1.5e3

    def test_small_number(self):
        """Test small number in scientific notation."""
        result = demonstrate_floats()
        assert result["small"] == 0.0015  # 1.5e-3

    def test_infinity(self):
        """Test positive infinity."""
        result = demonstrate_floats()
        assert math.isinf(result["infinity"])
        assert result["infinity"] > 0

    def test_negative_infinity(self):
        """Test negative infinity."""
        result = demonstrate_floats()
        assert math.isinf(result["neg_infinity"])
        assert result["neg_infinity"] < 0

    def test_nan(self):
        """Test NaN (Not a Number)."""
        result = demonstrate_floats()
        assert math.isnan(result["nan"])

    def test_type_name(self):
        """Test type name is 'float'."""
        result = demonstrate_floats()
        assert result["type"] == "float"


class TestDemonstrateStrings:
    """Test cases for demonstrate_strings()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_strings()
        assert isinstance(result, dict)

    def test_single_quotes(self):
        """Test string with single quotes."""
        result = demonstrate_strings()
        assert result["single_quotes"] == "Hello"

    def test_double_quotes(self):
        """Test string with double quotes."""
        result = demonstrate_strings()
        assert result["double_quotes"] == "World"

    def test_triple_quotes(self):
        """Test multi-line string with triple quotes."""
        result = demonstrate_strings()
        assert "Multi-line" in result["triple_quotes"]
        assert "\n" in result["triple_quotes"]

    def test_concatenation(self):
        """Test string concatenation."""
        result = demonstrate_strings()
        assert result["concatenation"] == "Hello World"

    def test_repetition(self):
        """Test string repetition."""
        result = demonstrate_strings()
        assert result["repetition"] == "Python! Python! Python! "

    def test_f_string(self):
        """Test f-string formatting."""
        result = demonstrate_strings()
        assert "Alice" in result["f_string"]
        assert "30" in result["f_string"]

    def test_escaped_characters(self):
        """Test escape characters."""
        result = demonstrate_strings()
        assert "\n" in result["escaped"]
        assert "\t" in result["escaped"]

    def test_raw_string(self):
        """Test raw string (no escape processing)."""
        result = demonstrate_strings()
        assert r"C:\Users\name\file.txt" == result["raw_string"]

    def test_length(self):
        """Test string length calculation."""
        result = demonstrate_strings()
        assert result["length"] == len("Hello World")

    def test_type_name(self):
        """Test type name is 'str'."""
        result = demonstrate_strings()
        assert result["type"] == "str"


class TestDemonstrateBooleans:
    """Test cases for demonstrate_booleans()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_booleans()
        assert isinstance(result, dict)

    def test_true_value(self):
        """Test True boolean value."""
        result = demonstrate_booleans()
        assert result["true"] is True

    def test_false_value(self):
        """Test False boolean value."""
        result = demonstrate_booleans()
        assert result["false"] is False

    def test_and_operation(self):
        """Test AND operation."""
        result = demonstrate_booleans()
        assert result["and_result"] is False  # True and False

    def test_or_operation(self):
        """Test OR operation."""
        result = demonstrate_booleans()
        assert result["or_result"] is True  # True or False

    def test_not_operation(self):
        """Test NOT operation."""
        result = demonstrate_booleans()
        assert result["not_result"] is False  # not True

    def test_comparison_equal(self):
        """Test equality comparison."""
        result = demonstrate_booleans()
        assert result["comparison_equal"] is True  # 5 == 5

    def test_comparison_not_equal(self):
        """Test not equal comparison."""
        result = demonstrate_booleans()
        assert result["comparison_not_equal"] is True  # 5 != 3

    def test_comparison_greater(self):
        """Test greater than comparison."""
        result = demonstrate_booleans()
        assert result["comparison_greater"] is True  # 10 > 5

    def test_comparison_less_equal(self):
        """Test less than or equal comparison."""
        result = demonstrate_booleans()
        assert result["comparison_less_equal"] is True  # 5 <= 5

    def test_truthy_count(self):
        """Test count of truthy values."""
        result = demonstrate_booleans()
        assert result["truthy_count"] == 4

    def test_falsy_count(self):
        """Test count of falsy values."""
        result = demonstrate_booleans()
        assert result["falsy_count"] == 5

    def test_type_name(self):
        """Test type name is 'bool'."""
        result = demonstrate_booleans()
        assert result["type"] == "bool"


class TestDemonstrateNone:
    """Test cases for demonstrate_none()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_none()
        assert isinstance(result, dict)

    def test_none_value(self):
        """Test None value."""
        result = demonstrate_none()
        assert result["value"] is None

    def test_result_with_value(self):
        """Test function returning a value."""
        result = demonstrate_none()
        assert result["result_with_value"] == "Something"

    def test_result_none(self):
        """Test function returning None."""
        result = demonstrate_none()
        assert result["result_none"] is None

    def test_is_none_check(self):
        """Test 'is None' check."""
        result = demonstrate_none()
        assert result["is_none_check"] is True

    def test_is_not_none_check(self):
        """Test 'is not None' check."""
        result = demonstrate_none()
        assert result["is_not_none_check"] is True

    def test_type_name(self):
        """Test type name is 'NoneType'."""
        result = demonstrate_none()
        assert result["type"] == "NoneType"


class TestDemonstrateTypeChecking:
    """Test cases for demonstrate_type_checking()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_type_checking(42)
        assert isinstance(result, dict)

    def test_integer_type_check(self):
        """Test type checking for integer."""
        result = demonstrate_type_checking(42)
        assert result["type"] == "int"
        assert result["is_int"] is True
        assert result["is_str"] is False
        assert result["is_number"] is True

    def test_string_type_check(self):
        """Test type checking for string."""
        result = demonstrate_type_checking("Hello")
        assert result["type"] == "str"
        assert result["is_str"] is True
        assert result["is_int"] is False

    def test_float_type_check(self):
        """Test type checking for float."""
        result = demonstrate_type_checking(3.14)
        assert result["type"] == "float"
        assert result["is_float"] is True
        assert result["is_number"] is True

    def test_boolean_type_check(self):
        """Test type checking for boolean."""
        result = demonstrate_type_checking(True)
        assert result["type"] == "bool"
        assert result["is_bool"] is True
        # Note: bool is a subclass of int in Python
        assert result["is_int"] is True

    def test_value_included(self):
        """Test that original value is included in result."""
        test_value = "test"
        result = demonstrate_type_checking(test_value)
        assert result["value"] == test_value


class TestDemonstrateTypeConversion:
    """Test cases for demonstrate_type_conversion()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_type_conversion()
        assert isinstance(result, dict)

    def test_string_to_int(self):
        """Test converting string to int."""
        result = demonstrate_type_conversion()
        assert result["str_to_int"] == 42
        assert isinstance(result["str_to_int"], int)

    def test_string_to_float(self):
        """Test converting string to float."""
        result = demonstrate_type_conversion()
        assert result["str_to_float"] == 3.14
        assert isinstance(result["str_to_float"], float)

    def test_int_to_string(self):
        """Test converting int to string."""
        result = demonstrate_type_conversion()
        assert result["int_to_str"] == "42"
        assert isinstance(result["int_to_str"], str)

    def test_float_to_string(self):
        """Test converting float to string."""
        result = demonstrate_type_conversion()
        assert result["float_to_str"] == "3.14"
        assert isinstance(result["float_to_str"], str)

    def test_int_to_float(self):
        """Test converting int to float."""
        result = demonstrate_type_conversion()
        assert result["int_to_float"] == 42.0
        assert isinstance(result["int_to_float"], float)

    def test_float_to_int(self):
        """Test converting float to int (truncation)."""
        result = demonstrate_type_conversion()
        assert result["float_to_int"] == 3  # 3.14 truncates to 3
        assert isinstance(result["float_to_int"], int)

    def test_int_to_bool(self):
        """Test converting int to bool."""
        result = demonstrate_type_conversion()
        assert result["int_to_bool"] is True
        assert result["zero_to_bool"] is False

    def test_string_to_bool(self):
        """Test converting string to bool."""
        result = demonstrate_type_conversion()
        assert result["str_to_bool"] is True
        assert result["empty_str_to_bool"] is False

    def test_bool_to_int(self):
        """Test converting bool to int."""
        result = demonstrate_type_conversion()
        assert result["bool_to_int"] == 1
        assert result["false_to_int"] == 0


class TestDemonstrateMultipleAssignment:
    """Test cases for demonstrate_multiple_assignment()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_multiple_assignment()
        assert isinstance(result, dict)

    def test_multiple_assignment(self):
        """Test multiple variable assignment."""
        result = demonstrate_multiple_assignment()
        assert result["x"] == 1
        assert result["y"] == 2
        assert result["z"] == 3

    def test_same_value_assignment(self):
        """Test assigning same value to multiple variables."""
        result = demonstrate_multiple_assignment()
        assert result["a_b_c"] == (10, 10, 10)

    def test_variable_swapping(self):
        """Test swapping variable values."""
        result = demonstrate_multiple_assignment()
        assert result["swapped"] == (10, 5)  # Originally (5, 10)

    def test_unpacking(self):
        """Test tuple unpacking."""
        result = demonstrate_multiple_assignment()
        assert result["x_coord"] == 100
        assert result["y_coord"] == 200


class TestMainFunction:
    """Test cases for the main() function."""

    def test_main_executes_without_error(self):
        """Test that main() runs without exceptions."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    def test_main_produces_output(self, capsys):
        """Test that main() produces output."""
        main()
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_main_includes_all_sections(self, capsys):
        """Test that main() includes all demonstration sections."""
        main()
        captured = capsys.readouterr()

        expected_sections = [
            "INTEGERS",
            "FLOATING-POINT",
            "STRINGS",
            "BOOLEANS",
            "NONE TYPE",
            "TYPE CHECKING",
            "TYPE CONVERSION",
            "MULTIPLE ASSIGNMENT",
        ]

        for section in expected_sections:
            assert section in captured.out, f"Expected '{section}' in output"

    def test_main_success_message(self, capsys):
        """Test that main() prints success message."""
        main()
        captured = capsys.readouterr()
        assert "completed successfully" in captured.out


class TestIntegration:
    """Integration tests for the complete program."""

    def test_all_functions_work_together(self):
        """Test that all functions can be called successfully."""
        functions = [
            demonstrate_integers,
            demonstrate_floats,
            demonstrate_strings,
            demonstrate_booleans,
            demonstrate_none,
            demonstrate_multiple_assignment,
            demonstrate_type_conversion,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict)
            assert len(result) > 0


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
