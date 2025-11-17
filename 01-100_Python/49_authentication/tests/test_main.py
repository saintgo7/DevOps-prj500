"""
Unit tests for 49_authentication program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_password_hashing,
    demonstrate_jwt_tokens,
    demonstrate_fastapi_auth,
    demonstrate_session_auth,
    demonstrate_api_key_auth,
    main
)


class TestPasswordHashing:
    """Test cases for demonstrate_password_hashing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_password_hashing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_password_hashing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_password_hashing()
        assert len(result) > 0

class TestJwtTokens:
    """Test cases for demonstrate_jwt_tokens()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_jwt_tokens()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_jwt_tokens()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_jwt_tokens()
        assert len(result) > 0

class TestFastapiAuth:
    """Test cases for demonstrate_fastapi_auth()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_fastapi_auth()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_fastapi_auth()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_fastapi_auth()
        assert len(result) > 0

class TestSessionAuth:
    """Test cases for demonstrate_session_auth()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_session_auth()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_session_auth()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_session_auth()
        assert len(result) > 0

class TestApiKeyAuth:
    """Test cases for demonstrate_api_key_auth()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_api_key_auth()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_api_key_auth()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_api_key_auth()
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
        assert "Program 49" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
