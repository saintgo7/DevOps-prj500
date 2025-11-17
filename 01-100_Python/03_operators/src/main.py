#!/usr/bin/env python3
"""
Program 03: Operators
Comprehensive exploration of all Python operators.

This program demonstrates:
- Arithmetic operators (+, -, *, /, //, %, **)
- Comparison operators (==, !=, <, >, <=, >=)
- Logical operators (and, or, not)
- Assignment operators (=, +=, -=, *=, etc.)
- Bitwise operators (&, |, ^, ~, <<, >>)
- Membership operators (in, not in)
- Identity operators (is, is not)
- Operator precedence
"""

from typing import Any


def demonstrate_arithmetic_operators() -> dict[str, Any]:
    """
    Demonstrate arithmetic operators.

    Returns:
        Dictionary with arithmetic operation examples
    """
    a, b = 10, 3

    # Basic arithmetic
    addition = a + b  # 13
    subtraction = a - b  # 7
    multiplication = a * b  # 30
    division = a / b  # 3.333...
    floor_division = a // b  # 3 (integer division)
    modulo = a % b  # 1 (remainder)
    exponentiation = a ** b  # 1000 (10^3)

    # Unary operators
    positive = +a  # 10
    negative = -a  # -10

    # More examples
    complex_expr = 2 + 3 * 4  # 14 (multiplication first)
    with_parens = (2 + 3) * 4  # 20 (parentheses first)

    return {
        "addition": addition,
        "subtraction": subtraction,
        "multiplication": multiplication,
        "division": division,
        "floor_division": floor_division,
        "modulo": modulo,
        "exponentiation": exponentiation,
        "positive": positive,
        "negative": negative,
        "complex_expr": complex_expr,
        "with_parens": with_parens,
    }


def demonstrate_comparison_operators() -> dict[str, Any]:
    """
    Demonstrate comparison operators.

    Returns:
        Dictionary with comparison operation examples
    """
    a, b = 10, 5

    # Comparison operators
    equal = (a == b)  # False
    not_equal = (a != b)  # True
    greater_than = (a > b)  # True
    less_than = (a < b)  # False
    greater_or_equal = (a >= b)  # True
    less_or_equal = (a <= b)  # False

    # Chained comparisons
    chained = (1 < 5 < 10)  # True (equivalent to: 1 < 5 and 5 < 10)
    chained_false = (1 < 5 > 10)  # False

    # String comparisons (lexicographic)
    str_equal = ("apple" == "apple")  # True
    str_less = ("apple" < "banana")  # True (alphabetical order)

    # List comparisons (element by element)
    list_equal = ([1, 2, 3] == [1, 2, 3])  # True
    list_less = ([1, 2] < [1, 3])  # True

    return {
        "equal": equal,
        "not_equal": not_equal,
        "greater_than": greater_than,
        "less_than": less_than,
        "greater_or_equal": greater_or_equal,
        "less_or_equal": less_or_equal,
        "chained": chained,
        "chained_false": chained_false,
        "str_equal": str_equal,
        "str_less": str_less,
        "list_equal": list_equal,
        "list_less": list_less,
    }


def demonstrate_logical_operators() -> dict[str, Any]:
    """
    Demonstrate logical operators.

    Returns:
        Dictionary with logical operation examples
    """
    # Boolean values
    true_val = True
    false_val = False

    # Logical AND
    and_tt = true_val and true_val  # True
    and_tf = true_val and false_val  # False
    and_ff = false_val and false_val  # False

    # Logical OR
    or_tt = true_val or true_val  # True
    or_tf = true_val or false_val  # True
    or_ff = false_val or false_val  # False

    # Logical NOT
    not_true = not true_val  # False
    not_false = not false_val  # True

    # Short-circuit evaluation
    # 'and' returns first falsy value or last value
    short_and_1 = (5 and 10)  # 10
    short_and_2 = (0 and 10)  # 0 (stops at first falsy)

    # 'or' returns first truthy value or last value
    short_or_1 = (5 or 10)  # 5 (stops at first truthy)
    short_or_2 = (0 or 10)  # 10

    # Complex expressions
    complex_and = (5 > 3) and (10 < 20)  # True
    complex_or = (5 > 10) or (10 < 20)  # True
    complex_not = not (5 > 10)  # True

    # With non-boolean values (truthy/falsy)
    truthy_and = ("hello" and "world")  # "world"
    falsy_and = ("" and "world")  # ""
    truthy_or = ("hello" or "world")  # "hello"
    falsy_or = ("" or "world")  # "world"

    return {
        "and_tt": and_tt,
        "and_tf": and_tf,
        "and_ff": and_ff,
        "or_tt": or_tt,
        "or_tf": or_tf,
        "or_ff": or_ff,
        "not_true": not_true,
        "not_false": not_false,
        "short_and_1": short_and_1,
        "short_and_2": short_and_2,
        "short_or_1": short_or_1,
        "short_or_2": short_or_2,
        "complex_and": complex_and,
        "complex_or": complex_or,
        "complex_not": complex_not,
        "truthy_and": truthy_and,
        "falsy_and": falsy_and,
        "truthy_or": truthy_or,
        "falsy_or": falsy_or,
    }


