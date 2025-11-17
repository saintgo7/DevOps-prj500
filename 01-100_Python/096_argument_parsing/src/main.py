#!/usr/bin/env python3
"""
Program 96: Advanced Argument Parsing
Demonstrates complex argument parsing, subcommands, and configuration.
"""

import argparse
import sys
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


@dataclass
class Config:
    """Application configuration."""
    verbose: bool = False
    log_level: str = 'info'
    output_dir: Optional[Path] = None
    dry_run: bool = False


def demonstrate_complex_subcommands() -> None:
    """Demonstrate complex subcommand structure."""
    print("\n" + "=" * 60)
    print("COMPLEX SUBCOMMANDS")
    print("=" * 60)

    parser = argparse.ArgumentParser(
        prog='devtools',
        description='Development tools suite'
    )

    # Global options
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--config', type=Path,
                       help='Config file path')

    # Subparsers
    subparsers = parser.add_subparsers(dest='command', required=True,
                                      help='Available commands')

    # Database subcommand with sub-subcommands
    db_parser = subparsers.add_parser('db', help='Database operations')
    db_subparsers = db_parser.add_subparsers(dest='db_command', required=True)

    # db migrate
    migrate = db_subparsers.add_parser('migrate', help='Run migrations')
    migrate.add_argument('--target', help='Target version')

    # db backup
    backup = db_subparsers.add_parser('backup', help='Backup database')
    backup.add_argument('--compress', action='store_true', help='Compress backup')

    # Deploy subcommand
    deploy = subparsers.add_parser('deploy', help='Deploy application')
    deploy.add_argument('environment', choices=['dev', 'staging', 'prod'])
    deploy.add_argument('--force', action='store_true', help='Force deployment')

    print("\n1. Command structure:")
    print("   devtools db migrate [--target VERSION]")
    print("   devtools db backup [--compress]")
    print("   devtools deploy ENVIRONMENT [--force]")

    # Example parsing
    args = parser.parse_args(['db', 'migrate', '--target', 'v2.0'])

    print(f"\n2. Parsed nested command:")
    print(f"   command: {args.command}")
    print(f"   db_command: {args.db_command}")
    print(f"   target: {args.target}")


def demonstrate_argument_validation() -> None:
    """Demonstrate advanced argument validation."""
    print("\n" + "=" * 60)
    print("ADVANCED VALIDATION")
    print("=" * 60)

    def port_number(value: str) -> int:
        """Validate port number."""
        try:
            port = int(value)
            if not 1 <= port <= 65535:
                raise ValueError
            return port
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"'{value}' is not a valid port number (1-65535)"
            )

    def existing_directory(value: str) -> Path:
        """Validate directory exists."""
        path = Path(value)
        if not path.exists():
            raise argparse.ArgumentTypeError(f"Directory '{value}' does not exist")
        if not path.is_dir():
            raise argparse.ArgumentTypeError(f"'{value}' is not a directory")
        return path

    def percentage(value: str) -> float:
        """Validate percentage."""
        try:
            pct = float(value)
            if not 0 <= pct <= 100:
                raise ValueError
            return pct
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"'{value}' is not a valid percentage (0-100)"
            )

    parser = argparse.ArgumentParser(prog='validator')
    parser.add_argument('--port', type=port_number, help='Port number')
    parser.add_argument('--threshold', type=percentage, help='Threshold percentage')

    print("\n1. Custom validators:")
    print("   port_number: 1-65535")
    print("   existing_directory: Must exist")
    print("   percentage: 0-100")

    args = parser.parse_args(['--port', '8080', '--threshold', '75.5'])

    print(f"\n2. Validated values:")
    print(f"   port: {args.port}")
    print(f"   threshold: {args.threshold}%")


def demonstrate_config_integration() -> None:
    """Demonstrate config file integration."""
    print("\n" + "=" * 60)
    print("CONFIG FILE INTEGRATION")
    print("=" * 60)

    def load_config(path: Path) -> Dict[str, Any]:
        """Load configuration from file."""
        if path.suffix == '.json':
            with open(path) as f:
                return json.load(f)
        return {}

    parser = argparse.ArgumentParser(prog='configurable')

    # Add arguments
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--config', type=Path, help='Config file')

    print("\n1. Precedence order:")
    print("   1. Command-line arguments (highest)")
    print("   2. Config file")
    print("   3. Defaults (lowest)")

    print("\n2. Usage pattern:")
    print("   # Load defaults from config")
    print("   if args.config:")
    print("       defaults = load_config(args.config)")
    print("       parser.set_defaults(**defaults)")
    print("       args = parser.parse_args()")


