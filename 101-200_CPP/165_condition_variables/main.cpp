/*
 * Program 165: Condition Variables - Thread Synchronization and Signaling
 *
 * This program demonstrates:
 * - std::condition_variable for thread signaling
 * - wait(), notify_one(), notify_all()
 * - Producer-consumer pattern
 * - Spurious wakeups and predicate-based waiting
 * - Thread synchronization patterns
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <vector>
#include <chrono>
#include <string>

std::mutex cout_mutex;

template<typename... Args>
void safe_print(Args&&... args) {
    std::lock_guard<std::mutex> lock(cout_mutex);
    (std::cout << ... << args) << std::endl;
}

// ==============================================
// 1. Basic Condition Variable Usage
// ==============================================

std::mutex mtx;
std::condition_variable cv;
bool ready = false;

void worker_thread(int id) {
    std::unique_lock<std::mutex> lock(mtx);

    safe_print("Worker ", id, " waiting...");

    // Wait until ready becomes true
    cv.wait(lock, [] { return ready; });

    safe_print("Worker ", id, " proceeding!");
}

void basicConditionVariable() {
    std::cout << "\n=== 1. Basic Condition Variable ===\n";

    std::vector<std::thread> workers;

    // Create waiting threads
    for (int i = 1; i <= 3; ++i) {
        workers.emplace_back(worker_thread, i);
    }

    std::this_thread::sleep_for(std::chrono::milliseconds(500));

    // Signal all waiting threads
    {
        std::lock_guard<std::mutex> lock(mtx);
        ready = true;
        std::cout << "Main thread signaling all workers...\n";
    }
    cv.notify_all();

    for (auto& t : workers) {
        t.join();
    }

    ready = false; // Reset for next demo
}

// ==============================================
// 2. Producer-Consumer Pattern
// ==============================================

template<typename T>
class ThreadSafeQueue {
private:
    std::queue<T> queue;
    mutable std::mutex mtx;
    std::condition_variable cv;
    bool done = false;

public:
    void push(T value) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            queue.push(std::move(value));
        }
        cv.notify_one(); // Wake up one waiting consumer
    }

    bool pop(T& value) {
        std::unique_lock<std::mutex> lock(mtx);

        // Wait until queue is not empty or done
        cv.wait(lock, [this] { return !queue.empty() || done; });

        if (queue.empty()) {
            return false; // Done and queue is empty
        }

        value = std::move(queue.front());
        queue.pop();
        return true;
    }

    void finish() {
        {
            std::lock_guard<std::mutex> lock(mtx);
            done = true;
        }
        cv.notify_all(); // Wake all waiting consumers
    }

    size_t size() const {
        std::lock_guard<std::mutex> lock(mtx);
        return queue.size();
    }
};

void producer(ThreadSafeQueue<int>& queue, int id, int count) {
    for (int i = 0; i < count; ++i) {
        int value = id * 100 + i;
        queue.push(value);
        safe_print("Producer ", id, " produced: ", value);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
}

void consumer(ThreadSafeQueue<int>& queue, int id) {
    int value;
    while (queue.pop(value)) {
        safe_print("Consumer ", id, " consumed: ", value);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    safe_print("Consumer ", id, " finished");
}

void producerConsumerDemo() {
    std::cout << "\n=== 2. Producer-Consumer Pattern ===\n";

    ThreadSafeQueue<int> queue;

    // Create producers
    std::thread p1(producer, std::ref(queue), 1, 5);
    std::thread p2(producer, std::ref(queue), 2, 5);

    // Create consumers
    std::thread c1(consumer, std::ref(queue), 1);
    std::thread c2(consumer, std::ref(queue), 2);

    // Wait for producers to finish
    p1.join();
    p2.join();

    // Signal consumers to stop
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    queue.finish();

    // Wait for consumers to finish
    c1.join();
    c2.join();

    std::cout << "Producer-Consumer completed\n";
}

// ==============================================
// 3. Spurious Wakeups
// ==============================================

void spuriousWakeupDemo() {
    std::cout << "\n=== 3. Spurious Wakeups ===\n";

    std::mutex m;
    std::condition_variable cv;
    bool condition = false;
    int wakeup_count = 0;

    std::thread waiter([&]() {
        std::unique_lock<std::mutex> lock(m);

        // WRONG: Doesn't handle spurious wakeups
        // cv.wait(lock);

        // CORRECT: Use predicate to handle spurious wakeups
        cv.wait(lock, [&]() {
            ++wakeup_count;
            return condition;
        });

        safe_print("Waiter woke up after ", wakeup_count, " checks");
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    {
        std::lock_guard<std::mutex> lock(m);
        condition = true;
    }
    cv.notify_one();

    waiter.join();

    std::cout << "Always use predicate-based wait to handle spurious wakeups!\n";
}

// ==============================================
// 4. notify_one() vs notify_all()
// ==============================================

void notifyDemo() {
    std::cout << "\n=== 4. notify_one() vs notify_all() ===\n";

    std::mutex m;
    std::condition_variable cv;
    int ready_count = 0;

    auto waiter = [&](int id) {
        std::unique_lock<std::mutex> lock(m);
        cv.wait(lock, [&] { return ready_count > 0; });
        --ready_count;
        safe_print("Thread ", id, " woke up");
    };

    // Create waiting threads
    std::vector<std::thread> threads;
    for (int i = 1; i <= 3; ++i) {
        threads.emplace_back(waiter, i);
    }

    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    // Wake one thread at a time
    std::cout << "\nUsing notify_one():\n";
    for (int i = 0; i < 3; ++i) {
        {
            std::lock_guard<std::mutex> lock(m);
            ++ready_count;
        }
        cv.notify_one();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    for (auto& t : threads) {
        t.join();
    }
}

// ==============================================
// 5. Timed Waits
// ==============================================

void timedWaitDemo() {
    std::cout << "\n=== 5. Timed Waits ===\n";

    std::mutex m;
    std::condition_variable cv;
    bool ready = false;

    std::thread waiter([&]() {
        std::unique_lock<std::mutex> lock(m);

        // Wait for up to 500ms
        if (cv.wait_for(lock, std::chrono::milliseconds(500), [&] { return ready; })) {
            safe_print("Condition met before timeout");
        } else {
            safe_print("Timeout - condition not met");
        }
    });

    // Don't signal - let it timeout
    waiter.join();

    // Now try with signal
    std::thread waiter2([&]() {
        std::unique_lock<std::mutex> lock(m);

        if (cv.wait_for(lock, std::chrono::milliseconds(500), [&] { return ready; })) {
            safe_print("Condition met before timeout");
        } else {
            safe_print("Timeout - condition not met");
        }
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    {
        std::lock_guard<std::mutex> lock(m);
        ready = true;
    }
    cv.notify_one();

    waiter2.join();
}

// ==============================================
// 6. Barrier Pattern
// ==============================================

class Barrier {
private:
    std::mutex mtx;
    std::condition_variable cv;
    size_t count;
    size_t waiting = 0;
    size_t generation = 0;

public:
    explicit Barrier(size_t n) : count(n) {}

    void wait() {
        std::unique_lock<std::mutex> lock(mtx);
        size_t gen = generation;

        if (++waiting == count) {
            // Last thread arrives
            ++generation;
            waiting = 0;
            cv.notify_all();
        } else {
            // Wait for all threads
            cv.wait(lock, [this, gen] { return gen != generation; });
        }
    }
};

void barrierDemo() {
    std::cout << "\n=== 6. Barrier Pattern ===\n";

    const int num_threads = 4;
    Barrier barrier(num_threads);

    auto worker = [&](int id) {
        safe_print("Thread ", id, " phase 1");
        std::this_thread::sleep_for(std::chrono::milliseconds(id * 100));

        safe_print("Thread ", id, " waiting at barrier");
        barrier.wait(); // All threads wait here

        safe_print("Thread ", id, " phase 2 - after barrier");
    };

    std::vector<std::thread> threads;
    for (int i = 1; i <= num_threads; ++i) {
        threads.emplace_back(worker, i);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "All threads synchronized at barrier\n";
}

// ==============================================
// 7. Semaphore Simulation
// ==============================================

class Semaphore {
private:
    std::mutex mtx;
    std::condition_variable cv;
    int count;

public:
    explicit Semaphore(int initial) : count(initial) {}

    void acquire() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return count > 0; });
        --count;
    }

    void release() {
        {
            std::lock_guard<std::mutex> lock(mtx);
            ++count;
        }
        cv.notify_one();
    }
};

void semaphoreDemo() {
    std::cout << "\n=== 7. Semaphore Simulation ===\n";

    Semaphore sem(2); // Allow 2 concurrent accesses

    auto worker = [&](int id) {
        safe_print("Thread ", id, " trying to acquire...");
        sem.acquire();

        safe_print("Thread ", id, " acquired semaphore");
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        safe_print("Thread ", id, " releasing semaphore");

        sem.release();
    };

    std::vector<std::thread> threads;
    for (int i = 1; i <= 5; ++i) {
        threads.emplace_back(worker, i);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Semaphore limited concurrent access to 2 threads\n";
}

// ==============================================
// 8. Event Flag
// ==============================================

class EventFlag {
private:
    std::mutex mtx;
    std::condition_variable cv;
    bool flag = false;

public:
    void set() {
        {
            std::lock_guard<std::mutex> lock(mtx);
            flag = true;
        }
        cv.notify_all();
    }

    void wait() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return flag; });
    }

    void reset() {
        std::lock_guard<std::mutex> lock(mtx);
        flag = false;
    }
};

void eventFlagDemo() {
    std::cout << "\n=== 8. Event Flag ===\n";

    EventFlag event;

    std::thread t1([&]() {
        safe_print("Thread 1 waiting for event...");
        event.wait();
        safe_print("Thread 1 received event!");
    });

    std::thread t2([&]() {
        safe_print("Thread 2 waiting for event...");
        event.wait();
        safe_print("Thread 2 received event!");
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    std::cout << "Setting event flag...\n";
    event.set();

    t1.join();
    t2.join();
}

int main() {
    std::cout << "=== C++ Condition Variables ===\n";

    // 1. Basic condition variable
    basicConditionVariable();

    // 2. Producer-consumer
    producerConsumerDemo();

    // 3. Spurious wakeups
    spuriousWakeupDemo();

    // 4. notify_one vs notify_all
    notifyDemo();

    // 5. Timed waits
    timedWaitDemo();

    // 6. Barrier pattern
    barrierDemo();

    // 7. Semaphore simulation
    semaphoreDemo();

    // 8. Event flag
    eventFlagDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. Condition variables coordinate threads through signaling\n";
    std::cout << "2. Always use unique_lock with condition variables\n";
    std::cout << "3. Use predicate-based wait to handle spurious wakeups\n";
    std::cout << "4. notify_one() wakes one thread, notify_all() wakes all\n";
    std::cout << "5. wait_for() and wait_until() provide timeout support\n";
    std::cout << "6. Producer-consumer is the classic use case\n";

    return 0;
}
