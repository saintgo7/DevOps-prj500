/*
 * Program 126: Abstraction in C++
 *
 * This program demonstrates:
 * - Abstract classes
 * - Pure virtual functions
 * - Interfaces (pure abstract classes)
 * - Abstract data types
 * - Implementation hiding
 * - Concrete implementations of abstract classes
 * - Multiple levels of abstraction
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <cmath>

using namespace std;

// ===== BASIC ABSTRACT CLASS =====

// Abstract class with pure virtual functions
class Shape {
protected:
    string name;
    string color;

public:
    Shape(string n, string c) : name(n), color(c) {}

    virtual ~Shape() {}

    // Pure virtual functions - must be implemented by derived classes
    virtual double area() const = 0;
    virtual double perimeter() const = 0;
    virtual void draw() const = 0;

    // Concrete method (has implementation)
    void displayInfo() const {
        cout << "Shape: " << name << ", Color: " << color << endl;
    }

    string getName() const { return name; }
    string getColor() const { return color; }
};

// Concrete class implementing abstract class
class Circle : public Shape {
private:
    double radius;

public:
    Circle(string c, double r) : Shape("Circle", c), radius(r) {}

    double area() const override {
        return 3.14159 * radius * radius;
    }

    double perimeter() const override {
        return 2 * 3.14159 * radius;
    }

    void draw() const override {
        cout << "Drawing " << color << " circle with radius " << radius << endl;
    }
};

class Rectangle : public Shape {
private:
    double width;
    double height;

public:
    Rectangle(string c, double w, double h)
        : Shape("Rectangle", c), width(w), height(h) {}

    double area() const override {
        return width * height;
    }

    double perimeter() const override {
        return 2 * (width + height);
    }

    void draw() const override {
        cout << "Drawing " << color << " rectangle " << width << "x" << height << endl;
    }
};

// ===== INTERFACE (PURE ABSTRACT CLASS) =====

// Interface for drawable objects
class IDrawable {
public:
    virtual ~IDrawable() {}
    virtual void draw() const = 0;
};

// Interface for printable objects
class IPrintable {
public:
    virtual ~IPrintable() {}
    virtual void print() const = 0;
};

// Interface for saveable objects
class ISaveable {
public:
    virtual ~ISaveable() {}
    virtual void save(const string& filename) const = 0;
    virtual void load(const string& filename) = 0;
};

// Class implementing multiple interfaces
class Document : public IPrintable, public ISaveable {
private:
    string title;
    string content;

public:
    Document(string t, string c) : title(t), content(c) {}

    void print() const override {
        cout << "Printing Document: " << title << endl;
        cout << "Content: " << content << endl;
    }

    void save(const string& filename) const override {
        cout << "Saving document '" << title << "' to " << filename << endl;
    }

    void load(const string& filename) override {
        cout << "Loading document from " << filename << endl;
    }
};

// ===== ABSTRACT DATA TYPE (ADT) =====

// Abstract class representing a database
class Database {
protected:
    string connectionString;
    bool isConnected;

public:
    Database(string conn) : connectionString(conn), isConnected(false) {}
    virtual ~Database() {}

    // Pure virtual functions - database operations
    virtual void connect() = 0;
    virtual void disconnect() = 0;
    virtual void executeQuery(const string& query) = 0;
    virtual vector<string> fetchResults() = 0;

    // Concrete helper method
    bool getConnectionStatus() const {
        return isConnected;
    }
};

// MySQL implementation
class MySQLDatabase : public Database {
private:
    vector<string> resultSet;

public:
    MySQLDatabase(string conn) : Database(conn) {}

    void connect() override {
        cout << "Connecting to MySQL database..." << endl;
        isConnected = true;
        cout << "Connected to MySQL at " << connectionString << endl;
    }

    void disconnect() override {
        cout << "Disconnecting from MySQL..." << endl;
        isConnected = false;
        cout << "Disconnected" << endl;
    }

    void executeQuery(const string& query) override {
        if (!isConnected) {
            cout << "Error: Not connected to database" << endl;
            return;
        }
        cout << "Executing MySQL query: " << query << endl;
        resultSet = {"Row1", "Row2", "Row3"};  // Simulated results
    }

    vector<string> fetchResults() override {
        return resultSet;
    }
};

// PostgreSQL implementation
class PostgreSQLDatabase : public Database {
private:
    vector<string> resultSet;

public:
    PostgreSQLDatabase(string conn) : Database(conn) {}

    void connect() override {
        cout << "Connecting to PostgreSQL database..." << endl;
        isConnected = true;
        cout << "Connected to PostgreSQL at " << connectionString << endl;
    }

    void disconnect() override {
        cout << "Disconnecting from PostgreSQL..." << endl;
        isConnected = false;
        cout << "Disconnected" << endl;
    }

    void executeQuery(const string& query) override {
        if (!isConnected) {
            cout << "Error: Not connected to database" << endl;
            return;
        }
        cout << "Executing PostgreSQL query: " << query << endl;
        resultSet = {"Data1", "Data2", "Data3", "Data4"};  // Simulated results
    }

    vector<string> fetchResults() override {
        return resultSet;
    }
};

// ===== MULTI-LEVEL ABSTRACTION =====

// Top-level abstract class
class Animal {
protected:
    string name;
    int age;

public:
    Animal(string n, int a) : name(n), age(a) {}
    virtual ~Animal() {}

    // Pure virtual functions
    virtual void makeSound() const = 0;
    virtual void move() const = 0;

    // Concrete method
    void displayInfo() const {
        cout << "Animal: " << name << ", Age: " << age << endl;
    }
};

// Intermediate abstract class
class Mammal : public Animal {
protected:
    string furColor;

public:
    Mammal(string n, int a, string fur)
        : Animal(n, a), furColor(fur) {}

    // Still abstract - doesn't implement all pure virtual functions
    virtual void giveBirth() const = 0;  // New pure virtual function

    void displayMammalInfo() const {
        displayInfo();
        cout << "Fur Color: " << furColor << endl;
    }
};

// Concrete class
class Dog : public Mammal {
public:
    Dog(string n, int a, string fur) : Mammal(n, a, fur) {}

    void makeSound() const override {
        cout << name << " barks: Woof! Woof!" << endl;
    }

    void move() const override {
        cout << name << " runs on four legs" << endl;
    }

    void giveBirth() const override {
        cout << name << " gives birth to puppies" << endl;
    }
};

// ===== PAYMENT PROCESSING ABSTRACTION =====

// Abstract payment processor
class PaymentProcessor {
protected:
    string accountId;
    double balance;

public:
    PaymentProcessor(string id, double bal) : accountId(id), balance(bal) {}
    virtual ~PaymentProcessor() {}

    // Pure virtual functions
    virtual bool processPayment(double amount) = 0;
    virtual bool refund(double amount) = 0;
    virtual string getPaymentMethod() const = 0;

    // Concrete methods
    double getBalance() const {
        return balance;
    }

    string getAccountId() const {
        return accountId;
    }
};

class CreditCardProcessor : public PaymentProcessor {
private:
    string cardNumber;
    string cvv;

public:
    CreditCardProcessor(string id, double bal, string card, string c)
        : PaymentProcessor(id, bal), cardNumber(card), cvv(c) {}

    bool processPayment(double amount) override {
        cout << "Processing credit card payment of $" << amount << endl;
        if (amount <= balance) {
            balance -= amount;
            cout << "Payment successful. Remaining balance: $" << balance << endl;
            return true;
        }
        cout << "Insufficient credit limit" << endl;
        return false;
    }

    bool refund(double amount) override {
        cout << "Refunding $" << amount << " to credit card" << endl;
        balance += amount;
        return true;
    }

    string getPaymentMethod() const override {
        return "Credit Card (****" + cardNumber.substr(cardNumber.length() - 4) + ")";
    }
};

class PayPalProcessor : public PaymentProcessor {
private:
    string email;

public:
    PayPalProcessor(string id, double bal, string e)
        : PaymentProcessor(id, bal), email(e) {}

    bool processPayment(double amount) override {
        cout << "Processing PayPal payment of $" << amount << endl;
        if (amount <= balance) {
            balance -= amount;
            cout << "Payment successful via PayPal. Remaining balance: $" << balance << endl;
            return true;
        }
        cout << "Insufficient PayPal balance" << endl;
        return false;
    }

    bool refund(double amount) override {
        cout << "Refunding $" << amount << " to PayPal account" << endl;
        balance += amount;
        return true;
    }

    string getPaymentMethod() const override {
        return "PayPal (" + email + ")";
    }
};

// ===== FILE SYSTEM ABSTRACTION =====

class FileSystem {
public:
    virtual ~FileSystem() {}

    // Pure virtual functions defining file operations
    virtual void createFile(const string& filename) = 0;
    virtual void deleteFile(const string& filename) = 0;
    virtual string readFile(const string& filename) = 0;
    virtual void writeFile(const string& filename, const string& content) = 0;
    virtual vector<string> listFiles() = 0;
};

class LocalFileSystem : public FileSystem {
private:
    vector<string> files;

public:
    void createFile(const string& filename) override {
        cout << "Creating local file: " << filename << endl;
        files.push_back(filename);
    }

    void deleteFile(const string& filename) override {
        cout << "Deleting local file: " << filename << endl;
        auto it = find(files.begin(), files.end(), filename);
        if (it != files.end()) {
            files.erase(it);
        }
    }

    string readFile(const string& filename) override {
        cout << "Reading local file: " << filename << endl;
        return "Content of " + filename;
    }

    void writeFile(const string& filename, const string& content) override {
        cout << "Writing to local file: " << filename << endl;
        cout << "Content: " << content << endl;
    }

    vector<string> listFiles() override {
        return files;
    }
};

class CloudFileSystem : public FileSystem {
private:
    string cloudProvider;
    vector<string> files;

public:
    CloudFileSystem(string provider) : cloudProvider(provider) {}

    void createFile(const string& filename) override {
        cout << "Creating file on " << cloudProvider << ": " << filename << endl;
        files.push_back(filename);
    }

    void deleteFile(const string& filename) override {
        cout << "Deleting file from " << cloudProvider << ": " << filename << endl;
        auto it = find(files.begin(), files.end(), filename);
        if (it != files.end()) {
            files.erase(it);
        }
    }

    string readFile(const string& filename) override {
        cout << "Reading from " << cloudProvider << ": " << filename << endl;
        return "Cloud content of " + filename;
    }

    void writeFile(const string& filename, const string& content) override {
        cout << "Writing to " << cloudProvider << ": " << filename << endl;
        cout << "Content: " << content << endl;
    }

    vector<string> listFiles() override {
        return files;
    }
};

// Helper function demonstrating abstraction
void processShapes(const vector<Shape*>& shapes) {
    cout << "\nProcessing shapes through abstraction:" << endl;
    cout << "---------------------------------------" << endl;

    double totalArea = 0;
    for (const auto& shape : shapes) {
        shape->draw();
        cout << "Area: " << shape->area() << endl;
        cout << "Perimeter: " << shape->perimeter() << endl;
        totalArea += shape->area();
        cout << endl;
    }

    cout << "Total area of all shapes: " << totalArea << endl;
}

int main() {
    cout << "=== Program 126: Abstraction in C++ ===" << endl;
    cout << "=======================================\n" << endl;

    // 1. Basic abstract class
    cout << "1. Basic Abstract Class - Shapes" << endl;
    cout << "---------------------------------" << endl;
    {
        // Shape shape("Generic", "red");  // Error: can't instantiate abstract class

        vector<Shape*> shapes;
        shapes.push_back(new Circle("red", 5.0));
        shapes.push_back(new Rectangle("blue", 4.0, 6.0));
        shapes.push_back(new Circle("green", 3.0));

        processShapes(shapes);

        for (auto shape : shapes) {
            delete shape;
        }
    }

    // 2. Interfaces (pure abstract classes)
    cout << "\n2. Interfaces - Document" << endl;
    cout << "-------------------------" << endl;
    {
        Document doc("Report", "This is a quarterly report.");

        IPrintable* printable = &doc;
        ISaveable* saveable = &doc;

        printable->print();
        saveable->save("report.pdf");
    }

    // 3. Abstract Data Type - Database
    cout << "\n3. Abstract Data Type - Database" << endl;
    cout << "---------------------------------" << endl;
    {
        vector<unique_ptr<Database>> databases;
        databases.push_back(make_unique<MySQLDatabase>("localhost:3306"));
        databases.push_back(make_unique<PostgreSQLDatabase>("localhost:5432"));

        for (auto& db : databases) {
            db->connect();
            db->executeQuery("SELECT * FROM users");

            vector<string> results = db->fetchResults();
            cout << "Results: ";
            for (const auto& result : results) {
                cout << result << " ";
            }
            cout << endl;

            db->disconnect();
            cout << endl;
        }
    }

    // 4. Multi-level abstraction
    cout << "\n4. Multi-Level Abstraction - Animals" << endl;
    cout << "-------------------------------------" << endl;
    {
        Dog dog("Buddy", 3, "Golden");
        dog.displayMammalInfo();
        dog.makeSound();
        dog.move();
        dog.giveBirth();
    }

    // 5. Payment processing abstraction
    cout << "\n5. Payment Processing Abstraction" << endl;
    cout << "----------------------------------" << endl;
    {
        vector<unique_ptr<PaymentProcessor>> processors;
        processors.push_back(make_unique<CreditCardProcessor>(
            "CC001", 5000.0, "1234567812345678", "123"));
        processors.push_back(make_unique<PayPalProcessor>(
            "PP001", 1000.0, "user@example.com"));

        for (auto& processor : processors) {
            cout << "\nPayment Method: " << processor->getPaymentMethod() << endl;
            cout << "Initial Balance: $" << processor->getBalance() << endl;

            processor->processPayment(150.0);
            processor->refund(50.0);

            cout << "Final Balance: $" << processor->getBalance() << endl;
            cout << endl;
        }
    }

    // 6. File system abstraction
    cout << "\n6. File System Abstraction" << endl;
    cout << "---------------------------" << endl;
    {
        vector<unique_ptr<FileSystem>> fileSystems;
        fileSystems.push_back(make_unique<LocalFileSystem>());
        fileSystems.push_back(make_unique<CloudFileSystem>("AWS S3"));

        for (auto& fs : fileSystems) {
            fs->createFile("document.txt");
            fs->writeFile("document.txt", "Hello, World!");
            string content = fs->readFile("document.txt");

            cout << "Read: " << content << endl;

            vector<string> files = fs->listFiles();
            cout << "Files: ";
            for (const auto& file : files) {
                cout << file << " ";
            }
            cout << "\n" << endl;
        }
    }

    // 7. Polymorphic behavior through abstraction
    cout << "\n7. Polymorphic Behavior Through Abstraction" << endl;
    cout << "--------------------------------------------" << endl;
    {
        Animal* animals[2];
        animals[0] = new Dog("Max", 4, "Brown");
        animals[1] = new Dog("Luna", 2, "White");

        for (int i = 0; i < 2; i++) {
            animals[i]->displayInfo();
            animals[i]->makeSound();
            animals[i]->move();
            cout << endl;
        }

        for (int i = 0; i < 2; i++) {
            delete animals[i];
        }
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Abstract classes - classes with pure virtual functions" << endl;
    cout << "2. Pure virtual functions - must be implemented by derived classes" << endl;
    cout << "3. Interfaces - pure abstract classes with only pure virtual functions" << endl;
    cout << "4. Multiple interface implementation" << endl;
    cout << "5. Abstract data types (ADT) - hiding implementation details" << endl;
    cout << "6. Multi-level abstraction - abstract classes inheriting from abstract classes" << endl;
    cout << "7. Implementation hiding - users work with abstractions, not implementations" << endl;
    cout << "8. Polymorphism through abstraction" << endl;
    cout << "9. Separation of interface and implementation" << endl;
    cout << "10. Benefits: flexibility, maintainability, testability" << endl;

    return 0;
}
