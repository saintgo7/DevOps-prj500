/*
 * Program 197: Compiler Optimization
 * Demonstrates compiler flags, optimization levels, and techniques
 * Compile with different flags to see the effects:
 *   g++ -std=c++17 -O0 -o program_O0 main.cpp
 *   g++ -std=c++17 -O2 -o program_O2 main.cpp
 *   g++ -std=c++17 -O3 -march=native -o program_O3 main.cpp
 */

#include <iostream>
#include <chrono>
#include <vector>
#include <cmath>

// Performance measurement
template<typename Func>
double measure(const std::string& name, Func func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    double ms = duration.count() / 1000.0;

    std::cout << name << ": " << ms << " ms" << std::endl;
    return ms;
}

void demonstrateOptimizationLevels() {
    std::cout << "\n=== Compiler Optimization Levels ===" << std::endl;

    std::cout << "\n-O0 (No Optimization):" << std::endl;
    std::cout << "  - Fastest compilation" << std::endl;
    std::cout << "  - Best for debugging" << std::endl;
    std::cout << "  - Produces largest, slowest code" << std::endl;
    std::cout << "  - Debug symbols work best" << std::endl;

    std::cout << "\n-O1 (Basic Optimization):" << std::endl;
    std::cout << "  - Moderate compilation time" << std::endl;
    std::cout << "  - Basic optimizations" << std::endl;
    std::cout << "  - Reduces code size and execution time" << std::endl;
    std::cout << "  - Still debuggable" << std::endl;

    std::cout << "\n-O2 (Recommended):" << std::endl;
    std::cout << "  - Most common for production" << std::endl;
    std::cout << "  - Nearly all optimizations" << std::endl;
    std::cout << "  - Good balance of speed vs compilation time" << std::endl;
    std::cout << "  - Includes:" << std::endl;
    std::cout << "    * Function inlining" << std::endl;
    std::cout << "    * Dead code elimination" << std::endl;
    std::cout << "    * Common subexpression elimination" << std::endl;
    std::cout << "    * Loop optimizations" << std::endl;

    std::cout << "\n-O3 (Aggressive):" << std::endl;
    std::cout << "  - All -O2 optimizations plus:" << std::endl;
    std::cout << "  - Auto-vectorization" << std::endl;
    std::cout << "  - More aggressive inlining" << std::endl;
    std::cout << "  - Loop unrolling" << std::endl;
    std::cout << "  - May increase code size" << std::endl;
    std::cout << "  - Sometimes slower than -O2!" << std::endl;

    std::cout << "\n-Os (Size Optimization):" << std::endl;
    std::cout << "  - Like -O2 but optimizes for size" << std::endl;
    std::cout << "  - Good for embedded systems" << std::endl;
    std::cout << "  - Disables optimizations that increase size" << std::endl;

    std::cout << "\n-Ofast (Fast Math):" << std::endl;
    std::cout << "  - All -O3 optimizations" << std::endl;
    std::cout << "  - Disregards strict standards compliance" << std::endl;
    std::cout << "  - Enables -ffast-math" << std::endl;
    std::cout << "  - WARNING: May produce incorrect results!" << std::endl;

    std::cout << "\n-Og (Debug Optimizations):" << std::endl;
    std::cout << "  - Optimizations that don't interfere with debugging" << std::endl;
    std::cout << "  - Better than -O0, more debuggable than -O1" << std::endl;
}

void demonstrateSpecificOptimizations() {
    std::cout << "\n=== Specific Optimization Flags ===" << std::endl;

    std::cout << "\nInlining:" << std::endl;
    std::cout << "  -finline-functions       Inline small functions" << std::endl;
    std::cout << "  -finline-limit=n         Set inlining threshold" << std::endl;
    std::cout << "  -fno-inline              Disable inlining" << std::endl;

    std::cout << "\nLoop Optimizations:" << std::endl;
    std::cout << "  -funroll-loops           Unroll loops" << std::endl;
    std::cout << "  -ftree-vectorize         Enable auto-vectorization" << std::endl;
    std::cout << "  -floop-interchange       Swap nested loops for cache" << std::endl;

    std::cout << "\nFunction Optimizations:" << std::endl;
    std::cout << "  -fomit-frame-pointer     Remove frame pointer" << std::endl;
    std::cout << "  -ffunction-sections      Each function in own section" << std::endl;
    std::cout << "  -fdata-sections          Each data in own section" << std::endl;

    std::cout << "\nLink-Time Optimization:" << std::endl;
    std::cout << "  -flto                    Enable LTO" << std::endl;
    std::cout << "  -flto=8                  LTO with 8 parallel jobs" << std::endl;

    std::cout << "\nArchitecture-Specific:" << std::endl;
    std::cout << "  -march=native            Optimize for current CPU" << std::endl;
    std::cout << "  -march=x86-64            Generic x86-64" << std::endl;
    std::cout << "  -mtune=skylake           Tune for Skylake" << std::endl;
}

