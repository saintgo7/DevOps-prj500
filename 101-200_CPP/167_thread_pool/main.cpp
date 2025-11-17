/*
 * Program 167: Thread Pool - Efficient Thread Management and Task Queue
 *
 * This program demonstrates:
 * - Thread pool implementation
 * - Task queue with work stealing
 * - Future-based results
 * - Dynamic thread management
 * - Work distribution strategies
 */

#include <iostream>
#include <thread>
#include <vector>
#include <queue>
#include <functional>
#include <mutex>
#include <condition_variable>
#include <future>
#include <atomic>
#include <chrono>
#include <random>

// ==============================================
// 1. Basic Thread Pool
// ==============================================

class BasicThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool stop = false;

public:
    explicit BasicThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this, i] {
                std::cout << "Worker " << i << " started\n";

                while (true) {
                    std::function<void()> task;

                    {
                        std::unique_lock<std::mutex> lock(queue_mutex);

                        // Wait for task or stop signal
                        condition.wait(lock, [this] {
                            return stop || !tasks.empty();
                        });

                        if (stop && tasks.empty()) {
                            std::cout << "Worker " << i << " stopping\n";
                            return;
                        }

                        task = std::move(tasks.front());
                        tasks.pop();
                    }

                    task(); // Execute task
                }
            });
        }
    }

    ~BasicThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }

        condition.notify_all();

        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }

        std::cout << "Thread pool destroyed\n";
    }

    void enqueue(std::function<void()> task) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            tasks.push(std::move(task));
        }
        condition.notify_one();
    }
};

void basicThreadPoolDemo() {
    std::cout << "\n=== 1. Basic Thread Pool ===\n";

    BasicThreadPool pool(4);

    for (int i = 0; i < 10; ++i) {
        pool.enqueue([i] {
            std::cout << "Task " << i << " executing on thread "
                     << std::this_thread::get_id() << "\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        });
    }

    std::this_thread::sleep_for(std::chrono::seconds(2));
    std::cout << "Basic thread pool demo completed\n";
}

// ==============================================
// 2. Thread Pool with Future Results
// ==============================================

class FutureThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool stop = false;

public:
    explicit FutureThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;

                    {
                        std::unique_lock<std::mutex> lock(queue_mutex);
                        condition.wait(lock, [this] {
                            return stop || !tasks.empty();
                        });

                        if (stop && tasks.empty()) {
                            return;
                        }

                        task = std::move(tasks.front());
                        tasks.pop();
                    }

                    task();
                }
            });
        }
    }

    ~FutureThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }
        condition.notify_all();

        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }

    template<typename F, typename... Args>
    auto enqueue(F&& f, Args&&... args)
        -> std::future<typename std::invoke_result<F, Args...>::type>
    {
        using return_type = typename std::invoke_result<F, Args...>::type;

        auto task = std::make_shared<std::packaged_task<return_type()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        );

        std::future<return_type> result = task->get_future();

        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            if (stop) {
                throw std::runtime_error("enqueue on stopped ThreadPool");
            }
            tasks.emplace([task]() { (*task)(); });
        }

        condition.notify_one();
        return result;
    }
};

int computeSquare(int x) {
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    return x * x;
}

void futureThreadPoolDemo() {
    std::cout << "\n=== 2. Thread Pool with Futures ===\n";

    FutureThreadPool pool(4);

    std::vector<std::future<int>> results;

    for (int i = 1; i <= 10; ++i) {
        results.push_back(pool.enqueue(computeSquare, i));
    }

    for (size_t i = 0; i < results.size(); ++i) {
        std::cout << "Result " << (i + 1) << ": " << results[i].get() << "\n";
    }

    std::cout << "Future-based thread pool demo completed\n";
}

// ==============================================
// 3. Thread Pool with Priority Queue
// ==============================================

struct PriorityTask {
    int priority;
    std::function<void()> task;

    bool operator<(const PriorityTask& other) const {
        return priority < other.priority; // Higher priority first
    }
};

class PriorityThreadPool {
private:
    std::vector<std::thread> workers;
    std::priority_queue<PriorityTask> tasks;
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool stop = false;

public:
    explicit PriorityThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;

                    {
                        std::unique_lock<std::mutex> lock(queue_mutex);
                        condition.wait(lock, [this] {
                            return stop || !tasks.empty();
                        });

                        if (stop && tasks.empty()) {
                            return;
                        }

                        task = std::move(tasks.top().task);
                        tasks.pop();
                    }

                    task();
                }
            });
        }
    }

    ~PriorityThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }
        condition.notify_all();

        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }

    void enqueue(int priority, std::function<void()> task) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            tasks.push({priority, std::move(task)});
        }
        condition.notify_one();
    }
};

