/*
 * Test Suite for Program 196: SIMD Vectorization
 */

#include <iostream>
#include <vector>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

// Scalar version
void add_scalar(const float* a, const float* b, float* c, int n) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// Vectorizable loop
void multiply_arrays(const vector<float>& a, const vector<float>& b, vector<float>& c) {
    for (size_t i = 0; i < a.size(); i++) {
        c[i] = a[i] * b[i];
    }
}

TEST(test_scalar_addition) {
    const int N = 4;
    float a[N] = {1.0f, 2.0f, 3.0f, 4.0f};
    float b[N] = {5.0f, 6.0f, 7.0f, 8.0f};
    float c[N];

    add_scalar(a, b, c, N);

    ASSERT_EQ(c[0], 6.0f);
    ASSERT_EQ(c[1], 8.0f);
    ASSERT_EQ(c[2], 10.0f);
    ASSERT_EQ(c[3], 12.0f);
}

TEST(test_vector_multiply) {
    vector<float> a = {1.0f, 2.0f, 3.0f, 4.0f};
    vector<float> b = {2.0f, 3.0f, 4.0f, 5.0f};
    vector<float> c(4);

    multiply_arrays(a, b, c);

    ASSERT_EQ(c[0], 2.0f);
    ASSERT_EQ(c[1], 6.0f);
    ASSERT_EQ(c[2], 12.0f);
    ASSERT_EQ(c[3], 20.0f);
}

TEST(test_aligned_access) {
    alignas(16) float data[4] = {1.0f, 2.0f, 3.0f, 4.0f};
    ASSERT_EQ(data[0], 1.0f);
}

TEST(test_vectorization_opportunity) {
    const int N = 1000;
    vector<int> v(N);

    // Simple loop that can be vectorized
    for (int i = 0; i < N; i++) {
        v[i] = i * 2;
    }

    ASSERT_EQ(v[0], 0);
    ASSERT_EQ(v[10], 20);
}

int main() {
    cout << "Running SIMD Vectorization Tests\n=================================\n\n";
    RUN_TEST(test_scalar_addition);
    RUN_TEST(test_vector_multiply);
    RUN_TEST(test_aligned_access);
    RUN_TEST(test_vectorization_opportunity);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
