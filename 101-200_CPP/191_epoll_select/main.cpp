/*
 * Program 191: Epoll and Select
 * Demonstrates event-driven I/O with epoll, select, and poll
 * Compile: g++ -std=c++17 -o epoll_select main.cpp
 */

#include <iostream>
#include <cstring>
#include <vector>
#include <sys/select.h>
#include <sys/epoll.h>
#include <poll.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

const int TEST_PORT = 9999;
const int MAX_EVENTS = 10;

// Set file descriptor to non-blocking mode
void setNonBlocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

// Create a listening socket
int createListenSocket(int port) {
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd == -1) {
        return -1;
    }

    int opt = 1;
    setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    if (bind(listen_fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        close(listen_fd);
        return -1;
    }

    if (listen(listen_fd, 5) == -1) {
        close(listen_fd);
        return -1;
    }

    return listen_fd;
}

void demonstrateSelect() {
    std::cout << "\n=== Select I/O Multiplexing ===" << std::endl;

    int listen_fd = createListenSocket(TEST_PORT);
    if (listen_fd == -1) {
        std::cerr << "Failed to create listen socket" << std::endl;
        return;
    }

    std::cout << "Server listening on port " << TEST_PORT << std::endl;
    std::cout << "Waiting for connections (timeout: 3 seconds)..." << std::endl;

    // Set up fd_set for select
    fd_set read_fds;
    struct timeval timeout;

    FD_ZERO(&read_fds);
    FD_SET(listen_fd, &read_fds);

    timeout.tv_sec = 3;
    timeout.tv_usec = 0;

    // Wait for activity
    int activity = select(listen_fd + 1, &read_fds, nullptr, nullptr, &timeout);

    if (activity == -1) {
        std::cerr << "Select error: " << strerror(errno) << std::endl;
    } else if (activity == 0) {
        std::cout << "Timeout: No connections received" << std::endl;
    } else {
        if (FD_ISSET(listen_fd, &read_fds)) {
            std::cout << "Connection available!" << std::endl;

            struct sockaddr_in client_addr;
            socklen_t addr_len = sizeof(client_addr);
            int client_fd = accept(listen_fd, (struct sockaddr*)&client_addr, &addr_len);

            if (client_fd != -1) {
                std::cout << "Accepted connection from "
                         << inet_ntoa(client_addr.sin_addr) << std::endl;

                char buffer[256] = {0};
                ssize_t n = read(client_fd, buffer, sizeof(buffer) - 1);

                if (n > 0) {
                    std::cout << "Received: " << buffer << std::endl;
                }

                close(client_fd);
            }
        }
    }

    close(listen_fd);
    std::cout << "Select demonstration complete" << std::endl;
}

void demonstratePoll() {
    std::cout << "\n=== Poll I/O Multiplexing ===" << std::endl;

    int listen_fd = createListenSocket(TEST_PORT + 1);
    if (listen_fd == -1) {
        std::cerr << "Failed to create listen socket" << std::endl;
        return;
    }

    std::cout << "Server listening on port " << (TEST_PORT + 1) << std::endl;
    std::cout << "Waiting for connections (timeout: 3000ms)..." << std::endl;

    // Set up poll structure
    struct pollfd fds[1];
    fds[0].fd = listen_fd;
    fds[0].events = POLLIN;  // Wait for readable data

    int timeout_ms = 3000;  // 3 seconds

    // Wait for activity
    int activity = poll(fds, 1, timeout_ms);

    if (activity == -1) {
        std::cerr << "Poll error: " << strerror(errno) << std::endl;
    } else if (activity == 0) {
        std::cout << "Timeout: No connections received" << std::endl;
    } else {
        if (fds[0].revents & POLLIN) {
            std::cout << "Connection available!" << std::endl;

            struct sockaddr_in client_addr;
            socklen_t addr_len = sizeof(client_addr);
            int client_fd = accept(listen_fd, (struct sockaddr*)&client_addr, &addr_len);

            if (client_fd != -1) {
                std::cout << "Accepted connection" << std::endl;

                char buffer[256] = {0};
                ssize_t n = read(client_fd, buffer, sizeof(buffer) - 1);

                if (n > 0) {
                    std::cout << "Received: " << buffer << std::endl;
                }

                close(client_fd);
            }
        }

        if (fds[0].revents & POLLERR) {
            std::cout << "Error on socket" << std::endl;
        }

        if (fds[0].revents & POLLHUP) {
            std::cout << "Hangup on socket" << std::endl;
        }
    }

    close(listen_fd);
    std::cout << "Poll demonstration complete" << std::endl;
}

