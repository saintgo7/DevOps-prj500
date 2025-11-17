# Program 27: Metaclasses

Master class creation and customization with metaclasses.

## Learning Objectives

- Understand metaclasses and the type() function
- Implement custom metaclasses with __new__ and __init__
- Use metaclasses for class validation and registration
- Create singleton patterns with metaclasses
- Automatically decorate methods with metaclasses

## Features

- type() as a metaclass
- Custom metaclass definition with __new__
- Metaclass __init__ and __call__
- Singleton pattern implementation
- Attribute validation
- Automatic method registration
- Class decoration
- Abstract method enforcement
- Class registry
- Metaclass inheritance

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Metaclass

```python
class SimpleMeta(type):
    def __new__(mcs, name, bases, dct):
        dct['added_by_metaclass'] = True
        return super().__new__(mcs, name, bases, dct)

class MyClass(metaclass=SimpleMeta):
    original_attr = "original"

print(MyClass.added_by_metaclass)  # True
```

### 2. Singleton Metaclass

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 3. Method Registration

```python
class RegistryMeta(type):
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)

        handlers = {}
        for key, value in dct.items():
            if key.startswith('handle_') and callable(value):
                event_name = key[7:]
                handlers[event_name] = value

        cls._handlers = handlers
        return cls
```

### 4. Class Registry

```python
class RegistryMeta(type):
    registry = {}

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        if name != 'Plugin':
            mcs.registry[name] = cls
        return cls
```

## Best Practices

1. **Use metaclasses sparingly** - They add complexity; consider decorators or __init_subclass__ first
2. **Document metaclass behavior** - Make it clear what the metaclass does
3. **Call super().__new__** - Always delegate to parent metaclass
4. **Metaclasses for frameworks** - Most useful in framework/library code
5. **Prefer __init_subclass__** - Simpler alternative for many use cases (Python 3.6+)

## Testing

```bash
pytest tests/
```

## Navigation

- Previous: [Program 26 - Context Managers](../26_context_managers/README.md)
- Next: [Program 28 - Descriptors](../28_descriptors/README.md)
- [Back to Main](../../README.md)