// Test function that benefits from optimization
int __attribute__((noinline)) unoptimizedFunction(int n) {
    int result = 0;
    for (int i = 0; i < n; ++i) {
        result += i;
        result *= 2;
        result /= 2;
    }
    return result;
}

// Inline hint for compiler
inline int optimizedFunction(int n) {
    int result = 0;
    for (int i = 0; i < n; ++i) {
        result += i;
    }
    return result;
}

void demonstrateInlining() {
    std::cout << "\n=== Function Inlining ===" << std::endl;

    const int ITERATIONS = 100000000;

    auto time1 = measure("Non-inline function calls", [&]() {
        volatile int result = 0;
        for (int i = 0; i < 1000000; ++i) {
            result = unoptimizedFunction(100);
        }
    });

    auto time2 = measure("Inline function calls", [&]() {
        volatile int result = 0;
        for (int i = 0; i < 1000000; ++i) {
            result = optimizedFunction(100);
        }
    });

    std::cout << "\nNote: Compiler may inline both with -O2/-O3" << std::endl;
}

void demonstrateDeadCodeElimination() {
    std::cout << "\n=== Dead Code Elimination ===" << std::endl;

    std::cout << "\nDead code example:" << std::endl;
    std::cout << "  int unused = expensive_computation();" << std::endl;
    std::cout << "  // 'unused' is never used" << std::endl;
    std::cout << "  return 42;" << std::endl;

    std::cout << "\nCompiler removes:" << std::endl;
    std::cout << "  - Unused variables" << std::endl;
    std::cout << "  - Unreachable code" << std::endl;
    std::cout << "  - Unused functions" << std::endl;

    auto time1 = measure("With dead code", [&]() {
        for (int i = 0; i < 1000000; ++i) {
            int unused = i * 2;  // Dead code
            volatile int result = 42;
        }
    });

    auto time2 = measure("Without dead code", [&]() {
        for (int i = 0; i < 1000000; ++i) {
            volatile int result = 42;
        }
    });

    std::cout << "Note: Optimizer removes dead code automatically" << std::endl;
}

void demonstrateConstantFolding() {
    std::cout << "\n=== Constant Folding ===" << std::endl;

    std::cout << "\nConstant folding examples:" << std::endl;
    std::cout << "  int x = 2 + 3;           -> int x = 5;" << std::endl;
    std::cout << "  int y = 10 * 20;         -> int y = 200;" << std::endl;
    std::cout << "  float z = sqrt(16.0);    -> float z = 4.0;" << std::endl;

    const int a = 5;
    const int b = 10;

    auto time1 = measure("Runtime calculation", [&]() {
        volatile int result = 0;
        for (int i = 0; i < 10000000; ++i) {
            result = (i + 5) * 10;  // Could be partially folded
        }
    });

    auto time2 = measure("Compile-time constant", [&]() {
        volatile int result = 0;
        constexpr int factor = 5 * 10;
        for (int i = 0; i < 10000000; ++i) {
            result = i + factor;
        }
    });
}

void demonstrateLoopOptimizations() {
    std::cout << "\n=== Loop Optimizations ===" << std::endl;

    const int SIZE = 10000000;
    std::vector<int> data(SIZE, 1);

    std::cout << "\n1. Loop Unrolling:" << std::endl;
    std::cout << "   Processes multiple iterations per loop" << std::endl;

    auto time1 = measure("Normal loop", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            sum += data[i];
        }
        volatile long result = sum;
    });

    auto time2 = measure("Manually unrolled (4x)", [&]() {
        long sum = 0;
        int i;
        for (i = 0; i + 3 < SIZE; i += 4) {
            sum += data[i] + data[i + 1] + data[i + 2] + data[i + 3];
        }
        for (; i < SIZE; ++i) {
            sum += data[i];
        }
        volatile long result = sum;
    });

    std::cout << "\n2. Loop Vectorization:" << std::endl;
    std::cout << "   Uses SIMD instructions automatically" << std::endl;
    std::cout << "   Enable with -ftree-vectorize (included in -O3)" << std::endl;

    std::cout << "\n3. Loop Interchange:" << std::endl;
    std::cout << "   Swaps nested loops for better cache locality" << std::endl;
}

