"""
Unit tests for 27_metaclasses program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_type_function,
    demonstrate_basic_metaclass,
    demonstrate_metaclass_init,
    demonstrate_singleton_metaclass,
    demonstrate_attribute_validation,
    demonstrate_method_registration,
    demonstrate_class_decoration,
    demonstrate_abstract_enforcement,
    demonstrate_class_registry,
    demonstrate_inheritance_metaclass,
    main
)


class TestTypeFunction:
    """Test cases for demonstrate_type_function()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_type_function()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_type_function()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_type_function()
        assert len(result) > 0

class TestBasicMetaclass:
    """Test cases for demonstrate_basic_metaclass()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_metaclass()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_metaclass()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_metaclass()
        assert len(result) > 0

class TestMetaclassInit:
    """Test cases for demonstrate_metaclass_init()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_metaclass_init()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_metaclass_init()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_metaclass_init()
        assert len(result) > 0

class TestSingletonMetaclass:
    """Test cases for demonstrate_singleton_metaclass()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_singleton_metaclass()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_singleton_metaclass()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_singleton_metaclass()
        assert len(result) > 0

class TestAttributeValidation:
    """Test cases for demonstrate_attribute_validation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_attribute_validation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_attribute_validation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_attribute_validation()
        assert len(result) > 0

class TestMethodRegistration:
    """Test cases for demonstrate_method_registration()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_method_registration()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_method_registration()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_method_registration()
        assert len(result) > 0

class TestClassDecoration:
    """Test cases for demonstrate_class_decoration()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_class_decoration()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_class_decoration()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_class_decoration()
        assert len(result) > 0

class TestAbstractEnforcement:
    """Test cases for demonstrate_abstract_enforcement()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_abstract_enforcement()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_abstract_enforcement()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_abstract_enforcement()
        assert len(result) > 0

class TestClassRegistry:
    """Test cases for demonstrate_class_registry()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_class_registry()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_class_registry()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_class_registry()
        assert len(result) > 0

class TestInheritanceMetaclass:
    """Test cases for demonstrate_inheritance_metaclass()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_inheritance_metaclass()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_inheritance_metaclass()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_inheritance_metaclass()
        assert len(result) > 0


class TestMainFunction:
    """Test cases for the main() function."""

    def test_main_runs_without_error(self, capsys):
        """Test that main() executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")

    def test_main_produces_output(self, capsys):
        """Test that main() produces output."""
        main()
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_main_header(self, capsys):
        """Test that main() prints header."""
        main()
        captured = capsys.readouterr()
        assert "Program 27" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
