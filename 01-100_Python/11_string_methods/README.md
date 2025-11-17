# 11_string_methods

## Description

Master Python string manipulation with comprehensive demonstrations of string methods, formatting, encoding, and advanced techniques. Strings are fundamental in Python programming, and this program covers everything from basic operations to advanced formatting patterns.

This is Program #11 in the 500 Programs Collection.

## Learning Objectives

- Master string case conversion methods
- Use search and find methods effectively
- Perform string validation checks
- Modify and clean strings
- Split and join strings efficiently
- Align and format text
- Use multiple string formatting approaches
- Handle encoding and decoding
- Apply string best practices

## Features

- Case conversion (upper, lower, title, capitalize, swapcase)
- Search methods (find, rfind, index, count, startswith, endswith)
- Validation methods (isalpha, isdigit, isalnum, etc.)
- Modification methods (strip, replace, removeprefix, removesuffix)
- Split and join operations
- Alignment methods (center, ljust, rjust, zfill)
- Multiple formatting approaches (%, format(), f-strings, Template)
- Encoding and decoding methods
- Advanced techniques (translate, expandtabs)

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Case Conversion Methods

```python
text = "Hello World Python"

text.lower()        # "hello world python"
text.upper()        # "HELLO WORLD PYTHON"
text.title()        # "Hello World Python"
text.capitalize()   # "Hello world python" (first char only)
text.swapcase()     # "hELLO wORLD pYTHON"
"ß".casefold()      # More aggressive than lower()
```

### 2. Search Methods

```python
text = "Hello World, Hello Python"

# find() - returns index or -1
text.find("Hello")           # 0
text.find("Hello", 10)       # 13 (start from index 10)
text.find("Java")            # -1 (not found)

# rfind() - find from right
text.rfind("Hello")          # 13

# index() - like find but raises ValueError
text.index("World")          # 6

# count() - count occurrences
text.count("Hello")          # 2

# startswith(), endswith()
text.startswith("Hello")     # True
text.endswith("Python")      # True

# in operator
"World" in text              # True
```

### 3. Validation Methods

```python
"abc".isalpha()              # True - all letters
"123".isdigit()              # True - all digits
"abc123".isalnum()           # True - letters and digits
"   ".isspace()              # True - all whitespace
"hello".islower()            # True
"HELLO".isupper()            # True
"Hello World".istitle()      # True
"variable_name".isidentifier()  # True - valid identifier
```

### 4. Modification Methods

```python
# strip() - remove whitespace
"  hello  ".strip()          # "hello"
"  hello  ".lstrip()         # "hello  " (left strip)
"  hello  ".rstrip()         # "  hello" (right strip)
"...hello...".strip(".")     # "hello" (strip specific chars)

# replace()
"hello world".replace("world", "python")  # "hello python"
"aaa bbb aaa".replace("aaa", "xxx", 1)   # "xxx bbb aaa" (limit)

# removeprefix(), removesuffix() (Python 3.9+)
"HelloWorld".removeprefix("Hello")  # "World"
"HelloWorld".removesuffix("World")  # "Hello"
```

### 5. Split and Join

```python
# split() - split into list
"apple,banana,cherry".split(",")     # ['apple', 'banana', 'cherry']
"hello world python".split()         # ['hello', 'world', 'python']
"a b c d e".split(" ", 2)           # ['a', 'b', 'c d e']

# rsplit() - split from right
"a b c d e".rsplit(" ", 2)          # ['a b c', 'd', 'e']

# splitlines()
"line1\nline2\nline3".splitlines()  # ['line1', 'line2', 'line3']

# partition() - split into 3 parts
"hello:world".partition(":")        # ('hello', ':', 'world')

# join() - combine list into string
",".join(["a", "b", "c"])           # "a,b,c"
" ".join(["hello", "world"])        # "hello world"
```

### 6. Alignment and Padding

```python
text = "hello"

# center()
text.center(20)                     # "       hello        "
text.center(20, "*")                # "*******hello********"

# ljust() - left justify
text.ljust(20)                      # "hello               "
text.ljust(20, "-")                 # "hello---------------"

# rjust() - right justify
text.rjust(20)                      # "               hello"
text.rjust(20, ".")                 # "...............hello"

# zfill() - zero padding
"42".zfill(10)                      # "0000000042"
"-42".zfill(10)                     # "-000000042"
```

### 7. String Formatting

