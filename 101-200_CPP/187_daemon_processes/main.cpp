/*
 * Program 187: Daemon Processes
 * Demonstrates creating daemons and background processes
 * Compile: g++ -std=c++17 -o daemon_processes main.cpp
 */

#include <iostream>
#include <fstream>
#include <cstring>
#include <ctime>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <syslog.h>
#include <errno.h>

const char* DAEMON_LOG_FILE = "/tmp/daemon_test.log";
const char* DAEMON_PID_FILE = "/tmp/daemon_test.pid";

// Write to log file
void writeLog(const std::string& message) {
    std::ofstream log(DAEMON_LOG_FILE, std::ios::app);
    if (log.is_open()) {
        time_t now = time(nullptr);
        char* time_str = ctime(&now);
        time_str[strlen(time_str) - 1] = '\0';  // Remove newline

        log << "[" << time_str << "] " << message << std::endl;
        log.close();
    }
}

// Signal handler for daemon
void daemon_signal_handler(int signum) {
    if (signum == SIGTERM || signum == SIGINT) {
        writeLog("Received termination signal, shutting down...");
        unlink(DAEMON_PID_FILE);
        exit(0);
    } else if (signum == SIGHUP) {
        writeLog("Received SIGHUP, reloading configuration...");
    }
}

// Create a daemon process using traditional method
pid_t createDaemon() {
    pid_t pid, sid;

    // Fork the parent process
    pid = fork();

    if (pid < 0) {
        return -1;  // Fork failed
    }

    if (pid > 0) {
        return pid;  // Return child PID to parent
    }

    // Child continues here

    // Create new session and become session leader
    sid = setsid();
    if (sid < 0) {
        exit(EXIT_FAILURE);
    }

    // Change working directory to root
    if (chdir("/") < 0) {
        exit(EXIT_FAILURE);
    }

    // Close standard file descriptors
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    // Redirect standard file descriptors to /dev/null
    int fd = open("/dev/null", O_RDWR);
    dup2(fd, STDIN_FILENO);
    dup2(fd, STDOUT_FILENO);
    dup2(fd, STDERR_FILENO);
    if (fd > 2) {
        close(fd);
    }

    return 0;  // Success (child process)
}

// Write PID file
bool writePidFile(const char* filename) {
    std::ofstream pidfile(filename);
    if (!pidfile.is_open()) {
        return false;
    }

    pidfile << getpid() << std::endl;
    pidfile.close();
    return true;
}

// Read PID from file
pid_t readPidFile(const char* filename) {
    std::ifstream pidfile(filename);
    if (!pidfile.is_open()) {
        return -1;
    }

    pid_t pid;
    pidfile >> pid;
    pidfile.close();
    return pid;
}

// Simple daemon that runs for a short time
void runSimpleDaemon(int duration) {
    // Set up signal handlers
    signal(SIGTERM, daemon_signal_handler);
    signal(SIGINT, daemon_signal_handler);
    signal(SIGHUP, daemon_signal_handler);

    // Write PID file
    if (!writePidFile(DAEMON_PID_FILE)) {
        exit(EXIT_FAILURE);
    }

    writeLog("Daemon started");
    writeLog("PID: " + std::to_string(getpid()));

    // Daemon main loop
    int count = 0;
    while (count < duration) {
        writeLog("Daemon is running... iteration " + std::to_string(count + 1));

        sleep(1);
        count++;
    }

    writeLog("Daemon completed normally");

    // Clean up
    unlink(DAEMON_PID_FILE);
}

void demonstrateSimpleDaemon() {
    std::cout << "\n=== Simple Daemon Demonstration ===" << std::endl;

    // Clear old log
    std::ofstream log(DAEMON_LOG_FILE, std::ios::trunc);
    log.close();

    std::cout << "Creating daemon process..." << std::endl;

    pid_t daemon_pid = createDaemon();

    if (daemon_pid < 0) {
        std::cerr << "Failed to create daemon" << std::endl;
        return;
    }

    if (daemon_pid > 0) {
        // Parent process
        std::cout << "Daemon created with PID: " << daemon_pid << std::endl;
        std::cout << "Log file: " << DAEMON_LOG_FILE << std::endl;

        // Give daemon time to start
        sleep(1);

        // Read and display log
        std::cout << "\nDaemon log (first 3 seconds):" << std::endl;
        std::cout << "----------------------------" << std::endl;

        for (int i = 0; i < 3; ++i) {
            sleep(1);

            std::ifstream log(DAEMON_LOG_FILE);
            if (log.is_open()) {
                std::string line;
                while (std::getline(log, line)) {
                    // Only print new lines (simple approach)
                }
                log.close();
            }
        }

        // Read final log
        std::ifstream log(DAEMON_LOG_FILE);
        if (log.is_open()) {
            std::string line;
            while (std::getline(log, line)) {
                std::cout << line << std::endl;
            }
            log.close();
        }

        std::cout << "----------------------------" << std::endl;

    } else {
        // Child (daemon) process
        runSimpleDaemon(5);
        exit(0);
    }
}