def demonstrate_environment_variables() -> None:
    """Demonstrate environment variable fallback."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT VARIABLES")
    print("=" * 60)

    import os

    class EnvDefault(argparse.Action):
        """Custom action with environment variable fallback."""

        def __init__(self, envvar, required=True, default=None, **kwargs):
            if envvar in os.environ:
                default = os.environ[envvar]
                required = False
            super().__init__(default=default, required=required, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, values)

    parser = argparse.ArgumentParser(prog='envaware')

    print("\n1. Environment variable integration:")
    print("   --api-key: Falls back to API_KEY env var")
    print("   --database-url: Falls back to DATABASE_URL")

    print("\n2. Example:")
    print("   export API_KEY=secret123")
    print("   ./app.py  # Uses API_KEY from environment")
    print("   ./app.py --api-key override  # Overrides env var")


def demonstrate_argument_groups_advanced() -> None:
    """Demonstrate advanced argument grouping."""
    print("\n" + "=" * 60)
    print("ADVANCED ARGUMENT GROUPS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='grouped')

    # Required named group
    required = parser.add_argument_group('required arguments')
    required.add_argument('--username', required=True, help='Username')
    required.add_argument('--password', required=True, help='Password')

    # Optional named group
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--email', help='Email address')
    optional.add_argument('--phone', help='Phone number')

    # Mutually exclusive group
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--json', action='store_true', help='JSON output')
    output.add_argument('--xml', action='store_true', help='XML output')
    output.add_argument('--csv', action='store_true', help='CSV output')

    print("\n1. Argument organization:")
    print("   Required arguments:")
    print("     --username, --password")
    print("   Optional arguments:")
    print("     --email, --phone")
    print("   Output format (mutually exclusive):")
    print("     --json | --xml | --csv")


def demonstrate_variable_arguments() -> None:
    """Demonstrate handling variable arguments."""
    print("\n" + "=" * 60)
    print("VARIABLE ARGUMENTS")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='varargs')

    # Different nargs patterns
    parser.add_argument('command', help='Command to run')
    parser.add_argument('args', nargs='*', help='Command arguments')
    parser.add_argument('--include', nargs='+', help='Files to include')
    parser.add_argument('--exclude', nargs='*', help='Files to exclude')
    parser.add_argument('--pair', nargs=2, help='Key-value pair')

    print("\n1. Variable argument patterns:")
    print("   nargs='*': 0 or more")
    print("   nargs='+': 1 or more (required)")
    print("   nargs='?': 0 or 1")
    print("   nargs=N: Exactly N values")

    args = parser.parse_args([
        'run',
        'arg1', 'arg2',
        '--include', 'file1.txt', 'file2.txt',
        '--pair', 'key', 'value'
    ])

    print(f"\n2. Parsed values:")
    print(f"   command: {args.command}")
    print(f"   args: {args.args}")
    print(f"   include: {args.include}")
    print(f"   pair: {args.pair}")


def demonstrate_custom_actions() -> None:
    """Demonstrate custom actions."""
    print("\n" + "=" * 60)
    print("CUSTOM ACTIONS")
    print("=" * 60)

    class KeyValueAction(argparse.Action):
        """Parse key=value pairs."""

        def __call__(self, parser, namespace, values, option_string=None):
            result = getattr(namespace, self.dest) or {}
            for item in values:
                key, value = item.split('=', 1)
                result[key] = value
            setattr(namespace, self.dest, result)

    parser = argparse.ArgumentParser(prog='custom')

    parser.add_argument(
        '--define', '-D',
        action=KeyValueAction,
        nargs='+',
        help='Define variables (KEY=VALUE)'
    )

    print("\n1. Custom action: KeyValueAction")
    print("   Parses KEY=VALUE pairs into dict")

    args = parser.parse_args([
        '-D', 'host=localhost', 'port=8080', 'debug=true'
    ])

    print(f"\n2. Parsed definitions:")
    for key, value in (args.define or {}).items():
        print(f"   {key} = {value}")


def demonstrate_parent_parsers() -> None:
    """Demonstrate parent parsers for common arguments."""
    print("\n" + "=" * 60)
    print("PARENT PARSERS")
    print("=" * 60)

    # Parent parser with common arguments
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('-v', '--verbose', action='store_true')
    common.add_argument('--log-file', type=Path)

    # Child parsers inherit from parent
    parser1 = argparse.ArgumentParser(
        parents=[common],
        prog='cmd1',
        description='Command 1'
    )
    parser1.add_argument('--specific1', help='Specific to cmd1')

    parser2 = argparse.ArgumentParser(
        parents=[common],
        prog='cmd2',
        description='Command 2'
    )
    parser2.add_argument('--specific2', help='Specific to cmd2')

    print("\n1. Parent parser pattern:")
    print("   Define common arguments once")
    print("   Reuse across multiple parsers")

    print("\n2. Common arguments:")
    print("   -v, --verbose")
    print("   --log-file")

    args = parser1.parse_args(['--verbose', '--specific1', 'value'])

    print(f"\n3. Inherited and specific:")
    print(f"   verbose: {args.verbose}")
    print(f"   specific1: {args.specific1}")


def demonstrate_dynamic_choices() -> None:
    """Demonstrate dynamic choices."""
    print("\n" + "=" * 60)
    print("DYNAMIC CHOICES")
    print("=" * 60)

    def get_available_themes() -> List[str]:
        """Get available themes dynamically."""
        return ['light', 'dark', 'auto']

    def get_available_plugins() -> List[str]:
        """Get available plugins."""
        return ['linter', 'formatter', 'debugger']

    parser = argparse.ArgumentParser(prog='dynamic')

    parser.add_argument(
        '--theme',
        choices=get_available_themes(),
        default='auto',
        help='Select theme'
    )

    parser.add_argument(
        '--plugin',
        choices=get_available_plugins(),
        action='append',
        help='Enable plugin (can be used multiple times)'
    )

    print("\n1. Dynamic choices:")
    print("   Choices determined at runtime")
    print("   Can come from:")
    print("   - File system")
    print("   - Database")
    print("   - API calls")

    args = parser.parse_args(['--theme', 'dark', '--plugin', 'linter'])

    print(f"\n2. Selected options:")
    print(f"   theme: {args.theme}")
    print(f"   plugins: {args.plugin}")


def demonstrate_error_handling() -> None:
    """Demonstrate error handling."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)

    parser = argparse.ArgumentParser(prog='errorhandler')
    parser.add_argument('--count', type=int, required=True)

    print("\n1. Error handling strategies:")

    print("\n2. Default behavior:")
    print("   - Prints error to stderr")
    print("   - Shows usage")
    print("   - Exits with code 2")

    print("\n3. Custom error handling:")
    print("   try:")
    print("       args = parser.parse_args()")
    print("   except SystemExit:")
    print("       # Handle error")


