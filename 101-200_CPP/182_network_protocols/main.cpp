/*
 * Program 182: Network Protocols
 * Demonstrates HTTP protocol implementation and custom protocols
 * Compile: g++ -std=c++17 -pthread -o network_protocols main.cpp
 */

#include <iostream>
#include <string>
#include <sstream>
#include <map>
#include <vector>
#include <thread>
#include <chrono>
#include <cstring>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>

const int HTTP_PORT = 8888;

// HTTP Request Parser
class HTTPRequest {
public:
    std::string method;
    std::string uri;
    std::string version;
    std::map<std::string, std::string> headers;
    std::string body;

    bool parse(const std::string& raw_request) {
        std::istringstream stream(raw_request);
        std::string line;

        // Parse request line
        if (!std::getline(stream, line)) return false;

        // Remove \r if present
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }

        std::istringstream request_line(line);
        if (!(request_line >> method >> uri >> version)) {
            return false;
        }

        // Parse headers
        while (std::getline(stream, line) && line != "\r" && !line.empty()) {
            if (line.back() == '\r') {
                line.pop_back();
            }

            size_t colon_pos = line.find(':');
            if (colon_pos != std::string::npos) {
                std::string key = line.substr(0, colon_pos);
                std::string value = line.substr(colon_pos + 1);

                // Trim leading whitespace from value
                size_t first = value.find_first_not_of(" \t");
                if (first != std::string::npos) {
                    value = value.substr(first);
                }

                headers[key] = value;
            }
        }

        // Parse body (remaining content)
        std::string remaining((std::istreambuf_iterator<char>(stream)),
                             std::istreambuf_iterator<char>());
        body = remaining;

        return true;
    }

    void print() const {
        std::cout << "Method: " << method << std::endl;
        std::cout << "URI: " << uri << std::endl;
        std::cout << "Version: " << version << std::endl;
        std::cout << "Headers:" << std::endl;
        for (const auto& [key, value] : headers) {
            std::cout << "  " << key << ": " << value << std::endl;
        }
        if (!body.empty()) {
            std::cout << "Body: " << body << std::endl;
        }
    }
};

// HTTP Response Builder
class HTTPResponse {
public:
    int status_code;
    std::string status_message;
    std::map<std::string, std::string> headers;
    std::string body;

    HTTPResponse(int code = 200, const std::string& message = "OK")
        : status_code(code), status_message(message) {
        headers["Server"] = "CustomHTTPServer/1.0";
        headers["Content-Type"] = "text/html";
    }

    std::string build() const {
        std::ostringstream response;

        // Status line
        response << "HTTP/1.1 " << status_code << " " << status_message << "\r\n";

        // Headers
        for (const auto& [key, value] : headers) {
            response << key << ": " << value << "\r\n";
        }

        // Content-Length
        response << "Content-Length: " << body.length() << "\r\n";
        response << "\r\n";

        // Body
        response << body;

        return response.str();
    }

    void setBody(const std::string& content) {
        body = content;
    }

    void setHeader(const std::string& key, const std::string& value) {
        headers[key] = value;
    }
};

// Simple HTTP Server
class HTTPServer {
private:
    int server_fd;
    struct sockaddr_in address;
    int port;

public:
    HTTPServer(int p) : port(p) {
        server_fd = socket(AF_INET, SOCK_STREAM, 0);
        if (server_fd == -1) {
            throw std::runtime_error("Socket creation failed");
        }

        int opt = 1;
        if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
            close(server_fd);
            throw std::runtime_error("setsockopt failed");
        }

        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(port);

        if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
            close(server_fd);
            throw std::runtime_error("Bind failed");
        }

        if (listen(server_fd, 3) < 0) {
            close(server_fd);
            throw std::runtime_error("Listen failed");
        }

        std::cout << "HTTP Server listening on port " << port << std::endl;
    }

    ~HTTPServer() {
        close(server_fd);
    }

    void handleRequest(int client_socket) {
        char buffer[4096] = {0};
        ssize_t bytes_read = read(client_socket, buffer, sizeof(buffer) - 1);

        if (bytes_read > 0) {
            HTTPRequest request;
            std::string raw_request(buffer, bytes_read);

            std::cout << "\n--- Received HTTP Request ---" << std::endl;

            if (request.parse(raw_request)) {
                request.print();

                HTTPResponse response;

                // Route handling
                if (request.uri == "/" || request.uri == "/index.html") {
                    response.setBody("<html><body><h1>Welcome to Custom HTTP Server!</h1>"
                                   "<p>This is a simple HTTP/1.1 server implementation.</p>"
                                   "</body></html>");
                } else if (request.uri == "/about") {
                    response.setBody("<html><body><h1>About</h1>"
                                   "<p>Custom HTTP Server - Network Protocol Demo</p>"
                                   "</body></html>");
                } else if (request.uri == "/api/status") {
                    response.setHeader("Content-Type", "application/json");
                    response.setBody("{\"status\":\"ok\",\"message\":\"Server is running\"}");
                } else {
                    response.status_code = 404;
                    response.status_message = "Not Found";
                    response.setBody("<html><body><h1>404 Not Found</h1>"
                                   "<p>The requested resource was not found.</p>"
                                   "</body></html>");
                }

                std::string response_str = response.build();
                send(client_socket, response_str.c_str(), response_str.length(), 0);

                std::cout << "\n--- Sent HTTP Response ---" << std::endl;
                std::cout << "Status: " << response.status_code << " "
                         << response.status_message << std::endl;
            }
        }

        close(client_socket);
    }

    void run(int max_requests = 1) {
        struct timeval timeout;
        timeout.tv_sec = 3;
        timeout.tv_usec = 0;
        setsockopt(server_fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

        int addrlen = sizeof(address);

        for (int i = 0; i < max_requests; ++i) {
            int client_socket = accept(server_fd, (struct sockaddr*)&address,
                                      (socklen_t*)&addrlen);
            if (client_socket >= 0) {
                handleRequest(client_socket);
            }
        }
    }
};

