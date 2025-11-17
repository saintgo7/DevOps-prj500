/*
 * Program 193: Performance Profiling
 * Demonstrates profiling tools, performance analysis, and timing
 * Compile: g++ -std=c++17 -pg -o performance_profiling main.cpp
 * Run gprof: gprof performance_profiling gmon.out > analysis.txt
 */

#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>
#include <cmath>
#include <sys/time.h>
#include <sys/resource.h>
#include <unistd.h>
#include <fstream>

// Timer class for measuring execution time
class PerformanceTimer {
private:
    std::chrono::high_resolution_clock::time_point start_time;
    std::string operation_name;

public:
    PerformanceTimer(const std::string& name) : operation_name(name) {
        start_time = std::chrono::high_resolution_clock::now();
    }

    ~PerformanceTimer() {
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
            end_time - start_time);

        std::cout << operation_name << ": " << duration.count() << " μs"
                  << " (" << (duration.count() / 1000.0) << " ms)" << std::endl;
    }

    double elapsed_ms() const {
        auto current = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
            current - start_time);
        return duration.count() / 1000.0;
    }
};

// Manual timing wrapper
template<typename Func>
double measureExecutionTime(const std::string& name, Func func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    double ms = duration.count() / 1000.0;

    std::cout << name << ": " << ms << " ms" << std::endl;
    return ms;
}

// Test function 1: Heavy computation
void heavyComputation() {
    double result = 0;
    for (int i = 0; i < 1000000; ++i) {
        result += std::sqrt(i) * std::sin(i);
    }
}

// Test function 2: Memory allocation
void memoryAllocation() {
    std::vector<int> vec;
    for (int i = 0; i < 100000; ++i) {
        vec.push_back(i);
    }
}

// Test function 3: String operations
void stringOperations() {
    std::string result;
    for (int i = 0; i < 10000; ++i) {
        result += "test";
    }
}

// Test function 4: Vector operations
void vectorOperations() {
    std::vector<int> vec(100000);
    for (int i = 0; i < 100000; ++i) {
        vec[i] = i * 2;
    }

    std::sort(vec.begin(), vec.end());
}

void demonstrateBasicTiming() {
    std::cout << "\n=== Basic Performance Timing ===" << std::endl;

    {
        PerformanceTimer timer("Heavy Computation");
        heavyComputation();
    }

    {
        PerformanceTimer timer("Memory Allocation");
        memoryAllocation();
    }

    {
        PerformanceTimer timer("String Operations");
        stringOperations();
    }

    {
        PerformanceTimer timer("Vector Operations");
        vectorOperations();
    }
}

void demonstrateHighResolutionTiming() {
    std::cout << "\n=== High-Resolution Timing ===" << std::endl;

    auto start = std::chrono::high_resolution_clock::now();

    // Quick operation
    volatile int sum = 0;
    for (int i = 0; i < 1000; ++i) {
        sum += i;
    }

    auto end = std::chrono::high_resolution_clock::now();

    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
    auto us = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();

    std::cout << "Quick operation timing:" << std::endl;
    std::cout << "  Nanoseconds: " << ns << " ns" << std::endl;
    std::cout << "  Microseconds: " << us << " μs" << std::endl;
    std::cout << "  Milliseconds: " << ms << " ms" << std::endl;
}

void demonstrateCPUTime() {
    std::cout << "\n=== CPU Time Measurement ===" << std::endl;

    clock_t start_clock = clock();

    // Do some work
    heavyComputation();

    clock_t end_clock = clock();

    double cpu_time = static_cast<double>(end_clock - start_clock) / CLOCKS_PER_SEC;

    std::cout << "CPU time used: " << cpu_time << " seconds" << std::endl;
    std::cout << "CLOCKS_PER_SEC: " << CLOCKS_PER_SEC << std::endl;
}

