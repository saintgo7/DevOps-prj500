# Program 96: Advanced Argument Parsing

Advanced command-line argument parsing with complex validation and configuration.

## Description

This program explores advanced argparse features including nested subcommands, custom actions, configuration file integration, environment variable fallbacks, and sophisticated validation patterns.

## Learning Objectives

- Master complex argument patterns
- Implement custom validation
- Integrate configuration files
- Use environment variables
- Create parent parsers
- Build sophisticated CLIs

## Features

- **Nested Subcommands**: Multi-level command structure
- **Custom Actions**: Implement custom argument behavior
- **Config Integration**: Combine CLI with config files
- **Environment Fallback**: Use env vars when args missing
- **Parent Parsers**: Share common arguments
- **Dynamic Choices**: Generate choices at runtime
- **Argument Dependencies**: Conditional requirements
- **Advanced Validation**: Complex validation logic

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/096_argument_parsing
python src/main.py --help
python src/main.py --config config.json command --option value
```

## Key Concepts

### Nested Subcommands

```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# Database subcommand
db_parser = subparsers.add_parser('db')
db_subparsers = db_parser.add_subparsers(dest='db_command')

# db migrate
migrate = db_subparsers.add_parser('migrate')
migrate.add_argument('--target')

# db backup
backup = db_subparsers.add_parser('backup')
backup.add_argument('--compress', action='store_true')
```

### Custom Validation

```python
def port_number(value):
    """Validate port number (1-65535)."""
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError(
            f"{value} is not a valid port number"
        )
    return port

parser.add_argument('--port', type=port_number)
```

### Config File Integration

```python
import json

def load_config(path):
    with open(path) as f:
        return json.load(f)

# Load defaults from config
parser.add_argument('--config', type=Path)
args, remaining = parser.parse_known_args()

if args.config:
    defaults = load_config(args.config)
    parser.set_defaults(**defaults)
    args = parser.parse_args(remaining)
```

### Environment Variable Fallback

```python
import os

class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if envvar in os.environ:
            default = os.environ[envvar]
            required = False
        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

parser.add_argument(
    '--api-key',
    action=EnvDefault,
    envvar='API_KEY',
    help='API key (or set API_KEY env var)'
)
```

### Parent Parsers

```python
# Common arguments
common = argparse.ArgumentParser(add_help=False)
common.add_argument('--verbose', '-v', action='store_true')
common.add_argument('--log-file')

# Child parser inherits from parent
parser = argparse.ArgumentParser(parents=[common])
parser.add_argument('--specific-option')
```

### Custom Actions

```python
class KeyValueAction(argparse.Action):
    """Parse KEY=VALUE pairs into dict."""
    def __call__(self, parser, namespace, values, option_string=None):
        result = getattr(namespace, self.dest) or {}
        for item in values:
            key, value = item.split('=', 1)
            result[key] = value
        setattr(namespace, self.dest, result)

parser.add_argument(
    '--define', '-D',
    action=KeyValueAction,
    nargs='+',
    help='Define KEY=VALUE pairs'
)
```

## Best Practices

1. **Organize complex CLIs**: Use subcommands and groups
2. **Validate early and clearly**: Good error messages
3. **Support config files**: Don't require all args on CLI
4. **Use environment variables**: Good for secrets
5. **Share common args**: Use parent parsers
6. **Document well**: Clear help text and examples
7. **Test thoroughly**: Cover all argument combinations
8. **Version your CLI**: Add --version flag

## Testing

```bash
# Run tests
pytest tests/

# Test with different argument combinations
python src/main.py --help
python src/main.py db migrate --target v2.0
python src/main.py --config config.json command

# Test environment variables
export API_KEY=test123
python src/main.py --verbose

# Test scenarios
# - All subcommands
# - Config file loading
# - Environment fallback
# - Validation errors
# - Help text generation
```

## Navigation

- **Previous**: [Program 95 - Command Line Tools](../095_command_line_tools/README.md)
- **Next**: [Program 97 - Automation](../097_automation/README.md)
- **Home**: [Main README](../README.md)
