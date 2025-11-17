/*
 * Program 130: Static Members in C++
 *
 * This program demonstrates:
 * - Static data members
 * - Static member functions
 * - Initialization of static members
 * - Static members in inheritance
 * - Static vs non-static members
 * - Use cases for static members
 * - Static local variables in member functions
 */

#include <iostream>
#include <string>
#include <vector>

using namespace std;

// ===== BASIC STATIC MEMBERS =====

class Counter {
private:
    static int totalCount;  // Static data member - shared by all instances
    int instanceId;

public:
    Counter() {
        instanceId = ++totalCount;  // Each instance gets unique ID
        cout << "Counter created with ID: " << instanceId << endl;
    }

    ~Counter() {
        cout << "Counter " << instanceId << " destroyed" << endl;
    }

    // Static member function - can only access static members
    static int getTotalCount() {
        // Can access static members
        return totalCount;

        // Cannot access non-static members
        // return instanceId;  // Error!
    }

    // Non-static member function - can access both
    void displayInfo() const {
        cout << "Instance ID: " << instanceId
             << ", Total count: " << totalCount << endl;
    }

    int getInstanceId() const {
        return instanceId;
    }
};

// Initialize static member outside class
int Counter::totalCount = 0;

// ===== STATIC MEMBERS FOR CONFIGURATION =====

class DatabaseConnection {
private:
    static string serverAddress;
    static int maxConnections;
    static int currentConnections;

    string connectionId;
    bool isConnected;

public:
    DatabaseConnection(string id) : connectionId(id), isConnected(false) {}

    // Static configuration methods
    static void configure(const string& address, int maxConn) {
        serverAddress = address;
        maxConnections = maxConn;
        cout << "Database configured: " << serverAddress
             << ", Max connections: " << maxConnections << endl;
    }

    static string getServerAddress() {
        return serverAddress;
    }

    static int getMaxConnections() {
        return maxConnections;
    }

    static int getCurrentConnections() {
        return currentConnections;
    }

    // Instance methods
    bool connect() {
        if (currentConnections >= maxConnections) {
            cout << "Cannot connect: maximum connections reached" << endl;
            return false;
        }

        isConnected = true;
        currentConnections++;
        cout << "Connection " << connectionId << " established. "
             << "Active connections: " << currentConnections << endl;
        return true;
    }

    void disconnect() {
        if (isConnected) {
            isConnected = false;
            currentConnections--;
            cout << "Connection " << connectionId << " closed. "
                 << "Active connections: " << currentConnections << endl;
        }
    }

    ~DatabaseConnection() {
        if (isConnected) {
            disconnect();
        }
    }
};

// Initialize static members
string DatabaseConnection::serverAddress = "localhost";
int DatabaseConnection::maxConnections = 5;
int DatabaseConnection::currentConnections = 0;

// ===== STATIC MEMBERS FOR OBJECT TRACKING =====

class Student {
private:
    static int totalStudents;
    static int nextRollNumber;
    static double totalGrades;

    string name;
    int rollNumber;
    double grade;

public:
    Student(string n, double g) : name(n), grade(g) {
        rollNumber = nextRollNumber++;
        totalStudents++;
        totalGrades += grade;
        cout << "Student enrolled: " << name << " (Roll: " << rollNumber << ")" << endl;
    }

    ~Student() {
        totalStudents--;
        totalGrades -= grade;
    }

    // Static functions for statistics
    static int getTotalStudents() {
        return totalStudents;
    }

    static double getAverageGrade() {
        if (totalStudents == 0) return 0.0;
        return totalGrades / totalStudents;
    }

    static int getNextRollNumber() {
        return nextRollNumber;
    }

    // Static function to reset (useful for testing)
    static void resetCounters() {
        totalStudents = 0;
        nextRollNumber = 1;
        totalGrades = 0.0;
    }

    void display() const {
        cout << "Student: " << name << ", Roll: " << rollNumber
             << ", Grade: " << grade << endl;
    }

    double getGrade() const { return grade; }
};

// Initialize static members
int Student::totalStudents = 0;
int Student::nextRollNumber = 1;
double Student::totalGrades = 0.0;

// ===== STATIC CONST MEMBERS =====