void demonstrateResourceUsage() {
    std::cout << "\n=== Resource Usage Profiling ===" << std::endl;

    struct rusage usage_start, usage_end;

    getrusage(RUSAGE_SELF, &usage_start);

    // Do some work
    heavyComputation();
    memoryAllocation();

    getrusage(RUSAGE_SELF, &usage_end);

    // Calculate differences
    long user_time_us = (usage_end.ru_utime.tv_sec - usage_start.ru_utime.tv_sec) * 1000000 +
                        (usage_end.ru_utime.tv_usec - usage_start.ru_utime.tv_usec);

    long sys_time_us = (usage_end.ru_stime.tv_sec - usage_start.ru_stime.tv_sec) * 1000000 +
                       (usage_end.ru_stime.tv_usec - usage_start.ru_stime.tv_usec);

    std::cout << "Resource usage:" << std::endl;
    std::cout << "  User CPU time: " << (user_time_us / 1000.0) << " ms" << std::endl;
    std::cout << "  System CPU time: " << (sys_time_us / 1000.0) << " ms" << std::endl;
    std::cout << "  Max RSS: " << usage_end.ru_maxrss << " KB" << std::endl;
    std::cout << "  Minor page faults: " << usage_end.ru_minflt << std::endl;
    std::cout << "  Major page faults: " << usage_end.ru_majflt << std::endl;
    std::cout << "  Voluntary context switches: " << usage_end.ru_nvcsw << std::endl;
    std::cout << "  Involuntary context switches: " << usage_end.ru_nivcsw << std::endl;
}

void demonstrateFunctionProfiling() {
    std::cout << "\n=== Function-Level Profiling ===" << std::endl;

    std::cout << "Profiling individual functions:" << std::endl;

    measureExecutionTime("Function 1 (Computation)", heavyComputation);
    measureExecutionTime("Function 2 (Memory)", memoryAllocation);
    measureExecutionTime("Function 3 (Strings)", stringOperations);
    measureExecutionTime("Function 4 (Vectors)", vectorOperations);
}

void demonstrateComparativeAnalysis() {
    std::cout << "\n=== Comparative Performance Analysis ===" << std::endl;

    // Compare different approaches
    std::cout << "\n1. Vector initialization comparison:" << std::endl;

    auto time1 = measureExecutionTime("  push_back", []() {
        std::vector<int> vec;
        for (int i = 0; i < 100000; ++i) {
            vec.push_back(i);
        }
    });

    auto time2 = measureExecutionTime("  resize + assign", []() {
        std::vector<int> vec(100000);
        for (int i = 0; i < 100000; ++i) {
            vec[i] = i;
        }
    });

    auto time3 = measureExecutionTime("  reserve + push_back", []() {
        std::vector<int> vec;
        vec.reserve(100000);
        for (int i = 0; i < 100000; ++i) {
            vec.push_back(i);
        }
    });

    std::cout << "\n  Speedup (resize vs push_back): " << (time1 / time2) << "x" << std::endl;
    std::cout << "  Speedup (reserve vs push_back): " << (time1 / time3) << "x" << std::endl;

    // Compare string concatenation
    std::cout << "\n2. String concatenation comparison:" << std::endl;

    auto str_time1 = measureExecutionTime("  operator+=", []() {
        std::string result;
        for (int i = 0; i < 10000; ++i) {
            result += "test";
        }
    });

    auto str_time2 = measureExecutionTime("  reserve + operator+=", []() {
        std::string result;
        result.reserve(50000);
        for (int i = 0; i < 10000; ++i) {
            result += "test";
        }
    });

    std::cout << "  Speedup (reserve): " << (str_time1 / str_time2) << "x" << std::endl;
}

void demonstrateHotspotIdentification() {
    std::cout << "\n=== Hotspot Identification ===" << std::endl;

    std::cout << "Identifying performance bottlenecks:" << std::endl;

    struct Function {
        std::string name;
        double time_ms;
    };

    std::vector<Function> functions;

    functions.push_back({"Math operations", measureExecutionTime("", []() {
        double result = 0;
        for (int i = 0; i < 1000000; ++i) {
            result += std::sqrt(i) * std::sin(i);
        }
    })});

    functions.push_back({"Vector sort", measureExecutionTime("", []() {
        std::vector<int> vec(100000);
        for (int i = 0; i < 100000; ++i) {
            vec[i] = rand();
        }
        std::sort(vec.begin(), vec.end());
    })});

    functions.push_back({"File I/O", measureExecutionTime("", []() {
        std::ofstream file("/tmp/profile_test.dat");
        for (int i = 0; i < 10000; ++i) {
            file << i << "\n";
        }
        file.close();
        unlink("/tmp/profile_test.dat");
    })});

    // Calculate total time
    double total_time = 0;
    for (const auto& func : functions) {
        total_time += func.time_ms;
    }

    // Sort by time (descending)
    std::sort(functions.begin(), functions.end(),
             [](const Function& a, const Function& b) {
                 return a.time_ms > b.time_ms;
             });

    std::cout << "\nHotspots (sorted by time):" << std::endl;
    for (const auto& func : functions) {
        double percentage = (func.time_ms / total_time) * 100;
        std::cout << "  " << func.name << ": " << func.time_ms << " ms ("
                  << percentage << "%)" << std::endl;
    }
}