def demonstrate_assignment_operators() -> dict[str, Any]:
    """
    Demonstrate assignment operators.

    Returns:
        Dictionary with assignment operation examples
    """
    # Simple assignment
    x = 10

    # Augmented assignment operators
    y = 5
    y += 3  # y = y + 3, result: 8

    z = 10
    z -= 4  # z = z - 4, result: 6

    a = 3
    a *= 4  # a = a * 4, result: 12

    b = 20
    b /= 4  # b = b / 4, result: 5.0

    c = 17
    c //= 5  # c = c // 5, result: 3

    d = 17
    d %= 5  # d = d % 5, result: 2

    e = 2
    e **= 3  # e = e ** 3, result: 8

    # Bitwise augmented assignment
    f = 12  # 1100 in binary
    f &= 10  # f = f & 10, result: 8 (1000)

    g = 12  # 1100 in binary
    g |= 3  # g = g | 3, result: 15 (1111)

    h = 12  # 1100 in binary
    h ^= 10  # h = h ^ 10, result: 6 (0110)

    i = 4  # 0100 in binary
    i <<= 2  # i = i << 2, result: 16 (10000)

    j = 16  # 10000 in binary
    j >>= 2  # j = j >> 2, result: 4 (0100)

    return {
        "simple": x,
        "add_assign": y,
        "sub_assign": z,
        "mul_assign": a,
        "div_assign": b,
        "floor_div_assign": c,
        "mod_assign": d,
        "exp_assign": e,
        "and_assign": f,
        "or_assign": g,
        "xor_assign": h,
        "left_shift_assign": i,
        "right_shift_assign": j,
    }


def demonstrate_bitwise_operators() -> dict[str, Any]:
    """
    Demonstrate bitwise operators.

    Returns:
        Dictionary with bitwise operation examples
    """
    a = 12  # Binary: 1100
    b = 10  # Binary: 1010

    # Bitwise AND
    bitwise_and = a & b  # 8 (1000)

    # Bitwise OR
    bitwise_or = a | b  # 14 (1110)

    # Bitwise XOR (exclusive OR)
    bitwise_xor = a ^ b  # 6 (0110)

    # Bitwise NOT (inversion)
    bitwise_not_a = ~a  # -13 (two's complement)

    # Left shift
    left_shift = a << 2  # 48 (110000)

    # Right shift
    right_shift = a >> 2  # 3 (0011)

    # Practical examples
    # Check if number is even (last bit is 0)
    is_even = (a & 1) == 0  # True if even

    # Set a specific bit
    set_bit = a | (1 << 2)  # Set bit at position 2

    # Clear a specific bit
    clear_bit = a & ~(1 << 2)  # Clear bit at position 2

    # Toggle a specific bit
    toggle_bit = a ^ (1 << 2)  # Toggle bit at position 2

    return {
        "bitwise_and": bitwise_and,
        "bitwise_or": bitwise_or,
        "bitwise_xor": bitwise_xor,
        "bitwise_not": bitwise_not_a,
        "left_shift": left_shift,
        "right_shift": right_shift,
        "is_even": is_even,
        "set_bit": set_bit,
        "clear_bit": clear_bit,
        "toggle_bit": toggle_bit,
        "binary_a": bin(a),
        "binary_b": bin(b),
    }


def demonstrate_membership_operators() -> dict[str, Any]:
    """
    Demonstrate membership operators.

    Returns:
        Dictionary with membership operation examples
    """
    # List membership
    numbers = [1, 2, 3, 4, 5]
    in_list = 3 in numbers  # True
    not_in_list = 10 not in numbers  # True

    # String membership
    text = "Python Programming"
    in_string = "Python" in text  # True
    not_in_string = "Java" not in text  # True

    # Tuple membership
    coordinates = (10, 20, 30)
    in_tuple = 20 in coordinates  # True

    # Dictionary membership (checks keys)
    person = {"name": "Alice", "age": 30}
    in_dict_keys = "name" in person  # True
    not_in_dict_keys = "email" not in person  # True

    # Set membership
    unique_numbers = {1, 2, 3, 4, 5}
    in_set = 3 in unique_numbers  # True

    # Substring search
    substring_check = "gram" in "Programming"  # True

    return {
        "in_list": in_list,
        "not_in_list": not_in_list,
        "in_string": in_string,
        "not_in_string": not_in_string,
        "in_tuple": in_tuple,
        "in_dict_keys": in_dict_keys,
        "not_in_dict_keys": not_in_dict_keys,
        "in_set": in_set,
        "substring_check": substring_check,
    }


