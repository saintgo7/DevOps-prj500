"""
Unit tests for 40_solid_principles program.

These tests verify all demonstration functions in the program.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_single_responsibility,
    demonstrate_open_closed,
    demonstrate_liskov_substitution,
    demonstrate_interface_segregation,
    demonstrate_dependency_inversion,
    demonstrate_srp_violation,
    demonstrate_ocp_extension,
    demonstrate_lsp_violation,
    demonstrate_isp_benefits,
    demonstrate_all_principles,
    main
)


class TestSingleResponsibility:
    """Test cases for demonstrate_single_responsibility()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_single_responsibility()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_single_responsibility()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_single_responsibility()
        assert len(result) > 0

class TestOpenClosed:
    """Test cases for demonstrate_open_closed()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_open_closed()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_open_closed()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_open_closed()
        assert len(result) > 0

class TestLiskovSubstitution:
    """Test cases for demonstrate_liskov_substitution()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_liskov_substitution()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_liskov_substitution()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_liskov_substitution()
        assert len(result) > 0

class TestInterfaceSegregation:
    """Test cases for demonstrate_interface_segregation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_interface_segregation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_interface_segregation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_interface_segregation()
        assert len(result) > 0

class TestDependencyInversion:
    """Test cases for demonstrate_dependency_inversion()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_dependency_inversion()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_dependency_inversion()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_dependency_inversion()
        assert len(result) > 0

class TestSrpViolation:
    """Test cases for demonstrate_srp_violation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_srp_violation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_srp_violation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_srp_violation()
        assert len(result) > 0

class TestOcpExtension:
    """Test cases for demonstrate_ocp_extension()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_ocp_extension()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_ocp_extension()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_ocp_extension()
        assert len(result) > 0

class TestLspViolation:
    """Test cases for demonstrate_lsp_violation()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_lsp_violation()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_lsp_violation()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_lsp_violation()
        assert len(result) > 0

class TestIspBenefits:
    """Test cases for demonstrate_isp_benefits()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_isp_benefits()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_isp_benefits()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_isp_benefits()
        assert len(result) > 0

class TestAllPrinciples:
    """Test cases for demonstrate_all_principles()."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = demonstrate_all_principles()
        assert isinstance(result, dict)

    def test_has_note(self):
        """Test that result includes explanatory note."""
        result = demonstrate_all_principles()
        assert "note" in result

    def test_result_not_empty(self):
        """Test that result is not empty."""
        result = demonstrate_all_principles()
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
        assert "Program 40" in captured.out

    def test_main_completion_message(self, capsys):
        """Test that main() prints completion message."""
        main()
        captured = capsys.readouterr()
        assert "completed" in captured.out.lower()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
