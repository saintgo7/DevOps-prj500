/*
 * Program 181: Socket Programming
 * Demonstrates TCP/UDP sockets with client/server basics
 * Compile: g++ -std=c++17 -pthread -o socket_programming main.cpp
 */

#include <iostream>
#include <cstring>
#include <thread>
#include <chrono>
#include <vector>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

const int TCP_PORT = 8080;
const int UDP_PORT = 8081;
const int BUFFER_SIZE = 1024;

// TCP Server implementation
class TCPServer {
private:
    int server_fd;
    struct sockaddr_in address;

public:
    TCPServer(int port) {
        // Create socket
        server_fd = socket(AF_INET, SOCK_STREAM, 0);
        if (server_fd == -1) {
            throw std::runtime_error("TCP socket creation failed");
        }

        // Set socket options to reuse address
        int opt = 1;
        if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
            close(server_fd);
            throw std::runtime_error("setsockopt failed");
        }

        // Setup address structure
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(port);

        // Bind socket
        if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
            close(server_fd);
            throw std::runtime_error("TCP bind failed");
        }

        // Listen for connections
        if (listen(server_fd, 3) < 0) {
            close(server_fd);
            throw std::runtime_error("TCP listen failed");
        }

        std::cout << "TCP Server listening on port " << port << std::endl;
    }

    ~TCPServer() {
        close(server_fd);
    }

    void run() {
        char buffer[BUFFER_SIZE] = {0};
        int addrlen = sizeof(address);

        // Set non-blocking with timeout
        struct timeval timeout;
        timeout.tv_sec = 2;
        timeout.tv_usec = 0;
        setsockopt(server_fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

        int client_socket = accept(server_fd, (struct sockaddr*)&address,
                                   (socklen_t*)&addrlen);

        if (client_socket >= 0) {
            std::cout << "TCP: Client connected" << std::endl;

            ssize_t bytes_read = read(client_socket, buffer, BUFFER_SIZE);
            if (bytes_read > 0) {
                std::cout << "TCP Received: " << buffer << std::endl;

                // Echo response
                const char* response = "TCP Echo: ";
                send(client_socket, response, strlen(response), 0);
                send(client_socket, buffer, bytes_read, 0);
            }

            close(client_socket);
        }
    }
};

// TCP Client implementation
class TCPClient {
private:
    int sock;
    struct sockaddr_in serv_addr;

public:
    TCPClient(const char* ip, int port) {
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            throw std::runtime_error("TCP client socket creation failed");
        }

        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(port);

        if (inet_pton(AF_INET, ip, &serv_addr.sin_addr) <= 0) {
            close(sock);
            throw std::runtime_error("Invalid address");
        }
    }

    ~TCPClient() {
        close(sock);
    }

    void sendMessage(const std::string& message) {
        if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
            throw std::runtime_error("TCP connection failed");
        }

        send(sock, message.c_str(), message.length(), 0);
        std::cout << "TCP Client: Message sent" << std::endl;

        char buffer[BUFFER_SIZE] = {0};
        ssize_t bytes_read = read(sock, buffer, BUFFER_SIZE);
        if (bytes_read > 0) {
            std::cout << "TCP Client received: " << buffer << std::endl;
        }
    }
};

