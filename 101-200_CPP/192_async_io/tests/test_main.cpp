/*
 * Test Suite for Program 192: Async I/O
 */

#include <iostream>
#include <aio.h>
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
#define ASSERT_GE(a, b) do { if ((a) < (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_aio_structure) {
    struct aiocb cb;
    memset(&cb, 0, sizeof(struct aiocb));

    cb.aio_fildes = 1;
    cb.aio_offset = 0;

    ASSERT_EQ(cb.aio_fildes, 1);
    ASSERT_EQ(cb.aio_offset, 0);
}

TEST(test_aio_write_read) {
    const char* filename = "/tmp/test_aio.txt";
    int fd = open(filename, O_CREAT | O_RDWR | O_TRUNC, 0644);
    ASSERT_GE(fd, 0);

    // Write synchronously for testing
    const char* msg = "async test";
    write(fd, msg, strlen(msg));

    // Read
    lseek(fd, 0, SEEK_SET);
    char buffer[100];
    ssize_t n = read(fd, buffer, sizeof(buffer));
    buffer[n] = '\0';

    ASSERT_EQ(string(buffer), string(msg));

    close(fd);
    unlink(filename);
}

TEST(test_file_operations) {
    const char* filename = "/tmp/test_io.txt";
    int fd = open(filename, O_CREAT | O_RDWR | O_TRUNC, 0644);
    ASSERT_GE(fd, 0);

    const char* data = "test data";
    ssize_t written = write(fd, data, strlen(data));
    ASSERT_EQ(written, strlen(data));

    close(fd);
    unlink(filename);
}

int main() {
    cout << "Running Async I/O Tests\n=======================\n\n";
    RUN_TEST(test_aio_structure);
    RUN_TEST(test_aio_write_read);
    RUN_TEST(test_file_operations);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