class Circle {
private:
    static const double PI;  // Static constant
    static int circleCount;

    double radius;
    int id;

public:
    Circle(double r) : radius(r) {
        id = ++circleCount;
    }

    ~Circle() {
        circleCount--;
    }

    double area() const {
        return PI * radius * radius;
    }

    double circumference() const {
        return 2 * PI * radius;
    }

    static double getPI() {
        return PI;
    }

    static int getCircleCount() {
        return circleCount;
    }

    void display() const {
        cout << "Circle " << id << ": radius = " << radius
             << ", area = " << area() << endl;
    }
};

// Initialize static members
const double Circle::PI = 3.14159265359;
int Circle::circleCount = 0;

// ===== STATIC MEMBERS IN INHERITANCE =====

class Vehicle {
protected:
    static int totalVehicles;
    string brand;

public:
    Vehicle(string b) : brand(b) {
        totalVehicles++;
        cout << "Vehicle created: " << brand << endl;
    }

    virtual ~Vehicle() {
        totalVehicles--;
        cout << "Vehicle destroyed: " << brand << endl;
    }

    static int getTotalVehicles() {
        return totalVehicles;
    }
};

int Vehicle::totalVehicles = 0;

class Car : public Vehicle {
private:
    static int totalCars;
    int doors;

public:
    Car(string b, int d) : Vehicle(b), doors(d) {
        totalCars++;
        cout << "Car created with " << doors << " doors" << endl;
    }

    ~Car() {
        totalCars--;
        cout << "Car destroyed" << endl;
    }

    static int getTotalCars() {
        return totalCars;
    }
};

int Car::totalCars = 0;

class Motorcycle : public Vehicle {
private:
    static int totalMotorcycles;

public:
    Motorcycle(string b) : Vehicle(b) {
        totalMotorcycles++;
        cout << "Motorcycle created" << endl;
    }

    ~Motorcycle() {
        totalMotorcycles--;
        cout << "Motorcycle destroyed" << endl;
    }

    static int getTotalMotorcycles() {
        return totalMotorcycles;
    }
};

int Motorcycle::totalMotorcycles = 0;

// ===== STATIC LOCAL VARIABLES IN MEMBER FUNCTIONS =====

class IdGenerator {
public:
    static int generateId() {
        static int lastId = 0;  // Static local variable - persists between calls
        return ++lastId;
    }

    static void demonstrateStaticLocal() {
        static int callCount = 0;  // Initialized only once
        callCount++;
        cout << "Function called " << callCount << " times" << endl;
    }
};

// ===== SINGLETON PATTERN USING STATIC MEMBERS =====

class Logger {
private:
    static Logger* instance;  // Static pointer to single instance
    vector<string> logs;

    // Private constructor prevents external instantiation
    Logger() {
        cout << "Logger instance created" << endl;
    }

    // Private copy constructor
    Logger(const Logger&) = delete;

    // Private assignment operator
    Logger& operator=(const Logger&) = delete;

public:
    // Static method to get singleton instance
    static Logger* getInstance() {
        if (instance == nullptr) {
            instance = new Logger();
        }
        return instance;
    }

    void log(const string& message) {
        logs.push_back(message);
        cout << "[LOG] " << message << endl;
    }

    void displayLogs() const {
        cout << "\n=== All Logs ===" << endl;
        for (size_t i = 0; i < logs.size(); i++) {
            cout << i + 1 << ". " << logs[i] << endl;
        }
    }

    static void destroyInstance() {
        if (instance != nullptr) {
            delete instance;
            instance = nullptr;
        }
    }
};

// Initialize static instance pointer
Logger* Logger::instance = nullptr;

// ===== STATIC MEMBERS FOR FACTORY PATTERN =====

class Shape {
protected:
    string type;
    static int shapeCount;

public:
    Shape(string t) : type(t) {
        shapeCount++;
    }

    virtual ~Shape() {
        shapeCount--;
    }

    virtual double area() const = 0;

    static int getShapeCount() {
        return shapeCount;
    }

    string getType() const { return type; }
};

int Shape::shapeCount = 0;

class Rectangle : public Shape {
private:
    double width, height;

public:
    Rectangle(double w, double h) : Shape("Rectangle"), width(w), height(h) {}

