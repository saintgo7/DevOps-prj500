/*
 * Test Suite for Program 189: Memory Mapped Files
 */

#include <iostream>
#include <sys/mman.h>
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

TEST(test_mmap_file) {
    const char* filename = "/tmp/test_mmap.txt";
    int fd = open(filename, O_CREAT | O_RDWR | O_TRUNC, 0644);
    ASSERT_TRUE(fd >= 0);

    ftruncate(fd, 4096);

    void* ptr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    ASSERT_NE(ptr, MAP_FAILED);

    const char* msg = "Memory mapped!";
    strcpy((char*)ptr, msg);

    ASSERT_EQ(string((char*)ptr), string(msg));

    munmap(ptr, 4096);
    close(fd);
    unlink(filename);
}

TEST(test_mmap_anonymous) {
    void* ptr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    ASSERT_NE(ptr, MAP_FAILED);

    int* data = (int*)ptr;
    data[0] = 123;
    ASSERT_EQ(data[0], 123);

    munmap(ptr, 4096);
}

TEST(test_mmap_protection) {
    void* ptr = mmap(NULL, 4096, PROT_READ, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    ASSERT_NE(ptr, MAP_FAILED);

    munmap(ptr, 4096);
}

TEST(test_msync) {
    const char* filename = "/tmp/test_msync.txt";
    int fd = open(filename, O_CREAT | O_RDWR | O_TRUNC, 0644);
    ftruncate(fd, 4096);

    void* ptr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    ASSERT_NE(ptr, MAP_FAILED);

    strcpy((char*)ptr, "sync test");

    int result = msync(ptr, 4096, MS_SYNC);
    ASSERT_EQ(result, 0);

    munmap(ptr, 4096);
    close(fd);
    unlink(filename);
}

int main() {
    cout << "Running Memory Mapped Files Tests\n==================================\n\n";
    RUN_TEST(test_mmap_file);
    RUN_TEST(test_mmap_anonymous);
    RUN_TEST(test_mmap_protection);
    RUN_TEST(test_msync);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
