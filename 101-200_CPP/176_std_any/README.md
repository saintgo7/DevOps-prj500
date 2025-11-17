# Program 176: std::any

## Description
Explores std::any (C++17), a type-safe container for single values of any type, providing type erasure for generic programming scenarios.

## Learning Objectives
- Use std::any for type erasure
- Store and retrieve values safely
- Check contained type
- Handle std::bad_any_cast
- Apply any in heterogeneous containers

## Features
- Basic any usage
- any_cast for value access
- type() for type checking
- has_value() checking
- Reset and emplace
- Exception handling

## Compilation
```bash
g++ -std=c++17 main.cpp -o std_any
./std_any
```

## Key Concepts
```cpp
std::any a = 42;
a = 3.14;
a = string("hello");

int i = std::any_cast<int>(a);  // Throws if wrong type
if (auto* p = std::any_cast<string>(&a)) { /* use p */ }

if (a.type() == typeid(string)) { /* is string */ }
```

## Best Practices
1. Use when type is truly unknown at compile-time
2. Prefer std::variant when types are known
3. Use any_cast with pointer for no-throw access
4. Document expected types
5. Consider performance implications

## Navigation
- **Previous**: [175 - Std Variant](/home/user/DevOps-prj500/101-200_CPP/175_std_variant/README.md)
- **Next**: [177 - String View](/home/user/DevOps-prj500/101-200_CPP/177_string_view/README.md)
