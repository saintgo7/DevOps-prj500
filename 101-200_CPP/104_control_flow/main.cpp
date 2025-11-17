/*
 * Program 104: Control Flow
 *
 * Topics Covered:
 * - if statement
 * - if-else statement
 * - else-if ladder
 * - Nested if statements
 * - switch statement
 * - switch with fall-through
 * - switch with [[fallthrough]] attribute (C++17)
 * - Ternary operator
 * - goto statement (and why to avoid it)
 * - C++17: if with initializer
 * - C++20: constexpr if improvements
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o control_flow main.cpp
 */

#include <iostream>
#include <string>
#include <ctime>

void demonstrateIfStatement();
void demonstrateIfElse();
void demonstrateElseIfLadder();
void demonstrateNestedIf();
void demonstrateSwitchStatement();
void demonstrateSwitchFallthrough();
void demonstrateTernaryOperator();
void demonstrateIfWithInitializer();
void demonstrateConstexprIf();

int main() {
    std::cout << "=== C++ Control Flow ===" << std::endl;
    std::cout << std::endl;

    // ============================================================
    // 1. if Statement
    // ============================================================

    demonstrateIfStatement();

    // ============================================================
    // 2. if-else Statement
    // ============================================================

    demonstrateIfElse();

    // ============================================================
    // 3. else-if Ladder
    // ============================================================

    demonstrateElseIfLadder();

    // ============================================================
    // 4. Nested if Statements
    // ============================================================

    demonstrateNestedIf();

    // ============================================================
    // 5. switch Statement
    // ============================================================

    demonstrateSwitchStatement();

    // ============================================================
    // 6. switch with Fall-through
    // ============================================================

    demonstrateSwitchFallthrough();

    // ============================================================
    // 7. Ternary Operator
    // ============================================================

    demonstrateTernaryOperator();

    // ============================================================
    // 8. if with Initializer (C++17)
    // ============================================================

    demonstrateIfWithInitializer();

    // ============================================================
    // 9. constexpr if (C++17)
    // ============================================================

    demonstrateConstexprIf();

    // ============================================================
    // 10. goto Statement (Anti-pattern)
    // ============================================================

    std::cout << "--- goto Statement (Avoid Using) ---" << std::endl;
    std::cout << "goto is generally considered bad practice" << std::endl;
    std::cout << "It makes code harder to read and maintain" << std::endl;
    std::cout << "Use loops and functions instead" << std::endl;

    // Example (for educational purposes only):
    int counter = 0;
    start:
        if (counter < 3) {
            std::cout << "Counter: " << counter << std::endl;
            counter++;
            goto start;  // Jump back to label
        }
    std::cout << "goto loop ended" << std::endl;

    std::cout << std::endl;

    return 0;
}

/**
 * Demonstrates basic if statement
 */
