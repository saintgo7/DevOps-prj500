# 02_variables_datatypes

## 📄 Description

A comprehensive exploration of Python's fundamental data types and variable handling. This program provides hands-on demonstrations of integers, floats, strings, booleans, None, type checking, type conversion, and multiple assignment patterns.

This is Program #2 in the 500 Programs Collection, building upon the basics introduced in Program 01.

## 🎯 Learning Objectives

- Master Python's fundamental data types (int, float, str, bool, None)
- Understand variable declaration and assignment
- Learn number systems (binary, octal, hexadecimal)
- Work with string operations and formatting
- Understand boolean logic and comparisons
- Master type checking with `type()` and `isinstance()`
- Learn type conversion (casting)
- Use multiple assignment and tuple unpacking
- Understand truthy and falsy values
- Recognize Python's dynamic typing

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
cd 01-100_Python/02_variables_datatypes

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
Program 02: Variables and Data Types
============================================================

📊 INTEGERS
------------------------------------------------------------
Positive integer: 42
Negative integer: -17
Large integer: 1,000,000
Binary 0b1010 = 10
Hexadecimal 0xA = 10
Type: int

🔢 FLOATING-POINT NUMBERS
------------------------------------------------------------
Simple float: 3.14
Scientific notation: 1500.0
Small number: 0.0015
Infinity: inf
Type: float

📝 STRINGS
------------------------------------------------------------
Concatenation: Hello World
Repetition: Python! Python! Python!
F-string: My name is Alice and I'm 30 years old
String length: 11
Type: str

✅ BOOLEANS
------------------------------------------------------------
True AND False = False
True OR False = True
NOT True = False
5 == 5 = True
Type: bool

∅ NONE TYPE
------------------------------------------------------------
None value: None
Function with value: Something
Function with None: None
Type: NoneType

🔍 TYPE CHECKING
------------------------------------------------------------
Value: 42 | Type: int | Is int: True
Value: Hello | Type: str | Is str: True

🔄 TYPE CONVERSION
------------------------------------------------------------
String '42' to int: 42
Int 42 to string: '42'
Float 3.14 to int: 3
Int 1 to bool: True
Bool True to int: 1

🔀 MULTIPLE ASSIGNMENT
------------------------------------------------------------
x, y, z = 1, 2, 3
a = b = c = (10, 10, 10)
Swapped values: (10, 5)

============================================================
✅ Program completed successfully!
============================================================
```

### Use as a Module

```python
from src.main import demonstrate_integers, demonstrate_type_checking

# Get integer demonstrations
integers = demonstrate_integers()
print(f"Large number: {integers['large']}")

# Check type of a value
type_info = demonstrate_type_checking(42)
print(f"Type: {type_info['type']}")
```

## 🧪 Running Tests

### Run All Tests

```bash
# Run tests with pytest
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test class
pytest tests/test_main.py::TestDemonstrateIntegers -v
```

### Expected Test Output

```
tests/test_main.py::TestDemonstrateIntegers::test_returns_dict PASSED
tests/test_main.py::TestDemonstrateIntegers::test_positive_integer PASSED
tests/test_main.py::TestDemonstrateFloats::test_simple_float PASSED
...
======================== 85+ passed in 0.15s ========================
```

## 📂 Project Structure

```
02_variables_datatypes/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── src/                   # Source code
│   ├── __init__.py       # Package initializer
│   └── main.py           # Main program (350+ lines)
└── tests/                # Test files
    ├── __init__.py       # Test package initializer
    └── test_main.py      # Unit tests (85+ test cases)
```

## 💡 Key Concepts

### 1. Integer (int)

Whole numbers without decimal points.

```python
positive = 42
negative = -17
binary = 0b1010      # Binary: 10
octal = 0o12         # Octal: 10
hexadecimal = 0xA    # Hex: 10
```

**Key Facts:**
- No size limit (arbitrary precision)
- Use underscores for readability: `1_000_000`
- Support multiple number systems

### 2. Float (float)

Numbers with decimal points.

```python
pi = 3.14
scientific = 1.5e3     # 1500.0
small = 1.5e-3         # 0.0015
infinity = float('inf')
nan = float('nan')
```

**Key Facts:**
- 64-bit double precision
- Special values: `inf`, `-inf`, `nan`
- Potential precision issues

### 3. String (str)

Sequences of characters.

```python
single = 'Hello'
double = "World"
triple = """Multi
line"""
formatted = f"Name: {name}"
raw = r"C:\path\file"
```

**Key Facts:**
- Immutable sequences
- Three quoting styles
- Rich set of methods
- F-strings for formatting

### 4. Boolean (bool)

True or False values.

```python
true_value = True
false_value = False
result = (5 > 3)  # True

# Truthy vs Falsy
bool(1)        # True
bool(0)        # False
bool("text")   # True
bool("")       # False
```

**Key Facts:**
- Subclass of int (`True == 1`, `False == 0`)
- Result of comparisons
- Used in control flow

### 5. None (NoneType)

Represents absence of value.

```python
empty = None

