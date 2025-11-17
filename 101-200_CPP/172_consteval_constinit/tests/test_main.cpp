/*
 * Test Suite for Program 172: Consteval and Constinit (C++20)
 */

#include <iostream>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

// constexpr - can be evaluated at compile-time or runtime
constexpr int ce_square(int x) {
    return x * x;
}

// consteval - MUST be evaluated at compile-time (C++20)
#if __cplusplus >= 202002L
consteval int cv_square(int x) {
    return x * x;
}
#endif

// constinit - ensures compile-time initialization (C++20)
#if __cplusplus >= 202002L
constinit int global_value = 42;
#else
constexpr int global_value = 42;
#endif

TEST(test_constexpr_usage) {
    constexpr int ct = ce_square(5);
    ASSERT_EQ(ct, 25);

    int x = 10;
    int rt = ce_square(x);  // Can be runtime
    ASSERT_EQ(rt, 100);
}

#if __cplusplus >= 202002L
TEST(test_consteval_usage) {
    constexpr int result = cv_square(7);  // Must be compile-time
    ASSERT_EQ(result, 49);
}
#endif

TEST(test_constinit_global) {
    ASSERT_EQ(global_value, 42);
}

TEST(test_compile_time_guarantee) {
    constexpr int value = ce_square(6);
    static_assert(value == 36, "Compile-time check");
    ASSERT_EQ(value, 36);
}

int main() {
    cout << "Running Consteval and Constinit Tests\n======================================\n\n";
    RUN_TEST(test_constexpr_usage);
#if __cplusplus >= 202002L
    RUN_TEST(test_consteval_usage);
#endif
    RUN_TEST(test_constinit_global);
    RUN_TEST(test_compile_time_guarantee);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
