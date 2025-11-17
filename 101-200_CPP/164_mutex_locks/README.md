# Program 164: Mutex and Locks

## Description
Demonstrates mutex and lock mechanisms in C++ for thread synchronization, including std::mutex, std::lock_guard, std::unique_lock, and std::scoped_lock to prevent data races.

## Learning Objectives
- Use std::mutex for mutual exclusion
- Apply std::lock_guard for RAII-style locking
- Master std::unique_lock for flexible locking
- Understand std::scoped_lock for multiple mutexes
- Prevent deadlocks
- Handle recursive locking

## Features
- Basic mutex usage
- lock_guard demonstration
- unique_lock with deferred/try locking
- scoped_lock for multiple mutexes
- Deadlock prevention techniques
- Recursive mutex
- Timed locks

## Compilation
```bash
g++ -std=c++17 main.cpp -o mutex_locks -pthread
./mutex_locks
```

## Key Concepts
```cpp
std::mutex mtx;
std::lock_guard<std::mutex> lock(mtx);  // RAII
std::unique_lock<std::mutex> ulock(mtx, std::defer_lock);
std::scoped_lock lock(mtx1, mtx2);  // C++17, prevents deadlock
```

## Best Practices
1. Prefer std::lock_guard for simple cases
2. Use std::scoped_lock for multiple mutexes (C++17)
3. Keep critical sections small
4. Never lock mutexes in different order across threads
5. Use RAII locks to prevent forget-to-unlock bugs

## Navigation
- **Previous**: [163 - Multithreading](/home/user/DevOps-prj500/101-200_CPP/163_multithreading/README.md)
- **Next**: [165 - Condition Variables](/home/user/DevOps-prj500/101-200_CPP/165_condition_variables/README.md)
