#!/usr/bin/env python3
"""
Program 05: Loops
Comprehensive exploration of Python's loop constructs.

This program demonstrates:
- For loops with various iterables
- Range function and its variations
- While loops
- Loop control statements (break, continue, pass)
- Nested loops
- Loop-else clause
- Enumerate and zip functions
- List comprehensions
- Common loop patterns and idioms
"""

from typing import Any, List, Tuple


def demonstrate_basic_for_loops() -> dict[str, Any]:
    """
    Demonstrate basic for loops.

    Returns:
        Dictionary with for loop examples
    """
    results = {}

    # Loop through list
    numbers = [1, 2, 3, 4, 5]
    sum_numbers = 0
    for num in numbers:
        sum_numbers += num
    results["sum_list"] = sum_numbers

    # Loop through string
    text = "Python"
    letters = []
    for char in text:
        letters.append(char)
    results["letters"] = letters

    # Loop through tuple
    coordinates = (10, 20, 30)
    coord_sum = 0
    for coord in coordinates:
        coord_sum += coord
    results["coord_sum"] = coord_sum

    # Loop through dictionary keys
    person = {"name": "Alice", "age": 30, "city": "NYC"}
    keys = []
    for key in person:
        keys.append(key)
    results["dict_keys"] = keys

    # Loop through dictionary values
    values = []
    for value in person.values():
        values.append(value)
    results["dict_values"] = values

    # Loop through dictionary items
    items = []
    for key, value in person.items():
        items.append(f"{key}:{value}")
    results["dict_items"] = items

    return results


def demonstrate_range_function() -> dict[str, Any]:
    """
    Demonstrate range function in loops.

    Returns:
        Dictionary with range examples
    """
    results = {}

    # Range with one argument (stop)
    range_list = []
    for i in range(5):  # 0 to 4
        range_list.append(i)
    results["range_5"] = range_list

    # Range with start and stop
    range_start = []
    for i in range(2, 7):  # 2 to 6
        range_start.append(i)
    results["range_2_7"] = range_start

    # Range with step
    range_step = []
    for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
        range_step.append(i)
    results["range_step_2"] = range_step

    # Range with negative step (countdown)
    countdown = []
    for i in range(10, 0, -1):  # 10 to 1
        countdown.append(i)
    results["countdown"] = countdown

    # Range for indexing
    items = ["a", "b", "c", "d"]
    indexed = []
    for i in range(len(items)):
        indexed.append(f"{i}:{items[i]}")
    results["indexed_items"] = indexed

    return results


def demonstrate_while_loops() -> dict[str, Any]:
    """
    Demonstrate while loops.

    Returns:
        Dictionary with while loop examples
    """
    results = {}

    # Basic while loop
    count = 0
    total = 0
    while count < 5:
        total += count
        count += 1
    results["while_sum"] = total
    results["while_count"] = count

    # While loop with condition
    number = 1
    factorial = 1
    n = 5
    while number <= n:
        factorial *= number
        number += 1
    results["factorial_5"] = factorial

    # While with complex condition
    x = 10
    iterations = 0
    while x > 0 and iterations < 100:
        x -= 2
        iterations += 1
    results["complex_while_iterations"] = iterations
    results["complex_while_x"] = x

    return results


def demonstrate_loop_control() -> dict[str, Any]:
    """
    Demonstrate loop control statements (break, continue, pass).

    Returns:
        Dictionary with loop control examples
    """
    results = {}

    # Break statement
    break_numbers = []
    for i in range(10):
        if i == 5:
            break  # Exit loop when i is 5
        break_numbers.append(i)
    results["break_at_5"] = break_numbers

    # Continue statement
    continue_numbers = []
    for i in range(10):
        if i % 2 == 0:
            continue  # Skip even numbers
        continue_numbers.append(i)
    results["odd_numbers"] = continue_numbers

    # Pass statement (placeholder)
    pass_count = 0
    for i in range(5):
        if i == 2:
            pass  # Do nothing, just a placeholder
        pass_count += 1
    results["pass_count"] = pass_count

    # Break in while loop
    search_number = 7
    found_index = -1
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 7, 9, 7, 9]
    index = 0
    while index < len(numbers):
        if numbers[index] == search_number:
            found_index = index
            break
        index += 1
    results["found_index"] = found_index

    # Continue with multiple conditions
    filtered = []
    for i in range(20):
        if i < 5:
            continue
        if i > 15:
            continue
        if i % 2 == 0:
            continue
        filtered.append(i)
    results["filtered_odd_5_15"] = filtered

    return results


