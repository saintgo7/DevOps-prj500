"""
Unit tests for 39_design_patterns program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_singleton,
    demonstrate_factory,
    demonstrate_observer,
    demonstrate_strategy,
    demonstrate_decorator_pattern,
    demonstrate_adapter,
    demonstrate_command,
    demonstrate_builder,
    demonstrate_template_method,
    demonstrate_dependency_injection,
    main
)


class TestSingleton:
    """Test cases for demonstrate_singleton()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_singleton()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_singleton()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_singleton()
        assert len(result) > 0

class TestFactory:
    """Test cases for demonstrate_factory()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_factory()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_factory()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_factory()
        assert len(result) > 0

class TestObserver:
    """Test cases for demonstrate_observer()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_observer()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_observer()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_observer()
        assert len(result) > 0

class TestStrategy:
    """Test cases for demonstrate_strategy()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_strategy()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_strategy()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_strategy()
        assert len(result) > 0

class TestDecoratorPattern:
    """Test cases for demonstrate_decorator_pattern()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_decorator_pattern()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_decorator_pattern()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_decorator_pattern()
        assert len(result) > 0

class TestAdapter:
    """Test cases for demonstrate_adapter()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_adapter()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_adapter()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_adapter()
        assert len(result) > 0

class TestCommand:
    """Test cases for demonstrate_command()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_command()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_command()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_command()
        assert len(result) > 0

class TestBuilder:
    """Test cases for demonstrate_builder()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_builder()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_builder()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_builder()
        assert len(result) > 0

class TestTemplateMethod:
    """Test cases for demonstrate_template_method()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_template_method()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_template_method()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_template_method()
        assert len(result) > 0

class TestDependencyInjection:
    """Test cases for demonstrate_dependency_injection()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_dependency_injection()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_dependency_injection()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_dependency_injection()
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
        assert "Program 39" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
