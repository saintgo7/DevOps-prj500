"""
Unit tests for 04_conditional_statements program.

These tests verify:
- Basic if statements
- If-else statements
- If-elif-else chains
- Nested conditions
- Ternary operators
- Match-case statements
- Truthy/falsy handling
- Guard clauses
- Common patterns
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_if,
    demonstrate_if_else,
    demonstrate_if_elif_else,
    demonstrate_nested_conditions,
    demonstrate_ternary_operator,
    demonstrate_match_case,
    demonstrate_truthy_falsy,
    demonstrate_guard_clauses,
    demonstrate_common_patterns,
    classify_number,
    main,
)


class TestBasicIf:
    """Test cases for basic if statements."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_if()
        assert isinstance(result, dict)

    def test_can_vote(self):
        """Test voting age check."""
        result = demonstrate_basic_if()
        assert result["can_vote"] is True  # age = 20

    def test_passed(self):
        """Test pass condition."""
        result = demonstrate_basic_if()
        assert result["passed"] is True  # score = 85

    def test_grade_message(self):
        """Test grade message."""
        result = demonstrate_basic_if()
        assert result["grade_message"] == "You passed!"

    def test_weather(self):
        """Test weather condition."""
        result = demonstrate_basic_if()
        assert result["weather"] == "hot"  # temp = 30

    def test_comfortable(self):
        """Test comfortable temperature."""
        result = demonstrate_basic_if()
        assert result["comfortable"] is True  # temp = 30 > 20

    def test_authentication(self):
        """Test authentication check."""
        result = demonstrate_basic_if()
        assert result["authenticated"] is True


class TestIfElse:
    """Test cases for if-else statements."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_if_else()
        assert isinstance(result, dict)

    def test_parity_odd(self):
        """Test odd number detection."""
        result = demonstrate_if_else()
        assert result["parity"] == "odd"  # 7 is odd

    def test_minor_status(self):
        """Test minor status."""
        result = demonstrate_if_else()
        assert result["status"] == "minor"  # age = 16

    def test_cannot_drive(self):
        """Test driving permission."""
        result = demonstrate_if_else()
        assert result["can_drive"] is False  # age = 16, even with license


class TestIfElifElse:
    """Test cases for if-elif-else chains."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_if_elif_else()
        assert isinstance(result, dict)

    def test_letter_grade_b(self):
        """Test B grade classification."""
        result = demonstrate_if_elif_else()
        assert result["letter_grade"] == "B"  # score = 85

    def test_temp_category_warm(self):
        """Test warm temperature classification."""
        result = demonstrate_if_elif_else()
        assert result["temp_category"] == "warm"  # temp = 25

    def test_age_group_adult(self):
        """Test adult age group."""
        result = demonstrate_if_elif_else()
        assert result["age_group"] == "adult"  # age = 35


class TestNestedConditions:
    """Test cases for nested conditions."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_nested_conditions()
        assert isinstance(result, dict)

    def test_can_drive_own_car(self):
        """Test can drive own car."""
        result = demonstrate_nested_conditions()
        assert result["can_drive_own_car"] is True

    def test_final_result_pass(self):
        """Test final result is pass."""
        result = demonstrate_nested_conditions()
        assert result["final_result"] == "Pass"

    def test_access_level_full(self):
        """Test full access level."""
        result = demonstrate_nested_conditions()
        assert result["access_level"] == "full"


class TestTernaryOperator:
    """Test cases for ternary operator."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_ternary_operator()
        assert isinstance(result, dict)

    def test_adult_status(self):
        """Test adult status with ternary."""
        result = demonstrate_ternary_operator()
        assert result["status"] == "adult"  # age = 20

    def test_parity_odd(self):
        """Test odd parity with ternary."""
        result = demonstrate_ternary_operator()
        assert result["parity"] == "odd"  # 7 is odd

    def test_nested_ternary_grade(self):
        """Test nested ternary for grade."""
        result = demonstrate_ternary_operator()
        assert result["grade"] == "B"  # score = 85

    def test_max_value(self):
        """Test maximum value selection."""
        result = demonstrate_ternary_operator()
        assert result["max_value"] == 10  # max(10, 5)

    def test_min_value(self):
        """Test minimum value selection."""
        result = demonstrate_ternary_operator()
        assert result["min_value"] == 5  # min(10, 5)

    def test_operation_result(self):
        """Test conditional operation execution."""
        result = demonstrate_ternary_operator()
        assert result["operation_result"] == "cheap result"


