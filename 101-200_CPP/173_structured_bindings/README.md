# Program 173: Structured Bindings

## Description
Demonstrates C++17 structured bindings for decomposing tuples, pairs, arrays, and structs into individual variables with clean, readable syntax.

## Learning Objectives
- Use structured bindings with pairs and tuples
- Decompose arrays with structured bindings
- Apply to user-defined types
- Understand auto deduction with bindings
- Work with references in bindings

## Features
- Pair decomposition
- Tuple decomposition
- Array decomposition
- Struct/class decomposition
- Reference bindings
- Const bindings

## Compilation
```bash
g++ -std=c++17 main.cpp -o structured_bindings
./structured_bindings
```

## Key Concepts
```cpp
auto [key, value] = myMap.insert({1, "one"});
auto [x, y, z] = std::make_tuple(1, 2, 3);
auto& [first, second] = myPair;  // Reference binding

struct Point { int x, y; };
Point p{1, 2};
auto [px, py] = p;
```

## Best Practices
1. Use for cleaner code when decomposing
2. Apply reference bindings when modifying
3. Use with range-based for loops
4. Leverage for multiple return values

## Navigation
- **Previous**: [172 - Consteval Constinit](/home/user/DevOps-prj500/101-200_CPP/172_consteval_constinit/README.md)
- **Next**: [174 - Std Optional](/home/user/DevOps-prj500/101-200_CPP/174_std_optional/README.md)
