/*
 * Program 127: Virtual Functions in C++
 *
 * This program demonstrates:
 * - Virtual functions
 * - Virtual function tables (vtables)
 * - Override keyword
 * - Final keyword
 * - Virtual destructors
 * - Pure virtual functions
 * - Early vs late binding
 * - Virtual function behavior in inheritance
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>

using namespace std;

// ===== BASIC VIRTUAL FUNCTIONS =====

class Animal {
protected:
    string name;

public:
    Animal(string n) : name(n) {
        cout << "Animal constructor: " << name << endl;
    }

    // Virtual destructor - CRUCIAL for polymorphic classes
    virtual ~Animal() {
        cout << "Animal destructor: " << name << endl;
    }

    // Virtual function - can be overridden
    virtual void makeSound() const {
        cout << name << " makes a generic animal sound" << endl;
    }

    // Virtual function
    virtual void eat() const {
        cout << name << " is eating" << endl;
    }

    // Non-virtual function - static binding
    void sleep() const {
        cout << name << " is sleeping" << endl;
    }

    // Virtual function with default parameter
    virtual void greet(string greeting = "Hello") const {
        cout << name << " says: " << greeting << endl;
    }
};

class Dog : public Animal {
public:
    Dog(string n) : Animal(n) {
        cout << "Dog constructor" << endl;
    }

    ~Dog() {
        cout << "Dog destructor" << endl;
    }

    // Override virtual function
    void makeSound() const override {
        cout << name << " barks: Woof! Woof!" << endl;
    }

    void eat() const override {
        cout << name << " is eating dog food" << endl;
    }

    // sleep() is not virtual, so this is a new function
    void sleep() const {
        cout << name << " is sleeping in the dog house" << endl;
    }

    // Dog-specific method
    void fetch() const {
        cout << name << " is fetching the ball" << endl;
    }
};

class Cat : public Animal {
public:
    Cat(string n) : Animal(n) {
        cout << "Cat constructor" << endl;
    }

    ~Cat() {
        cout << "Cat destructor" << endl;
    }

    void makeSound() const override {
        cout << name << " meows: Meow!" << endl;
    }

    void eat() const override {
        cout << name << " is eating cat food" << endl;
    }
};

// ===== OVERRIDE KEYWORD =====

class Base {
public:
    virtual void func1() {
        cout << "Base::func1()" << endl;
    }

    virtual void func2() const {
        cout << "Base::func2() const" << endl;
    }

    void func3() {  // Non-virtual
        cout << "Base::func3()" << endl;
    }
};

class Derived : public Base {
public:
    void func1() override {  // Correct override
        cout << "Derived::func1()" << endl;
    }

    void func2() const override {  // Correct override
        cout << "Derived::func2() const" << endl;
    }

    // void func2() override { }  // Error: signature doesn't match (missing const)

    void func3() {  // Not an override, just hiding
        cout << "Derived::func3()" << endl;
    }

    // void func4() override { }  // Error: no matching virtual function in base
};

// ===== FINAL KEYWORD =====

class BaseClass {
public:
    virtual void method1() {
        cout << "BaseClass::method1()" << endl;
    }

    virtual void method2() final {  // Cannot be overridden
        cout << "BaseClass::method2() - FINAL" << endl;
    }

    virtual void method3() {
        cout << "BaseClass::method3()" << endl;
    }
};

class DerivedClass : public BaseClass {
public:
    void method1() override {
        cout << "DerivedClass::method1()" << endl;
    }

    // void method2() override { }  // Error: can't override final method

    void method3() override final {  // This override is final
        cout << "DerivedClass::method3() - FINAL" << endl;
    }
};

// Can't override method3 anymore
// class FurtherDerived : public DerivedClass {
//     void method3() override { }  // Error!
// };

// ===== PURE VIRTUAL FUNCTIONS =====

class Shape {
protected:
    string color;

public:
    Shape(string c) : color(c) {}
    virtual ~Shape() {}

    // Pure virtual function
    virtual double area() const = 0;

    // Virtual function with implementation
    virtual void display() const {
        cout << "Color: " << color << endl;
    }
};

class Circle : public Shape {
private:
    double radius;

public:
    Circle(string c, double r) : Shape(c), radius(r) {}

    double area() const override {
        return 3.14159 * radius * radius;
    }

    void display() const override {
        cout << "Circle - ";
        Shape::display();  // Call base class version
        cout << "Radius: " << radius << ", Area: " << area() << endl;
    }
};

// ===== VIRTUAL DESTRUCTOR IMPORTANCE =====

class ResourceManager {
public:
    ResourceManager() {
        cout << "ResourceManager constructor" << endl;
    }

    // Virtual destructor is ESSENTIAL
    virtual ~ResourceManager() {
        cout << "ResourceManager destructor" << endl;
    }

    virtual void manage() {
        cout << "Managing resources" << endl;
    }
};

class FileManager : public ResourceManager {
private:
    int* fileHandles;

public:
    FileManager() {
        cout << "FileManager constructor - allocating memory" << endl;
        fileHandles = new int[100];
    }

    ~FileManager() {
        cout << "FileManager destructor - freeing memory" << endl;
        delete[] fileHandles;
    }

    void manage() override {
        cout << "Managing file resources" << endl;
    }
};

// ===== VIRTUAL FUNCTIONS IN CONSTRUCTOR/DESTRUCTOR =====

class ConstructorVirtual {
public:
    ConstructorVirtual() {
        cout << "ConstructorVirtual constructor" << endl;
        init();  // Virtual call in constructor
    }

    virtual ~ConstructorVirtual() {
        cout << "ConstructorVirtual destructor" << endl;
        cleanup();  // Virtual call in destructor
    }

    virtual void init() {
        cout << "ConstructorVirtual::init()" << endl;
    }

    virtual void cleanup() {
        cout << "ConstructorVirtual::cleanup()" << endl;
    }
};

class DerivedConstructorVirtual : public ConstructorVirtual {
public:
    DerivedConstructorVirtual() {
        cout << "DerivedConstructorVirtual constructor" << endl;
    }

    ~DerivedConstructorVirtual() {
        cout << "DerivedConstructorVirtual destructor" << endl;
    }

    void init() override {
        cout << "DerivedConstructorVirtual::init()" << endl;
    }

    void cleanup() override {
        cout << "DerivedConstructorVirtual::cleanup()" << endl;
    }
};

// ===== COVARIANT RETURN TYPES =====

class Employee {
protected:
    string name;

public:
    Employee(string n) : name(n) {}
    virtual ~Employee() {}

    virtual Employee* clone() const {
        cout << "Cloning Employee" << endl;
        return new Employee(name);
    }

    virtual void display() const {
        cout << "Employee: " << name << endl;
    }
};

class Manager : public Employee {
private:
    int teamSize;

public:
    Manager(string n, int size) : Employee(n), teamSize(size) {}

    // Covariant return type - returns Manager* instead of Employee*
    Manager* clone() const override {
        cout << "Cloning Manager" << endl;
        return new Manager(name, teamSize);
    }

    void display() const override {
        cout << "Manager: " << name << ", Team Size: " << teamSize << endl;
    }
};

// ===== VIRTUAL FUNCTION SLICING PROBLEM =====

class Vehicle {
public:
    string brand;

    Vehicle(string b = "Generic") : brand(b) {}
    virtual ~Vehicle() {}

    virtual void info() const {
        cout << "Vehicle brand: " << brand << endl;
    }
};

class Car : public Vehicle {
public:
    int doors;

    Car(string b = "Generic", int d = 4) : Vehicle(b), doors(d) {}

    void info() const override {
        cout << "Car brand: " << brand << ", Doors: " << doors << endl;
    }
};

// ===== MULTIPLE LEVELS OF VIRTUAL FUNCTIONS =====

class A {
public:
    virtual void func() {
        cout << "A::func()" << endl;
    }

    virtual ~A() {}
};

class B : public A {
public:
    void func() override {
        cout << "B::func()" << endl;
    }
};

class C : public B {
public:
    void func() override {
        cout << "C::func()" << endl;
    }
};

// Helper function to demonstrate polymorphism
void demonstratePolymorphism() {
    cout << "\nPolymorphism Demonstration:" << endl;
    cout << "----------------------------" << endl;

    vector<unique_ptr<Animal>> animals;
    animals.push_back(make_unique<Dog>("Buddy"));
    animals.push_back(make_unique<Cat>("Whiskers"));
    animals.push_back(make_unique<Dog>("Max"));

    for (const auto& animal : animals) {
        animal->makeSound();  // Polymorphic call
        animal->eat();        // Polymorphic call
        animal->sleep();      // Non-polymorphic (not virtual)
    }
}

int main() {
    cout << "=== Program 127: Virtual Functions ===" << endl;
    cout << "======================================\n" << endl;

    // 1. Basic virtual functions
    cout << "1. Basic Virtual Functions" << endl;
    cout << "---------------------------" << endl;
    {
        Dog dog("Buddy");
        Cat cat("Whiskers");

        Animal* animalPtr;

        animalPtr = &dog;
        animalPtr->makeSound();  // Dynamic binding - calls Dog::makeSound()
        animalPtr->eat();        // Dynamic binding - calls Dog::eat()
        animalPtr->sleep();      // Static binding - calls Animal::sleep()

        animalPtr = &cat;
        animalPtr->makeSound();  // Dynamic binding - calls Cat::makeSound()
        animalPtr->eat();        // Dynamic binding - calls Cat::eat()
    }

    // 2. Virtual vs non-virtual
    cout << "\n2. Virtual vs Non-Virtual Functions" << endl;
    cout << "------------------------------------" << endl;
    {
        Dog dog("Rex");
        Animal* ptr = &dog;

        ptr->makeSound();  // Virtual - calls Dog::makeSound()
        ptr->sleep();      // Non-virtual - calls Animal::sleep()

        dog.sleep();       // Calls Dog::sleep() directly
    }

    // 3. Override keyword
    cout << "\n3. Override Keyword" << endl;
    cout << "--------------------" << endl;
    {
        Base* basePtr;
        Derived derived;

        basePtr = &derived;
        basePtr->func1();  // Calls Derived::func1()
        basePtr->func2();  // Calls Derived::func2()
        basePtr->func3();  // Calls Base::func3() (not virtual)
    }

    // 4. Final keyword
    cout << "\n4. Final Keyword" << endl;
    cout << "-----------------" << endl;
    {
        BaseClass* ptr;
        DerivedClass derived;

        ptr = &derived;
        ptr->method1();  // Calls DerivedClass::method1()
        ptr->method2();  // Calls BaseClass::method2() (final)
        ptr->method3();  // Calls DerivedClass::method3() (final)
    }

    // 5. Pure virtual functions
    cout << "\n5. Pure Virtual Functions" << endl;
    cout << "--------------------------" << endl;
    {
        // Shape shape("red");  // Error: can't instantiate abstract class
        Circle circle("blue", 5.0);
        circle.display();

        Shape* shapePtr = &circle;
        shapePtr->display();
        cout << "Area: " << shapePtr->area() << endl;
    }

    // 6. Virtual destructor importance
    cout << "\n6. Virtual Destructor Importance" << endl;
    cout << "---------------------------------" << endl;
    {
        cout << "WITH virtual destructor:" << endl;
        ResourceManager* mgr = new FileManager();
        delete mgr;  // Properly calls both destructors
        cout << endl;
    }

    // 7. Virtual functions in constructor/destructor
    cout << "7. Virtual Functions in Constructor/Destructor" << endl;
    cout << "-----------------------------------------------" << endl;
    {
        cout << "Creating derived object:" << endl;
        DerivedConstructorVirtual obj;
        cout << "\nDestroying object:" << endl;
    }

    // 8. Covariant return types
    cout << "\n8. Covariant Return Types" << endl;
    cout << "--------------------------" << endl;
    {
        Manager mgr("Alice", 5);
        Manager* clonedMgr = mgr.clone();  // Returns Manager*

        mgr.display();
        clonedMgr->display();

        delete clonedMgr;
    }

    // 9. Object slicing problem
    cout << "\n9. Object Slicing Problem" << endl;
    cout << "--------------------------" << endl;
    {
        Car car("Toyota", 4);

        cout << "Using pointer (no slicing):" << endl;
        Vehicle* vPtr = &car;
        vPtr->info();  // Calls Car::info()

        cout << "\nUsing value (slicing occurs):" << endl;
        Vehicle v = car;  // Slices off Car-specific data
        v.info();         // Calls Vehicle::info()
    }

    // 10. Multiple levels of inheritance
    cout << "\n10. Multiple Levels of Virtual Functions" << endl;
    cout << "-----------------------------------------" << endl;
    {
        A* ptr;
        C c;

        ptr = &c;
        ptr->func();  // Calls C::func()

        B b;
        ptr = &b;
        ptr->func();  // Calls B::func()
    }

    // 11. Polymorphic container
    demonstratePolymorphism();

    // 12. Array of polymorphic objects
    cout << "\n12. Array of Polymorphic Objects" << endl;
    cout << "---------------------------------" << endl;
    {
        Animal* animals[3];
        animals[0] = new Dog("Rocky");
        animals[1] = new Cat("Fluffy");
        animals[2] = new Dog("Charlie");

        for (int i = 0; i < 3; i++) {
            cout << "\nAnimal " << i + 1 << ":" << endl;
            animals[i]->makeSound();
            animals[i]->eat();
        }

        // Clean up with virtual destructors
        for (int i = 0; i < 3; i++) {
            delete animals[i];  // Properly calls derived destructors
        }
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Virtual functions enable runtime polymorphism" << endl;
    cout << "2. Virtual tables (vtables) manage dynamic binding" << endl;
    cout << "3. Override keyword ensures correct overriding" << endl;
    cout << "4. Final keyword prevents further overriding" << endl;
    cout << "5. Virtual destructors are essential for polymorphic classes" << endl;
    cout << "6. Pure virtual functions create abstract classes" << endl;
    cout << "7. Virtual functions use late (dynamic) binding" << endl;
    cout << "8. Non-virtual functions use early (static) binding" << endl;
    cout << "9. Covariant return types in virtual functions" << endl;
    cout << "10. Object slicing with non-pointer/reference types" << endl;
    cout << "11. Virtual function calls in constructors/destructors" << endl;

    return 0;
}
