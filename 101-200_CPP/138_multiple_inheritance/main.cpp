/*
 * Program 138: Multiple Inheritance in C++
 *
 * This program demonstrates:
 * - Multiple inheritance basics
 * - Inheriting from multiple base classes
 * - Name ambiguity and resolution
 * - Diamond problem introduction
 * - Constructor order in multiple inheritance
 * - Use cases and best practices
 * - Interface implementation pattern
 */

#include <iostream>
#include <string>

using namespace std;

// ===== BASIC MULTIPLE INHERITANCE =====

class Flyer {
protected:
    double maxAltitude;

public:
    Flyer(double alt) : maxAltitude(alt) {
        cout << "Flyer constructor" << endl;
    }

    virtual ~Flyer() {
        cout << "Flyer destructor" << endl;
    }

    void fly() {
        cout << "Flying at altitude " << maxAltitude << " feet" << endl;
    }

    double getMaxAltitude() const { return maxAltitude; }
};

class Swimmer {
protected:
    double maxDepth;

public:
    Swimmer(double depth) : maxDepth(depth) {
        cout << "Swimmer constructor" << endl;
    }

    virtual ~Swimmer() {
        cout << "Swimmer destructor" << endl;
    }

    void swim() {
        cout << "Swimming at depth " << maxDepth << " feet" << endl;
    }

    double getMaxDepth() const { return maxDepth; }
};

// Duck inherits from both Flyer and Swimmer
class Duck : public Flyer, public Swimmer {
private:
    string name;

public:
    Duck(const string& n, double alt, double depth)
        : Flyer(alt), Swimmer(depth), name(n) {
        cout << "Duck constructor: " << name << endl;
    }

    ~Duck() {
        cout << "Duck destructor: " << name << endl;
    }

    void quack() {
        cout << name << " says: Quack!" << endl;
    }

    void displayInfo() {
        cout << "\nDuck: " << name << endl;
        cout << "Can fly up to " << maxAltitude << " feet" << endl;
        cout << "Can swim down to " << maxDepth << " feet" << endl;
    }
};

// ===== NAME AMBIGUITY =====

class Device {
public:
    void start() {
        cout << "Device: Starting..." << endl;
    }

    void displayInfo() {
        cout << "Device information" << endl;
    }
};

class PowerSource {
public:
    void start() {
        cout << "PowerSource: Powering on..." << endl;
    }

    void displayInfo() {
        cout << "Power source information" << endl;
    }
};

class Laptop : public Device, public PowerSource {
public:
    void boot() {
        // Ambiguity: which start() to call?
        // Must use scope resolution
        Device::start();
        PowerSource::start();
        cout << "Laptop: Booting OS..." << endl;
    }

    void showInfo() {
        cout << "\nLaptop Info:" << endl;
        Device::displayInfo();
        PowerSource::displayInfo();
    }
};

// ===== INTERFACE PATTERN WITH MULTIPLE INHERITANCE =====

// Pure abstract classes as interfaces
class Printable {
public:
    virtual ~Printable() {}
    virtual void print() const = 0;
};

class Scannable {
public:
    virtual ~Scannable() {}
    virtual void scan() = 0;
};

class Faxable {
public:
    virtual ~Faxable() {}
    virtual void fax(const string& number) = 0;
};

// Implements multiple interfaces
class MultiFunctionPrinter : public Printable, public Scannable, public Faxable {
private:
    string model;

public:
    MultiFunctionPrinter(const string& m) : model(m) {
        cout << "MultiFunctionPrinter created: " << model << endl;
    }

    void print() const override {
        cout << model << ": Printing document..." << endl;
    }

    void scan() override {
        cout << model << ": Scanning document..." << endl;
    }

    void fax(const string& number) override {
        cout << model << ": Faxing to " << number << "..." << endl;
    }
};

// ===== MULTIPLE INHERITANCE WITH DATA =====

class Person {
protected:
    string name;
    int age;

public:
    Person(const string& n, int a) : name(n), age(a) {
        cout << "Person constructor: " << name << endl;
    }

    virtual ~Person() {
        cout << "Person destructor: " << name << endl;
    }

    void introduce() {
        cout << "Hi, I'm " << name << ", " << age << " years old" << endl;
    }
};

class Employee {
protected:
    int employeeId;
    double salary;

public:
    Employee(int id, double sal) : employeeId(id), salary(sal) {
        cout << "Employee constructor: ID " << id << endl;
    }

    virtual ~Employee() {
        cout << "Employee destructor: ID " << employeeId << endl;
    }

    void work() {
        cout << "Employee " << employeeId << " is working" << endl;
    }
};

