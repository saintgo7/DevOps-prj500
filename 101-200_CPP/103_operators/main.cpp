/*
 * Program 103: Operators in C++
 *
 * Topics Covered:
 * - Arithmetic operators (+, -, *, /, %)
 * - Comparison/Relational operators (==, !=, <, >, <=, >=)
 * - Logical operators (&&, ||, !)
 * - Bitwise operators (&, |, ^, ~, <<, >>)
 * - Assignment operators (=, +=, -=, *=, /=, %=, etc.)
 * - Increment/Decrement operators (++, --)
 * - Conditional/Ternary operator (?:)
 * - sizeof operator
 * - Comma operator
 * - Member access operators (., ->)
 * - Operator precedence and associativity
 * - C++20: Three-way comparison operator (<=>)
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o operators main.cpp
 */

#include <iostream>
#include <iomanip>
#include <string>
#include <compare>  // C++20: For three-way comparison

void demonstrateArithmeticOperators();
void demonstrateComparisonOperators();
void demonstrateLogicalOperators();
void demonstrateBitwiseOperators();
void demonstrateAssignmentOperators();
void demonstrateIncrementDecrement();
void demonstrateTernaryOperator();
void demonstrateOtherOperators();
void demonstrateOperatorPrecedence();
void demonstrateThreeWayComparison();

int main() {
    std::cout << "=== C++ Operators ===" << std::endl;
    std::cout << std::endl;

    // ============================================================
    // 1. Arithmetic Operators
    // ============================================================

    demonstrateArithmeticOperators();

    // ============================================================
    // 2. Comparison/Relational Operators
    // ============================================================

    demonstrateComparisonOperators();

    // ============================================================
    // 3. Logical Operators
    // ============================================================

    demonstrateLogicalOperators();

    // ============================================================
    // 4. Bitwise Operators
    // ============================================================

    demonstrateBitwiseOperators();

    // ============================================================
    // 5. Assignment Operators
    // ============================================================

    demonstrateAssignmentOperators();

    // ============================================================
    // 6. Increment and Decrement Operators
    // ============================================================

    demonstrateIncrementDecrement();

    // ============================================================
    // 7. Ternary/Conditional Operator
    // ============================================================

    demonstrateTernaryOperator();

    // ============================================================
    // 8. Other Operators
    // ============================================================

    demonstrateOtherOperators();

    // ============================================================
    // 9. Operator Precedence
    // ============================================================

    demonstrateOperatorPrecedence();

    // ============================================================
    // 10. Three-Way Comparison Operator (C++20)
    // ============================================================

    demonstrateThreeWayComparison();

    return 0;
}

/**
 * Demonstrates arithmetic operators
 */
