# Program 168: Async and Future

## Description
Demonstrates std::async, std::future, and std::promise for asynchronous task execution and result retrieval, providing high-level abstractions for concurrent programming.

## Learning Objectives
- Use std::async for asynchronous task execution
- Retrieve results with std::future
- Create promises with std::promise
- Choose appropriate launch policies
- Handle future exceptions
- Understand shared_future

## Features
- std::async usage
- std::future result retrieval
- std::promise for custom async operations
- Launch policies (async, deferred)
- Exception propagation through futures
- std::shared_future for multiple waiters

## Compilation
```bash
g++ -std=c++17 main.cpp -o async_future -pthread
./async_future
```

## Key Concepts
```cpp
// Async
auto fut = std::async(std::launch::async, []{ return 42; });
int result = fut.get();

// Promise
std::promise<int> prom;
auto fut = prom.get_future();
prom.set_value(42);
```

## Best Practices
1. Use std::async for simple async tasks
2. Choose launch policy explicitly
3. Call get() only once per future
4. Handle exceptions from get()
5. Use shared_future for multiple consumers

## Navigation
- **Previous**: [167 - Thread Pool](/home/user/DevOps-prj500/101-200_CPP/167_thread_pool/README.md)
- **Next**: [169 - Coroutines](/home/user/DevOps-prj500/101-200_CPP/169_coroutines/README.md)
