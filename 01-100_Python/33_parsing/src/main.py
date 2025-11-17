#!/usr/bin/env python3
"""Program 33: Parsing - Master text parsing techniques and AST manipulation."""

import ast
import json
import csv
import io
from typing import Any, List, Dict
from urllib.parse import urlparse, parse_qs


def demonstrate_string_parsing() -> dict[str, Any]:
    """Demonstrate basic string parsing techniques."""

    # Parse CSV-like data
    data = "Alice,30,Engineer\nBob,25,Designer\nCharlie,35,Manager"
    rows = []
    for line in data.split('\n'):
        rows.append(line.split(','))

    # Parse key-value pairs
    config = "name=MyApp;version=1.0;debug=true"
    settings = {}
    for item in config.split(';'):
        key, value = item.split('=')
        settings[key] = value

    # Parse structured text
    log_line = "[2024-01-15 10:30:45] ERROR: Connection failed"
    parts = log_line.split('] ')
    timestamp = parts[0][1:]  # Remove [
    level_message = parts[1].split(': ')
    level = level_message[0]
    message = level_message[1]

    return {
        "csv_rows": rows,
        "settings": settings,
        "log_parsed": {"timestamp": timestamp, "level": level, "message": message},
        "note": "Basic parsing with split() and string manipulation",
    }


def demonstrate_json_parsing() -> dict[str, Any]:
    """Demonstrate JSON parsing."""

    # Parse JSON string
    json_str = '{"name": "Alice", "age": 30, "skills": ["Python", "JavaScript"]}'
    data = json.loads(json_str)

    # Parse nested JSON
    nested_json = '''
    {
        "user": {
            "id": 123,
            "profile": {
                "name": "Bob",
                "email": "bob@example.com"
            }
        }
    }
    '''
    nested_data = json.loads(nested_json)

    # Convert to JSON
    python_obj = {"status": "success", "count": 42}
    json_output = json.dumps(python_obj, indent=2)

    return {
        "parsed_name": data["name"],
        "parsed_skills": data["skills"],
        "nested_email": nested_data["user"]["profile"]["email"],
        "json_output_len": len(json_output),
        "note": "json.loads() parses, json.dumps() serializes",
    }


def demonstrate_csv_parsing() -> dict[str, Any]:
    """Demonstrate CSV parsing with csv module."""

    # Parse CSV
    csv_data = """name,age,city
Alice,30,NYC
Bob,25,LA
Charlie,35,Chicago"""

    # Using csv.reader
    reader = csv.reader(io.StringIO(csv_data))
    rows = list(reader)

    # Using csv.DictReader
    dict_reader = csv.DictReader(io.StringIO(csv_data))
    dict_rows = list(dict_reader)

    # Write CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Product', 'Price'])
    writer.writerow(['Widget', '19.99'])
    writer.writerow(['Gadget', '29.99'])
    csv_output = output.getvalue()

    return {
        "rows": rows[:2],
        "dict_rows": dict_rows[:2],
        "csv_output_lines": len(csv_output.split('\n')),
        "note": "csv module for parsing and writing CSV files",
    }


def demonstrate_url_parsing() -> dict[str, Any]:
    """Demonstrate URL parsing."""

    url = "https://example.com:8080/path/to/page?name=Alice&age=30&tags=a&tags=b#section"

    # Parse URL
    parsed = urlparse(url)

    # Parse query parameters
    params = parse_qs(parsed.query)

    return {
        "scheme": parsed.scheme,
        "hostname": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query_params": params,
        "fragment": parsed.fragment,
        "note": "urlparse breaks URL into components",
    }


def demonstrate_ast_parsing() -> dict[str, Any]:
    """Demonstrate Python AST parsing."""

    # Parse Python code
    code = """
def greet(name):
    return f"Hello, {name}!"

x = 42
y = x + 10
"""

    # Parse to AST
    tree = ast.parse(code)

    # Extract function names
    functions = []
    assignments = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments.append(target.id)

    return {
        "functions": functions,
        "assignments": assignments,
        "ast_type": type(tree).__name__,
        "note": "ast module parses Python source code",
    }


def demonstrate_ast_modification() -> dict[str, Any]:
    """Demonstrate AST modification."""

    # Original code
    code = "result = 5 + 3"
    tree = ast.parse(code)

    # Modify AST - change 5 to 10
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and node.value == 5:
            node.value = 10

    # Compile and execute modified AST
    compiled = compile(tree, filename="<ast>", mode="exec")
    namespace = {}
    exec(compiled, namespace)

    return {
        "original_code": code,
        "modified_result": namespace.get("result"),
        "note": "AST can be modified before compilation",
    }


