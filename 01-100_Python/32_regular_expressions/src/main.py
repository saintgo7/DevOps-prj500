#!/usr/bin/env python3
"""Program 32: Regular Expressions - Master pattern matching with regex."""

import re
from typing import Any, List, Optional


def demonstrate_basic_patterns() -> dict[str, Any]:
    """Demonstrate basic regex patterns."""

    text = "The price is $19.99 and the code is ABC123"

    # Match literal string
    match1 = re.search(r"price", text)

    # Match digits
    match2 = re.search(r"\d+", text)

    # Match word characters
    match3 = re.search(r"\w+", text)

    # Match specific pattern
    match4 = re.search(r"\$\d+\.\d+", text)

    return {
        "literal": match1.group() if match1 else None,
        "digits": match2.group() if match2 else None,
        "word": match3.group() if match3 else None,
        "price": match4.group() if match4 else None,
        "note": "Basic patterns: literals, \\d (digit), \\w (word), \\s (space)",
    }


def demonstrate_match_vs_search() -> dict[str, Any]:
    """Demonstrate difference between match() and search()."""

    text = "Hello World Python"

    # match() checks start of string
    match_result = re.match(r"Hello", text)
    match_world = re.match(r"World", text)

    # search() finds anywhere in string
    search_result = re.search(r"Hello", text)
    search_world = re.search(r"World", text)

    return {
        "match_hello": match_result.group() if match_result else None,
        "match_world": match_world.group() if match_world else None,
        "search_hello": search_result.group() if search_result else None,
        "search_world": search_world.group() if search_world else None,
        "note": "match() from start, search() anywhere",
    }


def demonstrate_findall_finditer() -> dict[str, Any]:
    """Demonstrate findall() and finditer()."""

    text = "Call me at 123-456-7890 or 987-654-3210"

    # findall returns list of all matches
    all_phones = re.findall(r"\d{3}-\d{3}-\d{4}", text)

    # finditer returns iterator of match objects
    matches = []
    for match in re.finditer(r"\d{3}-\d{3}-\d{4}", text):
        matches.append({
            "value": match.group(),
            "start": match.start(),
            "end": match.end(),
        })

    return {
        "findall_result": all_phones,
        "finditer_count": len(matches),
        "first_match": matches[0] if matches else None,
        "note": "findall() returns strings, finditer() returns match objects",
    }


def demonstrate_groups() -> dict[str, Any]:
    """Demonstrate capturing groups."""

    text = "John Doe (john@example.com)"

    # Groups with parentheses
    pattern = r"(\w+) (\w+) \(([^)]+)\)"
    match = re.search(pattern, text)

    if match:
        groups = match.groups()
        group_dict = {
            "full_match": match.group(0),
            "first_name": match.group(1),
            "last_name": match.group(2),
            "email": match.group(3),
        }
    else:
        group_dict = {}

    # Named groups
    pattern_named = r"(?P<first>\w+) (?P<last>\w+) \((?P<email>[^)]+)\)"
    match_named = re.search(pattern_named, text)

    return {
        **group_dict,
        "named_groups": match_named.groupdict() if match_named else {},
        "note": "() creates groups, (?P<name>...) creates named groups",
    }


def demonstrate_substitution() -> dict[str, Any]:
    """Demonstrate sub() and subn() for substitution."""

    text = "The price is $19.99 and discount is $5.00"

    # Simple substitution
    result1 = re.sub(r"\$(\d+\.\d+)", r"USD \1", text)

    # Substitution with count
    result2 = re.sub(r"\$", "€", text, count=1)

    # subn returns tuple (result, count)
    result3, count = re.subn(r"\$\d+\.\d+", "PRICE", text)

    # Function-based substitution
    def double_price(match):
        price = float(match.group(1))
        return f"${price * 2:.2f}"

    result4 = re.sub(r"\$(\d+\.\d+)", double_price, text)

    return {
        "add_currency": result1,
        "replace_first": result2,
        "replace_all": result3,
        "substitution_count": count,
        "double_prices": result4,
        "note": "sub() replaces, subn() returns (result, count)",
    }


def demonstrate_split() -> dict[str, Any]:
    """Demonstrate split() with regex."""

    text = "one,two;three:four|five"

    # Split on single delimiter
    split1 = re.split(r",", text)

    # Split on multiple delimiters
    split2 = re.split(r"[,;:|]", text)

    # Split with limit
    split3 = re.split(r"[,;:|]", text, maxsplit=2)

    # Split preserving delimiters
    split4 = re.split(r"([,;:|])", text)

    return {
        "single_delimiter": split1,
        "multiple_delimiters": split2,
        "with_limit": split3,
        "preserve_delimiters": split4[:5],
        "note": "split() divides string by pattern",
    }


