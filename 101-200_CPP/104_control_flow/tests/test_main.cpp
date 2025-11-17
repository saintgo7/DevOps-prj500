/*
 * Test Suite for Program 104: Control Flow
 *
 * Tests if, else if, else, switch statements
 */

#include <iostream>
#include <string>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define ASSERT_FALSE(condition) assert(!(condition))
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Helper functions to test
int getGrade(int score) {
    if (score >= 90) return 4;  // A
    else if (score >= 80) return 3;  // B
    else if (score >= 70) return 2;  // C
    else if (score >= 60) return 1;  // D
    else return 0;  // F
}

std::string getDayName(int day) {
    switch (day) {
        case 1: return "Monday";
        case 2: return "Tuesday";
        case 3: return "Wednesday";
        case 4: return "Thursday";
        case 5: return "Friday";
        case 6: return "Saturday";
        case 7: return "Sunday";
        default: return "Invalid";
    }
}

int evaluateNumber(int num) {
    if (num > 0) return 1;
    else if (num < 0) return -1;
    else return 0;
}

// Test if statements
TEST(test_simple_if) {
    int x = 10;
    bool executed = false;
    if (x > 5) {
        executed = true;
    }
    ASSERT_TRUE(executed);
}

TEST(test_if_else) {
    int result = 0;
    int x = 3;
    if (x > 5) {
        result = 1;
    } else {
        result = 2;
    }
    ASSERT_EQ(result, 2);
}

TEST(test_if_else_if_else) {
    ASSERT_EQ(getGrade(95), 4);
    ASSERT_EQ(getGrade(85), 3);
    ASSERT_EQ(getGrade(75), 2);
    ASSERT_EQ(getGrade(65), 1);
    ASSERT_EQ(getGrade(55), 0);
}

TEST(test_nested_if) {
    int x = 10, y = 20;
    int result = 0;
    if (x > 5) {
        if (y > 15) {
            result = 1;
        }
    }
    ASSERT_EQ(result, 1);
}

// Test switch statements
TEST(test_switch_basic) {
    ASSERT_EQ(getDayName(1), "Monday");
    ASSERT_EQ(getDayName(7), "Sunday");
}

TEST(test_switch_default) {
    ASSERT_EQ(getDayName(0), "Invalid");
    ASSERT_EQ(getDayName(10), "Invalid");
}

TEST(test_switch_fall_through) {
    auto getCategory = [](int num) {
        std::string category;
        switch (num) {
            case 1:
            case 2:
            case 3:
                category = "Low";
                break;
            case 4:
            case 5:
            case 6:
                category = "Medium";
                break;
            case 7:
            case 8:
            case 9:
            case 10:
                category = "High";
                break;
            default:
                category = "Invalid";
        }
        return category;
    };

    ASSERT_EQ(getCategory(2), "Low");
    ASSERT_EQ(getCategory(5), "Medium");
    ASSERT_EQ(getCategory(9), "High");
}

// Test ternary operator
TEST(test_ternary_operator) {
    int a = 10, b = 20;
    int max = (a > b) ? a : b;
    ASSERT_EQ(max, 20);

    int min = (a < b) ? a : b;
    ASSERT_EQ(min, 10);
}

TEST(test_nested_ternary) {
    int score = 85;
    std::string grade = (score >= 90) ? "A" :
                       (score >= 80) ? "B" :
                       (score >= 70) ? "C" :
                       (score >= 60) ? "D" : "F";
    ASSERT_EQ(grade, "B");
}

// Test logical conditions
TEST(test_compound_conditions) {
    int age = 25;
    bool hasLicense = true;
    bool canDrive = (age >= 18 && hasLicense);
    ASSERT_TRUE(canDrive);

    age = 16;
    canDrive = (age >= 18 && hasLicense);
    ASSERT_FALSE(canDrive);
}

TEST(test_or_conditions) {
    int day = 6;
    bool isWeekend = (day == 6 || day == 7);
    ASSERT_TRUE(isWeekend);

    day = 3;
    isWeekend = (day == 6 || day == 7);
    ASSERT_FALSE(isWeekend);
}

// Edge cases
TEST(test_zero_condition) {
    ASSERT_EQ(evaluateNumber(0), 0);
    ASSERT_EQ(evaluateNumber(5), 1);
    ASSERT_EQ(evaluateNumber(-5), -1);
}

TEST(test_boolean_conditions) {
    bool condition = true;
    int result = condition ? 1 : 0;
    ASSERT_EQ(result, 1);

    condition = false;
    result = condition ? 1 : 0;
    ASSERT_EQ(result, 0);
}

TEST(test_short_circuit_evaluation) {
    int x = 0;
    int y = 5;
    // Short-circuit: second condition not evaluated if first is false
    bool result = (x != 0) && (y / x > 0);  // Should not divide by zero
    ASSERT_FALSE(result);
}

TEST(test_boundary_conditions) {
    ASSERT_EQ(getGrade(90), 4);  // Boundary
    ASSERT_EQ(getGrade(89), 3);  // Just below boundary
    ASSERT_EQ(getGrade(60), 1);  // Boundary
    ASSERT_EQ(getGrade(59), 0);  // Just below boundary
}

int main() {
    std::cout << "=== Running Tests for Program 104: Control Flow ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_simple_if);
    RUN_TEST(test_if_else);
    RUN_TEST(test_if_else_if_else);
    RUN_TEST(test_nested_if);
    RUN_TEST(test_switch_basic);
    RUN_TEST(test_switch_default);
    RUN_TEST(test_switch_fall_through);
    RUN_TEST(test_ternary_operator);
    RUN_TEST(test_nested_ternary);
    RUN_TEST(test_compound_conditions);
    RUN_TEST(test_or_conditions);
    RUN_TEST(test_zero_condition);
    RUN_TEST(test_boolean_conditions);
    RUN_TEST(test_short_circuit_evaluation);
    RUN_TEST(test_boundary_conditions);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
