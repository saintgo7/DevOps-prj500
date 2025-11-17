# Program 109: References in C++

## Description
Comprehensive exploration of references in C++ covering reference basics, lvalue references, rvalue references (C++11), reference vs pointer comparison, passing by reference, returning references, and reference best practices. This program demonstrates how references provide safer and more convenient alternatives to pointers in many situations.

## Learning Objectives
- Understand reference fundamentals and syntax
- Master lvalue and rvalue references
- Differentiate between references and pointers
- Use references for function parameters and return values
- Understand reference binding rules
- Apply const references for optimization
- Work with reference wrappers

## Features
- Basic reference operations
- Lvalue references demonstrations
- Rvalue references (C++11)
- Pass-by-reference vs pass-by-value
- Const references for read-only access
- Reference return values
- References with arrays and structures
- Reference wrappers (std::reference_wrapper)
- Common reference patterns

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/109_references
g++ -std=c++20 -Wall -Wextra -o references main.cpp
```

### Execution
```bash
./references
```

## Key Concepts

### 1. Reference Basics
```cpp
// Reference declaration (must be initialized)
int x = 10;
int& ref = x;  // ref is alias for x

// Using reference
std::cout << ref;  // 10
ref = 20;          // Modifies x
std::cout << x;    // 20

// References cannot be null or reassigned
int y = 30;
ref = y;  // This assigns y's value to x, doesn't rebind ref!
```

### 2. Lvalue References
```cpp
// Named variables are lvalues
int a = 10;
int& lref = a;  // OK

// Cannot bind to temporary (rvalue)
// int& ref = 5;  // Error!

// But const reference can bind to rvalue
const int& cref = 5;  // OK - lifetime extended

// Reference to const
const int b = 20;
const int& ref2 = b;
// ref2 = 30;  // Error - cannot modify const
```

### 3. Rvalue References (C++11)
```cpp
// Rvalue reference with &&
int&& rref = 10;  // Binds to temporary
rref = 20;        // Can modify

// Function returning rvalue
int getValue() { return 42; }
int&& rref2 = getValue();

// Move semantics
std::string str = "Hello";
std::string&& rref3 = std::move(str);

// Can bind to:
int&& r1 = 5;           // Literals
int&& r2 = 2 + 3;       // Expressions
int&& r3 = getValue();  // Function returns
```

### 4. Pass by Reference
```cpp
// Pass by value (copies)
void modifyValue(int x) {
    x = 100;  // Only modifies local copy
}

// Pass by reference (no copy)
void modifyReference(int& x) {
    x = 100;  // Modifies original
}

// Pass by const reference (efficient, read-only)
void displayValue(const int& x) {
    std::cout << x;
    // x = 10;  // Error!
}

// Usage
int num = 10;
modifyValue(num);       // num still 10
modifyReference(num);   // num now 100

// Large objects - avoid copying
void processString(const std::string& str) {
    // No copy, can't modify
    std::cout << str.length();
}
```

### 5. Reference Return Values
```cpp
// Return reference to existing object
int& getElement(int arr[], int index) {
    return arr[index];
}

int numbers[] = {1, 2, 3, 4, 5};
getElement(numbers, 2) = 100;  // Modifies arr[2]

// Return const reference (read-only)
const std::string& getFirst(const std::vector<std::string>& vec) {
    return vec.front();
}

// WARNING: Never return reference to local variable!
int& badFunction() {
    int local = 10;
    return local;  // DANGER! local destroyed after return
}
```

### 6. References vs Pointers
```cpp
// Reference:
int x = 10;
int& ref = x;
ref = 20;         // Modify x

// Pointer:
int* ptr = &x;
*ptr = 30;        // Modify x

// Key differences:
// 1. References must be initialized
int& r;           // Error!
int* p;           // OK (uninitialized)

// 2. References cannot be null
int& ref2 = nullptr;  // Error!
int* ptr2 = nullptr;  // OK

// 3. References cannot be reassigned
int a = 1, b = 2;
int& r = a;
r = b;            // Assigns value, doesn't rebind
int* p = &a;
p = &b;           // Rebinds pointer

// 4. No reference arithmetic
// ref++;         // Changes value, not address
ptr++;            // Moves to next location
```

### 7. Const References
```cpp
// Bind to const objects
const int x = 10;
const int& ref = x;

// Bind to temporaries (lifetime extended)
const int& ref2 = 42;
const std::string& str = "Hello";

// Efficient parameter passing
void print(const std::vector<int>& vec) {
    for (int val : vec) {
        std::cout << val << " ";
    }
}

// Return const reference from class
class MyClass {
    std::string data;
public:
    const std::string& getData() const {
        return data;  // No copy
    }
};
```

### 8. Reference Wrappers
```cpp
#include <functional>

int a = 10, b = 20, c = 30;

// Cannot store references in containers
// std::vector<int&> refs;  // Error!

// Use std::reference_wrapper
std::vector<std::reference_wrapper<int>> refs;
refs.push_back(std::ref(a));
refs.push_back(std::ref(b));
refs.push_back(std::ref(c));

// Access and modify
refs[0].get() = 100;  // Modifies a
std::cout << a;        // 100

// Useful for storing references
std::reference_wrapper<int> refWrap = std::ref(a);
refWrap.get() = 50;
```

### 9. Universal References (Forwarding References)
```cpp
// Template with && (universal reference)
template<typename T>
void process(T&& arg) {
    // Can bind to both lvalues and rvalues
}

int x = 10;
process(x);       // T deduced as int&
process(20);      // T deduced as int

// Perfect forwarding
template<typename T>
void wrapper(T&& arg) {
    process(std::forward<T>(arg));
}
```

## Best Practices
1. **Prefer references over pointers** when possible
2. **Use const references** for large read-only parameters
3. **Never return references to local variables**
4. **Initialize references immediately** upon declaration
5. **Use pass-by-reference** to avoid unnecessary copies
6. **Use const references** for function parameters when not modifying
7. **Prefer references in range-based for loops** for large objects
8. **Use rvalue references** for move semantics
9. **Document whether function modifies reference parameters**
10. **Use auto& or const auto&** in range-based for loops appropriately

## Common Use Cases
```cpp
// 1. Avoiding copies
for (const auto& item : largeVector) { }

// 2. Modifying function arguments
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

// 3. Method chaining
class Builder {
    Builder& setName(const std::string& name) {
        // ...
        return *this;
    }
    Builder& setAge(int age) {
        // ...
        return *this;
    }
};
// Usage: builder.setName("John").setAge(25);

// 4. Operator overloading
std::ostream& operator<<(std::ostream& os, const MyClass& obj) {
    os << obj.toString();
    return os;
}
```

## Resources and References
- [cppreference.com - References](https://en.cppreference.com/w/cpp/language/reference)
- [cppreference.com - Rvalue references](https://en.cppreference.com/w/cpp/language/reference#Rvalue_references)
- [C++ Core Guidelines - References](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f15-prefer-simple-and-conventional-ways-of-passing-information)

## Navigation
- **Previous Program**: [108 - Pointers](../108_pointers/README.md)
- **Next Program**: [110 - Strings](../110_strings/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
