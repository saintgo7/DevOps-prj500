/*
 * Test Suite for Program 158: Ranges (C++20)
 *
 * Tests:
 * - Range views
 * - Range algorithms
 * - Range adaptors
 * - Range transformations
 */

#include <iostream>
#include <vector>
#include <ranges>
#include <algorithm>
#include <cassert>

using namespace std;
namespace ranges = std::ranges;
namespace views = std::views;

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

// Test cases
TEST(test_filter_view) {
    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto evens = v | views::filter([](int n) { return n % 2 == 0; });

    vector<int> result(evens.begin(), evens.end());
    vector<int> expected = {2, 4, 6, 8, 10};

    ASSERT_EQ(result.size(), expected.size());
    ASSERT_TRUE(ranges::equal(result, expected));
}

TEST(test_transform_view) {
    vector<int> v = {1, 2, 3, 4, 5};
    auto squared = v | views::transform([](int n) { return n * n; });

    vector<int> result(squared.begin(), squared.end());
    vector<int> expected = {1, 4, 9, 16, 25};

    ASSERT_TRUE(ranges::equal(result, expected));
}

TEST(test_take_view) {
    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto first_five = v | views::take(5);

    vector<int> result(first_five.begin(), first_five.end());
    vector<int> expected = {1, 2, 3, 4, 5};

    ASSERT_TRUE(ranges::equal(result, expected));
}

TEST(test_drop_view) {
    vector<int> v = {1, 2, 3, 4, 5};
    auto last_three = v | views::drop(2);

    vector<int> result(last_three.begin(), last_three.end());
    vector<int> expected = {3, 4, 5};

    ASSERT_TRUE(ranges::equal(result, expected));
}

TEST(test_composed_views) {
    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto result_view = v
        | views::filter([](int n) { return n % 2 == 0; })
        | views::transform([](int n) { return n * 2; })
        | views::take(3);

    vector<int> result(result_view.begin(), result_view.end());
    vector<int> expected = {4, 8, 12};

    ASSERT_TRUE(ranges::equal(result, expected));
}

TEST(test_iota_view) {
    auto nums = views::iota(1, 6);
    vector<int> result(nums.begin(), nums.end());
    vector<int> expected = {1, 2, 3, 4, 5};

    ASSERT_TRUE(ranges::equal(result, expected));
}

TEST(test_reverse_view) {
    vector<int> v = {1, 2, 3, 4, 5};
    auto reversed = v | views::reverse;

    vector<int> result(reversed.begin(), reversed.end());
    vector<int> expected = {5, 4, 3, 2, 1};

    ASSERT_TRUE(ranges::equal(result, expected));
}

TEST(test_edge_case_empty) {
    vector<int> v;
    auto filtered = v | views::filter([](int n) { return n > 0; });

    ASSERT_TRUE(filtered.empty());
}

TEST(test_edge_case_all_filtered) {
    vector<int> v = {1, 3, 5, 7, 9};
    auto evens = v | views::filter([](int n) { return n % 2 == 0; });

    ASSERT_TRUE(ranges::empty(evens));
}

int main() {
    cout << "Running Ranges Tests\n";
    cout << "====================\n\n";

    RUN_TEST(test_filter_view);
    RUN_TEST(test_transform_view);
    RUN_TEST(test_take_view);
    RUN_TEST(test_drop_view);
    RUN_TEST(test_composed_views);
    RUN_TEST(test_iota_view);
    RUN_TEST(test_reverse_view);
    RUN_TEST(test_edge_case_empty);
    RUN_TEST(test_edge_case_all_filtered);

    cout << "\n====================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