void demonstrateEpoll() {
    std::cout << "\n=== Epoll I/O Multiplexing (Linux) ===" << std::endl;

#ifdef __linux__
    int listen_fd = createListenSocket(TEST_PORT + 2);
    if (listen_fd == -1) {
        std::cerr << "Failed to create listen socket" << std::endl;
        return;
    }

    setNonBlocking(listen_fd);

    // Create epoll instance
    int epoll_fd = epoll_create1(0);
    if (epoll_fd == -1) {
        std::cerr << "Failed to create epoll instance: " << strerror(errno) << std::endl;
        close(listen_fd);
        return;
    }

    std::cout << "Created epoll instance" << std::endl;

    // Add listen socket to epoll
    struct epoll_event ev;
    ev.events = EPOLLIN;  // Monitor for input
    ev.data.fd = listen_fd;

    if (epoll_ctl(epoll_fd, EPOLL_CTL_ADD, listen_fd, &ev) == -1) {
        std::cerr << "Failed to add fd to epoll: " << strerror(errno) << std::endl;
        close(epoll_fd);
        close(listen_fd);
        return;
    }

    std::cout << "Server listening on port " << (TEST_PORT + 2) << std::endl;
    std::cout << "Waiting for events (timeout: 3000ms)..." << std::endl;

    struct epoll_event events[MAX_EVENTS];
    int timeout_ms = 3000;

    // Wait for events
    int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, timeout_ms);

    if (nfds == -1) {
        std::cerr << "Epoll wait error: " << strerror(errno) << std::endl;
    } else if (nfds == 0) {
        std::cout << "Timeout: No events received" << std::endl;
    } else {
        std::cout << "Received " << nfds << " events" << std::endl;

        for (int i = 0; i < nfds; ++i) {
            if (events[i].data.fd == listen_fd) {
                // New connection
                std::cout << "New connection available" << std::endl;

                struct sockaddr_in client_addr;
                socklen_t addr_len = sizeof(client_addr);
                int client_fd = accept(listen_fd, (struct sockaddr*)&client_addr, &addr_len);

                if (client_fd != -1) {
                    std::cout << "Accepted connection" << std::endl;

                    setNonBlocking(client_fd);

                    // Add client to epoll
                    ev.events = EPOLLIN | EPOLLET;  // Edge-triggered
                    ev.data.fd = client_fd;

                    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &ev);
                }
            } else {
                // Data from client
                int fd = events[i].data.fd;
                char buffer[256] = {0};
                ssize_t n = read(fd, buffer, sizeof(buffer) - 1);

                if (n > 0) {
                    std::cout << "Received: " << buffer << std::endl;
                } else if (n == 0) {
                    std::cout << "Client closed connection" << std::endl;
                    epoll_ctl(epoll_fd, EPOLL_CTL_DEL, fd, nullptr);
                    close(fd);
                }
            }
        }
    }

    close(epoll_fd);
    close(listen_fd);
    std::cout << "Epoll demonstration complete" << std::endl;
#else
    std::cout << "Epoll is Linux-specific and not available on this platform" << std::endl;
#endif
}

void demonstrateMultiplexingComparison() {
    std::cout << "\n=== I/O Multiplexing Comparison ===" << std::endl;

    std::cout << "\n1. SELECT:" << std::endl;
    std::cout << "   - POSIX standard, portable" << std::endl;
    std::cout << "   - Limited by FD_SETSIZE (typically 1024)" << std::endl;
    std::cout << "   - O(n) complexity - must scan all FDs" << std::endl;
    std::cout << "   - fd_set modified by call" << std::endl;

    std::cout << "\n2. POLL:" << std::endl;
    std::cout << "   - POSIX standard, portable" << std::endl;
    std::cout << "   - No FD limit" << std::endl;
    std::cout << "   - O(n) complexity - must scan all FDs" << std::endl;
    std::cout << "   - Cleaner API than select" << std::endl;

    std::cout << "\n3. EPOLL (Linux):" << std::endl;
    std::cout << "   - Linux-specific" << std::endl;
    std::cout << "   - No FD limit" << std::endl;
    std::cout << "   - O(1) complexity for ready events" << std::endl;
    std::cout << "   - Edge-triggered and level-triggered modes" << std::endl;
    std::cout << "   - Best performance for many connections" << std::endl;

    std::cout << "\nSimilar alternatives:" << std::endl;
    std::cout << "   - kqueue (BSD, macOS)" << std::endl;
    std::cout << "   - IOCP (Windows)" << std::endl;
}

