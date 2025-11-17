/*
 * Program 190: POSIX Threads
 * Demonstrates pthread API, thread management, synchronization
 * Compile: g++ -std=c++17 -pthread -o posix_threads main.cpp
 */

#include <iostream>
#include <cstring>
#include <pthread.h>
#include <unistd.h>
#include <errno.h>
#include <vector>

// Thread function parameters
struct ThreadData {
    int thread_id;
    int iterations;
    std::string message;
};

// Global shared data for synchronization demos
int shared_counter = 0;
pthread_mutex_t counter_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t counter_cond = PTHREAD_COND_INITIALIZER;

// Simple thread function
void* simpleThreadFunction(void* arg) {
    ThreadData* data = static_cast<ThreadData*>(arg);

    std::cout << "Thread " << data->thread_id << " started" << std::endl;
    std::cout << "Thread " << data->thread_id << " message: "
              << data->message << std::endl;

    // Do some work
    for (int i = 0; i < data->iterations; ++i) {
        std::cout << "Thread " << data->thread_id << " iteration " << i << std::endl;
        sleep(1);
    }

    std::cout << "Thread " << data->thread_id << " finished" << std::endl;

    pthread_exit(nullptr);
}

void demonstrateBasicThreads() {
    std::cout << "\n=== Basic Thread Creation ===" << std::endl;

    pthread_t thread1, thread2;
    ThreadData data1 = {1, 2, "Hello from thread 1"};
    ThreadData data2 = {2, 2, "Hello from thread 2"};

    // Create threads
    std::cout << "Creating threads..." << std::endl;

    int result = pthread_create(&thread1, nullptr, simpleThreadFunction, &data1);
    if (result != 0) {
        std::cerr << "Failed to create thread 1: " << strerror(result) << std::endl;
        return;
    }

    result = pthread_create(&thread2, nullptr, simpleThreadFunction, &data2);
    if (result != 0) {
        std::cerr << "Failed to create thread 2: " << strerror(result) << std::endl;
        return;
    }

    std::cout << "Threads created, waiting for completion..." << std::endl;

    // Wait for threads to finish
    pthread_join(thread1, nullptr);
    std::cout << "Thread 1 joined" << std::endl;

    pthread_join(thread2, nullptr);
    std::cout << "Thread 2 joined" << std::endl;
}

// Thread function with return value
void* threadWithReturnValue(void* arg) {
    int* input = static_cast<int*>(arg);
    int* result = new int;

    *result = (*input) * 2;

    std::cout << "Thread computed: " << *input << " * 2 = " << *result << std::endl;

    pthread_exit(result);
}

void demonstrateThreadReturnValue() {
    std::cout << "\n=== Thread Return Values ===" << std::endl;

    pthread_t thread;
    int input = 42;

    pthread_create(&thread, nullptr, threadWithReturnValue, &input);

    void* return_value;
    pthread_join(thread, &return_value);

    int* result = static_cast<int*>(return_value);
    std::cout << "Main thread received result: " << *result << std::endl;

    delete result;
}

// Thread function using mutex
void* mutexThreadFunction(void* arg) {
    int thread_id = *static_cast<int*>(arg);

    for (int i = 0; i < 5; ++i) {
        // Lock mutex
        pthread_mutex_lock(&counter_mutex);

        int old_value = shared_counter;
        usleep(10000);  // Simulate some work
        shared_counter = old_value + 1;

        std::cout << "Thread " << thread_id << " incremented counter to "
                  << shared_counter << std::endl;

        // Unlock mutex
        pthread_mutex_unlock(&counter_mutex);

        usleep(5000);
    }

    pthread_exit(nullptr);
}

void demonstrateMutex() {
    std::cout << "\n=== Mutex Synchronization ===" << std::endl;

    const int NUM_THREADS = 3;
    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];

    shared_counter = 0;

    std::cout << "Creating " << NUM_THREADS << " threads with mutex..." << std::endl;

    for (int i = 0; i < NUM_THREADS; ++i) {
        thread_ids[i] = i + 1;
        pthread_create(&threads[i], nullptr, mutexThreadFunction, &thread_ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], nullptr);
    }

    std::cout << "Final counter value: " << shared_counter << std::endl;
    std::cout << "Expected: " << (NUM_THREADS * 5) << std::endl;
}

