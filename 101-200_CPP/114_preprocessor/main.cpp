/*
 * Program 114: Preprocessor Directives
 *
 * Topics Covered:
 * - #include directive
 * - #define (macros and constants)
 * - #ifdef, #ifndef, #endif (conditional compilation)
 * - #if, #elif, #else
 * - #undef
 * - Predefined macros (__FILE__, __LINE__, __DATE__, etc.)
 * - Macro functions
 * - Header guards
 * - #pragma directive
 * - Stringizing (#) and token pasting (##)
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -DDEBUG_MODE -o preprocessor main.cpp
 */

#include <iostream>

// Define constants
#define PI 3.14159
#define MAX_SIZE 100
#define VERSION "1.0.0"

// Macro functions
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// Stringizing operator (#)
#define STRINGIFY(x) #x
#define TO_STRING(x) STRINGIFY(x)

// Token pasting operator (##)
#define CONCAT(a, b) a##b

// Conditional compilation
#ifdef DEBUG_MODE
    #define DEBUG_PRINT(x) std::cout << "DEBUG: " << x << std::endl
#else
    #define DEBUG_PRINT(x)
#endif

// Feature detection
#ifndef FEATURE_ENABLED
    #define FEATURE_ENABLED 0
#endif

void demonstrateBasicMacros();
void demonstrateMacroFunctions();
void demonstrateConditionalCompilation();
void demonstratePredefinedMacros();
void demonstrateAdvancedFeatures();

int main() {
    std::cout << "=== C++ Preprocessor Directives ===" << std::endl << std::endl;

    demonstrateBasicMacros();
    demonstrateMacroFunctions();
    demonstrateConditionalCompilation();
    demonstratePredefinedMacros();
    demonstrateAdvancedFeatures();

    return 0;
}

void demonstrateBasicMacros() {
    std::cout << "--- Basic Macros ---" << std::endl;

    // Using defined constants
    std::cout << "PI: " << PI << std::endl;
    std::cout << "MAX_SIZE: " << MAX_SIZE << std::endl;
    std::cout << "VERSION: " << VERSION << std::endl;

    // Macros are text replacement
    double radius = 5.0;
    double area = PI * radius * radius;
    std::cout << "Circle area (radius=" << radius << "): " << area << std::endl;

    // Why use const instead of #define for constants
    const double PI_CONST = 3.14159;  // Type-safe, scoped
    std::cout << "\nPrefer const over #define for constants" << std::endl;

    std::cout << std::endl;
}

void demonstrateMacroFunctions() {
    std::cout << "--- Macro Functions ---" << std::endl;

    int x = 5;
    std::cout << "x = " << x << std::endl;
    std::cout << "SQUARE(" << x << ") = " << SQUARE(x) << std::endl;

    int a = 10, b = 20;
    std::cout << "MAX(" << a << ", " << b << ") = " << MAX(a, b) << std::endl;
    std::cout << "MIN(" << a << ", " << b << ") = " << MIN(a, b) << std::endl;

    // Macro pitfalls
    std::cout << "\n--- Macro Pitfalls ---" << std::endl;

    // Problem 1: Side effects
    int n = 5;
    // SQUARE(n++) would expand to ((n++) * (n++)) - Bad!
    std::cout << "SQUARE with side effects is dangerous" << std::endl;

    // Problem 2: No type checking
    std::cout << "Macros have no type checking" << std::endl;

    // Better alternatives: inline functions or templates
    auto square = [](auto x) { return x * x; };
    std::cout << "\nInline lambda square(5) = " << square(5) << std::endl;

    std::cout << std::endl;
}

