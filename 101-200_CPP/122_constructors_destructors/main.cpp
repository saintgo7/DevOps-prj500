/*
 * Program 122: Constructors and Destructors in C++
 *
 * This program demonstrates:
 * - Default constructor
 * - Parameterized constructor
 * - Constructor overloading
 * - Copy constructor
 * - Destructor
 * - Constructor initialization list
 * - Delegating constructors
 * - Object lifecycle
 */

#include <iostream>
#include <string>
#include <cstring>

using namespace std;

// Class demonstrating various constructors
class Book {
private:
    string title;
    string author;
    int pages;
    double price;

public:
    // 1. Default constructor
    Book() {
        cout << "Default constructor called" << endl;
        title = "Unknown";
        author = "Unknown";
        pages = 0;
        price = 0.0;
    }

    // 2. Parameterized constructor
    Book(string t, string a, int p, double pr) {
        cout << "Parameterized constructor called" << endl;
        title = t;
        author = a;
        pages = p;
        price = pr;
    }

    // 3. Constructor with default parameters
    Book(string t, string a = "Anonymous", int p = 100) {
        cout << "Constructor with default parameters called" << endl;
        title = t;
        author = a;
        pages = p;
        price = 9.99;
    }

    // 4. Copy constructor
    Book(const Book& other) {
        cout << "Copy constructor called" << endl;
        title = other.title;
        author = other.author;
        pages = other.pages;
        price = other.price;
    }

    // Destructor
    ~Book() {
        cout << "Destructor called for: " << title << endl;
    }

    void display() const {
        cout << "Title: " << title << ", Author: " << author
             << ", Pages: " << pages << ", Price: $" << price << endl;
    }
};

// Class with initialization list
class Circle {
private:
    const double PI;  // const member must be initialized in initialization list
    double radius;
    static int objectCount;

public:
    // Constructor with initialization list
    Circle(double r) : PI(3.14159), radius(r) {
        cout << "Circle constructor called (radius = " << radius << ")" << endl;
        objectCount++;
    }

    // Copy constructor
    Circle(const Circle& other) : PI(other.PI), radius(other.radius) {
        cout << "Circle copy constructor called" << endl;
        objectCount++;
    }

    ~Circle() {
        cout << "Circle destructor called (radius = " << radius << ")" << endl;
        objectCount--;
    }

    double getArea() const {
        return PI * radius * radius;
    }

    double getCircumference() const {
        return 2 * PI * radius;
    }

    static int getObjectCount() {
        return objectCount;
    }

    void display() const {
        cout << "Circle - Radius: " << radius
             << ", Area: " << getArea()
             << ", Circumference: " << getCircumference() << endl;
    }
};

int Circle::objectCount = 0;

// Class demonstrating delegating constructors (C++11)
class Rectangle {
private:
    double width;
    double height;
    string color;

public:
    // Main constructor
    Rectangle(double w, double h, string c) : width(w), height(h), color(c) {
        cout << "Rectangle main constructor called" << endl;
    }

    // Delegating constructor - calls main constructor
    Rectangle(double side) : Rectangle(side, side, "white") {
        cout << "Rectangle square constructor (delegating)" << endl;
    }

    // Delegating constructor - calls main constructor
    Rectangle() : Rectangle(1.0, 1.0, "white") {
        cout << "Rectangle default constructor (delegating)" << endl;
    }

    ~Rectangle() {
        cout << "Rectangle destructor called" << endl;
    }

    void display() const {
        cout << "Rectangle: " << width << " x " << height
             << ", Color: " << color << endl;
    }
};

// Class with dynamic memory - demonstrates importance of destructors
class DynamicArray {
private:
    int* data;
    int size;

public:
    // Constructor
    DynamicArray(int s) : size(s) {
        cout << "DynamicArray constructor: allocating " << size << " integers" << endl;
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = i * 10;
        }
    }

    // Copy constructor - deep copy
    DynamicArray(const DynamicArray& other) : size(other.size) {
        cout << "DynamicArray copy constructor: deep copy" << endl;
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];
        }
    }

    // Destructor - frees allocated memory
    ~DynamicArray() {
        cout << "DynamicArray destructor: freeing memory" << endl;
        delete[] data;
    }

    void display() const {
        cout << "Array contents: ";
        for (int i = 0; i < size; i++) {
            cout << data[i] << " ";
        }
        cout << endl;
    }

    int getSize() const {
        return size;
    }
};

// Class demonstrating constructor chaining
class Person {
protected:
    string name;
    int age;

public:
    Person() : name("Unknown"), age(0) {
        cout << "Person default constructor" << endl;
    }

    Person(string n, int a) : name(n), age(a) {
        cout << "Person parameterized constructor" << endl;
    }

    virtual ~Person() {
        cout << "Person destructor for: " << name << endl;
    }

    virtual void display() const {
        cout << "Person: " << name << ", Age: " << age << endl;
    }
};

class Employee : public Person {
private:
    int employeeId;
    double salary;

public:
    // Constructor calling base class constructor
    Employee(string n, int a, int id, double sal)
        : Person(n, a), employeeId(id), salary(sal) {
        cout << "Employee constructor" << endl;
    }

    ~Employee() {
        cout << "Employee destructor for ID: " << employeeId << endl;
    }

    void display() const override {
        cout << "Employee: " << name << ", Age: " << age
             << ", ID: " << employeeId << ", Salary: $" << salary << endl;
    }
};