class TestMatchCase:
    """Test cases for match-case statements."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_match_case()
        assert isinstance(result, dict)

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
    def test_match_case_supported(self):
        """Test match-case is supported."""
        result = demonstrate_match_case()
        assert result["match_case_supported"] is True

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
    def test_day_type_monday(self):
        """Test Monday classification."""
        result = demonstrate_match_case()
        assert result["day_type"] == "Start of week"

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
    def test_http_message_ok(self):
        """Test HTTP 200 message."""
        result = demonstrate_match_case()
        assert result["http_message"] == "OK"

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
    def test_point_location_origin(self):
        """Test origin point classification."""
        result = demonstrate_match_case()
        assert result["point_location"] == "Origin"

    @pytest.mark.skipif(sys.version_info >= (3, 10), reason="Tests Python < 3.10")
    def test_match_case_not_supported(self):
        """Test match-case not supported message."""
        result = demonstrate_match_case()
        assert result["match_case_supported"] is False
        assert "3.10" in result["message"]


class TestTruthyFalsy:
    """Test cases for truthy and falsy values."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_truthy_falsy()
        assert isinstance(result, dict)

    def test_falsy_count(self):
        """Test count of falsy values."""
        result = demonstrate_truthy_falsy()
        assert result["falsy_count"] == 8  # All falsy values

    def test_truthy_count(self):
        """Test count of truthy values."""
        result = demonstrate_truthy_falsy()
        assert result["truthy_count"] == 6  # All truthy values

    def test_has_name(self):
        """Test name existence check."""
        result = demonstrate_truthy_falsy()
        assert result["has_name"] is True

    def test_list_is_empty(self):
        """Test empty list check."""
        result = demonstrate_truthy_falsy()
        assert result["list_is_empty"] is True

    def test_default_username(self):
        """Test default username fallback."""
        result = demonstrate_truthy_falsy()
        assert result["username"] == "Guest"  # Empty input

    def test_has_value_false(self):
        """Test optional value is None."""
        result = demonstrate_truthy_falsy()
        assert result["has_value"] is False


class TestGuardClauses:
    """Test cases for guard clauses."""

    def test_guard_none_value(self):
        """Test guard clause for None."""
        result = demonstrate_guard_clauses(None)
        assert result["error"] == "Value is None"
        assert result["processed"] is False

    def test_guard_negative_value(self):
        """Test guard clause for negative values."""
        result = demonstrate_guard_clauses(-5)
        assert result["error"] == "Value is negative"
        assert result["processed"] is False

    def test_guard_too_large(self):
        """Test guard clause for values too large."""
        result = demonstrate_guard_clauses(150)
        assert result["error"] == "Value too large"
        assert result["processed"] is False

    def test_successful_processing(self):
        """Test successful processing when guards pass."""
        result = demonstrate_guard_clauses(10)
        assert result["processed"] is True
        assert result["value"] == 10
        assert result["squared"] == 100

    def test_edge_case_zero(self):
        """Test edge case with zero."""
        result = demonstrate_guard_clauses(0)
        assert result["processed"] is True
        assert result["value"] == 0
        assert result["squared"] == 0

    def test_edge_case_max_valid(self):
        """Test edge case with maximum valid value."""
        result = demonstrate_guard_clauses(100)
        assert result["processed"] is True
        assert result["value"] == 100
        assert result["squared"] == 10000


