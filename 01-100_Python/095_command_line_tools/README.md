# Program 95: Command Line Tools

Building professional command-line applications using argparse and modern CLI patterns.

## Description

This program demonstrates creating robust command-line tools with argument parsing, subcommands, validation, help text, and user-friendly interfaces. Essential for building CLI utilities and automation scripts.

## Learning Objectives

- Master argparse module
- Implement subcommands
- Validate command-line arguments
- Create user-friendly interfaces
- Handle errors gracefully
- Follow CLI best practices

## Features

- **Argument Parsing**: Positional and optional arguments
- **Subcommands**: git-style command structure
- **Argument Types**: int, float, file, custom validators
- **Choices**: Restrict to specific values
- **Mutually Exclusive**: Either/or options
- **Argument Groups**: Organize related arguments
- **Help Generation**: Automatic --help
- **Configuration**: Combine CLI args with config files

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/095_command_line_tools
python src/main.py --help
python src/main.py command --option value
```

## Key Concepts

### Basic Argument Parser

```python
import argparse

parser = argparse.ArgumentParser(description='My CLI tool')

# Positional argument
parser.add_argument('input', help='Input file')

# Optional argument
parser.add_argument('--output', '-o', help='Output file')
parser.add_argument('--verbose', '-v', action='store_true')

args = parser.parse_args()
```

### Subcommands

```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# Add subcommand
add_parser = subparsers.add_parser('add', help='Add item')
add_parser.add_argument('name')

# Remove subcommand
remove_parser = subparsers.add_parser('remove', help='Remove item')
remove_parser.add_argument('name')

args = parser.parse_args()
if args.command == 'add':
    add_item(args.name)
```

### Argument Types

```python
# Built-in types
parser.add_argument('--count', type=int)
parser.add_argument('--ratio', type=float)
parser.add_argument('--file', type=argparse.FileType('r'))

# Custom validator
def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} must be positive")
    return ivalue

parser.add_argument('--size', type=positive_int)
```

### Choices

```python
parser.add_argument(
    '--format',
    choices=['json', 'xml', 'yaml'],
    default='json',
    help='Output format'
)
```

### Mutually Exclusive

```python
group = parser.add_mutually_exclusive_group()
group.add_argument('--json', action='store_true')
group.add_argument('--xml', action='store_true')
```

### Argument Groups

```python
input_group = parser.add_argument_group('input options')
input_group.add_argument('--input-file')
input_group.add_argument('--input-format')

output_group = parser.add_argument_group('output options')
output_group.add_argument('--output-file')
output_group.add_argument('--output-format')
```

## Best Practices

1. **Provide clear help text**: Users read --help first
2. **Use short and long options**: -v and --verbose
3. **Set sensible defaults**: Don't require everything
4. **Validate early**: Check arguments before processing
5. **Exit with proper codes**: 0 for success, non-zero for error
6. **Show progress**: For long operations
7. **Support --version**: Show program version
8. **Document examples**: Include usage examples in help

## Testing

```bash
# Run tests
pytest tests/

# Test CLI manually
python src/main.py --help
python src/main.py command --option value

# Test scenarios
# - Valid argument combinations
# - Invalid arguments (should error)
# - Missing required arguments
# - Subcommand dispatch
# - Help text generation
# - Error messages
```

## Navigation

- **Previous**: [Program 94 - Resource Management](../094_resource_management/README.md)
- **Next**: [Program 96 - Argument Parsing](../096_argument_parsing/README.md)
- **Home**: [Main README](../README.md)
