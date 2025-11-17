/*
 * Test Suite for Program 198: Benchmarking
 */

#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;
using namespace chrono;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

template<typename Func>
long long benchmark(Func f, int iterations = 1) {
    auto start = high_resolution_clock::now();
    for (int i = 0; i < iterations; i++) {
        f();
    }
    auto end = high_resolution_clock::now();
    return duration_cast<microseconds>(end - start).count();
}

TEST(test_vector_push_back) {
    auto time = benchmark([]() {
        vector<int> v;
        for (int i = 0; i < 1000; i++) {
            v.push_back(i);
        }
    });

    ASSERT_TRUE(time > 0);
}

TEST(test_vector_with_reserve) {
    auto time = benchmark([]() {
        vector<int> v;
        v.reserve(1000);
        for (int i = 0; i < 1000; i++) {
            v.push_back(i);
        }
    });

    ASSERT_TRUE(time > 0);
}

TEST(test_sorting_performance) {
    auto time = benchmark([]() {
        vector<int> v(1000);
        for (int i = 0; i < 1000; i++) {
            v[i] = 1000 - i;
        }
        sort(v.begin(), v.end());
    });

    ASSERT_TRUE(time > 0);
}

TEST(test_loop_performance) {
    auto time = benchmark([]() {
        long sum = 0;
        for (int i = 0; i < 100000; i++) {
            sum += i;
        }
    }, 10);

    ASSERT_TRUE(time > 0);
}

TEST(test_benchmark_comparison) {
    // Benchmark two different approaches
    auto time1 = benchmark([]() {
        int sum = 0;
        for (int i = 0; i < 1000; i++) sum += i;
    }, 100);

    auto time2 = benchmark([]() {
        int sum = 0;
        for (int i = 0; i < 1000; i++) sum += i;
    }, 100);

    ASSERT_TRUE(time1 > 0 && time2 > 0);
}

int main() {
    cout << "Running Benchmarking Tests\n==========================\n\n";
    RUN_TEST(test_vector_push_back);
    RUN_TEST(test_vector_with_reserve);
    RUN_TEST(test_sorting_performance);
    RUN_TEST(test_loop_performance);
    RUN_TEST(test_benchmark_comparison);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