    double area() const override {
        return width * height;
    }
};

class CircleShape : public Shape {
private:
    double radius;

public:
    CircleShape(double r) : Shape("Circle"), radius(r) {}

    double area() const override {
        return 3.14159 * radius * radius;
    }
};

class ShapeFactory {
private:
    static int rectanglesCreated;
    static int circlesCreated;

public:
    static Shape* createRectangle(double w, double h) {
        rectanglesCreated++;
        return new Rectangle(w, h);
    }

    static Shape* createCircle(double r) {
        circlesCreated++;
        return new CircleShape(r);
    }

    static void displayStatistics() {
        cout << "\n=== Shape Factory Statistics ===" << endl;
        cout << "Rectangles created: " << rectanglesCreated << endl;
        cout << "Circles created: " << circlesCreated << endl;
        cout << "Total shapes: " << Shape::getShapeCount() << endl;
    }
};

int ShapeFactory::rectanglesCreated = 0;
int ShapeFactory::circlesCreated = 0;

// ===== BANK ACCOUNT WITH STATIC INTEREST RATE =====

class BankAccount {
private:
    static double interestRate;  // Same for all accounts
    static int accountCount;

    string accountNumber;
    double balance;

public:
    BankAccount(string accNum, double bal)
        : accountNumber(accNum), balance(bal) {
        accountCount++;
    }

    ~BankAccount() {
        accountCount--;
    }

    // Static method to set interest rate for all accounts
    static void setInterestRate(double rate) {
        interestRate = rate;
        cout << "Interest rate set to " << rate * 100 << "%" << endl;
    }

    static double getInterestRate() {
        return interestRate;
    }

    static int getAccountCount() {
        return accountCount;
    }

    void applyInterest() {
        double interest = balance * interestRate;
        balance += interest;
        cout << "Account " << accountNumber << ": Interest $" << interest
             << " applied. New balance: $" << balance << endl;
    }

    void display() const {
        cout << "Account " << accountNumber << ": $" << balance << endl;
    }
};

// Initialize static members
double BankAccount::interestRate = 0.05;  // 5% default
int BankAccount::accountCount = 0;

