# Program 121: Classes and Objects in C++

## Description
Comprehensive exploration of classes and objects in C++ covering class declaration, member variables and functions, access specifiers, object creation, this pointer, and class fundamentals. This program introduces the foundation of object-oriented programming in C++.

## Learning Objectives
- Understand class declaration and definition
- Master member variables and functions
- Use access specifiers (public, private, protected)
- Create and manipulate objects
- Work with the this pointer
- Apply encapsulation principles
- Understand class vs struct differences

## Features
- Class declaration and definition
- Member variables (data members)
- Member functions (methods)
- Access specifiers
- Object creation (stack and heap)
- The this pointer
- Const member functions
- Static vs non-static members
- Inline member functions

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/121_classes_objects
g++ -std=c++20 -Wall -Wextra -o classes_objects main.cpp
```

### Execution
```bash
./classes_objects
```

## Key Concepts

### 1. Class Declaration and Definition
```cpp
// Class declaration
class Rectangle {
public:
    // Public members accessible from outside
    double width;
    double height;

    double area() {
        return width * height;
    }

    void display() {
        std::cout << "Rectangle: " << width << "x" << height << '\n';
    }
};

// Creating objects
Rectangle rect1;  // Stack allocation
rect1.width = 5.0;
rect1.height = 3.0;
std::cout << "Area: " << rect1.area() << '\n';

// Heap allocation
Rectangle* rect2 = new Rectangle();
rect2->width = 10.0;
rect2->height = 6.0;
delete rect2;
```

### 2. Access Specifiers
```cpp
class BankAccount {
private:
    // Private: only accessible within class
    double balance;
    std::string accountNumber;

protected:
    // Protected: accessible in class and derived classes
    int transactionCount;

public:
    // Public: accessible from anywhere
    std::string ownerName;

    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            transactionCount++;
        }
    }

    double getBalance() const {
        return balance;
    }
};

// Usage
BankAccount account;
account.ownerName = "John Doe";  // OK - public
account.deposit(1000.0);         // OK - public
// account.balance = 5000;       // Error - private
double bal = account.getBalance();  // OK - public method accesses private
```

### 3. Member Functions
```cpp
class Circle {
private:
    double radius;

public:
    // Member function implementation inside class (inline)
    void setRadius(double r) {
        radius = r;
    }

    // Declaration only
    double area() const;
    double circumference() const;
};

// Member function implementation outside class
double Circle::area() const {
    return 3.14159 * radius * radius;
}

double Circle::circumference() const {
    return 2 * 3.14159 * radius;
}

// Usage
Circle circle;
circle.setRadius(5.0);
std::cout << "Area: " << circle.area() << '\n';
```

### 4. The this Pointer
```cpp
class Person {
private:
    std::string name;
    int age;

public:
    // Constructor using this pointer
    Person(const std::string& name, int age) {
        this->name = name;  // Disambiguate parameter from member
        this->age = age;
    }

    // Method chaining with this
    Person& setName(const std::string& name) {
        this->name = name;
        return *this;
    }

    Person& setAge(int age) {
        this->age = age;
        return *this;
    }

    void display() const {
        std::cout << "Name: " << name << ", Age: " << age << '\n';
    }
};

// Method chaining
Person person("", 0);
person.setName("Alice").setAge(25).display();
```

### 5. Const Member Functions
```cpp
class Point {
private:
    int x, y;

public:
    Point(int x, int y) : x(x), y(y) {}

    // Const member function - promises not to modify object
    int getX() const { return x; }
    int getY() const { return y; }

    double distanceFromOrigin() const {
        return std::sqrt(x * x + y * y);
    }

    // Non-const member function
    void setX(int newX) { x = newX; }
    void setY(int newY) { y = newY; }
};

// Const object can only call const member functions
const Point p(3, 4);
std::cout << p.getX() << '\n';  // OK
// p.setX(5);                   // Error! Cannot call non-const
```

### 6. Class vs Struct
```cpp
// Class: members private by default
class MyClass {
    int value;  // Private by default
public:
    void setValue(int v) { value = v; }
};

// Struct: members public by default
struct MyStruct {
    int value;  // Public by default
    void setValue(int v) { value = v; }
};

// Convention:
// - Use struct for simple data aggregation (POD types)
// - Use class for objects with behavior and encapsulation
```

### 7. Encapsulation Example
```cpp
class Temperature {
private:
    double celsius;

    // Private helper function
    bool isValidTemperature(double temp) const {
        return temp >= -273.15;  // Absolute zero
    }

public:
    // Constructor with validation
    Temperature(double temp) {
        if (isValidTemperature(temp)) {
            celsius = temp;
        } else {
            celsius = 0.0;
        }
    }

    // Getters
    double getCelsius() const { return celsius; }
    double getFahrenheit() const { return celsius * 9.0 / 5.0 + 32.0; }
    double getKelvin() const { return celsius + 273.15; }

    // Setter with validation
    void setCelsius(double temp) {
        if (isValidTemperature(temp)) {
            celsius = temp;
        }
    }
};
```

### 8. Object Lifecycle
```cpp
class Resource {
public:
    Resource() {
        std::cout << "Resource created\n";
    }

    ~Resource() {
        std::cout << "Resource destroyed\n";
    }
};

void demonstrateLifecycle() {
    std::cout << "Entering function\n";
    Resource r1;  // Created on stack

    {
        std::cout << "Entering inner block\n";
        Resource r2;  // Created in inner scope
        std::cout << "Leaving inner block\n";
    }  // r2 destroyed here

    Resource* r3 = new Resource();  // Created on heap
    delete r3;  // Must explicitly delete

    std::cout << "Leaving function\n";
}  // r1 destroyed here
```

## Best Practices
1. **Use classes for encapsulation** and data hiding
2. **Make data members private** and provide public accessors
3. **Mark read-only functions const**
4. **Use meaningful class and member names**
5. **Initialize all members** in constructors
6. **Follow single responsibility principle**
7. **Prefer initialization lists** over assignment
8. **Document class interface** clearly
9. **Use structs for simple data** without behavior
10. **Apply Rule of Three/Five** when managing resources

## Common Patterns
```cpp
// 1. PIMPL (Pointer to Implementation)
class Widget {
    class Impl;
    std::unique_ptr<Impl> pImpl;
public:
    Widget();
    ~Widget();
    void doSomething();
};

// 2. Builder Pattern
class PersonBuilder {
    std::string name;
    int age = 0;
public:
    PersonBuilder& setName(const std::string& n) {
        name = n;
        return *this;
    }
    PersonBuilder& setAge(int a) {
        age = a;
        return *this;
    }
    Person build() { return Person(name, age); }
};
```

## Resources and References
- [cppreference.com - Classes](https://en.cppreference.com/w/cpp/language/class)
- [C++ Core Guidelines - Classes](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-class)

## Navigation
- **Previous Program**: [120 - Standard I/O](../120_standard_io/README.md)
- **Next Program**: [122 - Constructors and Destructors](../122_constructors_destructors/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
