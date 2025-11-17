/*
 * Test Suite for Program 105: Loops
 *
 * Tests for, while, do-while loops and loop control statements
 */

#include <iostream>
#include <vector>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Test for loops
TEST(test_basic_for_loop) {
    int sum = 0;
    for (int i = 1; i <= 10; i++) {
        sum += i;
    }
    ASSERT_EQ(sum, 55);  // 1+2+3+...+10 = 55
}

TEST(test_for_loop_decrement) {
    int count = 0;
    for (int i = 10; i > 0; i--) {
        count++;
    }
    ASSERT_EQ(count, 10);
}

TEST(test_for_loop_step) {
    int count = 0;
    for (int i = 0; i < 10; i += 2) {
        count++;
    }
    ASSERT_EQ(count, 5);  // 0, 2, 4, 6, 8
}

TEST(test_nested_for_loop) {
    int count = 0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            count++;
        }
    }
    ASSERT_EQ(count, 12);  // 3 * 4
}

TEST(test_range_based_for_loop) {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int num : numbers) {
        sum += num;
    }
    ASSERT_EQ(sum, 15);
}

// Test while loops
TEST(test_basic_while_loop) {
    int i = 0;
    int sum = 0;
    while (i < 10) {
        sum += i;
        i++;
    }
    ASSERT_EQ(sum, 45);  // 0+1+2+...+9
}

TEST(test_while_loop_condition) {
    int count = 0;
    int x = 1;
    while (x < 100) {
        x *= 2;
        count++;
    }
    ASSERT_EQ(count, 7);  // 1,2,4,8,16,32,64,128
    ASSERT_EQ(x, 128);
}

TEST(test_infinite_while_with_break) {
    int count = 0;
    while (true) {
        count++;
        if (count == 5) break;
    }
    ASSERT_EQ(count, 5);
}

// Test do-while loops
TEST(test_basic_do_while) {
    int i = 0;
    int sum = 0;
    do {
        sum += i;
        i++;
    } while (i < 10);
    ASSERT_EQ(sum, 45);
}

TEST(test_do_while_executes_once) {
    int count = 0;
    do {
        count++;
    } while (false);
    ASSERT_EQ(count, 1);  // Executes at least once
}

// Test break statement
TEST(test_break_in_loop) {
    int sum = 0;
    for (int i = 1; i <= 100; i++) {
        if (i > 10) break;
        sum += i;
    }
    ASSERT_EQ(sum, 55);  // 1+2+...+10
}

TEST(test_break_inner_loop) {
    int count = 0;
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            count++;
            if (j == 2) break;  // Only breaks inner loop
        }
    }
    ASSERT_EQ(count, 15);  // 5 * 3
}

// Test continue statement
TEST(test_continue_in_loop) {
    int sum = 0;
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) continue;  // Skip even numbers
        sum += i;
    }
    ASSERT_EQ(sum, 25);  // 1+3+5+7+9 = 25
}

TEST(test_continue_with_while) {
    int sum = 0;
    int i = 0;
    while (i < 10) {
        i++;
        if (i % 2 == 0) continue;
        sum += i;
    }
    ASSERT_EQ(sum, 25);  // Odd numbers 1+3+5+7+9
}

// Test loop patterns
TEST(test_factorial_loop) {
    int n = 5;
    int factorial = 1;
    for (int i = 1; i <= n; i++) {
        factorial *= i;
    }
    ASSERT_EQ(factorial, 120);  // 5! = 120
}

TEST(test_fibonacci_loop) {
    int n = 10;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    ASSERT_EQ(b, 55);  // 10th Fibonacci number
}

TEST(test_array_iteration) {
    int arr[] = {2, 4, 6, 8, 10};
    int sum = 0;
    for (int i = 0; i < 5; i++) {
        sum += arr[i];
    }
    ASSERT_EQ(sum, 30);
}

// Edge cases
TEST(test_empty_loop) {
    int count = 0;
    for (int i = 0; i < 0; i++) {
        count++;
    }
    ASSERT_EQ(count, 0);  // Loop never executes
}

TEST(test_single_iteration) {
    int count = 0;
    for (int i = 0; i < 1; i++) {
        count++;
    }
    ASSERT_EQ(count, 1);
}

TEST(test_negative_loop) {
    int count = 0;
    for (int i = 5; i > 0; i--) {
        count++;
    }
    ASSERT_EQ(count, 5);
}

TEST(test_loop_with_multiple_variables) {
    int sum = 0;
    for (int i = 0, j = 10; i < 5; i++, j--) {
        sum += i + j;
    }
    ASSERT_EQ(sum, 50);  // (0+10)+(1+9)+(2+8)+(3+7)+(4+6)
}

int main() {
    std::cout << "=== Running Tests for Program 105: Loops ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_basic_for_loop);
    RUN_TEST(test_for_loop_decrement);
    RUN_TEST(test_for_loop_step);
    RUN_TEST(test_nested_for_loop);
    RUN_TEST(test_range_based_for_loop);
    RUN_TEST(test_basic_while_loop);
    RUN_TEST(test_while_loop_condition);
    RUN_TEST(test_infinite_while_with_break);
    RUN_TEST(test_basic_do_while);
    RUN_TEST(test_do_while_executes_once);
    RUN_TEST(test_break_in_loop);
    RUN_TEST(test_break_inner_loop);
    RUN_TEST(test_continue_in_loop);
    RUN_TEST(test_continue_with_while);
    RUN_TEST(test_factorial_loop);
    RUN_TEST(test_fibonacci_loop);
    RUN_TEST(test_array_iteration);
    RUN_TEST(test_empty_loop);
    RUN_TEST(test_single_iteration);
    RUN_TEST(test_negative_loop);
    RUN_TEST(test_loop_with_multiple_variables);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
