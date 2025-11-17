/*
 * Program 169: C++20 Coroutines - co_await, co_yield, co_return
 *
 * This program demonstrates:
 * - Coroutine basics with co_await, co_yield, co_return
 * - Generator pattern with co_yield
 * - Async coroutines
 * - Promise types and awaitable objects
 * - Practical coroutine examples
 *
 * Note: Requires C++20 compiler with coroutine support
 * Compile with: g++ -std=c++20 -fcoroutines
 */

#include <iostream>
#include <coroutine>
#include <optional>
#include <stdexcept>
#include <memory>
#include <chrono>
#include <thread>

// ==============================================
// 1. Basic Generator with co_yield
// ==============================================

template<typename T>
struct Generator {
    struct promise_type {
        T current_value;
        std::exception_ptr exception;

        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }

        std::suspend_always yield_value(T value) {
            current_value = value;
            return {};
        }

        void return_void() {}

        void unhandled_exception() {
            exception = std::current_exception();
        }
    };

    std::coroutine_handle<promise_type> handle;

    explicit Generator(std::coroutine_handle<promise_type> h) : handle(h) {}

    ~Generator() {
        if (handle) {
            handle.destroy();
        }
    }

    // Non-copyable
    Generator(const Generator&) = delete;
    Generator& operator=(const Generator&) = delete;

    // Movable
    Generator(Generator&& other) noexcept : handle(other.handle) {
        other.handle = nullptr;
    }

    Generator& operator=(Generator&& other) noexcept {
        if (this != &other) {
            if (handle) {
                handle.destroy();
            }
            handle = other.handle;
            other.handle = nullptr;
        }
        return *this;
    }

    bool next() {
        if (!handle || handle.done()) {
            return false;
        }
        handle.resume();
        if (handle.promise().exception) {
            std::rethrow_exception(handle.promise().exception);
        }
        return !handle.done();
    }

    T value() const {
        return handle.promise().current_value;
    }
};

// Simple number generator
Generator<int> numberGenerator(int start, int end) {
    for (int i = start; i <= end; ++i) {
        co_yield i; // Suspend and return value
    }
}

void generatorDemo() {
    std::cout << "\n=== 1. Basic Generator with co_yield ===\n";

    auto gen = numberGenerator(1, 5);

    std::cout << "Generated numbers: ";
    while (gen.next()) {
        std::cout << gen.value() << " ";
    }
    std::cout << "\n";
}

// ==============================================
// 2. Fibonacci Generator
// ==============================================

