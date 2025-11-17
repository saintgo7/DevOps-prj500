/*
 * Program 106: Functions in C++
 *
 * Topics Covered:
 * - Function declaration and definition
 * - Function parameters (pass by value, pass by reference, pass by pointer)
 * - Return values and return types
 * - Function overloading
 * - Default parameters
 * - Inline functions
 * - Recursion
 * - Function pointers
 * - Lambda functions (C++11)
 * - constexpr functions
 * - [[nodiscard]] attribute (C++17)
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o functions main.cpp
 */

#include <iostream>
#include <string>
#include <vector>
#include <functional>

// Function declarations (prototypes)
void greet();
void greetPerson(std::string name);
int add(int a, int b);
double add(double a, double b);  // Overloaded function
int multiply(int a, int b = 2);  // Default parameter
void passByValue(int x);
void passByReference(int& x);
void passByPointer(int* x);
void passByConstReference(const std::string& str);
int factorial(int n);  // Recursive function
inline int square(int x);  // Inline function
[[nodiscard]] int getValue();  // C++17: warns if return value is ignored

void demonstrateFunctionBasics();
void demonstrateParameterPassing();
void demonstrateFunctionOverloading();
void demonstrateDefaultParameters();
void demonstrateRecursion();
void demonstrateInlineFunctions();
void demonstrateFunctionPointers();
void demonstrateLambdas();
void demonstrateConstexprFunctions();
void demonstrateReturnTypes();

int main() {
    std::cout << "=== C++ Functions ===" << std::endl;
    std::cout << std::endl;

    // ============================================================
    // 1. Function Basics
    // ============================================================

    demonstrateFunctionBasics();

    // ============================================================
    // 2. Parameter Passing
    // ============================================================

    demonstrateParameterPassing();

    // ============================================================
    // 3. Function Overloading
    // ============================================================

    demonstrateFunctionOverloading();

    // ============================================================
    // 4. Default Parameters
    // ============================================================

    demonstrateDefaultParameters();

    // ============================================================
    // 5. Recursion
    // ============================================================

    demonstrateRecursion();

    // ============================================================
    // 6. Inline Functions
    // ============================================================

    demonstrateInlineFunctions();

    // ============================================================
    // 7. Function Pointers
    // ============================================================

    demonstrateFunctionPointers();

    // ============================================================
    // 8. Lambda Functions
    // ============================================================

    demonstrateLambdas();

    // ============================================================
    // 9. constexpr Functions
    // ============================================================

    demonstrateConstexprFunctions();

    // ============================================================
    // 10. Return Types
    // ============================================================

    demonstrateReturnTypes();

    return 0;
}

// Function definitions

void greet() {
    std::cout << "Hello, World!" << std::endl;
}

void greetPerson(std::string name) {
    std::cout << "Hello, " << name << "!" << std::endl;
}

int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

void passByValue(int x) {
    x = 100;  // Only modifies local copy
    std::cout << "Inside passByValue: " << x << std::endl;
}

void passByReference(int& x) {
    x = 100;  // Modifies original variable
    std::cout << "Inside passByReference: " << x << std::endl;
}

void passByPointer(int* x) {
    if (x != nullptr) {
        *x = 100;  // Modifies original variable through pointer
        std::cout << "Inside passByPointer: " << *x << std::endl;
    }
}

void passByConstReference(const std::string& str) {
    // str[0] = 'X';  // Error: cannot modify const reference
    std::cout << "String: " << str << " (passed by const ref)" << std::endl;
}

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

inline int square(int x) {
    return x * x;
}

[[nodiscard]] int getValue() {
    return 42;
}

/**
 * Demonstrates function basics
 */
void demonstrateFunctionBasics() {
    std::cout << "--- Function Basics ---" << std::endl;

    // Calling void function
    greet();

    // Function with parameter
    greetPerson("Alice");

    // Function with return value
    int sum = add(5, 3);
    std::cout << "5 + 3 = " << sum << std::endl;

    // Using return value directly
    std::cout << "10 + 20 = " << add(10, 20) << std::endl;

    // [[nodiscard]] demonstration
    int value = getValue();  // OK
    std::cout << "Got value: " << value << std::endl;
    // getValue();  // Warning: ignoring return value of function declared with 'nodiscard'

    std::cout << std::endl;
}

/**
 * Demonstrates parameter passing methods
 */
