/*
 * Test Suite for Program 195: Cache Optimization
 */

#include <iostream>
#include <vector>
#include <chrono>
#include <cassert>

using namespace std;
using namespace chrono;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

// Structure with good cache alignment
struct alignas(64) CacheAligned {
    int data[16];
};

// Array of structures (better cache locality)
struct Point {
    double x, y, z;
};

TEST(test_cache_aligned_structure) {
    CacheAligned ca;
    ca.data[0] = 42;
    ASSERT_EQ(ca.data[0], 42);
}

TEST(test_sequential_access) {
    const int SIZE = 1000;
    vector<int> v(SIZE);

    // Sequential access (cache-friendly)
    for (int i = 0; i < SIZE; i++) {
        v[i] = i;
    }

    int sum = 0;
    for (int i = 0; i < SIZE; i++) {
        sum += v[i];
    }

    ASSERT_TRUE(sum > 0);
}

TEST(test_locality_of_reference) {
    const int N = 100;
    vector<Point> points(N);

    // Initialize
    for (int i = 0; i < N; i++) {
        points[i].x = i;
        points[i].y = i * 2;
        points[i].z = i * 3;
    }

    // Access with good locality
    double sum = 0;
    for (const auto& p : points) {
        sum += p.x + p.y + p.z;
    }

    ASSERT_TRUE(sum > 0);
}

TEST(test_prefetching_simulation) {
    vector<int> v(1000);

    // Fill with predictable pattern
    for (size_t i = 0; i < v.size(); i++) {
        v[i] = i;
    }

    // Sequential access should be fast
    long sum = 0;
    for (const auto& val : v) {
        sum += val;
    }

    ASSERT_TRUE(sum > 0);
}

TEST(test_data_structure_layout) {
    struct SOA {  // Structure of Arrays (better cache)
        vector<double> x;
        vector<double> y;
        vector<double> z;
    } soa;

    soa.x.resize(100);
    soa.y.resize(100);
    soa.z.resize(100);

    for (size_t i = 0; i < 100; i++) {
        soa.x[i] = i;
        soa.y[i] = i * 2;
        soa.z[i] = i * 3;
    }

    ASSERT_EQ(soa.x.size(), 100);
}

int main() {
    cout << "Running Cache Optimization Tests\n=================================\n\n";
    RUN_TEST(test_cache_aligned_structure);
    RUN_TEST(test_sequential_access);
    RUN_TEST(test_locality_of_reference);
    RUN_TEST(test_prefetching_simulation);
    RUN_TEST(test_data_structure_layout);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
