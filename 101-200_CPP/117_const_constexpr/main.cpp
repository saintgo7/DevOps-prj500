/*
 * Program 117: const and constexpr
 *
 * Topics Covered:
 * - const variables and const correctness
 * - const pointers and pointers to const
 * - const member functions
 * - constexpr variables (C++11)
 * - constexpr functions (C++11/14/17/20)
 * - consteval (C++20)
 * - constinit (C++20)
 * - Compile-time vs runtime evaluation
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o const_constexpr main.cpp
 */

#include <iostream>
#include <string>
#include <array>

void demonstrateConst();
void demonstrateConstPointers();
void demonstrateConstMemberFunctions();
void demonstrateConstexpr();
void demonstrateConstexprFunctions();
void demonstrateConsteval();

int main() {
    std::cout << "=== C++ const and constexpr ===" << std::endl << std::endl;

    demonstrateConst();
    demonstrateConstPointers();
    demonstrateConstMemberFunctions();
    demonstrateConstexpr();
    demonstrateConstexprFunctions();
    demonstrateConsteval();

    return 0;
}

void demonstrateConst() {
    std::cout << "--- const Variables ---" << std::endl;

    // Basic const
    const int MAX_SIZE = 100;
    std::cout << "MAX_SIZE: " << MAX_SIZE << std::endl;
    // MAX_SIZE = 200;  // Error: cannot modify const

    // const must be initialized
    // const int uninitialized;  // Error!

    // const reference
    const int& ref = MAX_SIZE;
    std::cout << "const reference: " << ref << std::endl;

    // const with auto
    auto x = 42;        // x is int
    const auto y = 42;  // y is const int

    // Top-level const (const variable)
    const int topLevel = 10;

    // Low-level const (pointer to const)
    const int* lowLevel = &topLevel;

    std::cout << std::endl;
}

void demonstrateConstPointers() {
    std::cout << "--- const Pointers ---" << std::endl;

    int value = 42;
    int other = 100;

    // Pointer to const (cannot modify value through pointer)
    const int* ptr1 = &value;
    std::cout << "Pointer to const: *ptr1 = " << *ptr1 << std::endl;
    // *ptr1 = 100;  // Error: cannot modify
    ptr1 = &other;   // OK: can change what it points to
    std::cout << "After reassignment: *ptr1 = " << *ptr1 << std::endl;

    // Const pointer (cannot change what it points to)
    int* const ptr2 = &value;
    std::cout << "\nConst pointer: *ptr2 = " << *ptr2 << std::endl;
    *ptr2 = 200;     // OK: can modify value
    std::cout << "After modification: *ptr2 = " << *ptr2 << std::endl;
    // ptr2 = &other;  // Error: cannot reassign pointer

    // Const pointer to const (neither can change)
    const int* const ptr3 = &value;
    std::cout << "\nConst pointer to const: *ptr3 = " << *ptr3 << std::endl;
    // *ptr3 = 300;    // Error: cannot modify value
    // ptr3 = &other;  // Error: cannot reassign pointer

    std::cout << std::endl;
}

class Rectangle {
public:
    Rectangle(double w, double h) : width(w), height(h), count(0) {}

    // Const member function (doesn't modify object)
    double area() const {
        return width * height;
    }

    double perimeter() const {
        // count++;  // Error: cannot modify in const function
        return 2 * (width + height);
    }

    // Mutable member can be modified in const functions
    void incrementCount() const {
        count++;  // OK: count is mutable
    }

    int getCount() const {
        return count;
    }

    // Non-const member function
    void setWidth(double w) {
        width = w;
    }

private:
    double width;
    double height;
    mutable int count;  // Can be modified in const functions
};

void demonstrateConstMemberFunctions() {
    std::cout << "--- const Member Functions ---" << std::endl;

    Rectangle rect(5.0, 3.0);
    std::cout << "Area: " << rect.area() << std::endl;
    std::cout << "Perimeter: " << rect.perimeter() << std::endl;

    // const object can only call const member functions
    const Rectangle constRect(10.0, 4.0);
    std::cout << "\nConst rectangle area: " << constRect.area() << std::endl;
    // constRect.setWidth(20.0);  // Error: cannot call non-const function

    // Mutable member
    constRect.incrementCount();
    constRect.incrementCount();
    std::cout << "Count (mutable): " << constRect.getCount() << std::endl;

    std::cout << std::endl;
}

