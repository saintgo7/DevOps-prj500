# Program 103: Operators in C++

## Description
A comprehensive exploration of all operator types available in C++, including arithmetic, comparison, logical, bitwise, assignment, and the modern three-way comparison operator (C++20). This program demonstrates operator usage, precedence, associativity, and practical applications.

## Learning Objectives
- Master arithmetic operators (+, -, *, /, %)
- Understand comparison/relational operators (==, !=, <, >, <=, >=)
- Learn logical operators (&&, ||, !) and short-circuit evaluation
- Explore bitwise operators (&, |, ^, ~, <<, >>)
- Use assignment operators (=, +=, -=, *=, /=, %=, etc.)
- Understand increment/decrement operators (++, --)
- Apply the ternary/conditional operator (?:)
- Learn the three-way comparison operator (<=>) in C++20
- Comprehend operator precedence and associativity

## Features
- Complete coverage of all C++ operators
- Practical examples for each operator category
- Bitwise operations with binary flag management
- Short-circuit evaluation demonstrations
- Truth tables for logical operators
- Operator precedence reference
- Three-way comparison (spaceship operator) examples
- Common use cases and patterns

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/103_operators
g++ -std=c++20 -Wall -Wextra -o operators main.cpp
```

### Execution
```bash
./operators
```

## Key Concepts

### 1. Arithmetic Operators
```cpp
int a = 15, b = 4;

a + b   // Addition: 19
a - b   // Subtraction: 11
a * b   // Multiplication: 60
a / b   // Integer division: 3
a % b   // Modulus (remainder): 3

+a      // Unary plus
-a      // Unary minus (negation)
```

### 2. Comparison/Relational Operators
```cpp
int a = 10, b = 20;

a == b  // Equal to: false
a != b  // Not equal to: true
a < b   // Less than: true
a > b   // Greater than: false
a <= b  // Less than or equal to: true
a >= b  // Greater than or equal to: false
```

### 3. Logical Operators
```cpp
bool p = true, q = false;

p && q  // Logical AND: false
p || q  // Logical OR: true
!p      // Logical NOT: false

// Short-circuit evaluation
false && (++x > 0)  // x is not incremented
true || (++y > 0)   // y is not incremented
```

### 4. Bitwise Operators
```cpp
unsigned int a = 60;  // Binary: 0011 1100
unsigned int b = 13;  // Binary: 0000 1101

a & b   // AND:  0000 1100 = 12
a | b   // OR:   0011 1101 = 61
a ^ b   // XOR:  0011 0001 = 49
~a      // NOT:  inverted bits
a << 2  // Left shift:  1111 0000 = 240
a >> 2  // Right shift: 0000 1111 = 15

// Practical use: Flag management
unsigned int flags = 0;
unsigned int FLAG_READ = 1 << 0;   // 0001
unsigned int FLAG_WRITE = 1 << 1;  // 0010

flags |= FLAG_READ;           // Set flag
bool canRead = (flags & FLAG_READ) != 0;  // Check flag
flags &= ~FLAG_WRITE;         // Clear flag
flags ^= FLAG_READ;           // Toggle flag
```

### 5. Assignment Operators
```cpp
int x = 10;

x += 5   // x = x + 5  ’  15
x -= 3   // x = x - 3  ’  12
x *= 2   // x = x * 2  ’  24
x /= 4   // x = x / 4  ’  6
x %= 3   // x = x % 3  ’  0

// Bitwise assignment
y &= 13  // y = y & 13
y |= 5   // y = y | 5
y ^= 3   // y = y ^ 3
y <<= 2  // y = y << 2
y >>= 1  // y = y >> 1
```

### 6. Increment and Decrement Operators
```cpp
int a = 5, b = 5;

++a      // Pre-increment: increment first, then use (a becomes 6, returns 6)
a++      // Post-increment: use first, then increment (returns 5, a becomes 6)

--a      // Pre-decrement: decrement first, then use
a--      // Post-decrement: use first, then decrement

// Practical example
int arr[] = {1, 2, 3, 4, 5};
int i = 0;
arr[i++]  // Uses arr[0], then increments i to 1
arr[++i]  // Increments i to 2, then uses arr[2]
```

### 7. Ternary/Conditional Operator
```cpp
// Syntax: condition ? value_if_true : value_if_false
int max = (a > b) ? a : b;
int min = (a < b) ? a : b;

// Nested ternary (use sparingly)
std::string category = (x < 10) ? "small" :
                      (x < 20) ? "medium" : "large";

// Common use case
bool isDark = true;
std::string theme = isDark ? "dark-theme" : "light-theme";
```

### 8. Three-Way Comparison Operator (C++20)
```cpp
#include <compare>

int a = 10, b = 20, c = 10;

auto cmp1 = a <=> b;   // Returns: < 0 (less)
auto cmp2 = a <=> c;   // Returns: == 0 (equal)
auto cmp3 = b <=> a;   // Returns: > 0 (greater)

if (cmp1 < 0) { /* a is less than b */ }
if (cmp2 == 0) { /* a equals c */ }
if (cmp3 > 0) { /* b is greater than a */ }

// Works with strings
std::string str1 = "apple", str2 = "banana";
auto strCmp = str1 <=> str2;  // Lexicographic comparison
```

### 9. Operator Precedence (high to low)
```
1. () [] -> .
2. ++ -- (postfix)
3. ++ -- (prefix) ! ~ + - * & sizeof
4. * / %
5. + -
6. << >>
7. < <= > >=
8. == !=
9. &
10. ^
11. |
12. &&
13. ||
14. ?:
15. = += -= *= /= %= etc.
16. ,
```

## Best Practices
1. **Use parentheses** to make complex expressions clear
2. **Prefer pre-increment** (++i) over post-increment (i++) when the value isn't used
3. **Be careful with operator precedence** - use parentheses when in doubt
4. **Avoid too many operators** in a single expression
5. **Use compound assignment operators** (+=, *=, etc.) for clarity
6. **Be aware of short-circuit evaluation** in logical operators
7. **Use bitwise operators** for flags and low-level operations
8. **Prefer ternary operator** only for simple conditional assignments
9. **Don't overuse the comma operator** outside of for loops
10. **Use C++20's spaceship operator** for consistent comparisons

## Common Pitfalls
- Mixing up `=` (assignment) with `==` (comparison)
- Not understanding operator precedence
- Using bitwise operators when logical operators are intended (`&` vs `&&`)
- Integer division truncation: `5 / 2` = 2, not 2.5
- Overflow with unsigned arithmetic
- Undefined behavior with division by zero
- Pre-increment vs post-increment in complex expressions

## Resources and References
- [cppreference.com - Operators](https://en.cppreference.com/w/cpp/language/operators)
- [cppreference.com - Operator precedence](https://en.cppreference.com/w/cpp/language/operator_precedence)
- [cppreference.com - Three-way comparison](https://en.cppreference.com/w/cpp/language/operator_comparison#Three-way_comparison)
- [C++ Core Guidelines - Expressions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-expr)

## Navigation
- **Previous Program**: [102 - Variables and Data Types](../102_variables_datatypes/README.md)
- **Next Program**: [104 - Control Flow](../104_control_flow/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
