#!/usr/bin/env python3
"""Program 38: Mocking - Master unittest.mock for test isolation."""

from unittest.mock import Mock, MagicMock, patch, call, PropertyMock, create_autospec
from typing import Any, List
import io


def demonstrate_basic_mock() -> dict[str, Any]:
    """Demonstrate basic Mock object."""

    # Create mock
    mock = Mock()

    # Configure return value
    mock.return_value = 42
    result1 = mock()

    # Configure method
    mock.get_data.return_value = {"id": 1, "name": "Alice"}
    result2 = mock.get_data()

    # Check calls
    mock.process("test", debug=True)

    return {
        "return_value": result1,
        "method_result": result2,
        "called": mock.process.called,
        "call_count": mock.process.call_count,
        "note": "Mock objects track calls and can return configured values",
    }


def demonstrate_magic_mock() -> dict[str, Any]:
    """Demonstrate MagicMock with magic methods."""

    # MagicMock supports magic methods
    magic_mock = MagicMock()

    # Configure magic methods
    magic_mock.__len__.return_value = 5
    magic_mock.__getitem__.return_value = "item"
    magic_mock.__iter__.return_value = iter([1, 2, 3])

    # Use magic methods
    length = len(magic_mock)
    item = magic_mock[0]
    items = list(magic_mock)

    return {
        "length": length,
        "item": item,
        "items": items,
        "note": "MagicMock provides default implementations of magic methods",
    }


def demonstrate_return_value_side_effect() -> dict[str, Any]:
    """Demonstrate return_value vs side_effect."""

    # return_value - static return
    mock1 = Mock()
    mock1.return_value = "always this"
    results1 = [mock1(), mock1(), mock1()]

    # side_effect - dynamic behavior
    mock2 = Mock()
    mock2.side_effect = [1, 2, 3]
    results2 = [mock2(), mock2(), mock2()]

    # side_effect with function
    mock3 = Mock()
    mock3.side_effect = lambda x: x * 2
    results3 = [mock3(5), mock3(10)]

    # side_effect with exception
    mock4 = Mock()
    mock4.side_effect = ValueError("Error!")
    error_raised = False
    try:
        mock4()
    except ValueError:
        error_raised = True

    return {
        "return_value": results1,
        "side_effect_list": results2,
        "side_effect_func": results3,
        "exception_raised": error_raised,
        "note": "side_effect provides dynamic behavior, return_value is static",
    }


def demonstrate_assert_methods() -> dict[str, Any]:
    """Demonstrate assertion methods."""

    mock = Mock()

    # Make some calls
    mock("arg1", "arg2", key="value")
    mock.method(42)
    mock.method(42)

    # Assertions
    assertions = {}

    # assert_called
    assertions["called"] = mock.called

    # assert_called_once
    assertions["method_called_twice"] = mock.method.call_count == 2

    # Check specific call
    mock.assert_called_with("arg1", "arg2", key="value")
    assertions["correct_args"] = True

    # Check method calls
    mock.method.assert_called_with(42)
    assertions["method_correct_args"] = True

    return {
        **assertions,
        "note": "Assert methods verify mock was called correctly",
    }


def demonstrate_call_tracking() -> dict[str, Any]:
    """Demonstrate call tracking."""

    mock = Mock()

    # Make various calls
    mock.foo(1, 2)
    mock.bar(x=3)
    mock.foo(4, 5)

    # Access call information
    call_list = mock.method_calls
    call_count = mock.call_count

    # Get specific calls
    foo_calls = [c for c in mock.method_calls if c[0] == 'foo']

    # call objects
    expected_calls = [call.foo(1, 2), call.bar(x=3), call.foo(4, 5)]

    return {
        "total_calls": call_count,
        "foo_call_count": len(foo_calls),
        "method_calls": str(call_list[:2]),
        "note": "Mocks track all calls with arguments",
    }


def demonstrate_patch_decorator() -> dict[str, Any]:
    """Demonstrate @patch decorator."""

    # Original module (simulated)
    class ExternalAPI:
        def get_data(self):
            return "real data"

    # Code using external API
    def fetch_user_data():
        api = ExternalAPI()
        return api.get_data()

    # Test with patch (conceptual)
    patch_example = """
@patch('module.ExternalAPI')
def test_fetch_data(mock_api):
    mock_api.return_value.get_data.return_value = 'mocked data'
    result = fetch_user_data()
    assert result == 'mocked data'
"""

    # Demonstrate patching with context manager
    with patch.object(ExternalAPI, 'get_data', return_value='mocked'):
        result = ExternalAPI().get_data()

    return {
        "patched_result": result,
        "decorator_syntax": "@patch('module.ClassName')",
        "context_manager": "with patch(...) as mock:",
        "note": "patch replaces objects during test execution",
    }


