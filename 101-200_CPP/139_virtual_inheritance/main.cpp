/*
 * Program 139: Virtual Inheritance in C++
 *
 * This program demonstrates:
 * - Diamond problem
 * - Virtual inheritance solution
 * - Constructor calling in virtual inheritance
 * - Memory layout differences
 * - Practical use cases
 * - Virtual base class initialization
 */

#include <iostream>
#include <string>

using namespace std;

// ===== DIAMOND PROBLEM WITHOUT VIRTUAL INHERITANCE =====

class Animal {
protected:
    string name;

public:
    Animal(const string& n) : name(n) {
        cout << "Animal constructor: " << name << endl;
    }

    void eat() {
        cout << name << " is eating" << endl;
    }

    void displayName() {
        cout << "Animal name: " << name << endl;
    }
};

class Mammal : public Animal {
public:
    Mammal(const string& n) : Animal(n) {
        cout << "Mammal constructor" << endl;
    }

    void feedYoung() {
        cout << name << " feeds young with milk" << endl;
    }
};

class Bird : public Animal {
public:
    Bird(const string& n) : Animal(n) {
        cout << "Bird constructor" << endl;
    }

    void layEggs() {
        cout << name << " lays eggs" << endl;
    }
};

// Diamond problem: Bat has TWO copies of Animal!
class Bat : public Mammal, public Bird {
public:
    Bat(const string& n) : Mammal(n), Bird(n) {
        cout << "Bat constructor" << endl;
    }

    void fly() {
        cout << "Bat is flying" << endl;
    }

    // Ambiguity - which name to use?
    void showInfo() {
        // name is ambiguous
        // displayName() is ambiguous
        Mammal::displayName();  // Must specify which one
        Bird::displayName();    // Two different Animals!
    }
};

// ===== DIAMOND PROBLEM SOLVED WITH VIRTUAL INHERITANCE =====

class AnimalVirtual {
protected:
    string name;

public:
    AnimalVirtual(const string& n = "Unknown") : name(n) {
        cout << "AnimalVirtual constructor: " << name << endl;
    }

    virtual ~AnimalVirtual() {
        cout << "AnimalVirtual destructor: " << name << endl;
    }

    void eat() {
        cout << name << " is eating" << endl;
    }

    void displayName() {
        cout << "Animal name: " << name << endl;
    }
};

// Virtual inheritance - only ONE copy of AnimalVirtual
class MammalVirtual : virtual public AnimalVirtual {
public:
    MammalVirtual(const string& n) : AnimalVirtual(n) {
        cout << "MammalVirtual constructor" << endl;
    }

    ~MammalVirtual() {
        cout << "MammalVirtual destructor" << endl;
    }

    void feedYoung() {
        cout << name << " feeds young with milk" << endl;
    }
};

class BirdVirtual : virtual public AnimalVirtual {
public:
    BirdVirtual(const string& n) : AnimalVirtual(n) {
        cout << "BirdVirtual constructor" << endl;
    }

    ~BirdVirtual() {
        cout << "BirdVirtual destructor" << endl;
    }

    void layEggs() {
        cout << name << " lays eggs" << endl;
    }
};

// Now Bat has only ONE copy of AnimalVirtual!
class BatVirtual : public MammalVirtual, public BirdVirtual {
public:
    // IMPORTANT: Most derived class must initialize virtual base
    BatVirtual(const string& n)
        : AnimalVirtual(n),  // Initialize virtual base directly
          MammalVirtual(n),
          BirdVirtual(n) {
        cout << "BatVirtual constructor" << endl;
    }

    ~BatVirtual() {
        cout << "BatVirtual destructor" << endl;
    }

    void fly() {
        cout << name << " is flying" << endl;
    }

    void showInfo() {
        // No ambiguity - only one name
        displayName();
        eat();
        feedYoung();
        layEggs();
        fly();
    }
};

// ===== PRACTICAL EXAMPLE: IOSTREAM HIERARCHY =====

// Similar to std::ios_base
class IOBase {
protected:
    int state;

public:
    IOBase() : state(0) {
        cout << "IOBase constructor" << endl;
    }

    virtual ~IOBase() {
        cout << "IOBase destructor" << endl;
    }

    void setState(int s) { state = s; }
    int getState() const { return state; }
};

// Similar to std::istream
class InputStream : virtual public IOBase {
public:
    InputStream() {
        cout << "InputStream constructor" << endl;
    }

    ~InputStream() {
        cout << "InputStream destructor" << endl;
    }

    void read() {
        cout << "Reading input (state: " << state << ")" << endl;
    }
};

// Similar to std::ostream
class OutputStream : virtual public IOBase {
public:
    OutputStream() {
        cout << "OutputStream constructor" << endl;
    }

    ~OutputStream() {
        cout << "OutputStream destructor" << endl;
    }

