/*
 * Program 123: Inheritance in C++
 *
 * This program demonstrates:
 * - Single inheritance
 * - Access specifiers in inheritance (public, protected, private)
 * - Base class access
 * - Method overriding
 * - Constructor and destructor chaining
 * - Protected members
 * - Calling base class methods
 */

#include <iostream>
#include <string>
#include <vector>

using namespace std;

// ===== BASIC INHERITANCE =====

// Base class
class Animal {
protected:
    string name;
    int age;
    string species;

public:
    Animal(string n, int a, string s) : name(n), age(a), species(s) {
        cout << "Animal constructor called for: " << name << endl;
    }

    virtual ~Animal() {
        cout << "Animal destructor called for: " << name << endl;
    }

    void eat() {
        cout << name << " is eating." << endl;
    }

    void sleep() {
        cout << name << " is sleeping." << endl;
    }

    virtual void makeSound() {
        cout << name << " makes a generic animal sound." << endl;
    }

    void displayInfo() {
        cout << "Name: " << name << ", Age: " << age
             << ", Species: " << species << endl;
    }

    string getName() const {
        return name;
    }
};

// Derived class - public inheritance
class Dog : public Animal {
private:
    string breed;

public:
    Dog(string n, int a, string b)
        : Animal(n, a, "Dog"), breed(b) {
        cout << "Dog constructor called" << endl;
    }

    ~Dog() {
        cout << "Dog destructor called" << endl;
    }

    // Override base class method
    void makeSound() override {
        cout << name << " barks: Woof! Woof!" << endl;
    }

    void fetch() {
        cout << name << " is fetching the ball!" << endl;
    }

    void displayDogInfo() {
        displayInfo();  // Calling base class method
        cout << "Breed: " << breed << endl;
    }

    // Method that uses protected members from base class
    void celebrate() {
        cout << name << " (age " << age << ") is celebrating!" << endl;
    }
};

// Another derived class
class Cat : public Animal {
private:
    bool isIndoor;

public:
    Cat(string n, int a, bool indoor)
        : Animal(n, a, "Cat"), isIndoor(indoor) {
        cout << "Cat constructor called" << endl;
    }

    ~Cat() {
        cout << "Cat destructor called" << endl;
    }

    void makeSound() override {
        cout << name << " meows: Meow! Meow!" << endl;
    }

    void scratch() {
        cout << name << " is scratching the furniture." << endl;
    }

    void displayCatInfo() {
        displayInfo();
        cout << "Indoor cat: " << (isIndoor ? "Yes" : "No") << endl;
    }
};

// ===== PROTECTED INHERITANCE =====

class Vehicle {
protected:
    string brand;
    int year;

public:
    Vehicle(string b, int y) : brand(b), year(y) {
        cout << "Vehicle constructor: " << brand << endl;
    }

    virtual ~Vehicle() {
        cout << "Vehicle destructor" << endl;
    }

    void displayVehicle() {
        cout << "Brand: " << brand << ", Year: " << year << endl;
    }

    void startEngine() {
        cout << brand << " engine started!" << endl;
    }
};

// Protected inheritance - public members of base become protected
class Car : protected Vehicle {
private:
    int numDoors;

public:
    Car(string b, int y, int doors)
        : Vehicle(b, y), numDoors(doors) {
        cout << "Car constructor" << endl;
    }

    ~Car() {
        cout << "Car destructor" << endl;
    }

    // Public method that uses protected base class methods
    void displayCar() {
        cout << "Car Information:" << endl;
        displayVehicle();  // Can access because it's protected now
        cout << "Number of doors: " << numDoors << endl;
    }

    void start() {
        startEngine();  // Can access protected member
    }

    // Expose specific base functionality
    void showBrand() {
        cout << "This car is a " << brand << endl;
    }
};

// ===== PRIVATE INHERITANCE =====

