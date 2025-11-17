/*
 * Program 102: Variables and Data Types
 *
 * Topics Covered:
 * - Fundamental data types (int, float, double, char, bool)
 * - Variable declaration and initialization
 * - Type modifiers (signed, unsigned, short, long)
 * - Size of data types (sizeof operator)
 * - Type inference with auto keyword (C++11)
 * - decltype for type deduction (C++11)
 * - Literal suffixes (L, U, F, etc.)
 * - Fixed-width integer types (C++11)
 * - Variable scope and lifetime
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o variables_datatypes main.cpp
 */

#include <iostream>
#include <iomanip>   // For std::setprecision
#include <limits>    // For std::numeric_limits
#include <cstdint>   // For fixed-width integer types
#include <string>

void demonstrateFundamentalTypes();
void demonstrateTypeModifiers();
void demonstrateAutoKeyword();
void demonstrateTypeInference();
void demonstrateLiterals();
void demonstrateFixedWidthTypes();
void demonstrateScope();

int main() {
    std::cout << "=== C++ Variables and Data Types ===" << std::endl;
    std::cout << std::endl;

    // ============================================================
    // 1. Basic Variable Declaration and Initialization
    // ============================================================

    std::cout << "--- Basic Variable Declaration ---" << std::endl;

    // Declaration only (uninitialized - contains garbage value)
    int uninitializedVar;

    // Declaration with initialization
    int age = 25;
    std::cout << "Age: " << age << std::endl;

    // Multiple declarations
    int x = 10, y = 20, z = 30;
    std::cout << "x = " << x << ", y = " << y << ", z = " << z << std::endl;

    // C++11 uniform initialization (brace initialization)
    int value{42};
    std::cout << "Value (brace init): " << value << std::endl;

    // Prevents narrowing conversions
    // int narrowed{3.14};  // Error: narrowing conversion

    std::cout << std::endl;

    // ============================================================
    // 2. Fundamental Data Types
    // ============================================================

    demonstrateFundamentalTypes();

    // ============================================================
    // 3. Type Modifiers
    // ============================================================

    demonstrateTypeModifiers();

    // ============================================================
    // 4. sizeof Operator
    // ============================================================

    std::cout << "--- Size of Data Types (bytes) ---" << std::endl;
    std::cout << "sizeof(bool):        " << sizeof(bool) << std::endl;
    std::cout << "sizeof(char):        " << sizeof(char) << std::endl;
    std::cout << "sizeof(short):       " << sizeof(short) << std::endl;
    std::cout << "sizeof(int):         " << sizeof(int) << std::endl;
    std::cout << "sizeof(long):        " << sizeof(long) << std::endl;
    std::cout << "sizeof(long long):   " << sizeof(long long) << std::endl;
    std::cout << "sizeof(float):       " << sizeof(float) << std::endl;
    std::cout << "sizeof(double):      " << sizeof(double) << std::endl;
    std::cout << "sizeof(long double): " << sizeof(long double) << std::endl;
    std::cout << std::endl;

    // ============================================================
    // 5. Type Ranges using std::numeric_limits
    // ============================================================

    std::cout << "--- Type Ranges ---" << std::endl;
    std::cout << "int min: " << std::numeric_limits<int>::min() << std::endl;
    std::cout << "int max: " << std::numeric_limits<int>::max() << std::endl;
    std::cout << "unsigned int max: " << std::numeric_limits<unsigned int>::max() << std::endl;
    std::cout << "float min: " << std::numeric_limits<float>::min() << std::endl;
    std::cout << "float max: " << std::numeric_limits<float>::max() << std::endl;
    std::cout << "double digits: " << std::numeric_limits<double>::digits10 << std::endl;
    std::cout << std::endl;

    // ============================================================
    // 6. Auto Keyword (Type Inference)
    // ============================================================

    demonstrateAutoKeyword();

    // ============================================================
    // 7. Type Inference with decltype
    // ============================================================

    demonstrateTypeInference();

    // ============================================================
    // 8. Literals and Suffixes
    // ============================================================

    demonstrateLiterals();

    // ============================================================
    // 9. Fixed-Width Integer Types (C++11)
    // ============================================================

    demonstrateFixedWidthTypes();

    // ============================================================
    // 10. Variable Scope and Lifetime
    // ============================================================

    demonstrateScope();

    // ============================================================
    // 11. Constants
    // ============================================================

    std::cout << "--- Constants ---" << std::endl;

    const int MAX_SIZE = 100;  // Compile-time constant
    std::cout << "MAX_SIZE (const): " << MAX_SIZE << std::endl;

    // MAX_SIZE = 200;  // Error: cannot modify const variable

    constexpr int COMPILE_TIME_VALUE = 50;  // C++11: guaranteed compile-time constant
    std::cout << "COMPILE_TIME_VALUE (constexpr): " << COMPILE_TIME_VALUE << std::endl;

    std::cout << std::endl;

    // ============================================================
    // 12. Type Aliases
    // ============================================================

    std::cout << "--- Type Aliases ---" << std::endl;

    // Using typedef (C-style)
    typedef unsigned long ulong;
    ulong bigNumber = 1000000UL;
    std::cout << "bigNumber (typedef): " << bigNumber << std::endl;

    // Using 'using' (C++11, preferred)
    using real = double;
    real pi = 3.14159265359;
    std::cout << "pi (using alias): " << std::setprecision(12) << pi << std::endl;

    std::cout << std::endl;

    return 0;
}

