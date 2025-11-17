/*
 * Program 196: SIMD Vectorization
 * Demonstrates SIMD instructions and vector operations
 * Compile: g++ -std=c++17 -O3 -mavx2 -o simd_vectorization main.cpp
 * Note: Requires CPU with AVX2 support
 */

#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>
#include <cstring>

#ifdef __AVX2__
#include <immintrin.h>
#define HAS_AVX2 1
#else
#define HAS_AVX2 0
#endif

#ifdef __SSE2__
#include <emmintrin.h>
#define HAS_SSE2 1
#else
#define HAS_SSE2 0
#endif

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

void demonstrateSIMDIntro() {
    std::cout << "\n=== SIMD Introduction ===" << std::endl;

    std::cout << "\nSIMD: Single Instruction, Multiple Data" << std::endl;
    std::cout << "Process multiple data elements with one instruction" << std::endl;

    std::cout << "\nCommon SIMD instruction sets:" << std::endl;
    std::cout << "  SSE (128-bit):  4 floats or 2 doubles" << std::endl;
    std::cout << "  AVX (256-bit):  8 floats or 4 doubles" << std::endl;
    std::cout << "  AVX-512 (512-bit): 16 floats or 8 doubles" << std::endl;

    std::cout << "\nSIMD support on this system:" << std::endl;
    std::cout << "  SSE2: " << (HAS_SSE2 ? "Yes" : "No") << std::endl;
    std::cout << "  AVX2: " << (HAS_AVX2 ? "Yes" : "No") << std::endl;
}

void demonstrateScalarVsVector() {
    std::cout << "\n=== Scalar vs Vector Addition ===" << std::endl;

    const int SIZE = 10000000;
    std::vector<float> a(SIZE, 1.5f);
    std::vector<float> b(SIZE, 2.5f);
    std::vector<float> result(SIZE);

    // Scalar addition
    auto time1 = measure("Scalar addition", [&]() {
        for (int i = 0; i < SIZE; ++i) {
            result[i] = a[i] + b[i];
        }
    });

#if HAS_AVX2
    // AVX2 vectorized addition
    auto time2 = measure("AVX2 vector addition", [&]() {
        for (int i = 0; i < SIZE; i += 8) {
            __m256 va = _mm256_loadu_ps(&a[i]);
            __m256 vb = _mm256_loadu_ps(&b[i]);
            __m256 vresult = _mm256_add_ps(va, vb);
            _mm256_storeu_ps(&result[i], vresult);
        }
    });

    std::cout << "Speedup (AVX2): " << (time1 / time2) << "x" << std::endl;
#else
    std::cout << "AVX2 not available on this system" << std::endl;
#endif

    // Auto-vectorization (compiler does it)
    auto time3 = measure("Auto-vectorized (compiler)", [&]() {
        #pragma omp simd
        for (int i = 0; i < SIZE; ++i) {
            result[i] = a[i] + b[i];
        }
    });

    std::cout << "Speedup (auto-vectorized): " << (time1 / time3) << "x" << std::endl;
}