    void write() {
        cout << "Writing output (state: " << state << ")" << endl;
    }
};

// Similar to std::iostream
class IOStream : public InputStream, public OutputStream {
public:
    IOStream() {
        cout << "IOStream constructor" << endl;
    }

    ~IOStream() {
        cout << "IOStream destructor" << endl;
    }

    void process() {
        read();
        write();
        cout << "Processing I/O (shared state: " << state << ")" << endl;
    }
};

// ===== COMPLEX HIERARCHY WITH VIRTUAL INHERITANCE =====

class Device {
protected:
    string deviceId;

public:
    Device(const string& id = "DEVICE-000") : deviceId(id) {
        cout << "Device constructor: " << deviceId << endl;
    }

    virtual ~Device() {
        cout << "Device destructor" << endl;
    }

    void powerOn() {
        cout << deviceId << " powered on" << endl;
    }
};

class Scanner : virtual public Device {
public:
    Scanner(const string& id) : Device(id) {
        cout << "Scanner constructor" << endl;
    }

    ~Scanner() {
        cout << "Scanner destructor" << endl;
    }

    void scan() {
        cout << deviceId << ": Scanning document" << endl;
    }
};

class Printer : virtual public Device {
public:
    Printer(const string& id) : Device(id) {
        cout << "Printer constructor" << endl;
    }

    ~Printer() {
        cout << "Printer destructor" << endl;
    }

    void print() {
        cout << deviceId << ": Printing document" << endl;
    }
};

class Copier : public Scanner, public Printer {
public:
    Copier(const string& id)
        : Device(id),  // Initialize virtual base
          Scanner(id),
          Printer(id) {
        cout << "Copier constructor" << endl;
    }

    ~Copier() {
        cout << "Copier destructor" << endl;
    }

    void copy() {
        cout << deviceId << ": Copying document" << endl;
        scan();
        print();
    }
};

// ===== VIRTUAL INHERITANCE WITH DATA =====

class Person {
protected:
    string name;
    int age;

public:
    Person(const string& n = "Unknown", int a = 0) : name(n), age(a) {
        cout << "Person constructor: " << name << endl;
    }

    virtual ~Person() {
        cout << "Person destructor" << endl;
    }

    void introduce() {
        cout << "Hi, I'm " << name << ", age " << age << endl;
    }
};

class Student : virtual public Person {
protected:
    int studentId;

public:
    Student(const string& n, int a, int id)
        : Person(n, a), studentId(id) {
        cout << "Student constructor: ID " << studentId << endl;
    }

    ~Student() {
        cout << "Student destructor" << endl;
    }

    void study() {
        cout << name << " (Student ID: " << studentId << ") is studying" << endl;
    }
};

class Employee : virtual public Person {
protected:
    int employeeId;

public:
    Employee(const string& n, int a, int id)
        : Person(n, a), employeeId(id) {
        cout << "Employee constructor: ID " << employeeId << endl;
    }

    ~Employee() {
        cout << "Employee destructor" << endl;
    }

    void work() {
        cout << name << " (Employee ID: " << employeeId << ") is working" << endl;
    }
};

class TeachingAssistant : public Student, public Employee {
public:
    TeachingAssistant(const string& n, int a, int stuId, int empId)
        : Person(n, a),  // Initialize virtual base directly
          Student(n, a, stuId),
          Employee(n, a, empId) {
        cout << "TeachingAssistant constructor" << endl;
    }

    ~TeachingAssistant() {
        cout << "TeachingAssistant destructor" << endl;
    }

    void performDuties() {
        cout << "\n" << name << "'s duties:" << endl;
        study();
        work();
        cout << "Also holding office hours" << endl;
    }
};

// ===== DEMONSTRATING SIZE DIFFERENCE =====

class BaseNonVirtual {
    int data;
};

class DerivedNonVirtual1 : public BaseNonVirtual {
    int data1;
};

class DerivedNonVirtual2 : public BaseNonVirtual {
    int data2;
};

class MultiDerivedNonVirtual : public DerivedNonVirtual1, public DerivedNonVirtual2 {
    int data3;
};

// ---

class BaseVirtual {
    int data;
};

class DerivedVirtual1 : virtual public BaseVirtual {
    int data1;
};

class DerivedVirtual2 : virtual public BaseVirtual {
    int data2;
};

class MultiDerivedVirtual : public DerivedVirtual1, public DerivedVirtual2 {
    int data3;
};

