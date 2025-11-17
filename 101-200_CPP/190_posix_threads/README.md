# Program 190: POSIX Threads

## Description
Explores POSIX threads (pthreads) API for low-level multithreading, providing comparison with std::thread and demonstrating pthread-specific features.

## Learning Objectives
- Create and manage pthreads
- Use pthread synchronization primitives
- Work with thread attributes
- Compare pthreads with std::thread
- Handle pthread-specific features

## Features
- pthread creation and joining
- pthread mutexes and condition variables
- Thread attributes
- Thread-local storage
- Thread cancellation
- Pthread barriers

## Compilation
```bash
g++ -std=c++17 main.cpp -o posix_threads -pthread
./posix_threads
```

## Key Concepts
```cpp
void* thread_func(void* arg) {
    // Thread code
    return nullptr;
}

pthread_t thread;
pthread_create(&thread, nullptr, thread_func, arg);
pthread_join(thread, nullptr);

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_lock(&mutex);
// Critical section
pthread_mutex_unlock(&mutex);
```

## Best Practices
1. Prefer std::thread for new code
2. Use pthreads for POSIX compatibility
3. Always check pthread function returns
4. Clean up thread resources
5. Use appropriate synchronization

## Navigation
- **Previous**: [189 - Memory Mapped Files](/home/user/DevOps-prj500/101-200_CPP/189_memory_mapped_files/README.md)
- **Next**: [191 - Epoll Select](/home/user/DevOps-prj500/101-200_CPP/191_epoll_select/README.md)