void demonstrateArithmeticOperators() {
    std::cout << "--- Arithmetic Operators ---" << std::endl;

    int a = 15, b = 4;

    std::cout << "a = " << a << ", b = " << b << std::endl;
    std::cout << "a + b = " << (a + b) << "  (Addition)" << std::endl;
    std::cout << "a - b = " << (a - b) << "  (Subtraction)" << std::endl;
    std::cout << "a * b = " << (a * b) << "  (Multiplication)" << std::endl;
    std::cout << "a / b = " << (a / b) << "  (Division - integer)" << std::endl;
    std::cout << "a % b = " << (a % b) << "  (Modulus - remainder)" << std::endl;

    // Floating-point division
    double x = 15.0, y = 4.0;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "x / y = " << (x / y) << "  (Division - floating-point)" << std::endl;

    // Unary operators
    std::cout << "+a = " << (+a) << "  (Unary plus)" << std::endl;
    std::cout << "-a = " << (-a) << "  (Unary minus)" << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates comparison/relational operators
 */
void demonstrateComparisonOperators() {
    std::cout << "--- Comparison/Relational Operators ---" << std::endl;

    int a = 10, b = 20, c = 10;

    std::cout << std::boolalpha;  // Print bool as true/false
    std::cout << "a = " << a << ", b = " << b << ", c = " << c << std::endl;

    std::cout << "a == b: " << (a == b) << "  (Equal to)" << std::endl;
    std::cout << "a == c: " << (a == c) << "  (Equal to)" << std::endl;
    std::cout << "a != b: " << (a != b) << "  (Not equal to)" << std::endl;
    std::cout << "a < b:  " << (a < b)  << "  (Less than)" << std::endl;
    std::cout << "a > b:  " << (a > b)  << "  (Greater than)" << std::endl;
    std::cout << "a <= c: " << (a <= c) << "  (Less than or equal to)" << std::endl;
    std::cout << "b >= a: " << (b >= a) << "  (Greater than or equal to)" << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates logical operators
 */
void demonstrateLogicalOperators() {
    std::cout << "--- Logical Operators ---" << std::endl;

    bool p = true, q = false;

    std::cout << std::boolalpha;
    std::cout << "p = " << p << ", q = " << q << std::endl;

    std::cout << "p && q: " << (p && q) << "  (Logical AND)" << std::endl;
    std::cout << "p || q: " << (p || q) << "  (Logical OR)" << std::endl;
    std::cout << "!p:     " << (!p)     << "  (Logical NOT)" << std::endl;
    std::cout << "!q:     " << (!q)     << "  (Logical NOT)" << std::endl;

    // Short-circuit evaluation
    std::cout << "\n--- Short-Circuit Evaluation ---" << std::endl;
    int x = 5, y = 10;

    // In AND, if first is false, second is not evaluated
    std::cout << "false && (++x > 0): " << (false && (++x > 0)) << std::endl;
    std::cout << "x remains: " << x << " (not incremented)" << std::endl;

    // In OR, if first is true, second is not evaluated
    std::cout << "true || (++y > 0): " << (true || (++y > 0)) << std::endl;
    std::cout << "y remains: " << y << " (not incremented)" << std::endl;

    // Truth table
    std::cout << "\n--- Truth Table ---" << std::endl;
    std::cout << "A     B     A&&B  A||B  !A" << std::endl;
    std::cout << "true  true  " << (true && true) << "  " << (true || true) << "  " << !true << std::endl;
    std::cout << "true  false " << (true && false) << " " << (true || false) << "  " << !true << std::endl;
    std::cout << "false true  " << (false && true) << " " << (false || true) << "  " << !false << std::endl;
    std::cout << "false false " << (false && false) << " " << (false || false) << " " << !false << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates bitwise operators
 */
void demonstrateBitwiseOperators() {
    std::cout << "--- Bitwise Operators ---" << std::endl;

    unsigned int a = 60;  // Binary: 0011 1100
    unsigned int b = 13;  // Binary: 0000 1101

    std::cout << "a = " << a << " (binary: 0011 1100)" << std::endl;
    std::cout << "b = " << b << " (binary: 0000 1101)" << std::endl;
    std::cout << std::endl;

    std::cout << "a & b  = " << (a & b)  << " (AND:  0000 1100 = 12)" << std::endl;
    std::cout << "a | b  = " << (a | b)  << " (OR:   0011 1101 = 61)" << std::endl;
    std::cout << "a ^ b  = " << (a ^ b)  << " (XOR:  0011 0001 = 49)" << std::endl;
    std::cout << "~a     = " << (~a)     << " (NOT:  inverted bits)" << std::endl;
    std::cout << "a << 2 = " << (a << 2) << " (Left shift:  1111 0000 = 240)" << std::endl;
    std::cout << "a >> 2 = " << (a >> 2) << " (Right shift: 0000 1111 = 15)" << std::endl;

    // Practical use cases
    std::cout << "\n--- Bitwise Operations Use Cases ---" << std::endl;

    // Setting a bit
    unsigned int flags = 0;
    unsigned int FLAG_READ = 1 << 0;   // 0001
    unsigned int FLAG_WRITE = 1 << 1;  // 0010
    unsigned int FLAG_EXEC = 1 << 2;   // 0100

    flags |= FLAG_READ;   // Set read flag
    flags |= FLAG_WRITE;  // Set write flag
    std::cout << "Flags after setting READ and WRITE: " << flags << std::endl;

    // Checking a bit
    bool canRead = (flags & FLAG_READ) != 0;
    bool canExec = (flags & FLAG_EXEC) != 0;
    std::cout << "Can read: " << std::boolalpha << canRead << std::endl;
    std::cout << "Can execute: " << canExec << std::endl;

    // Clearing a bit
    flags &= ~FLAG_WRITE;  // Clear write flag
    std::cout << "Flags after clearing WRITE: " << flags << std::endl;

    // Toggling a bit
    flags ^= FLAG_READ;  // Toggle read flag
    std::cout << "Flags after toggling READ: " << flags << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates assignment operators
 */
void demonstrateAssignmentOperators() {
    std::cout << "--- Assignment Operators ---" << std::endl;

    int x = 10;
    std::cout << "Initial x = " << x << std::endl;

    x += 5;   // x = x + 5
    std::cout << "x += 5  -> x = " << x << std::endl;

    x -= 3;   // x = x - 3
    std::cout << "x -= 3  -> x = " << x << std::endl;

    x *= 2;   // x = x * 2
    std::cout << "x *= 2  -> x = " << x << std::endl;

    x /= 4;   // x = x / 4
    std::cout << "x /= 4  -> x = " << x << std::endl;

    x %= 3;   // x = x % 3
    std::cout << "x %= 3  -> x = " << x << std::endl;

    // Bitwise assignment operators
    unsigned int y = 60;
    y &= 13;  // y = y & 13
    std::cout << "y &= 13 -> y = " << y << std::endl;

    y |= 5;   // y = y | 5
    std::cout << "y |= 5  -> y = " << y << std::endl;

    y ^= 3;   // y = y ^ 3
    std::cout << "y ^= 3  -> y = " << y << std::endl;

    y <<= 2;  // y = y << 2
    std::cout << "y <<= 2 -> y = " << y << std::endl;

    y >>= 1;  // y = y >> 1
    std::cout << "y >>= 1 -> y = " << y << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates increment and decrement operators
 */
void demonstrateIncrementDecrement() {
    std::cout << "--- Increment and Decrement Operators ---" << std::endl;

    int a = 5, b = 5;

    // Pre-increment (++a): increment first, then use
    std::cout << "a = " << a << std::endl;
    std::cout << "++a = " << (++a) << " (pre-increment)" << std::endl;
    std::cout << "a is now " << a << std::endl;

    // Post-increment (a++): use first, then increment
    std::cout << "\nb = " << b << std::endl;
    std::cout << "b++ = " << (b++) << " (post-increment)" << std::endl;
    std::cout << "b is now " << b << std::endl;

    int x = 10, y = 10;

    // Pre-decrement (--x): decrement first, then use
    std::cout << "\nx = " << x << std::endl;
    std::cout << "--x = " << (--x) << " (pre-decrement)" << std::endl;
    std::cout << "x is now " << x << std::endl;

    // Post-decrement (x--): use first, then decrement
    std::cout << "\ny = " << y << std::endl;
    std::cout << "y-- = " << (y--) << " (post-decrement)" << std::endl;
    std::cout << "y is now " << y << std::endl;

    // Practical example
    std::cout << "\n--- Practical Example ---" << std::endl;
    int arr[] = {1, 2, 3, 4, 5};
    int i = 0;
    std::cout << "arr[i++] outputs: " << arr[i++] << ", then i = " << i << std::endl;
    std::cout << "arr[++i] outputs: " << arr[++i] << ", with i = " << i << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates ternary/conditional operator
 */
void demonstrateTernaryOperator() {
    std::cout << "--- Ternary/Conditional Operator (?:) ---" << std::endl;

    int a = 10, b = 20;

    // Syntax: condition ? value_if_true : value_if_false
    int max = (a > b) ? a : b;
    std::cout << "max(" << a << ", " << b << ") = " << max << std::endl;

    int min = (a < b) ? a : b;
    std::cout << "min(" << a << ", " << b << ") = " << min << std::endl;

    // Nested ternary (use sparingly - can be hard to read)
    int x = 15;
    std::string category = (x < 10) ? "small" :
                          (x < 20) ? "medium" : "large";
    std::cout << "x = " << x << " is " << category << std::endl;

    // Common use case: selecting between two values
    bool isDark = true;
    std::string theme = isDark ? "dark-theme" : "light-theme";
    std::cout << "Current theme: " << theme << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates other operators
 */
void demonstrateOtherOperators() {
    std::cout << "--- Other Operators ---" << std::endl;

    // sizeof operator
    std::cout << "sizeof(int):    " << sizeof(int) << " bytes" << std::endl;
    std::cout << "sizeof(double): " << sizeof(double) << " bytes" << std::endl;

    int arr[10];
    std::cout << "sizeof(arr):    " << sizeof(arr) << " bytes" << std::endl;
    std::cout << "Array length:   " << (sizeof(arr) / sizeof(arr[0])) << std::endl;

    // Comma operator (rarely used, mostly in for loops)
    std::cout << "\n--- Comma Operator ---" << std::endl;
    int x = (5, 10, 15);  // Evaluates all, returns last
    std::cout << "x = (5, 10, 15): " << x << std::endl;

    // More common use in for loops
    for (int i = 0, j = 10; i < 5; i++, j--) {
        std::cout << "i = " << i << ", j = " << j << std::endl;
    }

    // Address-of operator (&)
    std::cout << "\n--- Address-of Operator (&) ---" << std::endl;
    int value = 42;
    std::cout << "value = " << value << std::endl;
    std::cout << "Address of value: " << &value << std::endl;

    // Dereference operator (*)
    int* ptr = &value;
    std::cout << "Dereferenced ptr: " << *ptr << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates operator precedence
 */
void demonstrateOperatorPrecedence() {
    std::cout << "--- Operator Precedence ---" << std::endl;

    int result;

    // Multiplication before addition
    result = 2 + 3 * 4;
    std::cout << "2 + 3 * 4 = " << result << " (not 20)" << std::endl;

    // Parentheses override precedence
    result = (2 + 3) * 4;
    std::cout << "(2 + 3) * 4 = " << result << std::endl;

    // Relational before logical
    bool b1 = true, b2 = false;
    int a = 5, b = 10;
    bool logicalResult = b1 || b2 && a < b;  // && has higher precedence
    std::cout << "true || false && 5 < 10 = " << std::boolalpha << logicalResult << std::endl;

    // Assignment has low precedence
    int x, y;
    x = y = 10;  // Right-to-left associativity
    std::cout << "x = y = 10: x = " << x << ", y = " << y << std::endl;

    std::cout << "\nPrecedence (high to low):" << std::endl;
    std::cout << "1. () [] -> ." << std::endl;
    std::cout << "2. ++ -- (postfix)" << std::endl;
    std::cout << "3. ++ -- (prefix) ! ~ + - * & sizeof" << std::endl;
    std::cout << "4. * / %" << std::endl;
    std::cout << "5. + -" << std::endl;
    std::cout << "6. << >>" << std::endl;
    std::cout << "7. < <= > >=" << std::endl;
    std::cout << "8. == !=" << std::endl;
    std::cout << "9. &" << std::endl;
    std::cout << "10. ^" << std::endl;
    std::cout << "11. |" << std::endl;
    std::cout << "12. &&" << std::endl;
    std::cout << "13. ||" << std::endl;
    std::cout << "14. ?:" << std::endl;
    std::cout << "15. = += -= *= /= %= etc." << std::endl;
    std::cout << "16. ," << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates three-way comparison operator (C++20)
 */
void demonstrateThreeWayComparison() {
    std::cout << "--- Three-Way Comparison Operator (C++20) ---" << std::endl;

    int a = 10, b = 20, c = 10;

    // Spaceship operator: <=>
    // Returns: < 0 (less), == 0 (equal), > 0 (greater)
    auto cmp1 = a <=> b;
    auto cmp2 = a <=> c;
    auto cmp3 = b <=> a;

    std::cout << "a = " << a << ", b = " << b << ", c = " << c << std::endl;

    if (cmp1 < 0) std::cout << "a < b" << std::endl;
    if (cmp2 == 0) std::cout << "a == c" << std::endl;
    if (cmp3 > 0) std::cout << "b > a" << std::endl;

    // Works with different types
    std::cout << "\n--- Comparing Different Types ---" << std::endl;
    double x = 3.14, y = 2.71;
    auto doubleCmp = x <=> y;
    if (doubleCmp > 0) {
        std::cout << x << " > " << y << std::endl;
    }

    // Strings also support <=>
    std::string str1 = "apple", str2 = "banana";
    auto strCmp = str1 <=> str2;
    if (strCmp < 0) {
        std::cout << str1 << " < " << str2 << " (lexicographically)" << std::endl;
    }

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Use parentheses to make complex expressions clear
 * 2. Prefer pre-increment (++i) over post-increment (i++) when the value isn't used
 * 3. Be careful with operator precedence - use parentheses when in doubt
 * 4. Avoid using too many operators in a single expression
 * 5. Use compound assignment operators (+=, *=, etc.) for clarity
 * 6. Be aware of short-circuit evaluation in logical operators
 * 7. Use bitwise operators for flags and low-level operations
 * 8. Prefer the ternary operator for simple conditional assignments
 * 9. Don't overuse the comma operator outside of for loops
 * 10. Use C++20's spaceship operator for consistent comparisons
 */
