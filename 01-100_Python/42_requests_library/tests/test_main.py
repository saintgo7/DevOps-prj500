"""
Unit tests for 42_requests_library program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_get_request,
    demonstrate_post_request,
    demonstrate_other_methods,
    demonstrate_sessions,
    demonstrate_authentication,
    demonstrate_error_handling,
    demonstrate_response_handling,
    demonstrate_advanced_features,
    main
)


class TestGetRequest:
    """Test cases for demonstrate_get_request()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_get_request()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_get_request()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_get_request()
        assert len(result) > 0

class TestPostRequest:
    """Test cases for demonstrate_post_request()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_post_request()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_post_request()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_post_request()
        assert len(result) > 0

class TestOtherMethods:
    """Test cases for demonstrate_other_methods()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_other_methods()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_other_methods()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_other_methods()
        assert len(result) > 0

class TestSessions:
    """Test cases for demonstrate_sessions()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_sessions()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_sessions()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_sessions()
        assert len(result) > 0

class TestAuthentication:
    """Test cases for demonstrate_authentication()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_authentication()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_authentication()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_authentication()
        assert len(result) > 0

class TestErrorHandling:
    """Test cases for demonstrate_error_handling()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_error_handling()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_error_handling()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_error_handling()
        assert len(result) > 0

class TestResponseHandling:
    """Test cases for demonstrate_response_handling()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_response_handling()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_response_handling()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_response_handling()
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
        assert "Program 42" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
