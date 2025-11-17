/*
 * Test Suite for Program 183: Process Management
 */

#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_GE(a, b) do { if ((a) < (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_getpid) {
    pid_t pid = getpid();
    ASSERT_TRUE(pid > 0);
}

TEST(test_getppid) {
    pid_t ppid = getppid();
    ASSERT_TRUE(ppid > 0);
}

TEST(test_fork_basic) {
    pid_t pid = fork();
    if (pid == 0) {
        // Child process
        _exit(0);
    } else {
        // Parent process
        ASSERT_TRUE(pid > 0);
        int status;
        waitpid(pid, &status, 0);
        ASSERT_TRUE(WIFEXITED(status));
    }
}

TEST(test_fork_return_value) {
    pid_t pid = fork();
    if (pid == 0) {
        // Child: fork returns 0
        _exit(0);
    } else {
        // Parent: fork returns child PID
        ASSERT_TRUE(pid > 0);
        wait(NULL);
    }
}

TEST(test_process_exists) {
    pid_t pid = getpid();
    ASSERT_TRUE(pid > 0);
}

int main() {
    cout << "Running Process Management Tests\n=================================\n\n";
    RUN_TEST(test_getpid);
    RUN_TEST(test_getppid);
    RUN_TEST(test_fork_basic);
    RUN_TEST(test_fork_return_value);
    RUN_TEST(test_process_exists);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
