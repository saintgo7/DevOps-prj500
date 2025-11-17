/*
 * Test Suite for Program 188: System Calls
 */

#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <cassert>
#include <cstring>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_GE(a, b) do { if ((a) < (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_open_close) {
    int fd = open("/dev/null", O_RDWR);
    ASSERT_GE(fd, 0);

    int result = close(fd);
    ASSERT_EQ(result, 0);
}

TEST(test_read_write) {
    const char* filename = "/tmp/test_syscall.txt";
    int fd = open(filename, O_CREAT | O_RDWR | O_TRUNC, 0644);
    ASSERT_GE(fd, 0);

    const char* msg = "Hello";
    ssize_t written = write(fd, msg, strlen(msg));
    ASSERT_EQ(written, strlen(msg));

    lseek(fd, 0, SEEK_SET);

    char buffer[100];
    ssize_t bytes_read = read(fd, buffer, sizeof(buffer));
    buffer[bytes_read] = '\0';

    ASSERT_EQ(string(buffer), string(msg));

    close(fd);
    unlink(filename);
}

TEST(test_stat) {
    struct stat st;
    int result = stat("/", &st);
    ASSERT_EQ(result, 0);
    ASSERT_TRUE(S_ISDIR(st.st_mode));
}

TEST(test_getpid_syscall) {
    pid_t pid = getpid();
    ASSERT_TRUE(pid > 0);
}

TEST(test_access) {
    int result = access("/", F_OK);
    ASSERT_EQ(result, 0);
}

int main() {
    cout << "Running System Calls Tests\n==========================\n\n";
    RUN_TEST(test_open_close);
    RUN_TEST(test_read_write);
    RUN_TEST(test_stat);
    RUN_TEST(test_getpid_syscall);
    RUN_TEST(test_access);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
