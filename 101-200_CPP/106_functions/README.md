# Program 106: Functions in C++

## Description
A comprehensive guide to functions in C++, covering function declaration, definition, parameter passing methods, function overloading, recursion, lambda functions, function pointers, and modern C++ function features. This program demonstrates all aspects of creating and using functions effectively.

## Learning Objectives
- Master function declaration and definition
- Understand parameter passing (by value, reference, pointer, const reference)
- Learn function overloading techniques
- Implement default parameters
- Work with inline functions
- Apply recursion effectively
- Use function pointers and std::function
- Create and use lambda functions (C++11)
- Understand constexpr functions
- Use the [[nodiscard]] attribute (C++17)

## Features
- Complete function basics (declaration, definition, calling)
- Parameter passing demonstrations (value, reference, pointer)
- Function overloading examples
- Default parameters usage
- Recursive functions (factorial, Fibonacci)
- Inline function optimizations
- Function pointers and callbacks
- Lambda functions with various capture modes
- constexpr functions for compile-time evaluation
- Return type variations and multiple return values

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/106_functions
g++ -std=c++20 -Wall -Wextra -o functions main.cpp
```

### Execution
```bash
./functions
```

## Key Concepts

### 1. Function Declaration and Definition
```cpp
// Declaration (prototype)
int add(int a, int b);
void greet(std::string name);

// Definition
int add(int a, int b) {
    return a + b;
}

void greet(std::string name) {
    std::cout << "Hello, " << name << "!" << std::endl;
}
```

### 2. Parameter Passing Methods
```cpp
// Pass by value (copy)
void passByValue(int x) {
    x = 100;  // Only modifies local copy
}

// Pass by reference (can modify original)
void passByReference(int& x) {
    x = 100;  // Modifies original variable
}

// Pass by pointer
void passByPointer(int* x) {
    if (x != nullptr) {
        *x = 100;  // Modifies original through pointer
    }
}

// Pass by const reference (efficient, read-only)
void passByConstReference(const std::string& str) {
    // str[0] = 'X';  // Error: cannot modify
    std::cout << str << std::endl;  // Can read
}

// Usage
int a = 10;
passByValue(a);         // a is still 10
passByReference(a);     // a is now 100
passByPointer(&a);      // a modified through pointer
```

### 3. Function Overloading
```cpp
// Same function name, different parameter types
int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

std::string add(std::string a, std::string b) {
    return a + b;
}

// Overloading based on number of parameters
void print(int x) {
    std::cout << "Integer: " << x << std::endl;
}

void print(int x, int y) {
    std::cout << "Two integers: " << x << ", " << y << std::endl;
}
```

### 4. Default Parameters
```cpp
// Default parameters must be rightmost
int multiply(int a, int b = 2) {
    return a * b;
}

multiply(5);      // Uses default: 5 * 2 = 10
multiply(5, 3);   // Overrides default: 5 * 3 = 15

// Multiple defaults
void greet(std::string name, std::string time = "day", bool formal = false) {
    if (formal) {
        std::cout << "Good " << time << ", " << name << std::endl;
    } else {
        std::cout << "Hey " << name << "!" << std::endl;
    }
}

greet("Alice");                    // Uses all defaults
greet("Bob", "morning");           // Overrides time
greet("Charlie", "evening", true); // Overrides all
```

### 5. Recursion
```cpp
// Factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;  // Base case
    }
    return n * factorial(n - 1);  // Recursive case
}

// Fibonacci
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Sum of digits
int sumDigits(int n) {
    if (n == 0) return 0;
    return (n % 10) + sumDigits(n / 10);
}
```

### 6. Inline Functions
```cpp
// Inline suggestion to compiler (may ignore)
inline int square(int x) {
    return x * x;
}

// Lambdas are implicitly inline
auto cube = [](int x) { return x * x * x; };
```

### 7. Function Pointers
```cpp
// Function pointer declaration
int (*funcPtr)(int, int);

// Assign function to pointer
int add(int a, int b) { return a + b; }
funcPtr = add;

// Call through pointer
int result = funcPtr(3, 4);  // Calls add(3, 4)

// std::function (C++11, more flexible)
#include <functional>
std::function<int(int, int)> func = add;
result = func(5, 6);

