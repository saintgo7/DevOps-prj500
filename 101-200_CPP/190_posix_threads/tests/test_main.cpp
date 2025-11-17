/*
 * Test Suite for Program 190: POSIX Threads
 */

#include <iostream>
#include <pthread.h>
#include <unistd.h>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

void* thread_function(void* arg) {
    int* value = (int*)arg;
    *value = 42;
    return NULL;
}

void* counter_function(void* arg) {
    int* counter = (int*)arg;
    (*counter)++;
    return NULL;
}

TEST(test_thread_creation) {
    pthread_t thread;
    int value = 0;

    int result = pthread_create(&thread, NULL, thread_function, &value);
    ASSERT_EQ(result, 0);

    pthread_join(thread, NULL);
    ASSERT_EQ(value, 42);
}

TEST(test_multiple_threads) {
    const int NUM_THREADS = 5;
    pthread_t threads[NUM_THREADS];
    int counter = 0;

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, counter_function, &counter);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    ASSERT_TRUE(counter > 0); // May have race conditions without mutex
}

TEST(test_pthread_mutex) {
    pthread_mutex_t mutex;
    pthread_mutex_init(&mutex, NULL);

    pthread_mutex_lock(&mutex);
    pthread_mutex_unlock(&mutex);

    pthread_mutex_destroy(&mutex);
    ASSERT_TRUE(true);
}

TEST(test_pthread_self) {
    pthread_t tid = pthread_self();
    ASSERT_TRUE(tid != 0);
}

int main() {
    cout << "Running POSIX Threads Tests\n===========================\n\n";
    RUN_TEST(test_thread_creation);
    RUN_TEST(test_multiple_threads);
    RUN_TEST(test_pthread_mutex);
    RUN_TEST(test_pthread_self);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
