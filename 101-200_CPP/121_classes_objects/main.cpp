/*
 * Program 121: Classes and Objects in C++
 *
 * This program demonstrates:
 * - Class definition and structure
 * - Member variables (data members)
 * - Member functions (methods)
 * - Access specifiers (public, private, protected)
 * - Object creation and usage
 * - this pointer
 */

#include <iostream>
#include <string>
#include <vector>

using namespace std;

// Simple class demonstrating basic structure
class Rectangle {
private:
    // Private data members - cannot be accessed directly from outside
    double width;
    double height;

public:
    // Public member functions - can be accessed from outside

    // Method to set dimensions
    void setDimensions(double w, double h) {
        // Using 'this' pointer to differentiate if needed
        if (w > 0 && h > 0) {
            width = w;
            height = h;
        } else {
            cout << "Invalid dimensions!" << endl;
        }
    }

    // Getter methods
    double getWidth() const {
        return width;
    }

    double getHeight() const {
        return height;
    }

    // Method to calculate area
    double calculateArea() const {
        return width * height;
    }

    // Method to calculate perimeter
    double calculatePerimeter() const {
        return 2 * (width + height);
    }

    // Method to display information
    void display() const {
        cout << "Rectangle: " << width << " x " << height << endl;
        cout << "Area: " << calculateArea() << endl;
        cout << "Perimeter: " << calculatePerimeter() << endl;
    }
};

// Class demonstrating all three access specifiers
class BankAccount {
private:
    // Private members - accessible only within the class
    string accountNumber;
    double balance;
    string pin;

protected:
    // Protected members - accessible in derived classes
    string accountType;

    void logTransaction(const string& message) {
        cout << "[LOG] " << message << endl;
    }

public:
    // Public members - accessible from anywhere
    string ownerName;

    // Public methods
    void initialize(const string& accNum, const string& owner, const string& type) {
        accountNumber = accNum;
        ownerName = owner;
        accountType = type;
        balance = 0.0;
        pin = "0000";
    }

    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            logTransaction("Deposited: $" + to_string(amount));
            cout << "Deposit successful. New balance: $" << balance << endl;
        } else {
            cout << "Invalid deposit amount!" << endl;
        }
    }

    bool withdraw(double amount, const string& enteredPin) {
        if (enteredPin != pin) {
            cout << "Incorrect PIN!" << endl;
            return false;
        }

        if (amount > 0 && amount <= balance) {
            balance -= amount;
            logTransaction("Withdrawn: $" + to_string(amount));
            cout << "Withdrawal successful. New balance: $" << balance << endl;
            return true;
        } else {
            cout << "Insufficient funds or invalid amount!" << endl;
            return false;
        }
    }

    double getBalance(const string& enteredPin) const {
        if (enteredPin == pin) {
            return balance;
        } else {
            cout << "Incorrect PIN!" << endl;
            return -1;
        }
    }

    void changePin(const string& oldPin, const string& newPin) {
        if (oldPin == pin) {
            pin = newPin;
            cout << "PIN changed successfully!" << endl;
        } else {
            cout << "Incorrect old PIN!" << endl;
        }
    }

    void displayInfo() const {
        cout << "\n=== Account Information ===" << endl;
        cout << "Owner: " << ownerName << endl;
        cout << "Account Type: " << accountType << endl;
        cout << "Account Number: " << accountNumber << endl;
        // Cannot directly display balance without PIN
    }
};

// Class demonstrating const member functions
class Counter {
private:
    int count;

public:
    Counter() : count(0) {}

    // Non-const member function - can modify the object
    void increment() {
        count++;
    }

    void decrement() {
        count--;
    }

    void reset() {
        count = 0;
    }

    // Const member function - cannot modify the object
    int getValue() const {
        return count;
    }

    void display() const {
        cout << "Counter value: " << count << endl;
    }
};

// Class demonstrating static members
class Student {
private:
    string name;
    int rollNumber;
    static int totalStudents;  // Static member - shared by all objects

public:
    Student(const string& n, int roll) : name(n), rollNumber(roll) {
        totalStudents++;
    }

    void display() const {
        cout << "Student: " << name << ", Roll: " << rollNumber << endl;
    }

    // Static member function - can access only static members
    static int getTotalStudents() {
        return totalStudents;
    }
};

// Initialize static member
int Student::totalStudents = 0;

// Class with inline member functions
class Point {
public:
    double x, y;

    // Inline functions defined inside class
    void setCoordinates(double x_val, double y_val) {
        x = x_val;
        y = y_val;
    }

    void display() const {
        cout << "Point(" << x << ", " << y << ")" << endl;
    }

    double distanceFromOrigin() const {
        return sqrt(x * x + y * y);
    }
};

