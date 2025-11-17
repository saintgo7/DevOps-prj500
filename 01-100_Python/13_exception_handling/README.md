# 13_exception_handling

## Description

Master Python exception handling with comprehensive demonstrations of try-except blocks, exception types, custom exceptions, exception chaining, and best practices for writing robust, error-resistant code. Exception handling is crucial for building production-ready applications.

This is Program #13 in the 500 Programs Collection.

## Learning Objectives

- Understand Python's exception hierarchy
- Use try-except-else-finally blocks
- Handle multiple exception types
- Raise and re-raise exceptions
- Create custom exception classes
- Implement exception chaining
- Use context managers with exceptions
- Apply exception handling best practices
- Use assertions for debugging

## Features

- Basic exception handling with try-except
- Multiple exception types handling
- Exception hierarchy and inheritance
- else and finally clauses
- Raising and re-raising exceptions
- Custom exception classes
- Exception chaining
- Context managers for cleanup
- Assertions for debugging
- Practical error handling patterns

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Basic Exception Handling

```python
# Basic try-except
try:
    result = 10 / 2
except ZeroDivisionError as e:
    print(f"Error: {e}")
    result = None

# Catching multiple exceptions separately
try:
    num = int("abc")
    result = 10 / num
except ValueError:
    print("Invalid number format")
except ZeroDivisionError:
    print("Cannot divide by zero")

# Catching multiple exceptions together
try:
    operation()
except (ValueError, TypeError) as e:
    print(f"Error: {type(e).__name__} - {e}")
```

### 2. Exception Hierarchy

```python
# Catch specific exceptions first
try:
    operation()
except ZeroDivisionError:
    print("Caught ZeroDivisionError")
except ArithmeticError:
    print("Caught ArithmeticError")  # Parent class
except Exception as e:
    print(f"Caught general exception: {e}")

# Common hierarchy:
# BaseException
#   └── Exception
#       ├── ArithmeticError
#       │   └── ZeroDivisionError
#       ├── LookupError
#       │   └── IndexError
#       │   └── KeyError
#       ├── ValueError
#       └── TypeError
```

### 3. else and finally Clauses

```python
# else - runs if no exception occurs
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error occurred")
else:
    print("No error - else executed")  # This runs
finally:
    print("Finally always executes")  # Always runs

# Common pattern with files
try:
    f = open("file.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("File not found")
else:
    print("File read successfully")
finally:
    if 'f' in locals() and not f.closed:
        f.close()
```

### 4. Raising Exceptions

```python
# Raise built-in exception
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return age

# Re-raising exceptions
try:
    process_data()
except ValueError:
    logging.error("Error processing data")
    raise  # Re-raises the same exception

# Raise with different exception
try:
    result = 10 / 0
except ZeroDivisionError:
    raise ValueError("Invalid operation") from None
```

### 5. Custom Exceptions

```python
# Basic custom exception
class InvalidEmailError(Exception):
    """Raised when email format is invalid."""
    pass

# Custom exception with attributes
class UserNotFoundError(Exception):
    """Raised when user is not found."""
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

# Exception hierarchy
class ValidationError(Exception):
    """Base validation error."""
    pass

class PasswordTooShortError(ValidationError):
    """Password is too short."""
    pass

class InvalidCharacterError(ValidationError):
    """Invalid characters in input."""
    pass

# Usage
def validate_email(email):
    if "@" not in email:
        raise InvalidEmailError(f"Invalid email: {email}")
    return email
```

### 6. Exception Chaining

```python
# Explicit chaining with 'from'
def process_data(data):
    try:
        num = int(data)
    except ValueError as e:
        raise TypeError("Data processing failed") from e

# The original exception is stored in __cause__

# Implicit chaining
try:
    num = int("abc")
except ValueError:
    raise TypeError("Cannot process invalid input")
# Previous exception stored in __context__

# Suppress chaining
try:
    operation()
except SomeError:
    raise DifferentError("New error") from None
```

### 7. Context Managers with Exceptions

```python
# Context manager automatically handles cleanup
try:
    with open("file.txt", "r") as f:
        content = f.read()
        # Exception here still closes file
except FileNotFoundError:
    print("File not found")
# File is automatically closed even if exception occurs

# Custom context manager
class ErrorLogger:
    def __enter__(self):
        self.errors = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.errors.append(f"{exc_type.__name__}: {exc_val}")
            return True  # Suppress exception

with ErrorLogger() as logger:
    raise ValueError("Test error")
# Exception is suppressed
```

