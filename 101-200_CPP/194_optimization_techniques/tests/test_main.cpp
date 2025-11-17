/*
 * Test Suite for Program 194: Optimization Techniques
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

// Loop unrolling example
int sum_unrolled(const vector<int>& v) {
    int sum = 0;
    size_t i = 0;
    for (; i + 3 < v.size(); i += 4) {
        sum += v[i] + v[i+1] + v[i+2] + v[i+3];
    }
    for (; i < v.size(); i++) {
        sum += v[i];
    }
    return sum;
}

// Inline function
inline int square_inline(int x) {
    return x * x;
}

// Move semantics optimization
vector<int> create_vector() {
    vector<int> v(1000);
    return v; // RVO/NRVO optimization
}

TEST(test_loop_unrolling) {
    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8};
    int sum = sum_unrolled(v);
    ASSERT_EQ(sum, 36);
}

TEST(test_inline_function) {
    int result = square_inline(5);
    ASSERT_EQ(result, 25);
}

TEST(test_rvo_optimization) {
    vector<int> v = create_vector();
    ASSERT_EQ(v.size(), 1000);
}

TEST(test_reserve_optimization) {
    vector<int> v;
    v.reserve(1000); // Pre-allocate

    for (int i = 0; i < 1000; i++) {
        v.push_back(i);
    }

    ASSERT_EQ(v.size(), 1000);
}

TEST(test_const_reference) {
    vector<int> v = {1, 2, 3, 4, 5};

    int sum = 0;
    for (const auto& val : v) {  // Avoid copy
        sum += val;
    }

    ASSERT_EQ(sum, 15);
}

TEST(test_move_semantics) {
    vector<int> v1 = {1, 2, 3};
    vector<int> v2 = move(v1);

    ASSERT_EQ(v2.size(), 3);
}

int main() {
    cout << "Running Optimization Techniques Tests\n======================================\n\n";
    RUN_TEST(test_loop_unrolling);
    RUN_TEST(test_inline_function);
    RUN_TEST(test_rvo_optimization);
    RUN_TEST(test_reserve_optimization);
    RUN_TEST(test_const_reference);
    RUN_TEST(test_move_semantics);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