// HTTP Client
class HTTPClient {
public:
    static std::string sendGET(const std::string& host, int port, const std::string& path) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            throw std::runtime_error("Socket creation failed");
        }

        struct sockaddr_in serv_addr;
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(port);

        if (inet_pton(AF_INET, host.c_str(), &serv_addr.sin_addr) <= 0) {
            close(sock);
            throw std::runtime_error("Invalid address");
        }

        if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
            close(sock);
            throw std::runtime_error("Connection failed");
        }

        // Build HTTP GET request
        std::ostringstream request;
        request << "GET " << path << " HTTP/1.1\r\n";
        request << "Host: " << host << "\r\n";
        request << "User-Agent: CustomHTTPClient/1.0\r\n";
        request << "Accept: */*\r\n";
        request << "Connection: close\r\n";
        request << "\r\n";

        std::string request_str = request.str();
        send(sock, request_str.c_str(), request_str.length(), 0);

        // Read response
        char buffer[4096];
        std::string response;
        ssize_t bytes_read;

        while ((bytes_read = read(sock, buffer, sizeof(buffer) - 1)) > 0) {
            buffer[bytes_read] = '\0';
            response += buffer;
        }

        close(sock);
        return response;
    }
};

// Custom Protocol: Simple Key-Value Protocol
class KeyValueProtocol {
public:
    enum class Command {
        SET,
        GET,
        DELETE,
        UNKNOWN
    };

    struct Message {
        Command command;
        std::string key;
        std::string value;

        std::string serialize() const {
            std::ostringstream oss;

            switch (command) {
                case Command::SET:
                    oss << "SET " << key << " " << value;
                    break;
                case Command::GET:
                    oss << "GET " << key;
                    break;
                case Command::DELETE:
                    oss << "DEL " << key;
                    break;
                default:
                    oss << "UNKNOWN";
            }

            return oss.str();
        }

        static Message deserialize(const std::string& data) {
            Message msg;
            std::istringstream iss(data);
            std::string cmd_str;

            iss >> cmd_str;

            if (cmd_str == "SET") {
                msg.command = Command::SET;
                iss >> msg.key >> msg.value;
            } else if (cmd_str == "GET") {
                msg.command = Command::GET;
                iss >> msg.key;
            } else if (cmd_str == "DEL") {
                msg.command = Command::DELETE;
                iss >> msg.key;
            } else {
                msg.command = Command::UNKNOWN;
            }

            return msg;
        }
    };
};

void demonstrateHTTPProtocol() {
    std::cout << "\n=== HTTP Protocol Demonstration ===" << std::endl;

    try {
        std::thread server_thread([]() {
            try {
                HTTPServer server(HTTP_PORT);
                server.run(3);  // Handle 3 requests
            } catch (const std::exception& e) {
                std::cerr << "Server error: " << e.what() << std::endl;
            }
        });

        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Send test requests
        try {
            std::cout << "\n--- Sending GET / ---" << std::endl;
            std::string response = HTTPClient::sendGET("127.0.0.1", HTTP_PORT, "/");
            std::cout << "Response preview: "
                     << response.substr(0, std::min(size_t(200), response.size()))
                     << "..." << std::endl;

            std::this_thread::sleep_for(std::chrono::milliseconds(200));

            std::cout << "\n--- Sending GET /api/status ---" << std::endl;
            response = HTTPClient::sendGET("127.0.0.1", HTTP_PORT, "/api/status");
            std::cout << "Response preview: "
                     << response.substr(0, std::min(size_t(200), response.size()))
                     << "..." << std::endl;

            std::this_thread::sleep_for(std::chrono::milliseconds(200));

            std::cout << "\n--- Sending GET /notfound ---" << std::endl;
            response = HTTPClient::sendGET("127.0.0.1", HTTP_PORT, "/notfound");
            std::cout << "Response preview: "
                     << response.substr(0, std::min(size_t(200), response.size()))
                     << "..." << std::endl;

        } catch (const std::exception& e) {
            std::cerr << "Client error: " << e.what() << std::endl;
        }

        server_thread.join();

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void demonstrateCustomProtocol() {
    std::cout << "\n=== Custom Key-Value Protocol Demonstration ===" << std::endl;

    // Create and serialize messages
    KeyValueProtocol::Message set_msg;
    set_msg.command = KeyValueProtocol::Command::SET;
    set_msg.key = "username";
    set_msg.value = "john_doe";

    std::cout << "SET message: " << set_msg.serialize() << std::endl;

    KeyValueProtocol::Message get_msg;
    get_msg.command = KeyValueProtocol::Command::GET;
    get_msg.key = "username";

    std::cout << "GET message: " << get_msg.serialize() << std::endl;

    // Deserialize messages
    std::string serialized = "SET age 25";
    auto parsed = KeyValueProtocol::Message::deserialize(serialized);
    std::cout << "Parsed SET - Key: " << parsed.key << ", Value: " << parsed.value << std::endl;

    serialized = "GET age";
    parsed = KeyValueProtocol::Message::deserialize(serialized);
    std::cout << "Parsed GET - Key: " << parsed.key << std::endl;
}

int main() {
    std::cout << "Network Protocols Demonstration" << std::endl;
    std::cout << "===============================" << std::endl;

    demonstrateHTTPProtocol();
    demonstrateCustomProtocol();

    std::cout << "\n=== Network Protocols Complete ===" << std::endl;

    return 0;
}
