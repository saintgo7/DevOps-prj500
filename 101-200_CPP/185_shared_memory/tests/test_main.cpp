/*
 * Test Suite for Program 185: Shared Memory
 */

#include <iostream>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstring>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_NE(a, b) do { if ((a) == (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_shm_open) {
    const char* name = "/test_shm";
    int fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    ASSERT_TRUE(fd >= 0);

    shm_unlink(name);
    close(fd);
}

TEST(test_shm_truncate) {
    const char* name = "/test_shm2";
    int fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    ASSERT_TRUE(fd >= 0);

    int result = ftruncate(fd, 4096);
    ASSERT_EQ(result, 0);

    shm_unlink(name);
    close(fd);
}

TEST(test_shm_write_read) {
    const char* name = "/test_shm3";
    int fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    ftruncate(fd, 4096);

    void* ptr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    ASSERT_NE(ptr, MAP_FAILED);

    const char* msg = "Hello, Shared Memory!";
    strcpy((char*)ptr, msg);

    ASSERT_EQ(string((char*)ptr), string(msg));

    munmap(ptr, 4096);
    shm_unlink(name);
    close(fd);
}

TEST(test_mmap_anonymous) {
    size_t size = 4096;
    void* ptr = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    ASSERT_NE(ptr, MAP_FAILED);

    int* data = (int*)ptr;
    data[0] = 42;
    ASSERT_EQ(data[0], 42);

    munmap(ptr, size);
}

int main() {
    cout << "Running Shared Memory Tests\n===========================\n\n";
    RUN_TEST(test_shm_open);
    RUN_TEST(test_shm_truncate);
    RUN_TEST(test_shm_write_read);
    RUN_TEST(test_mmap_anonymous);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
