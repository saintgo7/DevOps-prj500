# Program 174: std::optional

## Description
Explores std::optional (C++17), a type-safe way to represent optional values that may or may not contain a value, replacing error-prone pointer-based approaches.

## Learning Objectives
- Use std::optional for optional return values
- Check for value presence
- Access optional values safely
- Use value_or for defaults
- Apply optional in function parameters

## Features
- Basic optional usage
- value() vs operator*
- has_value() checking
- value_or() for defaults
- Optional with custom types
- Optional references

## Compilation
```bash
g++ -std=c++17 main.cpp -o std_optional
./std_optional
```

## Key Concepts
```cpp
std::optional<int> findValue(int key) {
    if (found) return value;
    return std::nullopt;
}

auto result = findValue(42);
if (result) {
    cout << *result;  // or result.value()
}
int val = result.value_or(0);  // Default to 0 if empty
```

## Best Practices
1. Use for functions that may not return a value
2. Prefer value_or() for default values
3. Check has_value() before accessing
4. Avoid optional of pointers
5. Use for config/settings that may be absent

## Navigation
- **Previous**: [173 - Structured Bindings](/home/user/DevOps-prj500/101-200_CPP/173_structured_bindings/README.md)
- **Next**: [175 - Std Variant](/home/user/DevOps-prj500/101-200_CPP/175_std_variant/README.md)
