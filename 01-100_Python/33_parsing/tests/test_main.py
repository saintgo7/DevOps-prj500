"""
Unit tests for 33_parsing program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_string_parsing,
    demonstrate_json_parsing,
    demonstrate_csv_parsing,
    demonstrate_url_parsing,
    demonstrate_ast_parsing,
    demonstrate_ast_modification,
    demonstrate_expression_parser,
    demonstrate_custom_parser,
    demonstrate_tokenization,
    demonstrate_validation_parsing,
    main
)


class TestStringParsing:
    """Test cases for demonstrate_string_parsing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_string_parsing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_string_parsing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_string_parsing()
        assert len(result) > 0

class TestJsonParsing:
    """Test cases for demonstrate_json_parsing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_json_parsing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_json_parsing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_json_parsing()
        assert len(result) > 0

class TestCsvParsing:
    """Test cases for demonstrate_csv_parsing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_csv_parsing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_csv_parsing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_csv_parsing()
        assert len(result) > 0

class TestUrlParsing:
    """Test cases for demonstrate_url_parsing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_url_parsing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_url_parsing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_url_parsing()
        assert len(result) > 0

class TestAstParsing:
    """Test cases for demonstrate_ast_parsing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_ast_parsing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_ast_parsing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_ast_parsing()
        assert len(result) > 0

class TestAstModification:
    """Test cases for demonstrate_ast_modification()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_ast_modification()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_ast_modification()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_ast_modification()
        assert len(result) > 0

class TestExpressionParser:
    """Test cases for demonstrate_expression_parser()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_expression_parser()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_expression_parser()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_expression_parser()
        assert len(result) > 0

class TestCustomParser:
    """Test cases for demonstrate_custom_parser()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_custom_parser()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_custom_parser()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_custom_parser()
        assert len(result) > 0

class TestTokenization:
    """Test cases for demonstrate_tokenization()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_tokenization()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_tokenization()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_tokenization()
        assert len(result) > 0

class TestValidationParsing:
    """Test cases for demonstrate_validation_parsing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_validation_parsing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_validation_parsing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_validation_parsing()
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
        assert "Program 33" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
