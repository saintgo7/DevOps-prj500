#!/usr/bin/env python3
"""
Program 04: Conditional Statements
Comprehensive exploration of Python's conditional statements.

This program demonstrates:
- Basic if statements
- if-else statements
- if-elif-else chains
- Nested conditions
- Ternary operator (conditional expression)
- Match-case statements (Python 3.10+)
- Truthy and falsy values in conditions
- Guard clauses and early returns
- Common conditional patterns
"""

from typing import Any, Optional
import sys


def demonstrate_basic_if() -> dict[str, Any]:
    """
    Demonstrate basic if statements.

    Returns:
        Dictionary with if statement examples
    """
    results = {}

    # Simple if statement
    age = 20
    if age >= 18:
        results["can_vote"] = True
    else:
        results["can_vote"] = False

    # If statement with block
    score = 85
    if score >= 60:
        results["grade_message"] = "You passed!"
        results["passed"] = True

    # Multiple if statements (independent)
    temperature = 30
    if temperature > 25:
        results["weather"] = "hot"
    if temperature > 20:
        results["comfortable"] = True
    if temperature < 10:
        results["cold"] = False  # This won't execute

    # If with logical operators
    username = "alice"
    password = "secret123"
    if username == "alice" and password == "secret123":
        results["authenticated"] = True

    return results


def demonstrate_if_else() -> dict[str, Any]:
    """
    Demonstrate if-else statements.

    Returns:
        Dictionary with if-else examples
    """
    results = {}

    # Basic if-else
    number = 7
    if number % 2 == 0:
        results["parity"] = "even"
    else:
        results["parity"] = "odd"

    # If-else with multiple conditions
    age = 16
    if age >= 18:
        results["status"] = "adult"
    else:
        results["status"] = "minor"

    # If-else with complex conditions
    has_license = True
    age_check = 18
    if age_check >= 18 and has_license:
        results["can_drive"] = True
    else:
        results["can_drive"] = False

    return results


def demonstrate_if_elif_else() -> dict[str, Any]:
    """
    Demonstrate if-elif-else chains.

    Returns:
        Dictionary with if-elif-else examples
    """
    results = {}

    # Grade classification
    score = 85
    if score >= 90:
        results["letter_grade"] = "A"
    elif score >= 80:
        results["letter_grade"] = "B"
    elif score >= 70:
        results["letter_grade"] = "C"
    elif score >= 60:
        results["letter_grade"] = "D"
    else:
        results["letter_grade"] = "F"

    # Temperature classification
    temp = 25
    if temp >= 30:
        results["temp_category"] = "hot"
    elif temp >= 20:
        results["temp_category"] = "warm"
    elif temp >= 10:
        results["temp_category"] = "cool"
    else:
        results["temp_category"] = "cold"

    # Age group classification
    age = 35
    if age < 13:
        results["age_group"] = "child"
    elif age < 20:
        results["age_group"] = "teenager"
    elif age < 65:
        results["age_group"] = "adult"
    else:
        results["age_group"] = "senior"

    return results


def demonstrate_nested_conditions() -> dict[str, Any]:
    """
    Demonstrate nested conditional statements.

    Returns:
        Dictionary with nested condition examples
    """
    results = {}

    # Nested if statements
    age = 25
    has_license = True
    has_car = True

    if age >= 18:
        if has_license:
            if has_car:
                results["can_drive_own_car"] = True
            else:
                results["can_drive_own_car"] = False
                results["can_rent_car"] = True
        else:
            results["needs_license"] = True
    else:
        results["too_young"] = True

    # Nested if-else
    score = 85
    attendance = 90

    if score >= 60:
        if attendance >= 75:
            results["final_result"] = "Pass"
        else:
            results["final_result"] = "Fail (Low Attendance)"
    else:
        results["final_result"] = "Fail (Low Score)"

    # Multiple levels of nesting
    user_type = "premium"
    account_active = True
    payment_current = True

    if user_type == "premium":
        if account_active:
            if payment_current:
                results["access_level"] = "full"
            else:
                results["access_level"] = "limited"
        else:
            results["access_level"] = "suspended"
    else:
        results["access_level"] = "basic"

    return results


def demonstrate_ternary_operator() -> dict[str, Any]:
    """
    Demonstrate ternary operator (conditional expression).

    Returns:
        Dictionary with ternary operator examples
    """
    results = {}

    # Basic ternary operator
    age = 20
    results["status"] = "adult" if age >= 18 else "minor"

    # Ternary with calculations
    number = 7
    results["parity"] = "even" if number % 2 == 0 else "odd"

    # Nested ternary (not recommended, but shown for completeness)
    score = 85
    results["grade"] = "A" if score >= 90 else "B" if score >= 80 else "C"

    # Ternary in expressions
    x, y = 10, 5
    results["max_value"] = x if x > y else y
    results["min_value"] = x if x < y else y

    # Ternary with function calls
    def expensive_operation():
        return "expensive result"

    def cheap_operation():
        return "cheap result"

    use_expensive = False
    results["operation_result"] = expensive_operation() if use_expensive else cheap_operation()

    return results