Generator<unsigned long long> fibonacci() {
    unsigned long long a = 0, b = 1;

    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

void fibonacciDemo() {
    std::cout << "\n=== 2. Fibonacci Generator ===\n";

    auto fib = fibonacci();

    std::cout << "First 10 Fibonacci numbers: ";
    for (int i = 0; i < 10; ++i) {
        fib.next();
        std::cout << fib.value() << " ";
    }
    std::cout << "\n";
}

// ==============================================
// 3. Task Coroutine with co_return
// ==============================================

template<typename T>
struct Task {
    struct promise_type {
        T value;
        std::exception_ptr exception;

        Task get_return_object() {
            return Task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }

        void return_value(T v) {
            value = v;
        }

        void unhandled_exception() {
            exception = std::current_exception();
        }
    };

    std::coroutine_handle<promise_type> handle;

    explicit Task(std::coroutine_handle<promise_type> h) : handle(h) {}

    ~Task() {
        if (handle) {
            handle.destroy();
        }
    }

    T get() {
        if (handle.promise().exception) {
            std::rethrow_exception(handle.promise().exception);
        }
        return handle.promise().value;
    }
};

Task<int> computeValue(int x) {
    std::cout << "Computing " << x << " * 2\n";
    co_return x * 2;
}

void taskDemo() {
    std::cout << "\n=== 3. Task Coroutine with co_return ===\n";

    auto task = computeValue(21);
    std::cout << "Result: " << task.get() << "\n";
}

// ==============================================
// 4. Awaitable Type
// ==============================================

struct Awaitable {
    int value;

    bool await_ready() const noexcept {
        std::cout << "await_ready() called\n";
        return false; // Always suspend
    }

    void await_suspend(std::coroutine_handle<> handle) const noexcept {
        std::cout << "await_suspend() called\n";
        // Could schedule resumption on another thread here
        handle.resume(); // Resume immediately for demo
    }

    int await_resume() const noexcept {
        std::cout << "await_resume() called\n";
        return value;
    }
};

Task<int> awaitableExample() {
    std::cout << "Before co_await\n";
    int result = co_await Awaitable{42};
    std::cout << "After co_await, got: " << result << "\n";
    co_return result * 2;
}

void awaitableDemo() {
    std::cout << "\n=== 4. Awaitable Type with co_await ===\n";

    auto task = awaitableExample();
    std::cout << "Final result: " << task.get() << "\n";
}

// ==============================================
// 5. Range Generator
// ==============================================

Generator<int> range(int start, int end, int step = 1) {
    for (int i = start; i < end; i += step) {
        co_yield i;
    }
}

void rangeDemo() {
    std::cout << "\n=== 5. Range Generator ===\n";

    std::cout << "Range(0, 20, 3): ";
    auto r = range(0, 20, 3);
    while (r.next()) {
        std::cout << r.value() << " ";
    }
    std::cout << "\n";
}

// ==============================================
// 6. Async Sleeper (Conceptual)
// ==============================================

struct SleepAwaitable {
    std::chrono::milliseconds duration;

    bool await_ready() const noexcept {
        return duration.count() <= 0;
    }

    void await_suspend(std::coroutine_handle<> handle) const {
        // In real implementation, would schedule resumption after delay
        std::thread([handle, duration = this->duration]() {
            std::this_thread::sleep_for(duration);
            handle.resume();
        }).detach();
    }

    void await_resume() const noexcept {}
};

SleepAwaitable sleep_for(std::chrono::milliseconds duration) {
    return SleepAwaitable{duration};
}

Task<void> asyncSleeper() {
    std::cout << "Starting sleep...\n";
    co_await sleep_for(std::chrono::milliseconds(500));
    std::cout << "Woke up after sleep!\n";
    co_return;
}

// Promise type for Task<void>
template<>
struct Task<void> {
    struct promise_type {
        std::exception_ptr exception;

        Task get_return_object() {
            return Task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }

        void return_void() {}

        void unhandled_exception() {
            exception = std::current_exception();
        }
    };

    std::coroutine_handle<promise_type> handle;

    explicit Task(std::coroutine_handle<promise_type> h) : handle(h) {}

    ~Task() {
        if (handle) {
            handle.destroy();
        }
    }

    void wait() {
        if (handle.promise().exception) {
            std::rethrow_exception(handle.promise().exception);
        }
    }
};

void asyncDemo() {
    std::cout << "\n=== 6. Async Sleeper ===\n";

    auto task = asyncSleeper();
    std::this_thread::sleep_for(std::chrono::milliseconds(600)); // Wait for async completion
}

// ==============================================
// 7. Recursive Generator
// ==============================================

Generator<int> tree_traversal(int depth, int value = 0) {
    if (depth == 0) {
        co_yield value;
    } else {
        auto left = tree_traversal(depth - 1, value * 2);
        while (left.next()) {
            co_yield left.value();
        }

        co_yield value;

        auto right = tree_traversal(depth - 1, value * 2 + 1);
        while (right.next()) {
            co_yield right.value();
        }
    }
}

void recursiveGeneratorDemo() {
    std::cout << "\n=== 7. Recursive Generator (Binary Tree) ===\n";

    auto tree = tree_traversal(3);

    std::cout << "Tree traversal: ";
    while (tree.next()) {
        std::cout << tree.value() << " ";
    }
    std::cout << "\n";
}

// ==============================================
// 8. Generator with Filtering
// ==============================================

template<typename T, typename Pred>
Generator<T> filter(Generator<T>& source, Pred predicate) {
    while (source.next()) {
        T value = source.value();
        if (predicate(value)) {
            co_yield value;
        }
    }
}

void filterDemo() {
    std::cout << "\n=== 8. Generator with Filtering ===\n";

    auto numbers = range(1, 20);
    auto evens = filter(numbers, [](int x) { return x % 2 == 0; });

    std::cout << "Even numbers: ";
    while (evens.next()) {
        std::cout << evens.value() << " ";
    }
    std::cout << "\n";
}

// ==============================================
// 9. Stateful Generator
// ==============================================

Generator<std::string> statefulGenerator() {
    int state = 0;

    while (state < 5) {
        std::string msg = "State: " + std::to_string(state);
        ++state;
        co_yield msg;
    }

    co_yield "Completed";
}

void statefulDemo() {
    std::cout << "\n=== 9. Stateful Generator ===\n";

    auto gen = statefulGenerator();

    while (gen.next()) {
        std::cout << gen.value() << "\n";
    }
}

// ==============================================
// 10. Exception Handling in Coroutines
// ==============================================

Generator<int> throwingGenerator() {
    co_yield 1;
    co_yield 2;
    throw std::runtime_error("Generator error!");
    co_yield 3; // Never reached
}

void exceptionDemo() {
    std::cout << "\n=== 10. Exception Handling ===\n";

    auto gen = throwingGenerator();

    try {
        while (gen.next()) {
            std::cout << "Value: " << gen.value() << "\n";
        }
    } catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << "\n";
    }
}

int main() {
    std::cout << "=== C++20 Coroutines ===\n";
    std::cout << "Note: Requires C++20 with coroutine support\n";

    // 1. Basic generator
    generatorDemo();

    // 2. Fibonacci
    fibonacciDemo();

    // 3. Task with co_return
    taskDemo();

    // 4. Awaitable
    awaitableDemo();

    // 5. Range
    rangeDemo();

    // 6. Async sleeper
    asyncDemo();

    // 7. Recursive generator
    recursiveGeneratorDemo();

    // 8. Filtering
    filterDemo();

    // 9. Stateful generator
    statefulDemo();

    // 10. Exception handling
    exceptionDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. co_yield suspends coroutine and returns value\n";
    std::cout << "2. co_return returns final value and ends coroutine\n";
    std::cout << "3. co_await suspends until awaitable is ready\n";
    std::cout << "4. promise_type defines coroutine behavior\n";
    std::cout << "5. Generators enable lazy evaluation\n";
    std::cout << "6. Coroutines are stackless and efficient\n";
    std::cout << "7. Great for async I/O and sequence generation\n";

    return 0;
}
