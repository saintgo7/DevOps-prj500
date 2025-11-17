# Program 163: Multithreading

## Description
This program introduces multithreading in C++ using the std::thread library. It demonstrates thread creation, management, synchronization basics, and common multithreading patterns.

## Learning Objectives
- Create and manage threads with std::thread
- Pass arguments to threads correctly
- Join and detach threads appropriately
- Understand thread lifecycle
- Handle thread exceptions
- Identify data races and race conditions

## Features
- Basic thread creation
- Passing arguments to threads
- Thread joining and detaching
- Lambda functions with threads
- Thread with member functions
- Multiple thread coordination
- Exception handling in threads

## Compilation and Usage
```bash
g++ -std=c++17 main.cpp -o multithreading -pthread
./multithreading
```

## Key Concepts

### Creating Threads
```cpp
void task() { /* work */ }
std::thread t1(task);
std::thread t2([](){ /* lambda */ });
t1.join();  // Wait for completion
```

### Passing Arguments
```cpp
void func(int x, const string& s);
std::thread t(func, 42, "hello");
```

## Best Practices
1. Always join or detach threads
2. Use RAII for thread management
3. Pass large objects by reference with std::ref
4. Be careful with thread-local variables
5. Handle exceptions in thread functions

## Resources
- [cppreference: std::thread](https://en.cppreference.com/w/cpp/thread/thread)
- [C++ Concurrency in Action](https://www.manning.com/books/c-plus-plus-concurrency-in-action)

## Navigation
- **Previous**: [162 - Perfect Forwarding](/home/user/DevOps-prj500/101-200_CPP/162_perfect_forwarding/README.md)
- **Next**: [164 - Mutex Locks](/home/user/DevOps-prj500/101-200_CPP/164_mutex_locks/README.md)
