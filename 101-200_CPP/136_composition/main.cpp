/*
 * Program 136: Composition in C++
 *
 * This program demonstrates:
 * - Composition (Has-A relationship)
 * - Strong ownership - parts lifecycle depends on whole
 * - Member objects
 * - Initialization of composed objects
 * - Composition vs inheritance
 * - Encapsulation through composition
 * - Constructor initialization lists
 */

#include <iostream>
#include <string>
#include <vector>

using namespace std;

// ===== BASIC COMPOSITION =====

class Engine {
private:
    int horsepower;
    string type;

public:
    Engine(int hp, const string& t) : horsepower(hp), type(t) {
        cout << "Engine created: " << hp << " HP, " << type << endl;
    }

    ~Engine() {
        cout << "Engine destroyed" << endl;
    }

    void start() {
        cout << "Engine started: " << type << " engine roaring!" << endl;
    }

    void stop() {
        cout << "Engine stopped" << endl;
    }

    int getHorsepower() const { return horsepower; }
    string getType() const { return type; }
};

class Transmission {
private:
    string type;
    int gears;

public:
    Transmission(const string& t, int g) : type(t), gears(g) {
        cout << "Transmission created: " << gears << "-speed " << type << endl;
    }

    ~Transmission() {
        cout << "Transmission destroyed" << endl;
    }

    void shift(int gear) {
        cout << "Shifting to gear " << gear << endl;
    }

    string getType() const { return type; }
};

class Wheel {
private:
    int size;

public:
    Wheel(int s) : size(s) {
        cout << "Wheel created: " << size << " inches" << endl;
    }

    ~Wheel() {
        cout << "Wheel destroyed" << endl;
    }

    int getSize() const { return size; }
};

// Car "has-a" Engine, Transmission, and Wheels
class Car {
private:
    string brand;
    string model;
    Engine engine;              // Composition - Engine is part of Car
    Transmission transmission;  // Composition - Transmission is part of Car
    Wheel wheels[4];           // Composition - Wheels are part of Car

public:
    // Member initializer list for composed objects
    Car(const string& b, const string& m, int hp, const string& engineType,
        const string& transType, int gears, int wheelSize)
        : brand(b), model(m),
          engine(hp, engineType),
          transmission(transType, gears),
          wheels{Wheel(wheelSize), Wheel(wheelSize), Wheel(wheelSize), Wheel(wheelSize)} {
        cout << "Car created: " << brand << " " << model << endl;
    }

    ~Car() {
        cout << "Car destroyed: " << brand << " " << model << endl;
        // Composed objects automatically destroyed
    }

    void start() {
        cout << "\nStarting " << brand << " " << model << endl;
        engine.start();
        cout << "Car is ready to drive!" << endl;
    }

    void drive() {
        cout << "\nDriving " << brand << " " << model << endl;
        transmission.shift(1);
        transmission.shift(2);
        transmission.shift(3);
        cout << "Cruising at speed..." << endl;
    }

    void stop() {
        cout << "\nStopping " << brand << " " << model << endl;
        engine.stop();
        cout << "Car stopped" << endl;
    }

    void displayInfo() const {
        cout << "\n=== Car Information ===" << endl;
        cout << "Brand: " << brand << endl;
        cout << "Model: " << model << endl;
        cout << "Engine: " << engine.getHorsepower() << " HP "
             << engine.getType() << endl;
        cout << "Transmission: " << transmission.getType() << endl;
        cout << "Wheels: " << wheels[0].getSize() << " inches" << endl;
    }
};

// ===== COMPOSITION VS INHERITANCE =====

// Instead of inheritance, use composition
class Logger {
public:
    void log(const string& message) {
        cout << "[LOG] " << message << endl;
    }
};

// Rather than: class Service : public Logger
// Use composition:
class Service {
private:
    Logger logger;  // Has-a Logger
    string serviceName;

public:
    Service(const string& name) : serviceName(name) {
        logger.log("Service '" + serviceName + "' created");
    }

    void performTask() {
        logger.log("Performing task in " + serviceName);
        // Do work...
        logger.log("Task completed");
    }
};

// ===== ADDRESS AND PERSON COMPOSITION =====

class Address {
private:
    string street;
    string city;
    string state;
    string zipCode;

public:
    Address(const string& st, const string& c, const string& s, const string& z)
        : street(st), city(c), state(s), zipCode(z) {
        cout << "Address created: " << city << ", " << state << endl;
    }

    ~Address() {
        cout << "Address destroyed" << endl;
    }

    void display() const {
        cout << street << endl;
        cout << city << ", " << state << " " << zipCode << endl;
    }

    string getCity() const { return city; }
};

