/*
 * Program 129: Friend Functions and Classes in C++
 *
 * This program demonstrates:
 * - Friend functions
 * - Friend classes
 * - Friend member functions
 * - Accessing private members through friend functions
 * - Operator overloading with friend functions
 * - Use cases for friend functions
 * - Friend function limitations
 */

#include <iostream>
#include <string>
#include <cmath>

using namespace std;

// ===== BASIC FRIEND FUNCTIONS =====

class Rectangle {
private:
    double width;
    double height;

public:
    Rectangle(double w, double h) : width(w), height(h) {}

    // Regular member function
    double area() const {
        return width * height;
    }

    // Friend function declaration
    friend void displayDimensions(const Rectangle& rect);
    friend double calculatePerimeter(const Rectangle& rect);

    // Friend function for comparison
    friend bool isLarger(const Rectangle& r1, const Rectangle& r2);
};

// Friend function implementation - can access private members
void displayDimensions(const Rectangle& rect) {
    cout << "Width: " << rect.width << ", Height: " << rect.height << endl;
}

double calculatePerimeter(const Rectangle& rect) {
    return 2 * (rect.width + rect.height);
}

bool isLarger(const Rectangle& r1, const Rectangle& r2) {
    return r1.area() > r2.area();
}

// ===== FRIEND FUNCTIONS FOR OPERATOR OVERLOADING =====

class Complex {
private:
    double real;
    double imag;

public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}

    // Friend function for stream output
    friend ostream& operator<<(ostream& os, const Complex& c);

    // Friend function for stream input
    friend istream& operator>>(istream& is, Complex& c);

    // Friend function for arithmetic with scalar
    friend Complex operator*(double scalar, const Complex& c);

    // Friend function for comparison
    friend bool operator==(const Complex& c1, const Complex& c2);

    // Member function version
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }
};

ostream& operator<<(ostream& os, const Complex& c) {
    os << c.real;
    if (c.imag >= 0) {
        os << " + " << c.imag << "i";
    } else {
        os << " - " << -c.imag << "i";
    }
    return os;
}

istream& operator>>(istream& is, Complex& c) {
    cout << "Enter real part: ";
    is >> c.real;
    cout << "Enter imaginary part: ";
    is >> c.imag;
    return is;
}

Complex operator*(double scalar, const Complex& c) {
    return Complex(scalar * c.real, scalar * c.imag);
}

bool operator==(const Complex& c1, const Complex& c2) {
    return c1.real == c2.real && c1.imag == c2.imag;
}

// ===== FRIEND CLASSES =====

// Forward declaration
class Student;

class GradeBook {
private:
    string courseName;

public:
    GradeBook(string name) : courseName(name) {}

    // This function can access private members of Student
    void displayStudentInfo(const Student& student);

    // Can modify private members
    void updateStudentGrade(Student& student, double newGrade);
};

class Student {
private:
    string name;
    int rollNumber;
    double grade;

    // Declare GradeBook as a friend class
    friend class GradeBook;

    // Alternatively, can friend specific functions
    // friend void GradeBook::displayStudentInfo(const Student&);

public:
    Student(string n, int roll, double g)
        : name(n), rollNumber(roll), grade(g) {}

    void display() const {
        cout << "Student: " << name << ", Roll: " << rollNumber
             << ", Grade: " << grade << endl;
    }
};

// GradeBook can access private members of Student
void GradeBook::displayStudentInfo(const Student& student) {
    cout << "Course: " << courseName << endl;
    cout << "Student Name: " << student.name << endl;
    cout << "Roll Number: " << student.rollNumber << endl;
    cout << "Grade: " << student.grade << endl;
}

void GradeBook::updateStudentGrade(Student& student, double newGrade) {
    student.grade = newGrade;
    cout << "Updated grade for " << student.name << " to " << newGrade << endl;
}

// ===== MUTUAL FRIENDS =====

class ClassB;  // Forward declaration

