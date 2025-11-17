/*
 * Program 198: Benchmarking
 * Demonstrates micro-benchmarking and performance testing techniques
 * Compile: g++ -std=c++17 -O2 -o benchmarking main.cpp
 */

#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <string>
#include <functional>
#include <iomanip>

// Simple benchmark timer
class BenchmarkTimer {
private:
    std::chrono::high_resolution_clock::time_point start_time;
    std::string name;
    bool print_on_destroy;

public:
    BenchmarkTimer(const std::string& n, bool auto_print = true)
        : name(n), print_on_destroy(auto_print) {
        start_time = std::chrono::high_resolution_clock::now();
    }

    ~BenchmarkTimer() {
        if (print_on_destroy) {
            auto duration = elapsed();
            std::cout << name << ": " << duration << " ms" << std::endl;
        }
    }

    double elapsed() const {
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
            end_time - start_time);
        return duration.count() / 1000.0;
    }

    void reset() {
        start_time = std::chrono::high_resolution_clock::now();
    }
};

// Advanced benchmark with statistics
class Benchmark {
private:
    std::string name;
    std::vector<double> measurements;
    int warmup_iterations;
    int test_iterations;

public:
    Benchmark(const std::string& n, int warmup = 3, int iterations = 10)
        : name(n), warmup_iterations(warmup), test_iterations(iterations) {}

    template<typename Func>
    void run(Func func) {
        // Warmup
        for (int i = 0; i < warmup_iterations; ++i) {
            func();
        }

        // Actual measurements
        measurements.clear();
        for (int i = 0; i < test_iterations; ++i) {
            auto start = std::chrono::high_resolution_clock::now();
            func();
            auto end = std::chrono::high_resolution_clock::now();

            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
            measurements.push_back(duration.count() / 1000.0);
        }
    }

    void report() const {
        if (measurements.empty()) {
            std::cout << name << ": No measurements" << std::endl;
            return;
        }

        // Calculate statistics
        double sum = std::accumulate(measurements.begin(), measurements.end(), 0.0);
        double mean = sum / measurements.size();

        double variance = 0.0;
        for (double m : measurements) {
            variance += (m - mean) * (m - mean);
        }
        variance /= measurements.size();
        double stddev = std::sqrt(variance);

        std::vector<double> sorted = measurements;
        std::sort(sorted.begin(), sorted.end());
        double median = sorted[sorted.size() / 2];
        double min = sorted.front();
        double max = sorted.back();

        std::cout << "\n" << name << " Results:" << std::endl;
        std::cout << "  Iterations: " << measurements.size() << std::endl;
        std::cout << std::fixed << std::setprecision(3);
        std::cout << "  Mean:   " << mean << " ms" << std::endl;
        std::cout << "  Median: " << median << " ms" << std::endl;
        std::cout << "  StdDev: " << stddev << " ms (" << (stddev / mean * 100) << "%)" << std::endl;
        std::cout << "  Min:    " << min << " ms" << std::endl;
        std::cout << "  Max:    " << max << " ms" << std::endl;
    }

    double getMean() const {
        if (measurements.empty()) return 0.0;
        return std::accumulate(measurements.begin(), measurements.end(), 0.0) / measurements.size();
    }
};

void demonstrateBasicBenchmarking() {
    std::cout << "\n=== Basic Benchmarking ===" << std::endl;

    const int SIZE = 1000000;

    {
        BenchmarkTimer timer("Vector push_back");
        std::vector<int> vec;
        for (int i = 0; i < SIZE; ++i) {
            vec.push_back(i);
        }
    }

    {
        BenchmarkTimer timer("Vector with reserve");
        std::vector<int> vec;
        vec.reserve(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec.push_back(i);
        }
    }

    {
        BenchmarkTimer timer("Vector with resize");
        std::vector<int> vec(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec[i] = i;
        }
    }
}

