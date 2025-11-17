/*
 * Program 186: Signal Handling
 * Demonstrates signal handlers, SIGINT, SIGTERM, and signal masking
 * Compile: g++ -std=c++17 -o signal_handling main.cpp
 */

#include <iostream>
#include <csignal>
#include <cstring>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <atomic>

// Atomic flag for signal-safe communication
std::atomic<bool> signal_received(false);
std::atomic<int> signal_count(0);

// Signal handler for SIGINT (Ctrl+C)
void sigint_handler(int signum) {
    // Note: Only async-signal-safe functions should be called here
    const char* msg = "\nSIGINT received! (Ctrl+C pressed)\n";
    write(STDOUT_FILENO, msg, strlen(msg));
    signal_received = true;
}

// Signal handler for SIGTERM
void sigterm_handler(int signum) {
    const char* msg = "\nSIGTERM received! Graceful shutdown requested.\n";
    write(STDOUT_FILENO, msg, strlen(msg));
    signal_received = true;
}

// Signal handler with counter
void counting_handler(int signum) {
    signal_count++;
    const char* msg = "Signal received (count incremented)\n";
    write(STDOUT_FILENO, msg, strlen(msg));
}

// Advanced signal handler with sigaction
void advanced_handler(int signum, siginfo_t* info, void* context) {
    char buffer[256];
    int len = snprintf(buffer, sizeof(buffer),
                      "\nAdvanced handler: Signal %d from process %d\n",
                      signum, info->si_pid);
    write(STDOUT_FILENO, buffer, len);
}

void demonstrateBasicSignalHandling() {
    std::cout << "\n=== Basic Signal Handling ===" << std::endl;
    std::cout << "Process ID: " << getpid() << std::endl;

    // Install signal handler for SIGINT
    signal(SIGINT, sigint_handler);

    std::cout << "SIGINT handler installed" << std::endl;
    std::cout << "Waiting for signals... (Press Ctrl+C or wait 3 seconds)" << std::endl;

    signal_received = false;

    // Wait for signal or timeout
    for (int i = 0; i < 3 && !signal_received; ++i) {
        std::cout << "Waiting... " << (3 - i) << std::endl;
        sleep(1);
    }

    if (signal_received) {
        std::cout << "Signal was received and handled!" << std::endl;
    } else {
        std::cout << "No signal received within timeout" << std::endl;
    }

    // Restore default handler
    signal(SIGINT, SIG_DFL);
}

void demonstrateMultipleSignals() {
    std::cout << "\n=== Multiple Signal Handlers ===" << std::endl;

    // Install handlers for multiple signals
    signal(SIGINT, counting_handler);
    signal(SIGTERM, counting_handler);
    signal(SIGUSR1, counting_handler);

    std::cout << "Handlers installed for SIGINT, SIGTERM, and SIGUSR1" << std::endl;
    std::cout << "Sending signals to self..." << std::endl;

    signal_count = 0;
    pid_t pid = getpid();

    // Send signals to ourselves
    kill(pid, SIGUSR1);
    sleep(1);

    kill(pid, SIGUSR1);
    sleep(1);

    std::cout << "Total signals received: " << signal_count << std::endl;

    // Restore defaults
    signal(SIGINT, SIG_DFL);
    signal(SIGTERM, SIG_DFL);
    signal(SIGUSR1, SIG_DFL);
}

void demonstrateSigaction() {
    std::cout << "\n=== Sigaction (Advanced Signal Handling) ===" << std::endl;

    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));

    // Set up sigaction structure
    sa.sa_sigaction = advanced_handler;
    sa.sa_flags = SA_SIGINFO;  // Use sa_sigaction instead of sa_handler
    sigemptyset(&sa.sa_mask);

    // Install handler
    if (sigaction(SIGUSR1, &sa, nullptr) == -1) {
        std::cerr << "Failed to install sigaction handler" << std::endl;
        return;
    }

    std::cout << "Advanced handler installed for SIGUSR1" << std::endl;

    // Send signal
    pid_t pid = getpid();
    std::cout << "Sending SIGUSR1 to self (PID " << pid << ")..." << std::endl;
    kill(pid, SIGUSR1);

    sleep(1);

    // Restore default
    signal(SIGUSR1, SIG_DFL);
}

void demonstrateSignalMasking() {
    std::cout << "\n=== Signal Masking ===" << std::endl;

    sigset_t mask, oldmask;

    // Initialize signal sets
    sigemptyset(&mask);
    sigemptyset(&oldmask);

    // Add SIGUSR1 to the mask
    sigaddset(&mask, SIGUSR1);

    std::cout << "Blocking SIGUSR1..." << std::endl;

    // Block SIGUSR1
    if (sigprocmask(SIG_BLOCK, &mask, &oldmask) == -1) {
        std::cerr << "Failed to block signal" << std::endl;
        return;
    }

    signal(SIGUSR1, counting_handler);
    signal_count = 0;

    // Send signal while blocked
    std::cout << "Sending SIGUSR1 while blocked..." << std::endl;
    kill(getpid(), SIGUSR1);

    sleep(1);

    std::cout << "Signals received while blocked: " << signal_count << std::endl;

    // Unblock signal
    std::cout << "Unblocking SIGUSR1..." << std::endl;
    sigprocmask(SIG_UNBLOCK, &mask, nullptr);

    sleep(1);

    std::cout << "Signals received after unblocking: " << signal_count << std::endl;

    // Check pending signals
    sigset_t pending;
    sigpending(&pending);

    if (sigismember(&pending, SIGUSR1)) {
        std::cout << "SIGUSR1 is pending" << std::endl;
    } else {
        std::cout << "No SIGUSR1 pending" << std::endl;
    }

    signal(SIGUSR1, SIG_DFL);
}

