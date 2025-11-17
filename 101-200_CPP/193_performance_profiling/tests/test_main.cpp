/*
 * Test Suite for Program 193: Performance Profiling
 */

#include <iostream>
#include <chrono>
#include <vector>
#include <cassert>

using namespace std;
using namespace chrono;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

long long fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

TEST(test_time_measurement) {
    auto start = high_resolution_clock::now();
    fibonacci(20);
    auto end = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(end - start);
    ASSERT_TRUE(duration.count() > 0);
}

TEST(test_vector_performance) {
    auto start = high_resolution_clock::now();

    vector<int> v;
    for (int i = 0; i < 10000; i++) {
        v.push_back(i);
    }

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);

    ASSERT_TRUE(duration.count() > 0);
    ASSERT_TRUE(v.size() == 10000);
}

TEST(test_loop_performance) {
    auto start = high_resolution_clock::now();

    long sum = 0;
    for (int i = 0; i < 1000000; i++) {
        sum += i;
    }

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);

    ASSERT_TRUE(duration.count() > 0);
    ASSERT_TRUE(sum > 0);
}

TEST(test_steady_clock) {
    auto t1 = steady_clock::now();
    auto t2 = steady_clock::now();

    ASSERT_TRUE(t2 >= t1);
}

int main() {
    cout << "Running Performance Profiling Tests\n====================================\n\n";
    RUN_TEST(test_time_measurement);
    RUN_TEST(test_vector_performance);
    RUN_TEST(test_loop_performance);
    RUN_TEST(test_steady_clock);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
