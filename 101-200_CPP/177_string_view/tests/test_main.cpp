/*
 * Test Suite for Program 177: std::string_view (C++17)
 */

#include <iostream>
#include <string_view>
#include <string>
#include <cassert>

using namespace std;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_string_view_from_string) {
    string s = "hello";
    string_view sv = s;
    ASSERT_EQ(sv.size(), 5);
    ASSERT_EQ(sv, "hello");
}

TEST(test_string_view_from_cstring) {
    string_view sv = "world";
    ASSERT_EQ(sv.size(), 5);
    ASSERT_EQ(sv, "world");
}

TEST(test_string_view_substr) {
    string_view sv = "hello world";
    string_view sub = sv.substr(0, 5);
    ASSERT_EQ(sub, "hello");
    ASSERT_EQ(sub.size(), 5);
}

TEST(test_string_view_at) {
    string_view sv = "test";
    ASSERT_EQ(sv[0], 't');
    ASSERT_EQ(sv[1], 'e');
    ASSERT_EQ(sv.at(2), 's');
}

TEST(test_string_view_empty) {
    string_view sv;
    ASSERT_TRUE(sv.empty());
    ASSERT_EQ(sv.size(), 0);
}

TEST(test_string_view_data) {
    string_view sv = "data";
    const char* ptr = sv.data();
    ASSERT_EQ(ptr[0], 'd');
}

TEST(test_string_view_remove_prefix) {
    string_view sv = "hello world";
    sv.remove_prefix(6);
    ASSERT_EQ(sv, "world");
}

TEST(test_string_view_remove_suffix) {
    string_view sv = "hello world";
    sv.remove_suffix(6);
    ASSERT_EQ(sv, "hello");
}

TEST(test_string_view_find) {
    string_view sv = "hello world";
    size_t pos = sv.find("world");
    ASSERT_EQ(pos, 6);
}

int main() {
    cout << "Running std::string_view Tests\n===============================\n\n";
    RUN_TEST(test_string_view_from_string);
    RUN_TEST(test_string_view_from_cstring);
    RUN_TEST(test_string_view_substr);
    RUN_TEST(test_string_view_at);
    RUN_TEST(test_string_view_empty);
    RUN_TEST(test_string_view_data);
    RUN_TEST(test_string_view_remove_prefix);
    RUN_TEST(test_string_view_remove_suffix);
    RUN_TEST(test_string_view_find);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
