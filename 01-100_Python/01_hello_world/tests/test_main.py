"""
Unit tests for 01_hello_world program.

These tests verify:
- Basic greeting functionality
- Parameter handling
- Edge cases
- Output format
"""

import sys
from io import StringIO
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import greet, main


class TestGreetFunction:
    """Test cases for the greet() function."""

    def test_greet_default(self):
        """Test greeting with default name (World)."""
        result = greet()
        assert result == "Hello, World!"

    def test_greet_with_name(self):
        """Test greeting with a specific name."""
        result = greet("Python")
        assert result == "Hello, Python!"

    def test_greet_with_empty_string(self):
        """Test greeting with empty string."""
        result = greet("")
        assert result == "Hello, !"

    def test_greet_with_none(self):
        """Test greeting with None (should default to World)."""
        result = greet(None)
        assert result == "Hello, World!"

    def test_greet_with_special_characters(self):
        """Test greeting with special characters in name."""
        result = greet("Python 3.11+")
        assert result == "Hello, Python 3.11+!"

    def test_greet_with_unicode(self):
        """Test greeting with unicode characters."""
        result = greet("世界")
        assert result == "Hello, 世界!"

    def test_greet_return_type(self):
        """Test that greet returns a string."""
        result = greet()
        assert isinstance(result, str)

    def test_greet_with_numbers(self):
        """Test greeting with numbers in name."""
        result = greet("2025")
        assert result == "Hello, 2025!"


class TestMainFunction:
    """Test cases for the main() function."""

    def test_main_output(self, capsys):
        """Test that main() produces output."""
        main()
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out

    def test_main_multiple_greetings(self, capsys):
        """Test that main() prints multiple greetings."""
        main()
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out
        assert "Hello, Python!" in captured.out
        assert "Hello, Vibe Coder!" in captured.out

    def test_main_welcome_message(self, capsys):
        """Test that main() prints welcome message."""
        main()
        captured = capsys.readouterr()
        assert "Welcome to Python" in captured.out

    def test_main_celebration(self, capsys):
        """Test that main() prints celebration message."""
        main()
        captured = capsys.readouterr()
        assert "Your first program is running!" in captured.out

    def test_main_no_exceptions(self):
        """Test that main() runs without exceptions."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")


class TestIntegration:
    """Integration tests for the complete program."""

    def test_program_execution(self, capsys):
        """Test complete program execution."""
        main()
        captured = capsys.readouterr()

        # Verify all expected outputs are present
        expected_outputs = [
            "Hello, World!",
            "Hello, Python!",
            "Hello, Vibe Coder!",
            "Welcome to Python",
            "Your first program is running!",
        ]

        for expected in expected_outputs:
            assert expected in captured.out, f"Expected '{expected}' in output"

    def test_output_formatting(self, capsys):
        """Test that output includes formatting elements."""
        main()
        captured = capsys.readouterr()
        # Check for separator lines
        assert "=" * 40 in captured.out


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_name(self):
        """Test greeting with very long name."""
        long_name = "A" * 1000
        result = greet(long_name)
        assert result == f"Hello, {long_name}!"

    def test_whitespace_name(self):
        """Test greeting with whitespace."""
        result = greet("   ")
        assert result == "Hello,    !"

    def test_newline_in_name(self):
        """Test greeting with newline character."""
        result = greet("Hello\nWorld")
        assert result == "Hello, Hello\nWorld!"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
