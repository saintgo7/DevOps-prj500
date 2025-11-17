# 01_hello_world

## 📄 Description

The classic "Hello, World!" program - your first step into Python programming! This program demonstrates the most fundamental concepts of Python, including basic output, functions, type hints, and documentation.

This is Program #1 in the 500 Programs Collection, designed as the perfect starting point for beginners learning Python.

## 🎯 Learning Objectives

- Understand basic Python syntax
- Learn how to use the `print()` function
- Work with strings and f-strings
- Create and call functions
- Use type hints for better code clarity
- Write docstrings for documentation
- Run Python programs from the command line
- Write unit tests with pytest

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
cd 01-100_Python/01_hello_world

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
Hello, World!
Hello, Python!
Hello, Vibe Coder!

Welcome to Python 3.11+!
========================================
🎉 Your first program is running! 🎉
========================================
```

### Use as a Module

```python
from src.main import greet

# Use the greet function
print(greet())  # Hello, World!
print(greet("Alice"))  # Hello, Alice!
```

## 📸 Example Output

```
$ python src/main.py
Hello, World!
Hello, Python!
Hello, Vibe Coder!

Welcome to Python 3.11+!
========================================
🎉 Your first program is running! 🎉
========================================
```

## 🧪 Running Tests

### Run All Tests

```bash
# Run tests with pytest
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

### Expected Test Output

```
tests/test_main.py::TestGreetFunction::test_greet_default PASSED
tests/test_main.py::TestGreetFunction::test_greet_with_name PASSED
tests/test_main.py::TestGreetFunction::test_greet_with_empty_string PASSED
...
======================== 20 passed in 0.05s ========================
```

### Code Quality Checks

```bash
# Format code with black
black src/ tests/

# Lint with pylint
pylint src/

# Type check with mypy
mypy src/
```

## 📂 Project Structure

```
01_hello_world/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── src/                   # Source code
│   ├── __init__.py       # Package initializer
│   └── main.py           # Main program
└── tests/                # Test files
    ├── __init__.py       # Test package initializer
    └── test_main.py      # Unit tests
```

## 💡 Key Concepts

### 1. Print Function
The `print()` function outputs text to the console:
```python
print("Hello, World!")
```

### 2. String Formatting
Python f-strings provide an elegant way to format strings:
```python
name = "Python"
print(f"Hello, {name}!")
```

### 3. Functions
Functions encapsulate reusable code:
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### 4. Type Hints
Type hints make code more readable and catch errors early:
```python
def greet(name: Optional[str] = None) -> str:
    # Function implementation
```

### 5. Docstrings
Docstrings document your code:
```python
"""
Generate a greeting message.

Args:
    name: Optional name to greet

Returns:
    A greeting string
"""
```

### 6. Main Guard
The main guard allows code to be imported or run directly:
```python
if __name__ == "__main__":
    main()
```

## 🔍 Code Walkthrough

### The greet() Function

```python
def greet(name: Optional[str] = None) -> str:
    if name is None:
        name = "World"
    return f"Hello, {name}!"
```

- **Parameter**: `name` is optional (can be None)
- **Default**: If no name provided, uses "World"
- **Return**: Formatted greeting string

### The main() Function

```python
def main() -> None:
    print(greet())
    print(greet("Python"))
    # More examples...
```

- Demonstrates multiple ways to call `greet()`
- Shows string formatting with f-strings
- Adds visual formatting with separators

## 📚 Related Programs

- **02_variables_datatypes**: Learn about different data types in Python
- **03_operators**: Explore Python operators
- **06_functions**: Deep dive into Python functions

## 🎓 Learning Notes

### Why Start with Hello World?

1. **Simple Syntax**: Introduces Python's clean, readable syntax
2. **Immediate Feedback**: See results instantly
3. **Build Confidence**: Success on day one!
4. **Foundation**: Every concept builds from here

### Best Practices Demonstrated

- ✅ Type hints for clarity
- ✅ Comprehensive docstrings
- ✅ Modular function design
- ✅ Unit tests with good coverage
- ✅ Clean code structure
- ✅ Professional project layout

### Common Beginner Mistakes

1. **Forgetting Parentheses**: `print "Hello"` ❌ → `print("Hello")` ✅
2. **Incorrect Indentation**: Python uses indentation for code blocks
3. **Quote Mismatch**: Use matching quotes `"` or `'`
4. **Case Sensitivity**: `Print` ≠ `print`

## 🔗 References

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Python Print Function Docs](https://docs.python.org/3/library/functions.html#print)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)

## 🚀 Next Steps

After mastering this program:

1. **Modify**: Try greeting different names
2. **Extend**: Add more greeting styles (different languages, times of day)
3. **Experiment**: What happens with very long names? Special characters?
4. **Move On**: Continue to Program 02 (Variables & Data Types)

## 🎉 Congratulations!

You've completed your first program in the 500 Programs Collection!

This is just the beginning of an exciting journey. Keep the momentum going!

---

**Program**: 01 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics
**Estimated Time**: 15-30 minutes

[← Back to Index](../../docs/INDEX.md) | [Next Program (02) →](../02_variables_datatypes/)
