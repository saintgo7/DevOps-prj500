"""
Unit tests for 14_classes_objects program.

These tests verify:
- Basic class definition
- Class vs instance attributes
- Different method types
- Special methods
- Properties
- Private attributes
- Composition
- Dataclasses
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_class,
    demonstrate_class_attributes,
    demonstrate_methods,
    demonstrate_special_methods,
    demonstrate_properties,
    demonstrate_private_attributes,
    demonstrate_class_composition,
    demonstrate_dataclasses,
    main,
)


class TestBasicClass:
    """Test cases for demonstrate_basic_class()."""

    def test_person_names(self):
        """Test person names."""
        result = demonstrate_basic_class()
        assert result["person1_name"] == "Alice"
        assert result["person2_name"] == "Bob"

    def test_greeting(self):
        """Test greeting method."""
        result = demonstrate_basic_class()
        assert "Alice" in result["greeting_before"]
        assert "25" in result["greeting_before"]

    def test_birthday_method(self):
        """Test birthday method."""
        result = demonstrate_basic_class()
        assert result["person1_age"] == 26


class TestClassAttributes:
    """Test cases for demonstrate_class_attributes()."""

    def test_instance_counts(self):
        """Test instance vs class attributes."""
        result = demonstrate_class_attributes()
        assert result["c1_count"] == 2
        assert result["c2_count"] == 1

    def test_total_count(self):
        """Test class attribute shared across instances."""
        result = demonstrate_class_attributes()
        assert result["total_count"] == 2

    def test_shared_attribute(self):
        """Test shared attribute."""
        result = demonstrate_class_attributes()
        assert result["shared_attribute"] is True


class TestMethods:
    """Test cases for demonstrate_methods()."""

    def test_instance_method(self):
        """Test instance method."""
        result = demonstrate_methods()
        assert result["instance_method"] == 30.8

    def test_class_method(self):
        """Test class method."""
        result = demonstrate_methods()
        assert result["after_class_method"] == 30.8

    def test_static_method(self):
        """Test static method."""
        result = demonstrate_methods()
        assert result["static_method"] is True

    def test_history_tracking(self):
        """Test history tracking."""
        result = demonstrate_methods()
        assert len(result["history"]) >= 1


class TestSpecialMethods:
    """Test cases for demonstrate_special_methods()."""

    def test_str_method(self):
        """Test __str__ method."""
        result = demonstrate_special_methods()
        assert "Python Basics" in result["str"]
        assert "300" in result["str"]

    def test_len_method(self):
        """Test __len__ method."""
        result = demonstrate_special_methods()
        assert result["len"] == 300

    def test_equality(self):
        """Test __eq__ method."""
        result = demonstrate_special_methods()
        assert result["equality"] is True
        assert result["not_equal"] is False

    def test_comparison(self):
        """Test __lt__ method."""
        result = demonstrate_special_methods()
        assert result["comparison"] is True

    def test_addition(self):
        """Test __add__ method."""
        result = demonstrate_special_methods()
        assert result["addition"] == 800


class TestProperties:
    """Test cases for demonstrate_properties()."""

    def test_initial_temperature(self):
        """Test initial temperature."""
        result = demonstrate_properties()
        assert result["initial_celsius"] == 0
        assert result["initial_fahrenheit"] == 32

    def test_boiling_point(self):
        """Test boiling point conversion."""
        result = demonstrate_properties()
        assert result["boiling_celsius"] == 100
        assert result["boiling_fahrenheit"] == 212

    def test_freezing_point(self):
        """Test setting via fahrenheit."""
        result = demonstrate_properties()
        assert result["freezing_celsius"] == 0

    def test_validation(self):
        """Test property validation."""
        result = demonstrate_properties()
        assert result["validation_works"] is True


class TestPrivateAttributes:
    """Test cases for demonstrate_private_attributes()."""

    def test_initial_balance(self):
        """Test initial balance."""
        result = demonstrate_private_attributes()
        assert result["initial_balance"] == 1000

    def test_deposit(self):
        """Test deposit operation."""
        result = demonstrate_private_attributes()
        assert result["after_deposit"] == 1500

    def test_withdraw(self):
        """Test withdraw operation."""
        result = demonstrate_private_attributes()
        assert result["after_withdraw"] == 1300

    def test_name_mangling(self):
        """Test name mangling for private attributes."""
        result = demonstrate_private_attributes()
        assert result["has_private_attr"] is False
        assert result["has_mangled_attr"] is True


class TestClassComposition:
    """Test cases for demonstrate_class_composition()."""

    def test_car_brand(self):
        """Test car brand."""
        result = demonstrate_class_composition()
        assert result["car_brand"] == "Toyota"

    def test_engine_horsepower(self):
        """Test engine horsepower."""
        result = demonstrate_class_composition()
        assert result["engine_hp"] == 150

    def test_start_message(self):
        """Test start message."""
        result = demonstrate_class_composition()
        assert "Toyota" in result["start_message"]
        assert "150" in result["start_message"]


class TestDataclasses:
    """Test cases for demonstrate_dataclasses()."""

    def test_student_average(self):
        """Test student average calculation."""
        result = demonstrate_dataclasses()
        assert abs(result["student1_avg"] - 87.67) < 0.1
        assert abs(result["student2_avg"] - 91.67) < 0.1

    def test_auto_repr(self):
        """Test automatic __repr__ generation."""
        result = demonstrate_dataclasses()
        assert "Alice" in result["student1"]


class TestMainFunction:
    """Test cases for the main() function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    def test_main_output(self, capsys):
        """Test that main produces expected output."""
        main()
        captured = capsys.readouterr()

        assert "Program 14: Classes and Objects" in captured.out


class TestIntegration:
    """Integration tests for classes and objects."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_basic_class,
            demonstrate_class_attributes,
            demonstrate_methods,
            demonstrate_special_methods,
            demonstrate_properties,
            demonstrate_private_attributes,
            demonstrate_class_composition,
            demonstrate_dataclasses,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
