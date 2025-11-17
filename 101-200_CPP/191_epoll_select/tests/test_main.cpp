/*
 * Test Suite for Program 191: Epoll and Select
 */

#include <iostream>
#include <sys/select.h>
#include <sys/epoll.h>
#include <unistd.h>
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

TEST(test_select_setup) {
    fd_set readfds;
    FD_ZERO(&readfds);
    FD_SET(0, &readfds);

    ASSERT_TRUE(FD_ISSET(0, &readfds));
}

TEST(test_select_timeout) {
    fd_set readfds;
    FD_ZERO(&readfds);

    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 1000; // 1ms timeout

    int result = select(1, &readfds, NULL, NULL, &tv);
    ASSERT_GE(result, 0);
}

TEST(test_epoll_create) {
    int epfd = epoll_create1(0);
    ASSERT_GE(epfd, 0);
    close(epfd);
}

TEST(test_epoll_ctl) {
    int epfd = epoll_create1(0);
    ASSERT_GE(epfd, 0);

    int pipefd[2];
    pipe(pipefd);

    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.fd = pipefd[0];

    int result = epoll_ctl(epfd, EPOLL_CTL_ADD, pipefd[0], &ev);
    ASSERT_EQ(result, 0);

    close(pipefd[0]);
    close(pipefd[1]);
    close(epfd);
}

TEST(test_fd_operations) {
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(1, &fds);
    ASSERT_TRUE(FD_ISSET(1, &fds));

    FD_CLR(1, &fds);
    ASSERT_TRUE(!FD_ISSET(1, &fds));
}

int main() {
    cout << "Running Epoll and Select Tests\n===============================\n\n";
    RUN_TEST(test_select_setup);
    RUN_TEST(test_select_timeout);
    RUN_TEST(test_epoll_create);
    RUN_TEST(test_epoll_ctl);
    RUN_TEST(test_fd_operations);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
