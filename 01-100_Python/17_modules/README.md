# 17_modules

## Description

Master Python modules and imports - essential for code organization and reusability. Learn the standard library, import styles, module attributes, and key modules like collections, itertools, pathlib, functools, os, sys, and json.

This is Program #17 in the 500 Programs Collection.

## Learning Objectives

- Understand Python's module system
- Use different import styles effectively
- Work with standard library modules
- Master collections (defaultdict, Counter, namedtuple, deque)
- Use itertools for efficient iteration
- Work with pathlib for modern path handling
- Apply functools patterns (reduce, partial, lru_cache)
- Handle JSON and system operations

## Features

- Standard library demonstrations (math, random, datetime)
- Multiple import styles
- Module attributes (__name__, __file__, __doc__)
- collections module (defaultdict, Counter, namedtuple, deque)
- itertools module (combinations, permutations, chain, cycle)
- pathlib for object-oriented paths
- functools utilities (reduce, partial, lru_cache)
- os and sys module operations
- JSON handling

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Import Styles

```python
# Standard import
import math
result = math.sqrt(16)

# From import
from math import sqrt, pi
result = sqrt(16)

# Import with alias
import statistics as stats
mean = stats.mean([1, 2, 3, 4, 5])

# Multiple imports
from operator import add, mul, sub

# Import all (not recommended)
# from math import *
```

### 2. Standard Library Modules

```python
import math
import random
import datetime

# Math
math.pi
math.sqrt(16)
math.ceil(4.3)

# Random
random.randint(1, 100)
random.choice(["apple", "banana"])
random.random()

# Datetime
now = datetime.datetime.now()
formatted = now.strftime("%Y-%m-%d")
```

### 3. collections Module

```python
from collections import defaultdict, Counter, namedtuple, deque

# defaultdict - no KeyError
counts = defaultdict(int)
for word in words:
    counts[word] += 1

# Counter - count frequencies
counter = Counter(["apple", "banana", "apple"])
counter.most_common(2)

# namedtuple - lightweight class
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x, p.y)

# deque - double-ended queue
dq = deque([1, 2, 3])
dq.appendleft(0)
dq.append(4)
```

### 4. itertools Module

```python
from itertools import combinations, permutations, chain, cycle

# combinations
combos = combinations([1, 2, 3, 4], 2)
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

# permutations
perms = permutations([1, 2, 3], 2)
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

# chain - combine iterables
chained = chain([1, 2], [3, 4], [5, 6])

# cycle - infinite repeating
cycled = cycle([1, 2, 3])

# islice - slice iterator
from itertools import islice
limited = islice(cycled, 10)
```

### 5. pathlib Module

```python
from pathlib import Path

# Create path
path = Path("file.txt")

# Write and read
path.write_text("Hello!")
content = path.read_text()

# Path properties
path.name       # "file.txt"
path.stem       # "file"
path.suffix     # ".txt"
path.parent     # parent directory
path.absolute() # absolute path

# Create directories
Path("dir").mkdir(exist_ok=True)
Path("parent/child").mkdir(parents=True, exist_ok=True)

# Glob patterns
for file in Path(".").glob("*.txt"):
    print(file)
```

### 6. functools Module

```python
from functools import reduce, partial, lru_cache

# reduce
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)

# partial - create specialized functions
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)

# lru_cache - memoization
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 7. os and sys Modules

```python
import os
import sys

# os module
cwd = os.getcwd()
os.mkdir("temp_dir")
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.listdir(".")

# sys module
sys.version
sys.platform
sys.argv  # Command line arguments
sys.path  # Module search paths
sys.exit()
```

### 8. JSON Module

```python
import json

data = {"name": "Alice", "age": 25}

# To JSON string
json_str = json.dumps(data, indent=2)

# From JSON string
parsed = json.loads(json_str)

# To file
with open("data.json", "w") as f:
    json.dump(data, f)

# From file
with open("data.json", "r") as f:
    loaded = json.load(f)
```

## Best Practices

1. **Prefer Explicit Imports**
2. **Use Standard Library First**
3. **Group Imports (stdlib, third-party, local)**
4. **Use Aliases for Long Names**
5. **Avoid Wildcard Imports**

## Testing

```bash
python src/main.py
```

---

**Program**: 17 of 500
**Difficulty**: ⭐⭐ Intermediate
**Category**: Python Basics / Modules
**Estimated Time**: 60 minutes

[← Previous (16)](../16_polymorphism/) | [Back to Index](../../docs/INDEX.md) | [Next (18) →](../18_packages/)