void demonstrateSSEOperations() {
    std::cout << "\n=== SSE Operations ===" << std::endl;

#if HAS_SSE2
    // Allocate aligned memory
    alignas(16) float a[4] = {1.0f, 2.0f, 3.0f, 4.0f};
    alignas(16) float b[4] = {5.0f, 6.0f, 7.0f, 8.0f};
    alignas(16) float result[4];

    // Load data into SSE registers
    __m128 va = _mm_load_ps(a);
    __m128 vb = _mm_load_ps(b);

    // Addition
    __m128 vadd = _mm_add_ps(va, vb);
    _mm_store_ps(result, vadd);

    std::cout << "Addition: ";
    for (int i = 0; i < 4; ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << std::endl;

    // Multiplication
    __m128 vmul = _mm_mul_ps(va, vb);
    _mm_store_ps(result, vmul);

    std::cout << "Multiplication: ";
    for (int i = 0; i < 4; ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << std::endl;

    // Dot product
    __m128 vproduct = _mm_mul_ps(va, vb);
    __m128 vsum = _mm_hadd_ps(vproduct, vproduct);
    vsum = _mm_hadd_ps(vsum, vsum);

    float dot_product;
    _mm_store_ss(&dot_product, vsum);

    std::cout << "Dot product: " << dot_product << std::endl;

#else
    std::cout << "SSE2 not available on this system" << std::endl;
#endif
}

void demonstrateAVXOperations() {
    std::cout << "\n=== AVX Operations ===" << std::endl;

#if HAS_AVX2
    // Allocate aligned memory
    alignas(32) float a[8] = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f};
    alignas(32) float b[8] = {8.0f, 7.0f, 6.0f, 5.0f, 4.0f, 3.0f, 2.0f, 1.0f};
    alignas(32) float result[8];

    // Load data
    __m256 va = _mm256_load_ps(a);
    __m256 vb = _mm256_load_ps(b);

    // FMA: Fused Multiply-Add (a * b + c)
    __m256 vc = _mm256_set1_ps(10.0f);  // All elements = 10.0
    __m256 vfma = _mm256_fmadd_ps(va, vb, vc);
    _mm256_store_ps(result, vfma);

    std::cout << "FMA (a * b + 10): ";
    for (int i = 0; i < 8; ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << std::endl;

    // Max
    __m256 vmax = _mm256_max_ps(va, vb);
    _mm256_store_ps(result, vmax);

    std::cout << "Max: ";
    for (int i = 0; i < 8; ++i) {
        std::cout << result[i] << " ";
    }
    std::cout << std::endl;

#else
    std::cout << "AVX2 not available on this system" << std::endl;
#endif
}

void demonstrateDotProduct() {
    std::cout << "\n=== Dot Product Performance ===" << std::endl;

    const int SIZE = 10000000;
    std::vector<float> a(SIZE, 1.5f);
    std::vector<float> b(SIZE, 2.5f);

    // Scalar dot product
    auto time1 = measure("Scalar dot product", [&]() {
        float result = 0.0f;
        for (int i = 0; i < SIZE; ++i) {
            result += a[i] * b[i];
        }
        volatile float r = result;
    });

#if HAS_AVX2
    // AVX2 dot product
    auto time2 = measure("AVX2 dot product", [&]() {
        __m256 vsum = _mm256_setzero_ps();

        for (int i = 0; i < SIZE; i += 8) {
            __m256 va = _mm256_loadu_ps(&a[i]);
            __m256 vb = _mm256_loadu_ps(&b[i]);
            __m256 vproduct = _mm256_mul_ps(va, vb);
            vsum = _mm256_add_ps(vsum, vproduct);
        }

        // Horizontal sum
        alignas(32) float temp[8];
        _mm256_store_ps(temp, vsum);
        float result = 0.0f;
        for (int i = 0; i < 8; ++i) {
            result += temp[i];
        }

        volatile float r = result;
    });

    std::cout << "Speedup (AVX2): " << (time1 / time2) << "x" << std::endl;
#else
    std::cout << "AVX2 not available" << std::endl;
#endif
}

void demonstrateMatrixMultiplication() {
    std::cout << "\n=== Matrix Multiplication with SIMD ===" << std::endl;

    const int N = 256;
    std::vector<float> A(N * N, 1.0f);
    std::vector<float> B(N * N, 2.0f);
    std::vector<float> C(N * N, 0.0f);

    // Scalar version
    auto time1 = measure("Scalar matrix multiply", [&]() {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                float sum = 0.0f;
                for (int k = 0; k < N; ++k) {
                    sum += A[i * N + k] * B[k * N + j];
                }
                C[i * N + j] = sum;
            }
        }
    });

#if HAS_AVX2
    // Reset C
    std::fill(C.begin(), C.end(), 0.0f);

    // AVX2 version
    auto time2 = measure("AVX2 matrix multiply", [&]() {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; j += 8) {
                __m256 vsum = _mm256_setzero_ps();

                for (int k = 0; k < N; ++k) {
                    __m256 va = _mm256_set1_ps(A[i * N + k]);
                    __m256 vb = _mm256_loadu_ps(&B[k * N + j]);
                    vsum = _mm256_fmadd_ps(va, vb, vsum);
                }

                _mm256_storeu_ps(&C[i * N + j], vsum);
            }
        }
    });

    std::cout << "Speedup (AVX2): " << (time1 / time2) << "x" << std::endl;
#else
    std::cout << "AVX2 not available" << std::endl;
#endif
}

void demonstrateVectorizationHints() {
    std::cout << "\n=== Compiler Vectorization Hints ===" << std::endl;

    const int SIZE = 1000000;
    std::vector<float> a(SIZE, 1.0f);
    std::vector<float> b(SIZE, 2.0f);
    std::vector<float> result(SIZE);

    // Without hints
    auto time1 = measure("Without hints", [&]() {
        for (int i = 0; i < SIZE; ++i) {
            result[i] = std::sqrt(a[i]) + std::sin(b[i]);
        }
    });

    // With pragma simd hint
    auto time2 = measure("With #pragma simd", [&]() {
        #pragma omp simd
        for (int i = 0; i < SIZE; ++i) {
            result[i] = std::sqrt(a[i]) + std::sin(b[i]);
        }
    });

    std::cout << "\nNote: Results depend on compiler support" << std::endl;
}

