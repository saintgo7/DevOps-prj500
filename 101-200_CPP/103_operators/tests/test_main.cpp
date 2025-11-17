/*
 * Test Suite for Program 103: Operators
 *
 * Tests arithmetic, logical, relational, bitwise, and other operators
 */

#include <iostream>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define ASSERT_FALSE(condition) assert(!(condition))
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Arithmetic operators
TEST(test_addition) {
    ASSERT_EQ(5 + 3, 8);
    ASSERT_EQ(-5 + 3, -2);
    ASSERT_EQ(0 + 0, 0);
}

TEST(test_subtraction) {
    ASSERT_EQ(10 - 3, 7);
    ASSERT_EQ(3 - 10, -7);
    ASSERT_EQ(5 - 5, 0);
}

TEST(test_multiplication) {
    ASSERT_EQ(5 * 3, 15);
    ASSERT_EQ(-5 * 3, -15);
    ASSERT_EQ(5 * 0, 0);
}

TEST(test_division) {
    ASSERT_EQ(10 / 2, 5);
    ASSERT_EQ(15 / 4, 3);  // Integer division
    ASSERT_TRUE(10.0 / 4.0 == 2.5);  // Floating-point division
}

TEST(test_modulo) {
    ASSERT_EQ(10 % 3, 1);
    ASSERT_EQ(15 % 5, 0);
    ASSERT_EQ(7 % 8, 7);
}

// Increment/Decrement
TEST(test_increment_decrement) {
    int x = 5;
    ASSERT_EQ(++x, 6);  // Pre-increment
    ASSERT_EQ(x, 6);

    int y = 5;
    ASSERT_EQ(y++, 5);  // Post-increment
    ASSERT_EQ(y, 6);

    int z = 5;
    ASSERT_EQ(--z, 4);  // Pre-decrement
    ASSERT_EQ(z, 4);

    int w = 5;
    ASSERT_EQ(w--, 5);  // Post-decrement
    ASSERT_EQ(w, 4);
}

// Relational operators
TEST(test_comparison_operators) {
    ASSERT_TRUE(5 > 3);
    ASSERT_TRUE(3 < 5);
    ASSERT_TRUE(5 >= 5);
    ASSERT_TRUE(5 <= 5);
    ASSERT_TRUE(5 == 5);
    ASSERT_TRUE(5 != 3);
}

TEST(test_comparison_edge_cases) {
    ASSERT_TRUE(0 == 0);
    ASSERT_TRUE(-5 < 0);
    ASSERT_TRUE(0 < 5);
    ASSERT_FALSE(5 == 6);
}

// Logical operators
TEST(test_logical_and) {
    ASSERT_TRUE(true && true);
    ASSERT_FALSE(true && false);
    ASSERT_FALSE(false && true);
    ASSERT_FALSE(false && false);
}

TEST(test_logical_or) {
    ASSERT_TRUE(true || true);
    ASSERT_TRUE(true || false);
    ASSERT_TRUE(false || true);
    ASSERT_FALSE(false || false);
}

TEST(test_logical_not) {
    ASSERT_TRUE(!false);
    ASSERT_FALSE(!true);
}

// Bitwise operators
TEST(test_bitwise_and) {
    ASSERT_EQ(5 & 3, 1);    // 101 & 011 = 001
    ASSERT_EQ(12 & 10, 8);  // 1100 & 1010 = 1000
}

TEST(test_bitwise_or) {
    ASSERT_EQ(5 | 3, 7);    // 101 | 011 = 111
    ASSERT_EQ(12 | 10, 14); // 1100 | 1010 = 1110
}

TEST(test_bitwise_xor) {
    ASSERT_EQ(5 ^ 3, 6);    // 101 ^ 011 = 110
    ASSERT_EQ(12 ^ 10, 6);  // 1100 ^ 1010 = 0110
}

TEST(test_bitwise_not) {
    unsigned char a = 5;    // 00000101
    unsigned char result = ~a; // 11111010 = 250
    ASSERT_EQ(result, 250);
}

