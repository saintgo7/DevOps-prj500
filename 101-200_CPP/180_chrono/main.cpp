/*
 * Program 180: std::chrono - Time Points, Durations, and Clocks
 *
 * This program demonstrates:
 * - std::chrono library for time utilities
 * - Duration types and arithmetic
 * - Time points and clocks
 * - Time measurement and benchmarking
 * - Date and time operations (C++20)
 */

#include <iostream>
#include <chrono>
#include <thread>
#include <iomanip>
#include <ctime>
#include <vector>
#include <algorithm>

// Namespace alias for convenience
using namespace std::chrono;
using namespace std::chrono_literals; // For 1s, 100ms, etc.

// ==============================================
// 1. Duration Basics
// ==============================================

void durationBasicsDemo() {
    std::cout << "\n=== 1. Duration Basics ===\n";

    // Standard duration types
    seconds sec(5);
    milliseconds ms(5000);
    microseconds us(5000000);
    nanoseconds ns(5000000000);
    minutes min(1);
    hours hr(1);

    std::cout << "5 seconds: " << sec.count() << " s\n";
    std::cout << "5000 milliseconds: " << ms.count() << " ms\n";
    std::cout << "1 minute: " << min.count() << " min\n";
    std::cout << "1 hour: " << hr.count() << " h\n";

    // Using literals (C++14)
    auto d1 = 100ms;
    auto d2 = 5s;
    auto d3 = 2min;
    auto d4 = 1h;

    std::cout << "\nUsing literals:\n";
    std::cout << "100ms: " << d1.count() << " ms\n";
    std::cout << "5s: " << d2.count() << " s\n";
}

// ==============================================
// 2. Duration Conversions
// ==============================================

void durationConversionsDemo() {
    std::cout << "\n=== 2. Duration Conversions ===\n";

    seconds sec(5);

    // Implicit conversion (safe direction: smaller to larger)
    minutes min = sec; // Error: loses precision

    // Explicit conversion using duration_cast
    auto ms = duration_cast<milliseconds>(sec);
    auto us = duration_cast<microseconds>(sec);

    std::cout << "5 seconds:\n";
    std::cout << "  = " << ms.count() << " milliseconds\n";
    std::cout << "  = " << us.count() << " microseconds\n";

    // Converting back (loses precision)
    milliseconds ms2(5500);
    auto sec2 = duration_cast<seconds>(ms2);
    std::cout << "\n5500 milliseconds:\n";
    std::cout << "  = " << sec2.count() << " seconds (truncated)\n";
}

// ==============================================
// 3. Duration Arithmetic
// ==============================================

void durationArithmeticDemo() {
    std::cout << "\n=== 3. Duration Arithmetic ===\n";

    auto d1 = 5s;
    auto d2 = 3s;

    // Addition
    auto sum = d1 + d2;
    std::cout << "5s + 3s = " << sum.count() << " s\n";

    // Subtraction
    auto diff = d1 - d2;
    std::cout << "5s - 3s = " << diff.count() << " s\n";

    // Multiplication
    auto mult = d1 * 3;
    std::cout << "5s * 3 = " << mult.count() << " s\n";

    // Division
    auto div = d1 / 2;
    std::cout << "5s / 2 = " << div.count() << " s\n";

    // Modulo
    auto mod = d1 % 2s;
    std::cout << "5s %% 2s = " << mod.count() << " s\n";

    // Mixed duration arithmetic
    auto mixed = 1h + 30min + 45s;
    auto total_seconds = duration_cast<seconds>(mixed);
    std::cout << "\n1h + 30min + 45s = " << total_seconds.count() << " s\n";
}

// ==============================================
// 4. Comparison
// ==============================================