def optional_return():
    if condition:
        return value
    return None  # Explicit is better
```

**Key Facts:**
- Singleton object
- Default return value
- Use `is None` not `== None`

### 6. Type Checking

```python
# Using type()
type(42)  # <class 'int'>
type(42).__name__  # 'int'

# Using isinstance()
isinstance(42, int)  # True
isinstance(42, (int, float))  # True (multiple types)
```

### 7. Type Conversion

```python
# To int
int("42")       # 42
int(3.14)       # 3 (truncates)
int(True)       # 1

# To float
float("3.14")   # 3.14
float(42)       # 42.0

# To string
str(42)         # "42"
str(3.14)       # "3.14"

# To boolean
bool(1)         # True
bool(0)         # False
bool("")        # False
bool("text")    # True
```

### 8. Multiple Assignment

```python
# Multiple variables
x, y, z = 1, 2, 3

# Same value
a = b = c = 10

# Swapping
x, y = y, x

# Unpacking
coords = (10, 20)
x, y = coords
```

## 🔍 Code Examples

### Working with Numbers

```python
# Arithmetic
result = 10 + 5 * 2  # 20 (order of operations)

# Integer division vs float division
print(10 / 3)   # 3.3333...
print(10 // 3)  # 3 (floor division)
print(10 % 3)   # 1 (modulo)

# Power
print(2 ** 10)  # 1024
```

### String Manipulation

```python
text = "Python Programming"

# Indexing
print(text[0])      # 'P'
print(text[-1])     # 'g'

# Slicing
print(text[0:6])    # 'Python'
print(text[7:])     # 'Programming'

# Methods
print(text.lower()) # 'python programming'
print(text.split()) # ['Python', 'Programming']
```

### Type Checking Patterns

```python
def process_value(value):
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    elif isinstance(value, (list, tuple)):
        return len(value)
    else:
        return None
```

## 📚 Related Programs

- **[01_hello_world](../01_hello_world/)**: Python basics
- **03_operators**: Arithmetic and logical operators (coming soon)
- **06_functions**: Function definitions and calls (coming soon)
- **14_classes_objects**: Object-oriented programming (coming soon)

## 🎓 Learning Notes

### Truthy and Falsy Values

**Falsy values** (evaluate to False):
- `False`
- `None`
- `0`, `0.0`, `0j`
- `""` (empty string)
- `[]` (empty list)
- `{}` (empty dict)
- `()` (empty tuple)
- `set()` (empty set)

**Everything else is truthy!**

### Best Practices

1. **Use Type Hints**
```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

2. **Use `isinstance()` for Type Checking**
```python
# Good
if isinstance(value, int):
    ...

# Avoid
if type(value) == int:
    ...
```

3. **Use `is` for None Checks**
```python
# Good
if value is None:
    ...

# Avoid
if value == None:
    ...
```

4. **Prefer F-strings for Formatting**
```python
# Modern (Python 3.6+)
message = f"Hello, {name}!"

# Older styles
message = "Hello, {}!".format(name)
message = "Hello, %s!" % name
```

### Common Pitfalls

1. **Float Precision**
```python
0.1 + 0.2  # 0.30000000000000004 (!)
# Use decimal module for precision
```

2. **Boolean is Subclass of Int**
```python
True == 1   # True
False == 0  # True
isinstance(True, int)  # True
```

3. **String Immutability**
```python
text = "hello"
text[0] = "H"  # TypeError! Strings are immutable
text = "H" + text[1:]  # Create new string instead
```

4. **Integer Division**
```python
10 / 3   # 3.3333... (float division)
10 // 3  # 3 (integer/floor division)
```

## 🔗 References

- [Python Data Types](https://docs.python.org/3/library/stdtypes.html)
- [Python Type System](https://docs.python.org/3/library/typing.html)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Python Numbers](https://docs.python.org/3/tutorial/introduction.html#numbers)
- [Python Strings](https://docs.python.org/3/tutorial/introduction.html#strings)
- [Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)

## 🚀 Next Steps

After mastering this program:

1. **Experiment**: Try different type conversions
2. **Practice**: Create variables of each type
3. **Explore**: Discover more string methods
4. **Challenge**: What happens with edge cases?
5. **Move On**: Continue to Program 03 (Operators)

## 📝 Exercises

Try these challenges:

1. Create variables of all data types and print their types
2. Convert between different number systems (binary, octal, hex)
3. Practice string slicing and methods
4. Write a function that accepts any type and returns its type name
5. Experiment with truthy/falsy values

## 🎉 Congratulations!

You've mastered Python's fundamental data types! You now understand the building blocks of Python programming.

---

**Program**: 02 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics
**Estimated Time**: 30-45 minutes

[← Previous Program (01)](../01_hello_world/) | [Back to Index](../../docs/INDEX.md) | [Next Program (03) →](../03_operators/)
