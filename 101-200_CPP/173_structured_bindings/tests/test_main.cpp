/*
 * Test Suite for Program 173: Structured Bindings (C++17)
 */

#include <iostream>
#include <tuple>
#include <map>
#include <string>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

struct Point {
    int x, y;
};

tuple<int, string, double> get_person() {
    return {25, "John", 5.9};
}

TEST(test_tuple_binding) {
    auto [age, name, height] = get_person();
    ASSERT_EQ(age, 25);
    ASSERT_EQ(name, "John");
    ASSERT_EQ(height, 5.9);
}

TEST(test_pair_binding) {
    pair<int, string> p = {42, "answer"};
    auto [num, text] = p;
    ASSERT_EQ(num, 42);
    ASSERT_EQ(text, "answer");
}

TEST(test_struct_binding) {
    Point pt{10, 20};
    auto [x, y] = pt;
    ASSERT_EQ(x, 10);
    ASSERT_EQ(y, 20);
}

TEST(test_array_binding) {
    int arr[] = {1, 2, 3};
    auto [a, b, c] = arr;
    ASSERT_EQ(a, 1);
    ASSERT_EQ(b, 2);
    ASSERT_EQ(c, 3);
}

TEST(test_map_iteration) {
    map<string, int> m = {{"one", 1}, {"two", 2}};
    int sum = 0;

    for (const auto& [key, value] : m) {
        sum += value;
    }

    ASSERT_EQ(sum, 3);
}

TEST(test_reference_binding) {
    Point pt{5, 10};
    auto& [x, y] = pt;

    x = 100;
    y = 200;

    ASSERT_EQ(pt.x, 100);
    ASSERT_EQ(pt.y, 200);
}

int main() {
    cout << "Running Structured Bindings Tests\n==================================\n\n";
    RUN_TEST(test_tuple_binding);
    RUN_TEST(test_pair_binding);
    RUN_TEST(test_struct_binding);
    RUN_TEST(test_array_binding);
    RUN_TEST(test_map_iteration);
    RUN_TEST(test_reference_binding);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