void demonstrateWarmupEffect() {
    std::cout << "\n=== Warmup Effect ===" << std::endl;

    const int SIZE = 1000000;

    auto test_function = [&]() {
        std::vector<int> vec;
        vec.reserve(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec.push_back(i);
        }
    };

    std::cout << "Running without warmup:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        BenchmarkTimer timer("  Iteration " + std::to_string(i + 1));
        test_function();
    }

    std::cout << "\nNote: First run often slower due to:" << std::endl;
    std::cout << "  - Cache cold start" << std::endl;
    std::cout << "  - Memory allocation overhead" << std::endl;
    std::cout << "  - CPU frequency scaling" << std::endl;
}

void demonstrateStatisticalBenchmarking() {
    std::cout << "\n=== Statistical Benchmarking ===" << std::endl;

    const int SIZE = 500000;

    Benchmark bench1("Vector allocation");
    bench1.run([&]() {
        std::vector<int> vec(SIZE, 42);
    });
    bench1.report();

    Benchmark bench2("Vector sort");
    std::vector<int> data(SIZE);
    bench2.run([&]() {
        for (int i = 0; i < SIZE; ++i) {
            data[i] = SIZE - i;
        }
        std::sort(data.begin(), data.end());
    });
    bench2.report();
}

void demonstrateComparativeBenchmark() {
    std::cout << "\n=== Comparative Benchmark ===" << std::endl;

    const int SIZE = 1000000;

    Benchmark bench1("Approach 1: push_back");
    bench1.run([&]() {
        std::vector<int> vec;
        for (int i = 0; i < SIZE; ++i) {
            vec.push_back(i);
        }
    });

    Benchmark bench2("Approach 2: reserve + push_back");
    bench2.run([&]() {
        std::vector<int> vec;
        vec.reserve(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec.push_back(i);
        }
    });

    Benchmark bench3("Approach 3: resize + assign");
    bench3.run([&]() {
        std::vector<int> vec(SIZE);
        for (int i = 0; i < SIZE; ++i) {
            vec[i] = i;
        }
    });

    bench1.report();
    bench2.report();
    bench3.report();

    double mean1 = bench1.getMean();
    double mean2 = bench2.getMean();
    double mean3 = bench3.getMean();

    std::cout << "\nSpeedup Analysis:" << std::endl;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "  Approach 2 vs 1: " << (mean1 / mean2) << "x faster" << std::endl;
    std::cout << "  Approach 3 vs 1: " << (mean1 / mean3) << "x faster" << std::endl;
    std::cout << "  Approach 3 vs 2: " << (mean2 / mean3) << "x faster" << std::endl;
}

void demonstrateMicroBenchmarkPitfalls() {
    std::cout << "\n=== Micro-Benchmark Pitfalls ===" << std::endl;

    std::cout << "\n1. Dead Code Elimination:" << std::endl;
    std::cout << "   Problem: Compiler removes benchmark code" << std::endl;
    std::cout << "   Solution: Use volatile or return result" << std::endl;

    {
        BenchmarkTimer timer("Without volatile (may be optimized away)");
        int sum = 0;
        for (int i = 0; i < 10000000; ++i) {
            sum += i;
        }
    }

    {
        BenchmarkTimer timer("With volatile (prevents optimization)");
        volatile int sum = 0;
        for (int i = 0; i < 10000000; ++i) {
            sum += i;
        }
    }

    std::cout << "\n2. Loop Overhead:" << std::endl;
    std::cout << "   Benchmark the loop itself to subtract overhead" << std::endl;

    std::cout << "\n3. Cache Effects:" << std::endl;
    std::cout << "   First run may be slower (cold cache)" << std::endl;
    std::cout << "   Later runs faster (warm cache)" << std::endl;

    std::cout << "\n4. CPU Frequency Scaling:" << std::endl;
    std::cout << "   CPU may run at different speeds" << std::endl;
    std::cout << "   Use performance governor: sudo cpupower frequency-set -g performance" << std::endl;

    std::cout << "\n5. Background Processes:" << std::endl;
    std::cout << "   Other processes affect timing" << std::endl;
    std::cout << "   Run multiple iterations and use statistics" << std::endl;
}