// Callback pattern
void performOperation(int a, int b, std::function<int(int, int)> op) {
    std::cout << "Result: " << op(a, b) << std::endl;
}

performOperation(7, 3, add);
performOperation(10, 5, [](int a, int b) { return a - b; });
```

### 8. Lambda Functions (C++11)
```cpp
// Basic lambda
auto greet = []() {
    std::cout << "Hello from lambda!" << std::endl;
};
greet();

// Lambda with parameters
auto add = [](int a, int b) {
    return a + b;
};

// Explicit return type
auto divide = [](int a, int b) -> double {
    return static_cast<double>(a) / b;
};

// Capture by value [=]
int x = 10;
auto captureValue = [x]() {
    std::cout << "Captured x: " << x << std::endl;
};

// Capture by reference [&]
int y = 20;
auto captureRef = [&y]() {
    y = 100;  // Modifies original
};

// Capture all by value
auto captureAll = [=]() {
    std::cout << "x=" << x << ", y=" << y << std::endl;
};

// Capture all by reference
auto captureAllRef = [&]() {
    x = 100;
    y = 200;
};

// Mixed capture
auto mixed = [x, &y]() {
    // x by value, y by reference
    y = 99;
};

// Generic lambda (C++14)
auto genericAdd = [](auto a, auto b) {
    return a + b;
};
```

### 9. constexpr Functions
```cpp
// Can be evaluated at compile time
constexpr int square(int x) {
    return x * x;
}

constexpr int result = square(5);  // Evaluated at compile time

// Also works at runtime
int runtimeValue = 7;
int runtimeResult = square(runtimeValue);

// constexpr lambda (C++17)
constexpr auto constexprSquare = [](int x) {
    return x * x;
};
```

### 10. [[nodiscard]] Attribute (C++17)
```cpp
// Warns if return value is ignored
[[nodiscard]] int getValue() {
    return 42;
}

int x = getValue();  // OK
getValue();          // Warning: ignoring return value
```

### 11. Return Types and Multiple Values
```cpp
// Returning struct for multiple values
struct Result {
    int sum;
    int product;
};

Result calculate(int a, int b) {
    return {a + b, a * b};
}

// C++17: Structured binding
auto [sum, product] = calculate(5, 3);

// Returning reference
int& getElement(std::vector<int>& vec, int index) {
    return vec[index];
}

std::vector<int> numbers = {1, 2, 3};
getElement(numbers, 0) = 100;  // Modifies through reference
```

## Best Practices
1. **Use meaningful function names** (verbs for actions)
2. **Keep functions small and focused** (single responsibility principle)
3. **Pass large objects by const reference** to avoid copying
4. **Prefer references over pointers** when possible
5. **Use const correctness** (const parameters, const member functions)
6. **Document complex functions** with comments
7. **Avoid too many parameters** (consider using structs/classes)
8. **Use [[nodiscard]]** for functions where ignoring return value is an error
9. **Prefer lambdas** for small, local functions
10. **Use constexpr** for compile-time computations
11. **Be careful with recursion** (stack overflow risk)
12. **Prefer function overloading** over default parameters for clarity

## Common Patterns

### Swap Function
```cpp
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}
```

### Validation Function
```cpp
bool isValid(const std::string& input) {
    return !input.empty() && input.length() <= 100;
}
```

### Factory Function
```cpp
std::unique_ptr<Widget> createWidget(WidgetType type) {
    switch (type) {
        case WidgetType::Button:
            return std::make_unique<Button>();
        case WidgetType::Label:
            return std::make_unique<Label>();
        default:
            return nullptr;
    }
}
```

## Resources and References
- [cppreference.com - Functions](https://en.cppreference.com/w/cpp/language/functions)
- [cppreference.com - Lambda expressions](https://en.cppreference.com/w/cpp/language/lambda)
- [cppreference.com - constexpr](https://en.cppreference.com/w/cpp/language/constexpr)
- [C++ Core Guidelines - Functions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-functions)

## Navigation
- **Previous Program**: [105 - Loops](../105_loops/README.md)
- **Next Program**: [107 - Arrays](../107_arrays/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
