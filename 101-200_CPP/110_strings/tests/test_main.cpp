/*
 * Test Suite for Program 110: Strings
 *
 * Tests C-style strings and std::string operations
 */

#include <iostream>
#include <string>
#include <cstring>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define ASSERT_FALSE(condition) assert(!(condition))
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Test C-style strings
TEST(test_c_string_declaration) {
    const char* str = "Hello";
    ASSERT_EQ(str[0], 'H');
    ASSERT_EQ(str[4], 'o');
}

TEST(test_c_string_length) {
    const char* str = "Hello";
    ASSERT_EQ(strlen(str), 5);
}

TEST(test_c_string_copy) {
    char dest[20];
    const char* src = "Hello";
    strcpy(dest, src);
    ASSERT_EQ(strcmp(dest, "Hello"), 0);
}

TEST(test_c_string_concatenation) {
    char str[20] = "Hello";
    strcat(str, " World");
    ASSERT_EQ(strcmp(str, "Hello World"), 0);
}

TEST(test_c_string_comparison) {
    ASSERT_EQ(strcmp("abc", "abc"), 0);
    ASSERT_TRUE(strcmp("abc", "abd") < 0);
    ASSERT_TRUE(strcmp("abd", "abc") > 0);
}

// Test std::string
TEST(test_string_declaration) {
    std::string str = "Hello";
    ASSERT_EQ(str, "Hello");
    ASSERT_EQ(str.length(), 5);
}

TEST(test_string_concatenation) {
    std::string str1 = "Hello";
    std::string str2 = " World";
    std::string result = str1 + str2;
    ASSERT_EQ(result, "Hello World");
}

TEST(test_string_append) {
    std::string str = "Hello";
    str.append(" World");
    ASSERT_EQ(str, "Hello World");

    str += "!";
    ASSERT_EQ(str, "Hello World!");
}

TEST(test_string_substring) {
    std::string str = "Hello World";
    std::string sub = str.substr(0, 5);
    ASSERT_EQ(sub, "Hello");

    sub = str.substr(6, 5);
    ASSERT_EQ(sub, "World");
}

TEST(test_string_find) {
    std::string str = "Hello World";
    size_t pos = str.find("World");
    ASSERT_EQ(pos, 6);

    pos = str.find("xyz");
    ASSERT_EQ(pos, std::string::npos);
}

TEST(test_string_replace) {
    std::string str = "Hello World";
    str.replace(6, 5, "C++");
    ASSERT_EQ(str, "Hello C++");
}

TEST(test_string_insert) {
    std::string str = "Hello";
    str.insert(5, " World");
    ASSERT_EQ(str, "Hello World");
}

TEST(test_string_erase) {
    std::string str = "Hello World";
    str.erase(5, 6);  // Erase " World"
    ASSERT_EQ(str, "Hello");
}

TEST(test_string_comparison) {
    std::string str1 = "Hello";
    std::string str2 = "Hello";
    std::string str3 = "World";

    ASSERT_TRUE(str1 == str2);
    ASSERT_TRUE(str1 != str3);
    ASSERT_TRUE(str1 < str3);
}

TEST(test_string_access) {
    std::string str = "Hello";
    ASSERT_EQ(str[0], 'H');
    ASSERT_EQ(str.at(4), 'o');
    ASSERT_EQ(str.front(), 'H');
    ASSERT_EQ(str.back(), 'o');
}

TEST(test_string_modification) {
    std::string str = "Hello";
    str[0] = 'h';
    ASSERT_EQ(str, "hello");
}

TEST(test_string_clear_empty) {
    std::string str = "Hello";
    ASSERT_FALSE(str.empty());

    str.clear();
    ASSERT_TRUE(str.empty());
    ASSERT_EQ(str.length(), 0);
}

TEST(test_string_size_length) {
    std::string str = "Hello";
    ASSERT_EQ(str.size(), 5);
    ASSERT_EQ(str.length(), 5);
    ASSERT_EQ(str.size(), str.length());
}

TEST(test_string_c_str) {
    std::string str = "Hello";
    const char* cstr = str.c_str();
    ASSERT_EQ(strcmp(cstr, "Hello"), 0);
}

// Test string operations
TEST(test_string_iteration) {
    std::string str = "Hello";
    int count = 0;
    for (char c : str) {
        count++;
    }
    ASSERT_EQ(count, 5);
}

TEST(test_string_push_pop) {
    std::string str = "Hello";
    str.push_back('!');
    ASSERT_EQ(str, "Hello!");

    str.pop_back();
    ASSERT_EQ(str, "Hello");
}

TEST(test_string_starts_ends_with) {
    std::string str = "Hello World";

    // Manual implementation since starts_with/ends_with are C++20
    ASSERT_TRUE(str.substr(0, 5) == "Hello");
    ASSERT_TRUE(str.substr(str.length() - 5) == "World");
}

// Edge cases
TEST(test_empty_string) {
    std::string str = "";
    ASSERT_TRUE(str.empty());
    ASSERT_EQ(str.length(), 0);
}

TEST(test_string_with_spaces) {
    std::string str = "Hello   World";
    ASSERT_EQ(str.length(), 13);
    ASSERT_EQ(str.find("   "), 5);
}

TEST(test_string_with_numbers) {
    std::string str = "Value: 42";
    ASSERT_EQ(str.find("42"), 7);
}

TEST(test_string_conversion) {
    int num = 42;
    std::string str = std::to_string(num);
    ASSERT_EQ(str, "42");

    std::string numStr = "123";
    int converted = std::stoi(numStr);
    ASSERT_EQ(converted, 123);
}

TEST(test_string_multiline) {
    std::string str = "Line1\nLine2\nLine3";
    ASSERT_TRUE(str.find('\n') != std::string::npos);
}

int main() {
    std::cout << "=== Running Tests for Program 110: Strings ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_c_string_declaration);
    RUN_TEST(test_c_string_length);
    RUN_TEST(test_c_string_copy);
    RUN_TEST(test_c_string_concatenation);
    RUN_TEST(test_c_string_comparison);
    RUN_TEST(test_string_declaration);
    RUN_TEST(test_string_concatenation);
    RUN_TEST(test_string_append);
    RUN_TEST(test_string_substring);
    RUN_TEST(test_string_find);
    RUN_TEST(test_string_replace);
    RUN_TEST(test_string_insert);
    RUN_TEST(test_string_erase);
    RUN_TEST(test_string_comparison);
    RUN_TEST(test_string_access);
    RUN_TEST(test_string_modification);
    RUN_TEST(test_string_clear_empty);
    RUN_TEST(test_string_size_length);
    RUN_TEST(test_string_c_str);
    RUN_TEST(test_string_iteration);
    RUN_TEST(test_string_push_pop);
    RUN_TEST(test_string_starts_ends_with);
    RUN_TEST(test_empty_string);
    RUN_TEST(test_string_with_spaces);
    RUN_TEST(test_string_with_numbers);
    RUN_TEST(test_string_conversion);
    RUN_TEST(test_string_multiline);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
