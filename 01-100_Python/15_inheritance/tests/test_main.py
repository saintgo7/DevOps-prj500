"""
Unit tests for 15_inheritance program.

These tests verify:
- Basic inheritance
- super() function
- Multiple inheritance
- Method resolution order
- Abstract classes
- Polymorphism
- Composition vs inheritance
- Mixins
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_inheritance,
    demonstrate_super,
    demonstrate_multiple_inheritance,
    demonstrate_method_resolution_order,
    demonstrate_abstract_classes,
    demonstrate_polymorphism,
    demonstrate_composition_vs_inheritance,
    demonstrate_mixins,
    main,
)


class TestBasicInheritance:
    """Test cases for demonstrate_basic_inheritance()."""

    def test_dog_speak(self):
        """Test dog speak method."""
        result = demonstrate_basic_inheritance()
        assert result["dog_speak"] == "Woof!"

    def test_cat_speak(self):
        """Test cat speak method."""
        result = demonstrate_basic_inheritance()
        assert result["cat_speak"] == "Meow!"

    def test_inheritance_check(self):
        """Test isinstance with inheritance."""
        result = demonstrate_basic_inheritance()
        assert result["dog_is_animal"] is True
        assert result["dog_is_dog"] is True


class TestSuper:
    """Test cases for demonstrate_super()."""

    def test_student_intro(self):
        """Test student introduction."""
        result = demonstrate_super()
        assert "Alice" in result["student_intro"]
        assert "S12345" in result["student_intro"]

    def test_grad_intro(self):
        """Test graduate student introduction."""
        result = demonstrate_super()
        assert "Bob" in result["grad_intro"]
        assert "AI" in result["grad_intro"]


class TestMultipleInheritance:
    """Test cases for demonstrate_multiple_inheritance()."""

    def test_duck_abilities(self):
        """Test duck has both fly and swim."""
        result = demonstrate_multiple_inheritance()
        assert "Flying" in result["duck_fly"]
        assert "Swimming" in result["duck_swim"]

    def test_penguin_abilities(self):
        """Test penguin can swim but not fly."""
        result = demonstrate_multiple_inheritance()
        assert "Swimming" in result["penguin_swim"]
        assert result["penguin_can_fly"] is False

    def test_mro(self):
        """Test method resolution order."""
        result = demonstrate_multiple_inheritance()
        mro = result["mro"]
        assert "Duck" in mro
        assert "Flyer" in mro
        assert "Swimmer" in mro


class TestMethodResolutionOrder:
    """Test cases for demonstrate_method_resolution_order()."""

    def test_diamond_inheritance(self):
        """Test diamond inheritance MRO."""
        result = demonstrate_method_resolution_order()
        assert result["d_method"] == "B"
        assert result["e_method"] == "E -> B"

    def test_mro_order(self):
        """Test MRO lists."""
        result = demonstrate_method_resolution_order()
        d_mro = result["d_mro"]
        assert d_mro[0] == "D"
        assert "B" in d_mro
        assert "C" in d_mro


class TestAbstractClasses:
    """Test cases for demonstrate_abstract_classes()."""

    def test_rectangle_description(self):
        """Test rectangle description."""
        result = demonstrate_abstract_classes()
        assert "Rectangle" in result["rectangle_desc"]
        assert "15.00" in result["rectangle_desc"]

    def test_circle_description(self):
        """Test circle description."""
        result = demonstrate_abstract_classes()
        assert "Circle" in result["circle_desc"]

    def test_cannot_instantiate_abc(self):
        """Test cannot instantiate abstract class."""
        result = demonstrate_abstract_classes()
        assert result["can_instantiate_abc"] is False

    def test_isinstance_check(self):
        """Test isinstance with ABC."""
        result = demonstrate_abstract_classes()
        assert result["rect_is_shape"] is True


class TestPolymorphism:
    """Test cases for demonstrate_polymorphism()."""

    def test_car_movement(self):
        """Test car movement."""
        result = demonstrate_polymorphism()
        assert "driving" in result["car_move"]

    def test_boat_movement(self):
        """Test boat movement."""
        result = demonstrate_polymorphism()
        assert "sailing" in result["boat_move"]

    def test_plane_movement(self):
        """Test plane movement."""
        result = demonstrate_polymorphism()
        assert "flying" in result["plane_move"]


class TestCompositionVsInheritance:
    """Test cases for demonstrate_composition_vs_inheritance()."""

    def test_inheritance_approach(self):
        """Test inheritance approach."""
        result = demonstrate_composition_vs_inheritance()
        assert result["inheritance_name"] == "Alice"
        assert result["inheritance_dept"] == "IT"

    def test_composition_approach(self):
        """Test composition approach."""
        result = demonstrate_composition_vs_inheritance()
        assert result["composition_name"] == "Bob"
        assert result["composition_dept"] == "HR"


class TestMixins:
    """Test cases for demonstrate_mixins()."""

    def test_json_mixin(self):
        """Test JSON mixin."""
        result = demonstrate_mixins()
        assert "alice" in result["json_output"]

    def test_log_mixin(self):
        """Test log mixin."""
        result = demonstrate_mixins()
        assert "User" in result["log_output"]

    def test_mixin_attributes(self):
        """Test that mixins add methods."""
        result = demonstrate_mixins()
        assert result["has_to_json"] is True
        assert result["has_log"] is True


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

        assert "Program 15: Inheritance" in captured.out


class TestIntegration:
    """Integration tests for inheritance."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_basic_inheritance,
            demonstrate_super,
            demonstrate_multiple_inheritance,
            demonstrate_method_resolution_order,
            demonstrate_abstract_classes,
            demonstrate_polymorphism,
            demonstrate_composition_vs_inheritance,
            demonstrate_mixins,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