void durationComparisonDemo() {
    std::cout << "\n=== 4. Duration Comparison ===\n";

    auto d1 = 5s;
    auto d2 = 5000ms;
    auto d3 = 3s;

    std::cout << std::boolalpha;
    std::cout << "5s == 5000ms: " << (d1 == d2) << "\n";
    std::cout << "5s != 3s: " << (d1 != d3) << "\n";
    std::cout << "5s > 3s: " << (d1 > d3) << "\n";
    std::cout << "3s < 5s: " << (d3 < d1) << "\n";
}

// ==============================================
// 5. Clocks
// ==============================================

void clocksDemo() {
    std::cout << "\n=== 5. Clocks ===\n";

    // system_clock - wall clock time
    std::cout << "system_clock:\n";
    std::cout << "  is_steady: " << std::boolalpha
              << system_clock::is_steady << "\n";

    auto now = system_clock::now();
    auto now_c = system_clock::to_time_t(now);
    std::cout << "  Current time: " << std::ctime(&now_c);

    // steady_clock - monotonic clock (never goes backwards)
    std::cout << "\nsteady_clock:\n";
    std::cout << "  is_steady: " << steady_clock::is_steady << "\n";
    std::cout << "  Use for timing and benchmarking\n";

    // high_resolution_clock - highest precision clock
    std::cout << "\nhigh_resolution_clock:\n";
    std::cout << "  is_steady: " << high_resolution_clock::is_steady << "\n";
    std::cout << "  Use for precise measurements\n";
}

// ==============================================
// 6. Time Points
// ==============================================

void timePointsDemo() {
    std::cout << "\n=== 6. Time Points ===\n";

    // Get current time point
    auto now = system_clock::now();

    // Time since epoch
    auto since_epoch = now.time_since_epoch();
    auto millis = duration_cast<milliseconds>(since_epoch);
    std::cout << "Milliseconds since epoch: " << millis.count() << "\n";

    // Time point arithmetic
    auto tomorrow = now + 24h;
    auto yesterday = now - 24h;

    std::cout << "\nTime points:\n";
    std::cout << "  Now (epoch ms): " << millis.count() << "\n";

    // Duration between time points
    auto diff = tomorrow - now;
    std::cout << "  Tomorrow - Now: " << duration_cast<hours>(diff).count() << " hours\n";
}

// ==============================================
// 7. Measuring Elapsed Time
// ==============================================

template<typename Func>
auto measureTime(Func func) {
    auto start = high_resolution_clock::now();
    func();
    auto end = high_resolution_clock::now();
    return end - start;
}

void measuringTimeDemo() {
    std::cout << "\n=== 7. Measuring Elapsed Time ===\n";

    auto elapsed = measureTime([] {
        std::this_thread::sleep_for(100ms);
    });

    auto ms = duration_cast<milliseconds>(elapsed);
    std::cout << "Sleep for 100ms took: " << ms.count() << " ms\n";

    // Benchmark example
    std::cout << "\nBenchmarking vector operations:\n";

    std::vector<int> vec(1000000);

    auto fill_time = measureTime([&vec] {
        std::fill(vec.begin(), vec.end(), 42);
    });

    auto sort_time = measureTime([&vec] {
        std::sort(vec.begin(), vec.end());
    });

    std::cout << "  Fill: " << duration_cast<microseconds>(fill_time).count() << " μs\n";
    std::cout << "  Sort: " << duration_cast<microseconds>(sort_time).count() << " μs\n";
}

// ==============================================
// 8. Timer Class
// ==============================================

class Timer {
private:
    time_point<high_resolution_clock> start_time;

public:
    Timer() : start_time(high_resolution_clock::now()) {}

    void reset() {
        start_time = high_resolution_clock::now();
    }

    template<typename Duration = milliseconds>
    auto elapsed() const {
        auto end = high_resolution_clock::now();
        return duration_cast<Duration>(end - start_time);
    }

    void printElapsed(const std::string& label = "Elapsed") const {
        std::cout << label << ": " << elapsed().count() << " ms\n";
    }
};

