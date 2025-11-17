#!/usr/bin/env python3
"""
Program 02: Variables and Data Types
Comprehensive exploration of Python's fundamental data types.

This program demonstrates:
- Variable declaration and assignment
- Basic data types (int, float, str, bool, None)
- Type checking with type() and isinstance()
- Type conversion (casting)
- Multiple assignment
- Variable naming conventions
"""

from typing import Any, Union


def demonstrate_integers() -> dict[str, Any]:
    """
    Demonstrate integer data type.

    Returns:
        Dictionary with integer examples and properties
    """
    # Integer literals
    positive_int = 42
    negative_int = -17
    zero = 0
    large_int = 1_000_000  # Underscores for readability

    # Different number systems
    binary = 0b1010  # Binary (10 in decimal)
    octal = 0o12  # Octal (10 in decimal)
    hexadecimal = 0xA  # Hexadecimal (10 in decimal)

    return {
        "positive": positive_int,
        "negative": negative_int,
        "zero": zero,
        "large": large_int,
        "binary": binary,
        "octal": octal,
        "hex": hexadecimal,
        "type": type(positive_int).__name__,
    }


def demonstrate_floats() -> dict[str, Any]:
    """
    Demonstrate floating-point data type.

    Returns:
        Dictionary with float examples and properties
    """
    # Float literals
    simple_float = 3.14
    negative_float = -2.5
    scientific_notation = 1.5e3  # 1500.0
    small_number = 1.5e-3  # 0.0015

    # Special float values
    infinity = float("inf")
    negative_infinity = float("-inf")
    not_a_number = float("nan")

    return {
        "simple": simple_float,
        "negative": negative_float,
        "scientific": scientific_notation,
        "small": small_number,
        "infinity": infinity,
        "neg_infinity": negative_infinity,
        "nan": not_a_number,
        "type": type(simple_float).__name__,
    }


def demonstrate_strings() -> dict[str, Any]:
    """
    Demonstrate string data type.

    Returns:
        Dictionary with string examples and properties
    """
    # String literals
    single_quotes = 'Hello'
    double_quotes = "World"
    triple_quotes = """Multi-line
    string example"""

    # String operations
    concatenation = single_quotes + " " + double_quotes
    repetition = "Python! " * 3

    # String formatting
    name = "Alice"
    age = 30
    f_string = f"My name is {name} and I'm {age} years old"

    # Escape characters
    escaped = "Line 1\nLine 2\tTabbed"
    raw_string = r"C:\Users\name\file.txt"

    return {
        "single_quotes": single_quotes,
        "double_quotes": double_quotes,
        "triple_quotes": triple_quotes,
        "concatenation": concatenation,
        "repetition": repetition,
        "f_string": f_string,
        "escaped": escaped,
        "raw_string": raw_string,
        "length": len(concatenation),
        "type": type(single_quotes).__name__,
    }


def demonstrate_booleans() -> dict[str, Any]:
    """
    Demonstrate boolean data type.

    Returns:
        Dictionary with boolean examples and operations
    """
    # Boolean literals
    true_value = True
    false_value = False

    # Boolean operations
    and_operation = True and False  # False
    or_operation = True or False  # True
    not_operation = not True  # False

    # Comparison operations
    equal = (5 == 5)  # True
    not_equal = (5 != 3)  # True
    greater = (10 > 5)  # True
    less_or_equal = (5 <= 5)  # True

    # Truthiness
    truthy_values = [1, "text", [1], {"key": "value"}]
    falsy_values = [0, "", [], {}, None]

    return {
        "true": true_value,
        "false": false_value,
        "and_result": and_operation,
        "or_result": or_operation,
        "not_result": not_operation,
        "comparison_equal": equal,
        "comparison_not_equal": not_equal,
        "comparison_greater": greater,
        "comparison_less_equal": less_or_equal,
        "truthy_count": len([x for x in truthy_values if x]),
        "falsy_count": len([x for x in falsy_values if not x]),
        "type": type(true_value).__name__,
    }


def demonstrate_none() -> dict[str, Any]:
    """
    Demonstrate None type (NoneType).

    Returns:
        Dictionary with None examples
    """
    # None represents absence of value
    empty_value = None

    # Common use cases
    def optional_return(return_value: bool) -> Union[str, None]:
        if return_value:
            return "Something"
        return None

    result1 = optional_return(True)
    result2 = optional_return(False)

    # None checking
    is_none = (empty_value is None)  # True
    is_not_none = (result1 is not None)  # True

    return {
        "value": empty_value,
        "result_with_value": result1,
        "result_none": result2,
        "is_none_check": is_none,
        "is_not_none_check": is_not_none,
        "type": type(empty_value).__name__,
    }


def demonstrate_type_checking(value: Any) -> dict[str, Any]:
    """
    Demonstrate type checking methods.

    Args:
        value: Any value to check type of

    Returns:
        Dictionary with type information
    """
    # Using type()
    value_type = type(value)
    type_name = type(value).__name__

    # Using isinstance()
    is_int = isinstance(value, int)
    is_str = isinstance(value, str)
    is_float = isinstance(value, float)
    is_bool = isinstance(value, bool)
    is_number = isinstance(value, (int, float))  # Check multiple types

    return {
        "value": value,
        "type": type_name,
        "type_object": value_type,
        "is_int": is_int,
        "is_str": is_str,
        "is_float": is_float,
        "is_bool": is_bool,
        "is_number": is_number,
    }


