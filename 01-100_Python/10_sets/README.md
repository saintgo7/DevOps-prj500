# 10_sets

## Description

Master Python sets - unordered collections of unique elements that provide fast membership testing and mathematical set operations. This program covers set creation, operations, methods, and demonstrates practical use cases like removing duplicates and finding common elements.

This is Program #10 in the 500 Programs Collection.

## Learning Objectives

- Create sets using various methods
- Perform mathematical set operations (union, intersection, difference)
- Use set methods effectively
- Understand set comparisons (subset, superset, disjoint)
- Write set comprehensions
- Work with frozensets (immutable sets)
- Apply sets for practical problem-solving
- Understand set performance characteristics

## Features

- Multiple set creation methods
- Complete set operations (union, intersection, difference, symmetric difference)
- All set methods (add, remove, discard, pop, etc.)
- Set comparisons (subset, superset, disjoint, equality)
- Set comprehensions
- frozenset for immutable sets
- Practical use cases (deduplication, membership testing, finding commons)
- Common patterns and idioms

## Usage

```bash
python src/main.py
```

## Example Output

```
============================================================
Program 10: Sets
============================================================

1. Set Creation:
   empty: set()
   numbers: {1, 2, 3, 4, 5}
   from_list_deduped: {1, 2, 3, 4, 5}
   from_string: {'h', 'e', 'l', 'o'}

2. Set Methods:
   add: {1, 2, 3, 4}
   update: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
   remove: {1, 2, 4, 5}

3. Set Operations:
   set_a: {1, 2, 3, 4, 5}
   set_b: {4, 5, 6, 7, 8}
   union: {1, 2, 3, 4, 5, 6, 7, 8}
   intersection: {4, 5}
   difference_a_b: {1, 2, 3}
   symmetric_difference: {1, 2, 3, 6, 7, 8}

============================================================
✅ Program completed!
============================================================
```

## Key Concepts

### 1. Set Creation

```python
# Empty set (note: {} creates empty dict, not set!)
empty = set()

# Set with elements
numbers = {1, 2, 3, 4, 5}

# From list (automatically removes duplicates)
unique = set([1, 2, 2, 3, 3, 3, 4])  # {1, 2, 3, 4}

# From string (unique characters)
chars = set("hello")  # {'h', 'e', 'l', 'o'}

# Set comprehension
squares = {x**2 for x in range(6)}
```

### 2. Set Methods

```python
s = {1, 2, 3}

# Add single element
s.add(4)  # {1, 2, 3, 4}

# Update with multiple elements
s.update([5, 6, 7])
s.update({8, 9}, [10, 11])

# Remove (raises KeyError if not found)
s.remove(3)

# Discard (no error if not found)
s.discard(99)  # No error

# Pop (removes and returns arbitrary element)
element = s.pop()

# Clear all elements
s.clear()

# Copy
copy = s.copy()
```

### 3. Mathematical Set Operations

```python
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Union (elements in either set)
union = set_a | set_b
union = set_a.union(set_b)

# Intersection (elements in both sets)
intersection = set_a & set_b
intersection = set_a.intersection(set_b)

# Difference (elements in first but not second)
difference = set_a - set_b
difference = set_a.difference(set_b)

# Symmetric difference (elements in either but not both)
sym_diff = set_a ^ set_b
sym_diff = set_a.symmetric_difference(set_b)
```

### 4. Set Comparisons

```python
set_a = {1, 2, 3}
set_b = {1, 2, 3, 4, 5}
set_c = {1, 2, 3}
set_d = {6, 7, 8}

# Subset
set_a <= set_b  # True
set_a.issubset(set_b)  # True

# Proper subset (subset but not equal)
set_a < set_b  # True

# Superset
set_b >= set_a  # True
set_b.issuperset(set_a)  # True

# Proper superset
set_b > set_a  # True

# Equality
set_a == set_c  # True

# Disjoint (no common elements)
set_a.isdisjoint(set_d)  # True
```

### 5. Set Comprehensions

```python
# Basic comprehension
squares = {x**2 for x in range(10)}

# With condition
even_squares = {x**2 for x in range(10) if x % 2 == 0}

# From string
vowels = {char.lower() for char in "Hello World" if char.lower() in "aeiou"}

# Set operations in comprehension
multiples_3 = {x for x in range(1, 31) if x % 3 == 0}
multiples_5 = {x for x in range(1, 31) if x % 5 == 0}
multiples_3_or_5 = multiples_3 | multiples_5
```

