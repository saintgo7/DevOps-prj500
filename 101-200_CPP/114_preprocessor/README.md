# Program 114: Preprocessor Directives in C++

## Description
Comprehensive exploration of C++ preprocessor directives covering #include, #define, conditional compilation, macros, header guards, and best practices. This program demonstrates how the preprocessor works and when to use (or avoid) preprocessor features.

## Learning Objectives
- Understand preprocessor operation and phases
- Master #include directive and header management
- Work with #define macros and constants
- Use conditional compilation effectively
- Implement header guards and #pragma once
- Apply macro best practices
- Understand when to avoid macros

## Features
- File inclusion with #include
- Macro definitions and expansion
- Function-like macros
- Conditional compilation (#if, #ifdef, #ifndef)
- Predefined macros
- Header guards and include guards
- #pragma directives
- Macro debugging and inspection
- Modern alternatives to macros

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/114_preprocessor
g++ -std=c++20 -Wall -Wextra -o preprocessor main.cpp
```

### Execution
```bash
./preprocessor
```

## Key Concepts

### 1. #include Directive
```cpp
// System headers (search system directories)
#include <iostream>
#include <vector>
#include <string>

// User headers (search current directory first)
#include "myheader.h"
#include "utils/helper.h"

// Include guards prevent multiple inclusion
// myheader.h:
#ifndef MYHEADER_H
#define MYHEADER_H

// Header content...

#endif // MYHEADER_H

// Modern alternative: #pragma once
#pragma once
// Header content...
```

### 2. #define Macros
```cpp
// Object-like macros (constants)
#define PI 3.14159
#define MAX_SIZE 1000
#define BUFFER_SIZE 512

// Usage
double area = PI * radius * radius;

// Function-like macros
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// Multi-line macros (use backslash)
#define SWAP(a, b) do { \
    auto temp = a;      \
    a = b;              \
    b = temp;           \
} while(0)

// Usage
int result = SQUARE(5);      // Expands to: ((5) * (5))
int maxVal = MAX(10, 20);    // Expands to: ((10) > (20) ? (10) : (20))
```

### 3. Macro Pitfalls and Solutions
```cpp
// Problem: Side effects
#define BAD_SQUARE(x) (x * x)
int a = 5;
int result = BAD_SQUARE(a++);  // a is incremented twice!

// Solution: Proper parenthesization
#define GOOD_SQUARE(x) ((x) * (x))

// Problem: Operator precedence
#define BAD_MULT(x, y) x * y
int result = BAD_MULT(2 + 3, 4);  // Expands to: 2 + 3 * 4 = 14, not 20

// Solution: Parenthesize parameters
#define GOOD_MULT(x, y) ((x) * (y))
int result = GOOD_MULT(2 + 3, 4);  // Expands to: ((2 + 3) * (4)) = 20

// Modern C++ alternatives
constexpr double PI = 3.14159;           // Instead of #define PI
constexpr int square(int x) { return x * x; }  // Instead of macro
template<typename T>
constexpr T max(T a, T b) { return a > b ? a : b; }  // Type-safe
```

### 4. Conditional Compilation
```cpp
// #ifdef / #ifndef
#ifdef DEBUG
    std::cout << "Debug mode enabled\n";
#endif

#ifndef NDEBUG
    assert(condition);
#endif

// #if defined
#if defined(LINUX) || defined(UNIX)
    // Linux/Unix specific code
#elif defined(WINDOWS)
    // Windows specific code
#else
    // Other platforms
#endif

// Numeric conditions
#define VERSION 3

#if VERSION >= 3
    // New features
#elif VERSION == 2
    // Version 2 features
#else
    // Old features
#endif

// Defined operator
#if defined(FEATURE_A) && !defined(FEATURE_B)
    // Code when A is defined but not B
#endif

// Toggle features
#define ENABLE_LOGGING 1
#define ENABLE_PROFILING 0

#if ENABLE_LOGGING
    log("Message");
#endif
```

### 5. Predefined Macros
```cpp
// Standard predefined macros
std::cout << "File: " << __FILE__ << '\n';        // Current file name
std::cout << "Line: " << __LINE__ << '\n';        // Current line number
std::cout << "Date: " << __DATE__ << '\n';        // Compilation date
std::cout << "Time: " << __TIME__ << '\n';        // Compilation time
std::cout << "Function: " << __func__ << '\n';    // Current function name

// C++ version
#if __cplusplus >= 202002L
    std::cout << "C++20 or later\n";
#elif __cplusplus >= 201703L
    std::cout << "C++17\n";
#elif __cplusplus >= 201402L
    std::cout << "C++14\n";
#elif __cplusplus >= 201103L
    std::cout << "C++11\n";
#endif

// Compiler detection
#ifdef _MSC_VER
    // Microsoft Visual C++
#endif

#ifdef __GNUC__
    // GCC
#endif

#ifdef __clang__
    // Clang
#endif

