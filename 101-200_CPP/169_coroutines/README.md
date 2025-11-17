# Program 169: Coroutines

## Description
Introduces C++20 coroutines, a powerful feature for writing asynchronous code that looks synchronous, using co_await, co_yield, and co_return keywords.

## Learning Objectives
- Understand coroutine basics
- Use co_await, co_yield, and co_return
- Implement generators with coroutines
- Create awaitable types
- Design coroutine promise types

## Features
- Basic coroutine syntax
- Generator implementation
- Awaitable objects
- Promise types
- Coroutine handles
- Practical async examples

## Compilation
```bash
g++ -std=c++20 main.cpp -o coroutines
./coroutines
```

## Key Concepts
```cpp
generator<int> range(int start, int end) {
    for (int i = start; i < end; ++i)
        co_yield i;
}

task<int> async_task() {
    co_return 42;
}
```

## Best Practices
1. Understand the promise type contract
2. Manage coroutine lifetimes carefully
3. Use coroutines for async I/O
4. Leverage existing coroutine libraries
5. Be aware of compiler support differences

## Navigation
- **Previous**: [168 - Async Future](/home/user/DevOps-prj500/101-200_CPP/168_async_future/README.md)
- **Next**: [170 - Modules](/home/user/DevOps-prj500/101-200_CPP/170_modules/README.md)
