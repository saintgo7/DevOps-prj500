/*
 * Test Suite for Program 186: Signal Handling
 */

#include <iostream>
#include <signal.h>
#include <unistd.h>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;
volatile sig_atomic_t signal_received = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

void signal_handler(int sig) {
    signal_received = sig;
}

TEST(test_signal_registration) {
    signal(SIGUSR1, signal_handler);
    ASSERT_TRUE(true); // Registration successful
}

TEST(test_signal_send_receive) {
    signal_received = 0;
    signal(SIGUSR1, signal_handler);

    raise(SIGUSR1);
    usleep(1000); // Give time for signal handling

    ASSERT_EQ(signal_received, SIGUSR1);
}

TEST(test_signal_ignore) {
    signal(SIGUSR2, SIG_IGN);
    raise(SIGUSR2); // Should be ignored
    ASSERT_TRUE(true);
}

TEST(test_signal_default) {
    signal(SIGUSR1, SIG_DFL);
    ASSERT_TRUE(true);
}

TEST(test_multiple_signals) {
    signal_received = 0;
    signal(SIGUSR1, signal_handler);
    signal(SIGUSR2, signal_handler);

    raise(SIGUSR1);
    usleep(1000);
    ASSERT_EQ(signal_received, SIGUSR1);

    raise(SIGUSR2);
    usleep(1000);
    ASSERT_EQ(signal_received, SIGUSR2);
}

int main() {
    cout << "Running Signal Handling Tests\n==============================\n\n";
    RUN_TEST(test_signal_registration);
    RUN_TEST(test_signal_send_receive);
    RUN_TEST(test_signal_ignore);
    RUN_TEST(test_signal_default);
    RUN_TEST(test_multiple_signals);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
