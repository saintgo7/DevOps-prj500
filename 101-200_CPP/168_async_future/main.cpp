/*
 * Program 168: Async, Future, Promise, and Packaged Task
 *
 * This program demonstrates:
 * - std::async for asynchronous task execution
 * - std::future for retrieving results
 * - std::promise for setting values
 * - std::packaged_task for wrapping callable objects
 * - Launch policies and async patterns
 */

#include <iostream>
#include <future>
#include <thread>
#include <chrono>
#include <vector>
#include <numeric>
#include <stdexcept>
#include <functional>

// ==============================================
// 1. Basic std::async and std::future
// ==============================================

int computeValue(int x) {
    std::cout << "Computing value for " << x << " on thread "
              << std::this_thread::get_id() << "\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    return x * x;
}

void basicAsyncDemo() {
    std::cout << "\n=== 1. Basic async and future ===\n";
    std::cout << "Main thread: " << std::this_thread::get_id() << "\n";

    // Launch async task
    std::future<int> result = std::async(computeValue, 10);

    std::cout << "Main thread doing other work...\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    // Get result (blocks until ready)
    std::cout << "Getting result...\n";
    int value = result.get();
    std::cout << "Result: " << value << "\n";
}

// ==============================================
// 2. Launch Policies
// ==============================================

void launchPoliciesDemo() {
    std::cout << "\n=== 2. Launch Policies ===\n";
    std::cout << "Main thread: " << std::this_thread::get_id() << "\n";

    // std::launch::async - guaranteed to run asynchronously
    auto future1 = std::async(std::launch::async, []() {
        std::cout << "async policy - thread: " << std::this_thread::get_id() << "\n";
        return 42;
    });

    // std::launch::deferred - lazy evaluation (runs when get() is called)
    auto future2 = std::async(std::launch::deferred, []() {
        std::cout << "deferred policy - thread: " << std::this_thread::get_id() << "\n";
        return 100;
    });

    // Default: async | deferred (implementation chooses)
    auto future3 = std::async([]() {
        std::cout << "default policy - thread: " << std::this_thread::get_id() << "\n";
        return 200;
    });

    std::cout << "\nCalling get() on futures...\n";
    std::cout << "Future1: " << future1.get() << "\n";
    std::cout << "Future2: " << future2.get() << " (runs now, on main thread)\n";
    std::cout << "Future3: " << future3.get() << "\n";
}

// ==============================================
// 3. Multiple Async Tasks
// ==============================================

int parallelSum(const std::vector<int>& data, size_t start, size_t end) {
    return std::accumulate(data.begin() + start, data.begin() + end, 0);
}

void multipleAsyncDemo() {
    std::cout << "\n=== 3. Multiple Async Tasks ===\n";

    std::vector<int> data(10000, 1);

    // Split work across multiple async tasks
    auto future1 = std::async(std::launch::async, parallelSum, std::cref(data), 0, 2500);
    auto future2 = std::async(std::launch::async, parallelSum, std::cref(data), 2500, 5000);
    auto future3 = std::async(std::launch::async, parallelSum, std::cref(data), 5000, 7500);
    auto future4 = std::async(std::launch::async, parallelSum, std::cref(data), 7500, 10000);

    // Collect results
    int total = future1.get() + future2.get() + future3.get() + future4.get();

    std::cout << "Parallel sum: " << total << "\n";
    std::cout << "Expected: " << data.size() << "\n";
}

// ==============================================
// 4. std::promise - Manual Result Setting
// ==============================================

void promiseDemo() {
    std::cout << "\n=== 4. std::promise ===\n";

    std::promise<int> promise;
    std::future<int> future = promise.get_future();

    // Thread that sets the promise value
    std::thread worker([&promise]() {
        std::cout << "Worker: Computing value...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Set the value
        promise.set_value(42);
        std::cout << "Worker: Value set\n";
    });

    std::cout << "Main: Waiting for result...\n";
    int result = future.get();
    std::cout << "Main: Got result: " << result << "\n";

    worker.join();
}

// ==============================================
// 5. Promise with Exception
// ==============================================

void promiseExceptionDemo() {
    std::cout << "\n=== 5. Promise with Exception ===\n";

    std::promise<int> promise;
    std::future<int> future = promise.get_future();

    std::thread worker([&promise]() {
        try {
            std::cout << "Worker: Simulating error...\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(300));

            throw std::runtime_error("Something went wrong!");
        } catch (...) {
            // Set exception instead of value
            promise.set_exception(std::current_exception());
        }
    });

    try {
        std::cout << "Main: Waiting for result...\n";
        int result = future.get();
        std::cout << "Main: Got result: " << result << "\n";
    } catch (const std::exception& e) {
        std::cout << "Main: Caught exception: " << e.what() << "\n";
    }

    worker.join();
}

// ==============================================
// 6. std::packaged_task
// ==============================================

int multiply(int a, int b) {
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    return a * b;
}

void packagedTaskDemo() {
    std::cout << "\n=== 6. std::packaged_task ===\n";

    // Create packaged task
    std::packaged_task<int(int, int)> task(multiply);

    // Get future before moving task
    std::future<int> result = task.get_future();

    // Run task in another thread
    std::thread worker(std::move(task), 6, 7);

    std::cout << "Main: Waiting for result...\n";
    std::cout << "Result: " << result.get() << "\n";

    worker.join();
}

// ==============================================
// 7. Future States and wait()
// ==============================================