void demonstrateChildSignals() {
    std::cout << "\n=== Child Process Signals ===" << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process
        signal(SIGUSR1, counting_handler);
        signal_count = 0;

        std::cout << "Child (PID " << getpid() << "): Waiting for signals..." << std::endl;

        // Wait for signals
        for (int i = 0; i < 5; ++i) {
            sleep(1);
        }

        std::cout << "Child: Received " << signal_count << " signals" << std::endl;
        exit(0);
    } else {
        // Parent process
        std::cout << "Parent: Created child with PID " << pid << std::endl;

        sleep(1);

        // Send signals to child
        for (int i = 0; i < 3; ++i) {
            std::cout << "Parent: Sending SIGUSR1 to child..." << std::endl;
            kill(pid, SIGUSR1);
            sleep(1);
        }

        // Wait for child to finish
        int status;
        waitpid(pid, &status, 0);

        std::cout << "Parent: Child terminated" << std::endl;
    }
}

void demonstrateAlarmSignal() {
    std::cout << "\n=== SIGALRM (Alarm Signal) ===" << std::endl;

    // Handler for SIGALRM
    signal(SIGALRM, [](int signum) {
        const char* msg = "\nAlarm triggered!\n";
        write(STDOUT_FILENO, msg, strlen(msg));
    });

    std::cout << "Setting alarm for 2 seconds..." << std::endl;
    alarm(2);

    std::cout << "Waiting for alarm..." << std::endl;

    // Pause until signal is received
    for (int i = 0; i < 3; ++i) {
        sleep(1);
        std::cout << "..." << std::endl;
    }

    std::cout << "Alarm demonstration complete" << std::endl;

    // Cancel any pending alarm
    alarm(0);
    signal(SIGALRM, SIG_DFL);
}

void demonstrateSignalSets() {
    std::cout << "\n=== Signal Sets Operations ===" << std::endl;

    sigset_t set1, set2, result;

    // Initialize empty sets
    sigemptyset(&set1);
    sigemptyset(&set2);

    // Add signals to set1
    sigaddset(&set1, SIGINT);
    sigaddset(&set1, SIGTERM);
    sigaddset(&set1, SIGUSR1);

    std::cout << "Set1 contains: SIGINT, SIGTERM, SIGUSR1" << std::endl;

    // Add signals to set2
    sigaddset(&set2, SIGTERM);
    sigaddset(&set2, SIGUSR1);
    sigaddset(&set2, SIGUSR2);

    std::cout << "Set2 contains: SIGTERM, SIGUSR1, SIGUSR2" << std::endl;

    // Check membership
    std::cout << "\nChecking membership in Set1:" << std::endl;
    std::cout << "  SIGINT: " << (sigismember(&set1, SIGINT) ? "yes" : "no") << std::endl;
    std::cout << "  SIGTERM: " << (sigismember(&set1, SIGTERM) ? "yes" : "no") << std::endl;
    std::cout << "  SIGUSR2: " << (sigismember(&set1, SIGUSR2) ? "yes" : "no") << std::endl;

    // Fill set (all signals)
    sigfillset(&result);
    std::cout << "\nFilled set with all signals" << std::endl;

    // Delete a signal
    sigdelset(&result, SIGKILL);
    std::cout << "Deleted SIGKILL from filled set" << std::endl;
}

void demonstrateIgnoreSignal() {
    std::cout << "\n=== Ignoring Signals ===" << std::endl;

    // Ignore SIGUSR1
    signal(SIGUSR1, SIG_IGN);

    std::cout << "SIGUSR1 set to be ignored" << std::endl;
    std::cout << "Sending SIGUSR1..." << std::endl;

    kill(getpid(), SIGUSR1);

    sleep(1);

    std::cout << "Signal was ignored (no handler called)" << std::endl;

    // Restore default
    signal(SIGUSR1, SIG_DFL);
}

int main() {
    std::cout << "Signal Handling Demonstration" << std::endl;
    std::cout << "==============================" << std::endl;
    std::cout << "\nNote: Some demonstrations wait for signals" << std::endl;
    std::cout << "You can press Ctrl+C during the first demo to trigger SIGINT" << std::endl;

    demonstrateBasicSignalHandling();
    demonstrateMultipleSignals();
    demonstrateSigaction();
    demonstrateSignalMasking();
    demonstrateSignalSets();
    demonstrateIgnoreSignal();
    demonstrateAlarmSignal();
    demonstrateChildSignals();

    std::cout << "\n=== Signal Handling Complete ===" << std::endl;

    return 0;
}