def demonstrate_output_formatting() -> None:
    """Demonstrate help output formatting."""
    print("\n" + "=" * 60)
    print("OUTPUT FORMATTING")
    print("=" * 60)

    # With defaults shown
    parser = argparse.ArgumentParser(
        prog='formatter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--host', default='localhost',
                       help='Server host')
    parser.add_argument('--port', type=int, default=8000,
                       help='Server port')

    print("\n1. Formatter classes:")
    print("   ArgumentDefaultsHelpFormatter: Shows defaults")
    print("   RawDescriptionHelpFormatter: Preserves formatting")
    print("   RawTextHelpFormatter: Preserves all formatting")
    print("   MetavarTypeHelpFormatter: Shows type info")


def demonstrate_best_practices() -> None:
    """Demonstrate argument parsing best practices."""
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)

    print("\n1. Argument design:")
    print("   ✓ Use clear, descriptive names")
    print("   ✓ Provide both short and long forms")
    print("   ✓ Set sensible defaults")
    print("   ✓ Document all arguments")

    print("\n2. Validation:")
    print("   ✓ Validate early")
    print("   ✓ Provide clear error messages")
    print("   ✓ Use custom types for complex validation")

    print("\n3. Organization:")
    print("   ✓ Group related arguments")
    print("   ✓ Use subcommands for complex CLIs")
    print("   ✓ Use parent parsers for common args")

    print("\n4. User experience:")
    print("   ✓ Provide --help for all commands")
    print("   ✓ Show examples in help text")
    print("   ✓ Support --version")
    print("   ✓ Use --dry-run for destructive operations")


def main() -> None:
    """Main function demonstrating argument parsing."""
    print("=" * 60)
    print("PYTHON ADVANCED ARGUMENT PARSING")
    print("=" * 60)

    demonstrate_complex_subcommands()
    demonstrate_argument_validation()
    demonstrate_config_integration()
    demonstrate_environment_variables()
    demonstrate_argument_groups_advanced()
    demonstrate_variable_arguments()
    demonstrate_custom_actions()
    demonstrate_parent_parsers()
    demonstrate_dynamic_choices()
    demonstrate_error_handling()
    demonstrate_output_formatting()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All argument parsing demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
