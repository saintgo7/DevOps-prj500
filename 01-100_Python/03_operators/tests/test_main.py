"""
Unit tests for 03_operators program.

These tests verify:
- Arithmetic operations
- Comparison operations
- Logical operations
- Assignment operations
- Bitwise operations
- Membership operations
- Identity operations
- Operator precedence
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_arithmetic_operators,
    demonstrate_comparison_operators,
    demonstrate_logical_operators,
    demonstrate_assignment_operators,
    demonstrate_bitwise_operators,
    demonstrate_membership_operators,
    demonstrate_identity_operators,
    demonstrate_operator_precedence,
    main,
)


class TestArithmeticOperators:
    """Test cases for arithmetic operators."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_arithmetic_operators()
        assert isinstance(result, dict)

    def test_addition(self):
        """Test addition operator."""
        result = demonstrate_arithmetic_operators()
        assert result["addition"] == 13  # 10 + 3

    def test_subtraction(self):
        """Test subtraction operator."""
        result = demonstrate_arithmetic_operators()
        assert result["subtraction"] == 7  # 10 - 3

    def test_multiplication(self):
        """Test multiplication operator."""
        result = demonstrate_arithmetic_operators()
        assert result["multiplication"] == 30  # 10 * 3

    def test_division(self):
        """Test division operator."""
        result = demonstrate_arithmetic_operators()
        assert abs(result["division"] - 3.333) < 0.01  # 10 / 3

    def test_floor_division(self):
        """Test floor division operator."""
        result = demonstrate_arithmetic_operators()
        assert result["floor_division"] == 3  # 10 // 3

    def test_modulo(self):
        """Test modulo operator."""
        result = demonstrate_arithmetic_operators()
        assert result["modulo"] == 1  # 10 % 3

    def test_exponentiation(self):
        """Test exponentiation operator."""
        result = demonstrate_arithmetic_operators()
        assert result["exponentiation"] == 1000  # 10 ** 3

    def test_unary_positive(self):
        """Test unary positive operator."""
        result = demonstrate_arithmetic_operators()
        assert result["positive"] == 10  # +10

    def test_unary_negative(self):
        """Test unary negative operator."""
        result = demonstrate_arithmetic_operators()
        assert result["negative"] == -10  # -10

    def test_operator_precedence(self):
        """Test operator precedence in expressions."""
        result = demonstrate_arithmetic_operators()
        assert result["complex_expr"] == 14  # 2 + 3 * 4
        assert result["with_parens"] == 20  # (2 + 3) * 4


class TestComparisonOperators:
    """Test cases for comparison operators."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_comparison_operators()
        assert isinstance(result, dict)

    def test_equal(self):
        """Test equality operator."""
        result = demonstrate_comparison_operators()
        assert result["equal"] is False  # 10 == 5

    def test_not_equal(self):
        """Test not equal operator."""
        result = demonstrate_comparison_operators()
        assert result["not_equal"] is True  # 10 != 5

    def test_greater_than(self):
        """Test greater than operator."""
        result = demonstrate_comparison_operators()
        assert result["greater_than"] is True  # 10 > 5

    def test_less_than(self):
        """Test less than operator."""
        result = demonstrate_comparison_operators()
        assert result["less_than"] is False  # 10 < 5

    def test_greater_or_equal(self):
        """Test greater or equal operator."""
        result = demonstrate_comparison_operators()
        assert result["greater_or_equal"] is True  # 10 >= 5

    def test_less_or_equal(self):
        """Test less or equal operator."""
        result = demonstrate_comparison_operators()
        assert result["less_or_equal"] is False  # 10 <= 5

    def test_chained_comparison(self):
        """Test chained comparison."""
        result = demonstrate_comparison_operators()
        assert result["chained"] is True  # 1 < 5 < 10
        assert result["chained_false"] is False  # 1 < 5 > 10

    def test_string_comparison(self):
        """Test string comparison."""
        result = demonstrate_comparison_operators()
        assert result["str_equal"] is True
        assert result["str_less"] is True  # alphabetical order

    def test_list_comparison(self):
        """Test list comparison."""
        result = demonstrate_comparison_operators()
        assert result["list_equal"] is True
        assert result["list_less"] is True


class TestLogicalOperators:
    """Test cases for logical operators."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_logical_operators()
        assert isinstance(result, dict)

    def test_and_operator(self):
        """Test logical AND operator."""
        result = demonstrate_logical_operators()
        assert result["and_tt"] is True
        assert result["and_tf"] is False
        assert result["and_ff"] is False

    def test_or_operator(self):
        """Test logical OR operator."""
        result = demonstrate_logical_operators()
        assert result["or_tt"] is True
        assert result["or_tf"] is True
        assert result["or_ff"] is False

    def test_not_operator(self):
        """Test logical NOT operator."""
        result = demonstrate_logical_operators()
        assert result["not_true"] is False
        assert result["not_false"] is True

    def test_short_circuit_and(self):
        """Test short-circuit evaluation with AND."""
        result = demonstrate_logical_operators()
        assert result["short_and_1"] == 10  # 5 and 10
        assert result["short_and_2"] == 0  # 0 and 10

    def test_short_circuit_or(self):
        """Test short-circuit evaluation with OR."""
        result = demonstrate_logical_operators()
        assert result["short_or_1"] == 5  # 5 or 10
        assert result["short_or_2"] == 10  # 0 or 10

    def test_complex_logical(self):
        """Test complex logical expressions."""
        result = demonstrate_logical_operators()
        assert result["complex_and"] is True
        assert result["complex_or"] is True
        assert result["complex_not"] is True

    def test_truthy_falsy_operations(self):
        """Test logical operations with truthy/falsy values."""
        result = demonstrate_logical_operators()
        assert result["truthy_and"] == "world"
        assert result["falsy_and"] == ""
        assert result["truthy_or"] == "hello"
        assert result["falsy_or"] == "world"