void demonstrateLinkTimeOptimization() {
    std::cout << "\n=== Link-Time Optimization (LTO) ===" << std::endl;

    std::cout << "\nWhat is LTO?" << std::endl;
    std::cout << "  - Optimizes across translation units" << std::endl;
    std::cout << "  - Enables whole-program optimization" << std::endl;
    std::cout << "  - Inlines functions across files" << std::endl;
    std::cout << "  - Removes unused code globally" << std::endl;

    std::cout << "\nHow to use LTO:" << std::endl;
    std::cout << "  1. Compile:  g++ -std=c++17 -O2 -flto -c file.cpp" << std::endl;
    std::cout << "  2. Link:     g++ -std=c++17 -O2 -flto -o program *.o" << std::endl;

    std::cout << "\nBenefits:" << std::endl;
    std::cout << "  - 5-15% performance improvement typical" << std::endl;
    std::cout << "  - Smaller binary size" << std::endl;
    std::cout << "  - Better inlining decisions" << std::endl;

    std::cout << "\nDrawbacks:" << std::endl;
    std::cout << "  - Longer compilation time" << std::endl;
    std::cout << "  - Higher memory usage during link" << std::endl;
}

void demonstrateProfileGuidedOptimization() {
    std::cout << "\n=== Profile-Guided Optimization (PGO) ===" << std::endl;

    std::cout << "\nHow PGO works:" << std::endl;
    std::cout << "  1. Compile with instrumentation" << std::endl;
    std::cout << "     g++ -O2 -fprofile-generate -o program main.cpp" << std::endl;

    std::cout << "\n  2. Run program with typical workload" << std::endl;
    std::cout << "     ./program < typical_input" << std::endl;
    std::cout << "     (generates *.gcda files)" << std::endl;

    std::cout << "\n  3. Recompile using profile data" << std::endl;
    std::cout << "     g++ -O2 -fprofile-use -o program main.cpp" << std::endl;

    std::cout << "\nBenefits:" << std::endl;
    std::cout << "  - Better branch prediction" << std::endl;
    std::cout << "  - Optimized code layout (hot/cold paths)" << std::endl;
    std::cout << "  - More accurate inlining decisions" << std::endl;
    std::cout << "  - 10-20% speedup possible" << std::endl;

    std::cout << "\nBest for:" << std::endl;
    std::cout << "  - Production builds" << std::endl;
    std::cout << "  - Long-running applications" << std::endl;
    std::cout << "  - Applications with clear typical usage" << std::endl;
}

void demonstrateOptimizationReports() {
    std::cout << "\n=== Optimization Reports ===" << std::endl;

    std::cout << "\nGCC/Clang flags to see what compiler does:" << std::endl;

    std::cout << "\nVectorization:" << std::endl;
    std::cout << "  -fopt-info-vec               Show vectorization info" << std::endl;
    std::cout << "  -fopt-info-vec-missed        Show failed vectorization" << std::endl;
    std::cout << "  -fopt-info-vec-all           Detailed vectorization info" << std::endl;

    std::cout << "\nInlining:" << std::endl;
    std::cout << "  -fopt-info-inline            Show inlining decisions" << std::endl;
    std::cout << "  -Winline                     Warn when inlining fails" << std::endl;

    std::cout << "\nAll optimizations:" << std::endl;
    std::cout << "  -fopt-info                   Show all optimizations" << std::endl;
    std::cout << "  -fopt-info-all               Detailed optimization info" << std::endl;

    std::cout << "\nExample:" << std::endl;
    std::cout << "  g++ -O3 -march=native -fopt-info-vec main.cpp" << std::endl;
}

