# 09_dictionaries

## Description

Master Python dictionaries - powerful key-value data structures essential for data organization, caching, counting, and mapping. This program covers dictionary creation, manipulation, comprehensions, nested dictionaries, and advanced patterns including defaultdict and Counter.

This is Program #9 in the 500 Programs Collection.

## Learning Objectives

- Create dictionaries using multiple methods
- Access and modify dictionary elements
- Use dictionary methods effectively
- Perform dictionary operations (merge, update, iterate)
- Write dictionary comprehensions
- Work with nested dictionaries
- Use collections.defaultdict and Counter
- Apply dictionary best practices and patterns

## Features

- Multiple dictionary creation methods
- Comprehensive element access patterns
- All built-in dictionary methods
- Dictionary operations and merging
- Dictionary comprehensions with conditions
- Nested dictionary manipulation
- defaultdict for cleaner code
- Counter for frequency counting
- Practical use cases and patterns

## Usage

```bash
python src/main.py
```

## Example Output

```
============================================================
Program 09: Dictionaries
============================================================

1. Dictionary Creation:
   empty: {}
   basic: {'name': 'Alice', 'age': 25, 'city': 'NYC'}
   constructor: {'name': 'Bob', 'age': 30, 'city': 'LA'}
   comprehension: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

2. Accessing Elements:
   name_bracket: Alice
   age_get: 25
   country_default: USA
   keys: ['name', 'age', 'city']

3. Dictionary Methods:
   update: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
   pop: {'dict': {'a': 1, 'c': 3}, 'popped': 2, 'default': 'not found'}

============================================================
✅ Program completed!
============================================================
```

## Key Concepts

### 1. Dictionary Creation

```python
# Empty dictionary
empty = {}

# Basic dictionary
person = {"name": "Alice", "age": 25, "city": "NYC"}

# dict() constructor
person2 = dict(name="Bob", age=30, city="LA")

# From list of tuples
pairs = [("a", 1), ("b", 2), ("c", 3)]
dict_from_pairs = dict(pairs)

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}

# fromkeys() - create with default values
keys = ["a", "b", "c"]
default_dict = dict.fromkeys(keys, 0)  # {'a': 0, 'b': 0, 'c': 0}
```

### 2. Accessing Elements

```python
person = {"name": "Alice", "age": 25}

# Using [] - raises KeyError if key doesn't exist
name = person["name"]

# Using get() - returns None or default if key doesn't exist
age = person.get("age")
country = person.get("country", "Unknown")  # Returns "Unknown"

# Check if key exists
if "name" in person:
    print(person["name"])
```

### 3. Dictionary Methods

```python
d = {"a": 1, "b": 2}

# Update - add/modify multiple items
d.update({"c": 3, "d": 4})
d.update(e=5, f=6)

# Pop - remove and return value
value = d.pop("b")
default = d.pop("z", "not found")

# Popitem - remove and return last inserted item (Python 3.7+)
key, value = d.popitem()

# Setdefault - get value or set default if missing
d.setdefault("x", 0)  # Returns existing value or sets default

# Keys, values, items
keys = d.keys()      # dict_keys(['a', 'b', 'c'])
values = d.values()  # dict_values([1, 2, 3])
items = d.items()    # dict_items([('a', 1), ('b', 2), ('c', 3)])

# Clear - remove all items
d.clear()

# Copy - shallow copy
copy = d.copy()
```

### 4. Dictionary Operations

```python
# Merge (Python 3.9+)
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged = dict1 | dict2

# Update with |=
dict1 |= dict2

# Iterate over keys
for key in person:
    print(key)

# Iterate over values
for value in person.values():
    print(value)

# Iterate over items
for key, value in person.items():
    print(f"{key}: {value}")
```

### 5. Dictionary Comprehensions

```python
# Basic comprehension
squares = {x: x**2 for x in range(6)}

# With condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}

# From two lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
combined = {k: v for k, v in zip(keys, values)}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}

# Conditional values
numbers = {x: "even" if x % 2 == 0 else "odd" for x in range(6)}
```

### 6. Nested Dictionaries

