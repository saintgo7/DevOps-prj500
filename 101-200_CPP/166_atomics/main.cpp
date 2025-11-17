/*
 * Program 166: Atomic Operations - Lock-Free Programming
 *
 * This program demonstrates:
 * - Atomic types and operations
 * - Memory ordering models
 * - Compare-and-swap operations
 * - Lock-free data structures
 * - Atomic flags and fences
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <chrono>
#include <mutex>

std::mutex cout_mutex;

template<typename... Args>
void safe_print(Args&&... args) {
    std::lock_guard<std::mutex> lock(cout_mutex);
    (std::cout << ... << args) << std::endl;
}

// ==============================================
// 1. Basic Atomic Operations
// ==============================================

void basicAtomicDemo() {
    std::cout << "\n=== 1. Basic Atomic Operations ===\n";

    std::atomic<int> counter{0};

    auto increment = [&counter]() {
        for (int i = 0; i < 10000; ++i) {
            counter++; // Atomic increment
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back(increment);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Counter value: " << counter.load() << "\n";
    std::cout << "Expected: 50000\n";
    std::cout << "Atomic operations ensure correctness without locks!\n";
}

// ==============================================
// 2. Atomic Operations and Methods
// ==============================================

void atomicOperationsDemo() {
    std::cout << "\n=== 2. Atomic Operations and Methods ===\n";

    std::atomic<int> value{10};

    std::cout << "Initial value: " << value.load() << "\n";

    // Store
    value.store(20);
    std::cout << "After store(20): " << value.load() << "\n";

    // Exchange (returns old value)
    int old = value.exchange(30);
    std::cout << "exchange(30) returned: " << old << ", new value: " << value.load() << "\n";

    // Arithmetic operations
    value.fetch_add(5);
    std::cout << "After fetch_add(5): " << value.load() << "\n";

    value.fetch_sub(3);
    std::cout << "After fetch_sub(3): " << value.load() << "\n";

    // Bitwise operations
    std::atomic<unsigned int> bits{0b1010};
    bits.fetch_or(0b0101);
    std::cout << "After fetch_or: " << std::bitset<4>(bits.load()) << "\n";

    bits.fetch_and(0b1100);
    std::cout << "After fetch_and: " << std::bitset<4>(bits.load()) << "\n";
}

// ==============================================
// 3. Compare-And-Swap (CAS)
// ==============================================

void compareAndSwapDemo() {
    std::cout << "\n=== 3. Compare-And-Swap (CAS) ===\n";

    std::atomic<int> value{100};

    int expected = 100;
    int desired = 200;

    // Try to change value from 100 to 200
    if (value.compare_exchange_strong(expected, desired)) {
        std::cout << "CAS succeeded: value changed to " << value.load() << "\n";
    } else {
        std::cout << "CAS failed: expected was " << expected << "\n";
    }

    // Try to change from 100 (but value is now 200)
    expected = 100;
    desired = 300;

    if (value.compare_exchange_strong(expected, desired)) {
        std::cout << "CAS succeeded\n";
    } else {
        std::cout << "CAS failed: expected was 100, actual is " << expected << "\n";
    }
}

// ==============================================
// 4. Memory Ordering
// ==============================================

void memoryOrderingDemo() {
    std::cout << "\n=== 4. Memory Ordering Models ===\n";

    std::atomic<int> x{0}, y{0};
    std::atomic<int> r1{0}, r2{0};

    std::cout << "Memory ordering types:\n";
    std::cout << "- memory_order_relaxed: No synchronization\n";
    std::cout << "- memory_order_acquire: Load operation\n";
    std::cout << "- memory_order_release: Store operation\n";
    std::cout << "- memory_order_acq_rel: Both load and store\n";
    std::cout << "- memory_order_seq_cst: Sequential consistency (default)\n";

    // Example with relaxed ordering
    std::thread t1([&]() {
        x.store(1, std::memory_order_relaxed);
    });

    std::thread t2([&]() {
        y.store(1, std::memory_order_relaxed);
    });

    t1.join();
    t2.join();

    std::cout << "Relaxed ordering allows maximum performance\n";
    std::cout << "But provides no ordering guarantees across threads\n";
}

// ==============================================
// 5. Acquire-Release Semantics
// ==============================================

std::atomic<bool> ready{false};
std::atomic<int> data{0};

void producer_thread() {
    data.store(42, std::memory_order_relaxed);
    ready.store(true, std::memory_order_release); // Release: all writes visible
}

void consumer_thread() {
    while (!ready.load(std::memory_order_acquire)) { // Acquire: see all writes
        std::this_thread::yield();
    }
    safe_print("Consumer read data: ", data.load(std::memory_order_relaxed));
}

void acquireReleaseDemo() {
    std::cout << "\n=== 5. Acquire-Release Semantics ===\n";

    ready = false;
    data = 0;

    std::thread producer(producer_thread);
    std::thread consumer(consumer_thread);

    producer.join();
    consumer.join();

    std::cout << "Acquire-release ensures proper memory visibility\n";
}

// ==============================================
// 6. Atomic Flag - Lock-Free Spinlock
// ==============================================

class Spinlock {
private:
    std::atomic_flag flag = ATOMIC_FLAG_INIT;

public:
    void lock() {
        while (flag.test_and_set(std::memory_order_acquire)) {
            // Spin until flag is clear
            std::this_thread::yield();
        }
    }

    void unlock() {
        flag.clear(std::memory_order_release);
    }
};

void spinlockDemo() {
    std::cout << "\n=== 6. Spinlock with atomic_flag ===\n";

    Spinlock spinlock;
    int counter = 0;

    auto worker = [&]() {
        for (int i = 0; i < 1000; ++i) {
            spinlock.lock();
            ++counter;
            spinlock.unlock();
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back(worker);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Counter with spinlock: " << counter << "\n";
    std::cout << "Expected: 5000\n";
}

// ==============================================
// 7. Lock-Free Stack
// ==============================================

template<typename T>
class LockFreeStack {
private:
    struct Node {
        T data;
        Node* next;
        Node(const T& d) : data(d), next(nullptr) {}
    };

    std::atomic<Node*> head{nullptr};

public:
    ~LockFreeStack() {
        while (Node* node = head.load()) {
            head.store(node->next);
            delete node;
        }
    }

    void push(const T& data) {
        Node* new_node = new Node(data);
        new_node->next = head.load();

        // CAS loop: retry until successful
        while (!head.compare_exchange_weak(new_node->next, new_node)) {
            // If CAS fails, new_node->next is updated to current head
            // Loop retries with updated value
        }
    }

    bool pop(T& result) {
        Node* old_head = head.load();

        while (old_head && !head.compare_exchange_weak(old_head, old_head->next)) {
            // Retry if another thread modified head
        }

        if (old_head) {
            result = old_head->data;
            delete old_head;
            return true;
        }

        return false;
    }
};

void lockFreeStackDemo() {
    std::cout << "\n=== 7. Lock-Free Stack ===\n";

    LockFreeStack<int> stack;

    // Producer threads
    auto producer = [&](int id) {
        for (int i = 0; i < 100; ++i) {
            stack.push(id * 100 + i);
        }
    };

    // Consumer threads
    std::atomic<int> consumed{0};
    auto consumer = [&]() {
        int value;
        while (consumed.load() < 500) {
            if (stack.pop(value)) {
                consumed++;
            } else {
                std::this_thread::yield();
            }
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back(producer, i);
    }
    for (int i = 0; i < 3; ++i) {
        threads.emplace_back(consumer);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Items consumed: " << consumed.load() << "\n";
    std::cout << "Lock-free stack allows concurrent access without locks!\n";
}

// ==============================================
// 8. Atomic Smart Pointer (C++20)
// ==============================================

void atomicSharedPtrDemo() {
    std::cout << "\n=== 8. Atomic Shared Pointer ===\n";

    // C++20: std::atomic<std::shared_ptr<T>>
    std::atomic<std::shared_ptr<int>> atomic_ptr;

    atomic_ptr.store(std::make_shared<int>(42));

    std::thread t1([&]() {
        auto ptr = atomic_ptr.load();
        if (ptr) {
            safe_print("Thread 1 read: ", *ptr);
        }
    });

    std::thread t2([&]() {
        atomic_ptr.store(std::make_shared<int>(100));
        safe_print("Thread 2 updated pointer");
    });

    t1.join();
    t2.join();

    std::cout << "Final value: " << *atomic_ptr.load() << "\n";
}

// ==============================================
// 9. Wait and Notify (C++20)
// ==============================================

void atomicWaitNotifyDemo() {
    std::cout << "\n=== 9. Atomic Wait/Notify (C++20) ===\n";

    std::atomic<bool> flag{false};

    std::thread waiter([&]() {
        safe_print("Waiter: waiting for flag...");
        flag.wait(false); // Wait until flag != false
        safe_print("Waiter: flag is now true!");
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(500));

    safe_print("Main: setting flag to true");
    flag.store(true);
    flag.notify_one(); // Wake waiting thread

    waiter.join();

    std::cout << "atomic wait/notify provides efficient synchronization\n";
}

// ==============================================
// 10. Performance Comparison
// ==============================================

void performanceComparison() {
    std::cout << "\n=== 10. Performance Comparison ===\n";

    const int iterations = 1000000;

    // Mutex-based counter
    {
        std::mutex mtx;
        int counter = 0;

        auto start = std::chrono::high_resolution_clock::now();

        std::thread t1([&]() {
            for (int i = 0; i < iterations; ++i) {
                std::lock_guard<std::mutex> lock(mtx);
                ++counter;
            }
        });

        std::thread t2([&]() {
            for (int i = 0; i < iterations; ++i) {
                std::lock_guard<std::mutex> lock(mtx);
                ++counter;
            }
        });

        t1.join();
        t2.join();

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Mutex-based: " << duration.count() << "ms\n";
    }

    // Atomic counter
    {
        std::atomic<int> counter{0};

        auto start = std::chrono::high_resolution_clock::now();

        std::thread t1([&]() {
            for (int i = 0; i < iterations; ++i) {
                ++counter;
            }
        });

        std::thread t2([&]() {
            for (int i = 0; i < iterations; ++i) {
                ++counter;
            }
        });

        t1.join();
        t2.join();

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Atomic-based: " << duration.count() << "ms\n";
    }

    std::cout << "Atomics are typically faster than mutexes for simple operations\n";
}

int main() {
    std::cout << "=== C++ Atomic Operations and Lock-Free Programming ===\n";

    // 1. Basic atomics
    basicAtomicDemo();

    // 2. Atomic operations
    atomicOperationsDemo();

    // 3. Compare-and-swap
    compareAndSwapDemo();

    // 4. Memory ordering
    memoryOrderingDemo();

    // 5. Acquire-release
    acquireReleaseDemo();

    // 6. Spinlock
    spinlockDemo();

    // 7. Lock-free stack
    lockFreeStackDemo();

    // 8. Atomic shared_ptr
    atomicSharedPtrDemo();

    // 9. Wait/notify
    atomicWaitNotifyDemo();

    // 10. Performance
    performanceComparison();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. Atomic types provide lock-free synchronization\n";
    std::cout << "2. CAS (compare-and-swap) is fundamental to lock-free algorithms\n";
    std::cout << "3. Memory ordering controls visibility of operations\n";
    std::cout << "4. relaxed < acquire/release < seq_cst (performance vs guarantees)\n";
    std::cout << "5. atomic_flag is the only guaranteed lock-free atomic\n";
    std::cout << "6. Lock-free != wait-free (may still loop in CAS)\n";
    std::cout << "7. C++20 adds atomic wait/notify and atomic<shared_ptr>\n";

    return 0;
}
