/*
 * Test Suite for Program 181: Socket Programming
 */

#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cassert>
#include <cstring>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_GE(a, b) do { if ((a) < (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_socket_creation) {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    ASSERT_GE(sockfd, 0);
    close(sockfd);
}

TEST(test_socket_address_setup) {
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    addr.sin_addr.s_addr = INADDR_ANY;

    ASSERT_TRUE(addr.sin_family == AF_INET);
    ASSERT_TRUE(ntohs(addr.sin_port) == 8080);
}

TEST(test_socket_options) {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    ASSERT_GE(sockfd, 0);

    int opt = 1;
    int result = setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    ASSERT_GE(result, 0);

    close(sockfd);
}

TEST(test_inet_addr) {
    const char* ip = "127.0.0.1";
    in_addr_t addr = inet_addr(ip);
    ASSERT_TRUE(addr != INADDR_NONE);
}

TEST(test_socket_types) {
    // TCP socket
    int tcp_sock = socket(AF_INET, SOCK_STREAM, 0);
    ASSERT_GE(tcp_sock, 0);
    close(tcp_sock);

    // UDP socket
    int udp_sock = socket(AF_INET, SOCK_DGRAM, 0);
    ASSERT_GE(udp_sock, 0);
    close(udp_sock);
}

int main() {
    cout << "Running Socket Programming Tests\n=================================\n\n";
    RUN_TEST(test_socket_creation);
    RUN_TEST(test_socket_address_setup);
    RUN_TEST(test_socket_options);
    RUN_TEST(test_inet_addr);
    RUN_TEST(test_socket_types);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
