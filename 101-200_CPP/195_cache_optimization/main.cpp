/*
 * Program 195: Cache Optimization
 * Demonstrates cache-friendly code and data structure optimization
 * Compile: g++ -std=c++17 -O2 -o cache_optimization main.cpp
 */

#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <cstdlib>
#include <cstring>

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

void demonstrateCacheLineSize() {
    std::cout << "\n=== Cache Line Size ===" << std::endl;

    // Typical cache line size is 64 bytes on modern CPUs
    std::cout << "Typical cache line size: 64 bytes" << std::endl;

#ifdef __linux__
    // Read from sysfs (Linux-specific)
    system("cat /sys/devices/system/cpu/cpu0/cache/index0/coherency_line_size 2>/dev/null || echo 'Cache info not available'");
#endif

    std::cout << "\nImplications:" << std::endl;
    std::cout << "  - 64 bytes = 16 ints or 8 doubles" << std::endl;
    std::cout << "  - Accessing one element loads entire cache line" << std::endl;
    std::cout << "  - Spatial locality is crucial" << std::endl;
}

void demonstrateSequentialVsRandom() {
    std::cout << "\n=== Sequential vs Random Access ===" << std::endl;

    const int SIZE = 10000000;
    std::vector<int> data(SIZE);

    // Fill with data
    for (int i = 0; i < SIZE; ++i) {
        data[i] = i;
    }

    // Sequential access (cache-friendly)
    auto time1 = measure("Sequential access", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            sum += data[i];
        }
        volatile long result = sum;  // Prevent optimization
    });

    // Random indices
    std::vector<int> indices(SIZE);
    for (int i = 0; i < SIZE; ++i) {
        indices[i] = i;
    }
    std::random_shuffle(indices.begin(), indices.end());

    // Random access (cache-unfriendly)
    auto time2 = measure("Random access", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; ++i) {
            sum += data[indices[i]];
        }
        volatile long result = sum;
    });

    std::cout << "Slowdown factor: " << (time2 / time1) << "x" << std::endl;
}

void demonstrateStridePattern() {
    std::cout << "\n=== Stride Patterns ===" << std::endl;

    const int SIZE = 10000000;
    std::vector<int> data(SIZE, 1);

    // Stride 1 (sequential)
    auto time1 = measure("Stride 1 (sequential)", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; i += 1) {
            sum += data[i];
        }
        volatile long result = sum;
    });

    // Stride 2
    auto time2 = measure("Stride 2", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; i += 2) {
            sum += data[i];
        }
        volatile long result = sum;
    });

    // Stride 8
    auto time3 = measure("Stride 8", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; i += 8) {
            sum += data[i];
        }
        volatile long result = sum;
    });

    // Stride 16
    auto time4 = measure("Stride 16", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; i += 16) {
            sum += data[i];
        }
        volatile long result = sum;
    });

    std::cout << "\nNote: Larger strides = more cache misses per element accessed" << std::endl;
}

void demonstrateAoSvsSoA() {
    std::cout << "\n=== Array of Structures vs Structure of Arrays ===" << std::endl;

    const int SIZE = 1000000;

    // Array of Structures (AoS)
    struct Particle {
        float x, y, z;
        float vx, vy, vz;
    };

    std::vector<Particle> aos(SIZE);

    for (int i = 0; i < SIZE; ++i) {
        aos[i] = {1.0f, 2.0f, 3.0f, 0.1f, 0.2f, 0.3f};
    }

    // Structure of Arrays (SoA)
    struct ParticlesSoA {
        std::vector<float> x, y, z;
        std::vector<float> vx, vy, vz;

        ParticlesSoA(int size) : x(size), y(size), z(size),
                                  vx(size), vy(size), vz(size) {}
    };

    ParticlesSoA soa(SIZE);

    for (int i = 0; i < SIZE; ++i) {
        soa.x[i] = 1.0f;
        soa.y[i] = 2.0f;
        soa.z[i] = 3.0f;
        soa.vx[i] = 0.1f;
        soa.vy[i] = 0.2f;
        soa.vz[i] = 0.3f;
    }

    // Update only positions (AoS)
    auto time1 = measure("AoS position update", [&]() {
        for (int i = 0; i < SIZE; ++i) {
            aos[i].x += aos[i].vx;
            aos[i].y += aos[i].vy;
            aos[i].z += aos[i].vz;
        }
    });

    // Update only positions (SoA)
    auto time2 = measure("SoA position update", [&]() {
        for (int i = 0; i < SIZE; ++i) {
            soa.x[i] += soa.vx[i];
            soa.y[i] += soa.vy[i];
            soa.z[i] += soa.vz[i];
        }
    });

    std::cout << "Speedup (SoA): " << (time1 / time2) << "x" << std::endl;
    std::cout << "\nWhen to use:" << std::endl;
    std::cout << "  AoS: When accessing all fields of single object" << std::endl;
    std::cout << "  SoA: When processing same field across many objects" << std::endl;
}