void demonstrateBenchmarkingTools() {
    std::cout << "\n=== Benchmarking Tools ===" << std::endl;

    std::cout << "\n1. Google Benchmark:" << std::endl;
    std::cout << "   - Industry-standard C++ benchmarking library" << std::endl;
    std::cout << "   - Statistical analysis built-in" << std::endl;
    std::cout << "   - Example:" << std::endl;
    std::cout << "     static void BM_Function(benchmark::State& state) {" << std::endl;
    std::cout << "       for (auto _ : state) {" << std::endl;
    std::cout << "         function_to_benchmark();" << std::endl;
    std::cout << "       }" << std::endl;
    std::cout << "     }" << std::endl;
    std::cout << "     BENCHMARK(BM_Function);" << std::endl;

    std::cout << "\n2. Hayai:" << std::endl;
    std::cout << "   - C++ benchmarking framework" << std::endl;
    std::cout << "   - Easy to use" << std::endl;
    std::cout << "   - Similar to Google Benchmark" << std::endl;

    std::cout << "\n3. Catch2 Benchmarking:" << std::endl;
    std::cout << "   - Part of Catch2 testing framework" << std::endl;
    std::cout << "   - Combines testing and benchmarking" << std::endl;

    std::cout << "\n4. perf (Linux):" << std::endl;
    std::cout << "   - perf stat ./program" << std::endl;
    std::cout << "   - Shows hardware counters" << std::endl;
    std::cout << "   - Cache misses, branch mispredictions, etc." << std::endl;

    std::cout << "\n5. time command:" << std::endl;
    std::cout << "   - /usr/bin/time -v ./program" << std::endl;
    std::cout << "   - Quick resource usage summary" << std::endl;
}

void demonstrateBenchmarkBestPractices() {
    std::cout << "\n=== Benchmark Best Practices ===" << std::endl;

    std::cout << "\n1. Isolate What You're Measuring:" << std::endl;
    std::cout << "   - Benchmark only the code you care about" << std::endl;
    std::cout << "   - Exclude setup/teardown from measurements" << std::endl;
    std::cout << "   - Use RAII for automatic timing" << std::endl;

    std::cout << "\n2. Use Realistic Data:" << std::endl;
    std::cout << "   - Test with production-like datasets" << std::endl;
    std::cout << "   - Include edge cases" << std::endl;
    std::cout << "   - Consider data distribution" << std::endl;

    std::cout << "\n3. Warm Up:" << std::endl;
    std::cout << "   - Run several iterations before measuring" << std::endl;
    std::cout << "   - Ensures caches are warm" << std::endl;
    std::cout << "   - Stabilizes CPU frequency" << std::endl;

    std::cout << "\n4. Multiple Iterations:" << std::endl;
    std::cout << "   - Never trust a single measurement" << std::endl;
    std::cout << "   - Run 10-100 times" << std::endl;
    std::cout << "   - Calculate mean, median, stddev" << std::endl;
    std::cout << "   - Look for outliers" << std::endl;

    std::cout << "\n5. Control the Environment:" << std::endl;
    std::cout << "   - Disable CPU frequency scaling" << std::endl;
    std::cout << "   - Close unnecessary programs" << std::endl;
    std::cout << "   - Use consistent compiler flags" << std::endl;
    std::cout << "   - Test on target hardware" << std::endl;

    std::cout << "\n6. Prevent Optimization:" << std::endl;
    std::cout << "   - Use volatile for results" << std::endl;
    std::cout << "   - Call DoNotOptimize() helpers" << std::endl;
    std::cout << "   - Return values from functions" << std::endl;

    std::cout << "\n7. Document Everything:" << std::endl;
    std::cout << "   - Record compiler, version, flags" << std::endl;
    std::cout << "   - Note hardware specifications" << std::endl;
    std::cout << "   - Save benchmark results" << std::endl;
    std::cout << "   - Track changes over time" << std::endl;
}