/**
 * Demonstrates fundamental data types
 */
void demonstrateFundamentalTypes() {
    std::cout << "--- Fundamental Data Types ---" << std::endl;

    // Boolean type (true or false)
    bool isActive = true;
    bool isEnabled = false;
    std::cout << "Boolean: " << std::boolalpha << isActive << ", " << isEnabled << std::endl;

    // Character type (single character, 1 byte)
    char letter = 'A';
    char digit = '5';
    std::cout << "Character: " << letter << ", " << digit << std::endl;

    // Integer type (whole numbers)
    int count = 42;
    std::cout << "Integer: " << count << std::endl;

    // Floating-point types (decimal numbers)
    float price = 19.99f;           // Single precision (4 bytes)
    double distance = 384400.0;     // Double precision (8 bytes)
    long double precise = 3.14159265358979323846L;  // Extended precision

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Float: " << price << std::endl;
    std::cout << "Double: " << distance << std::endl;
    std::cout << std::setprecision(20);
    std::cout << "Long Double: " << precise << std::endl;

    // Void type (no type)
    // Used for functions that don't return a value
    // Cannot declare variables of type void

    std::cout << std::endl;
}

/**
 * Demonstrates type modifiers
 */
void demonstrateTypeModifiers() {
    std::cout << "--- Type Modifiers ---" << std::endl;

    // Signed (can be positive or negative) - default for int
    signed int signedNum = -100;
    std::cout << "Signed int: " << signedNum << std::endl;

    // Unsigned (only positive values)
    unsigned int unsignedNum = 100;
    std::cout << "Unsigned int: " << unsignedNum << std::endl;

    // Short (smaller range)
    short smallNum = 32000;
    std::cout << "Short: " << smallNum << std::endl;

    // Long (larger range)
    long largeNum = 2000000000L;
    std::cout << "Long: " << largeNum << std::endl;

    // Long long (even larger range, C++11)
    long long veryLargeNum = 9000000000000000000LL;
    std::cout << "Long long: " << veryLargeNum << std::endl;

    // Combinations
    unsigned long long maxNum = 18446744073709551615ULL;
    std::cout << "Unsigned long long max: " << maxNum << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates auto keyword for type inference
 */
void demonstrateAutoKeyword() {
    std::cout << "--- Auto Keyword (Type Inference) ---" << std::endl;

    // Compiler deduces the type from initializer
    auto integer = 42;              // int
    auto floating = 3.14;           // double
    auto character = 'x';           // char
    auto boolean = true;            // bool
    auto text = "Hello";            // const char*
    auto message = std::string("World");  // std::string

    std::cout << "auto integer: " << integer << std::endl;
    std::cout << "auto floating: " << floating << std::endl;
    std::cout << "auto character: " << character << std::endl;
    std::cout << "auto boolean: " << std::boolalpha << boolean << std::endl;
    std::cout << "auto text: " << text << std::endl;
    std::cout << "auto message: " << message << std::endl;

    // auto with explicit type specification
    auto longValue = 100L;          // long
    auto floatValue = 3.14f;        // float

    std::cout << "auto long: " << longValue << std::endl;
    std::cout << "auto float: " << floatValue << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates decltype for type deduction
 */
void demonstrateTypeInference() {
    std::cout << "--- decltype (Type Deduction) ---" << std::endl;

    int x = 10;
    decltype(x) y = 20;  // y has the same type as x (int)

    std::cout << "x: " << x << ", y: " << y << std::endl;

    auto sum = x + y;
    decltype(sum) result = 100;

    std::cout << "sum: " << sum << ", result: " << result << std::endl;

    // decltype with expressions
    double pi = 3.14;
    decltype(pi * 2) doubledPi = pi * 2;
    std::cout << "doubledPi: " << doubledPi << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates literals and suffixes
 */
void demonstrateLiterals() {
    std::cout << "--- Literals and Suffixes ---" << std::endl;

    // Integer literals
    int decimal = 42;           // Decimal
    int octal = 052;            // Octal (starts with 0)
    int hex = 0x2A;             // Hexadecimal (starts with 0x)
    int binary = 0b101010;      // Binary (C++14, starts with 0b)

    std::cout << "Decimal: " << decimal << std::endl;
    std::cout << "Octal: " << octal << std::endl;
    std::cout << "Hex: " << hex << std::endl;
    std::cout << "Binary: " << binary << std::endl;

    // Floating-point literals
    float f = 3.14f;            // f or F suffix for float
    double d = 3.14;            // No suffix for double
    long double ld = 3.14L;     // L or l suffix for long double

    // Scientific notation
    double scientific = 1.23e4;  // 1.23 × 10^4 = 12300

    std::cout << "Scientific: " << scientific << std::endl;

    // Character literals
    char ch = 'A';              // Regular character
    char newline = '\n';        // Escape sequence
    char tab = '\t';            // Tab
    char unicode = '\u0041';    // Unicode (A)

    // String literals
    const char* cString = "C-style string";
    std::string cppString = "C++ string";

    // C++14: Digit separators for readability
    long long bigNum = 1'000'000'000;
    std::cout << "Big number with separators: " << bigNum << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates fixed-width integer types
 */
void demonstrateFixedWidthTypes() {
    std::cout << "--- Fixed-Width Integer Types (C++11) ---" << std::endl;

    // Exact width types (guaranteed size)
    int8_t   i8 = 127;           // Exactly 8 bits
    int16_t  i16 = 32767;        // Exactly 16 bits
    int32_t  i32 = 2147483647;   // Exactly 32 bits
    int64_t  i64 = 9223372036854775807LL;  // Exactly 64 bits

    uint8_t  ui8 = 255;          // Unsigned 8 bits
    uint16_t ui16 = 65535;       // Unsigned 16 bits
    uint32_t ui32 = 4294967295U; // Unsigned 32 bits
    uint64_t ui64 = 18446744073709551615ULL;  // Unsigned 64 bits

    std::cout << "int8_t: " << static_cast<int>(i8) << std::endl;
    std::cout << "int16_t: " << i16 << std::endl;
    std::cout << "int32_t: " << i32 << std::endl;
    std::cout << "int64_t: " << i64 << std::endl;

    std::cout << "uint8_t: " << static_cast<unsigned>(ui8) << std::endl;
    std::cout << "uint16_t: " << ui16 << std::endl;

    // Size verification
    std::cout << "sizeof(int32_t): " << sizeof(int32_t) << " bytes" << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates variable scope and lifetime
 */
void demonstrateScope() {
    std::cout << "--- Variable Scope and Lifetime ---" << std::endl;

    int globalScope = 100;
    std::cout << "Outer scope: " << globalScope << std::endl;

    {
        // Inner scope (block)
        int innerScope = 200;
        std::cout << "Inner scope: " << innerScope << std::endl;
        std::cout << "Can access outer: " << globalScope << std::endl;

        // Shadowing (not recommended)
        int globalScope = 300;  // Shadows the outer variable
        std::cout << "Shadowed variable: " << globalScope << std::endl;
    }

    // innerScope is not accessible here
    // std::cout << innerScope << std::endl;  // Error

    std::cout << "Back to outer scope: " << globalScope << std::endl;

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Always initialize variables when declaring them
 * 2. Use auto when the type is obvious from the initializer
 * 3. Use fixed-width types when you need guaranteed sizes
 * 4. Prefer brace initialization {} to prevent narrowing
 * 5. Use const/constexpr for values that don't change
 * 6. Choose the smallest data type that fits your needs
 * 7. Use meaningful variable names
 * 8. Avoid global variables when possible
 * 9. Be aware of integer overflow and underflow
 * 10. Use unsigned types carefully (avoid mixing signed/unsigned)
 */
