/*
 * Test Suite for Program 184: IPC Pipes
 */

#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
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

TEST(test_pipe_creation) {
    int pipefd[2];
    int result = pipe(pipefd);
    ASSERT_EQ(result, 0);
    close(pipefd[0]);
    close(pipefd[1]);
}

TEST(test_pipe_communication) {
    int pipefd[2];
    pipe(pipefd);

    const char* msg = "Hello";
    write(pipefd[1], msg, strlen(msg) + 1);

    char buffer[100];
    read(pipefd[0], buffer, sizeof(buffer));

    ASSERT_EQ(string(buffer), string(msg));

    close(pipefd[0]);
    close(pipefd[1]);
}

TEST(test_pipe_parent_child) {
    int pipefd[2];
    pipe(pipefd);

    pid_t pid = fork();
    if (pid == 0) {
        // Child writes
        close(pipefd[0]);
        const char* msg = "From child";
        write(pipefd[1], msg, strlen(msg) + 1);
        close(pipefd[1]);
        _exit(0);
    } else {
        // Parent reads
        close(pipefd[1]);
        char buffer[100];
        read(pipefd[0], buffer, sizeof(buffer));
        close(pipefd[0]);

        ASSERT_EQ(string(buffer), string("From child"));
        wait(NULL);
    }
}

TEST(test_pipe_bidirectional_setup) {
    int pipe1[2], pipe2[2];
    ASSERT_EQ(pipe(pipe1), 0);
    ASSERT_EQ(pipe(pipe2), 0);

    close(pipe1[0]);
    close(pipe1[1]);
    close(pipe2[0]);
    close(pipe2[1]);
}

int main() {
    cout << "Running IPC Pipes Tests\n=======================\n\n";
    RUN_TEST(test_pipe_creation);
    RUN_TEST(test_pipe_communication);
    RUN_TEST(test_pipe_parent_child);
    RUN_TEST(test_pipe_bidirectional_setup);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