```python
# Database-like structure
database = {
    "users": {
        "alice": {"age": 25, "city": "NYC"},
        "bob": {"age": 30, "city": "LA"}
    },
    "posts": {
        "post1": {"title": "Hello", "author": "alice"}
    }
}

# Access nested values
alice_age = database["users"]["alice"]["age"]

# Safe nested access with get()
country = database.get("users", {}).get("alice", {}).get("country", "Unknown")
```

### 7. defaultdict Pattern

```python
from collections import defaultdict

# Default int (starts at 0)
counts = defaultdict(int)
for word in ["apple", "banana", "apple"]:
    counts[word] += 1  # No KeyError!

# Default list
groups = defaultdict(list)
for category, item in data:
    groups[category].append(item)

# Default dict
nested = defaultdict(dict)
nested["user"]["name"] = "Alice"
```

### 8. Counter for Frequency Counting

```python
from collections import Counter

# Count elements
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
counter = Counter(numbers)

# Most common
most_common = counter.most_common(2)  # [(4, 4), (3, 3)]

# Counter operations
c1 = Counter(["a", "b", "c", "a"])
c2 = Counter(["a", "b", "d"])

addition = c1 + c2
subtraction = c1 - c2
intersection = c1 & c2
union = c1 | c2
```

## Best Practices

1. **Use get() for Safe Access**
   ```python
   # Good - no KeyError
   value = d.get("key", "default")

   # Risky
   value = d["key"]  # KeyError if key doesn't exist
   ```

2. **Use setdefault() for Initialization**
   ```python
   # Good
   d.setdefault("key", []).append(value)

   # More verbose
   if "key" not in d:
       d["key"] = []
   d["key"].append(value)
   ```

3. **Use Dictionary Comprehensions**
   ```python
   # Good - clear and concise
   squares = {x: x**2 for x in range(10)}

   # More verbose
   squares = {}
   for x in range(10):
       squares[x] = x**2
   ```

4. **Use defaultdict for Grouping**
   ```python
   from collections import defaultdict

   # Good
   groups = defaultdict(list)
   for item in items:
       groups[item.category].append(item)

   # More code
   groups = {}
   for item in items:
       if item.category not in groups:
           groups[item.category] = []
       groups[item.category].append(item)
   ```

5. **Use Counter for Frequency Counting**
   ```python
   # Good
   from collections import Counter
   counts = Counter(words)

   # Manual approach
   counts = {}
   for word in words:
       counts[word] = counts.get(word, 0) + 1
   ```

6. **Check Membership Before Access**
   ```python
   # Good
   if "key" in my_dict:
       value = my_dict["key"]

   # Or use get()
   value = my_dict.get("key")
   ```

## Common Patterns

### 1. Grouping Items

```python
from collections import defaultdict

data = [("fruit", "apple"), ("veg", "carrot"), ("fruit", "banana")]
groups = defaultdict(list)
for category, item in data:
    groups[category].append(item)
```

### 2. Counting Frequencies

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(words)
```

### 3. Inverting a Dictionary

```python
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
```

### 4. Merging Dictionaries

```python
# Python 3.9+
merged = dict1 | dict2

# Python 3.5+
merged = {**dict1, **dict2}

# Any version
merged = dict1.copy()
merged.update(dict2)
```

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

## Performance Tips

1. Dictionary lookups are O(1) - very fast
2. Use dictionaries for membership testing over lists
3. Keys must be hashable (immutable)
4. Dictionary order is guaranteed (Python 3.7+)

## Common Pitfalls

1. **Modifying Dictionary During Iteration**
   ```python
   # Wrong
   for key in d:
       if condition:
           del d[key]  # RuntimeError!

   # Correct
   keys_to_delete = [k for k in d if condition]
   for key in keys_to_delete:
       del d[key]
   ```

2. **Using Mutable Keys**
   ```python
   # Wrong
   d = {[1, 2]: "value"}  # TypeError: unhashable type: 'list'

   # Correct
   d = {(1, 2): "value"}  # Tuples are hashable
   ```

---

**Program**: 09 of 500
**Difficulty**: ⭐⭐ Beginner/Intermediate
**Category**: Python Basics / Data Structures
**Estimated Time**: 45-60 minutes

[← Previous (08)](../08_tuples/) | [Back to Index](../../docs/INDEX.md) | [Next (10) →](../10_sets/)