class TestAssignmentOperators:
    """Test cases for assignment operators."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_assignment_operators()
        assert isinstance(result, dict)

    def test_simple_assignment(self):
        """Test simple assignment."""
        result = demonstrate_assignment_operators()
        assert result["simple"] == 10

    def test_add_assign(self):
        """Test += operator."""
        result = demonstrate_assignment_operators()
        assert result["add_assign"] == 8  # 5 + 3

    def test_sub_assign(self):
        """Test -= operator."""
        result = demonstrate_assignment_operators()
        assert result["sub_assign"] == 6  # 10 - 4

    def test_mul_assign(self):
        """Test *= operator."""
        result = demonstrate_assignment_operators()
        assert result["mul_assign"] == 12  # 3 * 4

    def test_div_assign(self):
        """Test /= operator."""
        result = demonstrate_assignment_operators()
        assert result["div_assign"] == 5.0  # 20 / 4

    def test_floor_div_assign(self):
        """Test //= operator."""
        result = demonstrate_assignment_operators()
        assert result["floor_div_assign"] == 3  # 17 // 5

    def test_mod_assign(self):
        """Test %= operator."""
        result = demonstrate_assignment_operators()
        assert result["mod_assign"] == 2  # 17 % 5

    def test_exp_assign(self):
        """Test **= operator."""
        result = demonstrate_assignment_operators()
        assert result["exp_assign"] == 8  # 2 ** 3

    def test_bitwise_and_assign(self):
        """Test &= operator."""
        result = demonstrate_assignment_operators()
        assert result["and_assign"] == 8  # 12 & 10

    def test_bitwise_or_assign(self):
        """Test |= operator."""
        result = demonstrate_assignment_operators()
        assert result["or_assign"] == 15  # 12 | 3

    def test_bitwise_xor_assign(self):
        """Test ^= operator."""
        result = demonstrate_assignment_operators()
        assert result["xor_assign"] == 6  # 12 ^ 10

    def test_left_shift_assign(self):
        """Test <<= operator."""
        result = demonstrate_assignment_operators()
        assert result["left_shift_assign"] == 16  # 4 << 2

    def test_right_shift_assign(self):
        """Test >>= operator."""
        result = demonstrate_assignment_operators()
        assert result["right_shift_assign"] == 4  # 16 >> 2


