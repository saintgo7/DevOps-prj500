/*
 * Test Suite for Program 151: Templates Basics
 *
 * Tests:
 * - Function templates
 * - Class templates
 * - Template argument deduction
 * - Non-type template parameters
 * - Default template arguments
 */

#include <iostream>
#include <string>
#include <cassert>
#include <cmath>
#include <vector>

using namespace std;

// Simple test framework
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
        cerr << "  FAILED: " << #actual << " == " << #expected \
             << " (actual: " << (actual) << ", expected: " << (expected) << ")\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

#define ASSERT_TRUE(condition) do { \
    if (!(condition)) { \
        cerr << "  FAILED: " << #condition << " is false\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

#define ASSERT_NEAR(actual, expected, epsilon) do { \
    if (fabs((actual) - (expected)) > (epsilon)) { \
        cerr << "  FAILED: " << #actual << " ~= " << #expected \
             << " (actual: " << (actual) << ", expected: " << (expected) << ")\n"; \
        tests_failed++; \
        return; \
    } \
    tests_passed++; \
} while(0)

// Function templates to test
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

// Class template to test
template<typename T>
class Box {
private:
    T value;
public:
    Box(T v) : value(v) {}
    T getValue() const { return value; }
    void setValue(T v) { value = v; }
};

// Non-type template parameter
template<typename T, int Size>
class Array {
private:
    T data[Size];
public:
    Array() {
        for (int i = 0; i < Size; i++) {
            data[i] = T();
        }
    }
    T& operator[](int index) { return data[index]; }
    const T& operator[](int index) const { return data[index]; }
    int size() const { return Size; }
};

// Default template arguments
template<typename T = int, int Size = 10>
class Container {
private:
    T data[Size];
    int count;
public:
    Container() : count(0) {}
    void add(T value) {
        if (count < Size) {
            data[count++] = value;
        }
    }
    int getCount() const { return count; }
    T get(int index) const { return data[index]; }
};

// Factorial with template specialization
template<int N>
struct Factorial {
    static const int value = N * Factorial<N-1>::value;
};

template<>
struct Factorial<0> {
    static const int value = 1;
};

// Test cases
TEST(test_function_template_integers) {
    ASSERT_EQ(maximum(10, 20), 20);
    ASSERT_EQ(maximum(50, 30), 50);
    ASSERT_EQ(maximum(-5, -10), -5);
    ASSERT_EQ(maximum(0, 0), 0);
}

TEST(test_function_template_doubles) {
    ASSERT_NEAR(maximum(3.5, 2.1), 3.5, 0.001);
    ASSERT_NEAR(maximum(1.1, 5.5), 5.5, 0.001);
    ASSERT_NEAR(maximum(-1.5, -2.5), -1.5, 0.001);
}

TEST(test_function_template_strings) {
    ASSERT_EQ(maximum(string("apple"), string("banana")), string("banana"));
    ASSERT_EQ(maximum(string("zebra"), string("aardvark")), string("zebra"));
}

TEST(test_function_template_chars) {
    ASSERT_EQ(maximum('a', 'z'), 'z');
    ASSERT_EQ(maximum('Z', 'A'), 'Z');
}

TEST(test_multiple_type_parameters) {
    auto result1 = add(10, 3.5);
    ASSERT_NEAR(result1, 13.5, 0.001);

    auto result2 = add(3.5, 10);
    ASSERT_NEAR(result2, 13.5, 0.001);

    auto result3 = add(5, 7);
    ASSERT_EQ(result3, 12);
}

TEST(test_class_template_int) {
    Box<int> intBox(42);
    ASSERT_EQ(intBox.getValue(), 42);

    intBox.setValue(100);
    ASSERT_EQ(intBox.getValue(), 100);
}

TEST(test_class_template_string) {
    Box<string> strBox("Hello");
    ASSERT_EQ(strBox.getValue(), "Hello");

    strBox.setValue("World");
    ASSERT_EQ(strBox.getValue(), "World");
}

TEST(test_class_template_double) {
    Box<double> doubleBox(3.14);
    ASSERT_NEAR(doubleBox.getValue(), 3.14, 0.001);

    doubleBox.setValue(2.71);
    ASSERT_NEAR(doubleBox.getValue(), 2.71, 0.001);
}