def demonstrate_expression_parser() -> dict[str, Any]:
    """Demonstrate simple expression parser."""

    def evaluate_expr(expr: str) -> float:
        """Safely evaluate mathematical expression using AST."""
        tree = ast.parse(expr, mode='eval')

        # Only allow safe operations
        def eval_node(node):
            if isinstance(node, ast.Expression):
                return eval_node(node.body)
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                elif isinstance(node.op, ast.Sub):
                    return left - right
                elif isinstance(node.op, ast.Mult):
                    return left * right
                elif isinstance(node.op, ast.Div):
                    return left / right
            raise ValueError("Unsupported operation")

        return eval_node(tree)

    results = [
        evaluate_expr("5 + 3"),
        evaluate_expr("10 * 2"),
        evaluate_expr("20 / 4"),
    ]

    return {
        "expression_results": results,
        "note": "AST enables safe expression evaluation",
    }


def demonstrate_custom_parser() -> dict[str, Any]:
    """Demonstrate custom parser for simple format."""

    def parse_config(text: str) -> dict:
        """Parse simple INI-like configuration."""
        config = {}
        current_section = "default"
        config[current_section] = {}

        for line in text.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                config[current_section][key.strip()] = value.strip()

        return config

    config_text = """
# Database configuration
[database]
host = localhost
port = 5432
name = mydb

[server]
port = 8080
debug = true
"""

    parsed_config = parse_config(config_text)

    return {
        "sections": list(parsed_config.keys()),
        "db_host": parsed_config["database"]["host"],
        "server_port": parsed_config["server"]["port"],
        "note": "Custom parsers for domain-specific formats",
    }


def demonstrate_tokenization() -> dict[str, Any]:
    """Demonstrate tokenization."""

    def tokenize(text: str) -> List[tuple]:
        """Simple tokenizer for math expressions."""
        import re
        token_pattern = r'\d+|\+|\-|\*|\/|\(|\)'
        tokens = []

        for match in re.finditer(token_pattern, text):
            value = match.group()
            if value.isdigit():
                tokens.append(('NUMBER', int(value)))
            else:
                tokens.append(('OPERATOR', value))

        return tokens

    expression = "10 + 20 * 3"
    tokens = tokenize(expression)

    return {
        "expression": expression,
        "tokens": tokens,
        "token_count": len(tokens),
        "note": "Tokenization breaks text into meaningful units",
    }


def demonstrate_validation_parsing() -> dict[str, Any]:
    """Demonstrate parsing with validation."""

    def parse_person(data: str) -> dict:
        """Parse and validate person data."""
        parts = data.split(',')

        if len(parts) != 3:
            raise ValueError("Expected format: name,age,email")

        name, age_str, email = [p.strip() for p in parts]

        # Validate
        if not name:
            raise ValueError("Name cannot be empty")

        try:
            age = int(age_str)
            if age < 0 or age > 150:
                raise ValueError("Invalid age")
        except ValueError:
            raise ValueError("Age must be a number")

        if '@' not in email:
            raise ValueError("Invalid email")

        return {"name": name, "age": age, "email": email}

    valid = parse_person("Alice, 30, alice@example.com")

    try:
        invalid = parse_person("Bob, invalid, bob@example.com")
        error = None
    except ValueError as e:
        error = str(e)

    return {
        "valid_person": valid,
        "validation_error": error,
        "note": "Parsing should include validation",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 33: Parsing")
    print("=" * 60)

    print("\n1. String Parsing:")
    string = demonstrate_string_parsing()
    for key, value in string.items():
        print(f"   {key}: {value}")

    print("\n2. JSON Parsing:")
    json_demo = demonstrate_json_parsing()
    for key, value in json_demo.items():
        print(f"   {key}: {value}")

    print("\n3. CSV Parsing:")
    csv_demo = demonstrate_csv_parsing()
    for key, value in csv_demo.items():
        print(f"   {key}: {value}")

    print("\n4. URL Parsing:")
    url = demonstrate_url_parsing()
    for key, value in url.items():
        print(f"   {key}: {value}")

    print("\n5. AST Parsing:")
    ast_parse = demonstrate_ast_parsing()
    for key, value in ast_parse.items():
        print(f"   {key}: {value}")

    print("\n6. AST Modification:")
    ast_mod = demonstrate_ast_modification()
    for key, value in ast_mod.items():
        print(f"   {key}: {value}")

    print("\n7. Expression Parser:")
    expr = demonstrate_expression_parser()
    for key, value in expr.items():
        print(f"   {key}: {value}")

    print("\n8. Custom Parser:")
    custom = demonstrate_custom_parser()
    for key, value in custom.items():
        print(f"   {key}: {value}")

    print("\n9. Tokenization:")
    tokens = demonstrate_tokenization()
    for key, value in tokens.items():
        print(f"   {key}: {value}")

    print("\n10. Validation Parsing:")
    validation = demonstrate_validation_parsing()
    for key, value in validation.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