// Class with explicit constructor
class Wrapper {
private:
    int value;

public:
    // Explicit constructor prevents implicit conversions
    explicit Wrapper(int v) : value(v) {
        cout << "Wrapper constructor: " << value << endl;
    }

    ~Wrapper() {
        cout << "Wrapper destructor: " << value << endl;
    }

    int getValue() const {
        return value;
    }
};

// Helper function to demonstrate object lifecycle
void demonstrateLifecycle() {
    cout << "\n--- Inside demonstrateLifecycle function ---" << endl;
    Circle c(5.0);
    c.display();
    cout << "--- Leaving demonstrateLifecycle function ---" << endl;
    // Destructor will be called automatically when function exits
}

int main() {
    cout << "=== Program 122: Constructors and Destructors ===" << endl;
    cout << "=================================================\n" << endl;

    // 1. Default constructor
    cout << "1. Default Constructor" << endl;
    cout << "----------------------" << endl;
    {
        Book book1;
        book1.display();
    }  // Destructor called here when book1 goes out of scope

    // 2. Parameterized constructor
    cout << "\n2. Parameterized Constructor" << endl;
    cout << "-----------------------------" << endl;
    {
        Book book2("C++ Programming", "Bjarne Stroustrup", 1376, 59.99);
        book2.display();
    }

    // 3. Constructor overloading
    cout << "\n3. Constructor Overloading" << endl;
    cout << "---------------------------" << endl;
    {
        Book book3("Design Patterns");  // Uses default parameters
        book3.display();
    }

    // 4. Copy constructor
    cout << "\n4. Copy Constructor" << endl;
    cout << "--------------------" << endl;
    {
        Book original("The C++ Standard Library", "Nicolai Josuttis", 1136, 64.99);
        cout << "Original: ";
        original.display();

        Book copy = original;  // Copy constructor called
        cout << "Copy: ";
        copy.display();
    }

    // 5. Initialization list and const members
    cout << "\n5. Initialization List" << endl;
    cout << "-----------------------" << endl;
    {
        Circle c1(5.0);
        c1.display();
        cout << "Total Circle objects: " << Circle::getObjectCount() << endl;

        Circle c2 = c1;  // Copy constructor
        c2.display();
        cout << "Total Circle objects: " << Circle::getObjectCount() << endl;
    }
    cout << "After scope exit, Circle objects: " << Circle::getObjectCount() << endl;

    // 6. Delegating constructors
    cout << "\n6. Delegating Constructors" << endl;
    cout << "---------------------------" << endl;
    {
        Rectangle rect1;  // Default
        rect1.display();

        Rectangle rect2(5.0);  // Square
        rect2.display();

        Rectangle rect3(4.0, 6.0, "blue");  // Full specification
        rect3.display();
    }

    // 7. Dynamic memory and destructors
    cout << "\n7. Dynamic Memory Management" << endl;
    cout << "-----------------------------" << endl;
    {
        DynamicArray arr1(5);
        arr1.display();

        DynamicArray arr2 = arr1;  // Copy constructor - deep copy
        arr2.display();

        cout << "Both arrays exist independently" << endl;
    }  // Both destructors called, memory properly freed

    // 8. Object lifecycle
    cout << "\n8. Object Lifecycle" << endl;
    cout << "--------------------" << endl;
    cout << "Circle objects before function: " << Circle::getObjectCount() << endl;
    demonstrateLifecycle();
    cout << "Circle objects after function: " << Circle::getObjectCount() << endl;

    // 9. Inheritance and constructors
    cout << "\n9. Inheritance - Constructor and Destructor Order" << endl;
    cout << "--------------------------------------------------" << endl;
    {
        cout << "Creating Employee object:" << endl;
        Employee emp("Alice Johnson", 30, 12345, 75000.0);
        emp.display();
        cout << "\nEmployee object going out of scope:" << endl;
    }  // Destructor order: derived class first, then base class

    // 10. Explicit constructor
    cout << "\n10. Explicit Constructor" << endl;
    cout << "-------------------------" << endl;
    {
        Wrapper w1(42);  // OK: direct initialization
        // Wrapper w2 = 100;  // Error: implicit conversion not allowed
        Wrapper w3 = Wrapper(100);  // OK: explicit conversion
        cout << "w1 value: " << w1.getValue() << endl;
        cout << "w3 value: " << w3.getValue() << endl;
    }

    // 11. Array of objects
    cout << "\n11. Array of Objects" << endl;
    cout << "---------------------" << endl;
    {
        cout << "Creating array of 3 circles:" << endl;
        Circle circles[3] = {Circle(1.0), Circle(2.0), Circle(3.0)};

        for (int i = 0; i < 3; i++) {
            circles[i].display();
        }

        cout << "Total Circle objects: " << Circle::getObjectCount() << endl;
        cout << "Array going out of scope:" << endl;
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Default constructor - initializes objects with default values" << endl;
    cout << "2. Parameterized constructor - initializes with specific values" << endl;
    cout << "3. Copy constructor - creates deep copies of objects" << endl;
    cout << "4. Destructor - cleans up resources when object is destroyed" << endl;
    cout << "5. Initialization list - efficient member initialization" << endl;
    cout << "6. Delegating constructors - code reuse between constructors" << endl;
    cout << "7. Object lifecycle - automatic constructor/destructor calls" << endl;
    cout << "8. Constructor/destructor order in inheritance" << endl;
    cout << "9. Explicit keyword - prevents implicit conversions" << endl;
    cout << "10. Dynamic memory management in constructors/destructors" << endl;

    return 0;
}
