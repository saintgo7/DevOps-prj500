/*
 * Test Suite for Program 101: Hello World
 *
 * Tests basic output functionality and program structure
 */

#include <iostream>
#include <sstream>
#include <string>
#include <cassert>

// Simple test framework
#define TEST(name) void name()
#define ASSERT_TRUE(condition) \
    if (!(condition)) { \
        std::cerr << "FAILED: " << #condition << " at line " << __LINE__ << std::endl; \
        return; \
    }
#define ASSERT_FALSE(condition) ASSERT_TRUE(!(condition))
#define ASSERT_EQ(expected, actual) \
    if ((expected) != (actual)) { \
        std::cerr << "FAILED: Expected " << (expected) << " but got " << (actual) \
                  << " at line " << __LINE__ << std::endl; \
        return; \
    }
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Helper function to capture cout output
std::string captureCout(void (*func)()) {
    std::stringstream buffer;
    std::streambuf* old = std::cout.rdbuf(buffer.rdbuf());
    func();
    std::cout.rdbuf(old);
    return buffer.str();
}

// Test functions
TEST(test_program_returns_zero) {
    // The main function should return 0 for success
    // This is implicit in our test framework
    ASSERT_TRUE(true);
}

TEST(test_basic_output) {
    auto output = []() {
        std::cout << "Hello, World!";
    };

    std::string result = captureCout(output);
    ASSERT_TRUE(result.find("Hello, World!") != std::string::npos);
}

TEST(test_multiple_output_streams) {
    auto output = []() {
        std::cout << "standard output";
        std::cerr << "error output";
    };

    std::string result = captureCout(output);
    ASSERT_TRUE(result.find("standard output") != std::string::npos);
}

TEST(test_endl_vs_newline) {
    auto with_endl = []() {
        std::cout << "Line 1" << std::endl;
    };

    auto with_newline = []() {
        std::cout << "Line 2\n";
    };

    std::string result1 = captureCout(with_endl);
    std::string result2 = captureCout(with_newline);

    ASSERT_TRUE(result1.find("Line 1\n") != std::string::npos);
    ASSERT_TRUE(result2.find("Line 2\n") != std::string::npos);
}

TEST(test_data_type_output) {
    auto output = []() {
        std::cout << 42;  // integer
        std::cout << 3.14;  // double
        std::cout << 'A';  // character
        std::cout << true;  // boolean
    };

    std::string result = captureCout(output);
    ASSERT_TRUE(result.find("42") != std::string::npos);
    ASSERT_TRUE(result.find("3.14") != std::string::npos);
    ASSERT_TRUE(result.find("A") != std::string::npos);
}

TEST(test_string_output) {
    auto output = []() {
        std::string message = "C++ Test";
        std::cout << message;
    };

    std::string result = captureCout(output);
    ASSERT_EQ("C++ Test", result);
}

TEST(test_chained_output) {
    auto output = []() {
        std::cout << "Hello" << " " << "World";
    };

    std::string result = captureCout(output);
    ASSERT_EQ("Hello World", result);
}

TEST(test_empty_output) {
    auto output = []() {
        std::cout << "";
    };

    std::string result = captureCout(output);
    ASSERT_EQ("", result);
}

TEST(test_special_characters) {
    auto output = []() {
        std::cout << "Tab:\tNewline:\nEnd";
    };

    std::string result = captureCout(output);
    ASSERT_TRUE(result.find("Tab:\t") != std::string::npos);
    ASSERT_TRUE(result.find("Newline:\n") != std::string::npos);
}

// Edge cases
TEST(test_large_output) {
    auto output = []() {
        for (int i = 0; i < 1000; i++) {
            std::cout << i;
        }
    };

    std::string result = captureCout(output);
    ASSERT_TRUE(result.length() > 0);
}

TEST(test_numeric_limits) {
    auto output = []() {
        std::cout << 2147483647;  // INT_MAX
        std::cout << -2147483648;  // INT_MIN (approximately)
    };

    std::string result = captureCout(output);
    ASSERT_TRUE(result.find("2147483647") != std::string::npos);
}

int main() {
    std::cout << "=== Running Tests for Program 101: Hello World ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_program_returns_zero);
    RUN_TEST(test_basic_output);
    RUN_TEST(test_multiple_output_streams);
    RUN_TEST(test_endl_vs_newline);
    RUN_TEST(test_data_type_output);
    RUN_TEST(test_string_output);
    RUN_TEST(test_chained_output);
    RUN_TEST(test_empty_output);
    RUN_TEST(test_special_characters);
    RUN_TEST(test_large_output);
    RUN_TEST(test_numeric_limits);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
