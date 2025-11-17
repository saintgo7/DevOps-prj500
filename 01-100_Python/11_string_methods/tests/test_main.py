"""
Unit tests for 11_string_methods program.

These tests verify:
- Case conversion methods
- Search methods
- Check methods
- Modification methods
- Split and join methods
- Alignment methods
- Formatting methods
- Encoding methods
- Advanced string methods
- Edge cases
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_case_methods,
    demonstrate_search_methods,
    demonstrate_check_methods,
    demonstrate_modification_methods,
    demonstrate_split_join_methods,
    demonstrate_alignment_methods,
    demonstrate_formatting_methods,
    demonstrate_encoding_methods,
    demonstrate_advanced_methods,
    main,
)


class TestCaseMethods:
    """Test cases for demonstrate_case_methods()."""

    def test_lower_method(self):
        """Test lower() method."""
        result = demonstrate_case_methods()
        assert result["lower"] == "hello world python"

    def test_upper_method(self):
        """Test upper() method."""
        result = demonstrate_case_methods()
        assert result["upper"] == "HELLO WORLD PYTHON"

    def test_title_method(self):
        """Test title() method."""
        result = demonstrate_case_methods()
        assert result["title"] == "Hello World Python"

    def test_capitalize_method(self):
        """Test capitalize() method."""
        result = demonstrate_case_methods()
        assert result["capitalize"] == "Hello world python"

    def test_swapcase_method(self):
        """Test swapcase() method."""
        result = demonstrate_case_methods()
        assert result["swapcase"] == "hELLO wORLD pYTHON"


class TestSearchMethods:
    """Test cases for demonstrate_search_methods()."""

    def test_find_method(self):
        """Test find() method."""
        result = demonstrate_search_methods()
        assert result["find_hello"] == 0

    def test_find_with_start(self):
        """Test find() with start parameter."""
        result = demonstrate_search_methods()
        assert result["find_hello_start_10"] == 13

    def test_find_missing(self):
        """Test find() with missing substring."""
        result = demonstrate_search_methods()
        assert result["find_missing"] == -1

    def test_rfind_method(self):
        """Test rfind() method."""
        result = demonstrate_search_methods()
        assert result["rfind_hello"] == 13

    def test_count_method(self):
        """Test count() method."""
        result = demonstrate_search_methods()
        assert result["count_hello"] == 2
        assert result["count_o"] == 4

    def test_startswith_method(self):
        """Test startswith() method."""
        result = demonstrate_search_methods()
        assert result["startswith_hello"] is True

    def test_endswith_method(self):
        """Test endswith() method."""
        result = demonstrate_search_methods()
        assert result["endswith_python"] is True


class TestCheckMethods:
    """Test cases for demonstrate_check_methods()."""

    def test_isalpha_method(self):
        """Test isalpha() method."""
        result = demonstrate_check_methods()
        assert result["isalpha"]["abc"] is True
        assert result["isalpha"]["abc123"] is False

    def test_isdigit_method(self):
        """Test isdigit() method."""
        result = demonstrate_check_methods()
        assert result["isdigit"]["123"] is True
        assert result["isdigit"]["12.3"] is False

    def test_isalnum_method(self):
        """Test isalnum() method."""
        result = demonstrate_check_methods()
        assert result["isalnum"]["abc123"] is True
        assert result["isalnum"]["abc 123"] is False

    def test_islower_method(self):
        """Test islower() method."""
        result = demonstrate_check_methods()
        assert result["islower"]["hello"] is True
        assert result["islower"]["Hello"] is False

    def test_isupper_method(self):
        """Test isupper() method."""
        result = demonstrate_check_methods()
        assert result["isupper"]["HELLO"] is True
        assert result["isupper"]["Hello"] is False


class TestModificationMethods:
    """Test cases for demonstrate_modification_methods()."""

    def test_strip_method(self):
        """Test strip() method."""
        result = demonstrate_modification_methods()
        assert result["strip"] == "hello"

    def test_lstrip_method(self):
        """Test lstrip() method."""
        result = demonstrate_modification_methods()
        assert result["lstrip"] == "hello  "

    def test_rstrip_method(self):
        """Test rstrip() method."""
        result = demonstrate_modification_methods()
        assert result["rstrip"] == "  hello"

    def test_replace_method(self):
        """Test replace() method."""
        result = demonstrate_modification_methods()
        assert result["replace"] == "hello python"


class TestSplitJoinMethods:
    """Test cases for demonstrate_split_join_methods()."""

    def test_split_comma(self):
        """Test split() with comma."""
        result = demonstrate_split_join_methods()
        assert result["split_comma"] == ["apple", "banana", "cherry"]

    def test_split_whitespace(self):
        """Test split() with default whitespace."""
        result = demonstrate_split_join_methods()
        assert result["split_whitespace"] == ["hello", "world", "python"]

    def test_splitlines_method(self):
        """Test splitlines() method."""
        result = demonstrate_split_join_methods()
        assert result["splitlines"] == ["line1", "line2", "line3"]

    def test_join_comma(self):
        """Test join() with comma."""
        result = demonstrate_split_join_methods()
        assert result["join_comma"] == "a,b,c"

    def test_join_space(self):
        """Test join() with space."""
        result = demonstrate_split_join_methods()
        assert result["join_space"] == "hello world"


class TestAlignmentMethods:
    """Test cases for demonstrate_alignment_methods()."""

    def test_center_method(self):
        """Test center() method."""
        result = demonstrate_alignment_methods()
        assert len(result["center_20"]) == 20
        assert "hello" in result["center_20"]

    def test_ljust_method(self):
        """Test ljust() method."""
        result = demonstrate_alignment_methods()
        assert len(result["ljust_20"]) == 20

    def test_rjust_method(self):
        """Test rjust() method."""
        result = demonstrate_alignment_methods()
        assert len(result["rjust_20"]) == 20

    def test_zfill_method(self):
        """Test zfill() method."""
        result = demonstrate_alignment_methods()
        assert result["zfill_10"] == "0000000042"


class TestFormattingMethods:
    """Test cases for demonstrate_formatting_methods()."""

    def test_old_style_formatting(self):
        """Test old-style % formatting."""
        result = demonstrate_formatting_methods()
        assert "Alice" in result["old_style"]
        assert "25" in result["old_style"]

    def test_format_method(self):
        """Test str.format() method."""
        result = demonstrate_formatting_methods()
        assert "Bob" in result["format_positional"]

    def test_fstring_formatting(self):
        """Test f-string formatting."""
        result = demonstrate_formatting_methods()
        assert "David" in result["fstring"]

    def test_template_formatting(self):
        """Test Template string formatting."""
        result = demonstrate_formatting_methods()
        assert "Eve" in result["template"]


class TestEncodingMethods:
    """Test cases for demonstrate_encoding_methods()."""

    def test_encode_utf8(self):
        """Test UTF-8 encoding."""
        result = demonstrate_encoding_methods()
        assert isinstance(result["utf8_bytes"], bytes)

    def test_decode_method(self):
        """Test decoding."""
        result = demonstrate_encoding_methods()
        assert result["decoded"] == result["original"]

    def test_bytes_length(self):
        """Test byte length vs string length."""
        result = demonstrate_encoding_methods()
        # UTF-8 encoding of Chinese characters uses more bytes
        assert result["bytes_length_utf8"] > result["str_length"]


class TestAdvancedMethods:
    """Test cases for demonstrate_advanced_methods()."""

    def test_translate_method(self):
        """Test translate() method."""
        result = demonstrate_advanced_methods()
        assert "h" not in result["translate"]

    def test_expandtabs_method(self):
        """Test expandtabs() method."""
        result = demonstrate_advanced_methods()
        assert "\t" not in result["expandtabs"]

    def test_raw_string(self):
        """Test raw string."""
        result = demonstrate_advanced_methods()
        assert result["raw_equals_normal"] is True


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

        assert "Program 11: String Methods" in captured.out
        assert "Case Methods:" in captured.out
        assert "Search Methods:" in captured.out


class TestIntegration:
    """Integration tests for string methods."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_case_methods,
            demonstrate_search_methods,
            demonstrate_check_methods,
            demonstrate_modification_methods,
            demonstrate_split_join_methods,
            demonstrate_alignment_methods,
            demonstrate_formatting_methods,
            demonstrate_encoding_methods,
            demonstrate_advanced_methods,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_string_methods(self):
        """Test methods on empty string."""
        empty = ""
        assert empty.upper() == ""
        assert empty.lower() == ""
        assert empty.strip() == ""
        assert empty.split() == []

    def test_unicode_handling(self):
        """Test Unicode string handling."""
        unicode_str = "Hello 世界"
        assert unicode_str.upper() == "HELLO 世界"
        assert len(unicode_str) == 8


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
