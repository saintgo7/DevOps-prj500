/*
 * Test Suite for Program 178: std::span (C++20)
 */

#include <iostream>
#include <vector>
#include <array>
#include <cassert>

#if __cplusplus >= 202002L
#include <span>
using std::span;
#endif

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

#if __cplusplus >= 202002L
TEST(test_span_from_array) {
    int arr[] = {1, 2, 3, 4, 5};
    span<int> s(arr);
    ASSERT_EQ(s.size(), 5);
    ASSERT_EQ(s[0], 1);
    ASSERT_EQ(s[4], 5);
}

TEST(test_span_from_vector) {
    vector<int> v = {10, 20, 30};
    span<int> s(v);
    ASSERT_EQ(s.size(), 3);
    ASSERT_EQ(s[1], 20);
}

TEST(test_span_subspan) {
    int arr[] = {1, 2, 3, 4, 5};
    span<int> s(arr);
    auto sub = s.subspan(1, 3);
    ASSERT_EQ(sub.size(), 3);
    ASSERT_EQ(sub[0], 2);
}
#else
TEST(test_span_placeholder) {
    // Placeholder for C++17
    vector<int> v = {1, 2, 3};
    ASSERT_EQ(v.size(), 3);
}
#endif

int main() {
    cout << "Running std::span Tests\n=======================\n\n";
#if __cplusplus >= 202002L
    RUN_TEST(test_span_from_array);
    RUN_TEST(test_span_from_vector);
    RUN_TEST(test_span_subspan);
#else
    cout << "Note: std::span requires C++20\n";
    RUN_TEST(test_span_placeholder);
#endif
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