// Producer thread
void* producerThread(void* arg) {
    for (int i = 0; i < 5; ++i) {
        pthread_mutex_lock(&counter_mutex);

        shared_counter++;
        std::cout << "Producer: Produced item #" << shared_counter << std::endl;

        // Signal consumer
        pthread_cond_signal(&counter_cond);

        pthread_mutex_unlock(&counter_mutex);

        sleep(1);
    }

    pthread_exit(nullptr);
}

// Consumer thread
void* consumerThread(void* arg) {
    for (int i = 0; i < 5; ++i) {
        pthread_mutex_lock(&counter_mutex);

        // Wait for item to be available
        while (shared_counter == 0) {
            std::cout << "Consumer: Waiting for item..." << std::endl;
            pthread_cond_wait(&counter_cond, &counter_mutex);
        }

        std::cout << "Consumer: Consumed item #" << shared_counter << std::endl;
        shared_counter--;

        pthread_mutex_unlock(&counter_mutex);

        sleep(1);
    }

    pthread_exit(nullptr);
}

void demonstrateConditionVariable() {
    std::cout << "\n=== Condition Variables (Producer-Consumer) ===" << std::endl;

    pthread_t producer, consumer;
    shared_counter = 0;

    pthread_create(&producer, nullptr, producerThread, nullptr);
    pthread_create(&consumer, nullptr, consumerThread, nullptr);

    pthread_join(producer, nullptr);
    pthread_join(consumer, nullptr);

    std::cout << "Producer-Consumer complete" << std::endl;
}

void demonstrateThreadAttributes() {
    std::cout << "\n=== Thread Attributes ===" << std::endl;

    pthread_attr_t attr;
    pthread_t thread;

    // Initialize attributes
    pthread_attr_init(&attr);

    // Set detached state
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
    std::cout << "Set thread to joinable state" << std::endl;

    // Get stack size
    size_t stack_size;
    pthread_attr_getstacksize(&attr, &stack_size);
    std::cout << "Default stack size: " << stack_size << " bytes" << std::endl;

    // Set custom stack size
    size_t new_stack_size = 2 * 1024 * 1024;  // 2 MB
    pthread_attr_setstacksize(&attr, new_stack_size);
    std::cout << "Set stack size to: " << new_stack_size << " bytes" << std::endl;

    ThreadData data = {1, 2, "Thread with custom attributes"};

    // Create thread with attributes
    pthread_create(&thread, &attr, simpleThreadFunction, &data);

    pthread_join(thread, nullptr);

    // Clean up attributes
    pthread_attr_destroy(&attr);
}

void demonstrateDetachedThread() {
    std::cout << "\n=== Detached Threads ===" << std::endl;

    pthread_t thread;
    pthread_attr_t attr;

    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

    ThreadData data = {1, 2, "Detached thread"};

    pthread_create(&thread, &attr, simpleThreadFunction, &data);

    std::cout << "Detached thread created (cannot be joined)" << std::endl;
    std::cout << "Waiting for detached thread to complete..." << std::endl;

    sleep(3);  // Give thread time to finish

    pthread_attr_destroy(&attr);
}

pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;
int shared_data = 0;

void* readerThread(void* arg) {
    int thread_id = *static_cast<int*>(arg);

    for (int i = 0; i < 3; ++i) {
        pthread_rwlock_rdlock(&rwlock);

        std::cout << "Reader " << thread_id << " reads: " << shared_data << std::endl;

        pthread_rwlock_unlock(&rwlock);

        usleep(100000);
    }

    pthread_exit(nullptr);
}

void* writerThread(void* arg) {
    int thread_id = *static_cast<int*>(arg);

    for (int i = 0; i < 2; ++i) {
        pthread_rwlock_wrlock(&rwlock);

        shared_data++;
        std::cout << "Writer " << thread_id << " writes: " << shared_data << std::endl;

        pthread_rwlock_unlock(&rwlock);

        usleep(150000);
    }

    pthread_exit(nullptr);
}

