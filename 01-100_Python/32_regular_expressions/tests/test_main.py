"""
Unit tests for 32_regular_expressions program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_basic_patterns,
    demonstrate_match_vs_search,
    demonstrate_findall_finditer,
    demonstrate_groups,
    demonstrate_substitution,
    demonstrate_split,
    demonstrate_flags,
    demonstrate_lookahead_lookbehind,
    demonstrate_greedy_vs_lazy,
    demonstrate_practical_examples,
    main
)


class TestBasicPatterns:
    """Test cases for demonstrate_basic_patterns()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_basic_patterns()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_basic_patterns()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_basic_patterns()
        assert len(result) > 0

class TestMatchVsSearch:
    """Test cases for demonstrate_match_vs_search()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_match_vs_search()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_match_vs_search()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_match_vs_search()
        assert len(result) > 0

class TestFindallFinditer:
    """Test cases for demonstrate_findall_finditer()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_findall_finditer()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_findall_finditer()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_findall_finditer()
        assert len(result) > 0

class TestGroups:
    """Test cases for demonstrate_groups()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_groups()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_groups()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_groups()
        assert len(result) > 0

class TestSubstitution:
    """Test cases for demonstrate_substitution()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_substitution()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_substitution()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_substitution()
        assert len(result) > 0

class TestSplit:
    """Test cases for demonstrate_split()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_split()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_split()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_split()
        assert len(result) > 0

class TestFlags:
    """Test cases for demonstrate_flags()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_flags()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_flags()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_flags()
        assert len(result) > 0

class TestLookaheadLookbehind:
    """Test cases for demonstrate_lookahead_lookbehind()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_lookahead_lookbehind()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_lookahead_lookbehind()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_lookahead_lookbehind()
        assert len(result) > 0

class TestGreedyVsLazy:
    """Test cases for demonstrate_greedy_vs_lazy()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_greedy_vs_lazy()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_greedy_vs_lazy()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_greedy_vs_lazy()
        assert len(result) > 0

class TestPracticalExamples:
    """Test cases for demonstrate_practical_examples()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_practical_examples()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_practical_examples()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_practical_examples()
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
        assert "Program 32" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