def demonstrate_nested_loops() -> dict[str, Any]:
    """
    Demonstrate nested loops.

    Returns:
        Dictionary with nested loop examples
    """
    results = {}

    # Nested for loops - multiplication table
    mult_table = []
    for i in range(1, 4):
        row = []
        for j in range(1, 4):
            row.append(i * j)
        mult_table.append(row)
    results["mult_table_3x3"] = mult_table

    # Nested loops with lists
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = []
    for row in matrix:
        for item in row:
            flattened.append(item)
    results["flattened_matrix"] = flattened

    # Nested loops with break
    found_pair = None
    for i in range(1, 5):
        for j in range(1, 5):
            if i + j == 7:
                found_pair = (i, j)
                break
        if found_pair:
            break
    results["pair_sum_7"] = found_pair

    # Pattern printing (triangle)
    triangle = []
    for i in range(1, 6):
        row = ""
        for j in range(i):
            row += "* "
        triangle.append(row.strip())
    results["triangle_pattern"] = triangle

    return results


def demonstrate_loop_else() -> dict[str, Any]:
    """
    Demonstrate loop-else clause.

    Returns:
        Dictionary with loop-else examples
    """
    results = {}

    # For-else: else executes if loop completes normally
    numbers = [2, 4, 6, 8]
    found_odd = False
    for num in numbers:
        if num % 2 != 0:
            found_odd = True
            break
    else:
        # This executes because loop completed without break
        results["all_even"] = True

    # For-else with break
    numbers_with_odd = [2, 4, 5, 8]
    for num in numbers_with_odd:
        if num % 2 != 0:
            results["found_odd_number"] = num
            break
    else:
        results["no_odd_found"] = True

    # While-else
    count = 0
    while count < 3:
        count += 1
    else:
        # Executes after while condition becomes False
        results["while_else_executed"] = True
        results["final_count"] = count

    # Search with for-else
    target = 15
    items = [5, 10, 20, 25]
    for item in items:
        if item == target:
            results["target_found"] = True
            break
    else:
        results["target_not_found"] = True

    return results


def demonstrate_enumerate_zip() -> dict[str, Any]:
    """
    Demonstrate enumerate and zip functions.

    Returns:
        Dictionary with enumerate and zip examples
    """
    results = {}

    # Enumerate - get index and value
    fruits = ["apple", "banana", "cherry"]
    enumerated = []
    for index, fruit in enumerate(fruits):
        enumerated.append(f"{index}: {fruit}")
    results["enumerated_fruits"] = enumerated

    # Enumerate with start parameter
    enum_start = []
    for index, fruit in enumerate(fruits, start=1):
        enum_start.append(f"{index}. {fruit}")
    results["enumerated_start_1"] = enum_start

    # Zip - combine multiple iterables
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    zipped = []
    for name, age in zip(names, ages):
        zipped.append(f"{name} is {age}")
    results["zipped_name_age"] = zipped

    # Zip with three iterables
    cities = ["NYC", "LA", "Chicago"]
    combined = []
    for name, age, city in zip(names, ages, cities):
        combined.append(f"{name}, {age}, {city}")
    results["zipped_three"] = combined

    # Zip with unequal lengths (stops at shortest)
    short_list = [1, 2]
    long_list = [10, 20, 30, 40]
    zip_unequal = []
    for a, b in zip(short_list, long_list):
        zip_unequal.append((a, b))
    results["zip_unequal"] = zip_unequal

    return results


def demonstrate_list_comprehensions() -> dict[str, Any]:
    """
    Demonstrate list comprehensions as loop alternatives.

    Returns:
        Dictionary with list comprehension examples
    """
    results = {}

    # Basic list comprehension
    squares = [x**2 for x in range(5)]
    results["squares"] = squares

    # List comprehension with condition
    evens = [x for x in range(10) if x % 2 == 0]
    results["evens"] = evens

    # List comprehension with transformation
    words = ["hello", "world", "python"]
    upper_words = [word.upper() for word in words]
    results["upper_words"] = upper_words

    # List comprehension with if-else
    parity = ["even" if x % 2 == 0 else "odd" for x in range(5)]
    results["parity_list"] = parity

    # Nested list comprehension
    matrix = [[i * j for j in range(3)] for i in range(3)]
    results["matrix_3x3"] = matrix

    # List comprehension with multiple conditions
    filtered = [x for x in range(20) if x % 2 == 0 if x % 3 == 0]
    results["divisible_2_and_3"] = filtered

    return results


def demonstrate_common_patterns() -> dict[str, Any]:
    """
    Demonstrate common loop patterns and idioms.

    Returns:
        Dictionary with pattern examples
    """
    results = {}

    # Pattern 1: Counting occurrences
    text = "hello world"
    char_count = {}
    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    results["char_count"] = char_count

    # Pattern 2: Filtering with accumulation
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_sum = 0
    for num in numbers:
        if num % 2 == 0:
            even_sum += num
    results["even_sum"] = even_sum

    # Pattern 3: Finding min/max manually
    values = [45, 23, 67, 12, 89, 34]
    min_val = values[0]
    max_val = values[0]
    for val in values:
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    results["manual_min"] = min_val
    results["manual_max"] = max_val

    # Pattern 4: Building a list with conditions
    grades = [85, 92, 78, 90, 88, 76, 95]
    high_grades = []
    for grade in grades:
        if grade >= 90:
            high_grades.append(grade)
    results["high_grades"] = high_grades

    # Pattern 5: Reversing a list
    original = [1, 2, 3, 4, 5]
    reversed_list = []
    for i in range(len(original) - 1, -1, -1):
        reversed_list.append(original[i])
    results["reversed_manual"] = reversed_list

    # Pattern 6: Pairing adjacent elements
    nums = [1, 2, 3, 4, 5]
    pairs = []
    for i in range(len(nums) - 1):
        pairs.append((nums[i], nums[i + 1]))
    results["adjacent_pairs"] = pairs

    return results