### 6. Frozenset (Immutable Set)

```python
# Create frozenset
frozen = frozenset([1, 2, 3, 4, 5])

# Can be used as dictionary key
dict_with_frozen = {frozen: "value"}

# Can be element in another set
set_of_frozen = {frozenset([1, 2]), frozenset([3, 4])}

# Supports all query operations
frozen_a = frozenset([1, 2, 3])
frozen_b = frozenset([3, 4, 5])
union = frozen_a | frozen_b

# Cannot be modified (no add, remove, etc.)
```

## Best Practices

1. **Use Sets for Membership Testing**
   ```python
   # Fast O(1) lookup
   allowed_users = {"alice", "bob", "charlie"}
   if username in allowed_users:  # Very fast
       pass

   # Slow O(n) lookup with list
   allowed_list = ["alice", "bob", "charlie"]
   if username in allowed_list:  # Slower
       pass
   ```

2. **Remove Duplicates**
   ```python
   # Quick way to remove duplicates
   numbers = [1, 2, 2, 3, 3, 3, 4, 5]
   unique = list(set(numbers))
   ```

3. **Find Common Elements**
   ```python
   list1 = [1, 2, 3, 4, 5]
   list2 = [4, 5, 6, 7, 8]
   common = list(set(list1) & set(list2))  # [4, 5]
   ```

4. **Find Unique Elements**
   ```python
   unique_to_list1 = list(set(list1) - set(list2))
   unique_to_list2 = list(set(list2) - set(list1))
   all_unique = list(set(list1) ^ set(list2))
   ```

5. **Use Frozenset for Dictionary Keys**
   ```python
   # Frozensets are hashable
   game_state = {frozenset([1, 2, 3]): "player1"}

   # Regular sets are not hashable
   # bad = {set([1, 2, 3]): "player1"}  # TypeError!
   ```

6. **Set Comprehensions for Filtering**
   ```python
   # Efficient unique filtering
   even_numbers = {x for x in range(100) if x % 2 == 0}
   ```

## Practical Use Cases

### 1. Remove Duplicates (Preserving Order in Python 3.7+)

```python
def remove_duplicates_ordered(items):
    """Remove duplicates while preserving order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

### 2. Find Common Elements

```python
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
common = list(set(list1) & set(list2))
```

### 3. Count Unique Words

```python
text = "hello world hello python world"
unique_words = set(text.split())
count = len(unique_words)
```

### 4. Validate All Required Items Present

```python
required = {"username", "password", "email"}
provided = {"username", "password"}
missing = required - provided  # {"email"}
```

### 5. Find Duplicates

```python
def find_duplicates(items):
    """Find duplicate items in list."""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return duplicates
```

## Performance Characteristics

| Operation | Time Complexity |
|-----------|----------------|
| Add | O(1) |
| Remove | O(1) |
| Membership test | O(1) |
| Union | O(len(s) + len(t)) |
| Intersection | O(min(len(s), len(t))) |
| Difference | O(len(s)) |
| Subset test | O(len(s)) |

## Sets vs Lists vs Tuples

| Feature | Set | List | Tuple |
|---------|-----|------|-------|
| Ordered | No (insertion order in 3.7+) | Yes | Yes |
| Duplicates | No | Yes | Yes |
| Mutable | Yes | Yes | No |
| Indexing | No | Yes | Yes |
| Membership | O(1) | O(n) | O(n) |
| Use Case | Uniqueness, membership | Sequences | Immutable sequences |

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

## Common Patterns

### Set Operations on Multiple Collections

```python
sets = [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]
intersection_all = set.intersection(*sets)  # {3}
union_all = set.union(*sets)  # {1, 2, 3, 4, 5}
```

### Filtering with Sets

```python
valid_ids = {1, 3, 5, 7, 9}
data = [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]
filtered = [item for item in data if item["id"] in valid_ids]
```

---

**Program**: 10 of 500
**Difficulty**: ⭐ Beginner
**Category**: Python Basics / Data Structures
**Estimated Time**: 30-45 minutes

[← Previous (09)](../09_dictionaries/) | [Back to Index](../../docs/INDEX.md) | [Next (11) →](../11_string_methods/)
