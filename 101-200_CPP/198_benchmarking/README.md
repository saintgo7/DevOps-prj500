# Program 198: Benchmarking

## Description
Demonstrates benchmarking techniques for accurate performance measurement, using Google Benchmark and custom timing mechanisms.

## Learning Objectives
- Design effective benchmarks
- Use Google Benchmark framework
- Avoid common benchmarking pitfalls
- Measure statistical significance
- Compare algorithm performance

## Features
- Basic benchmarking patterns
- Google Benchmark usage
- Statistical analysis
- Micro-benchmarking
- Avoiding compiler optimizations in benchmarks
- Result interpretation

## Compilation
```bash
g++ -std=c++17 -O3 main.cpp -lbenchmark -lpthread -o benchmarking
./benchmarking
```

## Key Concepts
```cpp
#include <benchmark/benchmark.h>

static void BM_Function(benchmark::State& state) {
    for (auto _ : state) {
        // Code to benchmark
        benchmark::DoNotOptimize(result);
    }
}
BENCHMARK(BM_Function);

// Prevent optimization
benchmark::DoNotOptimize(value);
benchmark::ClobberMemory();
```

## Best Practices
1. Warm up before measuring
2. Run multiple iterations
3. Use DoNotOptimize for compiler barriers
4. Measure realistic workloads
5. Report statistical measures
6. Control for external factors

## Navigation
- **Previous**: [197 - Compiler Optimization](/home/user/DevOps-prj500/101-200_CPP/197_compiler_optimization/README.md)
- **Next**: [199 - Debugging Tools](/home/user/DevOps-prj500/101-200_CPP/199_debugging_tools/README.md)