void demonstratePragmaOptimizations() {
    std::cout << "\n=== Pragma Directives for Optimization ===" << std::endl;

    std::cout << "\nGCC/Clang pragmas:" << std::endl;

    std::cout << "\n1. Vectorization hints:" << std::endl;
    std::cout << "   #pragma GCC ivdep            // Ignore dependencies" << std::endl;
    std::cout << "   #pragma omp simd             // OpenMP vectorization" << std::endl;

    std::cout << "\n2. Unrolling hints:" << std::endl;
    std::cout << "   #pragma GCC unroll 4         // Unroll 4 times" << std::endl;
    std::cout << "   #pragma unroll               // Let compiler decide" << std::endl;

    std::cout << "\n3. Optimization level per-function:" << std::endl;
    std::cout << "   #pragma GCC optimize(\"O3\")   // Optimize function" << std::endl;

    std::cout << "\n4. Attributes:" << std::endl;
    std::cout << "   __attribute__((hot))         // Mark hot function" << std::endl;
    std::cout << "   __attribute__((cold))        // Mark cold function" << std::endl;
    std::cout << "   __attribute__((pure))        // Function has no side effects" << std::endl;
    std::cout << "   __attribute__((const))       // Function only uses arguments" << std::endl;
}

void demonstrateCompilationPipeline() {
    std::cout << "\n=== Compilation Pipeline ===" << std::endl;

    std::cout << "\nStages:" << std::endl;
    std::cout << "  1. Preprocessing    (-E flag to stop here)" << std::endl;
    std::cout << "  2. Compilation      (-S flag to see assembly)" << std::endl;
    std::cout << "  3. Assembly         (-c flag to get object file)" << std::endl;
    std::cout << "  4. Linking          (final executable)" << std::endl;

    std::cout << "\nOptimization happens:" << std::endl;
    std::cout << "  - During compilation (most optimizations)" << std::endl;
    std::cout << "  - During linking (LTO)" << std::endl;

    std::cout << "\nUseful commands:" << std::endl;
    std::cout << "  g++ -S -O3 main.cpp          # See optimized assembly" << std::endl;
    std::cout << "  objdump -d program           # Disassemble binary" << std::endl;
    std::cout << "  nm program                   # List symbols" << std::endl;
    std::cout << "  size program                 # Show section sizes" << std::endl;
}

void demonstrateBestPractices() {
    std::cout << "\n=== Optimization Best Practices ===" << std::endl;

    std::cout << "\n1. Development vs Production:" << std::endl;
    std::cout << "   Development: -Og or -O0 (fast compile, debuggable)" << std::endl;
    std::cout << "   Production:  -O2 or -O3 -march=native -flto" << std::endl;

    std::cout << "\n2. Recommended flags for production:" << std::endl;
    std::cout << "   g++ -std=c++17 -O3 -march=native -flto \\" << std::endl;
    std::cout << "       -fno-exceptions (if not using exceptions) \\" << std::endl;
    std::cout << "       -DNDEBUG (disable asserts) \\" << std::endl;
    std::cout << "       -o program main.cpp" << std::endl;

    std::cout << "\n3. Profile before optimizing:" << std::endl;
    std::cout << "   - Use profiling tools (gprof, perf)" << std::endl;
    std::cout << "   - Find hot spots first" << std::endl;
    std::cout << "   - Don't optimize prematurely" << std::endl;

    std::cout << "\n4. Measure everything:" << std::endl;
    std::cout << "   - Benchmark before and after" << std::endl;
    std::cout << "   - Test with realistic data" << std::endl;
    std::cout << "   - Watch for regressions" << std::endl;

    std::cout << "\n5. Safety first:" << std::endl;
    std::cout << "   - Avoid -Ofast unless necessary" << std::endl;
    std::cout << "   - Test thoroughly with optimizations" << std::endl;
    std::cout << "   - Be careful with undefined behavior" << std::endl;
}

int main() {
    std::cout << "Compiler Optimization Demonstration" << std::endl;
    std::cout << "====================================" << std::endl;

    demonstrateOptimizationLevels();
    demonstrateSpecificOptimizations();
    demonstrateInlining();
    demonstrateDeadCodeElimination();
    demonstrateConstantFolding();
    demonstrateLoopOptimizations();
    demonstrateLinkTimeOptimization();
    demonstrateProfileGuidedOptimization();
    demonstrateOptimizationReports();
    demonstratePragmaOptimizations();
    demonstrateCompilationPipeline();
    demonstrateBestPractices();

    std::cout << "\n=== Compiler Optimization Complete ===" << std::endl;
    std::cout << "\nTo see optimization effects, compile this program with:" << std::endl;
    std::cout << "  g++ -std=c++17 -O0 main.cpp  (no optimization)" << std::endl;
    std::cout << "  g++ -std=c++17 -O2 main.cpp  (recommended)" << std::endl;
    std::cout << "  g++ -std=c++17 -O3 -march=native main.cpp  (maximum)" << std::endl;

    return 0;
}
