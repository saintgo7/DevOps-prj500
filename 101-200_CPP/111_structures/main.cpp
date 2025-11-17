/*
 * Program 111: Structures in C++
 *
 * Topics Covered:
 * - Structure definition and declaration
 * - Member access
 * - Nested structures
 * - Structure initialization
 * - Structures and functions
 * - Structure arrays
 * - Structures with member functions
 * - Structures vs classes
 * - Designated initializers (C++20)
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o structures main.cpp
 */

#include <iostream>
#include <string>
#include <vector>
#include <cstring>

// Basic structure definition
struct Point {
    int x;
    int y;
};

// Structure with different types
struct Person {
    std::string name;
    int age;
    double height;
};

// Nested structure
struct Address {
    std::string street;
    std::string city;
    int zipCode;
};

struct Employee {
    std::string name;
    int id;
    Address address;  // Nested structure
};

// Structure with member functions
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

    void display() const {
        std::cout << "Rectangle: " << width << "x" << height << std::endl;
    }
};

void demonstrateBasicStructures();
void demonstrateNestedStructures();
void demonstrateStructuresWithFunctions();
void demonstrateStructureArrays();
void demonstrateDesignatedInitializers();

int main() {
    std::cout << "=== C++ Structures ===" << std::endl << std::endl;

    demonstrateBasicStructures();
    demonstrateNestedStructures();
    demonstrateStructuresWithFunctions();
    demonstrateStructureArrays();
    demonstrateDesignatedInitializers();

    return 0;
}

void demonstrateBasicStructures() {
    std::cout << "--- Basic Structures ---" << std::endl;

    // Structure initialization
    Point p1;
    p1.x = 10;
    p1.y = 20;

    std::cout << "Point p1: (" << p1.x << ", " << p1.y << ")" << std::endl;

    // Aggregate initialization
    Point p2 = {30, 40};
    std::cout << "Point p2: (" << p2.x << ", " << p2.y << ")" << std::endl;

    // Uniform initialization (C++11)
    Point p3{50, 60};
    std::cout << "Point p3: (" << p3.x << ", " << p3.y << ")" << std::endl;

    // Copy initialization
    Point p4 = p2;
    std::cout << "Point p4 (copy of p2): (" << p4.x << ", " << p4.y << ")" << std::endl;

    // Structure with mixed types
    Person person1 = {"Alice", 30, 5.6};
    std::cout << "\nPerson: " << person1.name << ", Age: " << person1.age
              << ", Height: " << person1.height << std::endl;

    // Modifying members
    person1.age = 31;
    std::cout << "After birthday: Age = " << person1.age << std::endl;

    std::cout << std::endl;
}

void demonstrateNestedStructures() {
    std::cout << "--- Nested Structures ---" << std::endl;

    // Creating nested structure
    Employee emp1 = {
        "John Doe",
        12345,
        {"123 Main St", "New York", 10001}
    };

    std::cout << "Employee: " << emp1.name << std::endl;
    std::cout << "ID: " << emp1.id << std::endl;
    std::cout << "Address: " << emp1.address.street << ", "
              << emp1.address.city << " " << emp1.address.zipCode << std::endl;

    // Accessing nested members
    emp1.address.city = "Los Angeles";
    emp1.address.zipCode = 90001;

    std::cout << "\nAfter relocation:" << std::endl;
    std::cout << "City: " << emp1.address.city << std::endl;
    std::cout << "Zip: " << emp1.address.zipCode << std::endl;

    std::cout << std::endl;
}

// Function taking structure by value
void printPoint(Point p) {
    std::cout << "Point: (" << p.x << ", " << p.y << ")" << std::endl;
}

// Function taking structure by reference
void movePoint(Point& p, int dx, int dy) {
    p.x += dx;
    p.y += dy;
}

// Function returning structure
Point createPoint(int x, int y) {
    return {x, y};
}

void demonstrateStructuresWithFunctions() {
    std::cout << "--- Structures with Functions ---" << std::endl;

    Point p{10, 20};

    // Pass by value
    printPoint(p);

    // Pass by reference
    std::cout << "Moving point by (5, -3)" << std::endl;
    movePoint(p, 5, -3);
    printPoint(p);

    // Return structure
    Point p2 = createPoint(100, 200);
    printPoint(p2);

    // Structure with member functions
    Rectangle rect{5.0, 3.0};
    rect.display();
    std::cout << "Area: " << rect.area() << std::endl;
    std::cout << "Perimeter: " << rect.perimeter() << std::endl;

    std::cout << std::endl;
}

void demonstrateStructureArrays() {
    std::cout << "--- Structure Arrays ---" << std::endl;

    // Array of structures
    Point points[3] = {
        {1, 2},
        {3, 4},
        {5, 6}
    };

    std::cout << "Array of points:" << std::endl;
    for (int i = 0; i < 3; i++) {
        std::cout << "  Point " << i << ": (" << points[i].x << ", " << points[i].y << ")" << std::endl;
    }

    // Vector of structures
    std::vector<Person> people = {
        {"Alice", 25, 5.5},
        {"Bob", 30, 6.0},
        {"Charlie", 35, 5.8}
    };

    std::cout << "\nVector of people:" << std::endl;
    for (const auto& person : people) {
        std::cout << "  " << person.name << ", " << person.age << " years" << std::endl;
    }

    std::cout << std::endl;
}

void demonstrateDesignatedInitializers() {
    std::cout << "--- Designated Initializers (C++20) ---" << std::endl;

    // Designated initializers allow initializing by name
    Point p1 = {.x = 10, .y = 20};
    std::cout << "p1: (" << p1.x << ", " << p1.y << ")" << std::endl;

    // Can skip members (they get default-initialized)
    Point p2 = {.y = 30};
    std::cout << "p2: (" << p2.x << ", " << p2.y << ")" << std::endl;

    // More readable for complex structures
    Employee emp = {
        .name = "Jane Smith",
        .id = 54321,
        .address = {
            .street = "456 Oak Ave",
            .city = "Chicago",
            .zipCode = 60601
        }
    };

    std::cout << "\nEmployee: " << emp.name << ", ID: " << emp.id << std::endl;

    std::cout << std::endl;
}

/*
 * Structures vs Classes:
 * - In C++, the only difference is default access:
 *   - struct: members are public by default
 *   - class: members are private by default
 * - Use struct for plain data (POD types)
 * - Use class for objects with behavior and encapsulation
 *
 * Best Practices:
 * 1. Use structures for simple data aggregates
 * 2. Use classes when you need encapsulation
 * 3. Initialize all struct members to avoid undefined behavior
 * 4. Pass large structures by const reference
 * 5. Use designated initializers (C++20) for clarity
 * 6. Consider using std::tuple or std::pair for simple pairs
 * 7. Structures can have constructors and member functions
 * 8. Use structures with member functions sparingly
 */
