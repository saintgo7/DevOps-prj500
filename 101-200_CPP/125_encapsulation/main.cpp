/*
 * Program 125: Encapsulation in C++
 *
 * This program demonstrates:
 * - Data hiding
 * - Getters and setters
 * - Access control (private, protected, public)
 * - Information hiding
 * - Validation in setters
 * - Read-only and write-only properties
 * - Encapsulation benefits
 */

#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>

using namespace std;

// ===== BASIC ENCAPSULATION =====

class BankAccount {
private:
    // Private data members - hidden from outside access
    string accountNumber;
    string accountHolder;
    double balance;
    string pin;
    vector<string> transactionHistory;

    // Private helper methods
    void logTransaction(const string& transaction) {
        transactionHistory.push_back(transaction);
    }

    bool validatePin(const string& enteredPin) const {
        return enteredPin == pin;
    }

public:
    // Constructor
    BankAccount(string accNum, string holder, string initialPin)
        : accountNumber(accNum), accountHolder(holder),
          balance(0.0), pin(initialPin) {
        logTransaction("Account created");
    }

    // Getters (read-only access)
    string getAccountNumber() const {
        return accountNumber;
    }

    string getAccountHolder() const {
        return accountHolder;
    }

    // Controlled access to balance - requires PIN
    double getBalance(const string& enteredPin) const {
        if (validatePin(enteredPin)) {
            return balance;
        } else {
            throw runtime_error("Invalid PIN");
        }
    }

    // Setter with validation
    void deposit(double amount) {
        if (amount <= 0) {
            throw invalid_argument("Deposit amount must be positive");
        }

        balance += amount;
        logTransaction("Deposited: $" + to_string(amount));
        cout << "Deposit successful. New balance: $" << balance << endl;
    }

    // Controlled withdrawal - requires PIN and validation
    bool withdraw(double amount, const string& enteredPin) {
        if (!validatePin(enteredPin)) {
            cout << "Invalid PIN" << endl;
            return false;
        }

        if (amount <= 0) {
            cout << "Invalid amount" << endl;
            return false;
        }

        if (amount > balance) {
            cout << "Insufficient funds" << endl;
            return false;
        }

        balance -= amount;
        logTransaction("Withdrew: $" + to_string(amount));
        cout << "Withdrawal successful. New balance: $" << balance << endl;
        return true;
    }

    // Controlled PIN change
    void changePin(const string& oldPin, const string& newPin) {
        if (!validatePin(oldPin)) {
            throw runtime_error("Invalid old PIN");
        }

        if (newPin.length() < 4) {
            throw invalid_argument("PIN must be at least 4 digits");
        }

        pin = newPin;
        logTransaction("PIN changed");
        cout << "PIN changed successfully" << endl;
    }

    // Controlled access to transaction history
    void printTransactionHistory(const string& enteredPin) const {
        if (!validatePin(enteredPin)) {
            cout << "Invalid PIN" << endl;
            return;
        }

        cout << "\nTransaction History for " << accountHolder << ":" << endl;
        cout << "----------------------------------------" << endl;
        for (size_t i = 0; i < transactionHistory.size(); i++) {
            cout << i + 1 << ". " << transactionHistory[i] << endl;
        }
    }
};

// ===== ENCAPSULATION WITH VALIDATION =====

class Person {
private:
    string name;
    int age;
    string email;
    string phoneNumber;

    // Private validation methods
    bool isValidEmail(const string& e) const {
        return e.find('@') != string::npos && e.find('.') != string::npos;
    }

    bool isValidPhone(const string& phone) const {
        return phone.length() >= 10;
    }

public:
    Person(string n, int a) : name(n), age(a) {
        if (age < 0 || age > 150) {
            throw invalid_argument("Invalid age");
        }
    }

    // Getters
    string getName() const { return name; }
    int getAge() const { return age; }
    string getEmail() const { return email; }
    string getPhoneNumber() const { return phoneNumber; }

    // Setters with validation
    void setName(const string& n) {
        if (n.empty()) {
            throw invalid_argument("Name cannot be empty");
        }
        name = n;
    }

    void setAge(int a) {
        if (a < 0 || a > 150) {
            throw invalid_argument("Age must be between 0 and 150");
        }
        age = a;
    }

    void setEmail(const string& e) {
        if (!isValidEmail(e)) {
            throw invalid_argument("Invalid email format");
        }
        email = e;
    }

    void setPhoneNumber(const string& phone) {
        if (!isValidPhone(phone)) {
            throw invalid_argument("Invalid phone number");
        }
        phoneNumber = phone;
    }

    void displayInfo() const {
        cout << "Name: " << name << ", Age: " << age << endl;
        if (!email.empty()) cout << "Email: " << email << endl;
        if (!phoneNumber.empty()) cout << "Phone: " << phoneNumber << endl;
    }
};

// ===== READ-ONLY PROPERTIES =====

class ImmutablePoint {
private:
    const double x;
    const double y;

public:
    ImmutablePoint(double xVal, double yVal) : x(xVal), y(yVal) {}

    // Getters only - no setters (read-only)
    double getX() const { return x; }
    double getY() const { return y; }