void timerClassDemo() {
    std::cout << "\n=== 8. Timer Class ===\n";

    Timer timer;

    std::this_thread::sleep_for(50ms);
    timer.printElapsed("After 50ms sleep");

    std::this_thread::sleep_for(100ms);
    timer.printElapsed("Total");

    timer.reset();
    std::this_thread::sleep_for(25ms);
    timer.printElapsed("After reset and 25ms");
}

// ==============================================
// 9. Timeout Operations
// ==============================================

bool waitForCondition(std::chrono::milliseconds timeout) {
    auto deadline = steady_clock::now() + timeout;

    while (steady_clock::now() < deadline) {
        // Simulate checking condition
        std::this_thread::sleep_for(10ms);

        // Random success after some time
        if (steady_clock::now() > deadline - 20ms) {
            return true; // Condition met
        }
    }

    return false; // Timeout
}

void timeoutDemo() {
    std::cout << "\n=== 9. Timeout Operations ===\n";

    std::cout << "Waiting for condition (100ms timeout)...\n";
    bool success = waitForCondition(100ms);

    if (success) {
        std::cout << "Condition met before timeout\n";
    } else {
        std::cout << "Timeout occurred\n";
    }
}

// ==============================================
// 10. Sleep Operations
// ==============================================

void sleepDemo() {
    std::cout << "\n=== 10. Sleep Operations ===\n";

    std::cout << "Sleeping for 100ms...\n";
    auto start = steady_clock::now();

    std::this_thread::sleep_for(100ms);

    auto elapsed = steady_clock::now() - start;
    std::cout << "Actual sleep time: "
              << duration_cast<milliseconds>(elapsed).count() << " ms\n";

    // Sleep until time point
    std::cout << "\nSleeping until time point (200ms from now)...\n";
    auto wake_time = steady_clock::now() + 200ms;
    start = steady_clock::now();

    std::this_thread::sleep_until(wake_time);

    elapsed = steady_clock::now() - start;
    std::cout << "Slept for: " << duration_cast<milliseconds>(elapsed).count() << " ms\n";
}

// ==============================================
// 11. Formatting Time
// ==============================================

void formatTimeDemo() {
    std::cout << "\n=== 11. Formatting Time ===\n";

    auto now = system_clock::now();
    auto now_c = system_clock::to_time_t(now);

    // C-style formatting
    std::cout << "Default format: " << std::ctime(&now_c);

    // Custom formatting
    std::tm* tm = std::localtime(&now_c);
    std::cout << "Custom format: "
              << std::put_time(tm, "%Y-%m-%d %H:%M:%S") << "\n";

    std::cout << "ISO 8601: "
              << std::put_time(tm, "%Y-%m-%dT%H:%M:%S") << "\n";
}

// ==============================================
// 12. Rate Limiting
// ==============================================

class RateLimiter {
private:
    std::chrono::milliseconds interval;
    time_point<steady_clock> last_action;

public:
    RateLimiter(std::chrono::milliseconds ms)
        : interval(ms), last_action(steady_clock::now() - interval) {}

    bool tryAction() {
        auto now = steady_clock::now();
        auto elapsed = now - last_action;

        if (elapsed >= interval) {
            last_action = now;
            return true;
        }

        return false;
    }

    void waitAndAction() {
        auto now = steady_clock::now();
        auto elapsed = now - last_action;

        if (elapsed < interval) {
            std::this_thread::sleep_for(interval - elapsed);
        }

        last_action = steady_clock::now();
    }
};

void rateLimitingDemo() {
    std::cout << "\n=== 12. Rate Limiting ===\n";

    RateLimiter limiter(50ms);

    std::cout << "Attempting actions (50ms rate limit):\n";
    for (int i = 0; i < 5; ++i) {
        if (limiter.tryAction()) {
            std::cout << "  Action " << i << " executed\n";
        } else {
            std::cout << "  Action " << i << " rate limited\n";
        }
        std::this_thread::sleep_for(30ms);
    }
}

// ==============================================
// 13. Performance Counter
// ==============================================

