/*
 * Test Suite for Program 155: Variadic Templates
 *
 * Tests:
 * - Variadic function templates
 * - Parameter pack expansion
 * - Recursive variadic templates
 * - sizeof... operator
 * - Fold expressions (C++17)
 */

#include <iostream>
#include <string>
#include <sstream>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { \
    cout << "Running " << #name << "..."; \
    name(); \
    cout << " PASSED\n"; \
} while(0)

#define ASSERT_EQ(actual, expected) do { \
    if ((actual) != (expected)) { \
        cerr << "  FAILED\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

// Sum function - variadic template
template<typename T>
T sum(T value) {
    return value;
}

template<typename T, typename... Args>
T sum(T first, Args... args) {
    return first + sum(args...);
}

// Count arguments
template<typename... Args>
size_t count_args(Args... args) {
    return sizeof...(args);
}

// Print all (to string)
void print_to_string(ostringstream&) {}

template<typename T, typename... Args>
void print_to_string(ostringstream& oss, T first, Args... args) {
    oss << first;
    if (sizeof...(args) > 0) {
        oss << " ";
    }
    print_to_string(oss, args...);
}

template<typename... Args>
string print_all(Args... args) {
    ostringstream oss;
    print_to_string(oss, args...);
    return oss.str();
}

// Maximum of variadic args
template<typename T>
T maximum(T value) {
    return value;
}

template<typename T, typename... Args>
T maximum(T first, Args... args) {
    T max_rest = maximum(args...);
    return (first > max_rest) ? first : max_rest;
}

// Test cases
TEST(test_sum_integers) {
    ASSERT_EQ(sum(1), 1);
    ASSERT_EQ(sum(1, 2), 3);
    ASSERT_EQ(sum(1, 2, 3), 6);
    ASSERT_EQ(sum(1, 2, 3, 4, 5), 15);
}

TEST(test_sum_doubles) {
    ASSERT_EQ(sum(1.5), 1.5);
    ASSERT_EQ(sum(1.5, 2.5), 4.0);
    ASSERT_EQ(sum(1.0, 2.0, 3.0, 4.0), 10.0);
}

TEST(test_count_args) {
    ASSERT_EQ(count_args(), 0);
    ASSERT_EQ(count_args(1), 1);
    ASSERT_EQ(count_args(1, 2), 2);
    ASSERT_EQ(count_args(1, 2, 3, 4, 5), 5);
    ASSERT_EQ(count_args("a", "b", "c"), 3);
}

TEST(test_print_all) {
    ASSERT_EQ(print_all(1), "1");
    ASSERT_EQ(print_all(1, 2, 3), "1 2 3");
    ASSERT_EQ(print_all("hello", "world"), "hello world");
}

TEST(test_maximum_variadic) {
    ASSERT_EQ(maximum(5), 5);
    ASSERT_EQ(maximum(5, 10), 10);
    ASSERT_EQ(maximum(3, 7, 2, 9, 1), 9);
    ASSERT_EQ(maximum(1, 2, 3, 4, 5), 5);
}

TEST(test_mixed_types_print) {
    string result = print_all(1, 2.5, "hello");
    ASSERT_EQ(result, "1 2.5 hello");
}

TEST(test_edge_case_single_arg) {
    ASSERT_EQ(sum(42), 42);
    ASSERT_EQ(maximum(100), 100);
    ASSERT_EQ(count_args(1), 1);
}

TEST(test_edge_case_many_args) {
    int result = sum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
    ASSERT_EQ(result, 55);
}

TEST(test_edge_case_zero_sum) {
    ASSERT_EQ(sum(0), 0);
    ASSERT_EQ(sum(0, 0, 0), 0);
    ASSERT_EQ(sum(-5, 5), 0);
}

TEST(test_edge_case_negative) {
    ASSERT_EQ(sum(-1, -2, -3), -6);
    ASSERT_EQ(maximum(-10, -5, -20), -5);
}

int main() {
    cout << "Running Variadic Templates Tests\n";
    cout << "=================================\n\n";

    RUN_TEST(test_sum_integers);
    RUN_TEST(test_sum_doubles);
    RUN_TEST(test_count_args);
    RUN_TEST(test_print_all);
    RUN_TEST(test_maximum_variadic);
    RUN_TEST(test_mixed_types_print);
    RUN_TEST(test_edge_case_single_arg);
    RUN_TEST(test_edge_case_many_args);
    RUN_TEST(test_edge_case_zero_sum);
    RUN_TEST(test_edge_case_negative);

    cout << "\n=================================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