    void display() const {
        cout << "Point(" << x << ", " << y << ")" << endl;
    }
};

// ===== WRITE-ONLY PROPERTIES (RARE) =====

class Logger {
private:
    vector<string> logs;
    string logLevel;

public:
    Logger() : logLevel("INFO") {}

    // Write-only - can add logs but can't read them directly
    void addLog(const string& message) {
        logs.push_back("[" + logLevel + "] " + message);
    }

    void setLogLevel(const string& level) {
        logLevel = level;
    }

    // Controlled read access
    void printLogs(const string& password) const {
        if (password == "admin123") {
            cout << "\n=== Logs ===" << endl;
            for (const auto& log : logs) {
                cout << log << endl;
            }
        } else {
            cout << "Access denied" << endl;
        }
    }

    int getLogCount() const {
        return logs.size();
    }
};

// ===== ENCAPSULATION WITH COMPUTED PROPERTIES =====

class Rectangle {
private:
    double width;
    double height;

public:
    Rectangle(double w, double h) : width(w), height(h) {
        if (w <= 0 || h <= 0) {
            throw invalid_argument("Dimensions must be positive");
        }
    }

    // Getters
    double getWidth() const { return width; }
    double getHeight() const { return height; }

    // Setters with validation
    void setWidth(double w) {
        if (w <= 0) {
            throw invalid_argument("Width must be positive");
        }
        width = w;
    }

    void setHeight(double h) {
        if (h <= 0) {
            throw invalid_argument("Height must be positive");
        }
        height = h;
    }

    // Computed properties (no stored value)
    double getArea() const {
        return width * height;
    }

    double getPerimeter() const {
        return 2 * (width + height);
    }

    bool isSquare() const {
        return width == height;
    }

    void display() const {
        cout << "Rectangle: " << width << " x " << height
             << ", Area: " << getArea()
             << ", Perimeter: " << getPerimeter() << endl;
    }
};

// ===== ENCAPSULATION IN CLASS HIERARCHY =====

class Vehicle {
protected:
    // Protected - accessible in derived classes but not outside
    string brand;
    int year;
    double mileage;

private:
    // Private - not accessible even in derived classes
    string engineNumber;

public:
    Vehicle(string b, int y, string engine)
        : brand(b), year(y), mileage(0.0), engineNumber(engine) {}

    // Public interface
    string getBrand() const { return brand; }
    int getYear() const { return year; }
    double getMileage() const { return mileage; }

    void addMileage(double miles) {
        if (miles < 0) {
            throw invalid_argument("Miles must be positive");
        }
        mileage += miles;
    }

    // Engine number is highly protected
    string getEngineNumber(const string& ownerCode) const {
        if (ownerCode == "OWNER123") {
            return engineNumber;
        }
        throw runtime_error("Unauthorized access to engine number");
    }
};

class Car : public Vehicle {
private:
    int numDoors;
    bool hasAC;

public:
    Car(string b, int y, string engine, int doors, bool ac)
        : Vehicle(b, y, engine), numDoors(doors), hasAC(ac) {}

    // Getters
    int getNumDoors() const { return numDoors; }
    bool hasAirConditioning() const { return hasAC; }

    // Setter
    void setAirConditioning(bool ac) {
        hasAC = ac;
    }

    void displayInfo() const {
        cout << "Car: " << brand << " " << year << endl;  // Can access protected
        cout << "Doors: " << numDoors << ", AC: " << (hasAC ? "Yes" : "No") << endl;
        cout << "Mileage: " << mileage << " miles" << endl;  // Can access protected
        // cout << engineNumber;  // Error: can't access private member
    }
};

// ===== ENCAPSULATION FOR DATA INTEGRITY =====

class Temperature {
private:
    double celsius;

    // Private validation
    bool isValidCelsius(double c) const {
        return c >= -273.15;  // Absolute zero
    }

public:
    Temperature(double c = 0.0) {
        if (!isValidCelsius(c)) {
            throw invalid_argument("Temperature below absolute zero");
        }
        celsius = c;
    }

    // Getter for celsius
    double getCelsius() const {
        return celsius;
    }

    // Setter with validation
    void setCelsius(double c) {
        if (!isValidCelsius(c)) {
            throw invalid_argument("Temperature below absolute zero");
        }
        celsius = c;
    }

    // Computed properties for different scales
    double getFahrenheit() const {
        return (celsius * 9.0 / 5.0) + 32.0;
    }

    void setFahrenheit(double f) {
        double c = (f - 32.0) * 5.0 / 9.0;
        setCelsius(c);  // Uses validation
    }

    double getKelvin() const {
        return celsius + 273.15;
    }

    void setKelvin(double k) {
        setCelsius(k - 273.15);  // Uses validation
    }

    void display() const {
        cout << "Temperature: " << celsius << "°C / "
             << getFahrenheit() << "°F / "
             << getKelvin() << "K" << endl;
    }
};

