/*
 * Test Suite for Program 182: Network Protocols
 */

#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_GE(a, b) do { if ((a) < (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_tcp_socket) {
    int sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    ASSERT_GE(sockfd, 0);
    close(sockfd);
}

TEST(test_udp_socket) {
    int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    ASSERT_GE(sockfd, 0);
    close(sockfd);
}

TEST(test_tcp_nodelay) {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    ASSERT_GE(sockfd, 0);

    int flag = 1;
    int result = setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));
    ASSERT_GE(result, 0);

    close(sockfd);
}

TEST(test_protocol_families) {
    // IPv4
    int sock4 = socket(AF_INET, SOCK_STREAM, 0);
    ASSERT_GE(sock4, 0);
    close(sock4);

    // IPv6
    int sock6 = socket(AF_INET6, SOCK_STREAM, 0);
    ASSERT_GE(sock6, 0);
    close(sock6);
}

TEST(test_port_conversion) {
    uint16_t port = 8080;
    uint16_t network_port = htons(port);
    uint16_t host_port = ntohs(network_port);
    ASSERT_EQ(host_port, port);
}

int main() {
    cout << "Running Network Protocols Tests\n================================\n\n";
    RUN_TEST(test_tcp_socket);
    RUN_TEST(test_udp_socket);
    RUN_TEST(test_tcp_nodelay);
    RUN_TEST(test_protocol_families);
    RUN_TEST(test_port_conversion);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
