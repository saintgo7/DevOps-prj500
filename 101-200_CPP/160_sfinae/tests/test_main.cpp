/*
 * Test Suite for Program 160: SFINAE
 *
 * Tests:
 * - Substitution Failure Is Not An Error
 * - enable_if usage
 * - Function overload resolution
 * - Type-based function selection
 */

#include <iostream>
#include <type_traits>
#include <string>
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

// SFINAE with enable_if for integral types
template<typename T>
typename enable_if<is_integral<T>::value, T>::type
process(T value) {
    return value * 2;
}

// SFINAE with enable_if for floating point types
template<typename T>
typename enable_if<is_floating_point<T>::value, T>::type
process(T value) {
    return value * 3.0;
}

// Check if type has size() method
template<typename T>
auto get_size(T& container) -> decltype(container.size()) {
    return container.size();
}

// Type-based printing
template<typename T>
enable_if_t<is_integral_v<T>, string>
type_name() {
    return "integral";
}

template<typename T>
enable_if_t<is_floating_point_v<T>, string>
type_name() {
    return "floating_point";
}

// Test cases
TEST(test_process_integral) {
    ASSERT_EQ(process(5), 10);
    ASSERT_EQ(process(10), 20);
    ASSERT_EQ(process(-3), -6);
}

TEST(test_process_floating_point) {
    ASSERT_EQ(process(2.0), 6.0);
    ASSERT_EQ(process(1.5), 4.5);
}

TEST(test_get_size_vector) {
    vector<int> v = {1, 2, 3, 4, 5};
    ASSERT_EQ(get_size(v), 5);
}

TEST(test_get_size_string) {
    string s = "hello";
    ASSERT_EQ(get_size(s), 5);
}

TEST(test_type_name_integral) {
    ASSERT_EQ(type_name<int>(), "integral");
    ASSERT_EQ(type_name<long>(), "integral");
}

TEST(test_type_name_floating) {
    ASSERT_EQ(type_name<double>(), "floating_point");
    ASSERT_EQ(type_name<float>(), "floating_point");
}

TEST(test_edge_case_zero) {
    ASSERT_EQ(process(0), 0);
    ASSERT_EQ(process(0.0), 0.0);
}

TEST(test_edge_case_negative) {
    ASSERT_EQ(process(-10), -20);
    ASSERT_EQ(process(-2.5), -7.5);
}

TEST(test_empty_container) {
    vector<int> v;
    ASSERT_EQ(get_size(v), 0);

    string s;
    ASSERT_EQ(get_size(s), 0);
}

int main() {
    cout << "Running SFINAE Tests\n";
    cout << "====================\n\n";

    RUN_TEST(test_process_integral);
    RUN_TEST(test_process_floating_point);
    RUN_TEST(test_get_size_vector);
    RUN_TEST(test_get_size_string);
    RUN_TEST(test_type_name_integral);
    RUN_TEST(test_type_name_floating);
    RUN_TEST(test_edge_case_zero);
    RUN_TEST(test_edge_case_negative);
    RUN_TEST(test_empty_container);

    cout << "\n====================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