class PerformanceCounter {
private:
    std::string name;
    long long count = 0;
    duration<double> total_time{0};
    time_point<high_resolution_clock> start;

public:
    PerformanceCounter(const std::string& n) : name(n) {}

    void startMeasurement() {
        start = high_resolution_clock::now();
    }

    void stopMeasurement() {
        auto end = high_resolution_clock::now();
        total_time += end - start;
        ++count;
    }

    void report() const {
        std::cout << name << " statistics:\n";
        std::cout << "  Calls: " << count << "\n";
        std::cout << "  Total time: " << total_time.count() << " s\n";

        if (count > 0) {
            auto avg = total_time / count;
            std::cout << "  Average time: " << avg.count() * 1000 << " ms\n";
        }
    }
};

void performanceCounterDemo() {
    std::cout << "\n=== 13. Performance Counter ===\n";

    PerformanceCounter counter("Work");

    for (int i = 0; i < 5; ++i) {
        counter.startMeasurement();
        std::this_thread::sleep_for(10ms + milliseconds(i * 5));
        counter.stopMeasurement();
    }

    counter.report();
}

// ==============================================
// 14. Practical Example: Stopwatch
// ==============================================

class Stopwatch {
private:
    time_point<steady_clock> start_time;
    duration<double> accumulated{0};
    bool running = false;

public:
    void start() {
        if (!running) {
            start_time = steady_clock::now();
            running = true;
        }
    }

    void stop() {
        if (running) {
            auto end = steady_clock::now();
            accumulated += end - start_time;
            running = false;
        }
    }

    void reset() {
        accumulated = duration<double>{0};
        running = false;
    }

    double elapsed() const {
        duration<double> total = accumulated;
        if (running) {
            auto end = steady_clock::now();
            total += end - start_time;
        }
        return total.count();
    }

    void display() const {
        std::cout << "Elapsed: " << std::fixed << std::setprecision(3)
                  << elapsed() << " s\n";
    }
};

void stopwatchDemo() {
    std::cout << "\n=== 14. Stopwatch Example ===\n";

    Stopwatch sw;

    std::cout << "Starting stopwatch...\n";
    sw.start();
    std::this_thread::sleep_for(500ms);
    sw.display();

    std::cout << "Pausing...\n";
    sw.stop();
    std::this_thread::sleep_for(200ms); // Not counted

    std::cout << "Resuming...\n";
    sw.start();
    std::this_thread::sleep_for(300ms);

    std::cout << "Final time:\n";
    sw.stop();
    sw.display();
}

int main() {
    std::cout << "=== C++ std::chrono - Time Utilities ===\n";

    // 1. Duration basics
    durationBasicsDemo();

    // 2. Duration conversions
    durationConversionsDemo();

    // 3. Duration arithmetic
    durationArithmeticDemo();

    // 4. Duration comparison
    durationComparisonDemo();

    // 5. Clocks
    clocksDemo();

    // 6. Time points
    timePointsDemo();

    // 7. Measuring time
    measuringTimeDemo();

    // 8. Timer class
    timerClassDemo();

    // 9. Timeout operations
    timeoutDemo();

    // 10. Sleep operations
    sleepDemo();

    // 11. Formatting time
    formatTimeDemo();

    // 12. Rate limiting
    rateLimitingDemo();

    // 13. Performance counter
    performanceCounterDemo();

    // 14. Stopwatch
    stopwatchDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::chrono provides type-safe time utilities\n";
    std::cout << "2. Duration represents time spans (seconds, milliseconds, etc.)\n";
    std::cout << "3. Time points represent specific moments in time\n";
    std::cout << "4. Three clocks: system_clock, steady_clock, high_resolution_clock\n";
    std::cout << "5. Use steady_clock for timing and benchmarking\n";
    std::cout << "6. Duration literals: 1s, 100ms, 5min, 2h (C++14)\n";
    std::cout << "7. Duration arithmetic and conversions are type-safe\n";

    return 0;
}