class ClassA {
private:
    int secretA;

public:
    ClassA(int val) : secretA(val) {}

    // Friend function that accesses both classes
    friend void compareSecrets(const ClassA& a, const ClassB& b);

    // Friend the other class
    friend class ClassB;
};

class ClassB {
private:
    int secretB;

public:
    ClassB(int val) : secretB(val) {}

    // Friend function
    friend void compareSecrets(const ClassA& a, const ClassB& b);

    // Can access ClassA's private members
    void accessClassA(const ClassA& a) {
        cout << "Accessing ClassA's secret: " << a.secretA << endl;
    }
};

void compareSecrets(const ClassA& a, const ClassB& b) {
    cout << "ClassA secret: " << a.secretA << endl;
    cout << "ClassB secret: " << b.secretB << endl;
    if (a.secretA == b.secretB) {
        cout << "Secrets are equal!" << endl;
    } else {
        cout << "Secrets are different." << endl;
    }
}

// ===== FRIEND FUNCTIONS FOR TWO-WAY OPERATIONS =====

class Distance {
private:
    double meters;

public:
    Distance(double m = 0) : meters(m) {}

    // Member function for Distance + Distance
    Distance operator+(const Distance& other) const {
        return Distance(meters + other.meters);
    }

    // Friend for Distance + double
    friend Distance operator+(const Distance& d, double m);

    // Friend for double + Distance (commutativity)
    friend Distance operator+(double m, const Distance& d);

    // Friend for output
    friend ostream& operator<<(ostream& os, const Distance& d);

    double getMeters() const { return meters; }
};

Distance operator+(const Distance& d, double m) {
    return Distance(d.meters + m);
}

Distance operator+(double m, const Distance& d) {
    return Distance(m + d.meters);
}

ostream& operator<<(ostream& os, const Distance& d) {
    os << d.meters << " meters";
    return os;
}

// ===== FRIEND FUNCTIONS VS MEMBER FUNCTIONS =====

class Matrix {
private:
    int rows, cols;
    double** data;

public:
    Matrix(int r, int c) : rows(r), cols(c) {
        data = new double*[rows];
        for (int i = 0; i < rows; i++) {
            data[i] = new double[cols];
            for (int j = 0; j < cols; j++) {
                data[i][j] = 0;
            }
        }
    }

    ~Matrix() {
        for (int i = 0; i < rows; i++) {
            delete[] data[i];
        }
        delete[] data;
    }

    void set(int r, int c, double val) {
        if (r >= 0 && r < rows && c >= 0 && c < cols) {
            data[r][c] = val;
        }
    }

    // Friend function for matrix output
    friend ostream& operator<<(ostream& os, const Matrix& m);

    // Friend function for scalar multiplication (scalar * matrix)
    friend Matrix operator*(double scalar, const Matrix& m);

    // Friend function for matrix comparison
    friend bool areDimensionsEqual(const Matrix& m1, const Matrix& m2);
};

ostream& operator<<(ostream& os, const Matrix& m) {
    for (int i = 0; i < m.rows; i++) {
        for (int j = 0; j < m.cols; j++) {
            os << m.data[i][j] << " ";
        }
        os << endl;
    }
    return os;
}

Matrix operator*(double scalar, const Matrix& m) {
    Matrix result(m.rows, m.cols);
    for (int i = 0; i < m.rows; i++) {
        for (int j = 0; j < m.cols; j++) {
            result.data[i][j] = scalar * m.data[i][j];
        }
    }
    return result;
}

bool areDimensionsEqual(const Matrix& m1, const Matrix& m2) {
    return m1.rows == m2.rows && m1.cols == m2.cols;
}

// ===== BANK ACCOUNT EXAMPLE WITH FRIEND =====

class Bank;  // Forward declaration

class Account {
private:
    string accountNumber;
    double balance;
    string pin;

    // Friend class for bank operations
    friend class Bank;

public:
    Account(string accNum, double initialBalance, string p)
        : accountNumber(accNum), balance(initialBalance), pin(p) {}

