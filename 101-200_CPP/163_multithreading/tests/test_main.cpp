/*
 * Test Suite for Program 163: Multithreading
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

void simple_function(int& result) {
    result = 42;
}

TEST(test_basic_thread) {
    int result = 0;
    thread t(simple_function, ref(result));
    t.join();
    ASSERT_EQ(result, 42);
}

TEST(test_multiple_threads) {
    atomic<int> counter{0};
    vector<thread> threads;

    for (int i = 0; i < 10; i++) {
        threads.emplace_back([&counter]() {
            counter++;
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    ASSERT_EQ(counter.load(), 10);
}

TEST(test_thread_with_lambda) {
    int value = 0;
    thread t([&value]() { value = 100; });
    t.join();
    ASSERT_EQ(value, 100);
}

TEST(test_hardware_concurrency) {
    unsigned int num = thread::hardware_concurrency();
    ASSERT_TRUE(num > 0);
}

int main() {
    cout << "Running Multithreading Tests\n============================\n\n";
    RUN_TEST(test_basic_thread);
    RUN_TEST(test_multiple_threads);
    RUN_TEST(test_thread_with_lambda);
    RUN_TEST(test_hardware_concurrency);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