void demonstrateParameterPassing() {
    std::cout << "--- Parameter Passing ---" << std::endl;

    // Pass by value
    int a = 10;
    std::cout << "Before passByValue: " << a << std::endl;
    passByValue(a);
    std::cout << "After passByValue: " << a << " (unchanged)" << std::endl;

    // Pass by reference
    int b = 10;
    std::cout << "\nBefore passByReference: " << b << std::endl;
    passByReference(b);
    std::cout << "After passByReference: " << b << " (modified)" << std::endl;

    // Pass by pointer
    int c = 10;
    std::cout << "\nBefore passByPointer: " << c << std::endl;
    passByPointer(&c);
    std::cout << "After passByPointer: " << c << " (modified)" << std::endl;

    // Pass by const reference (efficient for large objects)
    std::string message = "Hello, C++!";
    std::cout << "\n";
    passByConstReference(message);

    std::cout << std::endl;
}

/**
 * Demonstrates function overloading
 */
void demonstrateFunctionOverloading() {
    std::cout << "--- Function Overloading ---" << std::endl;

    // Same function name, different parameter types
    int intSum = add(5, 3);
    double doubleSum = add(5.5, 3.2);

    std::cout << "add(5, 3) = " << intSum << std::endl;
    std::cout << "add(5.5, 3.2) = " << doubleSum << std::endl;

    // Overloading based on number of parameters
    auto printValue = [](int x) {
        std::cout << "Integer: " << x << std::endl;
    };

    auto printTwoValues = [](int x, int y) {
        std::cout << "Two integers: " << x << ", " << y << std::endl;
    };

    printValue(42);
    printTwoValues(10, 20);

    std::cout << std::endl;
}

/**
 * Demonstrates default parameters
 */
void demonstrateDefaultParameters() {
    std::cout << "--- Default Parameters ---" << std::endl;

    // Using default value
    std::cout << "multiply(5) = " << multiply(5) << " (uses default 2)" << std::endl;

    // Overriding default value
    std::cout << "multiply(5, 3) = " << multiply(5, 3) << std::endl;

    // Function with multiple defaults
    auto greetWithTime = [](std::string name, std::string time = "day") {
        std::cout << "Good " << time << ", " << name << "!" << std::endl;
    };

    greetWithTime("Bob");
    greetWithTime("Alice", "morning");

    std::cout << std::endl;
}

/**
 * Demonstrates recursion
 */