void demonstrateAlignedVsUnaligned() {
    std::cout << "\n=== Aligned vs Unaligned Memory Access ===" << std::endl;

#if HAS_AVX2
    const int SIZE = 10000000;

    // Unaligned data
    std::vector<float> unaligned(SIZE + 1, 1.0f);
    float* unaligned_ptr = &unaligned[1];  // Offset by 1

    // Aligned data
    alignas(32) float aligned_data[SIZE];
    std::fill_n(aligned_data, SIZE, 1.0f);

    std::vector<float> result(SIZE);

    // Unaligned loads
    auto time1 = measure("Unaligned loads", [&]() {
        for (int i = 0; i < SIZE; i += 8) {
            __m256 v = _mm256_loadu_ps(&unaligned_ptr[i]);
            _mm256_storeu_ps(&result[i], v);
        }
    });

    // Aligned loads
    auto time2 = measure("Aligned loads", [&]() {
        for (int i = 0; i < SIZE; i += 8) {
            __m256 v = _mm256_load_ps(&aligned_data[i]);
            _mm256_store_ps(&result[i], v);
        }
    });

    std::cout << "Speedup (aligned): " << (time1 / time2) << "x" << std::endl;
#else
    std::cout << "AVX2 not available" << std::endl;
#endif
}

void demonstrateSIMDBestPractices() {
    std::cout << "\n=== SIMD Best Practices ===" << std::endl;

    std::cout << "\n1. Memory Alignment:" << std::endl;
    std::cout << "   - Align data to SIMD width (16/32/64 bytes)" << std::endl;
    std::cout << "   - Use alignas() or posix_memalign()" << std::endl;
    std::cout << "   - Aligned loads/stores are faster" << std::endl;

    std::cout << "\n2. Data Layout:" << std::endl;
    std::cout << "   - Structure of Arrays (SoA) better than AoS" << std::endl;
    std::cout << "   - Ensure contiguous memory access" << std::endl;
    std::cout << "   - Avoid scattered reads/writes" << std::endl;

    std::cout << "\n3. Compiler Help:" << std::endl;
    std::cout << "   - Use -O3 for auto-vectorization" << std::endl;
    std::cout << "   - Add -march=native for CPU-specific optimizations" << std::endl;
    std::cout << "   - Use #pragma omp simd hints" << std::endl;
    std::cout << "   - Check vectorization reports: -fopt-info-vec" << std::endl;

    std::cout << "\n4. When to Use SIMD:" << std::endl;
    std::cout << "   - Simple, independent operations (add, mul, etc.)" << std::endl;
    std::cout << "   - Large datasets" << std::endl;
    std::cout << "   - Tight inner loops" << std::endl;
    std::cout << "   - Avoid for complex control flow" << std::endl;

    std::cout << "\n5. Portability:" << std::endl;
    std::cout << "   - Provide scalar fallback" << std::endl;
    std::cout << "   - Use intrinsic wrappers or libraries" << std::endl;
    std::cout << "   - Consider cross-platform SIMD libraries:" << std::endl;
    std::cout << "     - Highway (Google)" << std::endl;
    std::cout << "     - xsimd" << std::endl;
    std::cout << "     - Eigen (for linear algebra)" << std::endl;
}

void demonstrateCompilerFlags() {
    std::cout << "\n=== Compiler Flags for SIMD ===" << std::endl;

    std::cout << "\nGCC/Clang flags:" << std::endl;
    std::cout << "  -msse4.2    Enable SSE4.2" << std::endl;
    std::cout << "  -mavx       Enable AVX" << std::endl;
    std::cout << "  -mavx2      Enable AVX2" << std::endl;
    std::cout << "  -mavx512f   Enable AVX-512" << std::endl;
    std::cout << "  -march=native  Use all CPU features" << std::endl;
    std::cout << "  -ftree-vectorize  Enable auto-vectorization" << std::endl;
    std::cout << "  -fopt-info-vec  Show vectorization info" << std::endl;

    std::cout << "\nExample compilation:" << std::endl;
    std::cout << "  g++ -std=c++17 -O3 -march=native -o program main.cpp" << std::endl;
}

int main() {
    std::cout << "SIMD Vectorization Demonstration" << std::endl;
    std::cout << "=================================" << std::endl;

    demonstrateSIMDIntro();
    demonstrateCompilerFlags();
    demonstrateSIMDBestPractices();
    demonstrateScalarVsVector();
    demonstrateSSEOperations();
    demonstrateAVXOperations();
    demonstrateDotProduct();
    demonstrateMatrixMultiplication();
    demonstrateAlignedVsUnaligned();
    demonstrateVectorizationHints();

    std::cout << "\n=== SIMD Vectorization Complete ===" << std::endl;
    std::cout << "\nKey points:" << std::endl;
    std::cout << "  - SIMD can provide 4-8x speedup for appropriate operations" << std::endl;
    std::cout << "  - Start with compiler auto-vectorization (-O3 -march=native)" << std::endl;
    std::cout << "  - Use intrinsics for critical hot spots" << std::endl;
    std::cout << "  - Always provide scalar fallback for portability" << std::endl;

    return 0;
}
