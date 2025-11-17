# Program 111: Structures in C++

## Description
Comprehensive exploration of structures in C++ covering structure basics, member functions, initialization, nested structures, structure arrays, structure pointers, and the relationship between structures and classes. This program demonstrates how structures provide a way to group related data.

## Learning Objectives
- Understand structure declaration and definition
- Work with structure members and access
- Use structure initialization techniques
- Implement member functions in structures
- Apply nested structures and structure arrays
- Use pointers to structures
- Understand structures vs classes

## Features
- Basic structure declaration and usage
- Member access operators (. and ->)
- Structure initialization methods
- Member functions in structures
- Nested structures
- Arrays of structures
- Pointers to structures
- Structure padding and alignment
- Structure comparison
- Structures as function parameters

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/111_structures
g++ -std=c++20 -Wall -Wextra -o structures main.cpp
```

### Execution
```bash
./structures
```

## Key Concepts

### 1. Structure Basics
```cpp
// Structure declaration
struct Person {
    std::string name;
    int age;
    double height;
};

// Creating instances
Person p1;                        // Default construction
Person p2 = {"Alice", 25, 5.6};   // Aggregate initialization
Person p3{"Bob", 30, 6.0};        // Uniform initialization (C++11)

// Accessing members
p1.name = "Charlie";
p1.age = 35;
p1.height = 5.9;

std::cout << p2.name << " is " << p2.age << " years old\n";
```

### 2. Structure Initialization
```cpp
// Designated initializers (C++20)
Person p = {
    .name = "Diana",
    .age = 28,
    .height = 5.7
};

// Partial initialization
Person p2 = {"Eve"};  // age and height are zero-initialized

// Copy initialization
Person p3 = p1;       // Memberwise copy

// Default member initializers (C++11)
struct Point {
    int x = 0;
    int y = 0;
};
Point pt;  // x and y are 0
```

### 3. Member Functions in Structures
```cpp
struct Rectangle {
    double width;
    double height;

    // Member functions
    double area() const {
        return width * height;
    }

    double perimeter() const {
        return 2 * (width + height);
    }

    void scale(double factor) {
        width *= factor;
        height *= factor;
    }

    void print() const {
        std::cout << "Width: " << width
                  << ", Height: " << height << '\n';
    }
};

// Usage
Rectangle rect{5.0, 3.0};
std::cout << "Area: " << rect.area() << '\n';
rect.scale(2.0);
rect.print();
```

### 4. Nested Structures
```cpp
struct Address {
    std::string street;
    std::string city;
    std::string state;
    int zipCode;
};

struct Employee {
    std::string name;
    int id;
    Address homeAddress;  // Nested structure
    Address workAddress;
};

// Usage
Employee emp = {
    "John Doe",
    1001,
    {"123 Main St", "Springfield", "IL", 62701},
    {"456 Oak Ave", "Springfield", "IL", 62702}
};

std::cout << emp.homeAddress.city << '\n';
```

### 5. Arrays of Structures
```cpp
// Array of structures
Person people[3] = {
    {"Alice", 25, 5.6},
    {"Bob", 30, 6.0},
    {"Charlie", 35, 5.9}
};

// Accessing array elements
for (int i = 0; i < 3; i++) {
    std::cout << people[i].name << " - " << people[i].age << '\n';
}

// With std::array (C++11)
std::array<Person, 3> peopleArr = {{
    {"Diana", 28, 5.7},
    {"Eve", 32, 5.8},
    {"Frank", 40, 6.1}
}};

// With std::vector
std::vector<Person> peopleVec = {
    {"Grace", 27, 5.5},
    {"Henry", 33, 6.2}
};
peopleVec.push_back({"Iris", 29, 5.6});
```

### 6. Pointers to Structures
```cpp
Person person = {"John", 30, 5.10};

// Pointer to structure
Person* ptr = &person;

// Access members using pointer
std::cout << (*ptr).name << '\n';  // Dereference first
std::cout << ptr->name << '\n';    // Arrow operator (preferred)

ptr->age = 31;
ptr->height = 5.11;

// Dynamic allocation
Person* dynamicPerson = new Person{"Alice", 25, 5.6};
std::cout << dynamicPerson->name << '\n';
delete dynamicPerson;

// Smart pointers (modern C++)
auto smartPerson = std::make_unique<Person>("Bob", 28, 6.0);
std::cout << smartPerson->name << '\n';
```

### 7. Structures as Function Parameters
```cpp
// Pass by value (copy)
void displayPerson(Person p) {
    std::cout << p.name << " - " << p.age << '\n';
}

