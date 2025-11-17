# Program 104: Control Flow

## Description
A comprehensive guide to control flow statements in C++, covering decision-making constructs like if-else, switch statements, and modern C++17/C++20 enhancements. This program demonstrates how to control program execution flow based on conditions.

## Learning Objectives
- Master `if`, `if-else`, and `else-if` ladder statements
- Understand nested if statements and their applications
- Learn `switch` statement syntax and use cases
- Explore switch fall-through behavior and `[[fallthrough]]` attribute (C++17)
- Apply the ternary operator for simple conditionals
- Use `if` with initializer (C++17)
- Understand `constexpr if` for compile-time branching (C++17)
- Recognize when to avoid `goto` statements

## Features
- Complete if statement variations (simple, if-else, else-if ladder, nested)
- Switch statement demonstrations with multiple patterns
- Fall-through examples with C++17 `[[fallthrough]]` attribute
- Ternary operator usage and nested ternary examples
- C++17 if with initializer for scoped variables
- constexpr if for compile-time conditional compilation
- Practical examples: login validation, grading systems, calculators
- goto statement explanation (anti-pattern)

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/104_control_flow
g++ -std=c++20 -Wall -Wextra -o control_flow main.cpp
```

### Execution
```bash
./control_flow
```

## Key Concepts

### 1. if Statement
```cpp
// Simple if
if (age >= 18) {
    std::cout << "You are an adult" << std::endl;
}

// Compound condition
if (hasLicense && age >= 18) {
    std::cout << "You can drive" << std::endl;
}
```

### 2. if-else Statement
```cpp
if (number % 2 == 0) {
    std::cout << number << " is even" << std::endl;
} else {
    std::cout << number << " is odd" << std::endl;
}
```

### 3. else-if Ladder
```cpp
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
```

### 4. Nested if Statements
```cpp
if (age >= 18) {
    if (hasTicket) {
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
```

### 5. switch Statement
```cpp
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
    // ... more cases
    default:
        std::cout << "Invalid day" << std::endl;
        break;
}
```

### 6. switch with Fall-through
```cpp
int month = 2;

// Multiple cases for same output
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

// Intentional fall-through with [[fallthrough]] (C++17)
switch (value) {
    case 1:
        std::cout << "Case 1" << std::endl;
        [[fallthrough]];  // Explicitly indicate intentional fall-through
    case 2:
        std::cout << "Case 2 (or fell through from 1)" << std::endl;
        break;
}
```

### 7. Ternary Operator
```cpp
// Syntax: condition ? value_if_true : value_if_false
std::string status = (age >= 18) ? "Adult" : "Minor";

// Finding max
int max = (a > b) ? a : b;

// Nested ternary (use sparingly!)
std::string grade = (score >= 90) ? "A" :
                   (score >= 80) ? "B" :
                   (score >= 70) ? "C" :
                   (score >= 60) ? "D" : "F";
```

### 8. if with Initializer (C++17)
```cpp
// Variable is scoped to the if-else block
if (int value = 42; value > 0) {
    std::cout << "Value is positive: " << value << std::endl;
}
// value is not accessible here

// Useful for checking function returns, map lookups, etc.
if (auto result = someFunction(); result == SUCCESS) {
    std::cout << "Operation succeeded" << std::endl;
} else {
    std::cout << "Operation failed: " << result << std::endl;
}

// Checking status codes
auto getStatus = []() { return 200; };

if (auto status = getStatus(); status == 200) {
    std::cout << "HTTP OK" << std::endl;
} else if (status == 404) {
    std::cout << "Not Found" << std::endl;
} else {
    std::cout << "Other status: " << status << std::endl;
}
```

### 9. constexpr if (C++17)
```cpp
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
// Very useful for template metaprogramming
```

### 10. goto Statement (Avoid!)
```cpp
// Example (for educational purposes only - DON'T USE!)
int counter = 0;
start:
    if (counter < 3) {
        std::cout << "Counter: " << counter << std::endl;
        counter++;
        goto start;  // Jump back to label
    }

// Better alternatives: use loops and functions instead!
```

## Best Practices
1. **Always use braces `{}`** for if statements, even for single statements
2. **Prefer switch over long else-if ladders** for discrete values
3. **Use ternary operator only for simple conditions** (avoid complex nested ternary)
4. **Avoid deeply nested if statements** - consider refactoring into functions
5. **Put the most likely condition first** in else-if chains (optimization)
6. **Always include a default case** in switch statements
7. **Use `[[fallthrough]]`** to indicate intentional fall-through in switch
8. **Avoid using goto** - use structured control flow instead
9. **Use if with initializer (C++17)** to limit variable scope
10. **Consider constexpr if** for compile-time decisions
11. **Keep conditions simple and readable** - extract complex conditions to variables
12. **Use early returns** to reduce nesting depth

## Common Patterns

### Login Validation
```cpp
if (username == "admin") {
    if (password == "secret") {
        if (accountActive) {
            std::cout << "Login successful" << std::endl;
        } else {
            std::cout << "Account inactive" << std::endl;
        }
    } else {
        std::cout << "Incorrect password" << std::endl;
    }
} else {
    std::cout << "User not found" << std::endl;
}
```

### Calculator
```cpp
switch (operation) {
    case '+':
        result = a + b;
        break;
    case '-':
        result = a - b;
        break;
    case '*':
        result = a * b;
        break;
    case '/':
        if (b != 0) {
            result = a / b;
        } else {
            std::cout << "Division by zero!" << std::endl;
        }
        break;
    default:
        std::cout << "Invalid operation" << std::endl;
}
```

## Resources and References
- [cppreference.com - if statement](https://en.cppreference.com/w/cpp/language/if)
- [cppreference.com - switch statement](https://en.cppreference.com/w/cpp/language/switch)
- [cppreference.com - Conditional operator](https://en.cppreference.com/w/cpp/language/operator_other#Conditional_operator)
- [C++17 - if with initializer](https://en.cppreference.com/w/cpp/language/if#If_Statements_with_Initializer)
- [C++17 - constexpr if](https://en.cppreference.com/w/cpp/language/if#Constexpr_If)

## Navigation
- **Previous Program**: [103 - Operators](../103_operators/README.md)
- **Next Program**: [105 - Loops](../105_loops/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
