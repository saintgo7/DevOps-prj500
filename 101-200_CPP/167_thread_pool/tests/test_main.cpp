/*
 * Test Suite for Program 167: Thread Pool
 */

#include <iostream>
#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <atomic>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

class SimpleThreadPool {
private:
    vector<thread> workers;
    queue<function<void()>> tasks;
    mutex queue_mutex;
    condition_variable condition;
    bool stop = false;

public:
    SimpleThreadPool(size_t threads) {
        for(size_t i = 0; i < threads; ++i) {
            workers.emplace_back([this] {
                while(true) {
                    function<void()> task;
                    {
                        unique_lock<mutex> lock(this->queue_mutex);
                        this->condition.wait(lock, [this]{ return this->stop || !this->tasks.empty(); });
                        if(this->stop && this->tasks.empty())
                            return;
                        task = move(this->tasks.front());
                        this->tasks.pop();
                    }
                    task();
                }
            });
        }
    }

    template<class F>
    void enqueue(F&& f) {
        {
            unique_lock<mutex> lock(queue_mutex);
            tasks.emplace(forward<F>(f));
        }
        condition.notify_one();
    }

    ~SimpleThreadPool() {
        {
            unique_lock<mutex> lock(queue_mutex);
            stop = true;
        }
        condition.notify_all();
        for(thread &worker: workers)
            worker.join();
    }
};

TEST(test_basic_pool) {
    SimpleThreadPool pool(4);
    atomic<int> counter{0};

    for(int i = 0; i < 10; i++) {
        pool.enqueue([&counter]{ counter++; });
    }

    this_thread::sleep_for(chrono::milliseconds(100));
    ASSERT_EQ(counter.load(), 10);
}

TEST(test_pool_multiple_tasks) {
    SimpleThreadPool pool(2);
    atomic<int> sum{0};

    for(int i = 1; i <= 5; i++) {
        pool.enqueue([&sum, i]{ sum += i; });
    }

    this_thread::sleep_for(chrono::milliseconds(100));
    ASSERT_EQ(sum.load(), 15); // 1+2+3+4+5
}

int main() {
    cout << "Running Thread Pool Tests\n=========================\n\n";
    RUN_TEST(test_basic_pool);
    RUN_TEST(test_pool_multiple_tasks);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
