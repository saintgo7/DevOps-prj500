/*
 * Program 124: Polymorphism in C++
 *
 * This program demonstrates:
 * - Compile-time polymorphism (Function overloading, Operator overloading)
 * - Runtime polymorphism (Virtual functions)
 * - Virtual functions and vtables
 * - Pure virtual functions
 * - Abstract classes
 * - Override and final keywords
 * - Dynamic binding
 * - Polymorphic behavior
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <cmath>

using namespace std;

// ===== COMPILE-TIME POLYMORPHISM (FUNCTION OVERLOADING) =====

class Calculator {
public:
    // Function overloading - same name, different parameters
    int add(int a, int b) {
        cout << "Adding two integers" << endl;
        return a + b;
    }

    double add(double a, double b) {
        cout << "Adding two doubles" << endl;
        return a + b;
    }

    int add(int a, int b, int c) {
        cout << "Adding three integers" << endl;
        return a + b + c;
    }

    string add(string a, string b) {
        cout << "Concatenating strings" << endl;
        return a + b;
    }
};

// ===== RUNTIME POLYMORPHISM (VIRTUAL FUNCTIONS) =====

// Base class with virtual functions
class Shape {
protected:
    string color;
    string name;

public:
    Shape(string n, string c) : name(n), color(c) {}

    virtual ~Shape() {
        cout << "Shape destructor: " << name << endl;
    }

    // Virtual function - can be overridden
    virtual void draw() const {
        cout << "Drawing a " << color << " " << name << endl;
    }

    // Pure virtual function - must be overridden
    virtual double area() const = 0;

    // Virtual function with default implementation
    virtual double perimeter() const {
        return 0.0;
    }

    // Non-virtual function
    void displayInfo() const {
        cout << "Shape: " << name << ", Color: " << color << endl;
    }

    string getName() const { return name; }
};

// Derived class - Circle
class Circle : public Shape {
private:
    double radius;

public:
    Circle(string c, double r) : Shape("Circle", c), radius(r) {}

    ~Circle() {
        cout << "Circle destructor" << endl;
    }

    // Override virtual function
    void draw() const override {
        cout << "Drawing a " << color << " circle with radius " << radius << endl;
    }

    // Implement pure virtual function
    double area() const override {
        return 3.14159 * radius * radius;
    }

    double perimeter() const override {
        return 2 * 3.14159 * radius;
    }
};

// Derived class - Rectangle
class Rectangle : public Shape {
private:
    double width;
    double height;

public:
    Rectangle(string c, double w, double h)
        : Shape("Rectangle", c), width(w), height(h) {}

    ~Rectangle() {
        cout << "Rectangle destructor" << endl;
    }

    void draw() const override {
        cout << "Drawing a " << color << " rectangle "
             << width << " x " << height << endl;
    }

    double area() const override {
        return width * height;
    }

    double perimeter() const override {
        return 2 * (width + height);
    }
};

// Derived class - Triangle
class Triangle : public Shape {
private:
    double side1, side2, side3;

public:
    Triangle(string c, double s1, double s2, double s3)
        : Shape("Triangle", c), side1(s1), side2(s2), side3(s3) {}

    ~Triangle() {
        cout << "Triangle destructor" << endl;
    }

    void draw() const override {
        cout << "Drawing a " << color << " triangle" << endl;
    }

    double area() const override {
        // Heron's formula
        double s = (side1 + side2 + side3) / 2;
        return sqrt(s * (s - side1) * (s - side2) * (s - side3));
    }

    double perimeter() const override {
        return side1 + side2 + side3;
    }
};

// ===== ABSTRACT BASE CLASS =====

class Employee {
protected:
    string name;
    int id;
    double baseSalary;

public:
    Employee(string n, int i, double sal) : name(n), id(i), baseSalary(sal) {}

    virtual ~Employee() {}

    // Pure virtual function - makes this an abstract class
    virtual double calculateSalary() const = 0;

    // Pure virtual function
    virtual void displayDetails() const = 0;

    // Virtual function with implementation
    virtual string getType() const {
        return "Generic Employee";
    }

    string getName() const { return name; }
};

class PermanentEmployee : public Employee {
private:
    double bonus;
    double benefits;

public:
    PermanentEmployee(string n, int i, double sal, double b, double ben)
        : Employee(n, i, sal), bonus(b), benefits(ben) {}

    double calculateSalary() const override {
        return baseSalary + bonus + benefits;
    }

    void displayDetails() const override {
        cout << "Permanent Employee: " << name << " (ID: " << id << ")" << endl;
        cout << "Total Salary: $" << calculateSalary() << endl;
    }

    string getType() const override {
        return "Permanent Employee";
    }
};

class ContractEmployee : public Employee {
private:
    int hoursWorked;
    double hourlyRate;

public:
    ContractEmployee(string n, int i, int hours, double rate)
        : Employee(n, i, 0), hoursWorked(hours), hourlyRate(rate) {}

    double calculateSalary() const override {
        return hoursWorked * hourlyRate;
    }

    void displayDetails() const override {
        cout << "Contract Employee: " << name << " (ID: " << id << ")" << endl;
        cout << "Hours: " << hoursWorked << ", Rate: $" << hourlyRate << "/hr" << endl;
        cout << "Total Payment: $" << calculateSalary() << endl;
    }

    string getType() const override {
        return "Contract Employee";
    }
};

// ===== OVERRIDE AND FINAL KEYWORDS =====

class Base {
public:
    virtual void func1() {
        cout << "Base::func1()" << endl;
    }

    virtual void func2() final {  // Cannot be overridden
        cout << "Base::func2() - final" << endl;
    }

    virtual void func3() {
        cout << "Base::func3()" << endl;
    }
};

class Derived : public Base {
public:
    void func1() override {  // override keyword ensures it's actually overriding
        cout << "Derived::func1()" << endl;
    }

    // void func2() override { }  // Error: can't override final function

    void func3() override final {  // This override is final
        cout << "Derived::func3() - final override" << endl;
    }
};

// class FurtherDerived : public Derived {
//     void func3() override { }  // Error: can't override final function
// };

// ===== VIRTUAL DESTRUCTOR DEMONSTRATION =====

class ResourceBase {
public:
    ResourceBase() {
        cout << "ResourceBase constructor" << endl;
    }

    virtual ~ResourceBase() {  // Virtual destructor is crucial!
        cout << "ResourceBase destructor" << endl;
    }
};

class ResourceDerived : public ResourceBase {
private:
    int* data;

public:
    ResourceDerived() {
        cout << "ResourceDerived constructor" << endl;
        data = new int[100];
    }

    ~ResourceDerived() {
        cout << "ResourceDerived destructor - freeing memory" << endl;
        delete[] data;
    }
};

// ===== POLYMORPHIC CONTAINER =====

void demonstratePolymorphicContainer() {
    cout << "\nPolymorphic Container Example:" << endl;
    cout << "-------------------------------" << endl;

    vector<unique_ptr<Shape>> shapes;

    shapes.push_back(make_unique<Circle>("red", 5.0));
    shapes.push_back(make_unique<Rectangle>("blue", 4.0, 6.0));
    shapes.push_back(make_unique<Triangle>("green", 3.0, 4.0, 5.0));
    shapes.push_back(make_unique<Circle>("yellow", 3.0));

    double totalArea = 0;
    double totalPerimeter = 0;

    for (const auto& shape : shapes) {
        shape->draw();  // Polymorphic call
        double a = shape->area();
        double p = shape->perimeter();
        cout << "Area: " << a << ", Perimeter: " << p << endl;
        totalArea += a;
        totalPerimeter += p;
        cout << endl;
    }

    cout << "Total area of all shapes: " << totalArea << endl;
    cout << "Total perimeter of all shapes: " << totalPerimeter << endl;
}

// ===== INTERFACE SIMULATION =====

// Interface (pure abstract class)
class Printable {
public:
    virtual ~Printable() {}
    virtual void print() const = 0;
};

class Saveable {
public:
    virtual ~Saveable() {}
    virtual void save() const = 0;
};

// Class implementing multiple interfaces
class Document : public Printable, public Saveable {
private:
    string content;
    string filename;

public:
    Document(string c, string f) : content(c), filename(f) {}

    void print() const override {
        cout << "Printing document: " << filename << endl;
        cout << "Content: " << content << endl;
    }

    void save() const override {
        cout << "Saving document to: " << filename << endl;
    }
};

int main() {
    cout << "=== Program 124: Polymorphism in C++ ===" << endl;
    cout << "========================================\n" << endl;

    // 1. Compile-time polymorphism (Function Overloading)
    cout << "1. Compile-Time Polymorphism - Function Overloading" << endl;
    cout << "-----------------------------------------------------" << endl;
    Calculator calc;
    cout << "Result: " << calc.add(5, 3) << endl;
    cout << "Result: " << calc.add(5.5, 3.2) << endl;
    cout << "Result: " << calc.add(1, 2, 3) << endl;
    cout << "Result: " << calc.add(string("Hello "), string("World")) << endl;

    // 2. Runtime polymorphism with virtual functions
    cout << "\n2. Runtime Polymorphism - Virtual Functions" << endl;
    cout << "--------------------------------------------" << endl;
    {
        Circle circle("red", 5.0);
        Rectangle rect("blue", 4.0, 6.0);

        Shape* shape1 = &circle;
        Shape* shape2 = &rect;

        // Polymorphic calls
        shape1->draw();
        cout << "Area: " << shape1->area() << endl;

        shape2->draw();
        cout << "Area: " << shape2->area() << endl;
    }

    // 3. Polymorphic array/container
    cout << "\n3. Polymorphic Array" << endl;
    cout << "---------------------" << endl;
    {
        Shape* shapes[4];
        shapes[0] = new Circle("red", 3.0);
        shapes[1] = new Rectangle("green", 5.0, 4.0);
        shapes[2] = new Triangle("blue", 3.0, 4.0, 5.0);
        shapes[3] = new Circle("yellow", 7.0);

        for (int i = 0; i < 4; i++) {
            cout << "\nShape " << i + 1 << ":" << endl;
            shapes[i]->draw();
            cout << "Area: " << shapes[i]->area() << endl;
            cout << "Perimeter: " << shapes[i]->perimeter() << endl;
        }

        // Clean up
        for (int i = 0; i < 4; i++) {
            delete shapes[i];
        }
    }

    // 4. Abstract class and pure virtual functions
    cout << "\n4. Abstract Classes - Employee Hierarchy" << endl;
    cout << "-----------------------------------------" << endl;
    {
        // Employee emp("Test", 1, 5000);  // Error: can't instantiate abstract class

        PermanentEmployee perm("Alice Johnson", 101, 50000, 5000, 3000);
        ContractEmployee contract("Bob Smith", 102, 160, 75);

        Employee* employees[2];
        employees[0] = &perm;
        employees[1] = &contract;

        for (int i = 0; i < 2; i++) {
            cout << "\nEmployee " << i + 1 << ":" << endl;
            employees[i]->displayDetails();
            cout << "Type: " << employees[i]->getType() << endl;
        }
    }

    // 5. Override and final keywords
    cout << "\n5. Override and Final Keywords" << endl;
    cout << "-------------------------------" << endl;
    {
        Base* basePtr;
        Derived derived;

        basePtr = &derived;
        basePtr->func1();  // Calls Derived::func1()
        basePtr->func2();  // Calls Base::func2() (final)
        basePtr->func3();  // Calls Derived::func3()
    }

    // 6. Virtual destructor importance
    cout << "\n6. Virtual Destructor Importance" << endl;
    cout << "---------------------------------" << endl;
    {
        cout << "With virtual destructor:" << endl;
        ResourceBase* ptr = new ResourceDerived();
        delete ptr;  // Properly calls both destructors
    }

    // 7. Polymorphic container with smart pointers
    demonstratePolymorphicContainer();

    // 8. Interface implementation
    cout << "\n8. Interface Implementation" << endl;
    cout << "----------------------------" << endl;
    {
        Document doc("This is a test document", "test.txt");

        Printable* printable = &doc;
        Saveable* saveable = &doc;

        printable->print();
        saveable->save();
    }

    // 9. Runtime type identification
    cout << "\n9. Runtime Behavior" << endl;
    cout << "--------------------" << endl;
    {
        vector<Shape*> shapeVec;
        shapeVec.push_back(new Circle("red", 5.0));
        shapeVec.push_back(new Rectangle("blue", 3.0, 4.0));

        for (auto shape : shapeVec) {
            cout << shape->getName() << ": ";
            shape->draw();
        }

        for (auto shape : shapeVec) {
            delete shape;
        }
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Compile-time polymorphism - function/operator overloading" << endl;
    cout << "2. Runtime polymorphism - virtual functions" << endl;
    cout << "3. Virtual function tables (vtables) - automatic behind scenes" << endl;
    cout << "4. Pure virtual functions - abstract classes" << endl;
    cout << "5. Override keyword - explicit override declaration" << endl;
    cout << "6. Final keyword - prevent further overriding" << endl;
    cout << "7. Virtual destructors - proper cleanup in polymorphic hierarchies" << endl;
    cout << "8. Polymorphic containers - storing different derived types" << endl;
    cout << "9. Dynamic binding - runtime method resolution" << endl;
    cout << "10. Interface simulation - pure abstract classes" << endl;

    return 0;
}