def demonstrate_identity_operators() -> dict[str, Any]:
    """
    Demonstrate identity operators.

    Returns:
        Dictionary with identity operation examples
    """
    # Identity checks object identity (memory address), not value
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a

    # 'is' checks if two variables point to the same object
    same_object = (a is c)  # True (c points to same object as a)
    different_object = (a is b)  # False (different objects)

    # 'is not'
    not_same = (a is not b)  # True

    # Value equality vs identity
    equal_values = (a == b)  # True (same values)
    same_identity = (a is b)  # False (different objects)

    # None checks (always use 'is')
    none_value = None
    is_none = (none_value is None)  # True
    is_not_none = (none_value is not None)  # False

    # Small integers are cached (-5 to 256)
    x = 256
    y = 256
    small_int_identity = (x is y)  # True (same object in cache)

    # Large integers are not cached
    large_x = 257
    large_y = 257
    large_int_identity = (large_x is large_y)  # May be False

    # Strings may be interned
    str1 = "hello"
    str2 = "hello"
    string_identity = (str1 is str2)  # Usually True (interned)

    return {
        "same_object": same_object,
        "different_object": different_object,
        "not_same": not_same,
        "equal_values": equal_values,
        "same_identity": same_identity,
        "is_none": is_none,
        "is_not_none": is_not_none,
        "small_int_identity": small_int_identity,
        "large_int_identity": large_int_identity,
        "string_identity": string_identity,
        "id_a": id(a),
        "id_b": id(b),
        "id_c": id(c),
    }


def demonstrate_operator_precedence() -> dict[str, Any]:
    """
    Demonstrate operator precedence.

    Returns:
        Dictionary with precedence examples
    """
    # Operator precedence (highest to lowest):
    # 1. Parentheses ()
    # 2. Exponentiation **
    # 3. Unary +, -, ~
    # 4. *, /, //, %
    # 5. +, -
    # 6. <<, >>
    # 7. &
    # 8. ^
    # 9. |
    # 10. ==, !=, <, >, <=, >=, is, is not, in, not in
    # 11. not
    # 12. and
    # 13. or

    # Examples
    expr1 = 2 + 3 * 4  # 14 (* before +)
    expr2 = (2 + 3) * 4  # 20 (parentheses first)
    expr3 = 2 ** 3 ** 2  # 512 (** is right-associative: 2**(3**2))
    expr4 = 10 + 5 * 2 - 3  # 17 (*, then + and -)
    expr5 = 5 > 3 and 10 < 20  # True (comparison before and)
    expr6 = 5 + 3 > 10 or 2 * 4 == 8  # True
    expr7 = not False and True  # True (not before and)
    expr8 = 2 * 3 + 4 * 5  # 26 (* before +)

    # Bitwise precedence
    expr9 = 5 | 3 & 2  # 5 (& before |)
    expr10 = (5 | 3) & 2  # 2 (parentheses first)

    # Complex expression
    complex = 2 + 3 * 4 ** 2 / 2 - 1  # 25.0

    return {
        "expr1": expr1,
        "expr2": expr2,
        "expr3": expr3,
        "expr4": expr4,
        "expr5": expr5,
        "expr6": expr6,
        "expr7": expr7,
        "expr8": expr8,
        "expr9": expr9,
        "expr10": expr10,
        "complex": complex,
    }


