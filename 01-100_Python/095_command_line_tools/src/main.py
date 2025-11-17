#!/usr/bin/env python3
"""
Program 95: Command Line Tools
Demonstrates argparse, click, and command-line application patterns.
"""

import argparse
import sys
from typing import List, Optional
from pathlib import Path


def demonstrate_argparse_basics() -> None:
    """Demonstrate basic argparse usage."""
    print("\n" + "=" * 60)
    print("ARGPARSE BASICS")
    print("=" * 60)

    print("\n1. Creating parser:")
    parser = argparse.ArgumentParser(
        description='Sample CLI tool',
        prog='mytool'
    )

    print("   ArgumentParser created")

    print("\n2. Adding arguments:")
    print("   - Positional: parser.add_argument('name')")
    print("   - Optional: parser.add_argument('--flag')")
    print("   - Short form: parser.add_argument('-f', '--flag')")


def demonstrate_positional_arguments() -> None:
    """Demonstrate positional arguments."""
    print("\n" + "=" * 60)
    print("POSITIONAL ARGUMENTS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    # Add positional arguments
    parser.add_argument('input', help='Input file')
    parser.add_argument('output', help='Output file')

    print("\n1. Defined positional arguments:")
    print("   input: Input file")
    print("   output: Output file")

    # Parse test arguments
    args = parser.parse_args(['input.txt', 'output.txt'])

    print(f"\n2. Parsed arguments:")
    print(f"   input: {args.input}")
    print(f"   output: {args.output}")


def demonstrate_optional_arguments() -> None:
    """Demonstrate optional arguments."""
    print("\n" + "=" * 60)
    print("OPTIONAL ARGUMENTS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    # Add optional arguments
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('-o', '--output', type=str,
                       help='Output file')
    parser.add_argument('-n', '--number', type=int, default=10,
                       help='Number of iterations')

    print("\n1. Defined optional arguments:")
    print("   -v/--verbose: Boolean flag")
    print("   -o/--output: String option")
    print("   -n/--number: Integer with default")

    # Parse test arguments
    args = parser.parse_args(['-v', '--number', '42'])

    print(f"\n2. Parsed arguments:")
    print(f"   verbose: {args.verbose}")
    print(f"   output: {args.output}")
    print(f"   number: {args.number}")


def demonstrate_argument_types() -> None:
    """Demonstrate argument types."""
    print("\n" + "=" * 60)
    print("ARGUMENT TYPES")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    # Different types
    parser.add_argument('--count', type=int)
    parser.add_argument('--ratio', type=float)
    parser.add_argument('--file', type=argparse.FileType('r'))
    parser.add_argument('--path', type=Path)

    print("\n1. Available types:")
    print("   int: Integer values")
    print("   float: Floating point")
    print("   str: Strings (default)")
    print("   FileType: File objects")
    print("   Path: Path objects")
    print("   Custom: Any callable")

    # Example with int and float
    args = parser.parse_args(['--count', '42', '--ratio', '3.14'])

    print(f"\n2. Parsed values:")
    print(f"   count: {args.count} (type: {type(args.count).__name__})")
    print(f"   ratio: {args.ratio} (type: {type(args.ratio).__name__})")


def demonstrate_choices() -> None:
    """Demonstrate choices constraint."""
    print("\n" + "=" * 60)
    print("CHOICES CONSTRAINT")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    parser.add_argument('--format', choices=['json', 'xml', 'yaml'],
                       default='json',
                       help='Output format')

    print("\n1. Defined choices:")
    print("   --format: json, xml, yaml")

    args = parser.parse_args(['--format', 'json'])

    print(f"\n2. Selected format: {args.format}")
    print("   (Invalid choices will raise error)")


def demonstrate_nargs() -> None:
    """Demonstrate nargs for multiple values."""
    print("\n" + "=" * 60)
    print("NARGS (Multiple Values)")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    # Different nargs options
    parser.add_argument('files', nargs='+', help='One or more files')
    parser.add_argument('--exclude', nargs='*', help='Files to exclude')

    print("\n1. nargs options:")
    print("   ?: 0 or 1 value")
    print("   *: 0 or more values")
    print("   +: 1 or more values")
    print("   N: Exactly N values")

    args = parser.parse_args(['file1.txt', 'file2.txt', 'file3.txt',
                             '--exclude', 'temp.txt'])

    print(f"\n2. Parsed values:")
    print(f"   files: {args.files}")
    print(f"   exclude: {args.exclude}")


def demonstrate_actions() -> None:
    """Demonstrate different actions."""
    print("\n" + "=" * 60)
    print("ARGUMENT ACTIONS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    # Different actions
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose mode')
    parser.add_argument('-q', '--quiet', action='store_false',
                       dest='verbose',
                       help='Disable verbose mode')
    parser.add_argument('--count', action='count', default=0,
                       help='Increase count')
    parser.add_argument('--list', action='append',
                       help='Append to list')

    print("\n1. Action types:")
    print("   store_true: Set to True if present")
    print("   store_false: Set to False if present")
    print("   count: Count occurrences")
    print("   append: Append to list")

    args = parser.parse_args(['-v', '--count', '--count',
                             '--list', 'a', '--list', 'b'])

    print(f"\n2. Parsed values:")
    print(f"   verbose: {args.verbose}")
    print(f"   count: {args.count}")
    print(f"   list: {args.list}")


def demonstrate_subcommands() -> None:
    """Demonstrate subcommands (like git)."""
    print("\n" + "=" * 60)
    print("SUBCOMMANDS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='mytool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add subcommand
    add_parser = subparsers.add_parser('add', help='Add item')
    add_parser.add_argument('name', help='Item name')

    # Remove subcommand
    remove_parser = subparsers.add_parser('remove', help='Remove item')
    remove_parser.add_argument('name', help='Item name')

    # List subcommand
    list_parser = subparsers.add_parser('list', help='List items')

    print("\n1. Defined subcommands:")
    print("   add <name>: Add item")
    print("   remove <name>: Remove item")
    print("   list: List items")

    args = parser.parse_args(['add', 'item1'])

    print(f"\n2. Parsed command:")
    print(f"   command: {args.command}")
    print(f"   name: {args.name}")


def demonstrate_mutually_exclusive() -> None:
    """Demonstrate mutually exclusive groups."""
    print("\n" + "=" * 60)
    print("MUTUALLY EXCLUSIVE GROUPS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--json', action='store_true',
                      help='JSON output')
    group.add_argument('--xml', action='store_true',
                      help='XML output')

    print("\n1. Mutually exclusive options:")
    print("   --json and --xml cannot be used together")

    args = parser.parse_args(['--json'])

    print(f"\n2. Selected option:")
    print(f"   json: {args.json}")
    print(f"   xml: {args.xml}")


def demonstrate_argument_groups() -> None:
    """Demonstrate argument groups."""
    print("\n" + "=" * 60)
    print("ARGUMENT GROUPS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='example')

    # Input group
    input_group = parser.add_argument_group('input options')
    input_group.add_argument('--input', help='Input file')
    input_group.add_argument('--format', help='Input format')

    # Output group
    output_group = parser.add_argument_group('output options')
    output_group.add_argument('--output', help='Output file')
    output_group.add_argument('--compress', action='store_true',
                            help='Compress output')

    print("\n1. Organized into groups:")
    print("   Input options:")
    print("     --input, --format")
    print("   Output options:")
    print("     --output, --compress")


def demonstrate_custom_validation() -> None:
    """Demonstrate custom argument validation."""
    print("\n" + "=" * 60)
    print("CUSTOM VALIDATION")
    print("=" * 60)

    def positive_int(value):
        """Validate positive integer."""
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} is not positive")
        return ivalue

    def existing_file(value):
        """Validate file exists."""
        path = Path(value)
        if not path.exists():
            raise argparse.ArgumentTypeError(f"{value} does not exist")
        return path

    parser = argparse.ArgumentParser(prog='example')
    parser.add_argument('--count', type=positive_int,
                       help='Positive integer')

    print("\n1. Custom validators:")
    print("   positive_int: Ensures value > 0")
    print("   existing_file: Ensures file exists")

    args = parser.parse_args(['--count', '42'])

    print(f"\n2. Validated value: {args.count}")


def demonstrate_help_formatting() -> None:
    """Demonstrate help text formatting."""
    print("\n" + "=" * 60)
    print("HELP FORMATTING")
    print("=" * 60)

    parser = argparse.ArgumentParser(
        prog='mytool',
        description='A comprehensive CLI tool',
        epilog='Thank you for using mytool!',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input', help='Input file path')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output\n(shows detailed information)')

    print("\n1. Help components:")
    print("   - Program name (prog)")
    print("   - Description")
    print("   - Usage pattern")
    print("   - Argument help")
    print("   - Epilog")

    print("\n2. Formatter classes:")
    print("   - ArgumentDefaultsHelpFormatter")
    print("   - RawDescriptionHelpFormatter")
    print("   - RawTextHelpFormatter")
    print("   - MetavarTypeHelpFormatter")


def demonstrate_config_file_pattern() -> None:
    """Demonstrate config file pattern."""
    print("\n" + "=" * 60)
    print("CONFIG FILE PATTERN")
    print("=" * 60)

    print("\n1. Common pattern:")
    print("   - Read defaults from config file")
    print("   - Override with command-line args")

    print("\n2. Implementation:")
    print("   defaults = load_config('config.yaml')")
    print("   parser.set_defaults(**defaults)")
    print("   args = parser.parse_args()")


def demonstrate_best_practices() -> None:
    """Demonstrate CLI best practices."""
    print("\n" + "=" * 60)
    print("CLI BEST PRACTICES")
    print("=" * 60)

    print("\n1. Design principles:")
    print("   ✓ Clear, concise help text")
    print("   ✓ Sensible defaults")
    print("   ✓ Validate inputs early")
    print("   ✓ Provide good error messages")

    print("\n2. Argument naming:")
    print("   ✓ Use lowercase with hyphens")
    print("   ✓ Provide both short and long forms")
    print("   ✓ Be consistent")

    print("\n3. User experience:")
    print("   ✓ Show progress for long operations")
    print("   ✓ Confirm destructive operations")
    print("   ✓ Support --version")
    print("   ✓ Return appropriate exit codes")

    print("\n4. Error handling:")
    print("   ✓ Catch exceptions")
    print("   ✓ Show helpful error messages")
    print("   ✓ Exit with non-zero code on error")


def demonstrate_complete_cli() -> None:
    """Demonstrate complete CLI application."""
    print("\n" + "=" * 60)
    print("COMPLETE CLI APPLICATION")
    print("=" * 60)

    parser = argparse.ArgumentParser(
        prog='filetools',
        description='File processing tools',
        epilog='For more information, visit: https://example.com'
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Process command
    process = subparsers.add_parser('process', help='Process files')
    process.add_argument('files', nargs='+', help='Files to process')
    process.add_argument('-o', '--output', help='Output directory')
    process.add_argument('-f', '--format', choices=['json', 'xml'],
                        default='json', help='Output format')
    process.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')

    # Validate command
    validate = subparsers.add_parser('validate', help='Validate files')
    validate.add_argument('files', nargs='+', help='Files to validate')
    validate.add_argument('--strict', action='store_true',
                         help='Strict validation')

    print("\n1. Application structure:")
    print("   - Version flag")
    print("   - Subcommands (process, validate)")
    print("   - Required and optional arguments")
    print("   - Choices and defaults")

    # Example usage
    args = parser.parse_args(['process', 'file1.txt', 'file2.txt',
                             '--format', 'json', '-v'])

    print(f"\n2. Example execution:")
    print(f"   Command: {args.command}")
    print(f"   Files: {args.files}")
    print(f"   Format: {args.format}")
    print(f"   Verbose: {args.verbose}")


def main() -> None:
    """Main function demonstrating command-line tools."""
    print("=" * 60)
    print("PYTHON COMMAND-LINE TOOLS")
    print("=" * 60)

    demonstrate_argparse_basics()
    demonstrate_positional_arguments()
    demonstrate_optional_arguments()
    demonstrate_argument_types()
    demonstrate_choices()
    demonstrate_nargs()
    demonstrate_actions()
    demonstrate_subcommands()
    demonstrate_mutually_exclusive()
    demonstrate_argument_groups()
    demonstrate_custom_validation()
    demonstrate_help_formatting()
    demonstrate_config_file_pattern()
    demonstrate_complete_cli()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All CLI demonstrations completed!")
    print("=" * 60)
    print("\nNote: For more advanced CLI tools, consider:")
    print("- Click: More Pythonic API")
    print("- Typer: Modern, type-hint based")
    print("- Fire: Automatically generate CLIs")


if __name__ == "__main__":
    main()
