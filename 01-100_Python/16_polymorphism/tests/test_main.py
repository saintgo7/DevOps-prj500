"""
Unit tests for 16_polymorphism program.

These tests verify:
- Duck typing
- Method overriding
- Operator overloading
- Protocol polymorphism
- Abstract polymorphism
- Function polymorphism
- Interface segregation
- Liskov substitution
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_duck_typing,
    demonstrate_method_overriding,
    demonstrate_operator_overloading,
    demonstrate_protocol_polymorphism,
    demonstrate_abstract_polymorphism,
    demonstrate_function_polymorphism,
    demonstrate_interface_segregation,
    demonstrate_liskov_substitution,
    main,
)


class TestDuckTyping:
    """Test cases for demonstrate_duck_typing()."""

    def test_different_speaks(self):
        """Test different objects with speak method."""
        result = demonstrate_duck_typing()
        assert result["dog_sound"] == "Woof!"
        assert result["cat_sound"] == "Meow!"
        assert result["robot_sound"] == "Beep boop!"


class TestMethodOverriding:
    """Test cases for demonstrate_method_overriding()."""

    def test_generic_sound(self):
        """Test generic animal sound."""
        result = demonstrate_method_overriding()
        assert "Generic" in result["generic_sound"]

    def test_dog_sound(self):
        """Test dog sound."""
        result = demonstrate_method_overriding()
        assert result["dog_sound"] == "Woof!"

    def test_bird_sound(self):
        """Test bird sound."""
        result = demonstrate_method_overriding()
        assert result["bird_sound"] == "Chirp!"


class TestOperatorOverloading:
    """Test cases for demonstrate_operator_overloading()."""

    def test_vector_addition(self):
        """Test vector addition."""
        result = demonstrate_operator_overloading()
        assert "4" in result["addition"]
        assert "6" in result["addition"]

    def test_vector_subtraction(self):
        """Test vector subtraction."""
        result = demonstrate_operator_overloading()
        assert "2" in result["subtraction"]

    def test_vector_multiplication(self):
        """Test vector multiplication."""
        result = demonstrate_operator_overloading()
        assert "3" in result["multiplication"]

    def test_vector_equality(self):
        """Test vector equality."""
        result = demonstrate_operator_overloading()
        assert result["equality"] is True


class TestProtocolPolymorphism:
    """Test cases for demonstrate_protocol_polymorphism()."""

    def test_circle_drawing(self):
        """Test circle drawing."""
        result = demonstrate_protocol_polymorphism()
        assert "circle" in result["circle"].lower()
        assert "5" in result["circle"]

    def test_square_drawing(self):
        """Test square drawing."""
        result = demonstrate_protocol_polymorphism()
        assert "square" in result["square"].lower()

    def test_triangle_drawing(self):
        """Test triangle drawing."""
        result = demonstrate_protocol_polymorphism()
        assert "triangle" in result["triangle"].lower()


class TestAbstractPolymorphism:
    """Test cases for demonstrate_abstract_polymorphism()."""

    def test_credit_card_payment(self):
        """Test credit card payment."""
        result = demonstrate_abstract_polymorphism()
        cc_result = result["credit_card"]
        assert cc_result["fee"] == 3.0
        assert cc_result["total"] == 103.0

    def test_paypal_payment(self):
        """Test PayPal payment."""
        result = demonstrate_abstract_polymorphism()
        pp_result = result["paypal"]
        assert pp_result["fee"] == 2.5

    def test_bank_transfer_payment(self):
        """Test bank transfer payment."""
        result = demonstrate_abstract_polymorphism()
        bt_result = result["bank_transfer"]
        assert bt_result["fee"] == 1.0


class TestFunctionPolymorphism:
    """Test cases for demonstrate_function_polymorphism()."""

    def test_len_polymorphism(self):
        """Test len() with different types."""
        result = demonstrate_function_polymorphism()
        assert result["string_len"] == 5
        assert result["list_len"] == 5
        assert result["dict_len"] == 2

    def test_custom_len(self):
        """Test custom __len__ implementation."""
        result = demonstrate_function_polymorphism()
        assert result["playlist_len"] == 3


class TestInterfaceSegregation:
    """Test cases for demonstrate_interface_segregation()."""

    def test_simple_printer(self):
        """Test simple printer."""
        result = demonstrate_interface_segregation()
        assert "Printing" in result["simple_print"]

    def test_multifunction_device(self):
        """Test multifunction device."""
        result = demonstrate_interface_segregation()
        assert "Printing" in result["mfd_print"]
        assert "Scanning" in result["mfd_scan"]
        assert "Faxing" in result["mfd_fax"]

    def test_interface_implementation(self):
        """Test interface implementation."""
        result = demonstrate_interface_segregation()
        assert result["simple_can_scan"] is False
        assert result["mfd_can_scan"] is True


class TestLiskovSubstitution:
    """Test cases for demonstrate_liskov_substitution()."""

    def test_sparrow_movement(self):
        """Test sparrow movement."""
        result = demonstrate_liskov_substitution()
        assert result["sparrow_move"] == "Flying"

    def test_penguin_movement(self):
        """Test penguin movement."""
        result = demonstrate_liskov_substitution()
        assert result["penguin_move"] == "Walking"

    def test_specific_abilities(self):
        """Test specific abilities."""
        result = demonstrate_liskov_substitution()
        assert "sky" in result["sparrow_fly"]
        assert "ground" in result["penguin_walk"]


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

        assert "Program 16: Polymorphism" in captured.out


class TestIntegration:
    """Integration tests for polymorphism."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_duck_typing,
            demonstrate_method_overriding,
            demonstrate_operator_overloading,
            demonstrate_protocol_polymorphism,
            demonstrate_abstract_polymorphism,
            demonstrate_function_polymorphism,
            demonstrate_interface_segregation,
            demonstrate_liskov_substitution,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