void demonstrateEdgeVsLevel() {
    std::cout << "\n=== Edge-Triggered vs Level-Triggered ===" << std::endl;

    std::cout << "\nLevel-Triggered (default):" << std::endl;
    std::cout << "   - Notification whenever data is available" << std::endl;
    std::cout << "   - Repeated notifications if not fully read" << std::endl;
    std::cout << "   - Easier to use, harder to misuse" << std::endl;
    std::cout << "   - Example: select, poll, epoll (default)" << std::endl;

    std::cout << "\nEdge-Triggered:" << std::endl;
    std::cout << "   - Notification only on state change" << std::endl;
    std::cout << "   - Must read all available data" << std::endl;
    std::cout << "   - More efficient, but requires careful handling" << std::endl;
    std::cout << "   - Example: epoll with EPOLLET flag" << std::endl;

#ifdef __linux__
    std::cout << "\nExample of edge-triggered epoll:" << std::endl;

    int pipe_fds[2];
    if (pipe(pipe_fds) == -1) {
        std::cerr << "Failed to create pipe" << std::endl;
        return;
    }

    setNonBlocking(pipe_fds[0]);

    int epoll_fd = epoll_create1(0);
    struct epoll_event ev;

    // Level-triggered
    std::cout << "\n1. Level-triggered mode:" << std::endl;
    ev.events = EPOLLIN;
    ev.data.fd = pipe_fds[0];
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, pipe_fds[0], &ev);

    write(pipe_fds[1], "test", 4);

    struct epoll_event events[1];

    // First wait - should trigger
    int n = epoll_wait(epoll_fd, events, 1, 100);
    std::cout << "   First wait: " << (n > 0 ? "triggered" : "not triggered") << std::endl;

    // Second wait - should still trigger (data still available)
    n = epoll_wait(epoll_fd, events, 1, 100);
    std::cout << "   Second wait: " << (n > 0 ? "triggered" : "not triggered") << std::endl;

    // Read data
    char buffer[10];
    read(pipe_fds[0], buffer, sizeof(buffer));

    epoll_ctl(epoll_fd, EPOLL_CTL_DEL, pipe_fds[0], nullptr);

    // Edge-triggered
    std::cout << "\n2. Edge-triggered mode:" << std::endl;
    ev.events = EPOLLIN | EPOLLET;
    ev.data.fd = pipe_fds[0];
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, pipe_fds[0], &ev);

    write(pipe_fds[1], "test", 4);

    // First wait - should trigger
    n = epoll_wait(epoll_fd, events, 1, 100);
    std::cout << "   First wait: " << (n > 0 ? "triggered" : "not triggered") << std::endl;

    // Second wait - should NOT trigger (no new data)
    n = epoll_wait(epoll_fd, events, 1, 100);
    std::cout << "   Second wait: " << (n > 0 ? "triggered" : "not triggered") << std::endl;

    close(epoll_fd);
    close(pipe_fds[0]);
    close(pipe_fds[1]);
#else
    std::cout << "\nEdge-triggered example requires Linux epoll" << std::endl;
#endif
}

void demonstrateSelectWithMultipleFDs() {
    std::cout << "\n=== Select with Multiple File Descriptors ===" << std::endl;

    // Create multiple pipes
    const int NUM_PIPES = 3;
    int pipes[NUM_PIPES][2];

    for (int i = 0; i < NUM_PIPES; ++i) {
        if (pipe(pipes[i]) == -1) {
            std::cerr << "Failed to create pipe " << i << std::endl;
            return;
        }
    }

    std::cout << "Created " << NUM_PIPES << " pipes" << std::endl;

    // Write to pipe 1
    write(pipes[1][1], "Data from pipe 1", 16);

    // Set up fd_set
    fd_set read_fds;
    FD_ZERO(&read_fds);

    int max_fd = 0;
    for (int i = 0; i < NUM_PIPES; ++i) {
        FD_SET(pipes[i][0], &read_fds);
        if (pipes[i][0] > max_fd) {
            max_fd = pipes[i][0];
        }
    }

    std::cout << "Monitoring " << NUM_PIPES << " read ends" << std::endl;

    struct timeval timeout;
    timeout.tv_sec = 1;
    timeout.tv_usec = 0;

    int activity = select(max_fd + 1, &read_fds, nullptr, nullptr, &timeout);

    if (activity > 0) {
        std::cout << "Activity detected on " << activity << " descriptor(s)" << std::endl;

        for (int i = 0; i < NUM_PIPES; ++i) {
            if (FD_ISSET(pipes[i][0], &read_fds)) {
                std::cout << "Pipe " << i << " has data available" << std::endl;

                char buffer[256] = {0};
                ssize_t n = read(pipes[i][0], buffer, sizeof(buffer) - 1);
                if (n > 0) {
                    std::cout << "   Data: " << buffer << std::endl;
                }
            }
        }
    }

    // Clean up
    for (int i = 0; i < NUM_PIPES; ++i) {
        close(pipes[i][0]);
        close(pipes[i][1]);
    }
}

int main() {
    std::cout << "Epoll and Select Demonstration" << std::endl;
    std::cout << "===============================" << std::endl;

    demonstrateMultiplexingComparison();
    demonstrateSelectWithMultipleFDs();
    demonstrateEdgeVsLevel();
    demonstrateSelect();
    demonstratePoll();
    demonstrateEpoll();

    std::cout << "\n=== Epoll/Select Complete ===" << std::endl;

    return 0;
}