void demonstrateRecursion() {
    std::cout << "--- Recursion ---" << std::endl;

    // Factorial
    std::cout << "Factorial of 5: " << factorial(5) << std::endl;
    std::cout << "Factorial of 10: " << factorial(10) << std::endl;

    // Fibonacci (recursive)
    auto fibonacci = [](auto&& self, int n) -> int {
        if (n <= 1) return n;
        return self(self, n - 1) + self(self, n - 2);
    };

    std::cout << "Fibonacci(7): " << fibonacci(fibonacci, 7) << std::endl;

    // Sum of digits (recursive)
    auto sumDigits = [](auto&& self, int n) -> int {
        if (n == 0) return 0;
        return (n % 10) + self(self, n / 10);
    };

    std::cout << "Sum of digits in 12345: " << sumDigits(sumDigits, 12345) << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates inline functions
 */
void demonstrateInlineFunctions() {
    std::cout << "--- Inline Functions ---" << std::endl;

    // Inline functions suggest compiler to insert code directly
    std::cout << "square(5) = " << square(5) << std::endl;
    std::cout << "square(10) = " << square(10) << std::endl;

    // Lambda functions are implicitly inline
    auto cube = [](int x) { return x * x * x; };
    std::cout << "cube(3) = " << cube(3) << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates function pointers
 */
void demonstrateFunctionPointers() {
    std::cout << "--- Function Pointers ---" << std::endl;

    // Function pointer syntax
    int (*funcPtr)(int, int);  // Pointer to function taking 2 ints, returning int

    funcPtr = add;  // Assign function to pointer
    std::cout << "funcPtr(3, 4) = " << funcPtr(3, 4) << std::endl;

    // Using std::function (C++11, more flexible)
    std::function<int(int, int)> func = add;
    std::cout << "func(5, 6) = " << func(5, 6) << std::endl;

    // Array of function pointers
    int (*operations[4])(int, int) = {add, add, add, add};
    std::cout << "operations[0](2, 3) = " << operations[0](2, 3) << std::endl;

    // Callback pattern
    auto performOperation = [](int a, int b, std::function<int(int, int)> op) {
        return op(a, b);
    };

    std::cout << "Callback with add: " << performOperation(7, 8, add) << std::endl;

    auto subtract = [](int a, int b) { return a - b; };
    std::cout << "Callback with subtract: " << performOperation(10, 3, subtract) << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates lambda functions
 */
void demonstrateLambdas() {
    std::cout << "--- Lambda Functions (C++11) ---" << std::endl;

    // Basic lambda
    auto greet = []() {
        std::cout << "Hello from lambda!" << std::endl;
    };
    greet();

    // Lambda with parameters
    auto add_lambda = [](int a, int b) {
        return a + b;
    };
    std::cout << "Lambda add(3, 4) = " << add_lambda(3, 4) << std::endl;

    // Lambda with explicit return type
    auto divide = [](int a, int b) -> double {
        return static_cast<double>(a) / b;
    };
    std::cout << "Lambda divide(7, 2) = " << divide(7, 2) << std::endl;

    // Capture by value
    int x = 10;
    auto captureValue = [x]() {
        std::cout << "Captured x by value: " << x << std::endl;
    };
    captureValue();

    // Capture by reference
    int y = 20;
    auto captureRef = [&y]() {
        y = 100;
        std::cout << "Modified y via reference: " << y << std::endl;
    };
    captureRef();
    std::cout << "y after lambda: " << y << std::endl;

    // Capture all by value
    int a = 1, b = 2;
    auto captureAll = [=]() {
        std::cout << "Captured all: a=" << a << ", b=" << b << std::endl;
    };
    captureAll();

    // Capture all by reference
    auto captureAllRef = [&]() {
        a = 100;
        b = 200;
    };
    captureAllRef();
    std::cout << "After captureAllRef: a=" << a << ", b=" << b << std::endl;

    // Mixed capture
    int c = 5, d = 10;
    auto mixedCapture = [c, &d]() {
        // c is by value, d is by reference
        d = 99;
        std::cout << "c=" << c << ", d=" << d << std::endl;
    };
    mixedCapture();

    // Generic lambda (C++14)
    auto genericAdd = [](auto a, auto b) {
        return a + b;
    };
    std::cout << "Generic lambda: " << genericAdd(5, 3) << std::endl;
    std::cout << "Generic lambda: " << genericAdd(5.5, 3.2) << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates constexpr functions
 */
void demonstrateConstexprFunctions() {
    std::cout << "--- constexpr Functions ---" << std::endl;

    // constexpr function (can be evaluated at compile time)
    constexpr auto constexprSquare = [](int x) {
        return x * x;
    };

    constexpr int result = constexprSquare(5);  // Evaluated at compile time
    std::cout << "constexpr square(5) = " << result << std::endl;

    // Can also be used at runtime
    int runtimeValue = 7;
    std::cout << "square(" << runtimeValue << ") = " << constexprSquare(runtimeValue) << std::endl;

    // constexpr factorial
    constexpr auto constexprFactorial = [](auto&& self, int n) -> int {
        return (n <= 1) ? 1 : n * self(self, n - 1);
    };

    constexpr int fact5 = constexprFactorial(constexprFactorial, 5);
    std::cout << "constexpr factorial(5) = " << fact5 << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates various return types
 */
void demonstrateReturnTypes() {
    std::cout << "--- Return Types ---" << std::endl;

    // Void return
    auto printMessage = []() {
        std::cout << "This function returns void" << std::endl;
    };
    printMessage();

    // Returning a value
    auto getAnswer = []() -> int {
        return 42;
    };
    std::cout << "The answer: " << getAnswer() << std::endl;

    // Returning multiple values via struct
    struct Result {
        int sum;
        int product;
    };

    auto calculate = [](int a, int b) -> Result {
        return {a + b, a * b};
    };

    auto [sum, product] = calculate(5, 3);  // C++17 structured binding
    std::cout << "Sum: " << sum << ", Product: " << product << std::endl;

    // Returning reference
    auto getFirst = [](std::vector<int>& vec) -> int& {
        return vec[0];
    };

    std::vector<int> numbers = {1, 2, 3, 4, 5};
    getFirst(numbers) = 100;  // Modify through reference
    std::cout << "Modified first element: " << numbers[0] << std::endl;

    // Auto return type deduction (C++14)
    auto autoReturn = [](int x) {
        if (x > 0) return x;
        else return -x;
    };
    std::cout << "autoReturn(-5) = " << autoReturn(-5) << std::endl;

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Use meaningful function names (verbs for actions)
 * 2. Keep functions small and focused (single responsibility)
 * 3. Pass large objects by const reference to avoid copying
 * 4. Use references instead of pointers when possible
 * 5. Prefer const correctness (const parameters, const member functions)
 * 6. Use default parameters judiciously
 * 7. Document complex functions with comments
 * 8. Avoid too many parameters (consider using structs)
 * 9. Use [[nodiscard]] for functions where ignoring return value is an error
 * 10. Prefer lambdas for small, local functions
 * 11. Use constexpr for compile-time computations
 * 12. Be careful with recursion (stack overflow risk)
 * 13. Use inline for very small, frequently called functions
 * 14. Prefer function overloading over default parameters for clarity
 */
