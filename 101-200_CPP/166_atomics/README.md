# Program 166: Atomics

## Description
Demonstrates std::atomic for lock-free programming, providing atomic operations on variables that can be safely accessed from multiple threads without mutexes.

## Learning Objectives
- Use std::atomic for lock-free data structures
- Understand memory ordering
- Apply compare-and-swap operations
- Implement spin locks
- Distinguish between different memory orderings

## Features
- Basic atomic operations
- Atomic load/store
- Compare-and-swap (CAS)
- Memory ordering (relaxed, acquire, release, seq_cst)
- Atomic flags
- Lock-free counters

## Compilation
```bash
g++ -std=c++17 main.cpp -o atomics -pthread
./atomics
```

## Key Concepts
```cpp
std::atomic<int> counter(0);
counter.fetch_add(1, std::memory_order_relaxed);
counter++;  // Equivalent to seq_cst

int expected = 5;
counter.compare_exchange_strong(expected, 10);
```

## Best Practices
1. Use std::atomic for simple lock-free operations
2. Understand memory ordering implications
3. Default to sequential consistency unless you know otherwise
4. Prefer mutexes for complex synchronization
5. Profile to ensure atomics provide actual benefit

## Navigation
- **Previous**: [165 - Condition Variables](/home/user/DevOps-prj500/101-200_CPP/165_condition_variables/README.md)
- **Next**: [167 - Thread Pool](/home/user/DevOps-prj500/101-200_CPP/167_thread_pool/README.md)