class Student {
protected:
    int studentId;
    string major;

public:
    Student(int id, const string& maj) : studentId(id), major(maj) {
        cout << "Student constructor: ID " << id << endl;
    }

    virtual ~Student() {
        cout << "Student destructor: ID " << studentId << endl;
    }

    void study() {
        cout << "Student " << studentId << " studying " << major << endl;
    }
};

// Teaching Assistant is both Employee and Student
class TeachingAssistant : public Employee, public Student {
private:
    string department;

public:
    TeachingAssistant(int empId, double sal, int stuId, const string& maj, const string& dept)
        : Employee(empId, sal), Student(stuId, maj), department(dept) {
        cout << "TeachingAssistant constructor: " << department << endl;
    }

    ~TeachingAssistant() {
        cout << "TeachingAssistant destructor: " << department << endl;
    }

    void performDuties() {
        cout << "\nTeaching Assistant in " << department << " department:" << endl;
        work();   // From Employee
        study();  // From Student
        cout << "Also grading papers and holding office hours" << endl;
    }

    void displayInfo() {
        cout << "\n=== Teaching Assistant Info ===" << endl;
        cout << "Employee ID: " << employeeId << endl;
        cout << "Student ID: " << studentId << endl;
        cout << "Major: " << major << endl;
        cout << "Department: " << department << endl;
        cout << "Salary: $" << salary << endl;
    }
};

// ===== MULTIPLE INHERITANCE WITH VIRTUAL FUNCTIONS =====

class Shape2D {
public:
    virtual ~Shape2D() {}

    virtual double area() const = 0;

    virtual void draw2D() const {
        cout << "Drawing 2D shape" << endl;
    }
};

class Shape3D {
public:
    virtual ~Shape3D() {}

    virtual double volume() const = 0;

    virtual void draw3D() const {
        cout << "Drawing 3D shape" << endl;
    }
};

class Cylinder : public Shape2D, public Shape3D {
private:
    double radius;
    double height;

public:
    Cylinder(double r, double h) : radius(r), height(h) {
        cout << "Cylinder created: radius=" << r << ", height=" << h << endl;
    }

    // Implement from Shape2D (circular base)
    double area() const override {
        return 3.14159 * radius * radius;
    }

    void draw2D() const override {
        cout << "Drawing circular base with radius " << radius << endl;
    }

    // Implement from Shape3D
    double volume() const override {
        return area() * height;
    }

    void draw3D() const override {
        cout << "Drawing cylinder with radius " << radius
             << " and height " << height << endl;
    }
};

// ===== MIXIN PATTERN =====

class Timestamped {
protected:
    string timestamp;

public:
    Timestamped() : timestamp("2025-01-01 12:00:00") {
        cout << "Timestamped mixin added" << endl;
    }

    void setTimestamp(const string& ts) {
        timestamp = ts;
    }

    string getTimestamp() const {
        return timestamp;
    }
};

class Serializable {
public:
    virtual ~Serializable() {}

    virtual string serialize() const {
        return "[Serialized data]";
    }
};

class Document : public Timestamped, public Serializable {
private:
    string title;
    string content;

public:
    Document(const string& t, const string& c) : title(t), content(c) {
        cout << "Document created: " << title << endl;
    }

    string serialize() const override {
        return "Document{title='" + title + "', content='" + content +
               "', timestamp='" + timestamp + "'}";
    }

    void display() {
        cout << "\n=== Document ===" << endl;
        cout << "Title: " << title << endl;
        cout << "Content: " << content << endl;
        cout << "Timestamp: " << getTimestamp() << endl;
    }
};

// ===== ADAPTER PATTERN WITH MULTIPLE INHERITANCE =====

class OldPrinter {
public:
    void printOldWay(const string& text) {
        cout << "Old printer: " << text << endl;
    }
};

class ModernPrintable {
public:
    virtual ~ModernPrintable() {}
    virtual void print() = 0;
};

class PrinterAdapter : public ModernPrintable, private OldPrinter {
private:
    string documentText;

public:
    PrinterAdapter(const string& text) : documentText(text) {}

    void print() override {
        cout << "Adapter converting to old format..." << endl;
        printOldWay(documentText);
    }
};

// ===== CONSTRUCTION AND DESTRUCTION ORDER =====

class Base1 {
public:
    Base1() { cout << "Base1 constructor" << endl; }
    ~Base1() { cout << "Base1 destructor" << endl; }
};

class Base2 {
public:
    Base2() { cout << "Base2 constructor" << endl; }
    ~Base2() { cout << "Base2 destructor" << endl; }
};

class Base3 {
public:
    Base3() { cout << "Base3 constructor" << endl; }
    ~Base3() { cout << "Base3 destructor" << endl; }
};

