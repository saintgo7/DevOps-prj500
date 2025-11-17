/*
 * Test Suite for Program 174: std::optional (C++17)
 */

#include <iostream>
#include <optional>
#include <string>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

optional<int> find_value(bool exists) {
    if (exists) return 42;
    return nullopt;
}

optional<string> get_name(bool has_name) {
    if (has_name) return "John";
    return nullopt;
}

TEST(test_optional_has_value) {
    optional<int> opt = 42;
    ASSERT_TRUE(opt.has_value());
    ASSERT_EQ(opt.value(), 42);
}

TEST(test_optional_no_value) {
    optional<int> opt;
    ASSERT_TRUE(!opt.has_value());
}

TEST(test_optional_value_or) {
    optional<int> opt1 = 42;
    optional<int> opt2;

    ASSERT_EQ(opt1.value_or(0), 42);
    ASSERT_EQ(opt2.value_or(100), 100);
}

TEST(test_optional_assignment) {
    optional<int> opt;
    opt = 50;
    ASSERT_TRUE(opt.has_value());
    ASSERT_EQ(opt.value(), 50);

    opt = nullopt;
    ASSERT_TRUE(!opt.has_value());
}

TEST(test_optional_string) {
    optional<string> opt = "Hello";
    ASSERT_TRUE(opt.has_value());
    ASSERT_EQ(opt.value(), "Hello");
}

TEST(test_optional_function_return) {
    auto result1 = find_value(true);
    auto result2 = find_value(false);

    ASSERT_TRUE(result1.has_value());
    ASSERT_EQ(result1.value(), 42);
    ASSERT_TRUE(!result2.has_value());
}

TEST(test_optional_dereferencing) {
    optional<int> opt = 100;
    ASSERT_EQ(*opt, 100);
}

TEST(test_optional_reset) {
    optional<int> opt = 42;
    opt.reset();
    ASSERT_TRUE(!opt.has_value());
}

int main() {
    cout << "Running std::optional Tests\n===========================\n\n";
    RUN_TEST(test_optional_has_value);
    RUN_TEST(test_optional_no_value);
    RUN_TEST(test_optional_value_or);
    RUN_TEST(test_optional_assignment);
    RUN_TEST(test_optional_string);
    RUN_TEST(test_optional_function_return);
    RUN_TEST(test_optional_dereferencing);
    RUN_TEST(test_optional_reset);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