class TestBitwiseOperators:
    """Test cases for bitwise operators."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_bitwise_operators()
        assert isinstance(result, dict)

    def test_bitwise_and(self):
        """Test bitwise AND operator."""
        result = demonstrate_bitwise_operators()
        assert result["bitwise_and"] == 8  # 12 & 10

    def test_bitwise_or(self):
        """Test bitwise OR operator."""
        result = demonstrate_bitwise_operators()
        assert result["bitwise_or"] == 14  # 12 | 10

    def test_bitwise_xor(self):
        """Test bitwise XOR operator."""
        result = demonstrate_bitwise_operators()
        assert result["bitwise_xor"] == 6  # 12 ^ 10

    def test_bitwise_not(self):
        """Test bitwise NOT operator."""
        result = demonstrate_bitwise_operators()
        assert result["bitwise_not"] == -13  # ~12

    def test_left_shift(self):
        """Test left shift operator."""
        result = demonstrate_bitwise_operators()
        assert result["left_shift"] == 48  # 12 << 2

    def test_right_shift(self):
        """Test right shift operator."""
        result = demonstrate_bitwise_operators()
        assert result["right_shift"] == 3  # 12 >> 2

    def test_even_check(self):
        """Test even number check using bitwise AND."""
        result = demonstrate_bitwise_operators()
        assert result["is_even"] is True  # 12 is even

    def test_bit_manipulation(self):
        """Test bit manipulation operations."""
        result = demonstrate_bitwise_operators()
        assert isinstance(result["set_bit"], int)
        assert isinstance(result["clear_bit"], int)
        assert isinstance(result["toggle_bit"], int)

    def test_binary_representation(self):
        """Test binary representation is included."""
        result = demonstrate_bitwise_operators()
        assert result["binary_a"] == "0b1100"
        assert result["binary_b"] == "0b1010"


class TestMembershipOperators:
    """Test cases for membership operators."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_membership_operators()
        assert isinstance(result, dict)

    def test_in_list(self):
        """Test 'in' operator with list."""
        result = demonstrate_membership_operators()
        assert result["in_list"] is True  # 3 in [1,2,3,4,5]

    def test_not_in_list(self):
        """Test 'not in' operator with list."""
        result = demonstrate_membership_operators()
        assert result["not_in_list"] is True  # 10 not in [1,2,3,4,5]

    def test_in_string(self):
        """Test 'in' operator with string."""
        result = demonstrate_membership_operators()
        assert result["in_string"] is True  # "Python" in "Python Programming"

    def test_not_in_string(self):
        """Test 'not in' operator with string."""
        result = demonstrate_membership_operators()
        assert result["not_in_string"] is True  # "Java" not in "Python Programming"

    def test_in_tuple(self):
        """Test 'in' operator with tuple."""
        result = demonstrate_membership_operators()
        assert result["in_tuple"] is True  # 20 in (10, 20, 30)

    def test_in_dict(self):
        """Test 'in' operator with dictionary keys."""
        result = demonstrate_membership_operators()
        assert result["in_dict_keys"] is True  # "name" in dict

    def test_not_in_dict(self):
        """Test 'not in' operator with dictionary keys."""
        result = demonstrate_membership_operators()
        assert result["not_in_dict_keys"] is True  # "email" not in dict

    def test_in_set(self):
        """Test 'in' operator with set."""
        result = demonstrate_membership_operators()
        assert result["in_set"] is True  # 3 in {1,2,3,4,5}

    def test_substring_check(self):
        """Test substring membership."""
        result = demonstrate_membership_operators()
        assert result["substring_check"] is True  # "gram" in "Programming"


