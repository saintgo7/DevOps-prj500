/*
 * Test Suite for Program 176: std::any (C++17)
 */

#include <iostream>
#include <any>
#include <string>
#include <vector>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_any_int) {
    any a = 42;
    ASSERT_TRUE(a.has_value());
    ASSERT_EQ(any_cast<int>(a), 42);
}

TEST(test_any_string) {
    any a = string("hello");
    ASSERT_TRUE(a.has_value());
    ASSERT_EQ(any_cast<string>(a), "hello");
}

TEST(test_any_double) {
    any a = 3.14;
    ASSERT_EQ(any_cast<double>(a), 3.14);
}

TEST(test_any_empty) {
    any a;
    ASSERT_TRUE(!a.has_value());
}

TEST(test_any_type_change) {
    any a = 42;
    ASSERT_EQ(any_cast<int>(a), 42);

    a = string("changed");
    ASSERT_EQ(any_cast<string>(a), "changed");

    a = 3.14;
    ASSERT_EQ(any_cast<double>(a), 3.14);
}

TEST(test_any_type) {
    any a = 42;
    ASSERT_TRUE(a.type() == typeid(int));

    a = string("test");
    ASSERT_TRUE(a.type() == typeid(string));
}

TEST(test_any_reset) {
    any a = 42;
    ASSERT_TRUE(a.has_value());

    a.reset();
    ASSERT_TRUE(!a.has_value());
}

TEST(test_any_vector) {
    any a = vector<int>{1, 2, 3};
    auto v = any_cast<vector<int>>(a);
    ASSERT_EQ(v.size(), 3);
    ASSERT_EQ(v[0], 1);
}

int main() {
    cout << "Running std::any Tests\n======================\n\n";
    RUN_TEST(test_any_int);
    RUN_TEST(test_any_string);
    RUN_TEST(test_any_double);
    RUN_TEST(test_any_empty);
    RUN_TEST(test_any_type_change);
    RUN_TEST(test_any_type);
    RUN_TEST(test_any_reset);
    RUN_TEST(test_any_vector);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