void demonstrateRealWorldBenchmark() {
    std::cout << "\n=== Real-World Benchmark Example ===" << std::endl;

    // Simulate benchmarking a real algorithm
    std::cout << "\nBenchmarking: Finding prime numbers" << std::endl;

    auto count_primes = [](int n) {
        int count = 0;
        for (int i = 2; i <= n; ++i) {
            bool is_prime = true;
            for (int j = 2; j * j <= i; ++j) {
                if (i % j == 0) {
                    is_prime = false;
                    break;
                }
            }
            if (is_prime) count++;
        }
        return count;
    };

    auto count_primes_optimized = [](int n) {
        if (n < 2) return 0;
        int count = 1;  // 2 is prime
        for (int i = 3; i <= n; i += 2) {  // Skip even numbers
            bool is_prime = true;
            for (int j = 3; j * j <= i; j += 2) {
                if (i % j == 0) {
                    is_prime = false;
                    break;
                }
            }
            if (is_prime) count++;
        }
        return count;
    };

    const int N = 100000;

    Benchmark bench1("Naive algorithm");
    bench1.run([&]() {
        volatile int result = count_primes(N);
    });

    Benchmark bench2("Optimized algorithm");
    bench2.run([&]() {
        volatile int result = count_primes_optimized(N);
    });

    bench1.report();
    bench2.report();

    std::cout << "\nSpeedup: " << std::fixed << std::setprecision(2)
              << (bench1.getMean() / bench2.getMean()) << "x" << std::endl;
}

void demonstratePerformanceRegression() {
    std::cout << "\n=== Performance Regression Testing ===" << std::endl;

    std::cout << "\nWhat is regression testing?" << std::endl;
    std::cout << "  - Track performance over time" << std::endl;
    std::cout << "  - Detect when changes slow down code" << std::endl;
    std::cout << "  - Automate in CI/CD pipeline" << std::endl;

    std::cout << "\nHow to implement:" << std::endl;
    std::cout << "  1. Save baseline benchmarks" << std::endl;
    std::cout << "  2. Run benchmarks on every commit" << std::endl;
    std::cout << "  3. Compare against baseline" << std::endl;
    std::cout << "  4. Alert if slowdown > threshold (e.g., 10%)" << std::endl;

    std::cout << "\nExample workflow:" << std::endl;
    std::cout << "  - Baseline: Function takes 100ms" << std::endl;
    std::cout << "  - After change: Function takes 115ms" << std::endl;
    std::cout << "  - Regression: 15% slower -> Alert!" << std::endl;
}

int main() {
    std::cout << "Benchmarking Demonstration" << std::endl;
    std::cout << "==========================" << std::endl;

    demonstrateBasicBenchmarking();
    demonstrateWarmupEffect();
    demonstrateStatisticalBenchmarking();
    demonstrateComparativeBenchmark();
    demonstrateMicroBenchmarkPitfalls();
    demonstrateRealWorldBenchmark();
    demonstrateBenchmarkingTools();
    demonstrateBenchmarkBestPractices();
    demonstratePerformanceRegression();

    std::cout << "\n=== Benchmarking Complete ===" << std::endl;
    std::cout << "\nKey takeaways:" << std::endl;
    std::cout << "  1. Always warm up before measuring" << std::endl;
    std::cout << "  2. Run multiple iterations" << std::endl;
    std::cout << "  3. Use statistics (mean, median, stddev)" << std::endl;
    std::cout << "  4. Control the environment" << std::endl;
    std::cout << "  5. Document everything" << std::endl;

    return 0;
}
