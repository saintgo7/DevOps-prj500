# 18_packages

## Description

Master Python packages - directories containing modules that enable hierarchical code organization. Learn package structure, __init__.py files, relative imports, namespace packages, and packaging concepts for distributable Python projects.

This is Program #18 in the 500 Programs Collection.

## Learning Objectives

- Understand package concepts and structure
- Use __init__.py effectively
- Master relative vs absolute imports
- Create well-structured Python packages
- Work with namespace packages (PEP 420)
- Understand package discovery mechanisms
- Use __main__.py for executable packages
- Learn packaging metadata (setup.py, pyproject.toml)

## Features

- Package concepts and terminology
- __init__.py file usage and patterns
- Relative and absolute imports
- Common package structures
- Namespace packages
- Package discovery
- __main__ module pattern
- Package metadata (setup.py, pyproject.toml)
- Virtual environment concepts

## Usage

```bash
python src/main.py
```

## Key Concepts

### 1. Package Structure

```
mypackage/
    __init__.py          # Makes it a package
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
```

### 2. __init__.py File

```python
# mypackage/__init__.py

__version__ = '1.0.0'

# Import for convenience
from .module1 import function1
from .module2 import Class1

# Control * imports
__all__ = ['function1', 'Class1']

# Package initialization
print(f"Initializing package {__version__}")
```

### 3. Relative Imports

```python
# In mypackage/subpackage/module_c.py

# Relative imports
from . import sibling_module      # Current package
from .. import parent_module      # Parent package
from ..other_sub import something # Sibling package

# Absolute imports (preferred for clarity)
from mypackage.module_a import function_a
```

### 4. Package Structures

**Small Project:**
```
myproject/
    setup.py
    README.md
    mypackage/
        __init__.py
        core.py
        utils.py
        tests/
            test_core.py
```

**Medium Project:**
```
myproject/
    setup.py
    requirements.txt
    mypackage/
        __init__.py
        core/
            __init__.py
            module1.py
        utils/
            __init__.py
            helpers.py
        tests/
            test_core.py
    docs/
```

**Application:**
```
myapp/
    setup.py
    myapp/
        __init__.py
        __main__.py      # Entry point
        cli.py
        models/
        services/
        api/
        tests/
```

### 5. __main__ Module

```python
# mypackage/__main__.py

from .core import main_function

def main():
    """Entry point when run as: python -m mypackage"""
    result = main_function()
    print(result)

if __name__ == '__main__':
    main()
```

Usage: `python -m mypackage`

### 6. Package Metadata (setup.py)

```python
from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='1.0.0',
    description='A sample package',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ],
    python_requires='>=3.8',
)
```

### 7. Modern Packaging (pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "1.0.0"
description = "A sample package"
dependencies = [
    "requests>=2.25.0",
]

[project.optional-dependencies]
dev = ["pytest>=6.0"]
```

### 8. Virtual Environments

```bash
# Create virtual environment
python -m venv myenv

# Activate
source myenv/bin/activate  # Unix
myenv\Scripts\activate     # Windows

# Install packages
pip install package_name

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Deactivate
deactivate
```

## Best Practices

1. **Always Use Virtual Environments**
2. **Include __init__.py in Package Directories**
3. **Prefer Absolute Imports**
4. **Structure Projects Consistently**
5. **Document Dependencies**
6. **Use pyproject.toml (Modern Standard)**

## Common Package Patterns

### Import Convenience

```python
# mypackage/__init__.py
from .core import main_function
from .utils import helper_function

# Users can now do:
from mypackage import main_function
```

### Version Management

```python
# mypackage/__init__.py
__version__ = '1.0.0'

# Access version
import mypackage
print(mypackage.__version__)
```

## Testing

```bash
python src/main.py
```

---

**Program**: 18 of 500
**Difficulty**: ⭐⭐⭐ Intermediate/Advanced
**Category**: Python Basics / Packaging
**Estimated Time**: 60-75 minutes

[← Previous (17)](../17_modules/) | [Back to Index](../../docs/INDEX.md) | [Next (19) →](../19_decorators/)
