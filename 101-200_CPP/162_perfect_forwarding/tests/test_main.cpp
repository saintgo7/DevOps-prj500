/*
 * Test Suite for Program 162: Perfect Forwarding
 */

#include <iostream>
#include <string>
#include <utility>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

int lvalue_count = 0;
int rvalue_count = 0;

void process(int& x) { lvalue_count++; }
void process(int&& x) { rvalue_count++; }

template<typename T>
void forward_call(T&& arg) {
    process(forward<T>(arg));
}

TEST(test_forward_lvalue) {
    lvalue_count = 0;
    int x = 10;
    forward_call(x);
    ASSERT_EQ(lvalue_count, 1);
}

TEST(test_forward_rvalue) {
    rvalue_count = 0;
    forward_call(10);
    ASSERT_EQ(rvalue_count, 1);
}

TEST(test_multiple_forwards) {
    lvalue_count = rvalue_count = 0;
    int x = 5;
    forward_call(x);
    forward_call(20);
    ASSERT_EQ(lvalue_count, 1);
    ASSERT_EQ(rvalue_count, 1);
}

int main() {
    cout << "Running Perfect Forwarding Tests\n=================================\n\n";
    RUN_TEST(test_forward_lvalue);
    RUN_TEST(test_forward_rvalue);
    RUN_TEST(test_multiple_forwards);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