void demonstrateDaemonControl() {
    std::cout << "\n=== Daemon Control Demonstration ===" << std::endl;

    // Check if daemon is running
    pid_t daemon_pid = readPidFile(DAEMON_PID_FILE);

    if (daemon_pid > 0) {
        std::cout << "Found daemon PID: " << daemon_pid << std::endl;

        // Check if process exists
        if (kill(daemon_pid, 0) == 0) {
            std::cout << "Daemon is running" << std::endl;

            // Send SIGHUP to reload
            std::cout << "Sending SIGHUP (reload signal)..." << std::endl;
            kill(daemon_pid, SIGHUP);

            sleep(1);

            // Send SIGTERM to terminate
            std::cout << "Sending SIGTERM (terminate signal)..." << std::endl;
            kill(daemon_pid, SIGTERM);

            sleep(1);

            std::cout << "Daemon terminated" << std::endl;
        } else {
            std::cout << "PID file exists but daemon is not running" << std::endl;
            unlink(DAEMON_PID_FILE);
        }
    } else {
        std::cout << "No daemon PID file found" << std::endl;
    }
}

void demonstrateSyslog() {
    std::cout << "\n=== Syslog Demonstration ===" << std::endl;

    // Open syslog
    openlog("daemon_demo", LOG_PID | LOG_CONS, LOG_USER);

    std::cout << "Writing messages to syslog..." << std::endl;

    // Write messages at different priority levels
    syslog(LOG_INFO, "Daemon demonstration: INFO message");
    syslog(LOG_WARNING, "Daemon demonstration: WARNING message");
    syslog(LOG_ERR, "Daemon demonstration: ERROR message");
    syslog(LOG_DEBUG, "Daemon demonstration: DEBUG message");

    std::cout << "Messages written to syslog (check with: journalctl -xe or /var/log/syslog)" << std::endl;

    // Close syslog
    closelog();
}

void demonstrateBackgroundProcess() {
    std::cout << "\n=== Background Process (Not Full Daemon) ===" << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process - runs in background
        std::cout << "Background process started (PID: " << getpid() << ")" << std::endl;

        // Do some work
        for (int i = 0; i < 3; ++i) {
            writeLog("Background process working... " + std::to_string(i));
            sleep(1);
        }

        writeLog("Background process completed");
        exit(0);
    } else {
        // Parent continues
        std::cout << "Started background process with PID: " << pid << std::endl;
        std::cout << "Parent continues execution..." << std::endl;

        // Parent doesn't wait, allowing child to run in background
        // (In a real scenario, you might use double-fork or proper daemon creation)
    }
}

void demonstrateProcessGroups() {
    std::cout << "\n=== Process Groups and Sessions ===" << std::endl;

    std::cout << "Current process information:" << std::endl;
    std::cout << "  PID: " << getpid() << std::endl;
    std::cout << "  PPID: " << getppid() << std::endl;
    std::cout << "  Process Group ID: " << getpgrp() << std::endl;
    std::cout << "  Session ID: " << getsid(0) << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child creates new session
        pid_t sid = setsid();

        std::cout << "\nChild process (new session leader):" << std::endl;
        std::cout << "  PID: " << getpid() << std::endl;
        std::cout << "  PPID: " << getppid() << std::endl;
        std::cout << "  Process Group ID: " << getpgrp() << std::endl;
        std::cout << "  Session ID: " << getsid(0) << std::endl;
        std::cout << "  New Session ID: " << sid << std::endl;

        exit(0);
    } else {
        // Parent waits
        sleep(1);
        std::cout << "\nParent process (unchanged):" << std::endl;
        std::cout << "  PID: " << getpid() << std::endl;
        std::cout << "  Process Group ID: " << getpgrp() << std::endl;
        std::cout << "  Session ID: " << getsid(0) << std::endl;
    }
}

void demonstrateDoubleFork() {
    std::cout << "\n=== Double Fork Technique ===" << std::endl;

    std::cout << "Creating daemon using double-fork technique..." << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "First fork failed" << std::endl;
        return;
    }

    if (pid > 0) {
        // Parent exits immediately
        std::cout << "Parent exiting, intermediate process continues..." << std::endl;
        return;
    }

    // First child - create new session
    setsid();

    // Second fork
    pid = fork();

    if (pid < 0) {
        exit(EXIT_FAILURE);
    }

    if (pid > 0) {
        // First child exits
        exit(0);
    }

    // Second child is now a daemon
    // It's orphaned and adopted by init
    // Cannot acquire controlling terminal

    std::cout << "Daemon created via double-fork (PID: " << getpid() << ")" << std::endl;

    writeLog("Double-fork daemon started");

    // Do daemon work
    for (int i = 0; i < 3; ++i) {
        writeLog("Double-fork daemon running... " + std::to_string(i));
        sleep(1);
    }

    writeLog("Double-fork daemon completed");
    exit(0);
}

int main() {
    std::cout << "Daemon Processes Demonstration" << std::endl;
    std::cout << "===============================" << std::endl;

    demonstrateProcessGroups();
    demonstrateBackgroundProcess();
    demonstrateSyslog();
    demonstrateSimpleDaemon();
    demonstrateDaemonControl();

    // Note: demonstrateDoubleFork creates an orphaned process
    // Uncomment to see it in action (check logs)
    // demonstrateDoubleFork();

    std::cout << "\n=== Daemon Processes Complete ===" << std::endl;
    std::cout << "Check " << DAEMON_LOG_FILE << " for daemon logs" << std::endl;

    return 0;
}