def demonstrate_type_conversion() -> dict[str, Any]:
    """
    Demonstrate type conversion (casting).

    Returns:
        Dictionary with conversion examples
    """
    # String to number
    str_to_int = int("42")
    str_to_float = float("3.14")

    # Number to string
    int_to_str = str(42)
    float_to_str = str(3.14)

    # Between number types
    int_to_float = float(42)
    float_to_int = int(3.14)  # Truncates to 3

    # To boolean
    int_to_bool = bool(1)  # True
    zero_to_bool = bool(0)  # False
    str_to_bool = bool("text")  # True
    empty_str_to_bool = bool("")  # False

    # Boolean to number
    bool_to_int = int(True)  # 1
    false_to_int = int(False)  # 0

    return {
        "str_to_int": str_to_int,
        "str_to_float": str_to_float,
        "int_to_str": int_to_str,
        "float_to_str": float_to_str,
        "int_to_float": int_to_float,
        "float_to_int": float_to_int,
        "int_to_bool": int_to_bool,
        "zero_to_bool": zero_to_bool,
        "str_to_bool": str_to_bool,
        "empty_str_to_bool": empty_str_to_bool,
        "bool_to_int": bool_to_int,
        "false_to_int": false_to_int,
    }


def demonstrate_multiple_assignment() -> dict[str, Any]:
    """
    Demonstrate multiple assignment techniques.

    Returns:
        Dictionary with assignment examples
    """
    # Multiple assignment
    x, y, z = 1, 2, 3

    # Same value to multiple variables
    a = b = c = 10

    # Swapping variables
    num1, num2 = 5, 10
    num1, num2 = num2, num1  # Swap

    # Unpacking
    coordinates = (100, 200)
    x_coord, y_coord = coordinates

    return {
        "x": x,
        "y": y,
        "z": z,
        "a_b_c": (a, b, c),
        "swapped": (num1, num2),
        "x_coord": x_coord,
        "y_coord": y_coord,
    }


def main() -> None:
    """
    Main function demonstrating all variable and data type concepts.
    """
    print("=" * 60)
    print("Program 02: Variables and Data Types")
    print("=" * 60)

    # Integers
    print("\n📊 INTEGERS")
    print("-" * 60)
    integers = demonstrate_integers()
    print(f"Positive integer: {integers['positive']}")
    print(f"Negative integer: {integers['negative']}")
    print(f"Large integer: {integers['large']:,}")
    print(f"Binary 0b1010 = {integers['binary']}")
    print(f"Hexadecimal 0xA = {integers['hex']}")
    print(f"Type: {integers['type']}")

    # Floats
    print("\n🔢 FLOATING-POINT NUMBERS")
    print("-" * 60)
    floats = demonstrate_floats()
    print(f"Simple float: {floats['simple']}")
    print(f"Scientific notation: {floats['scientific']}")
    print(f"Small number: {floats['small']}")
    print(f"Infinity: {floats['infinity']}")
    print(f"Type: {floats['type']}")

    # Strings
    print("\n📝 STRINGS")
    print("-" * 60)
    strings = demonstrate_strings()
    print(f"Concatenation: {strings['concatenation']}")
    print(f"Repetition: {strings['repetition']}")
    print(f"F-string: {strings['f_string']}")
    print(f"String length: {strings['length']}")
    print(f"Type: {strings['type']}")

    # Booleans
    print("\n✅ BOOLEANS")
    print("-" * 60)
    booleans = demonstrate_booleans()
    print(f"True AND False = {booleans['and_result']}")
    print(f"True OR False = {booleans['or_result']}")
    print(f"NOT True = {booleans['not_result']}")
    print(f"5 == 5 = {booleans['comparison_equal']}")
    print(f"Type: {booleans['type']}")

    # None
    print("\n∅ NONE TYPE")
    print("-" * 60)
    none_demo = demonstrate_none()
    print(f"None value: {none_demo['value']}")
    print(f"Function with value: {none_demo['result_with_value']}")
    print(f"Function with None: {none_demo['result_none']}")
    print(f"Type: {none_demo['type']}")

    # Type Checking
    print("\n🔍 TYPE CHECKING")
    print("-" * 60)
    check_int = demonstrate_type_checking(42)
    check_str = demonstrate_type_checking("Hello")
    print(f"Value: {check_int['value']} | Type: {check_int['type']} | Is int: {check_int['is_int']}")
    print(f"Value: {check_str['value']} | Type: {check_str['type']} | Is str: {check_str['is_str']}")

    # Type Conversion
    print("\n🔄 TYPE CONVERSION")
    print("-" * 60)
    conversions = demonstrate_type_conversion()
    print(f"String '42' to int: {conversions['str_to_int']}")
    print(f"Int 42 to string: '{conversions['int_to_str']}'")
    print(f"Float 3.14 to int: {conversions['float_to_int']}")
    print(f"Int 1 to bool: {conversions['int_to_bool']}")
    print(f"Bool True to int: {conversions['bool_to_int']}")

    # Multiple Assignment
    print("\n🔀 MULTIPLE ASSIGNMENT")
    print("-" * 60)
    assignments = demonstrate_multiple_assignment()
    print(f"x, y, z = {assignments['x']}, {assignments['y']}, {assignments['z']}")
    print(f"a = b = c = {assignments['a_b_c']}")
    print(f"Swapped values: {assignments['swapped']}")

    print("\n" + "=" * 60)
    print("✅ Program completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
