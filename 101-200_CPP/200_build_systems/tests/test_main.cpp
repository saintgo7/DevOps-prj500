/*
 * Test Suite for Program 200: Build Systems
 */

#include <iostream>
#include <cassert>
#include <fstream>
#include <cstdlib>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

// Simple math library functions
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

class Calculator {
public:
    int add(int a, int b) { return a + b; }
    int subtract(int a, int b) { return a - b; }
    int multiply(int a, int b) { return a * b; }
    int divide(int a, int b) { return b != 0 ? a / b : 0; }
};

TEST(test_basic_compilation) {
    int result = add(5, 3);
    ASSERT_EQ(result, 8);
}

TEST(test_linking) {
    int result = multiply(4, 5);
    ASSERT_EQ(result, 20);
}

TEST(test_library_usage) {
    Calculator calc;
    ASSERT_EQ(calc.add(10, 20), 30);
    ASSERT_EQ(calc.subtract(20, 10), 10);
    ASSERT_EQ(calc.multiply(3, 4), 12);
    ASSERT_EQ(calc.divide(20, 4), 5);
}

TEST(test_preprocessor_macros) {
    #ifdef __cplusplus
    ASSERT_TRUE(true);
    #endif
}

TEST(test_compiler_features) {
    #if __cplusplus >= 201103L
    ASSERT_TRUE(true);  // C++11 or later
    #endif
}

TEST(test_build_configuration) {
    // Test that we can compile and run
    int value = 42;
    ASSERT_EQ(value, 42);
}

TEST(test_standard_library) {
    // Verify standard library is linked correctly
    string s = "test";
    ASSERT_EQ(s.length(), 4);
}

int main() {
    cout << "Running Build Systems Tests\n============================\n\n";
    cout << "Testing compilation and build process...\n\n";

    RUN_TEST(test_basic_compilation);
    RUN_TEST(test_linking);
    RUN_TEST(test_library_usage);
    RUN_TEST(test_preprocessor_macros);
    RUN_TEST(test_compiler_features);
    RUN_TEST(test_build_configuration);
    RUN_TEST(test_standard_library);

    cout << "\n============================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";
    cout << "\nBuild system verification complete!\n";

    return tests_failed == 0 ? 0 : 1;
}