def demonstrate_patch_multiple() -> dict[str, Any]:
    """Demonstrate patching multiple objects."""

    patch_multiple_example = """
@patch('module.function1')
@patch('module.function2')
@patch('module.function3')
def test_multiple(mock3, mock2, mock1):
    # Note: mocks are in reverse order
    mock1.return_value = 'one'
    mock2.return_value = 'two'
    mock3.return_value = 'three'

# Or use patch.multiple
@patch.multiple('module',
                function1=DEFAULT,
                function2=DEFAULT,
                function3=DEFAULT)
def test_multiple2(function1, function2, function3):
    function1.return_value = 'one'
    function2.return_value = 'two'
    function3.return_value = 'three'
"""

    techniques = [
        "Stack @patch decorators",
        "Use patch.multiple()",
        "Combine with patch.dict()",
        "Use patch.object()",
    ]

    return {
        "techniques": techniques,
        "note": "Multiple patches can be applied in various ways",
    }


def demonstrate_spec_autospec() -> dict[str, Any]:
    """Demonstrate spec and autospec."""

    class RealClass:
        def real_method(self, x: int) -> int:
            return x * 2

        def another_method(self) -> str:
            return "real"

    # Mock without spec - allows any attribute
    mock_no_spec = Mock()
    mock_no_spec.fake_method()  # No error

    # Mock with spec - only allows real attributes
    mock_with_spec = Mock(spec=RealClass)

    # Can call real methods
    mock_with_spec.real_method.return_value = 10

    # Would raise AttributeError
    try:
        mock_with_spec.fake_method()
        has_fake = True
    except AttributeError:
        has_fake = False

    # autospec - automatic spec from object
    auto_mock = create_autospec(RealClass)
    auto_mock.real_method.return_value = 20

    return {
        "no_spec_allows_fake": True,
        "spec_prevents_fake": not has_fake,
        "note": "spec/autospec prevent misspelled method names",
    }


def demonstrate_property_mock() -> dict[str, Any]:
    """Demonstrate mocking properties."""

    class User:
        @property
        def full_name(self):
            return "John Doe"

    # Mock property
    mock_user = Mock(spec=User)
    type(mock_user).full_name = PropertyMock(return_value="Alice Smith")

    result = mock_user.full_name

    # Mock property with setter
    property_example = """
class Config:
    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

# Mock both getter and setter
mock_config = Mock(spec=Config)
type(mock_config).debug = PropertyMock(return_value=True)
"""

    return {
        "mocked_property": result,
        "note": "PropertyMock mocks properties with getters/setters",
    }


def demonstrate_practical_mocking() -> dict[str, Any]:
    """Demonstrate practical mocking scenarios."""

    # Mock database
    db_mock = Mock()
    db_mock.query.return_value = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]

    # Mock HTTP client
    http_mock = Mock()
    http_mock.get.return_value = Mock(
        status_code=200,
        json=Mock(return_value={"status": "success"})
    )

    # Mock file operations
    file_mock = MagicMock(spec=io.IOBase)
    file_mock.read.return_value = "file content"
    file_mock.__enter__.return_value = file_mock

    # Mock time-dependent code
    time_mock = Mock()
    time_mock.return_value = 1234567890.0

    scenarios = [
        "Database queries",
        "HTTP requests",
        "File I/O",
        "Time-dependent code",
        "External APIs",
        "System calls",
    ]

    return {
        "db_results": len(db_mock.query.return_value),
        "http_status": http_mock.get.return_value.status_code,
        "file_content": file_mock.read.return_value,
        "common_scenarios": scenarios,
        "note": "Mocking isolates code from external dependencies",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 38: Mocking")
    print("=" * 60)

    print("\n1. Basic Mock:")
    basic = demonstrate_basic_mock()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. MagicMock:")
    magic = demonstrate_magic_mock()
    for key, value in magic.items():
        print(f"   {key}: {value}")

    print("\n3. Return Value vs Side Effect:")
    side_effect = demonstrate_return_value_side_effect()
    for key, value in side_effect.items():
        print(f"   {key}: {value}")

    print("\n4. Assert Methods:")
    asserts = demonstrate_assert_methods()
    for key, value in asserts.items():
        print(f"   {key}: {value}")

    print("\n5. Call Tracking:")
    tracking = demonstrate_call_tracking()
    for key, value in tracking.items():
        print(f"   {key}: {value}")

    print("\n6. Patch Decorator:")
    patch_demo = demonstrate_patch_decorator()
    for key, value in patch_demo.items():
        print(f"   {key}: {value}")

    print("\n7. Patch Multiple:")
    multiple = demonstrate_patch_multiple()
    for key, value in multiple.items():
        print(f"   {key}: {value}")

    print("\n8. Spec and Autospec:")
    spec = demonstrate_spec_autospec()
    for key, value in spec.items():
        print(f"   {key}: {value}")

    print("\n9. Property Mock:")
    property_mock = demonstrate_property_mock()
    for key, value in property_mock.items():
        print(f"   {key}: {value}")

    print("\n10. Practical Mocking:")
    practical = demonstrate_practical_mocking()
    for key, value in practical.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
