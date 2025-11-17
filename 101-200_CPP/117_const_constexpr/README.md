# Program 117: const and constexpr in C++

## Description
Comprehensive exploration of const and constexpr in C++ covering const correctness, constexpr functions and variables, compile-time computation, const member functions, and best practices. This program demonstrates how to write more robust and efficient code using const and constexpr.

## Learning Objectives
- Understand const correctness principles
- Master constexpr for compile-time computation
- Use const with pointers and references
- Implement const member functions
- Apply constexpr functions and variables
- Understand constexpr vs const differences
- Work with consteval and constinit (C++20)

## Features
- Const variables and objects
- Const pointers and references
- Const member functions
- Constexpr variables and functions
- Constexpr if (C++17)
- Consteval immediate functions (C++20)
- Constinit for static initialization (C++20)
- Compile-time computation examples

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/117_const_constexpr
g++ -std=c++20 -Wall -Wextra -o const_constexpr main.cpp
```

### Execution
```bash
./const_constexpr
```

## Key Concepts

### 1. Const Variables
```cpp
// Const variables must be initialized
const int MAX_SIZE = 100;
// MAX_SIZE = 200;  // Error! Cannot modify

// Const with different types
const double PI = 3.14159;
const std::string NAME = "John";

// Const arrays
const int arr[] = {1, 2, 3, 4, 5};
// arr[0] = 10;  // Error!

// Runtime const (value known at runtime)
int input;
std::cin >> input;
const int value = input;  // OK, but value set at runtime
```

### 2. Const Pointers and References
```cpp
int x = 10, y = 20;

// Pointer to const (cannot modify value)
const int* ptr1 = &x;
// *ptr1 = 20;  // Error!
ptr1 = &y;      // OK, can change pointer

// Const pointer (cannot change address)
int* const ptr2 = &x;
*ptr2 = 30;     // OK, can modify value
// ptr2 = &y;   // Error! Cannot change pointer

// Const pointer to const
const int* const ptr3 = &x;
// *ptr3 = 40;  // Error!
// ptr3 = &y;   // Error!

// Const references
const int& ref = x;
// ref = 100;  // Error! Cannot modify through const reference
```

### 3. Const Member Functions
```cpp
class Rectangle {
    double width, height;

public:
    Rectangle(double w, double h) : width(w), height(h) {}

    // Const member function - promises not to modify object
    double getArea() const {
        return width * height;
    }

    double getPerimeter() const {
        return 2 * (width + height);
    }

    // Non-const member function
    void setWidth(double w) {
        width = w;
    }

    // Cannot call non-const from const
    void badConstFunction() const {
        // setWidth(10);  // Error! Cannot call non-const from const
    }
};

// Const objects can only call const member functions
const Rectangle rect(5.0, 3.0);
double area = rect.getArea();        // OK
// rect.setWidth(10);                // Error! Cannot call non-const
```

### 4. Constexpr Variables
```cpp
// Compile-time constant
constexpr int SIZE = 100;
int array[SIZE];  // OK, SIZE is compile-time constant

// Can use in templates
template<int N>
class Array {
    int data[N];
};
Array<SIZE> arr;  // OK

// Constexpr with complex types (C++11 limitations relaxed in C++14+)
constexpr double PI = 3.14159;
constexpr double TWICE_PI = 2 * PI;

// Constexpr implies const
constexpr int value = 42;
// Same as: const int value = 42; but evaluated at compile-time
```

### 5. Constexpr Functions
```cpp
// Simple constexpr function (C++11)
constexpr int square(int x) {
    return x * x;
}

// Use at compile-time
constexpr int result = square(5);  // Computed at compile-time
int arr[square(3)];                // Array size computed at compile-time

// Use at runtime
int n;
std::cin >> n;
int runtime = square(n);           // Can also be used at runtime

// More complex constexpr (C++14 and later)
constexpr int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

constexpr int fact5 = factorial(5);  // 120, computed at compile-time

// Constexpr with loops (C++14)
constexpr int sum(int n) {
    int result = 0;
    for (int i = 1; i <= n; ++i) {
        result += i;
    }
    return result;
}
```

### 6. Constexpr Classes and Constructors
```cpp
class Point {
    int x, y;

public:
    // Constexpr constructor
    constexpr Point(int x_val, int y_val) : x(x_val), y(y_val) {}

    // Constexpr member functions
    constexpr int getX() const { return x; }
    constexpr int getY() const { return y; }

    constexpr int distanceSquared() const {
        return x * x + y * y;
    }
};

