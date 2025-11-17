"""
Unit tests for 50_authorization program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_rbac_basics,
    demonstrate_fastapi_rbac,
    demonstrate_resource_authorization,
    demonstrate_policy_authorization,
    demonstrate_scope_authorization,
    demonstrate_decorators,
    main
)


class TestRbacBasics:
    """Test cases for demonstrate_rbac_basics()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_rbac_basics()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_rbac_basics()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_rbac_basics()
        assert len(result) > 0

class TestFastapiRbac:
    """Test cases for demonstrate_fastapi_rbac()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_fastapi_rbac()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_fastapi_rbac()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_fastapi_rbac()
        assert len(result) > 0

class TestResourceAuthorization:
    """Test cases for demonstrate_resource_authorization()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_resource_authorization()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_resource_authorization()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_resource_authorization()
        assert len(result) > 0

class TestPolicyAuthorization:
    """Test cases for demonstrate_policy_authorization()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_policy_authorization()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_policy_authorization()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_policy_authorization()
        assert len(result) > 0

class TestScopeAuthorization:
    """Test cases for demonstrate_scope_authorization()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_scope_authorization()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_scope_authorization()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_scope_authorization()
        assert len(result) > 0

class TestDecorators:
    """Test cases for demonstrate_decorators()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_decorators()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_decorators()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_decorators()
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
        assert "Program 50" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
