/*
 * Test Suite for Program 199: Debugging Tools
 */

#include <iostream>
#include <cassert>
#include <cstring>
#include <stdexcept>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

// Debug logging
void debug_log(const char* msg) {
    #ifdef DEBUG
    cout << "[DEBUG] " << msg << "\n";
    #endif
}

// Assert usage
void test_assert_condition(int value) {
    assert(value > 0);
}

TEST(test_basic_assertion) {
    test_assert_condition(10);
    ASSERT_TRUE(true);
}

TEST(test_debug_logging) {
    debug_log("Test message");
    ASSERT_TRUE(true);
}

TEST(test_exception_handling) {
    try {
        throw runtime_error("Test exception");
    } catch (const exception& e) {
        ASSERT_TRUE(strlen(e.what()) > 0);
    }
}

TEST(test_bounds_checking) {
    int arr[5] = {1, 2, 3, 4, 5};
    int index = 2;

    if (index >= 0 && index < 5) {
        ASSERT_EQ(arr[index], 3);
    }
}

TEST(test_null_pointer_check) {
    int* ptr = new int(42);
    ASSERT_TRUE(ptr != nullptr);

    if (ptr) {
        ASSERT_EQ(*ptr, 42);
    }

    delete ptr;
}

TEST(test_memory_initialization) {
    int* arr = new int[5]();  // Zero-initialized
    ASSERT_EQ(arr[0], 0);
    delete[] arr;
}

TEST(test_compile_time_checks) {
    static_assert(sizeof(int) >= 4, "int must be at least 4 bytes");
    ASSERT_TRUE(true);
}

int main() {
    cout << "Running Debugging Tools Tests\n==============================\n\n";
    RUN_TEST(test_basic_assertion);
    RUN_TEST(test_debug_logging);
    RUN_TEST(test_exception_handling);
    RUN_TEST(test_bounds_checking);
    RUN_TEST(test_null_pointer_check);
    RUN_TEST(test_memory_initialization);
    RUN_TEST(test_compile_time_checks);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
