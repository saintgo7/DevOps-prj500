/*
 * Test Suite for Program 159: Type Traits
 *
 * Tests:
 * - Type properties
 * - Type transformations
 * - Type relationships
 * - SFINAE applications
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

#define ASSERT_TRUE(condition) do { \
    if (!(condition)) { \
        cerr << "  FAILED\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

// Test cases
TEST(test_is_integral) {
    ASSERT_TRUE((is_integral<int>::value));
    ASSERT_TRUE((is_integral<long>::value));
    ASSERT_TRUE((is_integral<char>::value));
    ASSERT_TRUE((!is_integral<double>::value));
    ASSERT_TRUE((!is_integral<string>::value));
}

TEST(test_is_floating_point) {
    ASSERT_TRUE((is_floating_point<float>::value));
    ASSERT_TRUE((is_floating_point<double>::value));
    ASSERT_TRUE((!is_floating_point<int>::value));
}

TEST(test_is_pointer) {
    ASSERT_TRUE((is_pointer<int*>::value));
    ASSERT_TRUE((is_pointer<double*>::value));
    ASSERT_TRUE((!is_pointer<int>::value));
    ASSERT_TRUE((!is_pointer<int&>::value));
}

TEST(test_is_reference) {
    ASSERT_TRUE((is_reference<int&>::value));
    ASSERT_TRUE((is_reference<int&&>::value));
    ASSERT_TRUE((!is_reference<int>::value));
    ASSERT_TRUE((!is_reference<int*>::value));
}

TEST(test_is_const) {
    ASSERT_TRUE((is_const<const int>::value));
    ASSERT_TRUE((!is_const<int>::value));
    ASSERT_TRUE((is_const<const double>::value));
}

TEST(test_is_same) {
    ASSERT_TRUE((is_same<int, int>::value));
    ASSERT_TRUE((is_same<double, double>::value));
    ASSERT_TRUE((!is_same<int, double>::value));
    ASSERT_TRUE((!is_same<int, const int>::value));
}

TEST(test_remove_const) {
    ASSERT_TRUE((is_same<remove_const<const int>::type, int>::value));
    ASSERT_TRUE((is_same<remove_const<int>::type, int>::value));
}

TEST(test_remove_reference) {
    ASSERT_TRUE((is_same<remove_reference<int&>::type, int>::value));
    ASSERT_TRUE((is_same<remove_reference<int&&>::type, int>::value));
    ASSERT_TRUE((is_same<remove_reference<int>::type, int>::value));
}

TEST(test_add_pointer) {
    ASSERT_TRUE((is_same<add_pointer<int>::type, int*>::value));
    ASSERT_TRUE((is_same<add_pointer<double>::type, double*>::value));
}

TEST(test_remove_pointer) {
    ASSERT_TRUE((is_same<remove_pointer<int*>::type, int>::value));
    ASSERT_TRUE((is_same<remove_pointer<int>::type, int>::value));
}

TEST(test_is_class) {
    struct TestClass {};
    ASSERT_TRUE((is_class<TestClass>::value));
    ASSERT_TRUE((is_class<string>::value));
    ASSERT_TRUE((!is_class<int>::value));
}

TEST(test_is_arithmetic) {
    ASSERT_TRUE((is_arithmetic<int>::value));
    ASSERT_TRUE((is_arithmetic<double>::value));
    ASSERT_TRUE((is_arithmetic<float>::value));
    ASSERT_TRUE((!is_arithmetic<string>::value));
}

TEST(test_conditional) {
    using Type1 = conditional<true, int, double>::type;
    using Type2 = conditional<false, int, double>::type;

    ASSERT_TRUE((is_same<Type1, int>::value));
    ASSERT_TRUE((is_same<Type2, double>::value));
}

TEST(test_enable_if) {
    ASSERT_TRUE((is_same<enable_if<true, int>::type, int>::value));
}

int main() {
    cout << "Running Type Traits Tests\n";
    cout << "=========================\n\n";

    RUN_TEST(test_is_integral);
    RUN_TEST(test_is_floating_point);
    RUN_TEST(test_is_pointer);
    RUN_TEST(test_is_reference);
    RUN_TEST(test_is_const);
    RUN_TEST(test_is_same);
    RUN_TEST(test_remove_const);
    RUN_TEST(test_remove_reference);
    RUN_TEST(test_add_pointer);
    RUN_TEST(test_remove_pointer);
    RUN_TEST(test_is_class);
    RUN_TEST(test_is_arithmetic);
    RUN_TEST(test_conditional);
    RUN_TEST(test_enable_if);

    cout << "\n=========================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