class TestCommonPatterns:
    """Test cases for common conditional patterns."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_common_patterns()
        assert isinstance(result, dict)

    def test_working_age(self):
        """Test working age range check."""
        result = demonstrate_common_patterns()
        assert result["working_age"] is True  # 25 is in range

    def test_all_positive(self):
        """Test all() pattern."""
        result = demonstrate_common_patterns()
        assert result["all_positive"] is True

    def test_any_passing(self):
        """Test any() pattern."""
        result = demonstrate_common_patterns()
        assert result["any_passing"] is True

    def test_is_privileged(self):
        """Test membership check pattern."""
        result = demonstrate_common_patterns()
        assert result["is_privileged"] is True

    def test_is_integer(self):
        """Test type checking pattern."""
        result = demonstrate_common_patterns()
        assert result["is_integer"] is True

    def test_log_level(self):
        """Test dictionary get with default pattern."""
        result = demonstrate_common_patterns()
        assert result["log_level"] == "DEBUG"

    def test_display_name(self):
        """Test null coalescing pattern."""
        result = demonstrate_common_patterns()
        assert result["display_name"] == "Smith"  # first_name is None


class TestClassifyNumber:
    """Test cases for classify_number function."""

    def test_positive_even_large(self):
        """Test positive, even, large number."""
        result = classify_number(150)
        assert "positive" in result
        assert "even" in result
        assert "large" in result

    def test_negative_odd_small(self):
        """Test negative, odd, small number."""
        result = classify_number(-7)
        assert "negative" in result
        assert "odd" in result
        assert "small" in result

    def test_zero(self):
        """Test zero classification."""
        result = classify_number(0)
        assert "zero" in result
        assert "even" not in result  # Zero is not classified as even/odd
        assert "odd" not in result

    def test_positive_odd_medium(self):
        """Test positive, odd, medium number."""
        result = classify_number(15)
        assert "positive" in result
        assert "odd" in result
        assert "medium" in result

    def test_negative_even_medium(self):
        """Test negative, even, medium number."""
        result = classify_number(-50)
        assert "negative" in result
        assert "even" in result
        assert "medium" in result


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
            "BASIC IF STATEMENTS",
            "IF-ELSE STATEMENTS",
            "IF-ELIF-ELSE CHAINS",
            "NESTED CONDITIONS",
            "TERNARY OPERATOR",
            "MATCH-CASE",
            "TRUTHY AND FALSY",
            "GUARD CLAUSES",
            "COMMON PATTERNS",
            "NUMBER CLASSIFICATION",
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
            demonstrate_basic_if,
            demonstrate_if_else,
            demonstrate_if_elif_else,
            demonstrate_nested_conditions,
            demonstrate_ternary_operator,
            demonstrate_match_case,
            demonstrate_truthy_falsy,
            demonstrate_common_patterns,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict)
            assert len(result) > 0

    def test_guard_clauses_with_valid_values(self):
        """Test guard clauses with various valid values."""
        valid_values = [0, 1, 50, 100]
        for value in valid_values:
            result = demonstrate_guard_clauses(value)
            assert result["processed"] is True
            assert result["value"] == value

    def test_guard_clauses_with_invalid_values(self):
        """Test guard clauses with various invalid values."""
        invalid_values = [None, -1, -100, 101, 1000]
        for value in invalid_values:
            result = demonstrate_guard_clauses(value)
            assert result["processed"] is False
            assert "error" in result


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_classify_number_boundary_values(self):
        """Test classification with boundary values."""
        # Test boundaries for magnitude
        assert "small" in classify_number(1)
        assert "small" in classify_number(10)
        assert "medium" in classify_number(11)
        assert "medium" in classify_number(100)
        assert "large" in classify_number(101)

    def test_guard_clauses_boundaries(self):
        """Test guard clauses at boundaries."""
        # Just inside valid range
        result_0 = demonstrate_guard_clauses(0)
        assert result_0["processed"] is True

        result_100 = demonstrate_guard_clauses(100)
        assert result_100["processed"] is True

        # Just outside valid range
        result_neg1 = demonstrate_guard_clauses(-1)
        assert result_neg1["processed"] is False

        result_101 = demonstrate_guard_clauses(101)
        assert result_101["processed"] is False

    def test_empty_classifications(self):
        """Test that zero gets only 'zero' classification."""
        result = classify_number(0)
        parts = result.split(", ")
        assert len(parts) == 1
        assert parts[0] == "zero"


class TestRealWorldScenarios:
    """Test real-world scenario usage."""

    def test_age_verification_scenarios(self):
        """Test various age verification scenarios."""
        # Test data: (age, expected_can_vote)
        test_cases = [
            (17, False),
            (18, True),
            (25, True),
            (100, True),
        ]

        for age, expected in test_cases:
            can_vote = age >= 18
            assert can_vote == expected

    def test_grade_classification_scenarios(self):
        """Test grade classification scenarios."""
        # Test data: (score, expected_grade)
        test_cases = [
            (95, "A"),
            (85, "B"),
            (75, "C"),
            (65, "D"),
            (55, "F"),
        ]

        for score, expected in test_cases:
            if score >= 90:
                grade = "A"
            elif score >= 80:
                grade = "B"
            elif score >= 70:
                grade = "C"
            elif score >= 60:
                grade = "D"
            else:
                grade = "F"

            assert grade == expected


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
