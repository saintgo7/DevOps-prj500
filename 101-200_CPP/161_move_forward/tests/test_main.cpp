/*
 * Test Suite for Program 161: Move and Forward
 *
 * Tests:
 * - std::move semantics
 * - std::forward usage
 * - Rvalue references
 * - Move constructors
 */

#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { \
    cout << "Running " << #name << "..."; \
    name(); \
    cout << " PASSED\n"; \
} while(0)

#define ASSERT_EQ(actual, expected) do { \
    if ((actual) != (expected)) { \
        cerr << "  FAILED\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

#define ASSERT_TRUE(condition) do { \
    if (!(condition)) { \
        cerr << "  FAILED\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

class Resource {
public:
    int* data;
    size_t size;

    Resource() : data(nullptr), size(0) {}

    Resource(size_t s) : size(s) {
        data = new int[s];
    }

    // Move constructor
    Resource(Resource&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }

    // Move assignment
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }

    ~Resource() {
        delete[] data;
    }
};

// Test forwarding
template<typename T>
void process_value(T&& value) {
    // Forward preserves value category
    vector<decay_t<T>> v;
    v.push_back(forward<T>(value));
}

TEST(test_move_string) {
    string s1 = "Hello, World!";
    string s2 = move(s1);

    ASSERT_EQ(s2, "Hello, World!");
    // s1 is in valid but unspecified state
}

TEST(test_move_vector) {
    vector<int> v1 = {1, 2, 3, 4, 5};
    vector<int> v2 = move(v1);

    ASSERT_EQ(v2.size(), 5);
    ASSERT_EQ(v2[0], 1);
    ASSERT_EQ(v2[4], 5);
}

TEST(test_move_constructor) {
    Resource r1(10);
    r1.data[0] = 42;

    Resource r2(move(r1));
    ASSERT_EQ(r2.size, 10);
    ASSERT_EQ(r2.data[0], 42);
    ASSERT_EQ(r1.data, nullptr);
    ASSERT_EQ(r1.size, 0);
}

TEST(test_move_assignment) {
    Resource r1(10);
    r1.data[0] = 100;

    Resource r2;
    r2 = move(r1);

    ASSERT_EQ(r2.size, 10);
    ASSERT_EQ(r2.data[0], 100);
    ASSERT_EQ(r1.data, nullptr);
}

TEST(test_forward_lvalue) {
    int x = 42;
    process_value(x);
    ASSERT_EQ(x, 42); // x is still valid
}

TEST(test_forward_rvalue) {
    process_value(42); // Temporary rvalue
    ASSERT_TRUE(true); // Should compile and run
}

TEST(test_swap_with_move) {
    string s1 = "first";
    string s2 = "second";

    string temp = move(s1);
    s1 = move(s2);
    s2 = move(temp);

    ASSERT_EQ(s1, "second");
    ASSERT_EQ(s2, "first");
}

TEST(test_edge_case_empty) {
    vector<int> v1;
    vector<int> v2 = move(v1);
    ASSERT_TRUE(v2.empty());
}

TEST(test_edge_case_self_move) {
    Resource r(5);
    r = move(r); // Self-assignment
    ASSERT_TRUE(r.data != nullptr || r.size == 0);
}

int main() {
    cout << "Running Move and Forward Tests\n";
    cout << "===============================\n\n";

    RUN_TEST(test_move_string);
    RUN_TEST(test_move_vector);
    RUN_TEST(test_move_constructor);
    RUN_TEST(test_move_assignment);
    RUN_TEST(test_forward_lvalue);
    RUN_TEST(test_forward_rvalue);
    RUN_TEST(test_swap_with_move);
    RUN_TEST(test_edge_case_empty);
    RUN_TEST(test_edge_case_self_move);

    cout << "\n===============================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
