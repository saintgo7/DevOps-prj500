# Program 171: Constexpr Functions

## Description
Demonstrates constexpr functions in C++ for compile-time computation, enabling code to be evaluated at both compile-time and runtime depending on context.

## Learning Objectives
- Write constexpr functions
- Understand compile-time vs runtime evaluation
- Use constexpr in constant expressions
- Apply constexpr with user-defined types
- Leverage constexpr for optimization

## Features
- Basic constexpr functions
- Constexpr constructors
- Constexpr member functions
- Compile-time recursion
- Constexpr if (C++17)
- Constexpr std algorithms (C++20)

## Compilation
```bash
g++ -std=c++20 main.cpp -o constexpr_functions
./constexpr_functions
```

## Key Concepts
```cpp
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int value = factorial(5);  // Computed at compile-time
int arr[factorial(4)];              // Array size must be compile-time constant
```

## Best Practices
1. Mark functions constexpr when possible for optimization
2. Use constexpr for configuration values
3. Leverage constexpr if for compile-time branching (C++17)
4. Test both compile-time and runtime paths

## Navigation
- **Previous**: [170 - Modules](/home/user/DevOps-prj500/101-200_CPP/170_modules/README.md)
- **Next**: [172 - Consteval Constinit](/home/user/DevOps-prj500/101-200_CPP/172_consteval_constinit/README.md)
