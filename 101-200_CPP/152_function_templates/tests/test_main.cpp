/*
 * Test Suite for Program 152: Function Templates
 *
 * Tests:
 * - Basic function templates
 * - Template overloading
 * - Template specialization
 * - Multiple template parameters
 * - Return type deduction
 */

#include <iostream>
#include <string>
#include <vector>
#include <cassert>
#include <cmath>

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
        cerr << "  FAILED: " << #actual << " != " << #expected << "\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

#define ASSERT_NEAR(actual, expected, epsilon) do { \
    if (fabs((actual) - (expected)) > (epsilon)) { \
        cerr << "  FAILED: " << #actual << " not near " << #expected << "\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

// Function templates
template<typename T>
T square(T value) {
    return value * value;
}

template<typename T>
T add(T a, T b) {
    return a + b;
}

template<typename T, typename U>
auto multiply(T a, U b) -> decltype(a * b) {
    return a * b;
}

template<typename T>
T max3(T a, T b, T c) {
    T max_val = a;
    if (b > max_val) max_val = b;
    if (c > max_val) max_val = c;
    return max_val;
}

template<typename T>
void swap_values(T& a, T& b) {
    T temp = a;
    a = b;
    b = temp;
}

// Specialization
template<typename T>
string type_name() {
    return "unknown";
}

template<>
string type_name<int>() {
    return "int";
}

template<>
string type_name<double>() {
    return "double";
}

// Test cases
TEST(test_square_integers) {
    ASSERT_EQ(square(5), 25);
    ASSERT_EQ(square(0), 0);
    ASSERT_EQ(square(-3), 9);
    ASSERT_EQ(square(10), 100);
}

TEST(test_square_doubles) {
    ASSERT_NEAR(square(2.5), 6.25, 0.001);
    ASSERT_NEAR(square(1.5), 2.25, 0.001);
    ASSERT_NEAR(square(-2.0), 4.0, 0.001);
}

TEST(test_add_function) {
    ASSERT_EQ(add(5, 3), 8);
    ASSERT_EQ(add(10, 20), 30);
    ASSERT_NEAR(add(1.5, 2.5), 4.0, 0.001);
    ASSERT_EQ(add(string("Hello"), string("World")), string("HelloWorld"));
}

TEST(test_multiply_mixed_types) {
    auto result1 = multiply(5, 2.0);
    ASSERT_NEAR(result1, 10.0, 0.001);

    auto result2 = multiply(3.5, 2);
    ASSERT_NEAR(result2, 7.0, 0.001);

    auto result3 = multiply(4, 5);
    ASSERT_EQ(result3, 20);
}

TEST(test_max3_function) {
    ASSERT_EQ(max3(1, 2, 3), 3);
    ASSERT_EQ(max3(10, 5, 8), 10);
    ASSERT_EQ(max3(7, 12, 9), 12);
    ASSERT_NEAR(max3(1.5, 2.5, 2.0), 2.5, 0.001);
}

TEST(test_swap_function) {
    int a = 10, b = 20;
    swap_values(a, b);
    ASSERT_EQ(a, 20);
    ASSERT_EQ(b, 10);

    double x = 1.5, y = 2.5;
    swap_values(x, y);
    ASSERT_NEAR(x, 2.5, 0.001);
    ASSERT_NEAR(y, 1.5, 0.001);

    string s1 = "hello", s2 = "world";
    swap_values(s1, s2);
    ASSERT_EQ(s1, "world");
    ASSERT_EQ(s2, "hello");
}

TEST(test_template_specialization) {
    ASSERT_EQ(type_name<int>(), "int");
    ASSERT_EQ(type_name<double>(), "double");
    ASSERT_EQ(type_name<string>(), "unknown");
}

TEST(test_edge_case_zero) {
    ASSERT_EQ(square(0), 0);
    ASSERT_EQ(add(0, 0), 0);
    ASSERT_EQ(max3(0, 0, 0), 0);
}

TEST(test_edge_case_negative) {
    ASSERT_EQ(square(-5), 25);
    ASSERT_EQ(add(-10, 5), -5);
    ASSERT_EQ(max3(-1, -2, -3), -1);
}

TEST(test_edge_case_large_numbers) {
    ASSERT_EQ(square(1000), 1000000);
    ASSERT_EQ(add(1000000, 2000000), 3000000);
}

int main() {
    cout << "Running Function Templates Tests\n";
    cout << "=================================\n\n";

    RUN_TEST(test_square_integers);
    RUN_TEST(test_square_doubles);
    RUN_TEST(test_add_function);
    RUN_TEST(test_multiply_mixed_types);
    RUN_TEST(test_max3_function);
    RUN_TEST(test_swap_function);
    RUN_TEST(test_template_specialization);
    RUN_TEST(test_edge_case_zero);
    RUN_TEST(test_edge_case_negative);
    RUN_TEST(test_edge_case_large_numbers);

    cout << "\n=================================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
