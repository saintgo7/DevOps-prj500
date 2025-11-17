# Program 195: Cache Optimization

## Description
Demonstrates cache-friendly programming techniques to improve performance by maximizing cache hits and minimizing cache misses through data layout and access patterns.

## Learning Objectives
- Understand CPU cache hierarchy
- Implement cache-friendly data structures
- Optimize memory access patterns
- Use cache line alignment
- Reduce cache conflicts

## Features
- Cache hierarchy demonstration
- Structure of Arrays (SoA) vs Array of Structures (AoS)
- Cache line alignment
- Prefetching hints
- Spatial and temporal locality
- Cache performance measurement

## Compilation
```bash
g++ -std=c++17 -O3 main.cpp -o cache_optimization
./cache_optimization
```

## Key Concepts
```cpp
// Cache-friendly: Structure of Arrays
struct ParticlesSoA {
    vector<float> x, y, z;
    vector<float> vx, vy, vz;
};

// Cache line alignment
alignas(64) struct CacheAligned {
    int data[16];  // 64 bytes
};

// Sequential access (cache-friendly)
for (int i = 0; i < n; ++i) {
    sum += arr[i];  // Sequential, not random
}
```

## Best Practices
1. Access memory sequentially when possible
2. Align frequently accessed data
3. Use SoA for SIMD operations
4. Minimize cache line sharing
5. Profile cache performance
6. Consider false sharing in multithreading

## Navigation
- **Previous**: [194 - Optimization Techniques](/home/user/DevOps-prj500/101-200_CPP/194_optimization_techniques/README.md)
- **Next**: [196 - SIMD Vectorization](/home/user/DevOps-prj500/101-200_CPP/196_simd_vectorization/README.md)