void demonstrateConstexpr() {
    std::cout << "--- constexpr Variables (C++11) ---" << std::endl;

    // constexpr: must be evaluable at compile time
    constexpr int SIZE = 10;
    constexpr double PI = 3.14159;

    std::cout << "SIZE: " << SIZE << std::endl;
    std::cout << "PI: " << PI << std::endl;

    // Can be used in compile-time contexts
    int array[SIZE];  // OK: SIZE is compile-time constant
    std::cout << "Array size: " << sizeof(array) / sizeof(array[0]) << std::endl;

    // constexpr vs const
    const int x = 10;         // Runtime or compile-time constant
    constexpr int y = 20;     // Must be compile-time constant

    int input = 5;
    const int z = input;      // OK: runtime constant
    // constexpr int w = input;  // Error: not compile-time

    // constexpr with user-defined types
    std::cout << std::endl;
}

// constexpr function (C++11)
constexpr int square(int x) {
    return x * x;
}

// constexpr function with conditional (C++14)
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

// More complex constexpr (C++14)
constexpr int fibonacci(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// constexpr with multiple statements (C++14)
constexpr int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

void demonstrateConstexprFunctions() {
    std::cout << "--- constexpr Functions ---" << std::endl;

    // Compile-time evaluation
    constexpr int sq = square(5);
    std::cout << "square(5) at compile time: " << sq << std::endl;

    constexpr int fact = factorial(5);
    std::cout << "factorial(5) at compile time: " << fact << std::endl;

    constexpr int fib = fibonacci(10);
    std::cout << "fibonacci(10) at compile time: " << fib << std::endl;

    // Runtime evaluation also possible
    int x = 7;
    int runtimeSq = square(x);  // Evaluated at runtime
    std::cout << "square(7) at runtime: " << runtimeSq << std::endl;

    // Use in array size
    int arr[square(3)];  // Array of 9 elements
    std::cout << "Array size: " << sizeof(arr) / sizeof(arr[0]) << std::endl;

    // constexpr lambdas (C++17)
    constexpr auto lambda = [](int x) { return x * x; };
    constexpr int lambdaResult = lambda(4);
    std::cout << "constexpr lambda(4): " << lambdaResult << std::endl;

    std::cout << std::endl;
}

// consteval: must be evaluated at compile time (C++20)
consteval int compileTimeOnly(int x) {
    return x * x;
}

// constinit: ensure compile-time initialization (C++20)
constinit int globalInit = 42;

void demonstrateConsteval() {
    std::cout << "--- consteval and constinit (C++20) ---" << std::endl;

    // consteval must be compile-time
    constexpr int result = compileTimeOnly(5);
    std::cout << "consteval compileTimeOnly(5): " << result << std::endl;

    // int x = 5;
    // int bad = compileTimeOnly(x);  // Error: must be compile-time!

    // constinit
    std::cout << "constinit global: " << globalInit << std::endl;
    globalInit = 100;  // Can modify, just ensures compile-time init
    std::cout << "After modification: " << globalInit << std::endl;

    // Comparison of const, constexpr, consteval, constinit
    std::cout << "\n--- Comparison ---" << std::endl;
    std::cout << "const:      Runtime or compile-time, cannot modify" << std::endl;
    std::cout << "constexpr:  Compile-time if possible, can be runtime" << std::endl;
    std::cout << "consteval:  Must be compile-time, cannot be runtime" << std::endl;
    std::cout << "constinit:  Compile-time init, can modify later" << std::endl;

    std::cout << std::endl;
}

/*
 * const vs constexpr Summary:
 *
 * const:
 * - Value cannot be modified
 * - Can be runtime or compile-time constant
 * - Used for immutability
 *
 * constexpr (C++11):
 * - Evaluated at compile time when possible
 * - Can also be evaluated at runtime
 * - Enables compile-time computation
 * - Variables must be literal types
 *
 * consteval (C++20):
 * - Must be evaluated at compile time
 * - Immediate functions
 * - Stricter than constexpr
 *
 * constinit (C++20):
 * - Ensures compile-time initialization
 * - Variable can be modified later
 * - Only for static/thread_local variables
 *
 * Best Practices:
 * 1. Use const for immutable values
 * 2. Use constexpr for compile-time constants
 * 3. Make member functions const when they don't modify object
 * 4. Use constexpr functions for compile-time computations
 * 5. Prefer constexpr over macros for constants
 * 6. Use mutable for cache-like members in const functions
 * 7. Use const references for large objects as parameters
 * 8. Use consteval when compile-time evaluation is required
 * 9. Use constinit for static/global variables needing compile-time init
 * 10. Leverage constexpr for better performance
 */