TEST(test_bit_shift) {
    ASSERT_EQ(5 << 1, 10);  // Left shift: 5 * 2
    ASSERT_EQ(5 << 2, 20);  // Left shift: 5 * 4
    ASSERT_EQ(20 >> 1, 10); // Right shift: 20 / 2
    ASSERT_EQ(20 >> 2, 5);  // Right shift: 20 / 4
}

// Assignment operators
TEST(test_compound_assignment) {
    int x = 10;
    x += 5;
    ASSERT_EQ(x, 15);

    x -= 3;
    ASSERT_EQ(x, 12);

    x *= 2;
    ASSERT_EQ(x, 24);

    x /= 4;
    ASSERT_EQ(x, 6);

    x %= 4;
    ASSERT_EQ(x, 2);
}

TEST(test_bitwise_compound_assignment) {
    int x = 5;
    x &= 3;
    ASSERT_EQ(x, 1);

    x = 5;
    x |= 3;
    ASSERT_EQ(x, 7);

    x = 5;
    x ^= 3;
    ASSERT_EQ(x, 6);

    x = 5;
    x <<= 2;
    ASSERT_EQ(x, 20);

    x = 20;
    x >>= 2;
    ASSERT_EQ(x, 5);
}

// Ternary operator
TEST(test_ternary_operator) {
    int result = (5 > 3) ? 10 : 20;
    ASSERT_EQ(result, 10);

    result = (5 < 3) ? 10 : 20;
    ASSERT_EQ(result, 20);
}

// Comma operator
TEST(test_comma_operator) {
    int x = (5, 10, 15);
    ASSERT_EQ(x, 15);  // Comma operator returns last value
}

// Sizeof operator
TEST(test_sizeof_operator) {
    ASSERT_EQ(sizeof(char), 1);
    ASSERT_TRUE(sizeof(int) >= 4);
    ASSERT_EQ(sizeof(double), 8);
}

// Operator precedence
TEST(test_operator_precedence) {
    ASSERT_EQ(5 + 3 * 2, 11);      // Multiplication first
    ASSERT_EQ((5 + 3) * 2, 16);    // Parentheses change order
    ASSERT_EQ(10 - 5 - 2, 3);      // Left-to-right
    ASSERT_EQ(2 + 3 * 4 - 5, 9);   // Mixed operations
}

// Edge cases
TEST(test_division_by_zero_check) {
    int divisor = 0;
    // We can't divide by zero, but we can test the check
    ASSERT_TRUE(divisor == 0);
}

TEST(test_overflow) {
    unsigned char max = 255;
    unsigned char overflow = max + 1;
    ASSERT_EQ(overflow, 0);  // Wraps around
}

TEST(test_negative_modulo) {
    ASSERT_EQ(-10 % 3, -1);
    ASSERT_EQ(10 % -3, 1);
}

int main() {
    std::cout << "=== Running Tests for Program 103: Operators ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_addition);
    RUN_TEST(test_subtraction);
    RUN_TEST(test_multiplication);
    RUN_TEST(test_division);
    RUN_TEST(test_modulo);
    RUN_TEST(test_increment_decrement);
    RUN_TEST(test_comparison_operators);
    RUN_TEST(test_comparison_edge_cases);
    RUN_TEST(test_logical_and);
    RUN_TEST(test_logical_or);
    RUN_TEST(test_logical_not);
    RUN_TEST(test_bitwise_and);
    RUN_TEST(test_bitwise_or);
    RUN_TEST(test_bitwise_xor);
    RUN_TEST(test_bitwise_not);
    RUN_TEST(test_bit_shift);
    RUN_TEST(test_compound_assignment);
    RUN_TEST(test_bitwise_compound_assignment);
    RUN_TEST(test_ternary_operator);
    RUN_TEST(test_comma_operator);
    RUN_TEST(test_sizeof_operator);
    RUN_TEST(test_operator_precedence);
    RUN_TEST(test_division_by_zero_check);
    RUN_TEST(test_overflow);
    RUN_TEST(test_negative_modulo);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