// UDP Server implementation
class UDPServer {
private:
    int sockfd;
    struct sockaddr_in server_addr, client_addr;

public:
    UDPServer(int port) {
        sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        if (sockfd < 0) {
            throw std::runtime_error("UDP socket creation failed");
        }

        memset(&server_addr, 0, sizeof(server_addr));
        memset(&client_addr, 0, sizeof(client_addr));

        server_addr.sin_family = AF_INET;
        server_addr.sin_addr.s_addr = INADDR_ANY;
        server_addr.sin_port = htons(port);

        if (bind(sockfd, (const struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
            close(sockfd);
            throw std::runtime_error("UDP bind failed");
        }

        // Set timeout
        struct timeval timeout;
        timeout.tv_sec = 2;
        timeout.tv_usec = 0;
        setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

        std::cout << "UDP Server listening on port " << port << std::endl;
    }

    ~UDPServer() {
        close(sockfd);
    }

    void run() {
        char buffer[BUFFER_SIZE];
        socklen_t len = sizeof(client_addr);

        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0,
                            (struct sockaddr*)&client_addr, &len);

        if (n > 0) {
            buffer[n] = '\0';
            std::cout << "UDP Received: " << buffer << std::endl;

            // Echo response
            std::string response = "UDP Echo: " + std::string(buffer);
            sendto(sockfd, response.c_str(), response.length(), 0,
                  (const struct sockaddr*)&client_addr, len);
        }
    }
};

// UDP Client implementation
class UDPClient {
private:
    int sockfd;
    struct sockaddr_in serv_addr;

public:
    UDPClient(const char* ip, int port) {
        sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        if (sockfd < 0) {
            throw std::runtime_error("UDP client socket creation failed");
        }

        memset(&serv_addr, 0, sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(port);
        serv_addr.sin_addr.s_addr = inet_addr(ip);

        // Set timeout for receiving
        struct timeval timeout;
        timeout.tv_sec = 2;
        timeout.tv_usec = 0;
        setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
    }

    ~UDPClient() {
        close(sockfd);
    }

    void sendMessage(const std::string& message) {
        sendto(sockfd, message.c_str(), message.length(), 0,
              (const struct sockaddr*)&serv_addr, sizeof(serv_addr));
        std::cout << "UDP Client: Message sent" << std::endl;

        char buffer[BUFFER_SIZE];
        socklen_t len = sizeof(serv_addr);
        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0,
                            (struct sockaddr*)&serv_addr, &len);

        if (n > 0) {
            buffer[n] = '\0';
            std::cout << "UDP Client received: " << buffer << std::endl;
        }
    }
};

void demonstrateTCPSocket() {
    std::cout << "\n=== TCP Socket Demonstration ===" << std::endl;

    try {
        // Run server in separate thread
        std::thread server_thread([]() {
            try {
                TCPServer server(TCP_PORT);
                server.run();
            } catch (const std::exception& e) {
                std::cerr << "TCP Server error: " << e.what() << std::endl;
            }
        });

        // Give server time to start
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Run client
        try {
            TCPClient client("127.0.0.1", TCP_PORT);
            client.sendMessage("Hello from TCP client!");
        } catch (const std::exception& e) {
            std::cerr << "TCP Client error: " << e.what() << std::endl;
        }

        server_thread.join();

    } catch (const std::exception& e) {
        std::cerr << "TCP error: " << e.what() << std::endl;
    }
}

void demonstrateUDPSocket() {
    std::cout << "\n=== UDP Socket Demonstration ===" << std::endl;

    try {
        // Run server in separate thread
        std::thread server_thread([]() {
            try {
                UDPServer server(UDP_PORT);
                server.run();
            } catch (const std::exception& e) {
                std::cerr << "UDP Server error: " << e.what() << std::endl;
            }
        });

        // Give server time to start
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Run client
        try {
            UDPClient client("127.0.0.1", UDP_PORT);
            client.sendMessage("Hello from UDP client!");
        } catch (const std::exception& e) {
            std::cerr << "UDP Client error: " << e.what() << std::endl;
        }

        server_thread.join();

    } catch (const std::exception& e) {
        std::cerr << "UDP error: " << e.what() << std::endl;
    }
}

void demonstrateSocketOptions() {
    std::cout << "\n=== Socket Options Demonstration ===" << std::endl;

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Socket creation failed" << std::endl;
        return;
    }

    // Get and set various socket options
    int optval;
    socklen_t optlen = sizeof(optval);

    // Get receive buffer size
    if (getsockopt(sock, SOL_SOCKET, SO_RCVBUF, &optval, &optlen) == 0) {
        std::cout << "Default receive buffer size: " << optval << " bytes" << std::endl;
    }

    // Set receive buffer size
    optval = 8192;
    if (setsockopt(sock, SOL_SOCKET, SO_RCVBUF, &optval, sizeof(optval)) == 0) {
        std::cout << "Set receive buffer size to: " << optval << " bytes" << std::endl;
    }

    // Get send buffer size
    if (getsockopt(sock, SOL_SOCKET, SO_SNDBUF, &optval, &optlen) == 0) {
        std::cout << "Default send buffer size: " << optval << " bytes" << std::endl;
    }

    // Enable keepalive
    optval = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_KEEPALIVE, &optval, sizeof(optval)) == 0) {
        std::cout << "Keepalive enabled" << std::endl;
    }

    close(sock);
}

int main() {
    std::cout << "Socket Programming Demonstration" << std::endl;
    std::cout << "=================================" << std::endl;

    demonstrateTCPSocket();
    demonstrateUDPSocket();
    demonstrateSocketOptions();

    std::cout << "\n=== Socket Programming Complete ===" << std::endl;

    return 0;
}
