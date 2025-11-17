# 08_tuples

## Description

Master Python tuples - immutable sequences that provide data integrity, memory efficiency, and can be used as dictionary keys. This program covers tuple creation, operations, unpacking, and demonstrates when to use tuples vs lists.

This is Program #8 in the 500 Programs Collection.

## Learning Objectives

- Create tuples using various syntaxes
- Understand tuple immutability and its benefits
- Master tuple indexing and slicing
- Use tuple unpacking effectively
- Work with nested tuples
- Compare tuples with lists
- Understand tuple use cases (dictionary keys, function returns)
- Apply tuple best practices

## Features

- Multiple tuple creation methods
- Comprehensive indexing and slicing
- Tuple methods (count, index)
- Tuple operations (concatenation, repetition, comparison)
- Advanced tuple unpacking patterns
- Nested tuple operations
- Immutability demonstrations
- Memory efficiency comparisons with lists
- Practical use cases

## Usage

```bash
python src/main.py
```

## Example Output

```
============================================================
Program 08: Tuples
============================================================

1. Tuple Creation:
   empty: ()
   single: (1,)
   numbers: (1, 2, 3, 4, 5)
   mixed_types: (1, 'hello', 3.14, True, None)
   nested: ((1, 2), (3, 4), (5, 6))
   without_parens: (1, 2, 3)

2. Indexing and Slicing:
   first: 10
   last: 100
   slice_2_5: (30, 40, 50)

3. Tuple Unpacking:
   basic: {'x': 10, 'y': 20}
   swapped: {'x': 10, 'y': 5}
   extended: {'first': 1, 'second': 2, 'rest': [3, 4, 5, 6, 7, 8, 9, 10]}

============================================================
✅ Program completed!
============================================================
```

## Key Concepts

### 1. Tuple Creation

```python
# Empty tuple
empty = ()

# Single element (note the comma!)
single = (1,)  # Comma required
not_tuple = (1)  # This is just an integer

# Multiple elements
numbers = (1, 2, 3, 4, 5)

# Without parentheses (tuple packing)
coords = 10, 20, 30

# From other iterables
tuple_from_list = tuple([1, 2, 3])
tuple_from_string = tuple("hello")  # ('h', 'e', 'l', 'l', 'o')
```

### 2. Immutability

```python
numbers = (1, 2, 3, 4, 5)

# Cannot modify
# numbers[0] = 10  # TypeError!
# numbers.append(6)  # AttributeError!

# But mutable objects inside tuples CAN be modified
mixed = ([1, 2, 3], [4, 5, 6])
mixed[0].append(99)  # This works!

# To "modify" a tuple, create a new one
numbers_list = list(numbers)
numbers_list.append(6)
new_tuple = tuple(numbers_list)
```

### 3. Tuple Unpacking

```python
# Basic unpacking
point = (10, 20)
x, y = point

# Multiple assignment
a, b, c = 1, 2, 3

# Swap values elegantly
x, y = y, x

# Extended unpacking (Python 3+)
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
first, second, *rest = numbers
# first=1, second=2, rest=[3,4,5,6,7,8,9,10]

first, *middle, last = numbers
# first=1, middle=[2,3,4,5,6,7,8,9], last=10

# Nested unpacking
nested = ((1, 2), (3, 4))
(a, b), (c, d) = nested
```

### 4. Tuple Methods

```python
numbers = (1, 2, 3, 2, 4, 2, 5)

# count() - count occurrences
count = numbers.count(2)  # 3

# index() - find first occurrence
index = numbers.index(3)  # 2
```

### 5. Tuple Operations

```python
# Concatenation
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
combined = tuple1 + tuple2  # (1, 2, 3, 4, 5, 6)

# Repetition
repeated = (1, 2) * 3  # (1, 2, 1, 2, 1, 2)

# Membership
3 in (1, 2, 3)  # True
10 not in (1, 2, 3)  # True

# Comparison (lexicographic)
(1, 2, 3) < (1, 2, 4)  # True
(1, 2, 3) == (1, 2, 3)  # True
```

### 6. Tuples as Dictionary Keys

```python
# Tuples are hashable (lists are not)
locations = {
    (0, 0): "origin",
    (1, 0): "east",
    (0, 1): "north"
}

# This works
value = locations[(0, 0)]

# Lists cannot be dictionary keys
# bad = {[0, 0]: "origin"}  # TypeError!
```

### 7. Function Returns

```python
def get_stats(numbers):
    """Return multiple values as tuple."""
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

minimum, maximum, average = get_stats([1, 2, 3, 4, 5])
```

## Best Practices

1. **Use Tuples for Heterogeneous Data**
   ```python
   # Good - different types, fixed structure
   person = ("Alice", 25, "New York")

   # Lists better for homogeneous data
   numbers = [1, 2, 3, 4, 5]
   ```

2. **Remember the Comma for Single-Element Tuples**
   ```python
   single = (1,)  # Tuple with one element
   not_tuple = (1)  # Just an integer
   ```

3. **Use Tuples for Multiple Return Values**
   ```python
   def divide_with_remainder(a, b):
       return a // b, a % b

   quotient, remainder = divide_with_remainder(17, 5)
   ```

4. **Leverage Tuple Unpacking**
   ```python
   # Good - clear and Pythonic
   x, y, z = coordinates

   # Less Pythonic
   x = coordinates[0]
   y = coordinates[1]
   z = coordinates[2]
   ```

5. **Use Tuples as Dictionary Keys**
   ```python
   # Matrix representation
   matrix = {
       (0, 0): 1,
       (0, 1): 2,
       (1, 0): 3,
       (1, 1): 4
   }
   ```

6. **Prefer Tuples for Data Integrity**
   - When data shouldn't change
   - For configuration values
   - As dictionary keys
   - For function return values

## Tuple vs List Comparison

| Feature | Tuple | List |
|---------|-------|------|
| Mutability | Immutable | Mutable |
| Syntax | `()` | `[]` |
| Performance | Faster | Slower |
| Memory | Less | More |
| Methods | 2 (count, index) | Many (append, extend, etc.) |
| Use Case | Fixed data, dict keys | Dynamic collections |
| Hashable | Yes | No |

## When to Use Tuples

1. **Data that shouldn't change**: Configuration, constants
2. **Dictionary keys**: Coordinate systems, multi-key lookups
3. **Function returns**: Multiple values
4. **Performance**: Slightly faster than lists
5. **Data integrity**: Prevent accidental modifications

## When to Use Lists

1. **Data that needs modification**: Adding, removing items
2. **Homogeneous collections**: All same type
3. **Unknown size**: Dynamic growth needed
4. **Need list methods**: sort(), reverse(), etc.

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

## Memory Efficiency Example

```python
import sys

lst = [1, 2, 3, 4, 5]
tpl = (1, 2, 3, 4, 5)

list_size = sys.getsizeof(lst)    # Larger
tuple_size = sys.getsizeof(tpl)   # Smaller

# Tuples use less memory
```

## Common Patterns

### Named Tuples (for readability)

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)

# Access by name or index
print(p.x, p.y)    # 10 20
print(p[0], p[1])  # 10 20
```

---

**Program**: 08 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics / Data Structures
**Estimated Time**: 30-45 minutes

[← Previous (07)](../07_lists/) | [Back to Index](../../docs/INDEX.md) | [Next (09) →](../09_dictionaries/)
