# Program 170: Modules

## Description
Explores C++20 modules, a modern alternative to header files that improves compilation time, eliminates header guards, and provides better encapsulation.

## Learning Objectives
- Understand C++20 module syntax
- Create module interfaces
- Export declarations
- Import modules
- Use module partitions
- Compare modules with headers

## Features
- Basic module creation
- Export and import syntax
- Module partitions
- Private module fragments
- Module linkage
- Migration from headers

## Compilation
```bash
# Compiler-specific, example for recent GCC/Clang
g++ -std=c++20 -fmodules-ts module.cpp main.cpp -o modules
./modules
```

## Key Concepts
```cpp
// Module interface
export module math;
export int add(int a, int b) { return a + b; }

// Using module
import math;
int result = add(1, 2);
```

## Best Practices
1. Use modules for new projects when supported
2. Export only public interfaces
3. Use module partitions for organization
4. Understand compiler support status
5. Consider build system integration

## Navigation
- **Previous**: [169 - Coroutines](/home/user/DevOps-prj500/101-200_CPP/169_coroutines/README.md)
- **Next**: [171 - Constexpr Functions](/home/user/DevOps-prj500/101-200_CPP/171_constexpr_functions/README.md)