void demonstrateMatrixTraversal() {
    std::cout << "\n=== Matrix Traversal Order ===" << std::endl;

    const int ROWS = 2000;
    const int COLS = 2000;

    std::vector<std::vector<int>> matrix(ROWS, std::vector<int>(COLS, 1));

    // Row-major (cache-friendly for C++)
    auto time1 = measure("Row-major traversal", [&]() {
        long sum = 0;
        for (int i = 0; i < ROWS; ++i) {
            for (int j = 0; j < COLS; ++j) {
                sum += matrix[i][j];
            }
        }
        volatile long result = sum;
    });

    // Column-major (cache-unfriendly for C++)
    auto time2 = measure("Column-major traversal", [&]() {
        long sum = 0;
        for (int j = 0; j < COLS; ++j) {
            for (int i = 0; i < ROWS; ++i) {
                sum += matrix[i][j];
            }
        }
        volatile long result = sum;
    });

    std::cout << "Slowdown factor: " << (time2 / time1) << "x" << std::endl;
}

void demonstrateBlockedMatrix() {
    std::cout << "\n=== Blocked (Tiled) Matrix Multiplication ===" << std::endl;

    const int N = 512;
    std::vector<std::vector<float>> A(N, std::vector<float>(N, 1.0f));
    std::vector<std::vector<float>> B(N, std::vector<float>(N, 1.0f));
    std::vector<std::vector<float>> C(N, std::vector<float>(N, 0.0f));

    // Standard matrix multiplication
    auto time1 = measure("Standard multiplication", [&]() {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                float sum = 0.0f;
                for (int k = 0; k < N; ++k) {
                    sum += A[i][k] * B[k][j];
                }
                C[i][j] = sum;
            }
        }
    });

    // Reset C
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            C[i][j] = 0.0f;
        }
    }

    // Blocked matrix multiplication
    const int BLOCK_SIZE = 32;

    auto time2 = measure("Blocked multiplication", [&]() {
        for (int ii = 0; ii < N; ii += BLOCK_SIZE) {
            for (int jj = 0; jj < N; jj += BLOCK_SIZE) {
                for (int kk = 0; kk < N; kk += BLOCK_SIZE) {
                    // Multiply block
                    for (int i = ii; i < std::min(ii + BLOCK_SIZE, N); ++i) {
                        for (int j = jj; j < std::min(jj + BLOCK_SIZE, N); ++j) {
                            float sum = C[i][j];
                            for (int k = kk; k < std::min(kk + BLOCK_SIZE, N); ++k) {
                                sum += A[i][k] * B[k][j];
                            }
                            C[i][j] = sum;
                        }
                    }
                }
            }
        }
    });

    std::cout << "Speedup (blocked): " << (time1 / time2) << "x" << std::endl;
}

void demonstratePrefetching() {
    std::cout << "\n=== Data Prefetching ===" << std::endl;

    const int SIZE = 1000000;
    std::vector<int> data(SIZE);

    for (int i = 0; i < SIZE; ++i) {
        data[i] = i;
    }

    // Without prefetching
    auto time1 = measure("Without prefetching", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; i += 16) {
            sum += data[i];
        }
        volatile long result = sum;
    });

    // With manual prefetching (compiler intrinsic)
    auto time2 = measure("With prefetching", [&]() {
        long sum = 0;
        for (int i = 0; i < SIZE; i += 16) {
            // Prefetch data ahead
            if (i + 64 < SIZE) {
                __builtin_prefetch(&data[i + 64], 0, 1);
            }
            sum += data[i];
        }
        volatile long result = sum;
    });

    std::cout << "Note: Prefetching benefit depends on access pattern" << std::endl;
}

void demonstrateFalseSharing() {
    std::cout << "\n=== False Sharing ===" << std::endl;

    std::cout << "False sharing occurs when:" << std::endl;
    std::cout << "  - Multiple threads access different variables" << std::endl;
    std::cout << "  - Variables are on same cache line (64 bytes)" << std::endl;
    std::cout << "  - At least one thread writes" << std::endl;
    std::cout << "  - Causes cache line bouncing between cores" << std::endl;

    // Example structures
    struct BadAlignment {
        int counter1;  // Thread 1 uses this
        int counter2;  // Thread 2 uses this
        // These are likely on same cache line!
    };

    struct GoodAlignment {
        alignas(64) int counter1;  // On own cache line
        alignas(64) int counter2;  // On own cache line
    };

    std::cout << "\nBad alignment size: " << sizeof(BadAlignment) << " bytes" << std::endl;
    std::cout << "Good alignment size: " << sizeof(GoodAlignment) << " bytes" << std::endl;

    std::cout << "\nSolution: Align to cache line size (64 bytes)" << std::endl;
}

