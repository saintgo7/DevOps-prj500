# Program 175: std::variant

## Description
Demonstrates std::variant (C++17), a type-safe union that can hold one of several specified types, providing a modern alternative to C-style unions and void pointers.

## Learning Objectives
- Create and use std::variant
- Access variant values with std::get and std::visit
- Handle variant alternatives
- Use std::holds_alternative
- Apply variant for polymorphism without inheritance

## Features
- Basic variant usage
- std::get for value access
- std::visit for visitation
- std::holds_alternative checking
- Variant with custom types
- Exception handling (std::bad_variant_access)

## Compilation
```bash
g++ -std=c++17 main.cpp -o std_variant
./std_variant
```

## Key Concepts
```cpp
std::variant<int, double, string> v = "hello";

// Access
string s = std::get<string>(v);
if (auto* p = std::get_if<string>(&v)) { /* use p */ }

// Visit
std::visit([](auto&& arg) {
    cout << arg;
}, v);
```

## Best Practices
1. Use std::visit for type-safe handling
2. Prefer std::get_if to avoid exceptions
3. Apply for state machines
4. Use for polymorphism without inheritance
5. Consider std::variant over unions

## Navigation
- **Previous**: [174 - Std Optional](/home/user/DevOps-prj500/101-200_CPP/174_std_optional/README.md)
- **Next**: [176 - Std Any](/home/user/DevOps-prj500/101-200_CPP/176_std_any/README.md)
