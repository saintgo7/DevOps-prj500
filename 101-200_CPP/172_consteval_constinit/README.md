# Program 172: Consteval and Constinit

## Description
Explores C++20 consteval and constinit keywords, which provide more control over compile-time evaluation and static variable initialization.

## Learning Objectives
- Use consteval for guaranteed compile-time evaluation
- Apply constinit for static initialization
- Distinguish between constexpr, consteval, and constinit
- Prevent static initialization order fiasco

## Features
- Consteval immediate functions
- Constinit static variable initialization
- Comparison with constexpr
- Compile-time enforcement
- Static initialization patterns

## Compilation
```bash
g++ -std=c++20 main.cpp -o consteval_constinit
./consteval_constinit
```

## Key Concepts
```cpp
consteval int square(int n) {
    return n * n;  // Must be evaluated at compile-time
}

constinit int global = square(5);  // Static initialization at compile-time
```

## Best Practices
1. Use consteval when compile-time evaluation is required
2. Use constinit for thread-safe static initialization
3. Understand the differences from constexpr
4. Apply for configuration constants

## Navigation
- **Previous**: [171 - Constexpr Functions](/home/user/DevOps-prj500/101-200_CPP/171_constexpr_functions/README.md)
- **Next**: [173 - Structured Bindings](/home/user/DevOps-prj500/101-200_CPP/173_structured_bindings/README.md)