void demonstrateConditionalCompilation() {
    std::cout << "--- Conditional Compilation ---" << std::endl;

    // Debug mode (enabled by -DDEBUG_MODE compiler flag)
    DEBUG_PRINT("This is a debug message");
    std::cout << "Debug messages shown if DEBUG_MODE is defined" << std::endl;

    // Platform-specific code
    #ifdef _WIN32
        std::cout << "Compiling for Windows" << std::endl;
    #elif defined(__linux__)
        std::cout << "Compiling for Linux" << std::endl;
    #elif defined(__APPLE__)
        std::cout << "Compiling for macOS" << std::endl;
    #else
        std::cout << "Unknown platform" << std::endl;
    #endif

    // C++ standard version
    #if __cplusplus >= 202002L
        std::cout << "Using C++20 or later" << std::endl;
    #elif __cplusplus >= 201703L
        std::cout << "Using C++17" << std::endl;
    #elif __cplusplus >= 201402L
        std::cout << "Using C++14" << std::endl;
    #elif __cplusplus >= 201103L
        std::cout << "Using C++11" << std::endl;
    #else
        std::cout << "Using pre-C++11" << std::endl;
    #endif

    // Feature flags
    #if FEATURE_ENABLED
        std::cout << "Feature is enabled" << std::endl;
    #else
        std::cout << "Feature is disabled" << std::endl;
    #endif

    std::cout << std::endl;
}

void demonstratePredefinedMacros() {
    std::cout << "--- Predefined Macros ---" << std::endl;

    // File and line information
    std::cout << "File: " << __FILE__ << std::endl;
    std::cout << "Line: " << __LINE__ << std::endl;
    std::cout << "Function: " << __func__ << std::endl;  // C++11

    // Compilation date and time
    std::cout << "\nCompilation info:" << std::endl;
    std::cout << "Date: " << __DATE__ << std::endl;
    std::cout << "Time: " << __TIME__ << std::endl;

    // C++ standard version
    std::cout << "\n__cplusplus: " << __cplusplus << std::endl;

    // Compiler information
    #ifdef __GNUC__
        std::cout << "GCC version: " << __GNUC__ << "." << __GNUC_MINOR__ << std::endl;
    #endif

    #ifdef _MSC_VER
        std::cout << "MSVC version: " << _MSC_VER << std::endl;
    #endif

    #ifdef __clang__
        std::cout << "Clang version: " << __clang_major__ << "." << __clang_minor__ << std::endl;
    #endif

    std::cout << std::endl;
}

void demonstrateAdvancedFeatures() {
    std::cout << "--- Advanced Preprocessor Features ---" << std::endl;

    // Stringizing (#)
    std::cout << "Stringizing:" << std::endl;
    std::cout << "STRINGIFY(Hello): " << STRINGIFY(Hello) << std::endl;
    std::cout << "TO_STRING(123): " << TO_STRING(123) << std::endl;

    // Token pasting (##)
    std::cout << "\nToken pasting:" << std::endl;
    int value1 = 10;
    int value2 = 20;
    std::cout << "CONCAT(value, 1) = " << CONCAT(value, 1) << std::endl;
    std::cout << "CONCAT(value, 2) = " << CONCAT(value, 2) << std::endl;

    // Variadic macros (C++11)
    #define LOG(format, ...) printf(format "\n", __VA_ARGS__)

    // #undef to undefine macros
    #undef PI
    // PI is no longer defined

    // #pragma directive
    #pragma message("This is a compilation message")

    // Common pragmas:
    // #pragma once                    - Include guard (non-standard but widely supported)
    // #pragma GCC diagnostic          - GCC-specific warnings
    // #pragma warning                 - MSVC-specific warnings
    // #pragma pack                    - Structure packing

    std::cout << std::endl;
}

/*
 * Header Guards Pattern:
 *
 * // myheader.h
 * #ifndef MYHEADER_H
 * #define MYHEADER_H
 *
 * // Header content here
 *
 * #endif // MYHEADER_H
 *
 * Modern alternative (widely supported but non-standard):
 * #pragma once
 *
 * Best Practices:
 * 1. Prefer const/constexpr over #define for constants
 * 2. Prefer inline functions/templates over macro functions
 * 3. Use header guards or #pragma once
 * 4. Be careful with macro side effects
 * 5. Always parenthesize macro parameters
 * 6. Use #ifdef for conditional compilation
 * 7. Document complex macros thoroughly
 * 8. Avoid using macros when language features can do the job
 * 9. Use predefined macros for debugging
 * 10. Be aware that macros don't respect scope
 * 11. Use all caps for macro names
 * 12. Prefer feature detection over platform detection
 */