def demonstrate_flags() -> dict[str, Any]:
    """Demonstrate regex flags."""

    text = "Hello WORLD\nPython Rules"

    # Case insensitive
    match1 = re.search(r"world", text, re.IGNORECASE)

    # Multiline mode
    match2 = re.findall(r"^Python", text, re.MULTILINE)

    # Dot matches newline
    match3 = re.search(r"WORLD.+Python", text, re.DOTALL)

    # Verbose mode
    pattern_verbose = r"""
        (\d{3})  # Area code
        -        # Separator
        (\d{3})  # Exchange
        -        # Separator
        (\d{4})  # Number
    """
    phone = "123-456-7890"
    match4 = re.search(pattern_verbose, phone, re.VERBOSE)

    return {
        "ignorecase": match1.group() if match1 else None,
        "multiline": match2,
        "dotall": match3.group() if match3 else None,
        "verbose": match4.group() if match4 else None,
        "note": "Flags: IGNORECASE, MULTILINE, DOTALL, VERBOSE",
    }


def demonstrate_lookahead_lookbehind() -> dict[str, Any]:
    """Demonstrate lookahead and lookbehind assertions."""

    text = "Price: $100, Cost: $50, Tax: $10"

    # Positive lookahead
    prices = re.findall(r"\$\d+(?= |,)", text)

    # Negative lookahead
    not_tax = re.findall(r"\$\d+(?! Tax)", text)

    # Positive lookbehind
    amounts = re.findall(r"(?<=\$)\d+", text)

    # Negative lookbehind
    not_after_tax = re.findall(r"(?<!Tax: )\$\d+", text)

    return {
        "positive_lookahead": prices,
        "negative_lookahead": not_tax,
        "positive_lookbehind": amounts,
        "negative_lookbehind": not_after_tax[:2],
        "note": "(?=...) lookahead, (?<=...) lookbehind",
    }


def demonstrate_greedy_vs_lazy() -> dict[str, Any]:
    """Demonstrate greedy vs lazy quantifiers."""

    html = "<div>First</div><div>Second</div>"

    # Greedy (default)
    greedy = re.findall(r"<div>.*</div>", html)

    # Lazy (non-greedy)
    lazy = re.findall(r"<div>.*?</div>", html)

    text = "aaaaa"

    # Greedy quantifiers
    greedy_plus = re.search(r"a+", text).group()
    greedy_star = re.search(r"a*", text).group()

    # Lazy quantifiers
    lazy_plus = re.search(r"a+?", text).group()
    lazy_star = re.search(r"a*?", text).group()

    return {
        "greedy_div": greedy,
        "lazy_div": lazy,
        "greedy_plus": greedy_plus,
        "lazy_plus": lazy_plus,
        "note": "*?, +?, ?? are lazy versions of *, +, ?",
    }


def demonstrate_practical_examples() -> dict[str, Any]:
    """Demonstrate practical regex use cases."""

    # Email validation
    email = "user@example.com"
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    valid_email = bool(re.match(email_pattern, email))

    # Phone number extraction
    text = "Contact: (123) 456-7890 or 987.654.3210"
    phone_pattern = r"(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})"
    phones = re.findall(phone_pattern, text)

    # URL extraction
    text = "Visit https://example.com or http://test.org"
    url_pattern = r"https?://[^\s]+"
    urls = re.findall(url_pattern, text)

    # Password strength (has uppercase, lowercase, digit, special)
    password = "MyPass123!"
    strong = all([
        re.search(r"[A-Z]", password),
        re.search(r"[a-z]", password),
        re.search(r"\d", password),
        re.search(r"[!@#$%^&*]", password),
        len(password) >= 8
    ])

    # Extract hashtags
    tweet = "Learning #Python and #Regex is fun! #coding"
    hashtags = re.findall(r"#\w+", tweet)

    return {
        "valid_email": valid_email,
        "phones": phones,
        "urls": urls,
        "strong_password": strong,
        "hashtags": hashtags,
        "note": "Regex useful for validation, extraction, parsing",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 32: Regular Expressions")
    print("=" * 60)

    print("\n1. Basic Patterns:")
    basic = demonstrate_basic_patterns()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Match vs Search:")
    match_search = demonstrate_match_vs_search()
    for key, value in match_search.items():
        print(f"   {key}: {value}")

    print("\n3. Findall and Finditer:")
    findall = demonstrate_findall_finditer()
    for key, value in findall.items():
        print(f"   {key}: {value}")

    print("\n4. Groups:")
    groups = demonstrate_groups()
    for key, value in groups.items():
        print(f"   {key}: {value}")

    print("\n5. Substitution:")
    sub = demonstrate_substitution()
    for key, value in sub.items():
        print(f"   {key}: {value}")

    print("\n6. Split:")
    split = demonstrate_split()
    for key, value in split.items():
        print(f"   {key}: {value}")

    print("\n7. Flags:")
    flags = demonstrate_flags()
    for key, value in flags.items():
        print(f"   {key}: {value}")

    print("\n8. Lookahead/Lookbehind:")
    lookaround = demonstrate_lookahead_lookbehind()
    for key, value in lookaround.items():
        print(f"   {key}: {value}")

    print("\n9. Greedy vs Lazy:")
    greedy = demonstrate_greedy_vs_lazy()
    for key, value in greedy.items():
        print(f"   {key}: {value}")

    print("\n10. Practical Examples:")
    practical = demonstrate_practical_examples()
    for key, value in practical.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
