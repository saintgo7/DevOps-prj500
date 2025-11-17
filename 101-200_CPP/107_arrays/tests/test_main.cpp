/*
 * Test Suite for Program 107: Arrays
 *
 * Tests C-style arrays, std::array, and array operations
 */

#include <iostream>
#include <array>
#include <algorithm>
#include <numeric>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Test basic array operations
TEST(test_array_declaration_and_access) {
    int arr[5] = {1, 2, 3, 4, 5};
    ASSERT_EQ(arr[0], 1);
    ASSERT_EQ(arr[4], 5);
}

TEST(test_array_modification) {
    int arr[3] = {1, 2, 3};
    arr[1] = 10;
    ASSERT_EQ(arr[1], 10);
}

TEST(test_array_initialization) {
    int arr1[5] = {1, 2, 3, 4, 5};
    int arr2[5] = {1, 2};  // Rest are zero
    int arr3[5] = {0};     // All zero
    int arr4[5] = {};      // All zero

    ASSERT_EQ(arr2[3], 0);
    ASSERT_EQ(arr3[2], 0);
    ASSERT_EQ(arr4[4], 0);
}

TEST(test_array_size) {
    int arr[10];
    int size = sizeof(arr) / sizeof(arr[0]);
    ASSERT_EQ(size, 10);
}

// Test multidimensional arrays
TEST(test_2d_array) {
    int matrix[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    ASSERT_EQ(matrix[0][0], 1);
    ASSERT_EQ(matrix[1][1], 5);
    ASSERT_EQ(matrix[2][2], 9);
}

TEST(test_2d_array_iteration) {
    int matrix[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int sum = 0;
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            sum += matrix[i][j];
        }
    }
    ASSERT_EQ(sum, 21);  // 1+2+3+4+5+6
}

// Test array and pointer relationship
TEST(test_array_pointer_relationship) {
    int arr[] = {10, 20, 30};
    int* ptr = arr;
    ASSERT_EQ(*ptr, 10);
    ASSERT_EQ(*(ptr + 1), 20);
    ASSERT_EQ(ptr[2], 30);
}

TEST(test_pointer_arithmetic) {
    int arr[] = {1, 2, 3, 4, 5};
    int* ptr = arr;
    ASSERT_EQ(*(ptr + 0), 1);
    ASSERT_EQ(*(ptr + 4), 5);
}

// Test std::array
TEST(test_std_array_basic) {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    ASSERT_EQ(arr[0], 1);
    ASSERT_EQ(arr.at(4), 5);
    ASSERT_EQ(arr.size(), 5);
}

TEST(test_std_array_front_back) {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    ASSERT_EQ(arr.front(), 1);
    ASSERT_EQ(arr.back(), 5);
}

TEST(test_std_array_fill) {
    std::array<int, 5> arr;
    arr.fill(10);
    for (size_t i = 0; i < arr.size(); i++) {
        ASSERT_EQ(arr[i], 10);
    }
}

TEST(test_std_array_iteration) {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int val : arr) {
        sum += val;
    }
    ASSERT_EQ(sum, 15);
}

// Test array algorithms
TEST(test_array_sort) {
    std::array<int, 5> arr = {5, 2, 8, 1, 9};
    std::sort(arr.begin(), arr.end());
    ASSERT_EQ(arr[0], 1);
    ASSERT_EQ(arr[4], 9);
}

TEST(test_array_find) {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    auto it = std::find(arr.begin(), arr.end(), 3);
    ASSERT_TRUE(it != arr.end());
    ASSERT_EQ(*it, 3);
}

TEST(test_array_count) {
    std::array<int, 7> arr = {1, 2, 2, 3, 2, 4, 5};
    int count = std::count(arr.begin(), arr.end(), 2);
    ASSERT_EQ(count, 3);
}

TEST(test_array_sum) {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    int sum = std::accumulate(arr.begin(), arr.end(), 0);
    ASSERT_EQ(sum, 15);
}

TEST(test_array_min_max) {
    std::array<int, 5> arr = {3, 1, 4, 1, 5};
    auto minIt = std::min_element(arr.begin(), arr.end());
    auto maxIt = std::max_element(arr.begin(), arr.end());
    ASSERT_EQ(*minIt, 1);
    ASSERT_EQ(*maxIt, 5);
}

// Test common array operations
TEST(test_array_reverse) {
    int arr[] = {1, 2, 3, 4, 5};
    int reversed[5];
    for (int i = 0; i < 5; i++) {
        reversed[i] = arr[4 - i];
    }
    ASSERT_EQ(reversed[0], 5);
    ASSERT_EQ(reversed[4], 1);
}

TEST(test_array_copy) {
    int source[] = {1, 2, 3, 4, 5};
    int dest[5];
    std::copy(std::begin(source), std::end(source), std::begin(dest));
    for (int i = 0; i < 5; i++) {
        ASSERT_EQ(source[i], dest[i]);
    }
}

TEST(test_array_average) {
    int arr[] = {2, 4, 6, 8, 10};
    int sum = 0;
    for (int i = 0; i < 5; i++) {
        sum += arr[i];
    }
    double avg = static_cast<double>(sum) / 5;
    ASSERT_EQ(avg, 6.0);
}

// Edge cases
TEST(test_single_element_array) {
    int arr[1] = {42};
    ASSERT_EQ(arr[0], 42);
    ASSERT_EQ(sizeof(arr) / sizeof(arr[0]), 1);
}

TEST(test_large_array) {
    int arr[1000];
    for (int i = 0; i < 1000; i++) {
        arr[i] = i;
    }
    ASSERT_EQ(arr[0], 0);
    ASSERT_EQ(arr[999], 999);
}

TEST(test_array_bounds) {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    // at() throws exception for out of bounds
    bool caught = false;
    try {
        arr.at(10);
    } catch (const std::out_of_range&) {
        caught = true;
    }
    ASSERT_TRUE(caught);
}

int main() {
    std::cout << "=== Running Tests for Program 107: Arrays ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_array_declaration_and_access);
    RUN_TEST(test_array_modification);
    RUN_TEST(test_array_initialization);
    RUN_TEST(test_array_size);
    RUN_TEST(test_2d_array);
    RUN_TEST(test_2d_array_iteration);
    RUN_TEST(test_array_pointer_relationship);
    RUN_TEST(test_pointer_arithmetic);
    RUN_TEST(test_std_array_basic);
    RUN_TEST(test_std_array_front_back);
    RUN_TEST(test_std_array_fill);
    RUN_TEST(test_std_array_iteration);
    RUN_TEST(test_array_sort);
    RUN_TEST(test_array_find);
    RUN_TEST(test_array_count);
    RUN_TEST(test_array_sum);
    RUN_TEST(test_array_min_max);
    RUN_TEST(test_array_reverse);
    RUN_TEST(test_array_copy);
    RUN_TEST(test_array_average);
    RUN_TEST(test_single_element_array);
    RUN_TEST(test_large_array);
    RUN_TEST(test_array_bounds);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
