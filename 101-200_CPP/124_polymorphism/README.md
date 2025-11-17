# Program 124: Polymorphism in C++

## Description
Comprehensive exploration of polymorphism in C++ covering compile-time polymorphism (function overloading, templates) and runtime polymorphism (virtual functions, abstract classes), demonstrating dynamic binding and polymorphic behavior.

## Learning Objectives
- Understand compile-time vs runtime polymorphism
- Master virtual functions and dynamic dispatch
- Use abstract classes and interfaces
- Apply polymorphic design patterns
- Work with virtual destructors

## Features
- Function overloading (compile-time)
- Operator overloading (compile-time)
- Template polymorphism (compile-time)
- Virtual functions (runtime)
- Abstract classes and pure virtual functions
- Virtual destructors
- Dynamic binding

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/124_polymorphism
g++ -std=c++20 -Wall -Wextra -o polymorphism main.cpp
```

## Key Concepts

### 1. Compile-Time Polymorphism
```cpp
// Function overloading
void print(int x) { std::cout << x; }
void print(double x) { std::cout << x; }
void print(const std::string& x) { std::cout << x; }
```

### 2. Runtime Polymorphism
```cpp
class Shape {
public:
    virtual double area() const = 0;  // Pure virtual
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double radius;
public:
    double area() const override { return 3.14 * radius * radius; }
};

Shape* shape = new Circle();
std::cout << shape->area();  // Dynamic dispatch
delete shape;
```

### 3. Virtual Functions
```cpp
class Base {
public:
    virtual void func() { std::cout << "Base
"; }
    virtual ~Base() {}
};

class Derived : public Base {
public:
    void func() override { std::cout << "Derived
"; }
};
```

## Best Practices
1. **Make base class destructors virtual**
2. **Use override keyword for clarity**
3. **Prefer compile-time polymorphism when possible**
4. **Design interfaces with pure virtual functions**
5. **Avoid slicing with polymorphic objects**

## Resources and References
- [cppreference.com - Virtual functions](https://en.cppreference.com/w/cpp/language/virtual)

## Navigation
- **Previous Program**: [123 - Inheritance](../123_inheritance/README.md)
- **Next Program**: [125 - Encapsulation](../125_encapsulation/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