```python
# Old-style % formatting
"Hello, %s! You are %d years old." % ("Alice", 25)

# str.format()
"Hello, {}! You are {} years old.".format("Bob", 30)
"{1} {0}".format("World", "Hello")  # "Hello World"
"Hello, {name}! Age: {age}".format(name="Charlie", age=35)
"Pi: {:.2f}".format(3.14159)        # "Pi: 3.14"

# f-strings (Python 3.6+) - RECOMMENDED
name = "David"
age = 40
f"Hello, {name}! You are {age} years old."
f"Next year: {age + 1}"
f"Pi: {3.14159:.2f}"

# Template strings
from string import Template
t = Template("Hello, $name! Age: $age")
t.substitute(name="Eve", age=28)
```

### 8. Encoding and Decoding

```python
text = "Hello, 世界"

# Encode to bytes
utf8_bytes = text.encode("utf-8")
ascii_bytes = "Hello".encode("ascii")

# Decode from bytes
decoded = utf8_bytes.decode("utf-8")

# Different encodings
utf16_bytes = text.encode("utf-16")
latin1_bytes = "Hello".encode("latin-1")
```

## Best Practices

1. **Use f-strings for String Formatting (Python 3.6+)**
   ```python
   # Best
   message = f"Hello, {name}! Total: ${price:.2f}"

   # Older but acceptable
   message = "Hello, {}! Total: ${:.2f}".format(name, price)

   # Avoid (old style)
   message = "Hello, %s! Total: $%.2f" % (name, price)
   ```

2. **Use join() for String Concatenation**
   ```python
   # Efficient
   result = " ".join(words)

   # Inefficient (creates many intermediate strings)
   result = ""
   for word in words:
       result += word + " "
   ```

3. **Use Raw Strings for Regex and Paths**
   ```python
   # Good
   path = r"C:\new\test.txt"
   pattern = r"\d+\.\d+"

   # Works but needs escaping
   path = "C:\\new\\test.txt"
   ```

4. **Check for Empty Strings**
   ```python
   # Good
   if not text:
       print("Empty string")

   # Works but less Pythonic
   if text == "":
       print("Empty string")
   ```

5. **Use startswith() and endswith() for Multiple Values**
   ```python
   # Good
   if filename.endswith(('.txt', '.csv', '.log')):
       process_file(filename)

   # Less efficient
   if filename.endswith('.txt') or filename.endswith('.csv') or filename.endswith('.log'):
       process_file(filename)
   ```

6. **Use strip() to Clean Input**
   ```python
   user_input = input("Enter name: ").strip()
   ```

## Common Patterns

### 1. String Cleaning

```python
def clean_text(text):
    """Remove extra whitespace and normalize."""
    return " ".join(text.split())

clean_text("hello    world  ")  # "hello world"
```

### 2. Parse CSV Line Manually

```python
line = "name,age,city"
fields = line.split(",")
```

### 3. Build Dynamic SQL Queries (use parameterized queries in production!)

```python
query = f"SELECT * FROM users WHERE name = '{name}' AND age = {age}"
```

### 4. Format Table Output

```python
print(f"{'Name':<15} {'Age':>5} {'City':^10}")
print(f"{'Alice':<15} {25:>5} {'NYC':^10}")
```

### 5. Multi-line Strings

```python
# Triple quotes
message = """
This is a
multi-line
string
"""

# Line continuation
long_string = "This is a very long string that " \
              "spans multiple lines"
```

## String Methods Cheat Sheet

| Category | Methods |
|----------|---------|
| Case | lower(), upper(), title(), capitalize(), swapcase(), casefold() |
| Search | find(), rfind(), index(), rindex(), count() |
| Check | startswith(), endswith(), in operator |
| Validate | isalpha(), isdigit(), isalnum(), isspace(), islower(), isupper(), istitle(), isdecimal(), isnumeric(), isidentifier() |
| Modify | strip(), lstrip(), rstrip(), replace(), removeprefix(), removesuffix() |
| Split/Join | split(), rsplit(), splitlines(), partition(), rpartition(), join() |
| Align | center(), ljust(), rjust(), zfill() |
| Format | %, format(), f-strings, Template |
| Encode | encode(), decode() |

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

## Performance Tips

1. **Use join() for concatenation** - O(n) vs O(n²)
2. **f-strings are fast** - faster than % and format()
3. **String methods are optimized** - use built-ins
4. **Avoid repeated string creation** in loops

---

**Program**: 11 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics / String Manipulation
**Estimated Time**: 45-60 minutes

[← Previous (10)](../10_sets/) | [Back to Index](../../docs/INDEX.md) | [Next (12) →](../12_file_io/)