class Person {
private:
    string name;
    int age;
    Address homeAddress;  // Person "has-a" Address

public:
    Person(const string& n, int a, const Address& addr)
        : name(n), age(a), homeAddress(addr) {
        cout << "Person created: " << name << endl;
    }

    ~Person() {
        cout << "Person destroyed: " << name << endl;
    }

    void displayInfo() const {
        cout << "\n=== Person Information ===" << endl;
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
        cout << "Address:" << endl;
        homeAddress.display();
    }
};

// ===== COMPUTER COMPOSITION =====

class CPU {
private:
    string brand;
    double speed;

public:
    CPU(const string& b, double s) : brand(b), speed(s) {
        cout << "CPU: " << brand << " @ " << speed << " GHz" << endl;
    }

    ~CPU() { cout << "CPU destroyed" << endl; }

    void process() {
        cout << "CPU processing at " << speed << " GHz" << endl;
    }
};

class RAM {
private:
    int sizeGB;

public:
    RAM(int size) : sizeGB(size) {
        cout << "RAM: " << sizeGB << " GB" << endl;
    }

    ~RAM() { cout << "RAM destroyed" << endl; }

    void store() {
        cout << "Storing data in " << sizeGB << " GB RAM" << endl;
    }
};

class HardDrive {
private:
    int sizeTB;
    string type;

public:
    HardDrive(int size, const string& t) : sizeTB(size), type(t) {
        cout << "HardDrive: " << sizeTB << " TB " << type << endl;
    }

    ~HardDrive() { cout << "HardDrive destroyed" << endl; }

    void read() {
        cout << "Reading from " << type << " drive" << endl;
    }

    void write() {
        cout << "Writing to " << type << " drive" << endl;
    }
};

class Computer {
private:
    string brand;
    CPU cpu;
    RAM ram;
    HardDrive hdd;

public:
    Computer(const string& b, const string& cpuBrand, double cpuSpeed,
             int ramSize, int hddSize, const string& hddType)
        : brand(b),
          cpu(cpuBrand, cpuSpeed),
          ram(ramSize),
          hdd(hddSize, hddType) {
        cout << "Computer assembled: " << brand << endl;
    }

    ~Computer() {
        cout << "Computer destroyed: " << brand << endl;
    }

    void boot() {
        cout << "\nBooting " << brand << "..." << endl;
        cpu.process();
        ram.store();
        hdd.read();
        cout << "System ready!" << endl;
    }

    void saveFile() {
        cout << "\nSaving file..." << endl;
        cpu.process();
        ram.store();
        hdd.write();
        cout << "File saved!" << endl;
    }
};

// ===== BOOK AND LIBRARY =====

class Book {
private:
    string title;
    string author;
    string isbn;

public:
    Book(const string& t, const string& a, const string& i)
        : title(t), author(a), isbn(i) {
        cout << "Book created: " << title << endl;
    }

    ~Book() {
        cout << "Book destroyed: " << title << endl;
    }

    void display() const {
        cout << "  \"" << title << "\" by " << author
             << " (ISBN: " << isbn << ")" << endl;
    }

    string getTitle() const { return title; }
};

class Library {
private:
    string name;
    vector<Book> books;  // Library "has-many" Books

public:
    Library(const string& n) : name(n) {
        cout << "Library created: " << name << endl;
    }

    ~Library() {
        cout << "Library destroyed: " << name << endl;
    }

    void addBook(const Book& book) {
        books.push_back(book);
        cout << "Book added to library" << endl;
    }

    void displayCatalog() const {
        cout << "\n=== " << name << " Catalog ===" << endl;
        cout << "Total books: " << books.size() << endl;
        for (const auto& book : books) {
            book.display();
        }
    }
};

// ===== NESTED COMPOSITION =====

class Battery {
private:
    int capacity;

public:
    Battery(int cap) : capacity(cap) {
        cout << "Battery: " << capacity << " mAh" << endl;
    }

    ~Battery() { cout << "Battery destroyed" << endl; }

    void charge() {
        cout << "Charging " << capacity << " mAh battery" << endl;
    }
};

class Screen {
private:
    double size;

public:
    Screen(double s) : size(s) {
        cout << "Screen: " << size << " inches" << endl;
    }

    ~Screen() { cout << "Screen destroyed" << endl; }

    void display() {
        cout << "Displaying on " << size << "\" screen" << endl;
    }
};

class Camera {
private:
    int megapixels;

public:
    Camera(int mp) : megapixels(mp) {
        cout << "Camera: " << megapixels << " MP" << endl;
    }

    ~Camera() { cout << "Camera destroyed" << endl; }

    void takePhoto() {
        cout << "Taking " << megapixels << " MP photo" << endl;
    }
};