// Platform detection
#ifdef __linux__
    // Linux
#endif

#ifdef _WIN32
    // Windows (32-bit or 64-bit)
#endif

#ifdef __APPLE__
    // macOS
#endif
```

### 6. #pragma Directives
```cpp
// Pragma once (include guard alternative)
#pragma once

// Warning control
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-variable"
int unusedVar;
#pragma GCC diagnostic pop

// Pack structures
#pragma pack(push, 1)
struct PackedStruct {
    char c;
    int i;
};
#pragma pack(pop)

// Optimization hints
#pragma GCC optimize("O3")
#pragma GCC optimize("unroll-loops")

// Message during compilation
#pragma message("Compiling with special features")

// Platform-specific
#ifdef _MSC_VER
    #pragma warning(disable : 4996)  // Disable specific warning
#endif
```

### 7. Stringification and Token Pasting
```cpp
// Stringification: # operator converts to string
#define STRINGIFY(x) #x
#define TO_STRING(x) STRINGIFY(x)

int value = 42;
std::cout << STRINGIFY(value) << '\n';  // Prints: "value"
std::cout << TO_STRING(100) << '\n';    // Prints: "100"

// Token pasting: ## operator concatenates tokens
#define CONCAT(a, b) a##b

int CONCAT(var, 1) = 10;  // Creates variable: var1
int CONCAT(var, 2) = 20;  // Creates variable: var2

// Practical example: creating getters/setters
#define PROPERTY(type, name) \
private:                     \
    type m_##name;          \
public:                      \
    type get##name() const { return m_##name; } \
    void set##name(type value) { m_##name = value; }

class MyClass {
    PROPERTY(int, Age)
    PROPERTY(std::string, Name)
};
// Expands to getter/setter methods
```

### 8. Variadic Macros
```cpp
// Variadic macro with __VA_ARGS__
#define LOG(format, ...) \
    printf("[%s:%d] " format "\n", __FILE__, __LINE__, __VA_ARGS__)

LOG("Value: %d, String: %s", 42, "test");

// Debug macro
#ifdef DEBUG
    #define DEBUG_PRINT(fmt, ...) \
        fprintf(stderr, "DEBUG: %s:%d:%s(): " fmt "\n", \
                __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
    #define DEBUG_PRINT(fmt, ...) do {} while(0)
#endif

// Usage
DEBUG_PRINT("Starting process");
DEBUG_PRINT("Value is %d", value);

// Macro with variable arguments
#define CALL_FUNCTION(func, ...) \
    func(__VA_ARGS__)
```

### 9. Conditional Feature Detection
```cpp
// Feature test macros (C++20)
#ifdef __cpp_concepts
    std::cout << "Concepts supported\n";
#endif

#ifdef __cpp_constexpr
    std::cout << "constexpr supported\n";
#endif

#ifdef __cpp_modules
    std::cout << "Modules supported\n";
#endif

// Custom feature flags
#define FEATURE_DATABASE     1
#define FEATURE_NETWORKING   1
#define FEATURE_GRAPHICS     0

#if FEATURE_DATABASE
    #include "database.h"
#endif

#if FEATURE_NETWORKING
    #include "network.h"
#endif
```

## Best Practices
1. **Prefer constexpr over #define** for constants
2. **Use inline functions or templates** instead of function-like macros
3. **Always use #pragma once** or include guards
4. **Parenthesize macro parameters** to avoid precedence issues
5. **Use ALL_CAPS** for macro names
6. **Avoid side effects** in macro arguments
7. **Use do-while(0)** wrapper for multi-statement macros
8. **Document macro behavior** clearly
9. **Use #ifdef for feature detection** not #if
10. **Minimize preprocessor usage** in modern C++

## Modern C++ Alternatives
```cpp
// Instead of #define constants
// Old: #define MAX_SIZE 100
constexpr int MAX_SIZE = 100;

// Instead of function-like macros
// Old: #define SQUARE(x) ((x) * (x))
constexpr int square(int x) { return x * x; }

// Instead of type-unsafe macros
// Old: #define MAX(a, b) ((a) > (b) ? (a) : (b))
template<typename T>
constexpr T max(T a, T b) { return a > b ? a : b; }

// Instead of conditional compilation for debugging
// Old: #ifdef DEBUG ... #endif
if constexpr (DEBUG_MODE) {
    // Debug code
}

// Instead of include guards
// Old: #ifndef HEADER_H #define HEADER_H ... #endif
#pragma once
```

## Resources and References
- [cppreference.com - Preprocessor](https://en.cppreference.com/w/cpp/preprocessor)
- [C++ Core Guidelines - Preprocessor](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-macros)
- [GCC Preprocessor Documentation](https://gcc.gnu.org/onlinedocs/cpp/)

## Navigation
- **Previous Program**: [113 - File I/O](../113_file_io/README.md)
- **Next Program**: [115 - Namespaces](../115_namespaces/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