class MultiDerived : public Base1, public Base2, public Base3 {
public:
    MultiDerived() { cout << "MultiDerived constructor" << endl; }
    ~MultiDerived() { cout << "MultiDerived destructor" << endl; }
};

int main() {
    cout << "=== Program 138: Multiple Inheritance ===" << endl;
    cout << "=========================================\n" << endl;

    // 1. Basic multiple inheritance
    cout << "1. Basic Multiple Inheritance - Duck" << endl;
    cout << "-------------------------------------" << endl;
    {
        Duck mallard("Mallard", 10000, 20);
        mallard.quack();
        mallard.fly();
        mallard.swim();
        mallard.displayInfo();
        cout << "\nDestruction order:" << endl;
    }

    // 2. Name ambiguity
    cout << "\n\n2. Name Ambiguity Resolution" << endl;
    cout << "-----------------------------" << endl;
    {
        Laptop myLaptop;
        myLaptop.boot();
        myLaptop.showInfo();
    }

    // 3. Interface pattern
    cout << "\n\n3. Interface Pattern - Multiple Interfaces" << endl;
    cout << "-------------------------------------------" << endl;
    {
        MultiFunctionPrinter mfp("HP LaserJet Pro");

        Printable* printable = &mfp;
        printable->print();

        Scannable* scannable = &mfp;
        scannable->scan();

        Faxable* faxable = &mfp;
        faxable->fax("555-1234");
    }

    // 4. Teaching Assistant - multiple roles
    cout << "\n\n4. Teaching Assistant - Multiple Roles" << endl;
    cout << "---------------------------------------" << endl;
    {
        TeachingAssistant ta(1001, 25000.0, 2001, "Computer Science", "CS");
        ta.displayInfo();
        ta.performDuties();
        cout << "\nDestruction order:" << endl;
    }

    // 5. Shapes with multiple inheritance
    cout << "\n\n5. 2D and 3D Shapes - Cylinder" << endl;
    cout << "-------------------------------" << endl;
    {
        Cylinder cyl(5.0, 10.0);

        Shape2D* shape2d = &cyl;
        cout << "\nAs 2D shape:" << endl;
        shape2d->draw2D();
        cout << "Base area: " << shape2d->area() << endl;

        Shape3D* shape3d = &cyl;
        cout << "\nAs 3D shape:" << endl;
        shape3d->draw3D();
        cout << "Volume: " << shape3d->volume() << endl;
    }

    // 6. Mixin pattern
    cout << "\n\n6. Mixin Pattern - Document" << endl;
    cout << "----------------------------" << endl;
    {
        Document doc("Meeting Notes", "Discuss project milestones");
        doc.setTimestamp("2025-11-17 10:30:00");
        doc.display();
        cout << "Serialized: " << doc.serialize() << endl;
    }

    // 7. Adapter pattern
    cout << "\n\n7. Adapter Pattern with Multiple Inheritance" << endl;
    cout << "---------------------------------------------" << endl;
    {
        PrinterAdapter adapter("Hello from adapter");
        adapter.print();
    }

    // 8. Constructor/Destructor order
    cout << "\n\n8. Construction and Destruction Order" << endl;
    cout << "--------------------------------------" << endl;
    {
        cout << "Creating object:" << endl;
        MultiDerived obj;
        cout << "\nDestroying object:" << endl;
    }

    // 9. Polymorphism with multiple bases
    cout << "\n\n9. Polymorphism with Multiple Bases" << endl;
    cout << "------------------------------------" << endl;
    {
        Duck duck("Donald", 8000, 15);

        Flyer* flyer = &duck;
        flyer->fly();

        Swimmer* swimmer = &duck;
        swimmer->swim();
    }

    cout << "\n\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Multiple inheritance - inherit from multiple classes" << endl;
    cout << "2. Name ambiguity - resolve with scope resolution (::)" << endl;
    cout << "3. Constructor order - left to right in inheritance list" << endl;
    cout << "4. Destructor order - reverse of construction order" << endl;
    cout << "5. Interface implementation - multiple pure virtual bases" << endl;
    cout << "6. Mixin pattern - add functionality through inheritance" << endl;
    cout << "7. Diamond problem preview - duplicate base classes" << endl;
    cout << "8. Polymorphism - pointers to different base classes" << endl;
    cout << "9. Real-world modeling - objects with multiple capabilities" << endl;
    cout << "10. Use cases - interfaces, mixins, adapters" << endl;

    cout << "\nNote: Be careful with multiple inheritance!" << endl;
    cout << "It can lead to complexity. Use virtual inheritance for diamond problem." << endl;

    return 0;
}
