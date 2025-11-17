# Program 123: Inheritance in C++

## Description
Comprehensive exploration of inheritance in C++ covering single, multilevel, and hierarchical inheritance, access specifiers, protected members, base class initialization, function overriding, and inheritance patterns.

## Learning Objectives
- Understand inheritance fundamentals and syntax
- Master base and derived class relationships
- Use access specifiers in inheritance contexts
- Override base class functions
- Initialize base classes in constructors
- Apply inheritance design patterns

## Features
- Single inheritance
- Multilevel inheritance
- Hierarchical inheritance
- Protected members
- Base class initialization
- Function overriding
- Access control in inheritance
- Is-a relationships

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/123_inheritance
g++ -std=c++20 -Wall -Wextra -o inheritance main.cpp
```

## Key Concepts

### 1. Basic Inheritance
```cpp
class Animal {
protected:
    std::string name;
public:
    Animal(const std::string& n) : name(n) {}
    void eat() { std::cout << name << " is eating\n"; }
};

class Dog : public Animal {
public:
    Dog(const std::string& n) : Animal(n) {}
    void bark() { std::cout << name << " barks\n"; }
};
```

### 2. Access Specifiers
```cpp
// Public inheritance (is-a relationship)
class Derived : public Base {
    // public members stay public
    // protected members stay protected
    // private members inaccessible
};

// Protected inheritance
class Derived : protected Base {
    // public members become protected
    // protected members stay protected
};

// Private inheritance (implementation detail)
class Derived : private Base {
    // public members become private
    // protected members become private
};
```

### 3. Function Overriding
```cpp
class Shape {
public:
    void draw() { std::cout << "Drawing shape\n"; }
};

class Circle : public Shape {
public:
    void draw() { std::cout << "Drawing circle\n"; }  // Override
};

Circle c;
c.draw();  // Calls Circle::draw()
```

### 4. Base Class Initialization
```cpp
class Base {
    int value;
public:
    Base(int v) : value(v) {}
};

class Derived : public Base {
    int extra;
public:
    Derived(int v, int e) : Base(v), extra(e) {}  // Initialize base first
};
```

## Best Practices
1. **Use public inheritance for is-a relationships**
2. **Call base constructors explicitly**
3. **Use protected for inherited access**
4. **Make destructors virtual in base classes**
5. **Document inheritance hierarchies**
6. **Prefer composition over inheritance** when appropriate

## Resources and References
- [cppreference.com - Derived classes](https://en.cppreference.com/w/cpp/language/derived_class)

## Navigation
- **Previous Program**: [122 - Constructors and Destructors](../122_constructors_destructors/README.md)
- **Next Program**: [124 - Polymorphism](../124_polymorphism/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