class Engine {
protected:
    int horsepower;
    string type;

public:
    Engine(int hp, string t) : horsepower(hp), type(t) {
        cout << "Engine constructor: " << hp << " HP, " << type << endl;
    }

    virtual ~Engine() {
        cout << "Engine destructor" << endl;
    }

    void displayEngine() {
        cout << "Engine: " << horsepower << " HP, Type: " << type << endl;
    }

    int getHorsepower() {
        return horsepower;
    }
};

// Private inheritance - all base members become private
class Motorcycle : private Engine {
private:
    string model;

public:
    Motorcycle(string m, int hp, string type)
        : Engine(hp, type), model(m) {
        cout << "Motorcycle constructor" << endl;
    }

    ~Motorcycle() {
        cout << "Motorcycle destructor" << endl;
    }

    void displayMotorcycle() {
        cout << "Motorcycle: " << model << endl;
        displayEngine();  // Can access privately
    }

    // Expose specific functionality
    int getPower() {
        return getHorsepower();  // Can access privately
    }
};

// ===== MULTI-LEVEL INHERITANCE =====

class LivingBeing {
protected:
    bool isAlive;

public:
    LivingBeing() : isAlive(true) {
        cout << "LivingBeing constructor" << endl;
    }

    virtual ~LivingBeing() {
        cout << "LivingBeing destructor" << endl;
    }

    void breathe() {
        cout << "Breathing..." << endl;
    }
};

class Mammal : public LivingBeing {
protected:
    bool hasHair;

public:
    Mammal(bool hair) : hasHair(hair) {
        cout << "Mammal constructor" << endl;
    }

    ~Mammal() {
        cout << "Mammal destructor" << endl;
    }

    void feedYoung() {
        cout << "Feeding young with milk." << endl;
    }
};

class Human : public Mammal {
private:
    string name;
    int iq;

public:
    Human(string n, int intelligence)
        : Mammal(true), name(n), iq(intelligence) {
        cout << "Human constructor" << endl;
    }

    ~Human() {
        cout << "Human destructor" << endl;
    }

    void speak() {
        cout << name << " is speaking." << endl;
    }

    void displayHuman() {
        cout << "Human: " << name << ", IQ: " << iq << endl;
        breathe();      // From LivingBeing
        feedYoung();    // From Mammal
    }
};

// ===== CALLING BASE CLASS METHODS =====

class Shape {
protected:
    string color;

public:
    Shape(string c) : color(c) {}

    virtual void draw() {
        cout << "Drawing a " << color << " shape" << endl;
    }

    virtual double area() {
        return 0.0;
    }
};

class Circle : public Shape {
private:
    double radius;

public:
    Circle(string c, double r) : Shape(c), radius(r) {}

    void draw() override {
        Shape::draw();  // Call base class method
        cout << "Specifically, it's a circle with radius " << radius << endl;
    }

    double area() override {
        return 3.14159 * radius * radius;
    }
};

// ===== ACCESS CONTROL DEMONSTRATION =====

class Base {
private:
    int privateVar;

protected:
    int protectedVar;

public:
    int publicVar;

    Base() : privateVar(10), protectedVar(20), publicVar(30) {}

    void showBase() {
        cout << "Base - Private: " << privateVar
             << ", Protected: " << protectedVar
             << ", Public: " << publicVar << endl;
    }
};

class Derived : public Base {
public:
    void showAccess() {
        // Can't access privateVar
        // cout << privateVar;  // Error!

        // Can access protectedVar
        cout << "Protected from derived: " << protectedVar << endl;

        // Can access publicVar
        cout << "Public from derived: " << publicVar << endl;
    }

    void modifyProtected(int val) {
        protectedVar = val;  // Can modify protected members
    }
};

