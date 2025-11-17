"""
Unit tests for 45_flask_templates program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_rendering,
    demonstrate_template_syntax,
    demonstrate_filters,
    demonstrate_template_inheritance,
    demonstrate_macros,
    demonstrate_includes,
    demonstrate_context_processors,
    demonstrate_advanced_features,
    main
)


class TestBasicRendering:
    """Test cases for demonstrate_basic_rendering()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_rendering()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_rendering()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_rendering()
        assert len(result) > 0

class TestTemplateSyntax:
    """Test cases for demonstrate_template_syntax()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_template_syntax()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_template_syntax()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_template_syntax()
        assert len(result) > 0

class TestFilters:
    """Test cases for demonstrate_filters()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_filters()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_filters()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_filters()
        assert len(result) > 0

class TestTemplateInheritance:
    """Test cases for demonstrate_template_inheritance()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_template_inheritance()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_template_inheritance()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_template_inheritance()
        assert len(result) > 0

class TestMacros:
    """Test cases for demonstrate_macros()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_macros()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_macros()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_macros()
        assert len(result) > 0

class TestIncludes:
    """Test cases for demonstrate_includes()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_includes()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_includes()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_includes()
        assert len(result) > 0

class TestContextProcessors:
    """Test cases for demonstrate_context_processors()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_context_processors()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_context_processors()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_context_processors()
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
        assert "Program 45" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
