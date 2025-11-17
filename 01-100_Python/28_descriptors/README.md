# Program 28: Descriptors

Master attribute access control with the descriptor protocol.

## Learning Objectives

- Understand the descriptor protocol (__get__, __set__, __delete__)
- Differentiate data vs non-data descriptors
- Implement validated and typed attributes
- Create lazy properties with descriptors
- Understand how property(), classmethod(), and staticmethod() work

## Features

- Basic descriptor protocol
- Data vs non-data descriptors
- Validated attributes
- Type-checked attributes
- Lazy property evaluation
- Property() implementation
- Method descriptors
- Classmethod and staticmethod descriptors
- WeakKeyDictionary for storage
- Instance __dict__ storage strategy

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Descriptor

```python
class Descriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return f"Getting value"

    def __set__(self, instance, value):
        print(f"Setting to {value}")

    def __delete__(self, instance):
        print("Deleting")
```

### 2. Validated Attribute

```python
class ValidatedString:
    def __init__(self, min_length, max_length):
        self.min_length = min_length
        self.max_length = max_length
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.data.get(instance, "")

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Must be string")
        if len(value) < self.min_length:
            raise ValueError(f"Too short (min {self.min_length})")
        self.data[instance] = value
```

### 3. Lazy Property

```python
class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if instance not in self.data:
            self.data[instance] = self.function(instance)
        return self.data[instance]
```

## Best Practices

1. **Use WeakKeyDictionary** - Prevents memory leaks in descriptors
2. **Check for None instance** - Handle class-level access
3. **Data descriptors for validation** - Override instance __dict__
4. **Non-data for lazy computation** - Can be overridden by instance
5. **Property for simple cases** - Descriptor protocol for complex logic

## Testing

```bash
pytest tests/
```

## Navigation

- Previous: [Program 27 - Metaclasses](../27_metaclasses/README.md)
- Next: [Program 29 - Type Hints](../29_type_hints/README.md)
- [Back to Main](../../README.md)
