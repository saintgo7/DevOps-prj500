# Program 102: Variables and Data Types

## Description
This program provides a comprehensive exploration of C++ variables and fundamental data types. It covers variable declaration, initialization, type modifiers, type inference, and the full spectrum of built-in data types available in C++.

## Learning Objectives
- Master fundamental data types (int, float, double, char, bool)
- Understand variable declaration and initialization techniques
- Learn about type modifiers (signed, unsigned, short, long)
- Explore the `auto` keyword for type inference (C++11)
- Use `decltype` for type deduction (C++11)
- Work with fixed-width integer types (C++11)
- Understand variable scope and lifetime
- Learn about literal suffixes and numeric limits

## Features
- Comprehensive demonstrations of all fundamental data types
- Type size and range exploration using `sizeof` and `std::numeric_limits`
- Modern C++ type inference with `auto` and `decltype`
- Fixed-width integer types from `<cstdint>`
- Literal notation (decimal, octal, hex, binary, scientific)
- Type aliases using `typedef` and `using`
- Variable scope and shadowing demonstrations
- Brace initialization and narrowing conversion prevention

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/102_variables_datatypes
g++ -std=c++20 -Wall -Wextra -o variables_datatypes main.cpp
```

### Execution
```bash
./variables_datatypes
```

## Key Concepts

### 1. Variable Declaration and Initialization
```cpp
// Declaration only (uninitialized - dangerous!)
int uninitializedVar;

// Declaration with initialization
int age = 25;

// Multiple declarations
int x = 10, y = 20, z = 30;

// C++11 uniform initialization (brace initialization)
int value{42};

// Prevents narrowing conversions
// int narrowed{3.14};  // Error: narrowing conversion
```

### 2. Fundamental Data Types
```cpp
bool isActive = true;           // Boolean: true or false
char letter = 'A';              // Character: single character (1 byte)
int count = 42;                 // Integer: whole numbers
float price = 19.99f;           // Single precision (4 bytes)
double distance = 384400.0;     // Double precision (8 bytes)
long double precise = 3.14L;    // Extended precision
```

### 3. Type Modifiers
```cpp
signed int signedNum = -100;            // Can be positive or negative
unsigned int unsignedNum = 100;         // Only positive values
short smallNum = 32000;                 // Smaller range
long largeNum = 2000000000L;            // Larger range
long long veryLargeNum = 9000000LL;     // Even larger range (C++11)
unsigned long long maxNum = 18446ULL;   // Combination
```

### 4. Type Inference with auto (C++11)
```cpp
auto integer = 42;              // int
auto floating = 3.14;           // double
auto character = 'x';           // char
auto boolean = true;            // bool
auto text = "Hello";            // const char*
auto message = std::string("World");  // std::string

// With explicit type specification
auto longValue = 100L;          // long
auto floatValue = 3.14f;        // float
```

### 5. decltype for Type Deduction (C++11)
```cpp
int x = 10;
decltype(x) y = 20;  // y has the same type as x (int)

auto sum = x + y;
decltype(sum) result = 100;

// decltype with expressions
double pi = 3.14;
decltype(pi * 2) doubledPi = pi * 2;
```

### 6. Fixed-Width Integer Types (C++11)
```cpp
#include <cstdint>

int8_t   i8 = 127;              // Exactly 8 bits
int16_t  i16 = 32767;           // Exactly 16 bits
int32_t  i32 = 2147483647;      // Exactly 32 bits
int64_t  i64 = 9223372LL;       // Exactly 64 bits

uint8_t  ui8 = 255;             // Unsigned 8 bits
uint16_t ui16 = 65535;          // Unsigned 16 bits
uint32_t ui32 = 4294967295U;    // Unsigned 32 bits
uint64_t ui64 = 18446744ULL;    // Unsigned 64 bits
```

### 7. Literals and Suffixes
```cpp
int decimal = 42;           // Decimal
int octal = 052;            // Octal (starts with 0)
int hex = 0x2A;             // Hexadecimal (starts with 0x)
int binary = 0b101010;      // Binary (C++14, starts with 0b)

float f = 3.14f;            // f or F suffix for float
double d = 3.14;            // No suffix for double
long double ld = 3.14L;     // L or l suffix for long double

double scientific = 1.23e4;  // 1.23 × 10^4 = 12300

// C++14: Digit separators for readability
long long bigNum = 1'000'000'000;
```

### 8. Type Aliases
```cpp
// Using typedef (C-style)
typedef unsigned long ulong;
ulong bigNumber = 1000000UL;

// Using 'using' (C++11, preferred)
using real = double;
real pi = 3.14159265359;
```

## Best Practices
1. **Always initialize variables** when declaring them
2. **Use `auto`** when the type is obvious from the initializer
3. **Use fixed-width types** (`int32_t`, etc.) when you need guaranteed sizes
4. **Prefer brace initialization** `{}` to prevent narrowing conversions
5. **Use `const`/`constexpr`** for values that don't change
6. **Choose the smallest data type** that fits your needs
7. **Use meaningful variable names** (not just `x`, `y`, `z`)
8. **Avoid global variables** when possible
9. **Be aware of integer overflow and underflow**
10. **Use unsigned types carefully** (avoid mixing signed/unsigned)

## Type Sizes and Ranges
```cpp
sizeof(bool):        1 byte
sizeof(char):        1 byte
sizeof(short):       2 bytes (typically)
sizeof(int):         4 bytes (typically)
sizeof(long):        4-8 bytes (platform-dependent)
sizeof(long long):   8 bytes
sizeof(float):       4 bytes
sizeof(double):      8 bytes
sizeof(long double): 8-16 bytes (platform-dependent)
```

## Resources and References
- [cppreference.com - Fundamental types](https://en.cppreference.com/w/cpp/language/types)
- [cppreference.com - auto](https://en.cppreference.com/w/cpp/language/auto)
- [cppreference.com - decltype](https://en.cppreference.com/w/cpp/language/decltype)
- [cppreference.com - Fixed width integer types](https://en.cppreference.com/w/cpp/types/integer)
- [C++ Core Guidelines - Type safety](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#SS-type)

## Navigation
- **Previous Program**: [101 - Hello World](../101_hello_world/README.md)
- **Next Program**: [103 - Operators](../103_operators/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
