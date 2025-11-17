# Program 196: SIMD Vectorization

## Description
Explores SIMD (Single Instruction Multiple Data) vectorization for parallel processing using intrinsics and auto-vectorization techniques.

## Learning Objectives
- Understand SIMD concepts
- Use compiler auto-vectorization
- Apply SIMD intrinsics (SSE, AVX)
- Write vectorizable code
- Measure SIMD performance gains

## Features
- Auto-vectorization examples
- SSE/AVX intrinsics usage
- Vector operations
- Data alignment for SIMD
- SIMD best practices
- Performance comparison

## Compilation
```bash
g++ -std=c++17 -O3 -mavx2 main.cpp -o simd_vectorization
./simd_vectorization
```

## Key Concepts
```cpp
// Auto-vectorization (compiler does it)
for (int i = 0; i < n; ++i) {
    c[i] = a[i] + b[i];  // Compiler vectorizes
}

// Explicit intrinsics
#include <immintrin.h>
__m256 a_vec = _mm256_load_ps(&a[i]);
__m256 b_vec = _mm256_load_ps(&b[i]);
__m256 c_vec = _mm256_add_ps(a_vec, b_vec);
_mm256_store_ps(&c[i], c_vec);
```

## Best Practices
1. Let compiler auto-vectorize when possible
2. Align data for SIMD operations
3. Use appropriate instruction sets
4. Profile vectorized code
5. Consider portability
6. Use vector libraries when available

## Navigation
- **Previous**: [195 - Cache Optimization](/home/user/DevOps-prj500/101-200_CPP/195_cache_optimization/README.md)
- **Next**: [197 - Compiler Optimization](/home/user/DevOps-prj500/101-200_CPP/197_compiler_optimization/README.md)
