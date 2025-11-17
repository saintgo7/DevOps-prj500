#!/usr/bin/env python3
"""Program 11: String Methods - Master string manipulation in Python."""

from typing import List, Any


def demonstrate_case_methods() -> dict[str, Any]:
    """Demonstrate case conversion methods."""
    text = "Hello World Python"

    return {
        "original": text,
        "lower": text.lower(),
        "upper": text.upper(),
        "title": text.title(),
        "capitalize": text.capitalize(),
        "swapcase": text.swapcase(),
        "casefold": "ß".casefold(),  # More aggressive than lower()
    }


def demonstrate_search_methods() -> dict[str, Any]:
    """Demonstrate string search methods."""
    text = "Hello World, Hello Python"

    return {
        "find_hello": text.find("Hello"),
        "find_hello_start_10": text.find("Hello", 10),
        "find_missing": text.find("Java"),
        "rfind_hello": text.rfind("Hello"),
        "index_world": text.index("World"),
        "count_hello": text.count("Hello"),
        "count_o": text.count("o"),
        "startswith_hello": text.startswith("Hello"),
        "endswith_python": text.endswith("Python"),
        "in_operator": "World" in text,
    }


def demonstrate_check_methods() -> dict[str, Any]:
    """Demonstrate string checking methods."""
    return {
        "isalpha": {"abc": "abc".isalpha(), "abc123": "abc123".isalpha()},
        "isdigit": {"123": "123".isdigit(), "12.3": "12.3".isdigit()},
        "isalnum": {"abc123": "abc123".isalnum(), "abc 123": "abc 123".isalnum()},
        "isspace": {"   ": "   ".isspace(), " a ": " a ".isspace()},
        "islower": {"hello": "hello".islower(), "Hello": "Hello".islower()},
        "isupper": {"HELLO": "HELLO".isupper(), "Hello": "Hello".isupper()},
        "istitle": {"Hello World": "Hello World".istitle(), "hello world": "hello world".istitle()},
        "isdecimal": {"123": "123".isdecimal(), "12.3": "12.3".isdecimal()},
        "isnumeric": {"123": "123".isnumeric(), "½": "½".isnumeric()},
        "isidentifier": {"variable_name": "variable_name".isidentifier(), "123var": "123var".isidentifier()},
    }


def demonstrate_modification_methods() -> dict[str, Any]:
    """Demonstrate string modification methods."""
    return {
        "strip": "  hello  ".strip(),
        "lstrip": "  hello  ".lstrip(),
        "rstrip": "  hello  ".rstrip(),
        "strip_chars": "...hello...".strip("."),
        "replace": "hello world".replace("world", "python"),
        "replace_count": "aaa bbb aaa".replace("aaa", "xxx", 1),
        "removeprefix": "HelloWorld".removeprefix("Hello"),  # Python 3.9+
        "removesuffix": "HelloWorld".removesuffix("World"),  # Python 3.9+
    }


def demonstrate_split_join_methods() -> dict[str, Any]:
    """Demonstrate split and join methods."""
    text = "apple,banana,cherry"
    words = "hello world python"
    multiline = "line1\nline2\nline3"

    # Split
    split_comma = text.split(",")
    split_default = words.split()
    split_maxsplit = "a b c d e".split(" ", 2)
    rsplit = "a b c d e".rsplit(" ", 2)
    splitlines = multiline.splitlines()
    partition = "hello:world".partition(":")
    rpartition = "a:b:c".rpartition(":")

    # Join
    join_comma = ",".join(["a", "b", "c"])
    join_space = " ".join(["hello", "world"])
    join_numbers = "-".join(map(str, [1, 2, 3, 4, 5]))

    return {
        "split_comma": split_comma,
        "split_whitespace": split_default,
        "split_maxsplit": split_maxsplit,
        "rsplit": rsplit,
        "splitlines": splitlines,
        "partition": partition,
        "rpartition": rpartition,
        "join_comma": join_comma,
        "join_space": join_space,
        "join_numbers": join_numbers,
    }


def demonstrate_alignment_methods() -> dict[str, Any]:
    """Demonstrate string alignment methods."""
    text = "hello"

    return {
        "center_20": text.center(20),
        "center_20_star": text.center(20, "*"),
        "ljust_20": text.ljust(20),
        "ljust_20_dash": text.ljust(20, "-"),
        "rjust_20": text.rjust(20),
        "rjust_20_dot": text.rjust(20, "."),
        "zfill_10": "42".zfill(10),
        "zfill_negative": "-42".zfill(10),
    }


