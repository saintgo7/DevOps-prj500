/*
 * Test Suite for Program 106: Functions
 *
 * Tests function declarations, parameters, return values, overloading, and recursion
 */

#include <iostream>
#include <string>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define ASSERT_FALSE(condition) assert(!(condition))
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Test functions
int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

int multiply(int a, int b = 2) {
    return a * b;
}

void passByValue(int x) {
    x = 100;
}

void passByReference(int& x) {
    x = 100;
}

void passByPointer(int* x) {
    if (x != nullptr) {
        *x = 100;
    }
}

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

inline int square(int x) {
    return x * x;
}

// Tests
TEST(test_basic_function) {
    ASSERT_EQ(add(5, 3), 8);
    ASSERT_EQ(add(0, 0), 0);
    ASSERT_EQ(add(-5, 5), 0);
}

TEST(test_function_overloading) {
    ASSERT_EQ(add(5, 3), 8);
    ASSERT_TRUE(add(5.5, 3.2) > 8.6 && add(5.5, 3.2) < 8.8);
}

TEST(test_default_parameters) {
    ASSERT_EQ(multiply(5), 10);     // Uses default parameter 2
    ASSERT_EQ(multiply(5, 3), 15);  // Override default
}

TEST(test_pass_by_value) {
    int x = 10;
    passByValue(x);
    ASSERT_EQ(x, 10);  // Unchanged
}

TEST(test_pass_by_reference) {
    int x = 10;
    passByReference(x);
    ASSERT_EQ(x, 100);  // Modified
}

TEST(test_pass_by_pointer) {
    int x = 10;
    passByPointer(&x);
    ASSERT_EQ(x, 100);  // Modified
}

TEST(test_pass_null_pointer) {
    int* ptr = nullptr;
    passByPointer(ptr);  // Should not crash
    ASSERT_TRUE(ptr == nullptr);
}

TEST(test_recursion_factorial) {
    ASSERT_EQ(factorial(0), 1);
    ASSERT_EQ(factorial(1), 1);
    ASSERT_EQ(factorial(5), 120);
    ASSERT_EQ(factorial(10), 3628800);
}

TEST(test_inline_function) {
    ASSERT_EQ(square(5), 25);
    ASSERT_EQ(square(0), 0);
    ASSERT_EQ(square(-3), 9);
}

TEST(test_lambda_basic) {
    auto add_lambda = [](int a, int b) { return a + b; };
    ASSERT_EQ(add_lambda(5, 3), 8);
}

TEST(test_lambda_capture_by_value) {
    int x = 10;
    auto lambda = [x]() { return x * 2; };
    ASSERT_EQ(lambda(), 20);
    x = 20;
    ASSERT_EQ(lambda(), 20);  // Captured value doesn't change
}

TEST(test_lambda_capture_by_reference) {
    int x = 10;
    auto lambda = [&x]() { return x * 2; };
    ASSERT_EQ(lambda(), 20);
    x = 20;
    ASSERT_EQ(lambda(), 40);  // Captured reference reflects change
}

TEST(test_lambda_capture_all) {
    int a = 5, b = 10;
    auto lambda = [=]() { return a + b; };
    ASSERT_EQ(lambda(), 15);
}

TEST(test_lambda_modify_capture) {
    int x = 10;
    auto lambda = [&x]() { x = 100; };
    lambda();
    ASSERT_EQ(x, 100);
}

TEST(test_return_types) {
    auto getInt = []() -> int { return 42; };
    auto getDouble = []() -> double { return 3.14; };
    auto getString = []() -> std::string { return "test"; };

    ASSERT_EQ(getInt(), 42);
    ASSERT_TRUE(getDouble() > 3.13 && getDouble() < 3.15);
    ASSERT_EQ(getString(), "test");
}

TEST(test_multiple_return_paths) {
    auto abs_val = [](int x) {
        if (x < 0) return -x;
        return x;
    };

    ASSERT_EQ(abs_val(5), 5);
    ASSERT_EQ(abs_val(-5), 5);
    ASSERT_EQ(abs_val(0), 0);
}

TEST(test_void_function) {
    int result = 0;
    auto setValue = [&result](int x) { result = x; };
    setValue(42);
    ASSERT_EQ(result, 42);
}

// Edge cases
TEST(test_function_with_no_parameters) {
    auto getConstant = []() { return 100; };
    ASSERT_EQ(getConstant(), 100);
}

TEST(test_nested_function_calls) {
    auto double_val = [](int x) { return x * 2; };
    auto add_ten = [](int x) { return x + 10; };

    int result = add_ten(double_val(5));
    ASSERT_EQ(result, 20);  // (5 * 2) + 10
}

TEST(test_recursion_fibonacci) {
    auto fib = [](auto&& self, int n) -> int {
        if (n <= 1) return n;
        return self(self, n - 1) + self(self, n - 2);
    };

    ASSERT_EQ(fib(fib, 0), 0);
    ASSERT_EQ(fib(fib, 1), 1);
    ASSERT_EQ(fib(fib, 7), 13);
}

int main() {
    std::cout << "=== Running Tests for Program 106: Functions ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_basic_function);
    RUN_TEST(test_function_overloading);
    RUN_TEST(test_default_parameters);
    RUN_TEST(test_pass_by_value);
    RUN_TEST(test_pass_by_reference);
    RUN_TEST(test_pass_by_pointer);
    RUN_TEST(test_pass_null_pointer);
    RUN_TEST(test_recursion_factorial);
    RUN_TEST(test_inline_function);
    RUN_TEST(test_lambda_basic);
    RUN_TEST(test_lambda_capture_by_value);
    RUN_TEST(test_lambda_capture_by_reference);
    RUN_TEST(test_lambda_capture_all);
    RUN_TEST(test_lambda_modify_capture);
    RUN_TEST(test_return_types);
    RUN_TEST(test_multiple_return_paths);
    RUN_TEST(test_void_function);
    RUN_TEST(test_function_with_no_parameters);
    RUN_TEST(test_nested_function_calls);
    RUN_TEST(test_recursion_fibonacci);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
