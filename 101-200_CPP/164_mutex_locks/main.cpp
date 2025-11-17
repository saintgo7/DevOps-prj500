/*
 * Program 164: Mutex and Locks - Synchronization Primitives
 *
 * This program demonstrates:
 * - std::mutex for mutual exclusion
 * - std::lock_guard for RAII locking
 * - std::unique_lock for flexible locking
 * - std::scoped_lock for deadlock prevention (C++17)
 * - std::recursive_mutex and std::timed_mutex
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <shared_mutex>
#include <vector>
#include <chrono>
#include <string>

// Global mutex for thread-safe output
std::mutex cout_mutex;

template<typename... Args>
void safe_print(Args&&... args) {
    std::lock_guard<std::mutex> lock(cout_mutex);
    (std::cout << ... << args) << std::endl;
}

// ==============================================
// 1. Basic Mutex Usage
// ==============================================

class Counter {
private:
    int value;
    std::mutex mtx;

public:
    Counter() : value(0) {}

    void increment() {
        mtx.lock();
        ++value;
        mtx.unlock();
    }

    // Dangerous: exception between lock/unlock causes deadlock
    void increment_unsafe() {
        mtx.lock();
        // If exception thrown here, mutex never unlocked!
        ++value;
        mtx.unlock();
    }

    int get() {
        mtx.lock();
        int result = value;
        mtx.unlock();
        return result;
    }
};

void basicMutexDemo() {
    std::cout << "\n=== 1. Basic Mutex Usage ===\n";

    Counter counter;
    std::vector<std::thread> threads;

    for (int i = 0; i < 5; ++i) {
        threads.emplace_back([&counter]() {
            for (int j = 0; j < 1000; ++j) {
                counter.increment();
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Final counter value: " << counter.get() << "\n";
    std::cout << "Expected: 5000\n";
}

// ==============================================
// 2. std::lock_guard - RAII Locking
// ==============================================

class SafeCounter {
private:
    int value;
    mutable std::mutex mtx;

public:
    SafeCounter() : value(0) {}

    void increment() {
        std::lock_guard<std::mutex> lock(mtx); // RAII: auto-unlock on scope exit
        ++value;
    } // Mutex automatically unlocked here

    void add(int n) {
        std::lock_guard<std::mutex> lock(mtx);
        value += n;
        // Even if exception thrown, mutex is unlocked
    }

    int get() const {
        std::lock_guard<std::mutex> lock(mtx);
        return value;
    }
};

void lockGuardDemo() {
    std::cout << "\n=== 2. std::lock_guard Demo ===\n";

    SafeCounter counter;
    std::vector<std::thread> threads;

    for (int i = 0; i < 5; ++i) {
        threads.emplace_back([&counter]() {
            for (int j = 0; j < 1000; ++j) {
                counter.increment();
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Final value with lock_guard: " << counter.get() << "\n";
    std::cout << "lock_guard provides exception safety!\n";
}

// ==============================================
// 3. std::unique_lock - Flexible Locking
// ==============================================

class FlexibleCounter {
private:
    int value;
    mutable std::mutex mtx;

public:
    FlexibleCounter() : value(0) {}

    void increment() {
        std::unique_lock<std::mutex> lock(mtx);
        ++value;
    }

    void conditionalIncrement(bool condition) {
        std::unique_lock<std::mutex> lock(mtx);

        if (condition) {
            ++value;
        } else {
            lock.unlock(); // Can manually unlock early
            // Do work without holding lock
            std::this_thread::sleep_for(std::chrono::microseconds(1));
            lock.lock(); // Can re-lock
            ++value;
        }
    }

    // Deferred locking
    void deferredLock() {
        std::unique_lock<std::mutex> lock(mtx, std::defer_lock); // Don't lock yet

        // Do some work without lock
        // ...

        lock.lock(); // Lock when needed
        ++value;
    }

    int get() const {
        std::unique_lock<std::mutex> lock(mtx);
        return value;
    }
};

void uniqueLockDemo() {
    std::cout << "\n=== 3. std::unique_lock Demo ===\n";

    FlexibleCounter counter;

    std::thread t1([&]() {
        for (int i = 0; i < 100; ++i) {
            counter.conditionalIncrement(i % 2 == 0);
        }
    });

    std::thread t2([&]() {
        for (int i = 0; i < 100; ++i) {
            counter.deferredLock();
        }
    });

    t1.join();
    t2.join();

    std::cout << "Final value: " << counter.get() << "\n";
    std::cout << "unique_lock allows manual lock/unlock control\n";
}

// ==============================================
// 4. Deadlock Problem
// ==============================================

class BankAccount {
private:
    std::string name;
    int balance;
    std::mutex mtx;

public:
    BankAccount(const std::string& n, int bal) : name(n), balance(bal) {}

    // DANGEROUS: Can cause deadlock!
    void transfer_unsafe(BankAccount& to, int amount) {
        mtx.lock();
        std::this_thread::sleep_for(std::chrono::milliseconds(1)); // Simulate work
        to.mtx.lock(); // Potential deadlock here!

        balance -= amount;
        to.balance += amount;

        to.mtx.unlock();
        mtx.unlock();
    }

    // SAFE: Using std::lock to avoid deadlock
    void transfer_safe(BankAccount& to, int amount) {
        // Lock both mutexes without deadlock
        std::lock(mtx, to.mtx);

        // Adopt the locks
        std::lock_guard<std::mutex> lock1(mtx, std::adopt_lock);
        std::lock_guard<std::mutex> lock2(to.mtx, std::adopt_lock);

        balance -= amount;
        to.balance += amount;
    }

    int getBalance() {
        std::lock_guard<std::mutex> lock(mtx);
        return balance;
    }

    const std::string& getName() const { return name; }
};

void deadlockDemo() {
    std::cout << "\n=== 4. Deadlock Prevention ===\n";

    BankAccount acc1("Account1", 1000);
    BankAccount acc2("Account2", 1000);

    // Safe transfer using std::lock
    std::thread t1([&]() {
        for (int i = 0; i < 100; ++i) {
            acc1.transfer_safe(acc2, 10);
        }
    });

    std::thread t2([&]() {
        for (int i = 0; i < 100; ++i) {
            acc2.transfer_safe(acc1, 10);
        }
    });

    t1.join();
    t2.join();

    std::cout << acc1.getName() << " balance: " << acc1.getBalance() << "\n";
    std::cout << acc2.getName() << " balance: " << acc2.getBalance() << "\n";
    std::cout << "Total: " << (acc1.getBalance() + acc2.getBalance()) << "\n";
}

// ==============================================
// 5. std::scoped_lock (C++17) - Best Practice
// ==============================================

class ModernBankAccount {
private:
    std::string name;
    int balance;
    std::mutex mtx;

public:
    ModernBankAccount(const std::string& n, int bal) : name(n), balance(bal) {}

    // C++17: scoped_lock - simpler and safer
    void transfer(ModernBankAccount& to, int amount) {
        std::scoped_lock lock(mtx, to.mtx); // Locks all mutexes, deadlock-free!

        balance -= amount;
        to.balance += amount;
    }

    int getBalance() {
        std::scoped_lock lock(mtx);
        return balance;
    }

    const std::string& getName() const { return name; }
};

void scopedLockDemo() {
    std::cout << "\n=== 5. std::scoped_lock Demo (C++17) ===\n";

    ModernBankAccount acc1("Modern1", 1000);
    ModernBankAccount acc2("Modern2", 1000);

    std::thread t1([&]() {
        for (int i = 0; i < 100; ++i) {
            acc1.transfer(acc2, 10);
        }
    });

    std::thread t2([&]() {
        for (int i = 0; i < 100; ++i) {
            acc2.transfer(acc1, 10);
        }
    });

    t1.join();
    t2.join();

    std::cout << acc1.getName() << " balance: " << acc1.getBalance() << "\n";
    std::cout << acc2.getName() << " balance: " << acc2.getBalance() << "\n";
    std::cout << "scoped_lock is the modern C++17 way!\n";
}

// ==============================================
// 6. std::recursive_mutex
// ==============================================

class RecursiveCounter {
private:
    int value;
    std::recursive_mutex mtx; // Can be locked multiple times by same thread

public:
    RecursiveCounter() : value(0) {}

    void increment() {
        std::lock_guard<std::recursive_mutex> lock(mtx);
        ++value;
    }

    void incrementTwice() {
        std::lock_guard<std::recursive_mutex> lock(mtx);
        increment(); // Would deadlock with regular mutex!
        increment();
    }

    int get() {
        std::lock_guard<std::recursive_mutex> lock(mtx);
        return value;
    }
};

void recursiveMutexDemo() {
    std::cout << "\n=== 6. std::recursive_mutex Demo ===\n";

    RecursiveCounter counter;

    counter.increment();
    counter.incrementTwice(); // Recursive locking works!

    std::cout << "Value: " << counter.get() << "\n";
    std::cout << "recursive_mutex allows same thread to lock multiple times\n";
}

// ==============================================
// 7. std::timed_mutex
// ==============================================

class TimedResource {
private:
    std::timed_mutex mtx;
    int value;

public:
    TimedResource() : value(0) {}

    bool try_increment_for(std::chrono::milliseconds timeout) {
        if (mtx.try_lock_for(timeout)) {
            ++value;
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            mtx.unlock();
            return true;
        }
        return false;
    }

    bool try_increment_until(std::chrono::steady_clock::time_point deadline) {
        if (mtx.try_lock_until(deadline)) {
            ++value;
            mtx.unlock();
            return true;
        }
        return false;
    }

    int get() {
        std::lock_guard<std::timed_mutex> lock(mtx);
        return value;
    }
};

void timedMutexDemo() {
    std::cout << "\n=== 7. std::timed_mutex Demo ===\n";

    TimedResource resource;

    std::thread t1([&]() {
        for (int i = 0; i < 5; ++i) {
            if (resource.try_increment_for(std::chrono::milliseconds(50))) {
                safe_print("Thread 1: Successfully acquired lock");
            } else {
                safe_print("Thread 1: Timeout!");
            }
        }
    });

    std::thread t2([&]() {
        for (int i = 0; i < 5; ++i) {
            if (resource.try_increment_for(std::chrono::milliseconds(50))) {
                safe_print("Thread 2: Successfully acquired lock");
            } else {
                safe_print("Thread 2: Timeout!");
            }
        }
    });

    t1.join();
    t2.join();

    std::cout << "Final value: " << resource.get() << "\n";
}

// ==============================================
// 8. std::shared_mutex (C++17) - Reader-Writer Lock
// ==============================================

class SharedData {
private:
    int value;
    mutable std::shared_mutex mtx;

public:
    SharedData() : value(0) {}

    // Multiple readers can access simultaneously
    int read() const {
        std::shared_lock<std::shared_mutex> lock(mtx);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        return value;
    }

    // Only one writer can access
    void write(int new_value) {
        std::unique_lock<std::shared_mutex> lock(mtx);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        value = new_value;
    }
};

void sharedMutexDemo() {
    std::cout << "\n=== 8. std::shared_mutex Demo ===\n";

    SharedData data;
    data.write(42);

    // Multiple readers
    std::thread r1([&]() {
        for (int i = 0; i < 3; ++i) {
            int val = data.read();
            safe_print("Reader 1: ", val);
        }
    });

    std::thread r2([&]() {
        for (int i = 0; i < 3; ++i) {
            int val = data.read();
            safe_print("Reader 2: ", val);
        }
    });

    // Single writer
    std::thread w([&]() {
        for (int i = 1; i <= 3; ++i) {
            data.write(i * 10);
            safe_print("Writer: wrote ", i * 10);
        }
    });

    r1.join();
    r2.join();
    w.join();

    std::cout << "shared_mutex allows multiple readers or single writer\n";
}

int main() {
    std::cout << "=== C++ Mutex and Locks ===\n";

    // 1. Basic mutex
    basicMutexDemo();

    // 2. lock_guard
    lockGuardDemo();

    // 3. unique_lock
    uniqueLockDemo();

    // 4. Deadlock prevention
    deadlockDemo();

    // 5. scoped_lock (C++17)
    scopedLockDemo();

    // 6. recursive_mutex
    recursiveMutexDemo();

    // 7. timed_mutex
    timedMutexDemo();

    // 8. shared_mutex
    sharedMutexDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. Always use RAII locks (lock_guard, unique_lock, scoped_lock)\n";
    std::cout << "2. lock_guard: Simple, non-movable, always locked\n";
    std::cout << "3. unique_lock: Flexible, movable, can unlock/relock\n";
    std::cout << "4. scoped_lock (C++17): Best for multiple mutexes, deadlock-free\n";
    std::cout << "5. recursive_mutex: For recursive locking (use sparingly)\n";
    std::cout << "6. timed_mutex: Try to acquire with timeout\n";
    std::cout << "7. shared_mutex: Reader-writer lock for read-heavy workloads\n";

    return 0;
}