def main() -> None:
    """
    Main function demonstrating all operator types.
    """
    print("=" * 60)
    print("Program 03: Operators")
    print("=" * 60)

    # Arithmetic Operators
    print("\n🔢 ARITHMETIC OPERATORS")
    print("-" * 60)
    arithmetic = demonstrate_arithmetic_operators()
    print(f"10 + 3 = {arithmetic['addition']}")
    print(f"10 - 3 = {arithmetic['subtraction']}")
    print(f"10 * 3 = {arithmetic['multiplication']}")
    print(f"10 / 3 = {arithmetic['division']:.4f}")
    print(f"10 // 3 = {arithmetic['floor_division']} (floor division)")
    print(f"10 % 3 = {arithmetic['modulo']} (remainder)")
    print(f"10 ** 3 = {arithmetic['exponentiation']} (power)")
    print(f"2 + 3 * 4 = {arithmetic['complex_expr']} (order matters)")
    print(f"(2 + 3) * 4 = {arithmetic['with_parens']} (parentheses first)")

    # Comparison Operators
    print("\n⚖️  COMPARISON OPERATORS")
    print("-" * 60)
    comparison = demonstrate_comparison_operators()
    print(f"10 == 5: {comparison['equal']}")
    print(f"10 != 5: {comparison['not_equal']}")
    print(f"10 > 5: {comparison['greater_than']}")
    print(f"10 < 5: {comparison['less_than']}")
    print(f"10 >= 5: {comparison['greater_or_equal']}")
    print(f"10 <= 5: {comparison['less_or_equal']}")
    print(f"1 < 5 < 10: {comparison['chained']} (chained comparison)")
    print(f"'apple' < 'banana': {comparison['str_less']} (lexicographic)")

    # Logical Operators
    print("\n🔀 LOGICAL OPERATORS")
    print("-" * 60)
    logical = demonstrate_logical_operators()
    print(f"True and True: {logical['and_tt']}")
    print(f"True and False: {logical['and_tf']}")
    print(f"True or False: {logical['or_tf']}")
    print(f"False or False: {logical['or_ff']}")
    print(f"not True: {logical['not_true']}")
    print(f"5 and 10: {logical['short_and_1']} (returns last if all truthy)")
    print(f"0 and 10: {logical['short_and_2']} (returns first falsy)")
    print(f"5 or 10: {logical['short_or_1']} (returns first truthy)")
    print(f"0 or 10: {logical['short_or_2']} (returns last if all falsy)")

    # Assignment Operators
    print("\n✏️  ASSIGNMENT OPERATORS")
    print("-" * 60)
    assignment = demonstrate_assignment_operators()
    print(f"x = 10: {assignment['simple']}")
    print(f"y = 5; y += 3: {assignment['add_assign']}")
    print(f"z = 10; z -= 4: {assignment['sub_assign']}")
    print(f"a = 3; a *= 4: {assignment['mul_assign']}")
    print(f"b = 20; b /= 4: {assignment['div_assign']}")
    print(f"e = 2; e **= 3: {assignment['exp_assign']}")

    # Bitwise Operators
    print("\n🔣 BITWISE OPERATORS")
    print("-" * 60)
    bitwise = demonstrate_bitwise_operators()
    print(f"12 = {bitwise['binary_a']}, 10 = {bitwise['binary_b']}")
    print(f"12 & 10 = {bitwise['bitwise_and']} (AND)")
    print(f"12 | 10 = {bitwise['bitwise_or']} (OR)")
    print(f"12 ^ 10 = {bitwise['bitwise_xor']} (XOR)")
    print(f"~12 = {bitwise['bitwise_not']} (NOT)")
    print(f"12 << 2 = {bitwise['left_shift']} (left shift)")
    print(f"12 >> 2 = {bitwise['right_shift']} (right shift)")
    print(f"12 is even: {bitwise['is_even']}")

    # Membership Operators
    print("\n📍 MEMBERSHIP OPERATORS")
    print("-" * 60)
    membership = demonstrate_membership_operators()
    print(f"3 in [1,2,3,4,5]: {membership['in_list']}")
    print(f"10 not in [1,2,3,4,5]: {membership['not_in_list']}")
    print(f"'Python' in 'Python Programming': {membership['in_string']}")
    print(f"'name' in {{'name':'Alice'}}: {membership['in_dict_keys']}")
    print(f"'gram' in 'Programming': {membership['substring_check']}")

    # Identity Operators
    print("\n🔍 IDENTITY OPERATORS")
    print("-" * 60)
    identity = demonstrate_identity_operators()
    print(f"a = [1,2,3]; c = a; (a is c): {identity['same_object']}")
    print(f"a = [1,2,3]; b = [1,2,3]; (a is b): {identity['different_object']}")
    print(f"a == b: {identity['equal_values']} (equal values)")
    print(f"a is b: {identity['same_identity']} (same object)")
    print(f"None is None: {identity['is_none']}")
    print(f"256 is 256: {identity['small_int_identity']} (cached)")

    # Operator Precedence
    print("\n📊 OPERATOR PRECEDENCE")
    print("-" * 60)
    precedence = demonstrate_operator_precedence()
    print(f"2 + 3 * 4 = {precedence['expr1']} (* before +)")
    print(f"(2 + 3) * 4 = {precedence['expr2']} (parentheses first)")
    print(f"2 ** 3 ** 2 = {precedence['expr3']} (right-associative)")
    print(f"10 + 5 * 2 - 3 = {precedence['expr4']}")
    print(f"5 > 3 and 10 < 20 = {precedence['expr5']}")
    print(f"5 | 3 & 2 = {precedence['expr9']} (& before |)")
    print(f"(5 | 3) & 2 = {precedence['expr10']} (parentheses)")

    print("\n" + "=" * 60)
    print("✅ Program completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
