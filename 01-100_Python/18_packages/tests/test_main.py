"""
Unit tests for 18_packages program.

These tests verify:
- Package concepts
- __init__.py usage
- Relative imports
- Package structure
- Namespace packages
- Package discovery
- __main__ module
- Package metadata
- Virtual environments
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import (
    demonstrate_package_concept,
    demonstrate_init_file,
    demonstrate_relative_imports,
    demonstrate_package_structure,
    demonstrate_namespace_packages,
    demonstrate_package_discovery,
    demonstrate_main_module,
    demonstrate_package_metadata,
    demonstrate_virtual_environments,
    main,
)


class TestPackageConcept:
    """Test cases for demonstrate_package_concept()."""

    def test_concepts_returned(self):
        """Test package concepts."""
        result = demonstrate_package_concept()
        concepts = result["concepts"]
        assert "package" in concepts
        assert "module" in concepts


class TestInitFile:
    """Test cases for demonstrate_init_file()."""

    def test_purposes_returned(self):
        """Test __init__.py purposes."""
        result = demonstrate_init_file()
        purposes = result["purposes"]
        assert "marker" in purposes
        assert "initialization" in purposes


class TestRelativeImports:
    """Test cases for demonstrate_relative_imports()."""

    def test_import_examples(self):
        """Test import examples."""
        result = demonstrate_relative_imports()
        examples = result["import_examples"]
        assert "absolute_import" in examples
        assert "relative_current" in examples


class TestPackageStructure:
    """Test cases for demonstrate_package_structure()."""

    def test_small_structure(self):
        """Test small project structure."""
        result = demonstrate_package_structure()
        assert "setup.py" in result["small_project"]

    def test_medium_structure(self):
        """Test medium project structure."""
        result = demonstrate_package_structure()
        assert "requirements.txt" in result["medium_project"]


class TestNamespacePackages:
    """Test cases for demonstrate_namespace_packages()."""

    def test_namespace_concept(self):
        """Test namespace package concept."""
        result = demonstrate_namespace_packages()
        concept = result["concept"]
        assert "definition" in concept


class TestPackageDiscovery:
    """Test cases for demonstrate_package_discovery()."""

    def test_search_paths(self):
        """Test search paths."""
        result = demonstrate_package_discovery()
        assert result["search_paths_count"] > 0

    def test_json_package(self):
        """Test json package discovery."""
        result = demonstrate_package_discovery()
        assert len(result["json_public_items"]) > 0


class TestMainModule:
    """Test cases for demonstrate_main_module()."""

    def test_usage_patterns(self):
        """Test usage patterns."""
        result = demonstrate_main_module()
        usage = result["usage_patterns"]
        assert "with_main" in usage


class TestPackageMetadata:
    """Test cases for demonstrate_package_metadata()."""

    def test_setup_py(self):
        """Test setup.py content."""
        result = demonstrate_package_metadata()
        assert "setup" in result["setup_py"]

    def test_pyproject_toml(self):
        """Test pyproject.toml content."""
        result = demonstrate_package_metadata()
        assert "build-system" in result["pyproject_toml"]


class TestVirtualEnvironments:
    """Test cases for demonstrate_virtual_environments()."""

    def test_commands(self):
        """Test virtual environment commands."""
        result = demonstrate_virtual_environments()
        commands = result["commands"]
        assert "create_venv" in commands

    def test_benefits(self):
        """Test virtual environment benefits."""
        result = demonstrate_virtual_environments()
        benefits = result["benefits"]
        assert "isolation" in benefits


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

        assert "Program 18: Packages" in captured.out


class TestIntegration:
    """Integration tests for packages."""

    def test_all_functions_return_dicts(self):
        """Test that all demonstration functions return dictionaries."""
        functions = [
            demonstrate_package_concept,
            demonstrate_init_file,
            demonstrate_relative_imports,
            demonstrate_package_structure,
            demonstrate_namespace_packages,
            demonstrate_package_discovery,
            demonstrate_main_module,
            demonstrate_package_metadata,
            demonstrate_virtual_environments,
        ]

        for func in functions:
            result = func()
            assert isinstance(result, dict), f"{func.__name__} should return dict"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
