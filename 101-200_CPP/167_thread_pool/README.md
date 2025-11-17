# Program 167: Thread Pool

## Description
Implements a thread pool pattern for efficient task management, reusing a fixed number of worker threads to execute multiple tasks without the overhead of creating/destroying threads.

## Learning Objectives
- Design and implement a thread pool
- Use work queues for task distribution
- Apply RAII for resource management
- Handle thread pool shutdown gracefully
- Manage task futures for result retrieval

## Features
- Thread pool implementation
- Task queue management
- Worker thread lifecycle
- Task submission and execution
- Future-based result retrieval
- Graceful shutdown

## Compilation
```bash
g++ -std=c++17 main.cpp -o thread_pool -pthread
./thread_pool
```

## Key Concepts
```cpp
class ThreadPool {
    vector<thread> workers;
    queue<function<void()>> tasks;
    mutex queue_mutex;
    condition_variable condition;
    
    template<class F>
    auto enqueue(F&& f) -> future<...>;
};
```

## Best Practices
1. Size pool based on hardware concurrency
2. Use condition variables for efficient waiting
3. Implement graceful shutdown
4. Return futures for async results
5. Handle exceptions in tasks

## Navigation
- **Previous**: [166 - Atomics](/home/user/DevOps-prj500/101-200_CPP/166_atomics/README.md)
- **Next**: [168 - Async Future](/home/user/DevOps-prj500/101-200_CPP/168_async_future/README.md)