void priorityThreadPoolDemo() {
    std::cout << "\n=== 3. Priority Thread Pool ===\n";

    PriorityThreadPool pool(2);

    // Submit tasks with different priorities
    pool.enqueue(1, [] {
        std::cout << "Low priority task\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    });

    pool.enqueue(10, [] {
        std::cout << "High priority task\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    });

    pool.enqueue(5, [] {
        std::cout << "Medium priority task\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    std::cout << "Priority thread pool demo completed\n";
}

// ==============================================
// 4. Dynamic Thread Pool
// ==============================================

class DynamicThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable condition;
    std::atomic<bool> stop{false};
    std::atomic<int> active_threads{0};
    size_t min_threads;
    size_t max_threads;

    void worker_thread() {
        while (!stop) {
            std::function<void()> task;

            {
                std::unique_lock<std::mutex> lock(queue_mutex);

                condition.wait_for(lock, std::chrono::milliseconds(100), [this] {
                    return stop.load() || !tasks.empty();
                });

                if (stop && tasks.empty()) {
                    return;
                }

                if (tasks.empty()) {
                    continue;
                }

                task = std::move(tasks.front());
                tasks.pop();
            }

            ++active_threads;
            task();
            --active_threads;
        }
    }

public:
    DynamicThreadPool(size_t min_t, size_t max_t)
        : min_threads(min_t), max_threads(max_t)
    {
        for (size_t i = 0; i < min_threads; ++i) {
            workers.emplace_back([this] { worker_thread(); });
        }
        std::cout << "Dynamic pool started with " << min_threads << " threads\n";
    }

    ~DynamicThreadPool() {
        stop = true;
        condition.notify_all();

        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }

    void enqueue(std::function<void()> task) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            tasks.push(std::move(task));

            // Spawn new thread if needed and under max
            if (tasks.size() > active_threads && workers.size() < max_threads) {
                workers.emplace_back([this] { worker_thread(); });
                std::cout << "Spawned new thread, total: " << workers.size() << "\n";
            }
        }
        condition.notify_one();
    }

    size_t thread_count() const {
        return workers.size();
    }
};

void dynamicThreadPoolDemo() {
    std::cout << "\n=== 4. Dynamic Thread Pool ===\n";

    DynamicThreadPool pool(2, 8);

    // Submit many tasks to trigger thread spawning
    for (int i = 0; i < 20; ++i) {
        pool.enqueue([i] {
            std::cout << "Task " << i << " executing\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(200));
        });
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::cout << "Final thread count: " << pool.thread_count() << "\n";
}

// ==============================================
// 5. Work Stealing Thread Pool (Simplified)
// ==============================================

class WorkStealingPool {
private:
    struct WorkerData {
        std::queue<std::function<void()>> tasks;
        std::mutex mutex;
    };

    std::vector<std::thread> workers;
    std::vector<WorkerData> worker_queues;
    std::atomic<bool> stop{false};

    void worker_thread(size_t id) {
        std::random_device rd;
        std::mt19937 gen(rd());

        while (!stop) {
            std::function<void()> task;

            // Try to get task from own queue
            {
                std::unique_lock<std::mutex> lock(worker_queues[id].mutex);
                if (!worker_queues[id].tasks.empty()) {
                    task = std::move(worker_queues[id].tasks.front());
                    worker_queues[id].tasks.pop();
                }
            }

            // If no task, try to steal from another worker
            if (!task) {
                std::uniform_int_distribution<> dis(0, workers.size() - 1);
                size_t steal_from = dis(gen);

                if (steal_from != id) {
                    std::unique_lock<std::mutex> lock(worker_queues[steal_from].mutex);
                    if (!worker_queues[steal_from].tasks.empty()) {
                        task = std::move(worker_queues[steal_from].tasks.front());
                        worker_queues[steal_from].tasks.pop();
                        std::cout << "Worker " << id << " stole task from " << steal_from << "\n";
                    }
                }
            }

            if (task) {
                task();
            } else {
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
        }
    }

public:
    explicit WorkStealingPool(size_t num_threads) : worker_queues(num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this, i] { worker_thread(i); });
        }
    }

    ~WorkStealingPool() {
        stop = true;
        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }

    void enqueue(size_t worker_id, std::function<void()> task) {
        std::unique_lock<std::mutex> lock(worker_queues[worker_id].mutex);
        worker_queues[worker_id].tasks.push(std::move(task));
    }
};

void workStealingDemo() {
    std::cout << "\n=== 5. Work Stealing Thread Pool ===\n";

    WorkStealingPool pool(4);

    // Add all tasks to worker 0
    for (int i = 0; i < 16; ++i) {
        pool.enqueue(0, [i] {
            std::cout << "Task " << i << " on thread " << std::this_thread::get_id() << "\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        });
    }

    std::this_thread::sleep_for(std::chrono::seconds(2));
    std::cout << "Work stealing helps balance load across threads\n";
}

// ==============================================
// 6. Performance Comparison
// ==============================================

void performanceComparison() {
    std::cout << "\n=== 6. Performance Comparison ===\n";

    const int num_tasks = 100;

    auto compute = [](int x) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        return x * x;
    };

    // Single-threaded
    {
        auto start = std::chrono::high_resolution_clock::now();

        for (int i = 0; i < num_tasks; ++i) {
            compute(i);
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << "Single-threaded: " << duration.count() << "ms\n";
    }

    // Thread pool
    {
        auto start = std::chrono::high_resolution_clock::now();

        FutureThreadPool pool(8);
        std::vector<std::future<int>> results;

        for (int i = 0; i < num_tasks; ++i) {
            results.push_back(pool.enqueue(compute, i));
        }

        for (auto& result : results) {
            result.get();
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << "Thread pool (8 threads): " << duration.count() << "ms\n";
    }
}

int main() {
    std::cout << "=== C++ Thread Pool Implementation ===\n";

    // 1. Basic thread pool
    basicThreadPoolDemo();

    // 2. Future-based thread pool
    futureThreadPoolDemo();

    // 3. Priority thread pool
    priorityThreadPoolDemo();

    // 4. Dynamic thread pool
    dynamicThreadPoolDemo();

    // 5. Work stealing
    workStealingDemo();

    // 6. Performance comparison
    performanceComparison();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. Thread pools reuse threads, avoiding creation overhead\n";
    std::cout << "2. Use futures to get results from tasks\n";
    std::cout << "3. Priority queues allow task prioritization\n";
    std::cout << "4. Dynamic pools adapt to workload\n";
    std::cout << "5. Work stealing balances load across workers\n";
    std::cout << "6. Pool size should match hardware_concurrency()\n";

    return 0;
}