int main() {
    cout << "=== Program 130: Static Members ===" << endl;
    cout << "===================================\n" << endl;

    // 1. Basic static members
    cout << "1. Basic Static Members - Counter" << endl;
    cout << "----------------------------------" << endl;
    {
        cout << "Initial count: " << Counter::getTotalCount() << endl;

        Counter c1, c2, c3;

        cout << "Total count: " << Counter::getTotalCount() << endl;

        c1.displayInfo();
        c2.displayInfo();
        c3.displayInfo();

        cout << "\nGoing out of scope..." << endl;
    }
    cout << "Count after scope: " << Counter::getTotalCount() << endl;

    // 2. Static members for configuration
    cout << "\n2. Static Configuration - Database" << endl;
    cout << "-----------------------------------" << endl;
    {
        DatabaseConnection::configure("192.168.1.100", 3);

        DatabaseConnection conn1("CONN-1");
        DatabaseConnection conn2("CONN-2");
        DatabaseConnection conn3("CONN-3");

        conn1.connect();
        conn2.connect();
        conn3.connect();

        cout << "\nTrying to create more connections than allowed..." << endl;
        DatabaseConnection conn4("CONN-4");
        conn4.connect();  // Should fail

        conn1.disconnect();

        cout << "\nNow trying again..." << endl;
        conn4.connect();  // Should succeed
    }

    // 3. Object tracking with static members
    cout << "\n3. Object Tracking - Students" << endl;
    cout << "------------------------------" << endl;
    {
        Student s1("Alice", 85.0);
        Student s2("Bob", 90.0);
        Student s3("Charlie", 78.0);

        cout << "\nStatistics:" << endl;
        cout << "Total students: " << Student::getTotalStudents() << endl;
        cout << "Average grade: " << Student::getAverageGrade() << endl;
        cout << "Next roll number: " << Student::getNextRollNumber() << endl;
    }

    // 4. Static const members
    cout << "\n4. Static Const Members - Circle" << endl;
    cout << "---------------------------------" << endl;
    {
        cout << "PI = " << Circle::getPI() << endl;

        Circle c1(5.0);
        Circle c2(3.0);
        Circle c3(7.5);

        c1.display();
        c2.display();
        c3.display();

        cout << "Total circles: " << Circle::getCircleCount() << endl;
    }

    // 5. Static members in inheritance
    cout << "\n5. Static Members in Inheritance" << endl;
    cout << "---------------------------------" << endl;
    {
        cout << "Creating vehicles..." << endl;
        Car car1("Toyota", 4);
        Car car2("Honda", 4);
        Motorcycle moto1("Harley");
        Motorcycle moto2("Yamaha");

        cout << "\nVehicle statistics:" << endl;
        cout << "Total vehicles: " << Vehicle::getTotalVehicles() << endl;
        cout << "Total cars: " << Car::getTotalCars() << endl;
        cout << "Total motorcycles: " << Motorcycle::getTotalMotorcycles() << endl;

        cout << "\nDestroying vehicles..." << endl;
    }

    // 6. Static local variables
    cout << "\n6. Static Local Variables" << endl;
    cout << "--------------------------" << endl;
    {
        cout << "Generated IDs: ";
        for (int i = 0; i < 5; i++) {
            cout << IdGenerator::generateId() << " ";
        }
        cout << endl;

        for (int i = 0; i < 3; i++) {
            IdGenerator::demonstrateStaticLocal();
        }
    }

    // 7. Singleton pattern
    cout << "\n7. Singleton Pattern - Logger" << endl;
    cout << "------------------------------" << endl;
    {
        Logger* logger1 = Logger::getInstance();
        logger1->log("Application started");
        logger1->log("User logged in");

        Logger* logger2 = Logger::getInstance();  // Same instance
        logger2->log("Data loaded");

        cout << "logger1 == logger2: " << (logger1 == logger2 ? "Yes" : "No") << endl;

        logger1->displayLogs();

        Logger::destroyInstance();
    }

    // 8. Factory pattern with static methods
    cout << "\n8. Factory Pattern with Static Methods" << endl;
    cout << "----------------------------------------" << endl;
    {
        Shape* shapes[4];
        shapes[0] = ShapeFactory::createRectangle(5, 3);
        shapes[1] = ShapeFactory::createCircle(4);
        shapes[2] = ShapeFactory::createRectangle(7, 2);
        shapes[3] = ShapeFactory::createCircle(6);

        for (int i = 0; i < 4; i++) {
            cout << shapes[i]->getType() << " area: " << shapes[i]->area() << endl;
        }

        ShapeFactory::displayStatistics();

        for (int i = 0; i < 4; i++) {
            delete shapes[i];
        }
    }

    // 9. Bank account with static interest rate
    cout << "\n9. Bank Account with Static Interest Rate" << endl;
    cout << "------------------------------------------" << endl;
    {
        BankAccount acc1("ACC001", 1000.0);
        BankAccount acc2("ACC002", 2000.0);
        BankAccount acc3("ACC003", 1500.0);

        cout << "\nCurrent interest rate: "
             << BankAccount::getInterestRate() * 100 << "%" << endl;

        acc1.applyInterest();
        acc2.applyInterest();
        acc3.applyInterest();

        cout << "\nChanging interest rate for all accounts..." << endl;
        BankAccount::setInterestRate(0.07);  // 7%

        acc1.applyInterest();
        acc2.applyInterest();
        acc3.applyInterest();

        cout << "\nTotal accounts: " << BankAccount::getAccountCount() << endl;
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Static data members - shared by all instances" << endl;
    cout << "2. Static member functions - can only access static members" << endl;
    cout << "3. Static member initialization - outside class definition" << endl;
    cout << "4. Static const members - compile-time constants" << endl;
    cout << "5. Static members in inheritance - each class has its own" << endl;
    cout << "6. Static local variables - persist between function calls" << endl;
    cout << "7. Singleton pattern - single instance using static members" << endl;
    cout << "8. Factory pattern - static factory methods" << endl;
    cout << "9. Configuration management - static settings" << endl;
    cout << "10. Object counting and tracking" << endl;

    return 0;
}
