/*
 * Test Suite for Program 166: Atomics
 */

#include <iostream>
#include <thread>
#include <atomic>
#include <vector>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_atomic_int) {
    atomic<int> counter{0};
    vector<thread> threads;

    for (int i = 0; i < 100; i++) {
        threads.emplace_back([&counter]() {
            counter++;
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    ASSERT_EQ(counter.load(), 100);
}

TEST(test_atomic_bool) {
    atomic<bool> flag{false};
    flag.store(true);
    ASSERT_EQ(flag.load(), true);
}

TEST(test_atomic_exchange) {
    atomic<int> val{10};
    int old = val.exchange(20);
    ASSERT_EQ(old, 10);
    ASSERT_EQ(val.load(), 20);
}

TEST(test_atomic_compare_exchange) {
    atomic<int> val{100};
    int expected = 100;
    bool result = val.compare_exchange_strong(expected, 200);
    ASSERT_TRUE(result);
    ASSERT_EQ(val.load(), 200);
}

TEST(test_atomic_fetch_add) {
    atomic<int> val{10};
    int old = val.fetch_add(5);
    ASSERT_EQ(old, 10);
    ASSERT_EQ(val.load(), 15);
}

int main() {
    cout << "Running Atomics Tests\n=====================\n\n";
    RUN_TEST(test_atomic_int);
    RUN_TEST(test_atomic_bool);
    RUN_TEST(test_atomic_exchange);
    RUN_TEST(test_atomic_compare_exchange);
    RUN_TEST(test_atomic_fetch_add);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