class Smartphone {
private:
    string brand;
    CPU cpu;
    RAM ram;
    Battery battery;
    Screen screen;
    Camera camera;

public:
    Smartphone(const string& b, const string& cpuBrand, double cpuSpeed,
               int ramSize, int battCap, double screenSize, int camMP)
        : brand(b),
          cpu(cpuBrand, cpuSpeed),
          ram(ramSize),
          battery(battCap),
          screen(screenSize),
          camera(camMP) {
        cout << "Smartphone assembled: " << brand << endl;
    }

    ~Smartphone() {
        cout << "Smartphone destroyed: " << brand << endl;
    }

    void makeCall() {
        cout << "\nMaking a call..." << endl;
        cpu.process();
        cout << "Call connected" << endl;
    }

    void takePhoto() {
        cout << "\nTaking a photo..." << endl;
        camera.takePhoto();
        screen.display();
        cpu.process();
        ram.store();
        cout << "Photo saved" << endl;
    }

    void playVideo() {
        cout << "\nPlaying video..." << endl;
        cpu.process();
        ram.store();
        screen.display();
        battery.charge();
        cout << "Video playing" << endl;
    }
};

int main() {
    cout << "=== Program 136: Composition ===" << endl;
    cout << "================================\n" << endl;

    // 1. Basic composition - Car
    cout << "1. Basic Composition - Car with Engine, Transmission, Wheels" << endl;
    cout << "-------------------------------------------------------------" << endl;
    {
        Car myCar("Toyota", "Camry", 200, "V6", "Automatic", 6, 17);
        myCar.displayInfo();
        myCar.start();
        myCar.drive();
        myCar.stop();
        cout << "\nCar going out of scope (composed objects destroyed automatically):" << endl;
    }

    // 2. Composition vs Inheritance
    cout << "\n\n2. Composition vs Inheritance - Service with Logger" << endl;
    cout << "----------------------------------------------------" << endl;
    {
        Service webService("WebAPI");
        webService.performTask();
    }

    // 3. Person has Address
    cout << "\n\n3. Person with Address Composition" << endl;
    cout << "------------------------------------" << endl;
    {
        Address addr("123 Main St", "New York", "NY", "10001");
        Person person("John Doe", 30, addr);
        person.displayInfo();
    }

    // 4. Computer composition
    cout << "\n\n4. Computer Composition - CPU, RAM, HDD" << endl;
    cout << "----------------------------------------" << endl;
    {
        Computer pc("Dell XPS", "Intel i7", 3.5, 16, 1, "SSD");
        pc.boot();
        pc.saveFile();
    }

    // 5. Library with books
    cout << "\n\n5. Library with Books Collection" << endl;
    cout << "----------------------------------" << endl;
    {
        Library library("City Public Library");

        Book book1("The C++ Programming Language", "Bjarne Stroustrup", "978-0321563842");
        Book book2("Effective Modern C++", "Scott Meyers", "978-1491903995");
        Book book3("Design Patterns", "Gang of Four", "978-0201633610");

        library.addBook(book1);
        library.addBook(book2);
        library.addBook(book3);

        library.displayCatalog();
    }

    // 6. Nested composition - Smartphone
    cout << "\n\n6. Nested Composition - Smartphone" << endl;
    cout << "-----------------------------------" << endl;
    {
        Smartphone phone("iPhone", "A15 Bionic", 3.2, 6, 4000, 6.1, 12);
        phone.makeCall();
        phone.takePhoto();
        phone.playVideo();
        cout << "\nPhone going out of scope:" << endl;
    }

    // 7. Multiple objects of same type
    cout << "\n\n7. Multiple Instances" << endl;
    cout << "----------------------" << endl;
    {
        Car car1("Honda", "Civic", 180, "Inline-4", "Manual", 6, 16);
        Car car2("BMW", "M3", 425, "Inline-6", "Automatic", 8, 19);

        cout << "\nBoth cars created successfully" << endl;
        cout << "Destroying cars:" << endl;
    }

    cout << "\n\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Composition - 'has-a' relationship" << endl;
    cout << "2. Strong ownership - composed objects' lifetime tied to container" << endl;
    cout << "3. Member initialization list - proper construction order" << endl;
    cout << "4. Automatic destruction - composed objects cleaned up automatically" << endl;
    cout << "5. Encapsulation - hide implementation details" << endl;
    cout << "6. Composition over inheritance - more flexible design" << endl;
    cout << "7. Multiple composition - objects containing multiple parts" << endl;
    cout << "8. Nested composition - composed objects containing other objects" << endl;
    cout << "9. Collections as composition - vector of objects" << endl;
    cout << "10. Constructor chaining - composed objects constructed first" << endl;

    return 0;
}
