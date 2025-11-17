#!/usr/bin/env python3
"""Program 37: Advanced Testing - Master pytest fixtures, parametrization, and plugins."""

import pytest
from typing import Any, List
import tempfile
import os


def demonstrate_fixtures() -> dict[str, Any]:
    """Demonstrate pytest fixtures concept."""

    # Fixture example (conceptual, as we can't run pytest here)
    fixture_example = """
@pytest.fixture
def database():
    # Setup
    db = create_database()
    yield db
    # Teardown
    db.close()

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
"""

    fixture_types = [
        "function - Run once per test",
        "class - Run once per test class",
        "module - Run once per module",
        "session - Run once per session",
    ]

    return {
        "fixture_scopes": fixture_types,
        "example_lines": len(fixture_example.split('\n')),
        "note": "Fixtures provide setup/teardown and dependency injection",
    }


def demonstrate_parametrize() -> dict[str, Any]:
    """Demonstrate parametrize for test generation."""

    # Parametrize example
    parametrize_example = """
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
])
def test_double(input, expected):
    assert input * 2 == expected
"""

    # Multiple parameters
    multi_param_example = """
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_multiply(x, y):
    assert x * y > 0
"""

    test_cases = [
        ("add", [1, 2], 3),
        ("add", [5, 5], 10),
        ("multiply", [3, 4], 12),
        ("multiply", [2, 5], 10),
    ]

    return {
        "test_case_count": len(test_cases),
        "parametrize_example_lines": len(parametrize_example.split('\n')),
        "note": "parametrize generates multiple test cases from one function",
    }


def demonstrate_marks() -> dict[str, Any]:
    """Demonstrate pytest marks."""

    marks_examples = {
        "skip": "@pytest.mark.skip(reason='Not implemented')",
        "skipif": "@pytest.mark.skipif(sys.version_info < (3, 8), reason='Requires 3.8+')",
        "xfail": "@pytest.mark.xfail(reason='Known bug')",
        "slow": "@pytest.mark.slow  # Custom mark",
        "parametrize": "@pytest.mark.parametrize(...)",
    }

    custom_marks = [
        "slow - Long running tests",
        "integration - Integration tests",
        "unit - Unit tests",
        "smoke - Smoke tests",
    ]

    return {
        "builtin_marks": list(marks_examples.keys()),
        "custom_marks": custom_marks,
        "run_specific": "pytest -m slow",
        "note": "Marks categorize and selectively run tests",
    }


def demonstrate_fixtures_scope() -> dict[str, Any]:
    """Demonstrate fixture scopes and lifecycle."""

    fixture_lifecycle = """
# Module-level fixture (runs once per module)
@pytest.fixture(scope='module')
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

# Function-level fixture (runs per test)
@pytest.fixture(scope='function')
def transaction(database):
    trans = database.begin_transaction()
    yield trans
    trans.rollback()

# Use fixtures
def test_insert(transaction):
    transaction.insert(...)
    assert transaction.count() == 1

def test_update(transaction):
    transaction.insert(...)
    transaction.update(...)
    assert transaction.count() == 1
"""

    scopes = {
        "function": "Per test function (default)",
        "class": "Per test class",
        "module": "Per test module",
        "package": "Per test package",
        "session": "Per test session (entire run)",
    }

    return {
        "available_scopes": list(scopes.keys()),
        "scope_details": scopes,
        "note": "Fixture scope controls setup/teardown frequency",
    }


def demonstrate_fixture_parameters() -> dict[str, Any]:
    """Demonstrate fixture parametrization."""

    fixture_param_example = """
@pytest.fixture(params=['mysql', 'postgresql', 'sqlite'])
def database(request):
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.close()

def test_query(database):
    # This test runs 3 times, once per database
    result = database.query("SELECT 1")
    assert result is not None
"""

    benefits = [
        "Test against multiple configurations",
        "Ensure cross-platform compatibility",
        "Verify multiple implementations",
        "Reduce test code duplication",
    ]

    return {
        "example_params": ['mysql', 'postgresql', 'sqlite'],
        "tests_generated": 3,
        "benefits": benefits,
        "note": "Fixture params multiply test execution",
    }


def demonstrate_conftest() -> dict[str, Any]:
    """Demonstrate conftest.py for shared fixtures."""

    conftest_example = """
# conftest.py - Shared fixtures for entire project

import pytest

@pytest.fixture
def sample_data():
    return {'users': [1, 2, 3], 'items': [4, 5, 6]}

@pytest.fixture
def temp_file():
    file = create_temp_file()
    yield file
    file.cleanup()

# Hooks
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow")

def pytest_collection_modifyitems(config, items):
    # Modify collected tests
    pass
"""

    conftest_features = [
        "Share fixtures across test files",
        "Define pytest hooks",
        "Configure plugins",
        "Set up test environment",
    ]

    return {
        "conftest_location": "Root of test directory",
        "features": conftest_features,
        "auto_discovered": True,
        "note": "conftest.py provides shared test configuration",
    }