TEST(test_non_type_template_parameter) {
    Array<int, 5> arr;
    ASSERT_EQ(arr.size(), 5);

    for (int i = 0; i < arr.size(); i++) {
        arr[i] = i * 10;
    }

    ASSERT_EQ(arr[0], 0);
    ASSERT_EQ(arr[1], 10);
    ASSERT_EQ(arr[2], 20);
    ASSERT_EQ(arr[4], 40);
}

TEST(test_non_type_template_different_sizes) {
    Array<double, 3> arr1;
    ASSERT_EQ(arr1.size(), 3);

    Array<int, 10> arr2;
    ASSERT_EQ(arr2.size(), 10);
}

TEST(test_default_template_arguments) {
    Container<> c1; // Uses defaults: int, size 10
    c1.add(1);
    c1.add(2);
    c1.add(3);
    ASSERT_EQ(c1.getCount(), 3);
    ASSERT_EQ(c1.get(0), 1);
    ASSERT_EQ(c1.get(2), 3);
}

TEST(test_custom_type_default_size) {
    Container<double> c2; // double, size 10
    c2.add(1.1);
    c2.add(2.2);
    ASSERT_EQ(c2.getCount(), 2);
    ASSERT_NEAR(c2.get(0), 1.1, 0.001);
    ASSERT_NEAR(c2.get(1), 2.2, 0.001);
}

TEST(test_custom_type_and_size) {
    Container<int, 5> c3;
    for (int i = 0; i < 7; i++) {  // Try to add more than capacity
        c3.add(i);
    }
    ASSERT_EQ(c3.getCount(), 5);  // Should stop at 5
    ASSERT_EQ(c3.get(4), 4);
}

TEST(test_compile_time_factorial) {
    ASSERT_EQ(Factorial<0>::value, 1);
    ASSERT_EQ(Factorial<1>::value, 1);
    ASSERT_EQ(Factorial<5>::value, 120);
    ASSERT_EQ(Factorial<6>::value, 720);
}

TEST(test_template_with_vectors) {
    Box<vector<int>> vecBox(vector<int>{1, 2, 3});
    ASSERT_EQ(vecBox.getValue().size(), 3);
    ASSERT_EQ(vecBox.getValue()[0], 1);
    ASSERT_EQ(vecBox.getValue()[2], 3);
}

TEST(test_edge_case_empty_container) {
    Container<int, 5> c;
    ASSERT_EQ(c.getCount(), 0);
}

TEST(test_edge_case_negative_numbers) {
    ASSERT_EQ(maximum(-100, -50), -50);
    ASSERT_EQ(maximum(-5, 0), 0);

    Box<int> box(-42);
    ASSERT_EQ(box.getValue(), -42);
}

TEST(test_edge_case_large_numbers) {
    ASSERT_EQ(maximum(1000000, 999999), 1000000);

    Box<long long> box(9223372036854775807LL);
    ASSERT_EQ(box.getValue(), 9223372036854775807LL);
}

int main() {
    cout << "Running Template Basics Tests\n";
    cout << "==============================\n\n";

    // Run all tests
    RUN_TEST(test_function_template_integers);
    RUN_TEST(test_function_template_doubles);
    RUN_TEST(test_function_template_strings);
    RUN_TEST(test_function_template_chars);
    RUN_TEST(test_multiple_type_parameters);
    RUN_TEST(test_class_template_int);
    RUN_TEST(test_class_template_string);
    RUN_TEST(test_class_template_double);
    RUN_TEST(test_non_type_template_parameter);
    RUN_TEST(test_non_type_template_different_sizes);
    RUN_TEST(test_default_template_arguments);
    RUN_TEST(test_custom_type_default_size);
    RUN_TEST(test_custom_type_and_size);
    RUN_TEST(test_compile_time_factorial);
    RUN_TEST(test_template_with_vectors);
    RUN_TEST(test_edge_case_empty_container);
    RUN_TEST(test_edge_case_negative_numbers);
    RUN_TEST(test_edge_case_large_numbers);

    // Summary
    cout << "\n==============================\n";
    cout << "Test Results:\n";
    cout << "  Passed: " << tests_passed << "\n";
    cout << "  Failed: " << tests_failed << "\n";
    cout << "  Total:  " << (tests_passed + tests_failed) << "\n";

    return tests_failed == 0 ? 0 : 1;
}