    void displayPublicInfo() const {
        cout << "Account: " << accountNumber << endl;
        // Cannot display balance or PIN publicly
    }
};

class Bank {
private:
    string bankName;

public:
    Bank(string name) : bankName(name) {}

    // Can access private members of Account
    void displayFullAccountInfo(const Account& acc) const {
        cout << "\n=== " << bankName << " Account Details ===" << endl;
        cout << "Account Number: " << acc.accountNumber << endl;
        cout << "Balance: $" << acc.balance << endl;
        cout << "PIN: " << acc.pin << " (encrypted in real systems)" << endl;
    }

    void transfer(Account& from, Account& to, double amount, const string& pin) {
        if (from.pin != pin) {
            cout << "Invalid PIN!" << endl;
            return;
        }

        if (from.balance >= amount) {
            from.balance -= amount;
            to.balance += amount;
            cout << "Transfer successful: $" << amount << endl;
            cout << "From " << from.accountNumber << " to " << to.accountNumber << endl;
        } else {
            cout << "Insufficient funds!" << endl;
        }
    }

    double getBalance(const Account& acc, const string& pin) const {
        if (acc.pin == pin) {
            return acc.balance;
        }
        throw runtime_error("Invalid PIN");
    }
};

// ===== POINT AND CIRCLE EXAMPLE =====

class Point {
private:
    double x, y;

public:
    Point(double xVal = 0, double yVal = 0) : x(xVal), y(yVal) {}

    // Friend function to calculate distance
    friend double distance(const Point& p1, const Point& p2);

    friend ostream& operator<<(ostream& os, const Point& p) {
        os << "(" << p.x << ", " << p.y << ")";
        return os;
    }

    // Friend class
    friend class Circle;
};

double distance(const Point& p1, const Point& p2) {
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;
    return sqrt(dx * dx + dy * dy);
}

class Circle {
private:
    Point center;
    double radius;

public:
    Circle(const Point& c, double r) : center(c), radius(r) {}

    bool contains(const Point& p) const {
        // Can access private members of Point
        double dist = distance(center, p);
        return dist <= radius;
    }

    void display() const {
        cout << "Circle at " << center << " with radius " << radius << endl;
    }
};

