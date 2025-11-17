/*
 * Test Suite for Program 197: Compiler Optimization
 */

#include <iostream>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

// Const for optimization
const int CONST_VALUE = 42;

// Inline function
inline int add_inline(int a, int b) {
    return a + b;
}

// Constexpr for compile-time evaluation
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

TEST(test_const_optimization) {
    int value = CONST_VALUE;
    ASSERT_EQ(value, 42);
}

TEST(test_inline_function) {
    int result = add_inline(10, 20);
    ASSERT_EQ(result, 30);
}

TEST(test_constexpr_optimization) {
    constexpr int result = factorial(5);
    ASSERT_EQ(result, 120);
}

TEST(test_loop_optimization) {
    int sum = 0;
    for (int i = 0; i < 100; i++) {
        sum += i;
    }
    ASSERT_EQ(sum, 4950);
}

TEST(test_branch_prediction) {
    int count = 0;
    for (int i = 0; i < 100; i++) {
        if (i < 50) {  // Predictable branch
            count++;
        }
    }
    ASSERT_EQ(count, 50);
}

TEST(test_dead_code_elimination) {
    int x = 10;
    int y = 20;
    int z = x + y;  // This will be kept
    ASSERT_EQ(z, 30);
}

TEST(test_strength_reduction) {
    int result = 0;
    for (int i = 0; i < 10; i++) {
        result += i * 4;  // Can be optimized to shifts
    }
    ASSERT_EQ(result, 180);
}

int main() {
    cout << "Running Compiler Optimization Tests\n====================================\n\n";
    RUN_TEST(test_const_optimization);
    RUN_TEST(test_inline_function);
    RUN_TEST(test_constexpr_optimization);
    RUN_TEST(test_loop_optimization);
    RUN_TEST(test_branch_prediction);
    RUN_TEST(test_dead_code_elimination);
    RUN_TEST(test_strength_reduction);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