// Pass by reference (no copy)
void modifyPerson(Person& p) {
    p.age += 1;
}

// Pass by const reference (efficient, read-only)
void printPerson(const Person& p) {
    std::cout << p.name << " is " << p.age << " years old\n";
    // p.age = 30;  // Error!
}

// Return structure
Person createPerson(std::string name, int age, double height) {
    return {name, age, height};  // Return by value (efficient with RVO)
}

// Return by reference (only for existing objects)
Person& getOldest(std::vector<Person>& people) {
    return *std::max_element(people.begin(), people.end(),
        [](const Person& a, const Person& b) {
            return a.age < b.age;
        });
}
```

### 8. Structure Comparison
```cpp
struct Point {
    int x, y;

    // Equality operator
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }

    // Inequality operator
    bool operator!=(const Point& other) const {
        return !(*this == other);
    }

    // Less than (for sorting)
    bool operator<(const Point& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
};

// C++20 spaceship operator
struct Point3D {
    int x, y, z;

    auto operator<=>(const Point3D&) const = default;
};

// Usage
Point p1{1, 2}, p2{1, 2}, p3{3, 4};
bool same = (p1 == p2);      // true
bool different = (p1 != p3); // true
```

### 9. Structure Padding and Alignment
```cpp
#include <iostream>

struct Unoptimized {
    char c;      // 1 byte
    int i;       // 4 bytes (likely padded to 4-byte boundary)
    char c2;     // 1 byte
    double d;    // 8 bytes (likely padded to 8-byte boundary)
};

struct Optimized {
    double d;    // 8 bytes
    int i;       // 4 bytes
    char c;      // 1 byte
    char c2;     // 1 byte
    // Total: 16 bytes (with padding)
};

// Check sizes
std::cout << "Unoptimized: " << sizeof(Unoptimized) << " bytes\n";
std::cout << "Optimized: " << sizeof(Optimized) << " bytes\n";

// Packed structures (compiler-specific)
#pragma pack(push, 1)
struct Packed {
    char c;
    int i;
    char c2;
    double d;
};
#pragma pack(pop)
```

### 10. Structures vs Classes
```cpp
// Structure: members public by default
struct StructExample {
    int value;  // Public by default

    void display() {  // Public by default
        std::cout << value << '\n';
    }
};

// Class: members private by default
class ClassExample {
    int value;  // Private by default

public:  // Must specify public
    void display() {
        std::cout << value << '\n';
    }
};

// Structures commonly used for:
// - Plain Old Data (POD) types
// - Data aggregation
// - Public interfaces

// Classes commonly used for:
// - Encapsulation
// - Complex behavior
// - Private data with controlled access
```

## Best Practices
1. **Use structures for simple data aggregation** without complex behavior
2. **Use classes for data requiring encapsulation**
3. **Initialize all members** to avoid undefined behavior
4. **Order members by size** (largest first) to minimize padding
5. **Use const references** when passing large structures
6. **Provide comparison operators** when structures need ordering
7. **Consider alignment** for performance-critical code
8. **Use designated initializers (C++20)** for clarity
9. **Prefer aggregate initialization** over assignment
10. **Document structure layout** if padding matters

## Common Patterns
```cpp
// 1. Structure for configuration
struct Config {
    std::string filename = "default.txt";
    int maxConnections = 100;
    bool enableLogging = true;
    double timeout = 30.0;
};

// 2. Structure for return multiple values
struct DivisionResult {
    int quotient;
    int remainder;
};

DivisionResult divide(int a, int b) {
    return {a / b, a % b};
}

// 3. Structure for coordinates
struct Point3D {
    double x = 0.0;
    double y = 0.0;
    double z = 0.0;

    double distanceFromOrigin() const {
        return std::sqrt(x*x + y*y + z*z);
    }
};

// 4. Structure with factory method
struct Color {
    uint8_t r, g, b, a;

    static Color rgb(uint8_t r, uint8_t g, uint8_t b) {
        return {r, g, b, 255};
    }

    static Color rgba(uint8_t r, uint8_t g, uint8_t b, uint8_t a) {
        return {r, g, b, a};
    }
};
```

## Resources and References
- [cppreference.com - Structures](https://en.cppreference.com/w/cpp/language/class)
- [cppreference.com - Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization)
- [C++ Core Guidelines - Structs](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c2-use-class-if-the-class-has-an-invariant-use-struct-if-the-data-members-can-vary-independently)

## Navigation
- **Previous Program**: [110 - Strings](../110_strings/README.md)
- **Next Program**: [112 - Enums](../112_enums/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
