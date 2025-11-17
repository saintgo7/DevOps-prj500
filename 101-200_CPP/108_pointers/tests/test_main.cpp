/*
 * Test Suite for Program 108: Pointers
 *
 * Tests pointer declaration, dereferencing, arithmetic, and usage
 */

#include <iostream>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define ASSERT_FALSE(condition) assert(!(condition))
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Test basic pointer operations
TEST(test_pointer_declaration_and_dereferencing) {
    int x = 42;
    int* ptr = &x;
    ASSERT_EQ(*ptr, 42);
    ASSERT_TRUE(ptr == &x);
}

TEST(test_pointer_modification) {
    int x = 10;
    int* ptr = &x;
    *ptr = 20;
    ASSERT_EQ(x, 20);
    ASSERT_EQ(*ptr, 20);
}

TEST(test_null_pointer) {
    int* ptr = nullptr;
    ASSERT_TRUE(ptr == nullptr);
    ASSERT_FALSE(ptr != nullptr);
}

TEST(test_pointer_to_pointer) {
    int x = 42;
    int* ptr = &x;
    int** pptr = &ptr;

    ASSERT_EQ(**pptr, 42);
    ASSERT_TRUE(*pptr == ptr);
    ASSERT_TRUE(*pptr == &x);
}

// Test pointer arithmetic
TEST(test_pointer_arithmetic_increment) {
    int arr[] = {10, 20, 30, 40, 50};
    int* ptr = arr;

    ASSERT_EQ(*ptr, 10);
    ptr++;
    ASSERT_EQ(*ptr, 20);
    ptr += 2;
    ASSERT_EQ(*ptr, 40);
}

TEST(test_pointer_arithmetic_decrement) {
    int arr[] = {10, 20, 30, 40, 50};
    int* ptr = &arr[4];

    ASSERT_EQ(*ptr, 50);
    ptr--;
    ASSERT_EQ(*ptr, 40);
    ptr -= 2;
    ASSERT_EQ(*ptr, 20);
}

TEST(test_pointer_difference) {
    int arr[] = {1, 2, 3, 4, 5};
    int* ptr1 = &arr[1];
    int* ptr2 = &arr[4];

    ASSERT_EQ(ptr2 - ptr1, 3);
}

TEST(test_pointer_comparison) {
    int arr[] = {1, 2, 3};
    int* ptr1 = &arr[0];
    int* ptr2 = &arr[2];

    ASSERT_TRUE(ptr1 < ptr2);
    ASSERT_TRUE(ptr2 > ptr1);
    ASSERT_TRUE(ptr1 != ptr2);
}

// Test pointers with arrays
TEST(test_pointer_array_access) {
    int arr[] = {10, 20, 30, 40, 50};
    int* ptr = arr;

    ASSERT_EQ(ptr[0], 10);
    ASSERT_EQ(ptr[2], 30);
    ASSERT_EQ(ptr[4], 50);
}

TEST(test_array_name_as_pointer) {
    int arr[] = {1, 2, 3, 4, 5};
    ASSERT_EQ(*arr, 1);
    ASSERT_EQ(*(arr + 2), 3);
    ASSERT_EQ(arr[3], *(arr + 3));
}

// Test pointers to const and const pointers
TEST(test_pointer_to_const) {
    int x = 10;
    const int* ptr = &x;  // Pointer to const int

    ASSERT_EQ(*ptr, 10);
    // *ptr = 20;  // Error: cannot modify through pointer to const
    x = 20;  // But can modify x directly
    ASSERT_EQ(*ptr, 20);
}

TEST(test_const_pointer) {
    int x = 10, y = 20;
    int* const ptr = &x;  // Const pointer to int

    ASSERT_EQ(*ptr, 10);
    *ptr = 15;  // Can modify value
    ASSERT_EQ(*ptr, 15);
    ASSERT_EQ(x, 15);
    // ptr = &y;  // Error: cannot reassign const pointer
}

TEST(test_const_pointer_to_const) {
    int x = 10;
    const int* const ptr = &x;  // Const pointer to const int

    ASSERT_EQ(*ptr, 10);
    // *ptr = 20;  // Error: cannot modify value
    // ptr = nullptr;  // Error: cannot reassign pointer
}

// Test void pointers
TEST(test_void_pointer) {
    int x = 42;
    void* ptr = &x;

    // Must cast to use
    int* intPtr = static_cast<int*>(ptr);
    ASSERT_EQ(*intPtr, 42);
}

// Test function pointers
TEST(test_function_pointer) {
    auto add = [](int a, int b) { return a + b; };
    int (*funcPtr)(int, int) = add;

    ASSERT_EQ(funcPtr(5, 3), 8);
}

// Test dynamic memory
TEST(test_dynamic_allocation) {
    int* ptr = new int(42);
    ASSERT_EQ(*ptr, 42);

    *ptr = 100;
    ASSERT_EQ(*ptr, 100);

    delete ptr;
    // ptr is now dangling, don't use it
}

TEST(test_dynamic_array_allocation) {
    int* arr = new int[5]{1, 2, 3, 4, 5};

    ASSERT_EQ(arr[0], 1);
    ASSERT_EQ(arr[4], 5);

    delete[] arr;
}

// Edge cases
TEST(test_null_pointer_assignment) {
    int* ptr = nullptr;
    ASSERT_TRUE(ptr == nullptr);

    int x = 10;
    ptr = &x;
    ASSERT_FALSE(ptr == nullptr);
    ASSERT_EQ(*ptr, 10);
}

TEST(test_pointer_swap) {
    int a = 10, b = 20;
    int* ptr1 = &a;
    int* ptr2 = &b;

    int* temp = ptr1;
    ptr1 = ptr2;
    ptr2 = temp;

    ASSERT_EQ(*ptr1, 20);
    ASSERT_EQ(*ptr2, 10);
}

TEST(test_pointer_to_first_element) {
    int arr[] = {1, 2, 3, 4, 5};
    int* ptr = arr;
    int* ptr2 = &arr[0];

    ASSERT_TRUE(ptr == ptr2);
    ASSERT_EQ(*ptr, *ptr2);
}

int main() {
    std::cout << "=== Running Tests for Program 108: Pointers ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_pointer_declaration_and_dereferencing);
    RUN_TEST(test_pointer_modification);
    RUN_TEST(test_null_pointer);
    RUN_TEST(test_pointer_to_pointer);
    RUN_TEST(test_pointer_arithmetic_increment);
    RUN_TEST(test_pointer_arithmetic_decrement);
    RUN_TEST(test_pointer_difference);
    RUN_TEST(test_pointer_comparison);
    RUN_TEST(test_pointer_array_access);
    RUN_TEST(test_array_name_as_pointer);
    RUN_TEST(test_pointer_to_const);
    RUN_TEST(test_const_pointer);
    RUN_TEST(test_const_pointer_to_const);
    RUN_TEST(test_void_pointer);
    RUN_TEST(test_function_pointer);
    RUN_TEST(test_dynamic_allocation);
    RUN_TEST(test_dynamic_array_allocation);
    RUN_TEST(test_null_pointer_assignment);
    RUN_TEST(test_pointer_swap);
    RUN_TEST(test_pointer_to_first_element);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
