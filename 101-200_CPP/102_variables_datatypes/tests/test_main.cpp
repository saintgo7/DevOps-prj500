/*
 * Test Suite for Program 102: Variables and Data Types
 *
 * Tests fundamental data types, type modifiers, and type inference
 */

#include <iostream>
#include <limits>
#include <cstdint>
#include <string>
#include <cassert>

// Simple test framework
#define TEST(name) void name()
#define ASSERT_TRUE(condition) assert(condition)
#define ASSERT_FALSE(condition) assert(!(condition))
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Test fundamental types
TEST(test_boolean_type) {
    bool isTrue = true;
    bool isFalse = false;
    ASSERT_TRUE(isTrue);
    ASSERT_FALSE(isFalse);
    ASSERT_EQ(sizeof(bool), 1);
}

TEST(test_character_type) {
    char letter = 'A';
    char digit = '5';
    ASSERT_EQ(letter, 'A');
    ASSERT_EQ(digit, '5');
    ASSERT_EQ(sizeof(char), 1);
}

TEST(test_integer_type) {
    int positiveNum = 42;
    int negativeNum = -42;
    int zero = 0;
    ASSERT_EQ(positiveNum, 42);
    ASSERT_EQ(negativeNum, -42);
    ASSERT_EQ(zero, 0);
    ASSERT_TRUE(sizeof(int) >= 4);
}

TEST(test_floating_point_types) {
    float f = 3.14f;
    double d = 3.14159;
    long double ld = 3.14159265358979323846L;

    ASSERT_TRUE(f > 3.13f && f < 3.15f);
    ASSERT_TRUE(d > 3.14 && d < 3.15);
    ASSERT_TRUE(ld > 3.14L && ld < 3.15L);

    ASSERT_EQ(sizeof(float), 4);
    ASSERT_EQ(sizeof(double), 8);
}

// Test type modifiers
TEST(test_signed_unsigned) {
    signed int signedNum = -100;
    unsigned int unsignedNum = 100;

    ASSERT_EQ(signedNum, -100);
    ASSERT_EQ(unsignedNum, 100);
    ASSERT_TRUE(signedNum < 0);
    ASSERT_TRUE(unsignedNum > 0);
}

TEST(test_short_long) {
    short smallNum = 32000;
    long largeNum = 2000000000L;
    long long veryLargeNum = 9000000000000000000LL;

    ASSERT_EQ(smallNum, 32000);
    ASSERT_EQ(largeNum, 2000000000L);
    ASSERT_TRUE(sizeof(short) <= sizeof(int));
    ASSERT_TRUE(sizeof(int) <= sizeof(long));
    ASSERT_TRUE(sizeof(long) <= sizeof(long long));
}

// Test variable initialization
TEST(test_initialization_methods) {
    int a = 10;          // Copy initialization
    int b(20);           // Direct initialization
    int c{30};           // Uniform initialization
    int d = {40};        // Copy-list initialization

    ASSERT_EQ(a, 10);
    ASSERT_EQ(b, 20);
    ASSERT_EQ(c, 30);
    ASSERT_EQ(d, 40);
}

TEST(test_zero_initialization) {
    int arr1[3] = {0};
    int arr2[3] = {};

    for (int i = 0; i < 3; i++) {
        ASSERT_EQ(arr1[i], 0);
        ASSERT_EQ(arr2[i], 0);
    }
}

// Test auto keyword
TEST(test_auto_keyword) {
    auto intVar = 42;
    auto floatVar = 3.14f;
    auto doubleVar = 3.14;
    auto charVar = 'A';
    auto boolVar = true;

    ASSERT_EQ(intVar, 42);
    ASSERT_TRUE(floatVar > 3.13f && floatVar < 3.15f);
    ASSERT_TRUE(doubleVar > 3.13 && doubleVar < 3.15);
    ASSERT_EQ(charVar, 'A');
    ASSERT_TRUE(boolVar);
}

// Test constants
TEST(test_const_variables) {
    const int MAX_SIZE = 100;
    constexpr int COMPILE_TIME_VALUE = 50;

    ASSERT_EQ(MAX_SIZE, 100);
    ASSERT_EQ(COMPILE_TIME_VALUE, 50);

    // These should compile
    int arr1[MAX_SIZE];
    int arr2[COMPILE_TIME_VALUE];
    ASSERT_TRUE(sizeof(arr1) > 0);
    ASSERT_TRUE(sizeof(arr2) > 0);
}