int main() {
    cout << "=== Program 129: Friend Functions and Classes ===" << endl;
    cout << "=================================================\n" << endl;

    // 1. Basic friend functions
    cout << "1. Basic Friend Functions - Rectangle" << endl;
    cout << "--------------------------------------" << endl;
    {
        Rectangle rect1(5.0, 3.0);
        Rectangle rect2(4.0, 6.0);

        cout << "Rectangle 1: ";
        displayDimensions(rect1);
        cout << "Perimeter: " << calculatePerimeter(rect1) << endl;

        cout << "\nRectangle 2: ";
        displayDimensions(rect2);
        cout << "Perimeter: " << calculatePerimeter(rect2) << endl;

        cout << "\nRectangle 1 is larger: "
             << (isLarger(rect1, rect2) ? "Yes" : "No") << endl;
    }

    // 2. Friend functions for operators
    cout << "\n2. Friend Operators - Complex Numbers" << endl;
    cout << "--------------------------------------" << endl;
    {
        Complex c1(3, 4);
        Complex c2(3, 4);
        Complex c3(1, 2);

        cout << "c1 = " << c1 << endl;
        cout << "c2 = " << c2 << endl;
        cout << "c3 = " << c3 << endl;

        cout << "c1 == c2: " << (c1 == c2 ? "true" : "false") << endl;
        cout << "c1 == c3: " << (c1 == c3 ? "true" : "false") << endl;

        Complex c4 = 2.5 * c1;  // Possible because of friend function
        cout << "2.5 * c1 = " << c4 << endl;
    }

    // 3. Friend classes
    cout << "\n3. Friend Classes - Student and GradeBook" << endl;
    cout << "------------------------------------------" << endl;
    {
        Student student("Alice Johnson", 101, 85.5);
        GradeBook gradeBook("Object-Oriented Programming");

        cout << "Public display:" << endl;
        student.display();

        cout << "\nThrough friend class:" << endl;
        gradeBook.displayStudentInfo(student);

        gradeBook.updateStudentGrade(student, 92.0);

        cout << "\nAfter update:" << endl;
        student.display();
    }

    // 4. Mutual friends
    cout << "\n4. Mutual Friends - ClassA and ClassB" << endl;
    cout << "--------------------------------------" << endl;
    {
        ClassA objA(42);
        ClassB objB(42);

        compareSecrets(objA, objB);

        ClassB objB2(100);
        objB2.accessClassA(objA);
    }

    // 5. Two-way operations with friends
    cout << "\n5. Two-Way Operations - Distance" << endl;
    cout << "---------------------------------" << endl;
    {
        Distance d1(10.0);
        Distance d2 = d1 + 5.0;  // Distance + double
        Distance d3 = 5.0 + d1;  // double + Distance (needs friend)

        cout << "d1 = " << d1 << endl;
        cout << "d1 + 5.0 = " << d2 << endl;
        cout << "5.0 + d1 = " << d3 << endl;
    }

    // 6. Matrix operations with friends
    cout << "\n6. Matrix Operations with Friends" << endl;
    cout << "----------------------------------" << endl;
    {
        Matrix m(2, 3);
        m.set(0, 0, 1);
        m.set(0, 1, 2);
        m.set(0, 2, 3);
        m.set(1, 0, 4);
        m.set(1, 1, 5);
        m.set(1, 2, 6);

        cout << "Original matrix:" << endl;
        cout << m;

        Matrix m2 = 2.0 * m;  // Scalar multiplication (needs friend)
        cout << "\n2.0 * matrix:" << endl;
        cout << m2;
    }

    // 7. Bank account with friend class
    cout << "\n7. Bank Account with Friend Class" << endl;
    cout << "----------------------------------" << endl;
    {
        Account acc1("ACC001", 1000.0, "1234");
        Account acc2("ACC002", 500.0, "5678");
        Bank bank("Global Bank");

        acc1.displayPublicInfo();

        bank.displayFullAccountInfo(acc1);

        cout << "\nPerforming transfer..." << endl;
        bank.transfer(acc1, acc2, 200.0, "1234");

        bank.displayFullAccountInfo(acc1);
        bank.displayFullAccountInfo(acc2);
    }

    // 8. Point and Circle with friends
    cout << "\n8. Point and Circle - Friend Relationships" << endl;
    cout << "-------------------------------------------" << endl;
    {
        Point p1(0, 0);
        Point p2(3, 4);

        cout << "p1 = " << p1 << endl;
        cout << "p2 = " << p2 << endl;
        cout << "Distance: " << distance(p1, p2) << endl;

        Circle circle(p1, 5.0);
        circle.display();

        cout << "p2 inside circle? " << (circle.contains(p2) ? "Yes" : "No") << endl;

        Point p3(6, 6);
        cout << "Point " << p3 << " inside circle? "
             << (circle.contains(p3) ? "Yes" : "No") << endl;
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Friend functions - access private members of a class" << endl;
    cout << "2. Friend classes - all members can access private data" << endl;
    cout << "3. Friend operators - especially for symmetric operations" << endl;
    cout << "4. Mutual friends - functions that access multiple classes" << endl;
    cout << "5. Two-way operations - enabling commutative operations" << endl;
    cout << "6. Friend for stream operators (<<, >>)" << endl;
    cout << "7. Friend functions are not member functions" << endl;
    cout << "8. Friendship is not inherited or transitive" << endl;
    cout << "9. Use cases: operator overloading, closely related classes" << endl;
    cout << "10. Friendship should be used sparingly (breaks encapsulation)" << endl;

    return 0;
}
