/*
 * Test Suite for Program 168: Async and Future
 */

#include <iostream>
#include <future>
#include <thread>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

int compute(int x) {
    this_thread::sleep_for(chrono::milliseconds(10));
    return x * x;
}

TEST(test_async_basic) {
    future<int> result = async(launch::async, compute, 5);
    ASSERT_EQ(result.get(), 25);
}

TEST(test_multiple_async) {
    future<int> f1 = async(launch::async, compute, 3);
    future<int> f2 = async(launch::async, compute, 4);

    ASSERT_EQ(f1.get(), 9);
    ASSERT_EQ(f2.get(), 16);
}

TEST(test_promise_future) {
    promise<int> prom;
    future<int> fut = prom.get_future();

    thread t([&prom]() {
        this_thread::sleep_for(chrono::milliseconds(10));
        prom.set_value(42);
    });

    ASSERT_EQ(fut.get(), 42);
    t.join();
}

TEST(test_packaged_task) {
    packaged_task<int(int)> task(compute);
    future<int> result = task.get_future();

    thread t(move(task), 7);
    ASSERT_EQ(result.get(), 49);
    t.join();
}

TEST(test_future_wait) {
    future<int> result = async(launch::async, compute, 10);
    result.wait();
    ASSERT_EQ(result.get(), 100);
}

int main() {
    cout << "Running Async and Future Tests\n===============================\n\n";
    RUN_TEST(test_async_basic);
    RUN_TEST(test_multiple_async);
    RUN_TEST(test_promise_future);
    RUN_TEST(test_packaged_task);
    RUN_TEST(test_future_wait);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