int main() {
    cout << "=== Program 125: Encapsulation in C++ ===" << endl;
    cout << "=========================================\n" << endl;

    // 1. Basic encapsulation - Bank Account
    cout << "1. Basic Encapsulation - Bank Account" << endl;
    cout << "---------------------------------------" << endl;
    try {
        BankAccount account("ACC123456", "John Doe", "1234");

        cout << "Account Number: " << account.getAccountNumber() << endl;
        cout << "Account Holder: " << account.getAccountHolder() << endl;

        account.deposit(1000.0);
        account.deposit(500.0);
        account.withdraw(200.0, "1234");

        double balance = account.getBalance("1234");
        cout << "Current balance: $" << balance << endl;

        account.changePin("1234", "5678");
        account.withdraw(100.0, "5678");

        account.printTransactionHistory("5678");

        // Can't access private members
        // account.balance = 1000000;  // Error: private member
        // account.pin = "0000";       // Error: private member

    } catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
    }

    // 2. Validation in setters
    cout << "\n2. Validation in Setters - Person" << endl;
    cout << "-----------------------------------" << endl;
    try {
        Person person("Alice", 25);
        person.displayInfo();

        person.setEmail("alice@example.com");
        person.setPhoneNumber("1234567890");
        person.displayInfo();

        cout << "\nTrying invalid email..." << endl;
        person.setEmail("invalid-email");  // Will throw exception

    } catch (const exception& e) {
        cout << "Validation error: " << e.what() << endl;
    }

    // 3. Read-only properties
    cout << "\n3. Read-Only Properties - Immutable Point" << endl;
    cout << "------------------------------------------" << endl;
    {
        ImmutablePoint point(3.5, 7.2);
        point.display();
        cout << "X: " << point.getX() << ", Y: " << point.getY() << endl;

        // Can't modify
        // point.setX(5.0);  // No setter exists!
    }

    // 4. Write-only properties
    cout << "\n4. Write-Only Properties - Logger" << endl;
    cout << "----------------------------------" << endl;
    {
        Logger logger;
        logger.addLog("Application started");
        logger.addLog("User logged in");
        logger.setLogLevel("WARNING");
        logger.addLog("Low memory warning");

        cout << "Total logs: " << logger.getLogCount() << endl;

        cout << "\nTrying to view logs without password:" << endl;
        logger.printLogs("wrong");

        cout << "\nViewing logs with correct password:" << endl;
        logger.printLogs("admin123");
    }

    // 5. Computed properties
    cout << "\n5. Computed Properties - Rectangle" << endl;
    cout << "-----------------------------------" << endl;
    try {
        Rectangle rect(5.0, 3.0);
        rect.display();

        rect.setWidth(10.0);
        rect.display();

        cout << "Is square? " << (rect.isSquare() ? "Yes" : "No") << endl;

        rect.setHeight(10.0);
        cout << "Is square? " << (rect.isSquare() ? "Yes" : "No") << endl;

        cout << "\nTrying invalid dimension..." << endl;
        rect.setWidth(-5.0);  // Will throw exception

    } catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
    }

    // 6. Encapsulation in inheritance
    cout << "\n6. Encapsulation in Inheritance - Vehicle/Car" << endl;
    cout << "-----------------------------------------------" << endl;
    try {
        Car myCar("Toyota", 2022, "ENG789456", 4, true);
        myCar.displayInfo();

        myCar.addMileage(150.5);
        myCar.displayInfo();

        cout << "\nAccessing engine number with correct code:" << endl;
        string engine = myCar.getEngineNumber("OWNER123");
        cout << "Engine: " << engine << endl;

        cout << "\nTrying to access engine number without code:" << endl;
        myCar.getEngineNumber("WRONG");

    } catch (const exception& e) {
        cout << "Security error: " << e.what() << endl;
    }

    // 7. Data integrity through encapsulation
    cout << "\n7. Data Integrity - Temperature" << endl;
    cout << "--------------------------------" << endl;
    try {
        Temperature temp(25.0);
        temp.display();

        temp.setFahrenheit(98.6);  // Body temperature
        temp.display();

        temp.setKelvin(273.15);  // Freezing point
        temp.display();

        cout << "\nTrying invalid temperature (below absolute zero)..." << endl;
        temp.setCelsius(-300.0);  // Will throw exception

    } catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
    }

    // 8. Benefits demonstration
    cout << "\n8. Encapsulation Benefits" << endl;
    cout << "--------------------------" << endl;
    {
        Rectangle r1(4.0, 3.0);
        Rectangle r2(5.0, 5.0);

        cout << "Rectangle 1: ";
        r1.display();

        cout << "Rectangle 2: ";
        r2.display();

        // All validation is handled internally
        // Can't create invalid state
        // Implementation can change without affecting users
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Data hiding - private members" << endl;
    cout << "2. Controlled access - getters and setters" << endl;
    cout << "3. Validation - ensuring data integrity" << endl;
    cout << "4. Read-only properties - getters without setters" << endl;
    cout << "5. Write-only properties - setters without getters" << endl;
    cout << "6. Computed properties - calculated on demand" << endl;
    cout << "7. Protected access - for derived classes" << endl;
    cout << "8. Information hiding - internal implementation details" << endl;
    cout << "9. Security - controlled access to sensitive data" << endl;
    cout << "10. Maintainability - implementation can change safely" << endl;

    return 0;
}
