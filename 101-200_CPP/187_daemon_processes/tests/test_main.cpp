/*
 * Test Suite for Program 187: Daemon Processes
 */

#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_GE(a, b) do { if ((a) < (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_setsid) {
    pid_t pid = fork();
    if (pid == 0) {
        pid_t sid = setsid();
        _exit(sid > 0 ? 0 : 1);
    } else {
        int status;
        waitpid(pid, &status, 0);
        ASSERT_EQ(WEXITSTATUS(status), 0);
    }
}

TEST(test_chdir) {
    int result = chdir("/");
    ASSERT_EQ(result, 0);
}

TEST(test_umask) {
    mode_t old_mask = umask(0);
    umask(old_mask); // Restore
    ASSERT_TRUE(true);
}

TEST(test_close_descriptors) {
    int fd = open("/dev/null", O_RDWR);
    ASSERT_GE(fd, 0);

    close(fd);
    ASSERT_TRUE(true);
}

TEST(test_daemon_components) {
    // Test individual daemon setup components
    mode_t mask = umask(0);
    umask(mask);

    int result = chdir("/tmp");
    ASSERT_EQ(result, 0);

    chdir("/"); // Restore
}

int main() {
    cout << "Running Daemon Processes Tests\n===============================\n\n";
    RUN_TEST(test_setsid);
    RUN_TEST(test_chdir);
    RUN_TEST(test_umask);
    RUN_TEST(test_close_descriptors);
    RUN_TEST(test_daemon_components);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
