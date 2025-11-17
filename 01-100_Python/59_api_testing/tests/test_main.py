"""
Unit tests for 59_api_testing program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_test_setup,
    demonstrate_endpoint_testing,
    demonstrate_authentication_testing,
    demonstrate_mocking,
    demonstrate_integration_testing,
    demonstrate_test_coverage,
    main
)


class TestTestSetup:
    """Test cases for demonstrate_test_setup()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_test_setup()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_test_setup()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_test_setup()
        assert len(result) > 0

class TestEndpointTesting:
    """Test cases for demonstrate_endpoint_testing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_endpoint_testing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_endpoint_testing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_endpoint_testing()
        assert len(result) > 0

class TestAuthenticationTesting:
    """Test cases for demonstrate_authentication_testing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_authentication_testing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_authentication_testing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_authentication_testing()
        assert len(result) > 0

class TestMocking:
    """Test cases for demonstrate_mocking()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_mocking()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_mocking()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_mocking()
        assert len(result) > 0

class TestIntegrationTesting:
    """Test cases for demonstrate_integration_testing()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_integration_testing()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_integration_testing()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_integration_testing()
        assert len(result) > 0

class TestTestCoverage:
    """Test cases for demonstrate_test_coverage()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_test_coverage()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_test_coverage()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_test_coverage()
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
        assert "Program 59" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
