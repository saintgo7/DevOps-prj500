"""
Unit tests for 48_pydantic_models program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_models,
    demonstrate_field_types,
    demonstrate_field_constraints,
    demonstrate_validators,
    demonstrate_nested_models,
    demonstrate_model_config,
    demonstrate_serialization,
    demonstrate_advanced_features,
    main
)


class TestBasicModels:
    """Test cases for demonstrate_basic_models()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_models()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_models()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_models()
        assert len(result) > 0

class TestFieldTypes:
    """Test cases for demonstrate_field_types()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_field_types()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_field_types()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_field_types()
        assert len(result) > 0

class TestFieldConstraints:
    """Test cases for demonstrate_field_constraints()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_field_constraints()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_field_constraints()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_field_constraints()
        assert len(result) > 0

class TestValidators:
    """Test cases for demonstrate_validators()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_validators()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_validators()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_validators()
        assert len(result) > 0

class TestNestedModels:
    """Test cases for demonstrate_nested_models()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_nested_models()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_nested_models()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_nested_models()
        assert len(result) > 0

class TestModelConfig:
    """Test cases for demonstrate_model_config()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_model_config()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_model_config()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_model_config()
        assert len(result) > 0

class TestSerialization:
    """Test cases for demonstrate_serialization()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_serialization()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_serialization()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_serialization()
        assert len(result) > 0

class TestAdvancedFeatures:
    """Test cases for demonstrate_advanced_features()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_advanced_features()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_advanced_features()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_advanced_features()
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
        assert "Program 48" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