// Demonstration of this pointer
class ChainableCalculator {
private:
    double value;

public:
    ChainableCalculator() : value(0) {}

    // Methods returning *this for method chaining
    ChainableCalculator& add(double num) {
        value += num;
        return *this;
    }

    ChainableCalculator& subtract(double num) {
        value -= num;
        return *this;
    }

    ChainableCalculator& multiply(double num) {
        value *= num;
        return *this;
    }

    ChainableCalculator& divide(double num) {
        if (num != 0) {
            value /= num;
        }
        return *this;
    }

    double getResult() const {
        return value;
    }
};

int main() {
    cout << "=== Program 121: Classes and Objects ===" << endl;
    cout << "=========================================\n" << endl;

    // 1. Basic class usage
    cout << "1. Basic Class - Rectangle" << endl;
    cout << "-----------------------------" << endl;
    Rectangle rect1;
    rect1.setDimensions(5.0, 3.0);
    rect1.display();

    Rectangle rect2;
    rect2.setDimensions(10.0, 7.5);
    cout << "\nSecond rectangle area: " << rect2.calculateArea() << endl;

    // 2. Access specifiers demonstration
    cout << "\n\n2. Access Specifiers - Bank Account" << endl;
    cout << "-------------------------------------" << endl;
    BankAccount account;
    account.initialize("ACC123456", "John Doe", "Savings");

    // Can access public members
    account.ownerName = "John Michael Doe";  // Public member
    account.displayInfo();

    // Public methods
    account.deposit(1000.0);
    account.deposit(500.0);
    account.withdraw(300.0, "0000");

    double balance = account.getBalance("0000");
    cout << "Current balance: $" << balance << endl;

    account.changePin("0000", "1234");
    account.withdraw(100.0, "1234");

    // Cannot access private members directly
    // account.balance = 10000;  // Error: balance is private
    // account.pin = "9999";     // Error: pin is private

    // 3. Const member functions
    cout << "\n\n3. Const Member Functions - Counter" << endl;
    cout << "-------------------------------------" << endl;
    Counter counter;
    counter.increment();
    counter.increment();
    counter.increment();
    counter.display();

    counter.decrement();
    counter.display();

    const Counter constCounter;  // const object
    // constCounter.increment();  // Error: can't call non-const function on const object
    constCounter.display();       // OK: display() is const
    cout << "Value: " << constCounter.getValue() << endl;  // OK: getValue() is const

    // 4. Static members
    cout << "\n\n4. Static Members - Student" << endl;
    cout << "----------------------------" << endl;
    cout << "Total students: " << Student::getTotalStudents() << endl;

    Student s1("Alice", 101);
    Student s2("Bob", 102);
    Student s3("Charlie", 103);

    s1.display();
    s2.display();
    s3.display();

    cout << "Total students: " << Student::getTotalStudents() << endl;

    // 5. Inline functions and public members
    cout << "\n\n5. Inline Functions - Point" << endl;
    cout << "----------------------------" << endl;
    Point p1;
    p1.setCoordinates(3.0, 4.0);
    p1.display();
    cout << "Distance from origin: " << p1.distanceFromOrigin() << endl;

    // Direct access to public members
    p1.x = 5.0;
    p1.y = 12.0;
    p1.display();
    cout << "Distance from origin: " << p1.distanceFromOrigin() << endl;

    // 6. Method chaining with this pointer
    cout << "\n\n6. Method Chaining - Chainable Calculator" << endl;
    cout << "-------------------------------------------" << endl;
    ChainableCalculator calc;

    double result = calc.add(10).subtract(3).multiply(2).divide(2).getResult();
    cout << "Result of chained operations: " << result << endl;

    // Another example
    ChainableCalculator calc2;
    calc2.add(100).divide(4).subtract(5).multiply(3);
    cout << "Result: " << calc2.getResult() << endl;

    // 7. Multiple objects
    cout << "\n\n7. Multiple Objects" << endl;
    cout << "--------------------" << endl;
    vector<Rectangle> rectangles;

    for (int i = 1; i <= 5; i++) {
        Rectangle r;
        r.setDimensions(i * 2.0, i * 1.5);
        rectangles.push_back(r);
    }

    double totalArea = 0;
    for (const auto& rect : rectangles) {
        totalArea += rect.calculateArea();
    }

    cout << "Total area of 5 rectangles: " << totalArea << endl;

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Class definition with data and function members" << endl;
    cout << "2. Access specifiers: public, private, protected" << endl;
    cout << "3. Encapsulation - hiding internal details" << endl;
    cout << "4. Const member functions" << endl;
    cout << "5. Static members shared across all objects" << endl;
    cout << "6. this pointer for method chaining" << endl;
    cout << "7. Object creation and manipulation" << endl;

    return 0;
}
