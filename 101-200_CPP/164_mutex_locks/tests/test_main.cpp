/*
 * Test Suite for Program 164: Mutex and Locks
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_mutex_basic) {
    mutex mtx;
    int counter = 0;

    vector<thread> threads;
    for (int i = 0; i < 100; i++) {
        threads.emplace_back([&]() {
            lock_guard<mutex> lock(mtx);
            counter++;
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    ASSERT_EQ(counter, 100);
}

TEST(test_lock_guard) {
    mutex mtx;
    int value = 0;

    {
        lock_guard<mutex> lock(mtx);
        value = 42;
    }

    ASSERT_EQ(value, 42);
}

TEST(test_unique_lock) {
    mutex mtx;
    int value = 0;

    {
        unique_lock<mutex> lock(mtx);
        value = 100;
        lock.unlock();
        // Mutex is now unlocked
    }

    ASSERT_EQ(value, 100);
}

TEST(test_try_lock) {
    mutex mtx;
    ASSERT_TRUE(mtx.try_lock());
    mtx.unlock();
}

int main() {
    cout << "Running Mutex and Locks Tests\n==============================\n\n";
    RUN_TEST(test_mutex_basic);
    RUN_TEST(test_lock_guard);
    RUN_TEST(test_unique_lock);
    RUN_TEST(test_try_lock);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