def demonstrate_match_case() -> dict[str, Any]:
    """
    Demonstrate match-case statements (Python 3.10+).

    Returns:
        Dictionary with match-case examples
    """
    results = {}

    # Check Python version
    if sys.version_info < (3, 10):
        results["match_case_supported"] = False
        results["message"] = "Match-case requires Python 3.10+"
        return results

    results["match_case_supported"] = True

    # Simple match-case
    day = "Monday"
    match day:
        case "Monday":
            results["day_type"] = "Start of week"
        case "Friday":
            results["day_type"] = "End of work week"
        case "Saturday" | "Sunday":
            results["day_type"] = "Weekend"
        case _:
            results["day_type"] = "Weekday"

    # Match with values
    http_status = 200
    match http_status:
        case 200:
            results["http_message"] = "OK"
        case 404:
            results["http_message"] = "Not Found"
        case 500:
            results["http_message"] = "Server Error"
        case _:
            results["http_message"] = "Other Status"

    # Match with patterns
    point = (0, 0)
    match point:
        case (0, 0):
            results["point_location"] = "Origin"
        case (0, y):
            results["point_location"] = f"Y-axis at {y}"
        case (x, 0):
            results["point_location"] = f"X-axis at {x}"
        case (x, y):
            results["point_location"] = f"Point at ({x}, {y})"

    return results


def demonstrate_truthy_falsy() -> dict[str, Any]:
    """
    Demonstrate truthy and falsy values in conditions.

    Returns:
        Dictionary with truthy/falsy examples
    """
    results = {}

    # Falsy values
    falsy_values = [False, None, 0, 0.0, "", [], {}, ()]
    results["falsy_count"] = sum(1 for val in falsy_values if not val)

    # Truthy values
    truthy_values = [True, 1, "text", [1], {"key": "value"}, (1,)]
    results["truthy_count"] = sum(1 for val in truthy_values if val)

    # Using truthy/falsy in conditions
    name = "Alice"
    if name:  # Truthy check
        results["has_name"] = True

    empty_list = []
    if not empty_list:  # Falsy check
        results["list_is_empty"] = True

    # Default values using or
    user_input = ""
    results["username"] = user_input or "Guest"

    # Existence check
    optional_value = None
    if optional_value is not None:
        results["has_value"] = True
    else:
        results["has_value"] = False

    return results


def demonstrate_guard_clauses(value: Optional[int]) -> dict[str, Any]:
    """
    Demonstrate guard clauses and early returns.

    Args:
        value: Optional integer value to process

    Returns:
        Dictionary with processing results
    """
    # Guard clause: check for None
    if value is None:
        return {"error": "Value is None", "processed": False}

    # Guard clause: check for negative
    if value < 0:
        return {"error": "Value is negative", "processed": False}

    # Guard clause: check for too large
    if value > 100:
        return {"error": "Value too large", "processed": False}

    # Main logic (only reached if all guards pass)
    return {
        "value": value,
        "squared": value ** 2,
        "processed": True
    }


def demonstrate_common_patterns() -> dict[str, Any]:
    """
    Demonstrate common conditional patterns.

    Returns:
        Dictionary with pattern examples
    """
    results = {}

    # Pattern 1: Range checking
    age = 25
    if 18 <= age < 65:
        results["working_age"] = True

    # Pattern 2: Multiple conditions with all()
    values = [10, 20, 30, 40]
    if all(v > 0 for v in values):
        results["all_positive"] = True

    # Pattern 3: Multiple conditions with any()
    scores = [45, 55, 65, 75]
    if any(s >= 60 for s in scores):
        results["any_passing"] = True

    # Pattern 4: Value in collection
    user_role = "admin"
    if user_role in ["admin", "moderator", "superuser"]:
        results["is_privileged"] = True

    # Pattern 5: Type checking
    data = 42
    if isinstance(data, int):
        results["is_integer"] = True

    # Pattern 6: Dictionary get with default
    config = {"debug": True}
    results["log_level"] = "DEBUG" if config.get("debug") else "INFO"

    # Pattern 7: Null coalescing pattern
    first_name = None
    last_name = "Smith"
    results["display_name"] = first_name or last_name or "Unknown"

    return results


