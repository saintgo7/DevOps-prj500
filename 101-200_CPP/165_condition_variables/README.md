# Program 165: Condition Variables

## Description
Explores std::condition_variable for thread synchronization, enabling threads to wait for specific conditions and be notified when conditions are met, essential for producer-consumer patterns.

## Learning Objectives
- Use std::condition_variable for thread communication
- Implement wait, notify_one, and notify_all
- Create producer-consumer patterns
- Prevent spurious wakeups
- Understand predicate-based waiting

## Features
- Basic condition variable usage
- notify_one vs notify_all
- Producer-consumer implementation
- Spurious wakeup handling
- Predicate-based wait
- Timeout waiting

## Compilation
```bash
g++ -std=c++17 main.cpp -o condition_variables -pthread
./condition_variables
```

## Key Concepts
```cpp
std::condition_variable cv;
std::mutex mtx;

// Wait
std::unique_lock<std::mutex> lock(mtx);
cv.wait(lock, [](){ return ready; });

// Notify
cv.notify_one();
cv.notify_all();
```

## Best Practices
1. Always use predicate-based wait to avoid spurious wakeups
2. Hold lock when checking condition
3. Use unique_lock with condition variables
4. Consider notify_all vs notify_one carefully

## Navigation
- **Previous**: [164 - Mutex Locks](/home/user/DevOps-prj500/101-200_CPP/164_mutex_locks/README.md)
- **Next**: [166 - Atomics](/home/user/DevOps-prj500/101-200_CPP/166_atomics/README.md)
