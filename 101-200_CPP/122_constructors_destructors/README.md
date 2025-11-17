# Program 122: Constructors and Destructors in C++

## Description
Comprehensive exploration of constructors and destructors in C++ covering default constructors, parameterized constructors, copy constructors, move constructors, destructors, constructor initialization lists, and delegating constructors. Essential for proper object lifecycle management.

## Learning Objectives
- Master constructor types and syntax
- Understand constructor initialization lists
- Implement copy and move constructors
- Use destructors for resource cleanup
- Apply delegating constructors (C++11)
- Work with default and deleted constructors
- Follow constructor best practices

## Features
- Default constructors
- Parameterized constructors
- Copy constructors
- Move constructors (C++11)
- Destructors and RAII
- Initialization lists
- Delegating constructors
- Default/deleted constructors
- Constructor overloading

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/122_constructors_destructors
g++ -std=c++20 -Wall -Wextra -o constructors_destructors main.cpp
```

## Key Concepts

### 1. Default Constructor
```cpp
class MyClass {
public:
    MyClass() {  // Default constructor
        std::cout << "Default constructor called\n";
    }
};

// Compiler-generated default constructor
class Auto {
    int value = 0;  // In-class initialization
    // Implicit default constructor provided by compiler
};
```

### 2. Parameterized Constructor
```cpp
class Point {
    int x, y;
public:
    Point(int x_val, int y_val) : x(x_val), y(y_val) {
        std::cout << "Parameterized constructor\n";
    }
};

Point p(10, 20);  // Calls parameterized constructor
```

### 3. Copy Constructor
```cpp
class Array {
    int* data;
    size_t size;
public:
    // Copy constructor
    Array(const Array& other) : size(other.size) {
        data = new int[size];
        std::copy(other.data, other.data + size, data);
        std::cout << "Copy constructor\n";
    }

    ~Array() { delete[] data; }
};
```

### 4. Move Constructor (C++11)
```cpp
class String {
    char* data;
public:
    // Move constructor
    String(String&& other) noexcept : data(other.data) {
        other.data = nullptr;  // Transfer ownership
        std::cout << "Move constructor\n";
    }
};
```

### 5. Initialization Lists
```cpp
class Person {
    const std::string name;  // Must use init list for const
    int& age;                // Must use init list for references
public:
    Person(const std::string& n, int& a) : name(n), age(a) {
        // More efficient than assignment
    }
};
```

### 6. Delegating Constructors
```cpp
class Rectangle {
    double width, height;
public:
    Rectangle() : Rectangle(1.0, 1.0) {}  // Delegate to another constructor
    Rectangle(double w) : Rectangle(w, w) {}
    Rectangle(double w, double h) : width(w), height(h) {}
};
```

### 7. Destructor
```cpp
class Resource {
    int* data;
public:
    Resource() : data(new int[100]) {
        std::cout << "Resource acquired\n";
    }

    ~Resource() {  // Destructor
        delete[] data;
        std::cout << "Resource released\n";
    }
};
```

### 8. Explicit Constructors
```cpp
class Integer {
    int value;
public:
    explicit Integer(int v) : value(v) {}  // Prevents implicit conversion
};

Integer i1(10);      // OK
// Integer i2 = 10;  // Error! Explicit prevents this
```

## Best Practices
1. **Use initialization lists** for member initialization
2. **Mark single-argument constructors explicit**
3. **Make move constructors noexcept**
4. **Initialize all members** in constructors
5. **Use RAII** for resource management
6. **Follow Rule of Three/Five**
7. **Delegate constructors** to reduce code duplication
8. **Provide default constructor** when appropriate
9. **Document constructor requirements**
10. **Use = default and = delete** appropriately

## Resources and References
- [cppreference.com - Constructors](https://en.cppreference.com/w/cpp/language/constructor)
- [cppreference.com - Destructors](https://en.cppreference.com/w/cpp/language/destructor)

## Navigation
- **Previous Program**: [121 - Classes and Objects](../121_classes_objects/README.md)
- **Next Program**: [123 - Inheritance](../123_inheritance/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
