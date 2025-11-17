/*
 * Test Suite for Program 165: Condition Variables
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_notify_one) {
    mutex mtx;
    condition_variable cv;
    bool ready = false;
    int value = 0;

    thread worker([&]() {
        unique_lock<mutex> lock(mtx);
        cv.wait(lock, [&]{ return ready; });
        value = 42;
    });

    this_thread::sleep_for(chrono::milliseconds(10));
    {
        lock_guard<mutex> lock(mtx);
        ready = true;
    }
    cv.notify_one();

    worker.join();
    ASSERT_EQ(value, 42);
}

TEST(test_notify_all) {
    mutex mtx;
    condition_variable cv;
    bool ready = false;
    int counter = 0;

    vector<thread> threads;
    for (int i = 0; i < 5; i++) {
        threads.emplace_back([&]() {
            unique_lock<mutex> lock(mtx);
            cv.wait(lock, [&]{ return ready; });
            counter++;
        });
    }

    this_thread::sleep_for(chrono::milliseconds(10));
    {
        lock_guard<mutex> lock(mtx);
        ready = true;
    }
    cv.notify_all();

    for (auto& t : threads) {
        t.join();
    }

    ASSERT_EQ(counter, 5);
}

TEST(test_wait_for_timeout) {
    mutex mtx;
    condition_variable cv;
    bool ready = false;

    unique_lock<mutex> lock(mtx);
    bool result = cv.wait_for(lock, chrono::milliseconds(10), [&]{ return ready; });

    ASSERT_EQ(result, false); // Timeout occurred
}

int main() {
    cout << "Running Condition Variables Tests\n==================================\n\n";
    RUN_TEST(test_notify_one);
    RUN_TEST(test_notify_all);
    RUN_TEST(test_wait_for_timeout);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
