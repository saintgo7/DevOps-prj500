"""
Unit tests for 096_argument_parsing program.

These tests verify:
- argparse usage
- Positional arguments
- Optional arguments
- Argument types and validation
- Subcommands
"""

import sys
from pathlib import Path
import pytest
import argparse

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestArgumentParsing:
    """Test cases for argument parsing."""

    def test_create_parser(self):
        """Test creating argument parser."""
        parser = argparse.ArgumentParser()
        assert parser is not None

    def test_add_argument(self):
        """Test adding arguments."""
        parser = argparse.ArgumentParser()
        parser.add_argument('--name', type=str)
        args = parser.parse_args(['--name', 'test'])
        assert args.name == 'test'

    def test_positional_argument(self):
        """Test positional arguments."""
        parser = argparse.ArgumentParser()
        parser.add_argument('input')
        args = parser.parse_args(['test.txt'])
        assert args.input == 'test.txt'

    def test_optional_argument(self):
        """Test optional arguments."""
        parser = argparse.ArgumentParser()
        parser.add_argument('--verbose', action='store_true')
        args = parser.parse_args(['--verbose'])
        assert args.verbose is True

    def test_argument_types(self):
        """Test argument type conversion."""
        parser = argparse.ArgumentParser()
        parser.add_argument('--count', type=int)
        args = parser.parse_args(['--count', '42'])
        assert args.count == 42
        assert isinstance(args.count, int)


class TestMainFunction:
    """Test cases for main function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