void demonstrateMemoryProfiling() {
    std::cout << "\n=== Memory Profiling ===" << std::endl;

    struct rusage usage;

    std::cout << "Initial memory usage:" << std::endl;
    getrusage(RUSAGE_SELF, &usage);
    long initial_rss = usage.ru_maxrss;
    std::cout << "  Max RSS: " << initial_rss << " KB" << std::endl;

    // Allocate memory
    std::vector<std::vector<int>> large_data;
    for (int i = 0; i < 100; ++i) {
        large_data.push_back(std::vector<int>(10000, i));
    }

    std::cout << "\nAfter allocation:" << std::endl;
    getrusage(RUSAGE_SELF, &usage);
    long after_alloc_rss = usage.ru_maxrss;
    std::cout << "  Max RSS: " << after_alloc_rss << " KB" << std::endl;
    std::cout << "  Increase: " << (after_alloc_rss - initial_rss) << " KB" << std::endl;

    // Clear memory
    large_data.clear();

    std::cout << "\nAfter deallocation:" << std::endl;
    getrusage(RUSAGE_SELF, &usage);
    std::cout << "  Max RSS: " << usage.ru_maxrss << " KB" << std::endl;
}

void demonstrateProfilingTools() {
    std::cout << "\n=== Profiling Tools Overview ===" << std::endl;

    std::cout << "\n1. gprof (GNU Profiler):" << std::endl;
    std::cout << "   - Compile with -pg flag" << std::endl;
    std::cout << "   - Run program to generate gmon.out" << std::endl;
    std::cout << "   - Analyze: gprof program gmon.out > analysis.txt" << std::endl;

    std::cout << "\n2. perf (Linux):" << std::endl;
    std::cout << "   - perf record ./program" << std::endl;
    std::cout << "   - perf report" << std::endl;
    std::cout << "   - Hardware counter-based profiling" << std::endl;

    std::cout << "\n3. valgrind (callgrind):" << std::endl;
    std::cout << "   - valgrind --tool=callgrind ./program" << std::endl;
    std::cout << "   - kcachegrind callgrind.out.*" << std::endl;
    std::cout << "   - Detailed call graph analysis" << std::endl;

    std::cout << "\n4. valgrind (massif - memory profiler):" << std::endl;
    std::cout << "   - valgrind --tool=massif ./program" << std::endl;
    std::cout << "   - ms_print massif.out.*" << std::endl;

    std::cout << "\n5. time command:" << std::endl;
    std::cout << "   - /usr/bin/time -v ./program" << std::endl;
    std::cout << "   - Quick resource usage summary" << std::endl;

    std::cout << "\n6. Custom instrumentation:" << std::endl;
    std::cout << "   - Manual timers (like this program)" << std::endl;
    std::cout << "   - getrusage() for resource tracking" << std::endl;
    std::cout << "   - clock_gettime() for precise timing" << std::endl;
}

void demonstrateCacheProfiling() {
    std::cout << "\n=== Cache Performance Analysis ===" << std::endl;

    const int SIZE = 10000000;
    std::vector<int> data(SIZE);

    // Sequential access (cache-friendly)
    auto seq_time = measureExecutionTime("Sequential access", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            sum += data[i];
        }
    });

    // Strided access (less cache-friendly)
    auto stride_time = measureExecutionTime("Strided access (stride=16)", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; i += 16) {
            sum += data[i];
        }
    });

    std::cout << "\nCache impact:" << std::endl;
    std::cout << "  Sequential is the baseline" << std::endl;
    std::cout << "  Note: Strided accesses fewer elements but shows cache effects" << std::endl;
}

int main() {
    std::cout << "Performance Profiling Demonstration" << std::endl;
    std::cout << "====================================" << std::endl;

    demonstrateProfilingTools();
    demonstrateBasicTiming();
    demonstrateHighResolutionTiming();
    demonstrateCPUTime();
    demonstrateResourceUsage();
    demonstrateFunctionProfiling();
    demonstrateComparativeAnalysis();
    demonstrateHotspotIdentification();
    demonstrateMemoryProfiling();
    demonstrateCacheProfiling();

    std::cout << "\n=== Performance Profiling Complete ===" << std::endl;
    std::cout << "\nNote: Compile with -pg for gprof profiling:" << std::endl;
    std::cout << "  g++ -std=c++17 -pg -o program main.cpp" << std::endl;
    std::cout << "  ./program" << std::endl;
    std::cout << "  gprof program gmon.out > analysis.txt" << std::endl;

    return 0;
}