void demonstrateDataAlignment() {
    std::cout << "\n=== Data Structure Alignment ===" << std::endl;

    struct Unaligned {
        char a;
        int b;
        char c;
        double d;
    };

    struct Aligned {
        double d;  // 8-byte aligned
        int b;     // 4-byte aligned
        char a;    // 1-byte
        char c;    // 1-byte (padding added by compiler)
    };

    struct CacheAligned {
        alignas(64) int data;
    };

    std::cout << "Struct sizes:" << std::endl;
    std::cout << "  Unaligned: " << sizeof(Unaligned) << " bytes" << std::endl;
    std::cout << "  Aligned: " << sizeof(Aligned) << " bytes" << std::endl;
    std::cout << "  Cache-aligned: " << sizeof(CacheAligned) << " bytes" << std::endl;

    std::cout << "\nAlignments:" << std::endl;
    std::cout << "  Unaligned: " << alignof(Unaligned) << " bytes" << std::endl;
    std::cout << "  Aligned: " << alignof(Aligned) << " bytes" << std::endl;
    std::cout << "  Cache-aligned: " << alignof(CacheAligned) << " bytes" << std::endl;
}

void demonstrateCacheOptimizationTips() {
    std::cout << "\n=== Cache Optimization Tips ===" << std::endl;

    std::cout << "\n1. Data Layout:" << std::endl;
    std::cout << "   - Keep frequently accessed data together" << std::endl;
    std::cout << "   - Align critical data to cache line boundaries" << std::endl;
    std::cout << "   - Use SoA for SIMD and cache efficiency" << std::endl;

    std::cout << "\n2. Access Patterns:" << std::endl;
    std::cout << "   - Favor sequential over random access" << std::endl;
    std::cout << "   - Minimize stride in loops" << std::endl;
    std::cout << "   - Use blocking/tiling for large datasets" << std::endl;

    std::cout << "\n3. Working Set:" << std::endl;
    std::cout << "   - Keep hot data under L1 cache size (~32 KB)" << std::endl;
    std::cout << "   - Reuse data while in cache" << std::endl;
    std::cout << "   - Split operations if data doesn't fit" << std::endl;

    std::cout << "\n4. Avoid Cache Pollution:" << std::endl;
    std::cout << "   - Don't access rarely-used data in hot loops" << std::endl;
    std::cout << "   - Use non-temporal stores for write-only data" << std::endl;
    std::cout << "   - Prefetch strategically" << std::endl;

    std::cout << "\n5. Multi-threading:" << std::endl;
    std::cout << "   - Avoid false sharing (align to cache lines)" << std::endl;
    std::cout << "   - Partition data for thread affinity" << std::endl;
    std::cout << "   - Use thread-local storage when possible" << std::endl;
}

void demonstrateCacheHierarchy() {
    std::cout << "\n=== Cache Hierarchy ===" << std::endl;

    std::cout << "\nTypical modern CPU cache:" << std::endl;
    std::cout << "  L1 Data:  32-64 KB   (~4 cycles latency)" << std::endl;
    std::cout << "  L1 Inst:  32-64 KB   (~4 cycles latency)" << std::endl;
    std::cout << "  L2:       256-512 KB (~12 cycles latency)" << std::endl;
    std::cout << "  L3:       8-32 MB    (~40 cycles latency)" << std::endl;
    std::cout << "  RAM:      8-64 GB    (~200 cycles latency)" << std::endl;

    std::cout << "\nDesign implications:" << std::endl;
    std::cout << "  - L1 miss = 3x slowdown" << std::endl;
    std::cout << "  - L2 miss = 10x slowdown" << std::endl;
    std::cout << "  - L3 miss = 50x slowdown" << std::endl;
    std::cout << "  - Keep working set in L1 when possible!" << std::endl;
}

int main() {
    std::cout << "Cache Optimization Demonstration" << std::endl;
    std::cout << "=================================" << std::endl;

    demonstrateCacheHierarchy();
    demonstrateCacheLineSize();
    demonstrateCacheOptimizationTips();
    demonstrateSequentialVsRandom();
    demonstrateStridePattern();
    demonstrateAoSvsSoA();
    demonstrateMatrixTraversal();
    demonstrateBlockedMatrix();
    demonstrateDataAlignment();
    demonstrateFalseSharing();
    demonstratePrefetching();

    std::cout << "\n=== Cache Optimization Complete ===" << std::endl;
    std::cout << "\nKey takeaway: Cache misses are expensive!" << std::endl;
    std::cout << "Design for spatial and temporal locality." << std::endl;

    return 0;
}