// Test fixed-width integer types
TEST(test_fixed_width_types) {
    int8_t i8 = 127;
    int16_t i16 = 32767;
    int32_t i32 = 2147483647;
    int64_t i64 = 9223372036854775807LL;

    uint8_t ui8 = 255;
    uint16_t ui16 = 65535;
    uint32_t ui32 = 4294967295U;

    ASSERT_EQ(sizeof(int8_t), 1);
    ASSERT_EQ(sizeof(int16_t), 2);
    ASSERT_EQ(sizeof(int32_t), 4);
    ASSERT_EQ(sizeof(int64_t), 8);

    ASSERT_EQ(i8, 127);
    ASSERT_EQ(i16, 32767);
    ASSERT_EQ(i32, 2147483647);
}

// Test numeric limits
TEST(test_numeric_limits) {
    ASSERT_TRUE(std::numeric_limits<int>::min() < 0);
    ASSERT_TRUE(std::numeric_limits<int>::max() > 0);
    ASSERT_TRUE(std::numeric_limits<unsigned int>::min() == 0);
    ASSERT_TRUE(std::numeric_limits<unsigned int>::max() > 0);
}

// Test literals
TEST(test_integer_literals) {
    int decimal = 42;
    int octal = 052;      // 42 in octal
    int hex = 0x2A;       // 42 in hex
    int binary = 0b101010; // 42 in binary

    ASSERT_EQ(decimal, 42);
    ASSERT_EQ(octal, 42);
    ASSERT_EQ(hex, 42);
    ASSERT_EQ(binary, 42);
}

TEST(test_floating_literals) {
    float f = 3.14f;
    double d = 3.14;
    long double ld = 3.14L;
    double scientific = 1.23e4; // 12300

    ASSERT_TRUE(f > 3.13f);
    ASSERT_TRUE(d > 3.13);
    ASSERT_TRUE(ld > 3.13L);
    ASSERT_EQ(scientific, 12300.0);
}

// Test type aliases
TEST(test_type_aliases) {
    typedef unsigned long ulong;
    using real = double;

    ulong bigNumber = 1000000UL;
    real pi = 3.14159;

    ASSERT_EQ(bigNumber, 1000000UL);
    ASSERT_TRUE(pi > 3.14 && pi < 3.15);
}

// Edge cases
TEST(test_integer_overflow) {
    unsigned char maxUChar = 255;
    unsigned char overflow = maxUChar + 1; // Wraps to 0
    ASSERT_EQ(overflow, 0);
}

TEST(test_type_conversion) {
    int intVal = 10;
    double doubleVal = intVal; // Implicit conversion
    ASSERT_EQ(doubleVal, 10.0);

    double d = 3.7;
    int i = static_cast<int>(d); // Explicit conversion
    ASSERT_EQ(i, 3);
}

TEST(test_variable_scope) {
    int outer = 100;
    ASSERT_EQ(outer, 100);

    {
        int inner = 200;
        ASSERT_EQ(inner, 200);
        ASSERT_EQ(outer, 100); // Can access outer
    }

    // inner is not accessible here
    ASSERT_EQ(outer, 100);
}

int main() {
    std::cout << "=== Running Tests for Program 102: Variables and Data Types ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_boolean_type);
    RUN_TEST(test_character_type);
    RUN_TEST(test_integer_type);
    RUN_TEST(test_floating_point_types);
    RUN_TEST(test_signed_unsigned);
    RUN_TEST(test_short_long);
    RUN_TEST(test_initialization_methods);
    RUN_TEST(test_zero_initialization);
    RUN_TEST(test_auto_keyword);
    RUN_TEST(test_const_variables);
    RUN_TEST(test_fixed_width_types);
    RUN_TEST(test_numeric_limits);
    RUN_TEST(test_integer_literals);
    RUN_TEST(test_floating_literals);
    RUN_TEST(test_type_aliases);
    RUN_TEST(test_integer_overflow);
    RUN_TEST(test_type_conversion);
    RUN_TEST(test_variable_scope);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
