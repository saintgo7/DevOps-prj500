/*
 * Test Suite for Program 109: References
 *
 * Tests reference variables, reference parameters, and reference return types
 */

#include <iostream>
#include <string>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Helper functions
void increment(int& x) {
    x++;
}

void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

int& getElement(int arr[], int index) {
    return arr[index];
}

// Test basic references
TEST(test_reference_declaration) {
    int x = 42;
    int& ref = x;

    ASSERT_EQ(ref, 42);
    ASSERT_EQ(x, 42);
}

TEST(test_reference_modification) {
    int x = 10;
    int& ref = x;

    ref = 20;
    ASSERT_EQ(x, 20);
    ASSERT_EQ(ref, 20);
}

TEST(test_reference_alias) {
    int x = 100;
    int& ref = x;

    x = 200;
    ASSERT_EQ(ref, 200);

    ref = 300;
    ASSERT_EQ(x, 300);
}

// Test reference parameters
TEST(test_reference_parameter) {
    int x = 5;
    increment(x);
    ASSERT_EQ(x, 6);

    increment(x);
    ASSERT_EQ(x, 7);
}

TEST(test_reference_swap) {
    int a = 10, b = 20;
    swap(a, b);
    ASSERT_EQ(a, 20);
    ASSERT_EQ(b, 10);
}

TEST(test_const_reference) {
    int x = 42;
    const int& ref = x;

    ASSERT_EQ(ref, 42);
    // ref = 100;  // Error: cannot modify through const reference

    x = 100;  // Can modify x directly
    ASSERT_EQ(ref, 100);
}

// Test reference return types
TEST(test_reference_return) {
    int arr[] = {1, 2, 3, 4, 5};

    getElement(arr, 2) = 10;  // Modify through reference
    ASSERT_EQ(arr[2], 10);

    int& elem = getElement(arr, 0);
    elem = 99;
    ASSERT_EQ(arr[0], 99);
}

// Test references vs pointers
TEST(test_reference_vs_pointer) {
    int x = 10;
    int& ref = x;
    int* ptr = &x;

    ASSERT_EQ(ref, *ptr);

    ref = 20;
    ASSERT_EQ(*ptr, 20);

    *ptr = 30;
    ASSERT_EQ(ref, 30);
}

TEST(test_reference_cannot_be_null) {
    int x = 42;
    int& ref = x;  // Reference must be initialized
    ASSERT_EQ(ref, 42);

    // int& nullRef;  // Error: reference must be initialized
    // int& nullRef = nullptr;  // Error: cannot bind to nullptr
}

TEST(test_reference_cannot_be_rebound) {
    int x = 10, y = 20;
    int& ref = x;
    ASSERT_EQ(ref, 10);

    ref = y;  // This assigns y's value to x, doesn't rebind ref
    ASSERT_EQ(x, 20);  // x now has y's value
    ASSERT_EQ(ref, 20);  // ref still refers to x
}

// Test const references with temporaries
TEST(test_const_reference_to_temporary) {
    const int& ref = 42;  // Can bind to temporary
    ASSERT_EQ(ref, 42);

    const std::string& strRef = "Hello";
    ASSERT_EQ(strRef, "Hello");
}

TEST(test_const_reference_extends_lifetime) {
    const int& ref = 100 + 200;  // Temporary's lifetime extended
    ASSERT_EQ(ref, 300);
}

// Test reference in structures
TEST(test_reference_in_struct) {
    struct Wrapper {
        int& ref;
        Wrapper(int& r) : ref(r) {}
    };

    int x = 42;
    Wrapper w(x);
    ASSERT_EQ(w.ref, 42);

    w.ref = 100;
    ASSERT_EQ(x, 100);
}

// Test reference with arrays
TEST(test_reference_to_array) {
    int arr[] = {1, 2, 3, 4, 5};
    int (&arrRef)[5] = arr;

    ASSERT_EQ(arrRef[0], 1);
    ASSERT_EQ(arrRef[4], 5);

    arrRef[2] = 10;
    ASSERT_EQ(arr[2], 10);
}

// Test lvalue and rvalue references
TEST(test_lvalue_reference) {
    int x = 10;
    int& lref = x;  // lvalue reference
    ASSERT_EQ(lref, 10);
}

TEST(test_rvalue_reference) {
    int&& rref = 42;  // rvalue reference (C++11)
    ASSERT_EQ(rref, 42);

    rref = 100;
    ASSERT_EQ(rref, 100);
}

// Edge cases
TEST(test_multiple_references) {
    int x = 10;
    int& ref1 = x;
    int& ref2 = x;
    int& ref3 = ref1;

    ASSERT_EQ(ref1, 10);
    ASSERT_EQ(ref2, 10);
    ASSERT_EQ(ref3, 10);

    ref1 = 20;
    ASSERT_EQ(x, 20);
    ASSERT_EQ(ref2, 20);
    ASSERT_EQ(ref3, 20);
}

TEST(test_reference_size) {
    int x = 42;
    int& ref = x;

    // Reference doesn't take additional storage
    ASSERT_EQ(sizeof(ref), sizeof(x));
}

int main() {
    std::cout << "=== Running Tests for Program 109: References ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_reference_declaration);
    RUN_TEST(test_reference_modification);
    RUN_TEST(test_reference_alias);
    RUN_TEST(test_reference_parameter);
    RUN_TEST(test_reference_swap);
    RUN_TEST(test_const_reference);
    RUN_TEST(test_reference_return);
    RUN_TEST(test_reference_vs_pointer);
    RUN_TEST(test_reference_cannot_be_null);
    RUN_TEST(test_reference_cannot_be_rebound);
    RUN_TEST(test_const_reference_to_temporary);
    RUN_TEST(test_const_reference_extends_lifetime);
    RUN_TEST(test_reference_in_struct);
    RUN_TEST(test_reference_to_array);
    RUN_TEST(test_lvalue_reference);
    RUN_TEST(test_rvalue_reference);
    RUN_TEST(test_multiple_references);
    RUN_TEST(test_reference_size);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