def classify_number(num: int) -> str:
    """
    Classify a number using various conditionals.

    Args:
        num: Number to classify

    Returns:
        Classification string
    """
    classifications = []

    # Check sign
    if num > 0:
        classifications.append("positive")
    elif num < 0:
        classifications.append("negative")
    else:
        classifications.append("zero")

    # Check even/odd (if not zero)
    if num != 0:
        if num % 2 == 0:
            classifications.append("even")
        else:
            classifications.append("odd")

    # Check magnitude
    abs_num = abs(num)
    if abs_num > 100:
        classifications.append("large")
    elif abs_num > 10:
        classifications.append("medium")
    elif abs_num > 0:
        classifications.append("small")

    return ", ".join(classifications)


def main() -> None:
    """
    Main function demonstrating all conditional statement types.
    """
    print("=" * 60)
    print("Program 04: Conditional Statements")
    print("=" * 60)

    # Basic if
    print("\n📍 BASIC IF STATEMENTS")
    print("-" * 60)
    basic = demonstrate_basic_if()
    print(f"Can vote (age 20): {basic.get('can_vote')}")
    print(f"Passed (score 85): {basic.get('passed')}")
    print(f"Weather (30°C): {basic.get('weather')}")
    print(f"Authenticated: {basic.get('authenticated')}")

    # If-else
    print("\n🔀 IF-ELSE STATEMENTS")
    print("-" * 60)
    if_else = demonstrate_if_else()
    print(f"Number 7 is: {if_else['parity']}")
    print(f"Age 16 status: {if_else['status']}")
    print(f"Can drive: {if_else['can_drive']}")

    # If-elif-else
    print("\n🎯 IF-ELIF-ELSE CHAINS")
    print("-" * 60)
    chains = demonstrate_if_elif_else()
    print(f"Score 85 = Grade: {chains['letter_grade']}")
    print(f"Temp 25°C = {chains['temp_category']}")
    print(f"Age 35 = {chains['age_group']}")

    # Nested conditions
    print("\n🔗 NESTED CONDITIONS")
    print("-" * 60)
    nested = demonstrate_nested_conditions()
    print(f"Can drive own car: {nested.get('can_drive_own_car', False)}")
    print(f"Final result: {nested.get('final_result')}")
    print(f"Access level: {nested.get('access_level')}")

    # Ternary operator
    print("\n⚡ TERNARY OPERATOR")
    print("-" * 60)
    ternary = demonstrate_ternary_operator()
    print(f"Age 20 status: {ternary['status']}")
    print(f"Number 7 parity: {ternary['parity']}")
    print(f"Score 85 grade: {ternary['grade']}")
    print(f"Max of 10, 5: {ternary['max_value']}")

    # Match-case
    print("\n🎨 MATCH-CASE (Python 3.10+)")
    print("-" * 60)
    match_case = demonstrate_match_case()
    if match_case.get('match_case_supported'):
        print(f"Monday: {match_case.get('day_type')}")
        print(f"HTTP 200: {match_case.get('http_message')}")
        print(f"Point (0,0): {match_case.get('point_location')}")
    else:
        print(f"{match_case.get('message')}")

    # Truthy/Falsy
    print("\n✓ TRUTHY AND FALSY VALUES")
    print("-" * 60)
    truthy_falsy = demonstrate_truthy_falsy()
    print(f"Falsy values count: {truthy_falsy['falsy_count']}")
    print(f"Truthy values count: {truthy_falsy['truthy_count']}")
    print(f"Username (empty input): {truthy_falsy['username']}")
    print(f"Has optional value: {truthy_falsy['has_value']}")

    # Guard clauses
    print("\n🛡️  GUARD CLAUSES")
    print("-" * 60)
    guard1 = demonstrate_guard_clauses(None)
    guard2 = demonstrate_guard_clauses(-5)
    guard3 = demonstrate_guard_clauses(50)
    print(f"Process None: {guard1.get('error', 'Success')}")
    print(f"Process -5: {guard2.get('error', 'Success')}")
    print(f"Process 50: Squared = {guard3.get('squared')}")

    # Common patterns
    print("\n📋 COMMON PATTERNS")
    print("-" * 60)
    patterns = demonstrate_common_patterns()
    print(f"Working age (25): {patterns.get('working_age')}")
    print(f"All positive: {patterns.get('all_positive')}")
    print(f"Any passing score: {patterns.get('any_passing')}")
    print(f"Is privileged user: {patterns.get('is_privileged')}")

    # Number classification
    print("\n🔢 NUMBER CLASSIFICATION")
    print("-" * 60)
    print(f"42: {classify_number(42)}")
    print(f"-15: {classify_number(-15)}")
    print(f"0: {classify_number(0)}")
    print(f"150: {classify_number(150)}")

    print("\n" + "=" * 60)
    print("✅ Program completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