class TestIdentityOperators:
    """Test cases for identity operators."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_identity_operators()
        assert isinstance(result, dict)

    def test_same_object(self):
        """Test 'is' operator with same object."""
        result = demonstrate_identity_operators()
        assert result["same_object"] is True  # a is c

    def test_different_object(self):
        """Test 'is' operator with different objects."""
        result = demonstrate_identity_operators()
        assert result["different_object"] is False  # a is b

    def test_is_not(self):
        """Test 'is not' operator."""
        result = demonstrate_identity_operators()
        assert result["not_same"] is True  # a is not b

    def test_equality_vs_identity(self):
        """Test difference between == and is."""
        result = demonstrate_identity_operators()
        assert result["equal_values"] is True  # a == b
        assert result["same_identity"] is False  # a is b

    def test_none_check(self):
        """Test None identity checking."""
        result = demonstrate_identity_operators()
        assert result["is_none"] is True
        assert result["is_not_none"] is False

    def test_small_int_caching(self):
        """Test small integer caching."""
        result = demonstrate_identity_operators()
        assert result["small_int_identity"] is True  # 256 is 256

    def test_string_interning(self):
        """Test string interning."""
        result = demonstrate_identity_operators()
        # String interning behavior may vary
        assert isinstance(result["string_identity"], bool)

    def test_object_ids(self):
        """Test that object IDs are included."""
        result = demonstrate_identity_operators()
        assert isinstance(result["id_a"], int)
        assert isinstance(result["id_b"], int)
        assert isinstance(result["id_c"], int)
        # a and c should have same id
        assert result["id_a"] == result["id_c"]


class TestOperatorPrecedence:
    """Test cases for operator precedence."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_operator_precedence()
        assert isinstance(result, dict)

    def test_multiplication_before_addition(self):
        """Test that * has higher precedence than +."""
        result = demonstrate_operator_precedence()
        assert result["expr1"] == 14  # 2 + 3 * 4

    def test_parentheses_override(self):
        """Test that parentheses override precedence."""
        result = demonstrate_operator_precedence()
        assert result["expr2"] == 20  # (2 + 3) * 4

    def test_exponentiation_associativity(self):
        """Test right-associativity of **."""
        result = demonstrate_operator_precedence()
        assert result["expr3"] == 512  # 2 ** (3 ** 2)

    def test_mixed_operators(self):
        """Test precedence with mixed operators."""
        result = demonstrate_operator_precedence()
        assert result["expr4"] == 17  # 10 + 5 * 2 - 3

    def test_comparison_before_logical(self):
        """Test that comparison has higher precedence than logical."""
        result = demonstrate_operator_precedence()
        assert result["expr5"] is True  # 5 > 3 and 10 < 20

    def test_complex_expression(self):
        """Test complex expression with multiple operators."""
        result = demonstrate_operator_precedence()
        assert result["expr6"] is True  # 5 + 3 > 10 or 2 * 4 == 8

    def test_not_before_and(self):
        """Test that not has higher precedence than and."""
        result = demonstrate_operator_precedence()
        assert result["expr7"] is True  # not False and True

    def test_multiple_multiplications_and_additions(self):
        """Test expression with multiple * and +."""
        result = demonstrate_operator_precedence()
        assert result["expr8"] == 26  # 2 * 3 + 4 * 5

    def test_bitwise_precedence(self):
        """Test bitwise operator precedence."""
        result = demonstrate_operator_precedence()
        assert result["expr9"] == 5  # 5 | 3 & 2 (& before |)
        assert result["expr10"] == 2  # (5 | 3) & 2

    def test_very_complex_expression(self):
        """Test very complex expression."""
        result = demonstrate_operator_precedence()
        assert result["complex"] == 25.0  # 2 + 3 * 4 ** 2 / 2 - 1


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
        """Test that main() includes all operator sections."""
        main()
        captured = capsys.readouterr()

        expected_sections = [
            "ARITHMETIC OPERATORS",
            "COMPARISON OPERATORS",
            "LOGICAL OPERATORS",
            "ASSIGNMENT OPERATORS",
            "BITWISE OPERATORS",
            "MEMBERSHIP OPERATORS",
            "IDENTITY OPERATORS",
            "OPERATOR PRECEDENCE",
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
            demonstrate_arithmetic_operators,
            demonstrate_comparison_operators,
            demonstrate_logical_operators,
            demonstrate_assignment_operators,
            demonstrate_bitwise_operators,
            demonstrate_membership_operators,
            demonstrate_identity_operators,
            demonstrate_operator_precedence,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict)
            assert len(result) > 0

    def test_operator_consistency(self):
        """Test that operators produce consistent results."""
        # Run multiple times to ensure consistency
        for _ in range(3):
            arith = demonstrate_arithmetic_operators()
            assert arith["addition"] == 13

            comp = demonstrate_comparison_operators()
            assert comp["greater_than"] is True

            logic = demonstrate_logical_operators()
            assert logic["and_tf"] is False


class TestEdgeCases:
    """Test edge cases and special behaviors."""

    def test_division_by_large_number(self):
        """Test division operations."""
        result = demonstrate_arithmetic_operators()
        assert result["division"] > 3.0
        assert result["division"] < 3.5

    def test_zero_operations(self):
        """Test operations involving zero."""
        # These are implicit in the demonstrations
        assert 0 + 5 == 5
        assert 0 * 5 == 0
        assert 5 - 5 == 0

    def test_negative_number_operations(self):
        """Test operations with negative numbers."""
        assert -5 + 10 == 5
        assert -5 * 2 == -10
        assert -10 // 3 == -4  # Floor division with negative


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
