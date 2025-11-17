# Program 193: Performance Profiling

## Description
Demonstrates performance profiling techniques and tools for C++ applications, including gprof, perf, valgrind, and built-in timing mechanisms.

## Learning Objectives
- Use profiling tools (gprof, perf, valgrind)
- Identify performance bottlenecks
- Analyze function call frequency
- Measure memory usage
- Interpret profiling results

## Features
- gprof usage
- perf tool demonstration
- Valgrind cachegrind
- Custom timing instrumentation
- Hotspot identification
- Profiling guided optimization

## Compilation
```bash
g++ -std=c++17 -pg main.cpp -o performance_profiling
./performance_profiling
gprof performance_profiling gmon.out
```

## Key Concepts
```cpp
// Built-in timing
auto start = chrono::high_resolution_clock::now();
// Code to profile
auto end = chrono::high_resolution_clock::now();
auto duration = duration_cast<microseconds>(end - start);

// Compile with -pg for gprof
// Use perf record/report for detailed analysis
// valgrind --tool=callgrind for call graphs
```

## Best Practices
1. Profile before optimizing
2. Use appropriate profiling tools
3. Profile realistic workloads
4. Focus on hotspots
5. Measure impact of optimizations

## Navigation
- **Previous**: [192 - Async IO](/home/user/DevOps-prj500/101-200_CPP/192_async_io/README.md)
- **Next**: [194 - Optimization Techniques](/home/user/DevOps-prj500/101-200_CPP/194_optimization_techniques/README.md)
