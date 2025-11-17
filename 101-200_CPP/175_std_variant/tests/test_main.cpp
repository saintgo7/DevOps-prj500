/*
 * Test Suite for Program 175: std::variant (C++17)
 */

#include <iostream>
#include <variant>
#include <string>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_variant_int) {
    variant<int, string, double> v = 42;
    ASSERT_TRUE(holds_alternative<int>(v));
    ASSERT_EQ(get<int>(v), 42);
}

TEST(test_variant_string) {
    variant<int, string, double> v = "hello";
    ASSERT_TRUE(holds_alternative<string>(v));
    ASSERT_EQ(get<string>(v), "hello");
}

TEST(test_variant_double) {
    variant<int, string, double> v = 3.14;
    ASSERT_TRUE(holds_alternative<double>(v));
    ASSERT_EQ(get<double>(v), 3.14);
}

TEST(test_variant_index) {
    variant<int, string, double> v = 42;
    ASSERT_EQ(v.index(), 0);

    v = "test";
    ASSERT_EQ(v.index(), 1);

    v = 2.71;
    ASSERT_EQ(v.index(), 2);
}

TEST(test_variant_visit) {
    variant<int, string> v = 42;

    int result = visit([](auto&& arg) -> int {
        using T = decay_t<decltype(arg)>;
        if constexpr (is_same_v<T, int>)
            return arg * 2;
        else
            return 0;
    }, v);

    ASSERT_EQ(result, 84);
}

TEST(test_variant_reassignment) {
    variant<int, string> v = 10;
    ASSERT_EQ(get<int>(v), 10);

    v = "changed";
    ASSERT_EQ(get<string>(v), "changed");
}

TEST(test_variant_get_if) {
    variant<int, string> v = 100;

    int* ptr = get_if<int>(&v);
    ASSERT_TRUE(ptr != nullptr);
    ASSERT_EQ(*ptr, 100);

    string* sptr = get_if<string>(&v);
    ASSERT_TRUE(sptr == nullptr);
}

int main() {
    cout << "Running std::variant Tests\n==========================\n\n";
    RUN_TEST(test_variant_int);
    RUN_TEST(test_variant_string);
    RUN_TEST(test_variant_double);
    RUN_TEST(test_variant_index);
    RUN_TEST(test_variant_visit);
    RUN_TEST(test_variant_reassignment);
    RUN_TEST(test_variant_get_if);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
