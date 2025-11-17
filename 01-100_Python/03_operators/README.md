# 03_operators

## 📄 Description

A comprehensive exploration of all Python operators. This program provides hands-on demonstrations of arithmetic, comparison, logical, assignment, bitwise, membership, identity operators, and operator precedence rules.

This is Program #3 in the 500 Programs Collection, continuing the Python fundamentals series.

## 🎯 Learning Objectives

- Master all arithmetic operators (+, -, *, /, //, %, **)
- Understand comparison operators and chained comparisons
- Learn logical operators and short-circuit evaluation
- Practice augmented assignment operators
- Understand bitwise operators and bit manipulation
- Use membership operators effectively
- Distinguish between identity (is) and equality (==)
- Master operator precedence and associativity
- Apply operators in real-world scenarios

## 🛠️ Tech Stack

- **Python**: 3.11+
- **Testing**: pytest
- **Code Quality**: black, pylint, mypy
- **Type Hints**: Full type annotations

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

```bash
# Navigate to the program directory
cd 01-100_Python/03_operators

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Run the Program

```bash
# From the program directory
python src/main.py
```

### Expected Output

```
============================================================
Program 03: Operators
============================================================

🔢 ARITHMETIC OPERATORS
------------------------------------------------------------
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333
10 // 3 = 3 (floor division)
10 % 3 = 1 (remainder)
10 ** 3 = 1000 (power)
2 + 3 * 4 = 14 (order matters)
(2 + 3) * 4 = 20 (parentheses first)

⚖️  COMPARISON OPERATORS
------------------------------------------------------------
10 == 5: False
10 != 5: True
10 > 5: True
10 < 5: False
10 >= 5: True
10 <= 5: False
1 < 5 < 10: True (chained comparison)
'apple' < 'banana': True (lexicographic)

🔀 LOGICAL OPERATORS
------------------------------------------------------------
True and True: True
True and False: False
True or False: True
False or False: False
not True: False
5 and 10: 10 (returns last if all truthy)
0 and 10: 0 (returns first falsy)
5 or 10: 5 (returns first truthy)
0 or 10: 10 (returns last if all falsy)

✏️  ASSIGNMENT OPERATORS
------------------------------------------------------------
x = 10: 10
y = 5; y += 3: 8
z = 10; z -= 4: 6
a = 3; a *= 4: 12
b = 20; b /= 4: 5.0
e = 2; e **= 3: 8

🔣 BITWISE OPERATORS
------------------------------------------------------------
12 = 0b1100, 10 = 0b1010
12 & 10 = 8 (AND)
12 | 10 = 14 (OR)
12 ^ 10 = 6 (XOR)
~12 = -13 (NOT)
12 << 2 = 48 (left shift)
12 >> 2 = 3 (right shift)
12 is even: True

📍 MEMBERSHIP OPERATORS
------------------------------------------------------------
3 in [1,2,3,4,5]: True
10 not in [1,2,3,4,5]: True
'Python' in 'Python Programming': True
'name' in {'name':'Alice'}: True
'gram' in 'Programming': True

🔍 IDENTITY OPERATORS
------------------------------------------------------------
a = [1,2,3]; c = a; (a is c): True
a = [1,2,3]; b = [1,2,3]; (a is b): False
a == b: True (equal values)
a is b: False (same object)
None is None: True
256 is 256: True (cached)

📊 OPERATOR PRECEDENCE
------------------------------------------------------------
2 + 3 * 4 = 14 (* before +)
(2 + 3) * 4 = 20 (parentheses first)
2 ** 3 ** 2 = 512 (right-associative)
10 + 5 * 2 - 3 = 17
5 > 3 and 10 < 20 = True
5 | 3 & 2 = 5 (& before |)
(5 | 3) & 2 = 2 (parentheses)

============================================================
✅ Program completed successfully!
============================================================
```

## 🧪 Running Tests

### Run All Tests

```bash
# Run tests with pytest
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test class
pytest tests/test_main.py::TestArithmeticOperators -v
```

### Expected Test Output

```
tests/test_main.py::TestArithmeticOperators::test_addition PASSED
tests/test_main.py::TestComparisonOperators::test_equal PASSED
tests/test_main.py::TestLogicalOperators::test_and_operator PASSED
...
======================== 100+ passed in 0.20s ========================
```

## 📂 Project Structure

```
03_operators/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── src/                   # Source code
│   ├── __init__.py       # Package initializer
│   └── main.py           # Main program (500+ lines)
└── tests/                # Test files
    ├── __init__.py       # Test package initializer
    └── test_main.py      # Unit tests (100+ test cases)
```

## 💡 Key Concepts

### 1. Arithmetic Operators

Perform mathematical operations.

```python
a + b   # Addition
a - b   # Subtraction
a * b   # Multiplication
a / b   # Division (float result)
a // b  # Floor division (integer result)
a % b   # Modulo (remainder)
a ** b  # Exponentiation (power)
```

**Examples:**
```python
10 + 3    # 13
10 - 3    # 7
10 * 3    # 30
10 / 3    # 3.3333...
10 // 3   # 3
10 % 3    # 1
10 ** 3   # 1000
```

### 2. Comparison Operators

Compare two values and return boolean.

```python
a == b   # Equal
a != b   # Not equal
a > b    # Greater than
a < b    # Less than
a >= b   # Greater or equal
a <= b   # Less or equal
```

**Chained Comparisons:**
```python
1 < x < 10      # Equivalent to: 1 < x and x < 10
x < y <= z      # Can chain multiple comparisons
```

### 3. Logical Operators

Combine boolean expressions.

```python
a and b   # Logical AND
a or b    # Logical OR
not a     # Logical NOT
```

**Short-Circuit Evaluation:**
```python
# 'and' returns first falsy or last value
5 and 10    # 10
0 and 10    # 0 (stops at first falsy)

# 'or' returns first truthy or last value
5 or 10     # 5 (stops at first truthy)
0 or 10     # 10
```

### 4. Assignment Operators

Assign and modify values.

```python
x = 10      # Simple assignment
x += 5      # x = x + 5
x -= 3      # x = x - 3
x *= 2      # x = x * 2
x /= 4      # x = x / 4
x //= 3     # x = x // 3
x %= 2      # x = x % 2
x **= 3     # x = x ** 3
```

### 5. Bitwise Operators

Operate on binary representations.

```python
a & b    # Bitwise AND
a | b    # Bitwise OR
a ^ b    # Bitwise XOR
~a       # Bitwise NOT
a << n   # Left shift
a >> n   # Right shift
```

**Example:**
```python
12 & 10   # 8   (1100 & 1010 = 1000)
12 | 10   # 14  (1100 | 1010 = 1110)
12 ^ 10   # 6   (1100 ^ 1010 = 0110)
~12       # -13 (two's complement)
12 << 2   # 48  (shift left by 2: 110000)
12 >> 2   # 3   (shift right by 2: 0011)
```

**Practical Uses:**
```python
# Check if even
num & 1 == 0  # True if even

# Set bit at position n
num | (1 << n)

# Clear bit at position n
num & ~(1 << n)

# Toggle bit at position n
num ^ (1 << n)
```

### 6. Membership Operators

Check membership in sequences.

```python
x in seq        # True if x is in seq
x not in seq    # True if x is not in seq
```

**Examples:**
```python
3 in [1, 2, 3]              # True
"Python" in "Python Code"   # True
"name" in {"name": "Alice"} # True (checks keys)
```

### 7. Identity Operators

Check object identity (memory location).

```python
x is y        # True if same object
x is not y    # True if different objects
```

**Identity vs Equality:**
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b   # True (equal values)
a is b   # False (different objects)
a is c   # True (same object)
```

**None Checks:**
```python
# Always use 'is' for None
if value is None:
    ...

# Not recommended
if value == None:  # Don't do this
    ...
```

### 8. Operator Precedence

Order of evaluation (highest to lowest):

1. `()` - Parentheses
2. `**` - Exponentiation
3. `+x`, `-x`, `~x` - Unary operators
4. `*`, `/`, `//`, `%` - Multiplication, division
5. `+`, `-` - Addition, subtraction
6. `<<`, `>>` - Shifts
7. `&` - Bitwise AND
8. `^` - Bitwise XOR
9. `|` - Bitwise OR
10. `==`, `!=`, `<`, `>`, `<=`, `>=`, `is`, `in` - Comparisons
11. `not` - Logical NOT
12. `and` - Logical AND
13. `or` - Logical OR

**Examples:**
```python
2 + 3 * 4       # 14 (* before +)
(2 + 3) * 4     # 20 (parentheses first)
2 ** 3 ** 2     # 512 (** is right-associative: 2**(3**2))
5 > 3 and 10 < 20  # True (comparison before and)
```

## 🔍 Code Examples

### Practical Arithmetic

```python
# Temperature conversion
celsius = 25
fahrenheit = (celsius * 9/5) + 32  # 77.0

# Circle area
radius = 5
area = 3.14159 * radius ** 2  # 78.53975

# Average
numbers = [10, 20, 30, 40, 50]
average = sum(numbers) / len(numbers)  # 30.0
```

### Smart Comparisons

```python
# Range check
age = 25
is_adult = 18 <= age < 65  # True

# Sorting key
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
sorted_students = sorted(students, key=lambda x: x[1])
```

### Logical Patterns

```python
# Default values
name = user_input or "Guest"  # Use "Guest" if input is empty

# Validation
if username and password and len(password) >= 8:
    login()

# Multiple conditions
if (age >= 18 and has_license) or is_accompanied:
    allow_entry()
```

### Bitwise Tricks

```python
# Swap without temporary variable
a, b = 5, 10
a = a ^ b
b = a ^ b
a = a ^ b  # a=10, b=5

# Check power of 2
def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0

# Set flags
PERMISSION_READ = 1 << 0   # 0001
PERMISSION_WRITE = 1 << 1  # 0010
PERMISSION_EXEC = 1 << 2   # 0100

user_perms = PERMISSION_READ | PERMISSION_WRITE  # 0011
has_write = user_perms & PERMISSION_WRITE != 0   # True
```

## 📚 Related Programs

- **[01_hello_world](../01_hello_world/)**: Python basics
- **[02_variables_datatypes](../02_variables_datatypes/)**: Data types
- **04_conditional_statements**: If/elif/else (coming soon)
- **05_loops**: For and while loops (coming soon)

## 🎓 Learning Notes

### Best Practices

1. **Use Parentheses for Clarity**
```python
# Less clear
result = a + b * c - d / e

# More clear
result = a + (b * c) - (d / e)
```

2. **Use `is` for None**
```python
# Good
if value is None:
    ...

# Avoid
if value == None:
    ...
```

3. **Use `in` for Membership**
```python
# Good
if key in dictionary:
    ...

# Avoid
if dictionary.get(key) is not None:
    ...
```

4. **Avoid Comparing Booleans**
```python
# Good
if is_valid:
    ...

# Avoid
if is_valid == True:
    ...
```

### Common Pitfalls

1. **Float Division vs Integer Division**
```python
10 / 3   # 3.3333... (always float in Python 3)
10 // 3  # 3 (integer/floor division)
```

2. **Operator Precedence**
```python
5 + 3 * 2  # 11, not 16 (* before +)
```

3. **Identity vs Equality**
```python
a = [1, 2]
b = [1, 2]
a == b  # True (equal values)
a is b  # False (different objects)
```

4. **Bitwise vs Logical**
```python
True & False   # 0 (bitwise AND on integers)
True and False # False (logical AND)
```

5. **Division by Zero**
```python
x / 0   # ZeroDivisionError!
x / 0.0 # ZeroDivisionError!
```

### Performance Tips

1. **Augmented Assignment is Faster**
```python
# Faster
x += 1

# Slower
x = x + 1
```

2. **Membership Testing is Fast for Sets**
```python
# Fast: O(1)
if item in my_set:
    ...

# Slower: O(n)
if item in my_list:
    ...
```

3. **Short-Circuit Evaluation**
```python
# Only calls expensive() if needed
if cheap_check() and expensive():
    ...
```

## 🔗 References

- [Python Operators](https://docs.python.org/3/library/operator.html)
- [Operator Precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)
- [Bitwise Operations](https://wiki.python.org/moin/BitwiseOperators)
- [Comparison Operations](https://docs.python.org/3/reference/expressions.html#comparisons)

## 🚀 Next Steps

After mastering this program:

1. **Practice**: Solve problems using different operators
2. **Experiment**: Try edge cases and special values
3. **Apply**: Use operators in real calculations
4. **Move On**: Continue to Program 04 (Conditional Statements)

## 📝 Exercises

Try these challenges:

1. Write a calculator using all arithmetic operators
2. Create a function that checks if a number is in range using chained comparisons
3. Implement bit manipulation functions (set, clear, toggle, check bit)
4. Write a validator using logical operators
5. Compare performance of `in` with list vs set

## 🎉 Congratulations!

You've mastered Python operators! You now have the tools to perform calculations, make comparisons, manipulate bits, and write complex expressions.

---

**Program**: 03 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics
**Estimated Time**: 45-60 minutes

[← Previous Program (02)](../02_variables_datatypes/) | [Back to Index](../../docs/INDEX.md) | [Next Program (04) →](../04_conditional_statements/)
