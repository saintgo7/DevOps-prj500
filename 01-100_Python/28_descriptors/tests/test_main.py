"""
Unit tests for 28_descriptors program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_descriptor,
    demonstrate_data_vs_non_data,
    demonstrate_validated_attribute,
    demonstrate_typed_attribute,
    demonstrate_lazy_property,
    demonstrate_property_implementation,
    demonstrate_method_descriptor,
    demonstrate_class_method_descriptor,
    demonstrate_static_method_descriptor,
    demonstrate_descriptor_storage_strategies,
    main
)


class TestBasicDescriptor:
    """Test cases for demonstrate_basic_descriptor()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_descriptor()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_descriptor()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_descriptor()
        assert len(result) > 0

class TestDataVsNonData:
    """Test cases for demonstrate_data_vs_non_data()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_data_vs_non_data()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_data_vs_non_data()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_data_vs_non_data()
        assert len(result) > 0

class TestValidatedAttribute:
    """Test cases for demonstrate_validated_attribute()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_validated_attribute()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_validated_attribute()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_validated_attribute()
        assert len(result) > 0

class TestTypedAttribute:
    """Test cases for demonstrate_typed_attribute()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_typed_attribute()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_typed_attribute()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_typed_attribute()
        assert len(result) > 0

class TestLazyProperty:
    """Test cases for demonstrate_lazy_property()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_lazy_property()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_lazy_property()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_lazy_property()
        assert len(result) > 0

class TestPropertyImplementation:
    """Test cases for demonstrate_property_implementation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_property_implementation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_property_implementation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_property_implementation()
        assert len(result) > 0

class TestMethodDescriptor:
    """Test cases for demonstrate_method_descriptor()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_method_descriptor()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_method_descriptor()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_method_descriptor()
        assert len(result) > 0

class TestClassMethodDescriptor:
    """Test cases for demonstrate_class_method_descriptor()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_class_method_descriptor()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_class_method_descriptor()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_class_method_descriptor()
        assert len(result) > 0

class TestStaticMethodDescriptor:
    """Test cases for demonstrate_static_method_descriptor()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_static_method_descriptor()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_static_method_descriptor()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_static_method_descriptor()
        assert len(result) > 0

class TestDescriptorStorageStrategies:
    """Test cases for demonstrate_descriptor_storage_strategies()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_descriptor_storage_strategies()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_descriptor_storage_strategies()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_descriptor_storage_strategies()
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
        assert "Program 28" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
