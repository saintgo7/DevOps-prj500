/*
 * Program 183: Process Management
 * Demonstrates fork, exec, process control, and inter-process operations
 * Compile: g++ -std=c++17 -o process_management main.cpp
 */

#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <signal.h>
#include <errno.h>

void demonstrateFork() {
    std::cout << "\n=== Fork Demonstration ===" << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed: " << strerror(errno) << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process
        std::cout << "Child process:" << std::endl;
        std::cout << "  PID: " << getpid() << std::endl;
        std::cout << "  Parent PID: " << getppid() << std::endl;
        std::cout << "  Child executing task..." << std::endl;

        // Simulate some work
        sleep(1);
        std::cout << "  Child task complete!" << std::endl;
        exit(0);
    } else {
        // Parent process
        std::cout << "Parent process:" << std::endl;
        std::cout << "  PID: " << getpid() << std::endl;
        std::cout << "  Created child with PID: " << pid << std::endl;

        // Wait for child
        int status;
        pid_t waited_pid = wait(&status);

        std::cout << "  Child process " << waited_pid << " terminated" << std::endl;
        if (WIFEXITED(status)) {
            std::cout << "  Exit status: " << WEXITSTATUS(status) << std::endl;
        }
    }
}

void demonstrateMultipleForks() {
    std::cout << "\n=== Multiple Fork Demonstration ===" << std::endl;

    const int NUM_CHILDREN = 3;
    std::vector<pid_t> children;

    std::cout << "Parent (PID " << getpid() << ") creating " << NUM_CHILDREN
              << " child processes" << std::endl;

    for (int i = 0; i < NUM_CHILDREN; ++i) {
        pid_t pid = fork();

        if (pid < 0) {
            std::cerr << "Fork failed" << std::endl;
            continue;
        }

        if (pid == 0) {
            // Child process
            std::cout << "Child " << i << " (PID " << getpid() << ") started" << std::endl;

            // Each child does different amount of work
            sleep(i + 1);

            std::cout << "Child " << i << " (PID " << getpid() << ") finished" << std::endl;
            exit(i);
        } else {
            // Parent process
            children.push_back(pid);
        }
    }

    // Parent waits for all children
    std::cout << "\nParent waiting for all children..." << std::endl;

    for (size_t i = 0; i < children.size(); ++i) {
        int status;
        pid_t pid = wait(&status);

        if (pid > 0) {
            std::cout << "Child PID " << pid << " terminated with status ";
            if (WIFEXITED(status)) {
                std::cout << WEXITSTATUS(status) << std::endl;
            }
        }
    }

    std::cout << "All children terminated" << std::endl;
}

void demonstrateExec() {
    std::cout << "\n=== Exec Demonstration ===" << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process - execute 'ls' command
        std::cout << "Child: Executing 'ls -l' command..." << std::endl;

        // Using execl to execute ls
        char* args[] = {(char*)"ls", (char*)"-l", (char*)"/tmp", nullptr};
        execvp("ls", args);

        // If exec fails, we'll reach here
        std::cerr << "Exec failed: " << strerror(errno) << std::endl;
        exit(1);
    } else {
        // Parent process
        int status;
        waitpid(pid, &status, 0);

        std::cout << "\nParent: Child process completed" << std::endl;
        if (WIFEXITED(status)) {
            std::cout << "Exit status: " << WEXITSTATUS(status) << std::endl;
        }
    }
}

void demonstrateProcessInfo() {
    std::cout << "\n=== Process Information ===" << std::endl;

    std::cout << "Current Process ID (PID): " << getpid() << std::endl;
    std::cout << "Parent Process ID (PPID): " << getppid() << std::endl;
    std::cout << "User ID (UID): " << getuid() << std::endl;
    std::cout << "Effective User ID (EUID): " << geteuid() << std::endl;
    std::cout << "Group ID (GID): " << getgid() << std::endl;
    std::cout << "Effective Group ID (EGID): " << getegid() << std::endl;

    // Process group
    std::cout << "Process Group ID: " << getpgrp() << std::endl;

    // Session ID
    std::cout << "Session ID: " << getsid(0) << std::endl;
}

