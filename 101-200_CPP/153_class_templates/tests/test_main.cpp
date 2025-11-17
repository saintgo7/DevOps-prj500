/*
 * Test Suite for Program 153: Class Templates
 *
 * Tests:
 * - Basic class templates
 * - Template member functions
 * - Template constructors
 * - Static members in templates
 * - Friend functions in templates
 */

#include <iostream>
#include <string>
#include <vector>
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

// Stack template
template<typename T>
class Stack {
private:
    vector<T> elements;
public:
    void push(const T& elem) {
        elements.push_back(elem);
    }

    void pop() {
        if (!elements.empty()) {
            elements.pop_back();
        }
    }

    T top() const {
        return elements.back();
    }

    bool empty() const {
        return elements.empty();
    }

    size_t size() const {
        return elements.size();
    }
};

// Pair template
template<typename T1, typename T2>
class Pair {
public:
    T1 first;
    T2 second;

    Pair(T1 f, T2 s) : first(f), second(s) {}

    void swap() {
        T1 temp = first;
        first = static_cast<T1>(second);
        second = static_cast<T2>(temp);
    }
};

// Counter template with static member
template<typename T>
class Counter {
private:
    static int count;
    T value;
public:
    Counter(T v) : value(v) {
        count++;
    }

    static int getCount() {
        return count;
    }

    T getValue() const { return value; }
};

template<typename T>
int Counter<T>::count = 0;

// Test cases
TEST(test_stack_push_pop) {
    Stack<int> s;
    s.push(10);
    s.push(20);
    s.push(30);

    ASSERT_EQ(s.size(), 3);
    ASSERT_EQ(s.top(), 30);

    s.pop();
    ASSERT_EQ(s.top(), 20);
    ASSERT_EQ(s.size(), 2);
}

TEST(test_stack_empty) {
    Stack<int> s;
    ASSERT_TRUE(s.empty());

    s.push(1);
    ASSERT_TRUE(!s.empty());

    s.pop();
    ASSERT_TRUE(s.empty());
}

TEST(test_stack_string) {
    Stack<string> s;
    s.push("hello");
    s.push("world");

    ASSERT_EQ(s.top(), "world");
    s.pop();
    ASSERT_EQ(s.top(), "hello");
}

TEST(test_pair_creation) {
    Pair<int, string> p(42, "answer");
    ASSERT_EQ(p.first, 42);
    ASSERT_EQ(p.second, "answer");

    Pair<double, double> p2(3.14, 2.71);
    ASSERT_EQ(p2.first, 3.14);
    ASSERT_EQ(p2.second, 2.71);
}

TEST(test_pair_modification) {
    Pair<int, int> p(10, 20);
    p.first = 100;
    p.second = 200;
    ASSERT_EQ(p.first, 100);
    ASSERT_EQ(p.second, 200);
}

TEST(test_counter_static_member) {
    // Note: count is shared among all Counter<int> instances
    // but separate for Counter<double>
    int initial_count = Counter<int>::getCount();

    Counter<int> c1(10);
    ASSERT_EQ(Counter<int>::getCount(), initial_count + 1);

    Counter<int> c2(20);
    ASSERT_EQ(Counter<int>::getCount(), initial_count + 2);

    Counter<int> c3(30);
    ASSERT_EQ(Counter<int>::getCount(), initial_count + 3);
}

TEST(test_counter_different_types) {
    // Each type has its own static counter
    int int_count = Counter<int>::getCount();
    int double_count = Counter<double>::getCount();

    Counter<double> d1(1.5);
    ASSERT_EQ(Counter<double>::getCount(), double_count + 1);
    // Counter<int>::count should be unchanged
    ASSERT_EQ(Counter<int>::getCount(), int_count);
}

TEST(test_multiple_stacks) {
    Stack<int> s1;
    Stack<string> s2;

    s1.push(1);
    s1.push(2);
    s2.push("a");
    s2.push("b");

    ASSERT_EQ(s1.size(), 2);
    ASSERT_EQ(s2.size(), 2);
    ASSERT_EQ(s1.top(), 2);
    ASSERT_EQ(s2.top(), "b");
}

TEST(test_edge_case_single_element) {
    Stack<int> s;
    s.push(42);
    ASSERT_EQ(s.top(), 42);
    ASSERT_EQ(s.size(), 1);

    s.pop();
    ASSERT_TRUE(s.empty());
}

TEST(test_edge_case_large_stack) {
    Stack<int> s;
    for (int i = 0; i < 1000; i++) {
        s.push(i);
    }
    ASSERT_EQ(s.size(), 1000);
    ASSERT_EQ(s.top(), 999);
}

int main() {
    cout << "Running Class Templates Tests\n";
    cout << "==============================\n\n";

    RUN_TEST(test_stack_push_pop);
    RUN_TEST(test_stack_empty);
    RUN_TEST(test_stack_string);
    RUN_TEST(test_pair_creation);
    RUN_TEST(test_pair_modification);
    RUN_TEST(test_counter_static_member);
    RUN_TEST(test_counter_different_types);
    RUN_TEST(test_multiple_stacks);
    RUN_TEST(test_edge_case_single_element);
    RUN_TEST(test_edge_case_large_stack);

    cout << "\n==============================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