### 8. Assertions

```python
def calculate_average(numbers):
    assert len(numbers) > 0, "List cannot be empty"
    assert all(isinstance(n, int) for n in numbers), "All must be integers"
    return sum(numbers) / len(numbers)

# Assertions for debugging (can be disabled with -O flag)
# Use exceptions for user input validation
```

## Best Practices

1. **Catch Specific Exceptions**
   ```python
   # Good
   try:
       operation()
   except ValueError:
       handle_value_error()

   # Bad - too broad
   try:
       operation()
   except Exception:
       pass  # Silent failure!
   ```

2. **Don't Use Bare except**
   ```python
   # Bad - catches everything including KeyboardInterrupt
   try:
       operation()
   except:
       pass

   # Good
   try:
       operation()
   except Exception as e:
       log.error(f"Error: {e}")
   ```

3. **Use finally for Cleanup**
   ```python
   # Good
   resource = acquire_resource()
   try:
       use_resource(resource)
   finally:
       release_resource(resource)
   ```

4. **Provide Helpful Error Messages**
   ```python
   # Good
   if age < 0:
       raise ValueError(f"Age must be positive, got {age}")

   # Less helpful
   if age < 0:
       raise ValueError("Invalid age")
   ```

5. **Don't Suppress Exceptions Silently**
   ```python
   # Bad
   try:
       critical_operation()
   except:
       pass  # Silent failure!

   # Good
   try:
       critical_operation()
   except Exception as e:
       logger.error(f"Critical operation failed: {e}")
       raise  # Re-raise if appropriate
   ```

6. **Use Custom Exceptions for Domain Logic**
   ```python
   # Good - clear intent
   class InsufficientFundsError(Exception):
       pass

   if balance < amount:
       raise InsufficientFundsError()

   # Less clear
   if balance < amount:
       raise ValueError("Not enough funds")
   ```

## Common Exception Types

| Exception | Use Case |
|-----------|----------|
| ValueError | Invalid value for operation |
| TypeError | Wrong type passed |
| KeyError | Dictionary key not found |
| IndexError | List index out of range |
| FileNotFoundError | File doesn't exist |
| ZeroDivisionError | Division by zero |
| AttributeError | Attribute doesn't exist |
| ImportError | Module cannot be imported |
| RuntimeError | General runtime error |
| NotImplementedError | Abstract method not implemented |

## Exception Handling Patterns

### 1. Retry Pattern

```python
def retry_operation(max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return risky_operation()
        except TemporaryError:
            if attempt == max_attempts - 1:
                raise
            time.sleep(1)
```

### 2. Fallback Pattern

```python
def get_config():
    try:
        return load_config("config.json")
    except FileNotFoundError:
        return default_config()
```

### 3. Error Collection

```python
errors = []
for item in items:
    try:
        process(item)
    except Exception as e:
        errors.append((item, str(e)))

if errors:
    raise Exception(f"Failed to process {len(errors)} items")
```

### 4. EAFP vs LBYL

```python
# EAFP (Easier to Ask Forgiveness than Permission) - Pythonic
try:
    value = dictionary[key]
except KeyError:
    value = default

# LBYL (Look Before You Leap) - Less Pythonic
if key in dictionary:
    value = dictionary[key]
else:
    value = default
```

## Testing

Run the comprehensive demonstration:

```bash
python src/main.py
```

## When to Use Exceptions

**DO use exceptions for:**
- Handling unexpected errors
- Input validation failures
- Resource unavailability
- Network/IO errors
- Programming errors that need context

**DON'T use exceptions for:**
- Normal control flow
- Expected conditions
- Performance-critical code paths
- Simple validation (use if statements)

## Common Pitfalls

1. **Catching Too Broadly**
2. **Silent Exception Suppression**
3. **Not Cleaning Up Resources**
4. **Confusing Exception Types**
5. **Using Exceptions for Control Flow**
6. **Not Providing Error Context**

---

**Program**: 13 of 500
**Difficulty**: ⭐⭐ Intermediate
**Category**: Python Basics / Error Handling
**Estimated Time**: 45-60 minutes

[← Previous (12)](../12_file_io/) | [Back to Index](../../docs/INDEX.md) | [Next (14) →](../14_classes_objects/)