int main() {
    cout << "=== Program 123: Inheritance in C++ ===" << endl;
    cout << "======================================\n" << endl;

    // 1. Basic public inheritance
    cout << "1. Public Inheritance - Animals" << endl;
    cout << "--------------------------------" << endl;
    {
        Dog myDog("Buddy", 3, "Golden Retriever");
        myDog.displayDogInfo();
        myDog.makeSound();
        myDog.eat();      // Inherited from Animal
        myDog.sleep();    // Inherited from Animal
        myDog.fetch();    // Dog-specific method
        myDog.celebrate();

        cout << endl;

        Cat myCat("Whiskers", 2, true);
        myCat.displayCatInfo();
        myCat.makeSound();
        myCat.scratch();
    }

    // 2. Protected inheritance
    cout << "\n2. Protected Inheritance - Car" << endl;
    cout << "-------------------------------" << endl;
    {
        Car myCar("Toyota", 2022, 4);
        myCar.displayCar();
        myCar.start();
        myCar.showBrand();

        // Can't access Vehicle methods directly (they're protected)
        // myCar.displayVehicle();  // Error!
        // myCar.startEngine();     // Error!
    }

    // 3. Private inheritance
    cout << "\n3. Private Inheritance - Motorcycle" << endl;
    cout << "------------------------------------" << endl;
    {
        Motorcycle bike("Harley Davidson", 100, "V-Twin");
        bike.displayMotorcycle();
        cout << "Power: " << bike.getPower() << " HP" << endl;

        // Can't access Engine methods directly (they're private)
        // bike.displayEngine();    // Error!
        // bike.getHorsepower();    // Error!
    }

    // 4. Multi-level inheritance
    cout << "\n4. Multi-Level Inheritance - Human" << endl;
    cout << "-----------------------------------" << endl;
    {
        Human person("Alice", 140);
        person.displayHuman();
        person.speak();
    }

    // 5. Calling base class methods
    cout << "\n5. Calling Base Class Methods" << endl;
    cout << "------------------------------" << endl;
    {
        Circle circle("red", 5.0);
        circle.draw();
        cout << "Area: " << circle.area() << endl;
    }

    // 6. Access control in inheritance
    cout << "\n6. Access Control in Inheritance" << endl;
    cout << "---------------------------------" << endl;
    {
        Derived derived;
        derived.showBase();      // Can access public method
        derived.showAccess();    // Shows what derived class can access
        derived.publicVar = 100; // Can access public members
        derived.modifyProtected(200);
        derived.showBase();

        // Can't access protected members from outside
        // derived.protectedVar = 50;  // Error!
    }

    // 7. Polymorphism preview with inheritance
    cout << "\n7. Polymorphism with Inheritance" << endl;
    cout << "---------------------------------" << endl;
    {
        Animal* animals[3];
        animals[0] = new Dog("Max", 4, "Labrador");
        animals[1] = new Cat("Felix", 3, false);
        animals[2] = new Animal("Generic", 5, "Unknown");

        for (int i = 0; i < 3; i++) {
            cout << "\nAnimal " << i + 1 << ":" << endl;
            animals[i]->displayInfo();
            animals[i]->makeSound();  // Polymorphic call
        }

        // Clean up
        for (int i = 0; i < 3; i++) {
            delete animals[i];
        }
    }

    // 8. Constructor and destructor order
    cout << "\n8. Constructor/Destructor Order" << endl;
    cout << "--------------------------------" << endl;
    {
        cout << "Creating Dog object:" << endl;
        Dog tempDog("Temporary", 1, "Poodle");
        cout << "\nGoing out of scope:" << endl;
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Public inheritance - 'is-a' relationship" << endl;
    cout << "2. Protected inheritance - restricted 'is-a' relationship" << endl;
    cout << "3. Private inheritance - 'implemented-in-terms-of' relationship" << endl;
    cout << "4. Protected members - accessible in derived classes" << endl;
    cout << "5. Method overriding - redefining base class behavior" << endl;
    cout << "6. Calling base class methods using scope resolution" << endl;
    cout << "7. Constructor/destructor chaining" << endl;
    cout << "8. Multi-level inheritance" << endl;
    cout << "9. Access control in inheritance" << endl;

    return 0;
}