void demonstrateResourceLimits() {
    std::cout << "\n=== Resource Limits Demonstration ===" << std::endl;

    struct rlimit limit;

    // Get CPU time limit
    if (getrlimit(RLIMIT_CPU, &limit) == 0) {
        std::cout << "CPU Time Limit:" << std::endl;
        std::cout << "  Soft: " << (limit.rlim_cur == RLIM_INFINITY ? "unlimited" :
                                   std::to_string(limit.rlim_cur)) << std::endl;
        std::cout << "  Hard: " << (limit.rlim_max == RLIM_INFINITY ? "unlimited" :
                                   std::to_string(limit.rlim_max)) << std::endl;
    }

    // Get file size limit
    if (getrlimit(RLIMIT_FSIZE, &limit) == 0) {
        std::cout << "\nFile Size Limit:" << std::endl;
        std::cout << "  Soft: " << (limit.rlim_cur == RLIM_INFINITY ? "unlimited" :
                                   std::to_string(limit.rlim_cur)) << std::endl;
        std::cout << "  Hard: " << (limit.rlim_max == RLIM_INFINITY ? "unlimited" :
                                   std::to_string(limit.rlim_max)) << std::endl;
    }

    // Get number of open files limit
    if (getrlimit(RLIMIT_NOFILE, &limit) == 0) {
        std::cout << "\nOpen Files Limit:" << std::endl;
        std::cout << "  Soft: " << limit.rlim_cur << std::endl;
        std::cout << "  Hard: " << limit.rlim_max << std::endl;
    }

    // Get stack size limit
    if (getrlimit(RLIMIT_STACK, &limit) == 0) {
        std::cout << "\nStack Size Limit:" << std::endl;
        std::cout << "  Soft: " << (limit.rlim_cur == RLIM_INFINITY ? "unlimited" :
                                   std::to_string(limit.rlim_cur) + " bytes") << std::endl;
        std::cout << "  Hard: " << (limit.rlim_max == RLIM_INFINITY ? "unlimited" :
                                   std::to_string(limit.rlim_max) + " bytes") << std::endl;
    }

    // Try to set a limit (demonstration only)
    limit.rlim_cur = 1024;
    limit.rlim_max = 2048;

    std::cout << "\nAttempting to set custom limit (may require privileges)..." << std::endl;
    if (setrlimit(RLIMIT_NOFILE, &limit) == 0) {
        std::cout << "Successfully set open files limit" << std::endl;

        // Verify the change
        getrlimit(RLIMIT_NOFILE, &limit);
        std::cout << "New soft limit: " << limit.rlim_cur << std::endl;
    } else {
        std::cout << "Failed to set limit: " << strerror(errno) << std::endl;
    }
}

void demonstrateProcessControl() {
    std::cout << "\n=== Process Control Demonstration ===" << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process
        std::cout << "Child: Running and waiting for signals..." << std::endl;

        for (int i = 0; i < 10; ++i) {
            std::cout << "Child: Working... " << i << std::endl;
            sleep(1);
        }

        std::cout << "Child: Completed normally" << std::endl;
        exit(0);
    } else {
        // Parent process
        std::cout << "Parent: Created child " << pid << std::endl;

        // Let child run for a bit
        sleep(3);

        // Send SIGSTOP to pause child
        std::cout << "Parent: Stopping child..." << std::endl;
        kill(pid, SIGSTOP);

        sleep(2);

        // Send SIGCONT to resume child
        std::cout << "Parent: Resuming child..." << std::endl;
        kill(pid, SIGCONT);

        sleep(2);

        // Terminate child
        std::cout << "Parent: Terminating child..." << std::endl;
        kill(pid, SIGTERM);

        // Wait for child
        int status;
        waitpid(pid, &status, 0);

        std::cout << "Parent: Child terminated" << std::endl;
        if (WIFSIGNALED(status)) {
            std::cout << "Terminated by signal: " << WTERMSIG(status) << std::endl;
        }
    }
}

void demonstrateZombieProcess() {
    std::cout << "\n=== Zombie Process Demonstration ===" << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process exits immediately
        std::cout << "Child: Exiting immediately (will become zombie)" << std::endl;
        exit(42);
    } else {
        // Parent doesn't wait immediately - child becomes zombie
        std::cout << "Parent: Child created but not waiting yet" << std::endl;
        std::cout << "Child PID " << pid << " is now a zombie process" << std::endl;

        sleep(2);

        // Now clean up the zombie
        std::cout << "Parent: Cleaning up zombie process" << std::endl;
        int status;
        waitpid(pid, &status, 0);

        if (WIFEXITED(status)) {
            std::cout << "Zombie cleaned up. Exit status was: "
                     << WEXITSTATUS(status) << std::endl;
        }
    }
}

void demonstrateOrphanProcess() {
    std::cout << "\n=== Orphan Process Demonstration ===" << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process
        std::cout << "Child: Initial parent PID: " << getppid() << std::endl;

        // Wait for parent to exit
        sleep(2);

        std::cout << "Child: New parent PID (should be 1 or init): "
                 << getppid() << std::endl;

        sleep(1);
        std::cout << "Child: Exiting" << std::endl;
        exit(0);
    } else {
        // Parent exits quickly, making child an orphan
        std::cout << "Parent: Created child " << pid << " and exiting immediately" << std::endl;
        std::cout << "Parent: Child will become orphan and be adopted by init" << std::endl;
        // Parent exits without waiting
    }
}

int main() {
    std::cout << "Process Management Demonstration" << std::endl;
    std::cout << "================================" << std::endl;

    demonstrateProcessInfo();
    demonstrateFork();
    demonstrateMultipleForks();
    demonstrateExec();
    demonstrateResourceLimits();
    demonstrateProcessControl();
    demonstrateZombieProcess();

    // Note: demonstrateOrphanProcess() is commented out as it causes parent to exit
    // Uncomment to see orphan process behavior
    // demonstrateOrphanProcess();

    std::cout << "\n=== Process Management Complete ===" << std::endl;

    return 0;
}