def fibonacci_sequence(n: int) -> List[int]:
    """
    Generate Fibonacci sequence using loops.

    Args:
        n: Number of terms to generate

    Returns:
        List of Fibonacci numbers
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])

    return fib


def main() -> None:
    """
    Main function demonstrating all loop types and patterns.
    """
    print("=" * 60)
    print("Program 05: Loops")
    print("=" * 60)

    # Basic for loops
    print("\n🔁 BASIC FOR LOOPS")
    print("-" * 60)
    basic = demonstrate_basic_for_loops()
    print(f"Sum of [1,2,3,4,5]: {basic['sum_list']}")
    print(f"Letters in 'Python': {basic['letters']}")
    print(f"Dictionary keys: {basic['dict_keys']}")
    print(f"Dictionary items: {basic['dict_items'][:2]}...")

    # Range function
    print("\n📊 RANGE FUNCTION")
    print("-" * 60)
    ranges = demonstrate_range_function()
    print(f"range(5): {ranges['range_5']}")
    print(f"range(2, 7): {ranges['range_2_7']}")
    print(f"range(0, 10, 2): {ranges['range_step_2']}")
    print(f"Countdown: {ranges['countdown'][:5]}...")

    # While loops
    print("\n⏳ WHILE LOOPS")
    print("-" * 60)
    while_demo = demonstrate_while_loops()
    print(f"While sum (0-4): {while_demo['while_sum']}")
    print(f"Factorial of 5: {while_demo['factorial_5']}")
    print(f"Complex while iterations: {while_demo['complex_while_iterations']}")

    # Loop control
    print("\n🎮 LOOP CONTROL (break, continue, pass)")
    print("-" * 60)
    control = demonstrate_loop_control()
    print(f"Break at 5: {control['break_at_5']}")
    print(f"Odd numbers (continue): {control['odd_numbers']}")
    print(f"Found 7 at index: {control['found_index']}")
    print(f"Filtered (5-15, odd): {control['filtered_odd_5_15']}")

    # Nested loops
    print("\n🔗 NESTED LOOPS")
    print("-" * 60)
    nested = demonstrate_nested_loops()
    print(f"3x3 Multiplication table: {nested['mult_table_3x3']}")
    print(f"Flattened matrix: {nested['flattened_matrix']}")
    print(f"Pair that sums to 7: {nested['pair_sum_7']}")
    print("Triangle pattern:")
    for line in nested['triangle_pattern']:
        print(f"  {line}")

    # Loop-else
    print("\n🔚 LOOP-ELSE CLAUSE")
    print("-" * 60)
    loop_else = demonstrate_loop_else()
    print(f"All even: {loop_else.get('all_even', False)}")
    print(f"Found odd number: {loop_else.get('found_odd_number', 'None')}")
    print(f"While-else executed: {loop_else.get('while_else_executed')}")
    print(f"Target not found: {loop_else.get('target_not_found', False)}")

    # Enumerate and zip
    print("\n🔢 ENUMERATE & ZIP")
    print("-" * 60)
    enum_zip = demonstrate_enumerate_zip()
    print(f"Enumerated: {enum_zip['enumerated_fruits']}")
    print(f"Enumerated (start=1): {enum_zip['enumerated_start_1']}")
    print(f"Zipped: {enum_zip['zipped_name_age']}")
    print(f"Zip unequal: {enum_zip['zip_unequal']}")

    # List comprehensions
    print("\n⚡ LIST COMPREHENSIONS")
    print("-" * 60)
    comprehensions = demonstrate_list_comprehensions()
    print(f"Squares: {comprehensions['squares']}")
    print(f"Evens: {comprehensions['evens']}")
    print(f"Upper words: {comprehensions['upper_words']}")
    print(f"Parity: {comprehensions['parity_list']}")

    # Common patterns
    print("\n📋 COMMON PATTERNS")
    print("-" * 60)
    patterns = demonstrate_common_patterns()
    print(f"Char count in 'hello world': {dict(list(patterns['char_count'].items())[:3])}...")
    print(f"Even sum (1-10): {patterns['even_sum']}")
    print(f"Min/Max: {patterns['manual_min']}, {patterns['manual_max']}")
    print(f"Adjacent pairs: {patterns['adjacent_pairs'][:3]}...")

    # Fibonacci
    print("\n🔢 FIBONACCI SEQUENCE")
    print("-" * 60)
    fib = fibonacci_sequence(10)
    print(f"First 10 Fibonacci numbers: {fib}")

    print("\n" + "=" * 60)
    print("✅ Program completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
