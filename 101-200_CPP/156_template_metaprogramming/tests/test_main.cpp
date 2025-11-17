/*
 * Test Suite for Program 156: Template Metaprogramming
 *
 * Tests:
 * - Compile-time computations
 * - Factorial computation
 * - Fibonacci computation
 * - Type selection
 * - Compile-time conditionals
 */

#include <iostream>
#include <cassert>
#include <type_traits>

using namespace std;

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

// Compile-time factorial
template<int N>
struct Factorial {
    static const int value = N * Factorial<N-1>::value;
};

template<>
struct Factorial<0> {
    static const int value = 1;
};

// Compile-time Fibonacci
template<int N>
struct Fibonacci {
    static const int value = Fibonacci<N-1>::value + Fibonacci<N-2>::value;
};

template<>
struct Fibonacci<0> {
    static const int value = 0;
};

template<>
struct Fibonacci<1> {
    static const int value = 1;
};

// Compile-time power
template<int Base, int Exp>
struct Power {
    static const int value = Base * Power<Base, Exp-1>::value;
};

template<int Base>
struct Power<Base, 0> {
    static const int value = 1;
};

// Conditional type selection
template<bool Condition, typename T, typename F>
struct IfThenElse {
    using type = T;
};

template<typename T, typename F>
struct IfThenElse<false, T, F> {
    using type = F;
};

// Test cases
TEST(test_factorial) {
    ASSERT_EQ(Factorial<0>::value, 1);
    ASSERT_EQ(Factorial<1>::value, 1);
    ASSERT_EQ(Factorial<5>::value, 120);
    ASSERT_EQ(Factorial<6>::value, 720);
    ASSERT_EQ(Factorial<10>::value, 3628800);
}

TEST(test_fibonacci) {
    ASSERT_EQ(Fibonacci<0>::value, 0);
    ASSERT_EQ(Fibonacci<1>::value, 1);
    ASSERT_EQ(Fibonacci<2>::value, 1);
    ASSERT_EQ(Fibonacci<3>::value, 2);
    ASSERT_EQ(Fibonacci<4>::value, 3);
    ASSERT_EQ(Fibonacci<5>::value, 5);
    ASSERT_EQ(Fibonacci<6>::value, 8);
    ASSERT_EQ(Fibonacci<10>::value, 55);
}

TEST(test_power) {
    ASSERT_EQ((Power<2, 0>::value), 1);
    ASSERT_EQ((Power<2, 1>::value), 2);
    ASSERT_EQ((Power<2, 3>::value), 8);
    ASSERT_EQ((Power<2, 10>::value), 1024);
    ASSERT_EQ((Power<3, 2>::value), 9);
    ASSERT_EQ((Power<5, 3>::value), 125);
}

TEST(test_conditional_type_true) {
    using ResultType = IfThenElse<true, int, double>::type;
    ASSERT_TRUE((is_same<ResultType, int>::value));
}

TEST(test_conditional_type_false) {
    using ResultType = IfThenElse<false, int, double>::type;
    ASSERT_TRUE((is_same<ResultType, double>::value));
}

TEST(test_compile_time_constants) {
    constexpr int fact5 = Factorial<5>::value;
    constexpr int fib10 = Fibonacci<10>::value;
    constexpr int pow2_8 = Power<2, 8>::value;

    ASSERT_EQ(fact5, 120);
    ASSERT_EQ(fib10, 55);
    ASSERT_EQ(pow2_8, 256);
}

TEST(test_edge_case_zero) {
    ASSERT_EQ(Factorial<0>::value, 1);
    ASSERT_EQ(Fibonacci<0>::value, 0);
    ASSERT_EQ((Power<10, 0>::value), 1);
}

TEST(test_edge_case_one) {
    ASSERT_EQ(Factorial<1>::value, 1);
    ASSERT_EQ(Fibonacci<1>::value, 1);
    ASSERT_EQ((Power<5, 1>::value), 5);
}

TEST(test_type_selection_complex) {
    using Type1 = IfThenElse<(5 > 3), long, short>::type;
    using Type2 = IfThenElse<(2 > 10), long, short>::type;

    ASSERT_TRUE((is_same<Type1, long>::value));
    ASSERT_TRUE((is_same<Type2, short>::value));
}

int main() {
    cout << "Running Template Metaprogramming Tests\n";
    cout << "=======================================\n\n";

    RUN_TEST(test_factorial);
    RUN_TEST(test_fibonacci);
    RUN_TEST(test_power);
    RUN_TEST(test_conditional_type_true);
    RUN_TEST(test_conditional_type_false);
    RUN_TEST(test_compile_time_constants);
    RUN_TEST(test_edge_case_zero);
    RUN_TEST(test_edge_case_one);
    RUN_TEST(test_type_selection_complex);

    cout << "\n=======================================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