int main() {
    cout << "=== Program 139: Virtual Inheritance ===" << endl;
    cout << "========================================\n" << endl;

    // 1. Diamond problem WITHOUT virtual inheritance
    cout << "1. Diamond Problem - WITHOUT Virtual Inheritance" << endl;
    cout << "--------------------------------------------------" << endl;
    {
        Bat bat("Chiroptera");
        cout << "\nBat has TWO Animal objects:" << endl;
        bat.showInfo();
        cout << "\nDestruction:" << endl;
    }

    // 2. Diamond problem SOLVED with virtual inheritance
    cout << "\n\n2. Diamond Problem SOLVED - WITH Virtual Inheritance" << endl;
    cout << "-----------------------------------------------------" << endl;
    {
        BatVirtual batVirtual("VirtualChiroptera");
        cout << "\nBat has only ONE AnimalVirtual object:" << endl;
        batVirtual.showInfo();
        cout << "\nDestruction order:" << endl;
    }

    // 3. Practical example: IOStream hierarchy
    cout << "\n\n3. Practical Example - IOStream Hierarchy" << endl;
    cout << "------------------------------------------" << endl;
    {
        IOStream iostream;
        iostream.setState(42);
        iostream.process();
        cout << "\nDestruction order:" << endl;
    }

    // 4. Device hierarchy with copier
    cout << "\n\n4. Device Hierarchy - Copier" << endl;
    cout << "-----------------------------" << endl;
    {
        Copier copier("COPIER-001");
        copier.powerOn();
        copier.copy();
        cout << "\nDestruction order:" << endl;
    }

    // 5. Teaching Assistant with virtual inheritance
    cout << "\n\n5. Teaching Assistant - Virtual Inheritance" << endl;
    cout << "--------------------------------------------" << endl;
    {
        TeachingAssistant ta("Alice Johnson", 25, 2001, 1001);
        ta.introduce();  // Only one Person object!
        ta.performDuties();
        cout << "\nDestruction order:" << endl;
    }

    // 6. Constructor initialization demonstration
    cout << "\n\n6. Constructor Initialization Order" << endl;
    cout << "------------------------------------" << endl;
    {
        cout << "Creating BatVirtual:" << endl;
        BatVirtual bat("Demo");
        cout << "\nNote: Virtual base (AnimalVirtual) is constructed first," << endl;
        cout << "even though it appears last in the inheritance tree!" << endl;
    }

    // 7. Size comparison
    cout << "\n\n7. Memory Layout Comparison" << endl;
    cout << "----------------------------" << endl;
    {
        cout << "Without virtual inheritance:" << endl;
        cout << "  MultiDerivedNonVirtual size: "
             << sizeof(MultiDerivedNonVirtual) << " bytes" << endl;
        cout << "  (Contains TWO copies of BaseNonVirtual)" << endl;

        cout << "\nWith virtual inheritance:" << endl;
        cout << "  MultiDerivedVirtual size: "
             << sizeof(MultiDerivedVirtual) << " bytes" << endl;
        cout << "  (Contains only ONE copy of BaseVirtual)" << endl;
        cout << "  (Larger due to virtual table pointers)" << endl;
    }

    // 8. Polymorphism with virtual inheritance
    cout << "\n\n8. Polymorphism with Virtual Inheritance" << endl;
    cout << "-----------------------------------------" << endl;
    {
        BatVirtual bat("PolyBat");

        AnimalVirtual* animalPtr = &bat;
        animalPtr->eat();

        MammalVirtual* mammalPtr = &bat;
        mammalPtr->feedYoung();

        BirdVirtual* birdPtr = &bat;
        birdPtr->layEggs();
    }

    // 9. Accessing shared base
    cout << "\n\n9. Accessing Shared Virtual Base" << endl;
    cout << "----------------------------------" << endl;
    {
        TeachingAssistant ta("Bob Smith", 30, 3001, 2001);

        Person* personPtr = &ta;
        personPtr->introduce();

        Student* studentPtr = &ta;
        studentPtr->introduce();  // Same Person object

        Employee* employeePtr = &ta;
        employeePtr->introduce();  // Same Person object

        cout << "\nAll point to the SAME Person object!" << endl;
    }

    cout << "\n\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Diamond problem - multiple inheritance ambiguity" << endl;
    cout << "2. Virtual inheritance - solves diamond problem" << endl;
    cout << "3. Single shared base - only one copy with virtual" << endl;
    cout << "4. Most derived class - initializes virtual base" << endl;
    cout << "5. Constructor order - virtual bases first" << endl;
    cout << "6. Destructor order - reverse of construction" << endl;
    cout << "7. IOStream pattern - practical real-world use" << endl;
    cout << "8. Memory overhead - vtable pointers for virtual bases" << endl;
    cout << "9. No ambiguity - single path to virtual base" << endl;
    cout << "10. Polymorphism - works correctly with virtual inheritance" << endl;

    cout << "\nWhen to use virtual inheritance:" << endl;
    cout << "- Solving diamond problem in multiple inheritance" << endl;
    cout << "- Sharing common base class data/functionality" << endl;
    cout << "- iostream-like hierarchies" << endl;
    cout << "- Complex class hierarchies with shared roots" << endl;

    return 0;
}
