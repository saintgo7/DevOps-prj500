#!/usr/bin/env python3
"""Program 18: Packages - Master Python package structure and organization."""

import sys
from pathlib import Path
from typing import Any, List


def demonstrate_package_concept() -> dict[str, Any]:
    """Demonstrate basic package concepts."""
    # A package is a directory containing __init__.py
    # It allows hierarchical structuring of modules

    concepts = {
        "package": "Directory with __init__.py file",
        "module": "Single Python file (.py)",
        "subpackage": "Package inside another package",
        "namespace": "Package name creates namespace",
        "import_path": "Use dot notation to import: package.module",
    }

    # Example structure:
    example_structure = """
    mypackage/
        __init__.py
        module1.py
        module2.py
        subpackage/
            __init__.py
            module3.py
    """

    return {
        "concepts": concepts,
        "example_structure": example_structure.strip(),
    }


def demonstrate_init_file() -> dict[str, Any]:
    """Demonstrate __init__.py usage."""
    # __init__.py purposes:
    purposes = {
        "marker": "Marks directory as Python package",
        "initialization": "Run initialization code when package imported",
        "namespace": "Control what gets imported with 'from package import *'",
        "convenience": "Expose submodule contents at package level",
    }

    # Example __init__.py content
    init_example = """
# __init__.py

# Package version
__version__ = '1.0.0'

# Import submodules for convenience
from .module1 import function1
from .module2 import Class1

# Define __all__ for 'from package import *'
__all__ = ['function1', 'Class1', 'helper']

# Package-level initialization
print(f"Initializing package version {__version__}")
    """

    return {
        "purposes": purposes,
        "init_example": init_example.strip(),
    }


def demonstrate_relative_imports() -> dict[str, Any]:
    """Demonstrate relative vs absolute imports."""
    # Given structure:
    # myproject/
    #   mypackage/
    #     __init__.py
    #     module_a.py
    #     module_b.py
    #     subpackage/
    #       __init__.py
    #       module_c.py

    examples = {
        "absolute_import": "from mypackage.module_a import function",
        "relative_current": "from . import module_b  # Current package",
        "relative_parent": "from .. import module_a  # Parent package",
        "relative_sibling": "from ..subpackage import module_c  # Sibling",
        "explicit_relative": "from .module_b import Class",
    }

    # In module_c.py (subpackage/module_c.py):
    module_c_imports = """
# Absolute import
from mypackage.module_a import function_a

# Relative import - parent package
from ..module_a import function_a

# Relative import - current package
from . import other_module

# Relative import - sibling package
from ..other_subpackage import something
    """

    guidelines = {
        "prefer_absolute": "More readable, less error-prone",
        "use_relative": "For internal package structure",
        "avoid_mixing": "Be consistent within a package",
    }

    return {
        "import_examples": examples,
        "module_c_example": module_c_imports.strip(),
        "guidelines": guidelines,
    }


def demonstrate_package_structure() -> dict[str, Any]:
    """Demonstrate common package structures."""
    # Small project structure
    small_structure = """
myproject/
    setup.py
    README.md
    mypackage/
        __init__.py
        core.py
        utils.py
        tests/
            __init__.py
            test_core.py
            test_utils.py
    """

    # Medium project structure
    medium_structure = """
myproject/
    setup.py
    README.md
    requirements.txt
    mypackage/
        __init__.py
        core/
            __init__.py
            module1.py
            module2.py
        utils/
            __init__.py
            helpers.py
            validators.py
        tests/
            __init__.py
            test_core.py
            test_utils.py
    docs/
        conf.py
        index.rst
    """

    # Application structure
    app_structure = """
myapp/
    setup.py
    README.md
    requirements.txt
    myapp/
        __init__.py
        __main__.py  # Entry point for 'python -m myapp'
        cli.py
        config.py
        models/
            __init__.py
            user.py
            product.py
        services/
            __init__.py
            auth.py
            database.py
        api/
            __init__.py
            routes.py
            handlers.py
        tests/
            __init__.py
            test_models.py
            test_services.py
    """

    return {
        "small_project": small_structure.strip(),
        "medium_project": medium_structure.strip(),
        "application": app_structure.strip(),
    }


def demonstrate_namespace_packages() -> dict[str, Any]:
    """Demonstrate namespace packages (PEP 420)."""
    # Namespace packages (Python 3.3+)
    # Allow splitting a package across multiple directories

    concept = {
        "definition": "Package split across multiple directories",
        "no_init": "No __init__.py required",
        "use_case": "Plugin systems, shared namespaces",
    }

    example = """
# Structure 1 (in site-packages/company/)
company/
    project1/
        module_a.py

# Structure 2 (in another location)
company/
    project2/
        module_b.py

# Both can be imported as:
from company.project1 import module_a
from company.project2 import module_b
    """

    return {
        "concept": concept,
        "example": example.strip(),
        "note": "Useful for plugin architectures",
    }


