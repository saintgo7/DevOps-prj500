"""
Unit tests for 082_path_operations program.

These tests verify:
- Path creation and manipulation
- Path properties and attributes
- Path resolution and normalization
- File finding with glob patterns
- Path comparison and traversal
"""

import sys
from pathlib import Path, PurePath
import tempfile
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import find_files_by_pattern, main


class TestPathCreation:
    """Test cases for path creation."""

    def test_create_path_from_string(self):
        """Test creating path from string."""
        p = Path('/home/user/documents')
        assert isinstance(p, Path)

    def test_create_path_from_parts(self):
        """Test creating path from parts."""
        p = Path('home', 'user', 'documents')
        assert p.parts == ('home', 'user', 'documents')

    def test_join_paths(self):
        """Test joining paths."""
        base = Path('/home/user')
        full = base / 'documents' / 'file.txt'
        assert str(full) == '/home/user/documents/file.txt'


class TestPathProperties:
    """Test cases for path properties."""

    def test_path_name(self):
        """Test getting file name."""
        p = Path('/home/user/documents/file.txt')
        assert p.name == 'file.txt'

    def test_path_stem(self):
        """Test getting file stem."""
        p = Path('/home/user/documents/file.txt')
        assert p.stem == 'file'

    def test_path_suffix(self):
        """Test getting file suffix."""
        p = Path('/home/user/documents/file.txt')
        assert p.suffix == '.txt'

    def test_path_suffixes(self):
        """Test getting all suffixes."""
        p = Path('/home/user/file.tar.gz')
        assert p.suffixes == ['.tar', '.gz']

    def test_path_parent(self):
        """Test getting parent directory."""
        p = Path('/home/user/documents/file.txt')
        assert p.parent == Path('/home/user/documents')

    def test_path_parents(self):
        """Test getting all parents."""
        p = Path('/home/user/documents/file.txt')
        parents = list(p.parents)
        assert len(parents) > 0

    def test_path_parts(self):
        """Test getting path parts."""
        p = Path('/home/user/documents')
        assert 'home' in p.parts
        assert 'user' in p.parts


class TestPathManipulation:
    """Test cases for path manipulation."""

    def test_with_name(self):
        """Test changing file name."""
        p = Path('/home/user/file.txt')
        new_p = p.with_name('newfile.txt')
        assert new_p.name == 'newfile.txt'

    def test_with_suffix(self):
        """Test changing file suffix."""
        p = Path('/home/user/file.txt')
        new_p = p.with_suffix('.md')
        assert new_p.suffix == '.md'

    def test_with_stem(self):
        """Test changing file stem."""
        p = Path('/home/user/file.txt')
        new_p = p.with_stem('newfile')
        assert new_p.stem == 'newfile'
        assert new_p.suffix == '.txt'


class TestPathResolution:
    """Test cases for path resolution."""

    def test_absolute_path(self):
        """Test getting absolute path."""
        p = Path('relative/path')
        abs_p = p.absolute()
        assert abs_p.is_absolute()

    def test_is_absolute(self):
        """Test checking if path is absolute."""
        assert Path('/home/user').is_absolute()
        assert not Path('relative/path').is_absolute()

    def test_expanduser(self):
        """Test expanding user home directory."""
        p = Path('~/documents')
        expanded = p.expanduser()
        assert '~' not in str(expanded)


class TestFileinding:
    """Test cases for file finding."""

    def test_find_files_by_pattern(self):
        """Test finding files with pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / 'file1.txt').write_text('Text')
            (base_dir / 'file2.txt').write_text('Text')
            (base_dir / 'file3.py').write_text('Python')

            txt_files = find_files_by_pattern(base_dir, '*.txt')
            assert len(txt_files) == 2

    def test_glob_pattern(self):
        """Test glob pattern matching."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / 'test1.txt').write_text('Text')
            (base_dir / 'test2.txt').write_text('Text')

            files = list(base_dir.glob('*.txt'))
            assert len(files) == 2

    def test_rglob_recursive(self):
        """Test recursive glob."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / 'file.txt').write_text('Text')
            (base_dir / 'subdir').mkdir()
            (base_dir / 'subdir' / 'nested.txt').write_text('Text')

            files = list(base_dir.rglob('*.txt'))
            assert len(files) == 2


class TestPathComparison:
    """Test cases for path comparison."""

    def test_path_equality(self):
        """Test path equality."""
        p1 = Path('/home/user/documents')
        p2 = Path('/home/user/documents')
        assert p1 == p2

    def test_path_inequality(self):
        """Test path inequality."""
        p1 = Path('/home/user/documents')
        p2 = Path('/home/user/downloads')
        assert p1 != p2


class TestPathTraversal:
    """Test cases for path traversal."""

    def test_iterdir(self):
        """Test iterating directory contents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / 'file1.txt').write_text('Text')
            (base_dir / 'file2.txt').write_text('Text')

            items = list(base_dir.iterdir())
            assert len(items) == 2

    def test_walk_up_tree(self):
        """Test walking up directory tree."""
        p = Path('/home/user/documents/file.txt')
        parents = [str(parent.name) for parent in p.parents]
        assert 'documents' in parents


class TestPurePaths:
    """Test cases for pure paths."""

    def test_pure_path_creation(self):
        """Test creating pure path."""
        p = PurePath('/home/user/file.txt')
        assert isinstance(p, PurePath)

    def test_pure_path_properties(self):
        """Test pure path properties."""
        p = PurePath('/home/user/file.txt')
        assert p.name == 'file.txt'
        assert p.suffix == '.txt'


class TestMainFunction:
    """Test cases for main function."""

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

        assert "PATH OPERATIONS" in captured.out
        assert "PATH CREATION" in captured.out


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
