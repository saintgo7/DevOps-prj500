"""
Unit tests for 58_websockets program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_websocket_basics,
    demonstrate_fastapi_websocket,
    demonstrate_connection_manager,
    demonstrate_chat_application,
    demonstrate_error_handling,
    main
)


class TestWebsocketBasics:
    """Test cases for demonstrate_websocket_basics()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_websocket_basics()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_websocket_basics()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_websocket_basics()
        assert len(result) > 0

class TestFastapiWebsocket:
    """Test cases for demonstrate_fastapi_websocket()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_fastapi_websocket()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_fastapi_websocket()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_fastapi_websocket()
        assert len(result) > 0

class TestConnectionManager:
    """Test cases for demonstrate_connection_manager()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_connection_manager()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_connection_manager()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_connection_manager()
        assert len(result) > 0

class TestChatApplication:
    """Test cases for demonstrate_chat_application()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_chat_application()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_chat_application()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_chat_application()
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
        assert "Program 58" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