void demonstrateReadWriteLock() {
    std::cout << "\n=== Read-Write Locks ===" << std::endl;

    const int NUM_READERS = 3;
    const int NUM_WRITERS = 2;

    pthread_t readers[NUM_READERS];
    pthread_t writers[NUM_WRITERS];
    int reader_ids[NUM_READERS];
    int writer_ids[NUM_WRITERS];

    shared_data = 0;

    // Create readers
    for (int i = 0; i < NUM_READERS; ++i) {
        reader_ids[i] = i + 1;
        pthread_create(&readers[i], nullptr, readerThread, &reader_ids[i]);
    }

    // Create writers
    for (int i = 0; i < NUM_WRITERS; ++i) {
        writer_ids[i] = i + 1;
        pthread_create(&writers[i], nullptr, writerThread, &writer_ids[i]);
    }

    // Join all threads
    for (int i = 0; i < NUM_READERS; ++i) {
        pthread_join(readers[i], nullptr);
    }

    for (int i = 0; i < NUM_WRITERS; ++i) {
        pthread_join(writers[i], nullptr);
    }

    std::cout << "Final shared_data value: " << shared_data << std::endl;
}

void demonstrateThreadSpecificData() {
    std::cout << "\n=== Thread-Specific Data ===" << std::endl;

    pthread_key_t key;

    // Create key for thread-specific data
    pthread_key_create(&key, nullptr);

    auto thread_func = [](void* arg) -> void* {
        pthread_key_t* key_ptr = static_cast<pthread_key_t*>(arg);
        int* thread_data = new int;

        // Each thread gets its own copy
        *thread_data = pthread_self() % 100;

        pthread_setspecific(*key_ptr, thread_data);

        std::cout << "Thread " << pthread_self() << " stored: "
                  << *thread_data << std::endl;

        sleep(1);

        // Retrieve thread-specific data
        int* retrieved = static_cast<int*>(pthread_getspecific(*key_ptr));
        std::cout << "Thread " << pthread_self() << " retrieved: "
                  << *retrieved << std::endl;

        delete retrieved;
        pthread_exit(nullptr);
    };

    const int NUM_THREADS = 3;
    pthread_t threads[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_create(&threads[i], nullptr,
                      [](void* arg) -> void* {
                          pthread_key_t* key_ptr = static_cast<pthread_key_t*>(arg);
                          int* thread_data = new int;
                          *thread_data = pthread_self() % 100;
                          pthread_setspecific(*key_ptr, thread_data);
                          std::cout << "Thread stored value" << std::endl;
                          sleep(1);
                          int* retrieved = static_cast<int*>(pthread_getspecific(*key_ptr));
                          std::cout << "Thread retrieved value" << std::endl;
                          delete retrieved;
                          pthread_exit(nullptr);
                      }, &key);
    }

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], nullptr);
    }

    pthread_key_delete(key);
}

void demonstrateThreadCancellation() {
    std::cout << "\n=== Thread Cancellation ===" << std::endl;

    auto cancelable_thread = [](void* arg) -> void* {
        pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, nullptr);
        pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, nullptr);

        std::cout << "Cancelable thread started" << std::endl;

        for (int i = 0; i < 10; ++i) {
            std::cout << "Thread working... " << i << std::endl;

            // Cancellation point
            pthread_testcancel();

            sleep(1);
        }

        std::cout << "Thread completed normally" << std::endl;
        pthread_exit(nullptr);
    };

    pthread_t thread;
    pthread_create(&thread, nullptr, cancelable_thread, nullptr);

    // Let thread run for a bit
    sleep(3);

    // Cancel thread
    std::cout << "Main: Canceling thread..." << std::endl;
    pthread_cancel(thread);

    void* result;
    pthread_join(thread, &result);

    if (result == PTHREAD_CANCELED) {
        std::cout << "Thread was canceled" << std::endl;
    } else {
        std::cout << "Thread completed normally" << std::endl;
    }
}

int main() {
    std::cout << "POSIX Threads Demonstration" << std::endl;
    std::cout << "============================" << std::endl;

    demonstrateBasicThreads();
    demonstrateThreadReturnValue();
    demonstrateMutex();
    demonstrateConditionVariable();
    demonstrateReadWriteLock();
    demonstrateThreadAttributes();
    demonstrateDetachedThread();
    demonstrateThreadSpecificData();
    demonstrateThreadCancellation();

    // Clean up
    pthread_mutex_destroy(&counter_mutex);
    pthread_cond_destroy(&counter_cond);
    pthread_rwlock_destroy(&rwlock);

    std::cout << "\n=== POSIX Threads Complete ===" << std::endl;

    return 0;
}