def demonstrate_monkeypatch() -> dict[str, Any]:
    """Demonstrate monkeypatch fixture."""

    monkeypatch_example = """
# Original code
def get_user_input():
    return input("Enter name: ")

# Test with monkeypatch
def test_user_input(monkeypatch):
    # Mock input
    monkeypatch.setattr('builtins.input', lambda _: 'Alice')
    result = get_user_input()
    assert result == 'Alice'

# Patch environment variable
def test_env_var(monkeypatch):
    monkeypatch.setenv('API_KEY', 'test-key')
    assert os.getenv('API_KEY') == 'test-key'

# Patch attribute
def test_patch_attr(monkeypatch):
    monkeypatch.setattr('module.Class.method', lambda: 'mocked')
    result = module.Class.method()
    assert result == 'mocked'
"""

    monkeypatch_methods = [
        "setattr - Patch object attribute",
        "delattr - Delete attribute",
        "setitem - Patch dictionary item",
        "setenv - Set environment variable",
        "delenv - Delete environment variable",
        "syspath_prepend - Modify sys.path",
        "chdir - Change directory",
    ]

    return {
        "methods": monkeypatch_methods,
        "note": "monkeypatch safely modifies objects during tests",
    }


def demonstrate_tmp_path() -> dict[str, Any]:
    """Demonstrate tmp_path fixture."""

    tmp_path_example = """
def test_file_operations(tmp_path):
    # tmp_path is a Path object
    test_file = tmp_path / "test.txt"

    # Write
    test_file.write_text("Hello, World!")

    # Read
    content = test_file.read_text()
    assert content == "Hello, World!"

    # File automatically cleaned up after test

def test_directory(tmp_path):
    # Create subdirectory
    sub_dir = tmp_path / "subdir"
    sub_dir.mkdir()

    # Create file in subdirectory
    (sub_dir / "file.txt").write_text("content")

    assert (sub_dir / "file.txt").exists()
"""

    # Actually demonstrate temporary path creation
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = os.path.join(tmp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        file_created = os.path.exists(test_file)

    return {
        "file_created": file_created,
        "auto_cleanup": True,
        "note": "tmp_path provides temporary directory per test",
    }


def demonstrate_capsys() -> dict[str, Any]:
    """Demonstrate capsys for capturing output."""

    capsys_example = """
def greet(name):
    print(f"Hello, {name}!")

def test_output(capsys):
    greet("Alice")

    # Capture output
    captured = capsys.readouterr()

    assert captured.out == "Hello, Alice!\\n"
    assert captured.err == ""

def test_multiple_captures(capsys):
    print("First")
    captured1 = capsys.readouterr()

    print("Second")
    captured2 = capsys.readouterr()

    assert captured1.out == "First\\n"
    assert captured2.out == "Second\\n"
"""

    capsys_fixtures = [
        "capsys - Capture stdout/stderr (text)",
        "capsysbinary - Capture stdout/stderr (binary)",
        "capfd - Capture file descriptors",
        "caplog - Capture log records",
    ]

    return {
        "capture_fixtures": capsys_fixtures,
        "methods": ["readouterr()", "disabled()"],
        "note": "capsys captures and tests printed output",
    }


def demonstrate_testing_best_practices() -> dict[str, Any]:
    """Demonstrate testing best practices."""

    best_practices = {
        "AAA Pattern": "Arrange, Act, Assert",
        "One assertion per test": "Test one thing at a time",
        "Descriptive names": "test_user_login_with_invalid_password",
        "Fixtures for DRY": "Reuse setup code",
        "Fast tests": "Keep unit tests fast",
        "Isolated tests": "No dependencies between tests",
        "Deterministic": "Tests should not be flaky",
        "Readable": "Tests are documentation",
    }

    test_structure = """
def test_user_can_login_with_valid_credentials():
    # Arrange
    user = create_user(email='test@example.com', password='secret')
    login_form = LoginForm()

    # Act
    result = login_form.submit(email='test@example.com', password='secret')

    # Assert
    assert result.success is True
    assert result.user == user
"""

    return {
        "best_practices": best_practices,
        "pattern": "Arrange-Act-Assert",
        "note": "Good tests are fast, isolated, and descriptive",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 37: Advanced Testing")
    print("=" * 60)

    print("\n1. Fixtures:")
    fixtures = demonstrate_fixtures()
    for key, value in fixtures.items():
        print(f"   {key}: {value}")

    print("\n2. Parametrize:")
    parametrize = demonstrate_parametrize()
    for key, value in parametrize.items():
        print(f"   {key}: {value}")

    print("\n3. Marks:")
    marks = demonstrate_marks()
    for key, value in marks.items():
        print(f"   {key}: {value}")

    print("\n4. Fixture Scopes:")
    scopes = demonstrate_fixtures_scope()
    for key, value in scopes.items():
        print(f"   {key}: {value}")

    print("\n5. Fixture Parameters:")
    params = demonstrate_fixture_parameters()
    for key, value in params.items():
        print(f"   {key}: {value}")

    print("\n6. Conftest:")
    conftest = demonstrate_conftest()
    for key, value in conftest.items():
        print(f"   {key}: {value}")

    print("\n7. Monkeypatch:")
    monkeypatch = demonstrate_monkeypatch()
    for key, value in monkeypatch.items():
        print(f"   {key}: {value}")

    print("\n8. Tmp Path:")
    tmp_path = demonstrate_tmp_path()
    for key, value in tmp_path.items():
        print(f"   {key}: {value}")

    print("\n9. Capsys:")
    capsys = demonstrate_capsys()
    for key, value in capsys.items():
        print(f"   {key}: {value}")

    print("\n10. Best Practices:")
    practices = demonstrate_testing_best_practices()
    for key, value in practices.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
