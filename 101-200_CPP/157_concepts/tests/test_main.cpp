/*
 * Test Suite for Program 157: Concepts (C++20)
 *
 * Tests:
 * - Basic concepts
 * - Type constraints
 * - Concept requirements
 * - Standard library concepts
 */

#include <iostream>
#include <string>
#include <vector>
#include <concepts>
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

#define ASSERT_TRUE(condition) do { \
    if (!(condition)) { \
        cerr << "  FAILED\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

// Concept-constrained functions
template<integral T>
T add(T a, T b) {
    return a + b;
}

template<floating_point T>
T multiply(T a, T b) {
    return a * b;
}

// Custom concept
template<typename T>
concept Numeric = integral<T> || floating_point<T>;

template<Numeric T>
T square(T value) {
    return value * value;
}

// Test cases
TEST(test_integral_add) {
    ASSERT_EQ(add(5, 3), 8);
    ASSERT_EQ(add(10, 20), 30);
    ASSERT_EQ(add(-5, 10), 5);
}

TEST(test_floating_point_multiply) {
    ASSERT_EQ(multiply(2.5, 4.0), 10.0);
    ASSERT_EQ(multiply(1.5, 2.0), 3.0);
}

TEST(test_numeric_concept_int) {
    ASSERT_EQ(square(5), 25);
    ASSERT_EQ(square(10), 100);
    ASSERT_EQ(square(-3), 9);
}

TEST(test_numeric_concept_double) {
    ASSERT_EQ(square(2.0), 4.0);
    ASSERT_EQ(square(3.5), 12.25);
}

TEST(test_standard_concepts) {
    ASSERT_TRUE((integral<int>));
    ASSERT_TRUE((integral<long>));
    ASSERT_TRUE((!integral<double>));
    ASSERT_TRUE((floating_point<double>));
    ASSERT_TRUE((floating_point<float>));
    ASSERT_TRUE((!floating_point<int>));
}

TEST(test_edge_case_zero) {
    ASSERT_EQ(add(0, 0), 0);
    ASSERT_EQ(square(0), 0);
}

TEST(test_edge_case_negative) {
    ASSERT_EQ(add(-5, -3), -8);
    ASSERT_EQ(square(-5), 25);
}

int main() {
    cout << "Running Concepts Tests\n";
    cout << "======================\n\n";

    RUN_TEST(test_integral_add);
    RUN_TEST(test_floating_point_multiply);
    RUN_TEST(test_numeric_concept_int);
    RUN_TEST(test_numeric_concept_double);
    RUN_TEST(test_standard_concepts);
    RUN_TEST(test_edge_case_zero);
    RUN_TEST(test_edge_case_negative);

    cout << "\n======================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
