#!/usr/bin/env python3
"""
Program 01: Hello World
A simple program demonstrating basic Python output.

This is the foundational program that introduces:
- Basic Python syntax
- Print function
- String literals
- Program execution
- Docstrings
"""

from typing import Optional


def greet(name: Optional[str] = None) -> str:
    """
    Generate a greeting message.

    Args:
        name: Optional name to greet. If None, uses "World"

    Returns:
        A greeting string

    Examples:
        >>> greet()
        'Hello, World!'
        >>> greet("Python")
        'Hello, Python!'
    """
    if name is None:
        name = "World"
    return f"Hello, {name}!"


def main() -> None:
    """
    Main entry point for the program.
    Prints a greeting message to the console.
    """
    # Basic hello world
    print(greet())

    # Demonstrate with custom name
    print(greet("Python"))
    print(greet("Vibe Coder"))

    # Additional examples showing string formatting
    language = "Python"
    version = "3.11+"
    print(f"\nWelcome to {language} {version}!")
    print("=" * 40)
    print("🎉 Your first program is running! 🎉")
    print("=" * 40)


if __name__ == "__main__":
    main()
