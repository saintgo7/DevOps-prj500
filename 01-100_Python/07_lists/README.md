# 07_lists

## Description

Master Python lists with comprehensive demonstrations of list creation, manipulation, indexing, slicing, methods, comprehensions, and common patterns. Lists are one of the most fundamental and versatile data structures in Python, used extensively in everyday programming.

This is Program #7 in the 500 Programs Collection.

## Learning Objectives

- Create lists using various methods
- Master indexing and slicing operations
- Use built-in list methods effectively
- Perform common list operations (concatenation, repetition, membership)
- Write powerful list comprehensions
- Work with nested lists (2D arrays, matrices)
- Apply functional programming patterns (map, filter, zip)
- Understand list mutability and copying

## Features

- Multiple ways to create lists
- Comprehensive indexing and slicing demonstrations
- All built-in list methods (append, extend, insert, remove, pop, etc.)
- List operations (concatenation, repetition, membership testing)
- List comprehensions with conditions and nested loops
- Nested list operations and matrix manipulation
- Common patterns (filter, map, zip, enumerate, sorted)
- Performance considerations and best practices

## Usage

```bash
python src/main.py
```

## Example Output

```
============================================================
Program 07: Lists
============================================================

1. List Creation:
   empty: []
   numbers: [1, 2, 3, 4, 5]
   mixed_types: [1, 'hello', 3.14, True, None]
   nested: [[1, 2], [3, 4], [5, 6]]
   from_range: [1, 2, 3, 4, 5]
   repeated: [0, 0, 0, 0, 0]
   comprehension: [0, 2, 4, 6, 8]

2. Indexing and Slicing:
   first: 10
   last: 100
   slice_2_5: [30, 40, 50]
   reverse: [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

3. List Methods:
   append: [1, 2, 3, 4]
   extend: [1, 2, 3, 4, 5, 6]
   sort_asc: [1, 1, 2, 3, 4, 5, 6, 9]

============================================================
✅ Program completed!
============================================================
```

## Key Concepts

### 1. List Creation

```python
# Empty list
empty = []

# List with elements
numbers = [1, 2, 3, 4, 5]

# Mixed types
mixed = [1, "hello", 3.14, True, None]

# From range
range_list = list(range(1, 6))  # [1, 2, 3, 4, 5]

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
```

### 2. Indexing and Slicing

```python
numbers = [10, 20, 30, 40, 50]

# Positive indexing
first = numbers[0]    # 10
third = numbers[2]    # 30

# Negative indexing
last = numbers[-1]    # 50
second_last = numbers[-2]  # 40

# Slicing [start:stop:step]
numbers[1:4]    # [20, 30, 40]
numbers[:3]     # [10, 20, 30]
numbers[2:]     # [30, 40, 50]
numbers[::2]    # [10, 30, 50]
numbers[::-1]   # [50, 40, 30, 20, 10] - reverse
```

### 3. List Methods

```python
lst = [1, 2, 3]

# Adding elements
lst.append(4)           # [1, 2, 3, 4]
lst.extend([5, 6])      # [1, 2, 3, 4, 5, 6]
lst.insert(0, 0)        # [0, 1, 2, 3, 4, 5, 6]

# Removing elements
lst.remove(0)           # Remove first occurrence
popped = lst.pop()      # Remove and return last
popped_idx = lst.pop(0) # Remove and return at index

# Finding elements
index = lst.index(3)    # Find index of value
count = lst.count(2)    # Count occurrences

# Sorting and reversing
lst.sort()              # Sort in place
lst.reverse()           # Reverse in place

# Other
lst.clear()             # Remove all elements
copy = lst.copy()       # Shallow copy
```

### 4. List Operations

```python
# Concatenation
list1 + list2

# Repetition
[1, 2] * 3              # [1, 2, 1, 2, 1, 2]

# Membership
3 in [1, 2, 3]          # True
10 not in [1, 2, 3]     # True

# Length, min, max, sum
len(numbers)
min(numbers)
max(numbers)
sum(numbers)
```

### 5. List Comprehensions

```python
# Basic comprehension
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# With if-else
labels = ["even" if x % 2 == 0 else "odd" for x in range(10)]

# Nested comprehension
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]

# Flatten nested list
nested = [[1, 2, 3], [4, 5, 6]]
flat = [item for sublist in nested for item in sublist]
```

### 6. Common Patterns

```python
# Filter
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Map
doubled = list(map(lambda x: x * 2, numbers))

# Zip (combine lists)
names = ["Alice", "Bob"]
ages = [25, 30]
combined = list(zip(names, ages))  # [('Alice', 25), ('Bob', 30)]

# Enumerate (get index and value)
for index, value in enumerate(items):
    print(f"{index}: {value}")

# Sorted (non-mutating)
sorted_list = sorted(unsorted)
```

## Best Practices

1. **Use List Comprehensions for Transformations**
   ```python
   # Good
   squares = [x**2 for x in range(10)]

   # Less efficient
   squares = []
   for x in range(10):
       squares.append(x**2)
   ```

2. **Be Careful with Copies**
   ```python
   # Shallow copy
   copy1 = original.copy()
   copy2 = original[:]
   copy3 = list(original)

   # Deep copy (for nested lists)
   import copy
   deep_copy = copy.deepcopy(original)
   ```

3. **Use Built-in Functions**
   ```python
   # Good
   total = sum(numbers)
   maximum = max(numbers)

   # Less efficient
   total = 0
   for num in numbers:
       total += num
   ```

4. **Avoid Modifying Lists While Iterating**
   ```python
   # Bad
   for item in items:
       if condition:
           items.remove(item)  # Can skip elements!

   # Good
   items = [item for item in items if not condition]
   ```

5. **Use enumerate() Instead of range(len())**
   ```python
   # Good
   for index, value in enumerate(items):
       print(f"{index}: {value}")

   # Less Pythonic
   for i in range(len(items)):
       print(f"{i}: {items[i]}")
   ```

6. **Check for Empty Lists**
   ```python
   # Good
   if not my_list:
       print("List is empty")

   # Works but less Pythonic
   if len(my_list) == 0:
       print("List is empty")
   ```

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

## Performance Tips

1. **append() vs. extend()**: Use extend() for adding multiple items
2. **List comprehensions are faster** than loops with append()
3. **Use generators** for large datasets to save memory
4. **Avoid repeated concatenation** in loops (use join() for strings)
5. **in operator is O(n)**: Use sets for frequent membership testing

## Common Pitfalls

1. **Mutable Default Arguments**
   ```python
   # Wrong
   def add_item(item, lst=[]):
       lst.append(item)
       return lst

   # Correct
   def add_item(item, lst=None):
       if lst is None:
           lst = []
       lst.append(item)
       return lst
   ```

2. **Modifying List During Iteration**
3. **Shallow vs Deep Copy** confusion with nested lists

---

**Program**: 07 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics / Data Structures
**Estimated Time**: 45-60 minutes

[← Previous (06)](../06_functions/) | [Back to Index](../../docs/INDEX.md) | [Next (08) →](../08_tuples/)