void demonstrateIfStatement() {
    std::cout << "--- if Statement ---" << std::endl;

    int age = 18;

    // Simple if
    if (age >= 18) {
        std::cout << "You are an adult" << std::endl;
    }

    // if with multiple statements
    int score = 85;
    if (score >= 80) {
        std::cout << "Excellent score!" << std::endl;
        std::cout << "You passed with distinction" << std::endl;
    }

    // if without braces (not recommended for multiple statements)
    if (score > 50)
        std::cout << "You passed" << std::endl;

    // Compound condition
    bool hasLicense = true;
    int drivingAge = 20;

    if (hasLicense && drivingAge >= 18) {
        std::cout << "You can drive" << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates if-else statement
 */
void demonstrateIfElse() {
    std::cout << "--- if-else Statement ---" << std::endl;

    int number = 15;

    if (number % 2 == 0) {
        std::cout << number << " is even" << std::endl;
    } else {
        std::cout << number << " is odd" << std::endl;
    }

    // Checking password
    std::string password = "secret123";
    std::string input = "secret123";

    if (input == password) {
        std::cout << "Access granted" << std::endl;
    } else {
        std::cout << "Access denied" << std::endl;
    }

    // Comparing values
    int a = 10, b = 20;

    if (a > b) {
        std::cout << a << " is greater than " << b << std::endl;
    } else {
        std::cout << a << " is not greater than " << b << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates else-if ladder
 */
void demonstrateElseIfLadder() {
    std::cout << "--- else-if Ladder ---" << std::endl;

    int score = 75;

    if (score >= 90) {
        std::cout << "Grade: A" << std::endl;
    } else if (score >= 80) {
        std::cout << "Grade: B" << std::endl;
    } else if (score >= 70) {
        std::cout << "Grade: C" << std::endl;
    } else if (score >= 60) {
        std::cout << "Grade: D" << std::endl;
    } else {
        std::cout << "Grade: F" << std::endl;
    }

    // Categorizing age groups
    int age = 35;

    if (age < 13) {
        std::cout << "Category: Child" << std::endl;
    } else if (age < 20) {
        std::cout << "Category: Teenager" << std::endl;
    } else if (age < 60) {
        std::cout << "Category: Adult" << std::endl;
    } else {
        std::cout << "Category: Senior" << std::endl;
    }

    // Temperature categorization
    int temp = 25;

    if (temp < 0) {
        std::cout << "Freezing" << std::endl;
    } else if (temp < 10) {
        std::cout << "Cold" << std::endl;
    } else if (temp < 20) {
        std::cout << "Cool" << std::endl;
    } else if (temp < 30) {
        std::cout << "Warm" << std::endl;
    } else {
        std::cout << "Hot" << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates nested if statements
 */
void demonstrateNestedIf() {
    std::cout << "--- Nested if Statements ---" << std::endl;

    int age = 25;
    bool hasTicket = true;
    bool hasID = true;

    // Checking multiple conditions
    if (age >= 18) {
        std::cout << "Age requirement met" << std::endl;

        if (hasTicket) {
            std::cout << "Ticket verified" << std::endl;

            if (hasID) {
                std::cout << "Entry granted!" << std::endl;
            } else {
                std::cout << "ID required" << std::endl;
            }
        } else {
            std::cout << "No ticket" << std::endl;
        }
    } else {
        std::cout << "Must be 18 or older" << std::endl;
    }

    // Login validation
    std::cout << "\n--- Login Validation ---" << std::endl;
    std::string username = "admin";
    std::string password = "password123";
    bool accountActive = true;

    if (username == "admin") {
        if (password == "password123") {
            if (accountActive) {
                std::cout << "Login successful" << std::endl;
            } else {
                std::cout << "Account is inactive" << std::endl;
            }
        } else {
            std::cout << "Incorrect password" << std::endl;
        }
    } else {
        std::cout << "User not found" << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates switch statement
 */
void demonstrateSwitchStatement() {
    std::cout << "--- switch Statement ---" << std::endl;

    int day = 3;

    switch (day) {
        case 1:
            std::cout << "Monday" << std::endl;
            break;
        case 2:
            std::cout << "Tuesday" << std::endl;
            break;
        case 3:
            std::cout << "Wednesday" << std::endl;
            break;
        case 4:
            std::cout << "Thursday" << std::endl;
            break;
        case 5:
            std::cout << "Friday" << std::endl;
            break;
        case 6:
            std::cout << "Saturday" << std::endl;
            break;
        case 7:
            std::cout << "Sunday" << std::endl;
            break;
        default:
            std::cout << "Invalid day" << std::endl;
            break;
    }

    // Switch with char
    std::cout << "\n--- Switch with Character ---" << std::endl;
    char grade = 'B';

    switch (grade) {
        case 'A':
            std::cout << "Excellent!" << std::endl;
            break;
        case 'B':
            std::cout << "Good job!" << std::endl;
            break;
        case 'C':
            std::cout << "Well done" << std::endl;
            break;
        case 'D':
            std::cout << "You passed" << std::endl;
            break;
        case 'F':
            std::cout << "Better luck next time" << std::endl;
            break;
        default:
            std::cout << "Invalid grade" << std::endl;
            break;
    }

    // Calculator using switch
    std::cout << "\n--- Calculator Example ---" << std::endl;
    char operation = '+';
    int a = 10, b = 5;
    int result;

    switch (operation) {
        case '+':
            result = a + b;
            std::cout << a << " + " << b << " = " << result << std::endl;
            break;
        case '-':
            result = a - b;
            std::cout << a << " - " << b << " = " << result << std::endl;
            break;
        case '*':
            result = a * b;
            std::cout << a << " * " << b << " = " << result << std::endl;
            break;
        case '/':
            if (b != 0) {
                result = a / b;
                std::cout << a << " / " << b << " = " << result << std::endl;
            } else {
                std::cout << "Error: Division by zero" << std::endl;
            }
            break;
        default:
            std::cout << "Invalid operation" << std::endl;
            break;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates switch with fall-through
 */
void demonstrateSwitchFallthrough() {
    std::cout << "--- switch with Fall-through ---" << std::endl;

    int month = 2;

    // Without break - fall through
    std::cout << "Days in month " << month << ": ";
    switch (month) {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            std::cout << "31 days" << std::endl;
            break;
        case 4: case 6: case 9: case 11:
            std::cout << "30 days" << std::endl;
            break;
        case 2:
            std::cout << "28 or 29 days" << std::endl;
            break;
        default:
            std::cout << "Invalid month" << std::endl;
    }

    // Intentional fall-through with [[fallthrough]] attribute (C++17)
    std::cout << "\n--- Intentional Fall-through ---" << std::endl;
    int value = 2;

    switch (value) {
        case 1:
            std::cout << "Case 1" << std::endl;
            [[fallthrough]];  // Explicitly indicate intentional fall-through
        case 2:
            std::cout << "Case 2 (or fell through from 1)" << std::endl;
            [[fallthrough]];
        case 3:
            std::cout << "Case 3 (or fell through from 1 or 2)" << std::endl;
            break;
        default:
            std::cout << "Default case" << std::endl;
    }

    // Weekday vs Weekend
    std::cout << "\n--- Weekday vs Weekend ---" << std::endl;
    int dayNum = 6;

    switch (dayNum) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            std::cout << "It's a weekday" << std::endl;
            break;
        case 6:
        case 7:
            std::cout << "It's the weekend!" << std::endl;
            break;
        default:
            std::cout << "Invalid day" << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates ternary operator
 */
void demonstrateTernaryOperator() {
    std::cout << "--- Ternary Operator ---" << std::endl;

    int age = 20;

    // Basic ternary
    std::string status = (age >= 18) ? "Adult" : "Minor";
    std::cout << "Status: " << status << std::endl;

    // Finding max
    int a = 15, b = 25;
    int max = (a > b) ? a : b;
    std::cout << "Max of " << a << " and " << b << " is " << max << std::endl;

    // Nested ternary
    int score = 75;
    std::string grade = (score >= 90) ? "A" :
                       (score >= 80) ? "B" :
                       (score >= 70) ? "C" :
                       (score >= 60) ? "D" : "F";
    std::cout << "Score: " << score << ", Grade: " << grade << std::endl;

    // Conditional assignment
    bool isPremium = true;
    double discount = isPremium ? 0.20 : 0.05;
    std::cout << "Discount: " << (discount * 100) << "%" << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates if with initializer (C++17)
 */
void demonstrateIfWithInitializer() {
    std::cout << "--- if with Initializer (C++17) ---" << std::endl;

    // Variable is scoped to the if-else block
    if (int value = 42; value > 0) {
        std::cout << "Value is positive: " << value << std::endl;
    }
    // value is not accessible here

    // Useful for checking map lookups, function returns, etc.
    if (auto result = 10 * 5; result > 40) {
        std::cout << "Result " << result << " is greater than 40" << std::endl;
    } else {
        std::cout << "Result " << result << " is not greater than 40" << std::endl;
    }

    // Checking status and using it
    auto getStatus = []() { return 200; };

    if (auto status = getStatus(); status == 200) {
        std::cout << "HTTP Status: " << status << " - OK" << std::endl;
    } else if (status == 404) {
        std::cout << "HTTP Status: " << status << " - Not Found" << std::endl;
    } else {
        std::cout << "HTTP Status: " << status << " - Other" << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates constexpr if (C++17)
 */
void demonstrateConstexprIf() {
    std::cout << "--- constexpr if (C++17) ---" << std::endl;

    // Compile-time conditional compilation
    constexpr bool isDebug = false;

    if constexpr (isDebug) {
        std::cout << "Debug mode is ON" << std::endl;
        // This code is compiled only if isDebug is true
    } else {
        std::cout << "Debug mode is OFF" << std::endl;
        // This code is compiled only if isDebug is false
    }

    // The unused branch is not compiled at all
    // Useful for template metaprogramming

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Always use braces {} for if statements, even for single statements
 * 2. Prefer switch over long else-if ladders for discrete values
 * 3. Use ternary operator only for simple conditions
 * 4. Avoid deeply nested if statements - consider refactoring
 * 5. Put the most likely condition first in else-if chains
 * 6. Always include a default case in switch statements
 * 7. Use [[fallthrough]] to indicate intentional fall-through
 * 8. Avoid using goto - use structured control flow instead
 * 9. Use if with initializer (C++17) to limit variable scope
 * 10. Consider using constexpr if for compile-time decisions
 * 11. Keep conditions simple and readable
 * 12. Use early returns to reduce nesting
 */
