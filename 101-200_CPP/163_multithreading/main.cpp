/*
 * Program 163: Multithreading - std::thread, Thread Management, Thread Safety
 *
 * This program demonstrates:
 * - Creating and managing threads with std::thread
 * - Thread lifecycle and joining/detaching
 * - Passing arguments to threads
 * - Thread safety and race conditions
 * - Thread identification
 */

#include <iostream>
#include <thread>
#include <vector>
#include <string>
#include <chrono>
#include <mutex>
#include <atomic>
#include <functional>

// Mutex for thread-safe console output
std::mutex cout_mutex;

// Thread-safe print function
template<typename... Args>
void thread_safe_print(Args&&... args) {
    std::lock_guard<std::mutex> lock(cout_mutex);
    (std::cout << ... << args) << std::endl;
}

// ==============================================
// 1. Basic Thread Creation
// ==============================================

void simpleFunction() {
    thread_safe_print("Hello from simple function in thread ",
                     std::this_thread::get_id());
}

void functionWithArgs(const std::string& name, int count) {
    for (int i = 0; i < count; ++i) {
        thread_safe_print("Thread ", name, " iteration ", i);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

void basicThreadCreation() {
    std::cout << "\n=== 1. Basic Thread Creation ===\n";

    // Create thread with function
    std::thread t1(simpleFunction);

    // Create thread with function and arguments
    std::thread t2(functionWithArgs, "Worker", 3);

    // Create thread with lambda
    std::thread t3([]() {
        thread_safe_print("Hello from lambda in thread ",
                         std::this_thread::get_id());
    });

    // Must join or detach before thread object is destroyed
    t1.join();
    t2.join();
    t3.join();

    std::cout << "All basic threads completed\n";
}

// ==============================================
// 2. Thread Lifecycle - Join vs Detach
// ==============================================

void threadLifecycle() {
    std::cout << "\n=== 2. Thread Lifecycle - Join vs Detach ===\n";

    // Join: Wait for thread to complete
    std::thread t1([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        thread_safe_print("Joined thread completed");
    });

    std::cout << "Waiting for joined thread...\n";
    t1.join(); // Blocks until t1 finishes
    std::cout << "Joined thread finished\n";

    // Detach: Thread runs independently
    std::thread t2([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        thread_safe_print("Detached thread running independently");
    });

    if (t2.joinable()) {
        std::cout << "Detaching thread...\n";
        t2.detach(); // Thread runs in background
    }

    // Note: Detached thread may not complete before main ends
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    std::cout << "Detach example completed\n";
}

// ==============================================
// 3. Passing Arguments to Threads
// ==============================================

void modifyValue(int& value) {
    value += 10;
    thread_safe_print("Modified value to: ", value);
}

void passingArguments() {
    std::cout << "\n=== 3. Passing Arguments to Threads ===\n";

    int value = 5;

    // Pass by value (copy)
    std::thread t1([](int val) {
        thread_safe_print("Value (copy): ", val);
    }, value);

    // Pass by reference using std::ref
    std::thread t2(modifyValue, std::ref(value));

    // Move semantics
    std::string str = "Move me";
    std::thread t3([](std::string s) {
        thread_safe_print("Moved string: ", s);
    }, std::move(str));

    t1.join();
    t2.join();
    t3.join();

    std::cout << "Final value: " << value << "\n";
    std::cout << "Original string after move: '" << str << "'\n";
}

// ==============================================
// 4. Class Member Functions as Threads
// ==============================================

class Worker {
private:
    std::string name;
    int task_count;

public:
    Worker(const std::string& n) : name(n), task_count(0) {}

    void doWork(int iterations) {
        for (int i = 0; i < iterations; ++i) {
            thread_safe_print("Worker ", name, " - task ", ++task_count);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }

    int getTaskCount() const { return task_count; }
};

void memberFunctionThreads() {
    std::cout << "\n=== 4. Member Function Threads ===\n";

    Worker worker("Alice");

    // Thread with member function: &Class::method, object, args
    std::thread t(&Worker::doWork, &worker, 3);

    t.join();
    std::cout << "Total tasks completed: " << worker.getTaskCount() << "\n";
}

// ==============================================
// 5. Thread Pool Pattern (Simple)
// ==============================================

void workerThread(int id, int tasks) {
    for (int i = 0; i < tasks; ++i) {
        thread_safe_print("Worker ", id, " executing task ", i);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
}

void simpleThreadPool() {
    std::cout << "\n=== 5. Simple Thread Pool ===\n";

    const int num_threads = 4;
    std::vector<std::thread> thread_pool;

    // Create thread pool
    for (int i = 0; i < num_threads; ++i) {
        thread_pool.emplace_back(workerThread, i, 3);
    }

    // Join all threads
    for (auto& t : thread_pool) {
        if (t.joinable()) {
            t.join();
        }
    }

    std::cout << "Thread pool completed\n";
}

// ==============================================
// 6. Race Conditions (Unsafe)
// ==============================================

int unsafe_counter = 0;

void unsafeIncrement(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        ++unsafe_counter; // Race condition!
    }
}

void raceConditionDemo() {
    std::cout << "\n=== 6. Race Condition Demo (Unsafe) ===\n";

    unsafe_counter = 0;
    const int iterations = 10000;

    std::thread t1(unsafeIncrement, iterations);
    std::thread t2(unsafeIncrement, iterations);
    std::thread t3(unsafeIncrement, iterations);

    t1.join();
    t2.join();
    t3.join();

    std::cout << "Expected: " << (iterations * 3) << "\n";
    std::cout << "Actual: " << unsafe_counter << "\n";
    std::cout << "Data race caused incorrect result!\n";
}

// ==============================================
// 7. Thread-Safe Counter with Mutex
// ==============================================

class SafeCounter {
private:
    int count;
    mutable std::mutex mutex;

public:
    SafeCounter() : count(0) {}

    void increment() {
        std::lock_guard<std::mutex> lock(mutex);
        ++count;
    }

    int get() const {
        std::lock_guard<std::mutex> lock(mutex);
        return count;
    }
};

void safeIncrement(SafeCounter& counter, int iterations) {
    for (int i = 0; i < iterations; ++i) {
        counter.increment();
    }
}

void threadSafeDemo() {
    std::cout << "\n=== 7. Thread-Safe Counter ===\n";

    SafeCounter counter;
    const int iterations = 10000;

    std::thread t1(safeIncrement, std::ref(counter), iterations);
    std::thread t2(safeIncrement, std::ref(counter), iterations);
    std::thread t3(safeIncrement, std::ref(counter), iterations);

    t1.join();
    t2.join();
    t3.join();

    std::cout << "Expected: " << (iterations * 3) << "\n";
    std::cout << "Actual: " << counter.get() << "\n";
    std::cout << "Mutex ensured correct result!\n";
}

// ==============================================
// 8. Atomic Operations
// ==============================================

std::atomic<int> atomic_counter{0};

void atomicIncrement(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        ++atomic_counter; // Atomic operation, no mutex needed
    }
}

void atomicDemo() {
    std::cout << "\n=== 8. Atomic Operations ===\n";

    atomic_counter = 0;
    const int iterations = 10000;

    std::thread t1(atomicIncrement, iterations);
    std::thread t2(atomicIncrement, iterations);
    std::thread t3(atomicIncrement, iterations);

    t1.join();
    t2.join();
    t3.join();

    std::cout << "Expected: " << (iterations * 3) << "\n";
    std::cout << "Actual: " << atomic_counter.load() << "\n";
    std::cout << "Atomic operations ensured correctness!\n";
}

// ==============================================
// 9. Thread Hardware Information
// ==============================================

void threadHardwareInfo() {
    std::cout << "\n=== 9. Thread Hardware Information ===\n";

    unsigned int num_cores = std::thread::hardware_concurrency();
    std::cout << "Hardware concurrency: " << num_cores << " threads\n";
    std::cout << "Main thread ID: " << std::this_thread::get_id() << "\n";

    std::thread t([]() {
        thread_safe_print("Worker thread ID: ", std::this_thread::get_id());
    });

    t.join();
}

// ==============================================
// 10. RAII Thread Wrapper
// ==============================================

class ThreadGuard {
private:
    std::thread& t;

public:
    explicit ThreadGuard(std::thread& thread) : t(thread) {}

    ~ThreadGuard() {
        if (t.joinable()) {
            t.join(); // Automatically join on destruction
        }
    }

    ThreadGuard(const ThreadGuard&) = delete;
    ThreadGuard& operator=(const ThreadGuard&) = delete;
};

void raiiThreadDemo() {
    std::cout << "\n=== 10. RAII Thread Wrapper ===\n";

    std::thread t([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        thread_safe_print("RAII thread completed");
    });

    ThreadGuard guard(t); // Automatically joins in destructor

    std::cout << "ThreadGuard will auto-join on scope exit\n";
    // No explicit join needed - guard destructor handles it
}

int main() {
    std::cout << "=== C++ Multithreading with std::thread ===\n";

    // 1. Basic thread creation
    basicThreadCreation();

    // 2. Thread lifecycle
    threadLifecycle();

    // 3. Passing arguments
    passingArguments();

    // 4. Member function threads
    memberFunctionThreads();

    // 5. Simple thread pool
    simpleThreadPool();

    // 6. Race condition demo
    raceConditionDemo();

    // 7. Thread-safe operations
    threadSafeDemo();

    // 8. Atomic operations
    atomicDemo();

    // 9. Hardware info
    threadHardwareInfo();

    // 10. RAII thread wrapper
    raiiThreadDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. Always join() or detach() threads before destruction\n";
    std::cout << "2. Use std::ref() to pass references to threads\n";
    std::cout << "3. Race conditions occur without synchronization\n";
    std::cout << "4. Use mutex or atomic for thread safety\n";
    std::cout << "5. hardware_concurrency() shows available parallelism\n";
    std::cout << "6. RAII wrappers ensure proper thread cleanup\n";

    return 0;
}
