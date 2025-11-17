/*
 * Test Suite for Program 171: Constexpr Functions
 */

#include <iostream>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

constexpr int square(int x) {
    return x * x;
}

constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int fibonacci(int n) {
    return n <= 1 ? n : fibonacci(n-1) + fibonacci(n-2);
}

constexpr bool is_prime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

TEST(test_constexpr_square) {
    constexpr int result = square(5);
    ASSERT_EQ(result, 25);
    ASSERT_EQ(square(10), 100);
}

TEST(test_constexpr_factorial) {
    constexpr int result = factorial(5);
    ASSERT_EQ(result, 120);
    ASSERT_EQ(factorial(0), 1);
    ASSERT_EQ(factorial(6), 720);
}

TEST(test_constexpr_fibonacci) {
    constexpr int result = fibonacci(10);
    ASSERT_EQ(result, 55);
    ASSERT_EQ(fibonacci(0), 0);
    ASSERT_EQ(fibonacci(1), 1);
    ASSERT_EQ(fibonacci(7), 13);
}

TEST(test_constexpr_is_prime) {
    constexpr bool result1 = is_prime(7);
    constexpr bool result2 = is_prime(10);
    ASSERT_EQ(result1, true);
    ASSERT_EQ(result2, false);
    ASSERT_EQ(is_prime(2), true);
    ASSERT_EQ(is_prime(17), true);
    ASSERT_EQ(is_prime(20), false);
}

TEST(test_compile_time_vs_runtime) {
    // Compile-time
    constexpr int ct_result = square(8);
    ASSERT_EQ(ct_result, 64);

    // Runtime
    int x = 8;
    int rt_result = square(x);
    ASSERT_EQ(rt_result, 64);
}

int main() {
    cout << "Running Constexpr Functions Tests\n==================================\n\n";
    RUN_TEST(test_constexpr_square);
    RUN_TEST(test_constexpr_factorial);
    RUN_TEST(test_constexpr_fibonacci);
    RUN_TEST(test_constexpr_is_prime);
    RUN_TEST(test_compile_time_vs_runtime);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