// Create constexpr object
constexpr Point origin(0, 0);
constexpr Point p(3, 4);

// Use in constexpr context
constexpr int dist = p.distanceSquared();  // 25, at compile-time

// Array initialization with constexpr
constexpr Point points[] = {
    Point(0, 0),
    Point(1, 1),
    Point(2, 2)
};
```

### 7. Constexpr if (C++17)
```cpp
template<typename T>
auto getValue(T t) {
    if constexpr (std::is_integral_v<T>) {
        return t + 1;  // For integers
    } else if constexpr (std::is_floating_point_v<T>) {
        return t + 0.1;  // For floating-point
    } else {
        return t;  // For others
    }
}

// Only one branch is compiled
int i = getValue(5);      // Returns 6
double d = getValue(5.0);  // Returns 5.1

// Template specialization alternative
template<bool Condition>
void doSomething() {
    if constexpr (Condition) {
        std::cout << "Condition is true\n";
    } else {
        std::cout << "Condition is false\n";
    }
}
```

### 8. Consteval (C++20)
```cpp
// Immediate function - MUST be evaluated at compile-time
consteval int sqr(int n) {
    return n * n;
}

constexpr int a = sqr(5);  // OK, compile-time
int arr[sqr(3)];           // OK, compile-time

int x = 5;
// int b = sqr(x);         // Error! x is not constant

// Difference from constexpr
constexpr int add(int a, int b) {
    return a + b;
}

consteval int add_immediate(int a, int b) {
    return a + b;
}

constexpr int r1 = add(1, 2);      // Compile-time
int r2 = add(1, 2);                // Runtime OK
constexpr int r3 = add_immediate(1, 2);  // Compile-time
// int r4 = add_immediate(x, 2);   // Error! Must be compile-time
```

### 9. Constinit (C++20)
```cpp
// Ensures static/thread_local initialization at compile-time
constinit int global1 = 42;
constinit static int global2 = 100;

// Error checking
int runtimeValue() { return 42; }
// constinit int global3 = runtimeValue();  // Error! Not constant

// Useful for static initialization order
constinit static int initialized = []() {
    return 42;
}();

// Unlike constexpr, can be modified later
constinit int value = 10;
void modify() {
    value = 20;  // OK
}

// constexpr cannot be modified
constexpr int constValue = 10;
// void modify2() { constValue = 20; }  // Error!
```

### 10. Const vs Constexpr
```cpp
// const: Value cannot be modified, may be runtime
const int runtime = []() { return 42; }();

// constexpr: Compile-time constant, implies const
constexpr int compiletime = 42;

// Usage differences
int arr1[compiletime];  // OK
// int arr2[runtime];   // Error! Not compile-time constant

// const doesn't guarantee compile-time
int input;
std::cin >> input;
const int c = input;      // OK, runtime const
// constexpr int ce = input;  // Error! Must be compile-time

// All constexpr are const, but not all const are constexpr
constexpr int a = 10;  // const and compile-time
const int b = a;       // const, may or may not be compile-time
```

## Best Practices
1. **Use const for immutability** whenever possible
2. **Make member functions const** if they don't modify state
3. **Use constexpr for compile-time constants**
4. **Prefer constexpr over const** for compile-time values
5. **Use consteval** when function must run at compile-time
6. **Mark constructors constexpr** when possible
7. **Use const references** for read-only parameters
8. **Apply const correctness** throughout your code
9. **Use constexpr if** to eliminate dead code branches
10. **Document why something isn't const**

## Common Patterns
```cpp
// 1. Const correctness in classes
class MyClass {
    int value;
public:
    int getValue() const { return value; }     // Getter is const
    void setValue(int v) { value = v; }        // Setter is non-const
};

// 2. Constexpr lookup tables
constexpr int factorial_table[] = {
    factorial(0), factorial(1), factorial(2),
    factorial(3), factorial(4), factorial(5)
};

// 3. Compile-time string hashing
constexpr uint32_t hash(const char* str) {
    uint32_t hash = 5381;
    while (*str) {
        hash = ((hash << 5) + hash) + (*str++);
    }
    return hash;
}

constexpr uint32_t cmd = hash("command");
```

## Resources and References
- [cppreference.com - const](https://en.cppreference.com/w/cpp/language/cv)
- [cppreference.com - constexpr](https://en.cppreference.com/w/cpp/language/constexpr)
- [C++ Core Guidelines - const](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-immutable)

## Navigation
- **Previous Program**: [116 - Memory Management](../116_memory_management/README.md)
- **Next Program**: [118 - Type Casting](../118_type_casting/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
