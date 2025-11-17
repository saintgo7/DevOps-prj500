/*
 * Test Suite for Program 154: Template Specialization
 *
 * Tests:
 * - Full template specialization
 * - Partial template specialization
 * - Function template specialization
 * - Class template specialization
 */

#include <iostream>
#include <string>
#include <cstring>
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

// Generic compare
template<typename T>
bool compare(T a, T b) {
    return a == b;
}

// Specialization for C-strings
template<>
bool compare<const char*>(const char* a, const char* b) {
    return strcmp(a, b) == 0;
}

// Generic storage class
template<typename T>
class Storage {
private:
    T value;
public:
    Storage(T v) : value(v) {}
    T getValue() const { return value; }
    string getType() const { return "generic"; }
};

// Specialization for pointers
template<typename T>
class Storage<T*> {
private:
    T* value;
public:
    Storage(T* v) : value(v) {}
    T* getValue() const { return value; }
    string getType() const { return "pointer"; }
};

// Full specialization for bool
template<>
class Storage<bool> {
private:
    bool value;
public:
    Storage(bool v) : value(v) {}
    bool getValue() const { return value; }
    string getType() const { return "bool"; }
};

// Test cases
TEST(test_compare_integers) {
    ASSERT_TRUE(compare(5, 5));
    ASSERT_TRUE(!compare(5, 10));
    ASSERT_TRUE(compare(0, 0));
}

TEST(test_compare_strings) {
    ASSERT_TRUE(compare(string("hello"), string("hello")));
    ASSERT_TRUE(!compare(string("hello"), string("world")));
}

TEST(test_compare_cstrings) {
    // Uses specialized version
    ASSERT_TRUE(compare("test", "test"));
    ASSERT_TRUE(!compare("hello", "world"));
}

TEST(test_storage_generic) {
    Storage<int> s(42);
    ASSERT_EQ(s.getValue(), 42);
    ASSERT_EQ(s.getType(), "generic");

    Storage<double> s2(3.14);
    ASSERT_EQ(s2.getValue(), 3.14);
    ASSERT_EQ(s2.getType(), "generic");
}

TEST(test_storage_pointer_specialization) {
    int value = 100;
    Storage<int*> s(&value);
    ASSERT_EQ(*s.getValue(), 100);
    ASSERT_EQ(s.getType(), "pointer");
}

TEST(test_storage_bool_specialization) {
    Storage<bool> s(true);
    ASSERT_EQ(s.getValue(), true);
    ASSERT_EQ(s.getType(), "bool");

    Storage<bool> s2(false);
    ASSERT_EQ(s2.getValue(), false);
}

TEST(test_specialization_selection) {
    // Generic version
    Storage<int> s1(10);
    ASSERT_EQ(s1.getType(), "generic");

    // Pointer specialization
    int val = 20;
    Storage<int*> s2(&val);
    ASSERT_EQ(s2.getType(), "pointer");

    // Full specialization
    Storage<bool> s3(true);
    ASSERT_EQ(s3.getType(), "bool");
}

TEST(test_edge_case_empty_string) {
    ASSERT_TRUE(compare(string(""), string("")));
    ASSERT_TRUE(compare("", ""));
}

TEST(test_edge_case_nullptr) {
    Storage<int*> s(nullptr);
    ASSERT_EQ(s.getValue(), nullptr);
}

TEST(test_edge_case_negative) {
    ASSERT_TRUE(compare(-5, -5));
    ASSERT_TRUE(!compare(-5, 5));

    Storage<int> s(-100);
    ASSERT_EQ(s.getValue(), -100);
}

int main() {
    cout << "Running Template Specialization Tests\n";
    cout << "======================================\n\n";

    RUN_TEST(test_compare_integers);
    RUN_TEST(test_compare_strings);
    RUN_TEST(test_compare_cstrings);
    RUN_TEST(test_storage_generic);
    RUN_TEST(test_storage_pointer_specialization);
    RUN_TEST(test_storage_bool_specialization);
    RUN_TEST(test_specialization_selection);
    RUN_TEST(test_edge_case_empty_string);
    RUN_TEST(test_edge_case_nullptr);
    RUN_TEST(test_edge_case_negative);

    cout << "\n======================================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";

    return tests_failed == 0 ? 0 : 1;
}
