/*
 * Program 194: Optimization Techniques
 * Demonstrates code optimization strategies and best practices
 * Compile: g++ -std=c++17 -O3 -o optimization_techniques main.cpp
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <string>
#include <memory>

// Performance measurement helper
template<typename Func>
double measure(const std::string& name, Func func, int iterations = 1) {
    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < iterations; ++i) {
        func();
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    double ms = duration.count() / 1000.0;

    std::cout << name << ": " << ms << " ms";
    if (iterations > 1) {
        std::cout << " (" << (ms / iterations) << " ms per iteration)";
    }
    std::cout << std::endl;

    return ms;
}

void demonstrateLoopOptimization() {
    std::cout << "\n=== Loop Optimization ===" << std::endl;

    const int SIZE = 1000000;

    // Unoptimized: repeated calculation
    auto time1 = measure("Unoptimized loop", [&]() {
        std::vector<int> vec(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec[i] = i * 2;
        }
    });

    // Optimized: cache vector size
    auto time2 = measure("Cached size", [&]() {
        std::vector<int> vec(SIZE);
        int size = vec.size();
        for (int i = 0; i < size; ++i) {
            vec[i] = i * 2;
        }
    });

    // Loop unrolling
    auto time3 = measure("Loop unrolling (4x)", [&]() {
        std::vector<int> vec(SIZE);
        int size = vec.size();
        int i;
        for (i = 0; i + 3 < size; i += 4) {
            vec[i] = i * 2;
            vec[i + 1] = (i + 1) * 2;
            vec[i + 2] = (i + 2) * 2;
            vec[i + 3] = (i + 3) * 2;
        }
        for (; i < size; ++i) {
            vec[i] = i * 2;
        }
    });

    std::cout << "Speedup (cached): " << (time1 / time2) << "x" << std::endl;
    std::cout << "Speedup (unrolled): " << (time1 / time3) << "x" << std::endl;
}

void demonstrateFunctionInlining() {
    std::cout << "\n=== Function Inlining ===" << std::endl;

    const int ITERATIONS = 10000000;

    // Non-inline function
    auto non_inline_func = [](int x) {
        return x * x + 2 * x + 1;
    };

    // Inline function (compiler likely inlines lambda anyway)
    inline auto inline_func = [](int x) -> int {
        return x * x + 2 * x + 1;
    };

    auto time1 = measure("Non-inline", [&]() {
        volatile int result = 0;
        for (int i = 0; i < ITERATIONS; ++i) {
            result = non_inline_func(i);
        }
    });

    auto time2 = measure("Inline hint", [&]() {
        volatile int result = 0;
        for (int i = 0; i < ITERATIONS; ++i) {
            result = inline_func(i);
        }
    });

    auto time3 = measure("Direct computation", [&]() {
        volatile int result = 0;
        for (int i = 0; i < ITERATIONS; ++i) {
            result = i * i + 2 * i + 1;
        }
    });

    std::cout << "Note: Modern compilers auto-inline aggressively with -O2/-O3" << std::endl;
}

void demonstrateMemoryAlignment() {
    std::cout << "\n=== Memory Alignment ===" << std::endl;

    struct UnalignedStruct {
        char a;
        int b;
        char c;
        double d;
    };

    struct AlignedStruct {
        double d;
        int b;
        char a;
        char c;
    };

    struct PackedStruct {
        char a;
        int b;
        char c;
        double d;
    } __attribute__((packed));

    std::cout << "Size comparisons:" << std::endl;
    std::cout << "  Unaligned struct: " << sizeof(UnalignedStruct) << " bytes" << std::endl;
    std::cout << "  Aligned struct: " << sizeof(AlignedStruct) << " bytes" << std::endl;
    std::cout << "  Packed struct: " << sizeof(PackedStruct) << " bytes" << std::endl;

    std::cout << "\nAlignment info:" << std::endl;
    std::cout << "  char: " << alignof(char) << " bytes" << std::endl;
    std::cout << "  int: " << alignof(int) << " bytes" << std::endl;
    std::cout << "  double: " << alignof(double) << " bytes" << std::endl;
    std::cout << "  UnalignedStruct: " << alignof(UnalignedStruct) << " bytes" << std::endl;
    std::cout << "  AlignedStruct: " << alignof(AlignedStruct) << " bytes" << std::endl;
}

void demonstrateBranchPrediction() {
    std::cout << "\n=== Branch Prediction ===" << std::endl;

    const int SIZE = 1000000;
    std::vector<int> data(SIZE);

    // Fill with random-ish data
    for (int i = 0; i < SIZE; ++i) {
        data[i] = (i * 31) % 100;
    }

    // Unpredictable branches
    auto time1 = measure("Unpredictable branches", [&]() {
        int sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            if (data[i] < 50) {
                sum += data[i];
            } else {
                sum -= data[i];
            }
        }
    });

    // Sort to make branches predictable
    std::sort(data.begin(), data.end());

    auto time2 = measure("Predictable branches (sorted)", [&]() {
        int sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            if (data[i] < 50) {
                sum += data[i];
            } else {
                sum -= data[i];
            }
        }
    });

    // Branch-free version
    auto time3 = measure("Branch-free", [&]() {
        int sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            int is_less = (data[i] < 50) ? 1 : -1;
            sum += data[i] * is_less;
        }
    });

    std::cout << "Speedup (predictable): " << (time1 / time2) << "x" << std::endl;
    std::cout << "Speedup (branch-free): " << (time1 / time3) << "x" << std::endl;
}

void demonstrateCacheLocality() {
    std::cout << "\n=== Cache Locality ===" << std::endl;

    const int ROWS = 1000;
    const int COLS = 1000;
    std::vector<std::vector<int>> matrix(ROWS, std::vector<int>(COLS, 1));

    // Row-major traversal (cache-friendly)
    auto time1 = measure("Row-major (cache-friendly)", [&]() {
        long sum = 0;
        for (int i = 0; i < ROWS; ++i) {
            for (int j = 0; j < COLS; ++j) {
                sum += matrix[i][j];
            }
        }
    });

    // Column-major traversal (cache-unfriendly)
    auto time2 = measure("Column-major (cache-unfriendly)", [&]() {
        long sum = 0;
        for (int j = 0; j < COLS; ++j) {
            for (int i = 0; i < ROWS; ++i) {
                sum += matrix[i][j];
            }
        }
    });

    std::cout << "Slowdown (column-major): " << (time2 / time1) << "x" << std::endl;
}

void demonstrateStringOptimization() {
    std::cout << "\n=== String Optimization ===" << std::endl;

    const int ITERATIONS = 10000;

    // Naive concatenation
    auto time1 = measure("Naive concatenation", [&]() {
        std::string result;
        for (int i = 0; i < ITERATIONS; ++i) {
            result += "test";
        }
    });

    // Reserve space
    auto time2 = measure("With reserve", [&]() {
        std::string result;
        result.reserve(ITERATIONS * 4);
        for (int i = 0; i < ITERATIONS; ++i) {
            result += "test";
        }
    });

    // Use append
    auto time3 = measure("Using append", [&]() {
        std::string result;
        result.reserve(ITERATIONS * 4);
        for (int i = 0; i < ITERATIONS; ++i) {
            result.append("test");
        }
    });

    std::cout << "Speedup (reserve): " << (time1 / time2) << "x" << std::endl;
    std::cout << "Speedup (append): " << (time1 / time3) << "x" << std::endl;
}

void demonstrateContainerChoice() {
    std::cout << "\n=== Container Selection ===" << std::endl;

    const int SIZE = 100000;

    // Vector push_back
    auto time1 = measure("vector push_back", [&]() {
        std::vector<int> vec;
        for (int i = 0; i < SIZE; ++i) {
            vec.push_back(i);
        }
    });

    // Vector with reserve
    auto time2 = measure("vector with reserve", [&]() {
        std::vector<int> vec;
        vec.reserve(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec.push_back(i);
        }
    });

    // Vector with resize
    auto time3 = measure("vector with resize", [&]() {
        std::vector<int> vec(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec[i] = i;
        }
    });

    std::cout << "Speedup (reserve): " << (time1 / time2) << "x" << std::endl;
    std::cout << "Speedup (resize): " << (time1 / time3) << "x" << std::endl;
}

void demonstrateMoveSemantics() {
    std::cout << "\n=== Move Semantics ===" << std::endl;

    const int SIZE = 10000;

    // Copy semantics
    auto time1 = measure("Copy semantics", [&]() {
        std::vector<std::vector<int>> outer;
        for (int i = 0; i < SIZE; ++i) {
            std::vector<int> temp(100, i);
            outer.push_back(temp);  // Copy
        }
    });

    // Move semantics
    auto time2 = measure("Move semantics", [&]() {
        std::vector<std::vector<int>> outer;
        for (int i = 0; i < SIZE; ++i) {
            std::vector<int> temp(100, i);
            outer.push_back(std::move(temp));  // Move
        }
    });

    // Emplace
    auto time3 = measure("Emplace", [&]() {
        std::vector<std::vector<int>> outer;
        for (int i = 0; i < SIZE; ++i) {
            outer.emplace_back(100, i);  // Construct in-place
        }
    });

    std::cout << "Speedup (move): " << (time1 / time2) << "x" << std::endl;
    std::cout << "Speedup (emplace): " << (time1 / time3) << "x" << std::endl;
}

void demonstrateConstCorrectness() {
    std::cout << "\n=== Const Correctness Optimization ===" << std::endl;

    const int SIZE = 1000000;
    std::vector<int> data(SIZE, 42);

    // Non-const reference
    auto time1 = measure("Non-const reference", [&]() {
        auto& vec = data;
        long sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            sum += vec[i];
        }
    });

    // Const reference (allows more optimizations)
    auto time2 = measure("Const reference", [&]() {
        const auto& vec = data;
        long sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            sum += vec[i];
        }
    });

    std::cout << "Note: const allows compiler to assume data won't change" << std::endl;
}

void demonstrateCommonOptimizations() {
    std::cout << "\n=== Common Optimization Patterns ===" << std::endl;

    std::cout << "\n1. Avoid unnecessary copies:" << std::endl;
    std::cout << "   - Pass large objects by const reference" << std::endl;
    std::cout << "   - Use move semantics for transfers" << std::endl;
    std::cout << "   - Use emplace instead of push + copy" << std::endl;

    std::cout << "\n2. Minimize allocations:" << std::endl;
    std::cout << "   - Reserve space in vectors/strings" << std::endl;
    std::cout << "   - Reuse objects instead of recreating" << std::endl;
    std::cout << "   - Use object pools for frequent allocations" << std::endl;

    std::cout << "\n3. Cache-friendly code:" << std::endl;
    std::cout << "   - Access memory sequentially" << std::endl;
    std::cout << "   - Align data structures" << std::endl;
    std::cout << "   - Use array-of-structs vs struct-of-arrays wisely" << std::endl;

    std::cout << "\n4. Branch prediction:" << std::endl;
    std::cout << "   - Put likely path first in if-else" << std::endl;
    std::cout << "   - Use likely/unlikely hints (compiler-specific)" << std::endl;
    std::cout << "   - Consider branch-free algorithms for hot paths" << std::endl;

    std::cout << "\n5. Compiler optimizations:" << std::endl;
    std::cout << "   - Use -O2 or -O3 flags" << std::endl;
    std::cout << "   - Enable link-time optimization (-flto)" << std::endl;
    std::cout << "   - Use profile-guided optimization (PGO)" << std::endl;

    std::cout << "\n6. Algorithm selection:" << std::endl;
    std::cout << "   - Choose right complexity (O(n) vs O(n log n) vs O(n²))" << std::endl;
    std::cout << "   - Use appropriate data structures" << std::endl;
    std::cout << "   - Consider trade-offs (time vs space)" << std::endl;
}

void demonstrateCompilerOptimizationFlags() {
    std::cout << "\n=== Compiler Optimization Flags ===" << std::endl;

    std::cout << "\nGCC/Clang optimization levels:" << std::endl;
    std::cout << "  -O0: No optimization (default, fast compilation)" << std::endl;
    std::cout << "  -O1: Basic optimizations" << std::endl;
    std::cout << "  -O2: Recommended optimizations (good balance)" << std::endl;
    std::cout << "  -O3: Aggressive optimizations (may increase code size)" << std::endl;
    std::cout << "  -Os: Optimize for size" << std::endl;
    std::cout << "  -Ofast: -O3 + fast math (non-standard compliant)" << std::endl;

    std::cout << "\nAdditional flags:" << std::endl;
    std::cout << "  -march=native: Optimize for current CPU" << std::endl;
    std::cout << "  -flto: Link-time optimization" << std::endl;
    std::cout << "  -fprofile-generate/use: Profile-guided optimization" << std::endl;
    std::cout << "  -finline-functions: Aggressive inlining" << std::endl;
}

int main() {
    std::cout << "Optimization Techniques Demonstration" << std::endl;
    std::cout << "=====================================" << std::endl;

    demonstrateCommonOptimizations();
    demonstrateCompilerOptimizationFlags();
    demonstrateLoopOptimization();
    demonstrateFunctionInlining();
    demonstrateMemoryAlignment();
    demonstrateBranchPrediction();
    demonstrateCacheLocality();
    demonstrateStringOptimization();
    demonstrateContainerChoice();
    demonstrateMoveSemantics();
    demonstrateConstCorrectness();

    std::cout << "\n=== Optimization Techniques Complete ===" << std::endl;
    std::cout << "\nBest practices:" << std::endl;
    std::cout << "  1. Profile first, optimize later" << std::endl;
    std::cout << "  2. Focus on algorithmic improvements" << std::endl;
    std::cout << "  3. Let compiler do its job (use -O2/-O3)" << std::endl;
    std::cout << "  4. Measure impact of optimizations" << std::endl;

    return 0;
}
