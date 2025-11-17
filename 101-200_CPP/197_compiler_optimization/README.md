# Program 197: Compiler Optimization

## Description
Explores compiler optimization flags, pragmas, and attributes to guide compiler optimizations for better performance.

## Learning Objectives
- Use optimization flags (-O1, -O2, -O3)
- Apply compiler-specific attributes
- Use pragmas for optimization hints
- Understand optimization trade-offs
- Profile optimization levels

## Features
- Optimization flag comparison
- Function attributes (inline, hot, cold)
- Pragmas (unroll, vectorize)
- Link-time optimization (LTO)
- Profile-guided optimization (PGO)
- Optimization report generation

## Compilation
```bash
g++ -std=c++17 -O3 -flto -fprofile-generate main.cpp -o compiler_optimization
./compiler_optimization
g++ -std=c++17 -O3 -flto -fprofile-use main.cpp -o compiler_optimization
```

## Key Concepts
```cpp
// Function attributes
__attribute__((hot)) void frequently_called();
__attribute__((cold)) void rarely_called();
__attribute__((always_inline)) inline void must_inline();

// Pragmas
#pragma GCC optimize("O3")
#pragma GCC unroll 4

// Compile flags
// -O2: Recommended for production
// -O3: Aggressive optimizations
// -flto: Link-time optimization
// -fprofile-generate/use: PGO
```

## Best Practices
1. Use -O2 for production builds
2. Test with different optimization levels
3. Enable LTO for final builds
4. Use PGO for critical paths
5. Understand optimization trade-offs
6. Check generated assembly

## Navigation
- **Previous**: [196 - SIMD Vectorization](/home/user/DevOps-prj500/101-200_CPP/196_simd_vectorization/README.md)
- **Next**: [198 - Benchmarking](/home/user/DevOps-prj500/101-200_CPP/198_benchmarking/README.md)