def demonstrate_package_discovery() -> dict[str, Any]:
    """Demonstrate package and module discovery."""
    # Get package information
    import json

    # Module search path
    search_paths = sys.path[:5]  # First 5 paths

    # Find module location
    import_loc = json.__file__

    # Check if something is a package
    from pathlib import Path
    json_path = Path(json.__file__).parent
    is_package = (json_path / "__init__.py").exists()

    # List package contents
    json_contents = [
        item for item in dir(json)
        if not item.startswith('_')
    ][:10]

    return {
        "search_paths_count": len(sys.path),
        "first_3_paths": [str(Path(p).name) for p in search_paths[:3]],
        "json_location": str(Path(import_loc).parent.name),
        "json_is_package": is_package,
        "json_public_items": json_contents,
    }


def demonstrate_main_module() -> dict[str, Any]:
    """Demonstrate __main__ module pattern."""
    # __main__.py allows running package as script
    # python -m mypackage

    main_example = """
# mypackage/__main__.py

from .core import main_function
from .cli import parse_args

def main():
    \"\"\"Entry point when package run as script.\"\"\"
    args = parse_args()
    result = main_function(args)
    print(result)

if __name__ == '__main__':
    main()
    """

    # Alternative: Use __name__ == '__main__' in regular module
    module_example = """
# mypackage/core.py

def run_application():
    \"\"\"Main application logic.\"\"\"
    print("Running application")

if __name__ == '__main__':
    # This runs when: python mypackage/core.py
    run_application()
    """

    usage = {
        "with_main": "python -m mypackage",
        "direct_module": "python mypackage/core.py",
        "script": "python myscript.py",
    }

    return {
        "main_py_example": main_example.strip(),
        "module_example": module_example.strip(),
        "usage_patterns": usage,
    }


def demonstrate_package_metadata() -> dict[str, Any]:
    """Demonstrate package metadata and versioning."""
    # setup.py example
    setup_example = """
from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='1.0.0',
    description='A sample Python package',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/mypackage',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'pandas>=1.2.0',
    ],
    extras_require={
        'dev': ['pytest>=6.0', 'black>=21.0'],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
    """

    # pyproject.toml (modern approach)
    pyproject_example = """
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "1.0.0"
description = "A sample Python package"
authors = [{name = "Your Name", email = "your.email@example.com"}]
dependencies = [
    "requests>=2.25.0",
    "pandas>=1.2.0",
]

[project.optional-dependencies]
dev = ["pytest>=6.0", "black>=21.0"]
    """

    return {
        "setup_py": setup_example.strip(),
        "pyproject_toml": pyproject_example.strip(),
        "note": "pyproject.toml is the modern standard (PEP 518)",
    }


def demonstrate_virtual_environments() -> dict[str, Any]:
    """Demonstrate virtual environment concepts."""
    commands = {
        "create_venv": "python -m venv myenv",
        "activate_unix": "source myenv/bin/activate",
        "activate_windows": "myenv\\Scripts\\activate",
        "deactivate": "deactivate",
        "install_package": "pip install package_name",
        "freeze_deps": "pip freeze > requirements.txt",
        "install_deps": "pip install -r requirements.txt",
    }

    benefits = {
        "isolation": "Each project has its own dependencies",
        "reproducibility": "requirements.txt ensures same environment",
        "no_conflicts": "Different versions for different projects",
        "clean_system": "Don't pollute system Python",
    }

    return {
        "commands": commands,
        "benefits": benefits,
        "recommendation": "Always use virtual environments for projects",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 18: Packages")
    print("=" * 60)

    print("\n1. Package Concept:")
    concept = demonstrate_package_concept()
    for key, value in concept.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}:\n{value}\n")

    print("\n2. __init__.py File:")
    init_demo = demonstrate_init_file()
    for key, value in init_demo.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}:\n{value}\n")

    print("\n3. Relative Imports:")
    rel_imports = demonstrate_relative_imports()
    for key, value in rel_imports.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}:")
            print(f"      {value}\n")

    print("\n4. Package Structure:")
    structures = demonstrate_package_structure()
    for key, value in structures.items():
        print(f"   {key}:\n{value}\n")

    print("\n5. Namespace Packages:")
    namespace = demonstrate_namespace_packages()
    for key, value in namespace.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}:")
            if key != "note":
                print(f"{value}\n")
            else:
                print(f"      {value}")

    print("\n6. Package Discovery:")
    discovery = demonstrate_package_discovery()
    for key, value in discovery.items():
        print(f"   {key}: {value}")

    print("\n7. __main__ Module:")
    main_mod = demonstrate_main_module()
    for key, value in main_mod.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}:\n{value}\n")

    print("\n8. Package Metadata:")
    metadata = demonstrate_package_metadata()
    print(f"   Note: {metadata['note']}")

    print("\n9. Virtual Environments:")
    venv = demonstrate_virtual_environments()
    print(f"   Commands:")
    for k, v in list(venv['commands'].items())[:4]:
        print(f"      {k}: {v}")
    print(f"   Recommendation: {venv['recommendation']}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