def demonstrate_formatting_methods() -> dict[str, Any]:
    """Demonstrate string formatting methods."""
    # Old-style formatting (%)
    old_style = "Hello, %s! You are %d years old." % ("Alice", 25)

    # str.format()
    format_positional = "Hello, {}! You are {} years old.".format("Bob", 30)
    format_indexed = "{1} {0}".format("World", "Hello")
    format_named = "Hello, {name}! You are {age} years old.".format(name="Charlie", age=35)
    format_number = "Pi: {:.2f}".format(3.14159)
    format_padding = "{:>10}".format("right")

    # f-strings (Python 3.6+)
    name = "David"
    age = 40
    fstring = f"Hello, {name}! You are {age} years old."
    fstring_expr = f"Next year: {age + 1}"
    fstring_format = f"Pi: {3.14159:.2f}"

    # Template strings
    from string import Template
    template = Template("Hello, $name! You are $age years old.")
    template_result = template.substitute(name="Eve", age=28)

    return {
        "old_style": old_style,
        "format_positional": format_positional,
        "format_indexed": format_indexed,
        "format_named": format_named,
        "format_number": format_number,
        "format_padding": format_padding,
        "fstring": fstring,
        "fstring_expr": fstring_expr,
        "fstring_format": fstring_format,
        "template": template_result,
    }


def demonstrate_encoding_methods() -> dict[str, Any]:
    """Demonstrate encoding and decoding methods."""
    text = "Hello, 世界"

    # Encode to bytes
    utf8_bytes = text.encode("utf-8")
    ascii_bytes = "Hello".encode("ascii")

    # Decode from bytes
    decoded = utf8_bytes.decode("utf-8")

    # Different encodings
    utf16_bytes = text.encode("utf-16")
    latin1_bytes = "Hello".encode("latin-1")

    return {
        "original": text,
        "utf8_bytes": utf8_bytes,
        "ascii_bytes": ascii_bytes,
        "decoded": decoded,
        "utf16_bytes": utf16_bytes,
        "latin1_bytes": latin1_bytes,
        "bytes_length_utf8": len(utf8_bytes),
        "str_length": len(text),
    }


def demonstrate_advanced_methods() -> dict[str, Any]:
    """Demonstrate advanced string methods."""
    # Translate
    translation_table = str.maketrans("aeiou", "12345")
    translated = "hello world".translate(translation_table)

    # Expandtabs
    tabbed = "hello\tworld\tpython"
    expanded = tabbed.expandtabs(4)

    # String concatenation performance
    # Bad: repeated concatenation
    # Good: join for multiple strings
    words = ["hello", "world", "python"]
    efficient = " ".join(words)

    # Raw strings
    raw = r"C:\new\text.txt"
    normal = "C:\\new\\text.txt"

    # Multiline strings
    multiline = """Line 1
Line 2
Line 3"""

    return {
        "translate": translated,
        "expandtabs": expanded,
        "join_efficient": efficient,
        "raw_string": raw,
        "normal_string": normal,
        "raw_equals_normal": raw == normal,
        "multiline": multiline,
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 11: String Methods")
    print("=" * 60)

    print("\n1. Case Methods:")
    case_methods = demonstrate_case_methods()
    for key, value in case_methods.items():
        print(f"   {key}: {value}")

    print("\n2. Search Methods:")
    search_methods = demonstrate_search_methods()
    for key, value in search_methods.items():
        print(f"   {key}: {value}")

    print("\n3. Check Methods:")
    check_methods = demonstrate_check_methods()
    for key, value in check_methods.items():
        print(f"   {key}: {value}")

    print("\n4. Modification Methods:")
    modification_methods = demonstrate_modification_methods()
    for key, value in modification_methods.items():
        print(f"   {key}: {value}")

    print("\n5. Split and Join:")
    split_join = demonstrate_split_join_methods()
    for key, value in split_join.items():
        print(f"   {key}: {value}")

    print("\n6. Alignment Methods:")
    alignment = demonstrate_alignment_methods()
    for key, value in alignment.items():
        print(f"   {key}: '{value}'")

    print("\n7. Formatting Methods:")
    formatting = demonstrate_formatting_methods()
    for key, value in formatting.items():
        print(f"   {key}: {value}")

    print("\n8. Encoding Methods:")
    encoding = demonstrate_encoding_methods()
    for key, value in encoding.items():
        print(f"   {key}: {value}")

    print("\n9. Advanced Methods:")
    advanced = demonstrate_advanced_methods()
    for key, value in advanced.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