void futureStatesDemo() {
    std::cout << "\n=== 7. Future States ===\n";

    auto future = std::async(std::launch::async, []() {
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        return 42;
    });

    // Check if result is ready
    std::cout << "Checking future status...\n";

    for (int i = 0; i < 5; ++i) {
        auto status = future.wait_for(std::chrono::milliseconds(100));

        if (status == std::future_status::ready) {
            std::cout << "Future is ready!\n";
            break;
        } else if (status == std::future_status::timeout) {
            std::cout << "Still waiting... (" << (i + 1) << ")\n";
        } else if (status == std::future_status::deferred) {
            std::cout << "Deferred execution\n";
        }
    }

    std::cout << "Result: " << future.get() << "\n";
}

// ==============================================
// 8. std::shared_future
// ==============================================

void sharedFutureDemo() {
    std::cout << "\n=== 8. std::shared_future ===\n";

    std::promise<int> promise;
    std::shared_future<int> shared = promise.get_future().share();

    // Multiple threads can wait on shared_future
    auto waiter = [](std::shared_future<int> future, int id) {
        std::cout << "Thread " << id << " waiting...\n";
        int value = future.get(); // Multiple threads can call get()
        std::cout << "Thread " << id << " got value: " << value << "\n";
    };

    std::thread t1(waiter, shared, 1);
    std::thread t2(waiter, shared, 2);
    std::thread t3(waiter, shared, 3);

    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    std::cout << "Setting promise value...\n";
    promise.set_value(100);

    t1.join();
    t2.join();
    t3.join();

    std::cout << "shared_future allows multiple threads to access same result\n";
}

// ==============================================
// 9. Async with Return Reference
// ==============================================

void asyncReferenceDemo() {
    std::cout << "\n=== 9. Async with References ===\n";

    int value = 10;

    // Pass by reference using std::ref
    auto future = std::async(std::launch::async, [](int& val) {
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        val *= 2;
        return val;
    }, std::ref(value));

    int result = future.get();

    std::cout << "Result: " << result << "\n";
    std::cout << "Original value modified: " << value << "\n";
}

// ==============================================
// 10. Exception Handling with Async
// ==============================================

int riskyOperation(int x) {
    if (x < 0) {
        throw std::invalid_argument("Negative value not allowed");
    }
    return x * 2;
}

void asyncExceptionDemo() {
    std::cout << "\n=== 10. Exception Handling with Async ===\n";

    auto future1 = std::async(std::launch::async, riskyOperation, 10);
    auto future2 = std::async(std::launch::async, riskyOperation, -5);

    try {
        std::cout << "Result 1: " << future1.get() << "\n";
    } catch (const std::exception& e) {
        std::cout << "Exception from future1: " << e.what() << "\n";
    }

    try {
        std::cout << "Result 2: " << future2.get() << "\n";
    } catch (const std::exception& e) {
        std::cout << "Exception from future2: " << e.what() << "\n";
    }
}

// ==============================================
// 11. Producer-Consumer with Promise/Future
// ==============================================

void producerConsumerDemo() {
    std::cout << "\n=== 11. Producer-Consumer Pattern ===\n";

    std::vector<std::promise<int>> promises(5);
    std::vector<std::future<int>> futures;

    // Get futures from promises
    for (auto& promise : promises) {
        futures.push_back(promise.get_future());
    }

    // Consumer thread
    std::thread consumer([&futures]() {
        for (size_t i = 0; i < futures.size(); ++i) {
            int value = futures[i].get();
            std::cout << "Consumed: " << value << "\n";
        }
    });

    // Producer thread
    std::thread producer([&promises]() {
        for (size_t i = 0; i < promises.size(); ++i) {
            std::this_thread::sleep_for(std::chrono::milliseconds(200));
            promises[i].set_value(i * 10);
            std::cout << "Produced: " << (i * 10) << "\n";
        }
    });

    producer.join();
    consumer.join();
}

// ==============================================
// 12. Chaining Async Operations
// ==============================================

void chainingAsyncDemo() {
    std::cout << "\n=== 12. Chaining Async Operations ===\n";

    auto stage1 = std::async(std::launch::async, []() {
        std::cout << "Stage 1: Processing...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        return 10;
    });

    auto stage2 = std::async(std::launch::async, [&stage1]() {
        int value = stage1.get();
        std::cout << "Stage 2: Got " << value << ", processing...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        return value * 2;
    });

    auto stage3 = std::async(std::launch::async, [&stage2]() {
        int value = stage2.get();
        std::cout << "Stage 3: Got " << value << ", processing...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        return value + 5;
    });

    std::cout << "Final result: " << stage3.get() << "\n";
}

int main() {
    std::cout << "=== C++ Async, Future, Promise, and Packaged Task ===\n";

    // 1. Basic async
    basicAsyncDemo();

    // 2. Launch policies
    launchPoliciesDemo();

    // 3. Multiple async tasks
    multipleAsyncDemo();

    // 4. Promise
    promiseDemo();

    // 5. Promise with exception
    promiseExceptionDemo();

    // 6. Packaged task
    packagedTaskDemo();

    // 7. Future states
    futureStatesDemo();

    // 8. Shared future
    sharedFutureDemo();

    // 9. Async with references
    asyncReferenceDemo();

    // 10. Exception handling
    asyncExceptionDemo();

    // 11. Producer-consumer
    producerConsumerDemo();

    // 12. Chaining operations
    chainingAsyncDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::async runs tasks asynchronously and returns future\n";
    std::cout << "2. std::future retrieves result (blocking on get())\n";
    std::cout << "3. std::promise allows manual result setting\n";
    std::cout << "4. std::packaged_task wraps callable for async execution\n";
    std::cout << "5. Launch policies: async (new thread) vs deferred (lazy)\n";
    std::cout << "6. std::shared_future allows multiple readers\n";
    std::cout << "7. Exceptions propagate through futures\n";

    return 0;
}
