/*
 * Program 128: Operator Overloading in C++
 *
 * This program demonstrates:
 * - Arithmetic operator overloading (+, -, *, /)
 * - Comparison operator overloading (==, !=, <, >, <=, >=)
 * - Stream operator overloading (<<, >>)
 * - Assignment operator (=)
 * - Increment/decrement operators (++, --)
 * - Subscript operator ([])
 * - Function call operator (())
 * - Member access operator (->)
 * - Type conversion operators
 */

#include <iostream>
#include <string>
#include <cmath>
#include <stdexcept>

using namespace std;

// ===== BASIC ARITHMETIC OPERATORS =====

class Complex {
private:
    double real;
    double imag;

public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}

    // Getters
    double getReal() const { return real; }
    double getImag() const { return imag; }

    // Arithmetic operators
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }

    Complex operator-(const Complex& other) const {
        return Complex(real - other.real, imag - other.imag);
    }

    Complex operator*(const Complex& other) const {
        return Complex(
            real * other.real - imag * other.imag,
            real * other.imag + imag * other.real
        );
    }

    Complex operator/(const Complex& other) const {
        double denominator = other.real * other.real + other.imag * other.imag;
        if (denominator == 0) {
            throw runtime_error("Division by zero");
        }
        return Complex(
            (real * other.real + imag * other.imag) / denominator,
            (imag * other.real - real * other.imag) / denominator
        );
    }

    // Unary minus
    Complex operator-() const {
        return Complex(-real, -imag);
    }

    // Comparison operators
    bool operator==(const Complex& other) const {
        return real == other.real && imag == other.imag;
    }

    bool operator!=(const Complex& other) const {
        return !(*this == other);
    }

    // Compound assignment operators
    Complex& operator+=(const Complex& other) {
        real += other.real;
        imag += other.imag;
        return *this;
    }

    Complex& operator-=(const Complex& other) {
        real -= other.real;
        imag -= other.imag;
        return *this;
    }

    // Stream operators (friend functions)
    friend ostream& operator<<(ostream& os, const Complex& c);
    friend istream& operator>>(istream& is, Complex& c);

    void display() const {
        cout << real << " + " << imag << "i" << endl;
    }
};

// Stream output operator
ostream& operator<<(ostream& os, const Complex& c) {
    os << c.real;
    if (c.imag >= 0) {
        os << " + " << c.imag << "i";
    } else {
        os << " - " << -c.imag << "i";
    }
    return os;
}

// Stream input operator
istream& operator>>(istream& is, Complex& c) {
    cout << "Enter real part: ";
    is >> c.real;
    cout << "Enter imaginary part: ";
    is >> c.imag;
    return is;
}

// ===== COMPARISON OPERATORS =====

class Fraction {
private:
    int numerator;
    int denominator;

    int gcd(int a, int b) const {
        return b == 0 ? a : gcd(b, a % b);
    }

    void simplify() {
        int g = gcd(abs(numerator), abs(denominator));
        numerator /= g;
        denominator /= g;
        if (denominator < 0) {
            numerator = -numerator;
            denominator = -denominator;
        }
    }

public:
    Fraction(int num = 0, int den = 1) : numerator(num), denominator(den) {
        if (denominator == 0) {
            throw invalid_argument("Denominator cannot be zero");
        }
        simplify();
    }

    // Arithmetic operators
    Fraction operator+(const Fraction& other) const {
        return Fraction(
            numerator * other.denominator + other.numerator * denominator,
            denominator * other.denominator
        );
    }

    Fraction operator-(const Fraction& other) const {
        return Fraction(
            numerator * other.denominator - other.numerator * denominator,
            denominator * other.denominator
        );
    }

    Fraction operator*(const Fraction& other) const {
        return Fraction(
            numerator * other.numerator,
            denominator * other.denominator
        );
    }

    Fraction operator/(const Fraction& other) const {
        return Fraction(
            numerator * other.denominator,
            denominator * other.numerator
        );
    }

    // Comparison operators
    bool operator==(const Fraction& other) const {
        return numerator == other.numerator && denominator == other.denominator;
    }

    bool operator!=(const Fraction& other) const {
        return !(*this == other);
    }

    bool operator<(const Fraction& other) const {
        return numerator * other.denominator < other.numerator * denominator;
    }

    bool operator>(const Fraction& other) const {
        return other < *this;
    }

    bool operator<=(const Fraction& other) const {
        return !(other < *this);
    }

    bool operator>=(const Fraction& other) const {
        return !(*this < other);
    }

    friend ostream& operator<<(ostream& os, const Fraction& f) {
        os << f.numerator << "/" << f.denominator;
        return os;
    }
};

// ===== INCREMENT AND DECREMENT OPERATORS =====

class Counter {
private:
    int count;

public:
    Counter(int c = 0) : count(c) {}

    int getCount() const { return count; }

    // Pre-increment
    Counter& operator++() {
        ++count;
        return *this;
    }

    // Post-increment (dummy int parameter)
    Counter operator++(int) {
        Counter temp(*this);
        count++;
        return temp;
    }

    // Pre-decrement
    Counter& operator--() {
        --count;
        return *this;
    }

    // Post-decrement
    Counter operator--(int) {
        Counter temp(*this);
        count--;
        return temp;
    }

    friend ostream& operator<<(ostream& os, const Counter& c) {
        os << c.count;
        return os;
    }
};

// ===== SUBSCRIPT OPERATOR =====

class Array {
private:
    int* data;
    int size;

public:
    Array(int s) : size(s) {
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = 0;
        }
    }

    ~Array() {
        delete[] data;
    }

    // Copy constructor
    Array(const Array& other) : size(other.size) {
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];
        }
    }

    // Assignment operator
    Array& operator=(const Array& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new int[size];
            for (int i = 0; i < size; i++) {
                data[i] = other.data[i];
            }
        }
        return *this;
    }

    // Subscript operator (non-const)
    int& operator[](int index) {
        if (index < 0 || index >= size) {
            throw out_of_range("Index out of range");
        }
        return data[index];
    }

    // Subscript operator (const)
    const int& operator[](int index) const {
        if (index < 0 || index >= size) {
            throw out_of_range("Index out of range");
        }
        return data[index];
    }

    int getSize() const { return size; }

    friend ostream& operator<<(ostream& os, const Array& arr) {
        os << "[";
        for (int i = 0; i < arr.size; i++) {
            os << arr.data[i];
            if (i < arr.size - 1) os << ", ";
        }
        os << "]";
        return os;
    }
};

// ===== FUNCTION CALL OPERATOR =====

class Multiplier {
private:
    int factor;

public:
    Multiplier(int f) : factor(f) {}

    // Function call operator
    int operator()(int value) const {
        return value * factor;
    }

    // Overloaded with different parameters
    int operator()(int a, int b) const {
        return (a + b) * factor;
    }
};

class Matrix {
private:
    int rows, cols;
    int** data;

public:
    Matrix(int r, int c) : rows(r), cols(c) {
        data = new int*[rows];
        for (int i = 0; i < rows; i++) {
            data[i] = new int[cols];
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

    // Function call operator for element access
    int& operator()(int row, int col) {
        if (row < 0 || row >= rows || col < 0 || col >= cols) {
            throw out_of_range("Matrix index out of range");
        }
        return data[row][col];
    }

    void display() const {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                cout << data[i][j] << " ";
            }
            cout << endl;
        }
    }
};

// ===== TYPE CONVERSION OPERATORS =====

class Distance {
private:
    double meters;

public:
    Distance(double m = 0) : meters(m) {}

    // Conversion to double (returns meters)
    operator double() const {
        return meters;
    }

    // Conversion to int (returns whole meters)
    operator int() const {
        return static_cast<int>(meters);
    }

    friend ostream& operator<<(ostream& os, const Distance& d) {
        os << d.meters << " meters";
        return os;
    }
};

// ===== SMART POINTER SIMULATION =====

template<typename T>
class SmartPtr {
private:
    T* ptr;

public:
    explicit SmartPtr(T* p = nullptr) : ptr(p) {}

    ~SmartPtr() {
        delete ptr;
    }

    // Dereference operator
    T& operator*() const {
        return *ptr;
    }

    // Member access operator
    T* operator->() const {
        return ptr;
    }

    // Bool conversion
    operator bool() const {
        return ptr != nullptr;
    }
};

class Person {
public:
    string name;
    int age;

    Person(string n, int a) : name(n), age(a) {}

    void display() const {
        cout << "Person: " << name << ", Age: " << age << endl;
    }
};

// ===== STRING CLASS WITH OPERATORS =====

class MyString {
private:
    char* str;
    int len;

public:
    MyString(const char* s = "") {
        len = strlen(s);
        str = new char[len + 1];
        strcpy(str, s);
    }

    ~MyString() {
        delete[] str;
    }

    // Copy constructor
    MyString(const MyString& other) {
        len = other.len;
        str = new char[len + 1];
        strcpy(str, other.str);
    }

    // Assignment operator
    MyString& operator=(const MyString& other) {
        if (this != &other) {
            delete[] str;
            len = other.len;
            str = new char[len + 1];
            strcpy(str, other.str);
        }
        return *this;
    }

    // Concatenation
    MyString operator+(const MyString& other) const {
        char* temp = new char[len + other.len + 1];
        strcpy(temp, str);
        strcat(temp, other.str);
        MyString result(temp);
        delete[] temp;
        return result;
    }

    // Equality
    bool operator==(const MyString& other) const {
        return strcmp(str, other.str) == 0;
    }

    friend ostream& operator<<(ostream& os, const MyString& s) {
        os << s.str;
        return os;
    }
};

int main() {
    cout << "=== Program 128: Operator Overloading ===" << endl;
    cout << "=========================================\n" << endl;

    // 1. Arithmetic operators - Complex numbers
    cout << "1. Arithmetic Operators - Complex Numbers" << endl;
    cout << "------------------------------------------" << endl;
    {
        Complex c1(3, 4);
        Complex c2(1, 2);

        cout << "c1 = " << c1 << endl;
        cout << "c2 = " << c2 << endl;

        Complex sum = c1 + c2;
        cout << "c1 + c2 = " << sum << endl;

        Complex diff = c1 - c2;
        cout << "c1 - c2 = " << diff << endl;

        Complex prod = c1 * c2;
        cout << "c1 * c2 = " << prod << endl;

        Complex quot = c1 / c2;
        cout << "c1 / c2 = " << quot << endl;

        Complex neg = -c1;
        cout << "-c1 = " << neg << endl;

        c1 += c2;
        cout << "c1 += c2: " << c1 << endl;
    }

    // 2. Comparison operators - Fractions
    cout << "\n2. Comparison Operators - Fractions" << endl;
    cout << "------------------------------------" << endl;
    {
        Fraction f1(1, 2);
        Fraction f2(2, 4);
        Fraction f3(3, 4);

        cout << "f1 = " << f1 << endl;
        cout << "f2 = " << f2 << endl;
        cout << "f3 = " << f3 << endl;

        cout << "f1 == f2: " << (f1 == f2 ? "true" : "false") << endl;
        cout << "f1 != f3: " << (f1 != f3 ? "true" : "false") << endl;
        cout << "f1 < f3: " << (f1 < f3 ? "true" : "false") << endl;
        cout << "f1 > f3: " << (f1 > f3 ? "true" : "false") << endl;

        Fraction sum = f1 + f3;
        cout << "f1 + f3 = " << sum << endl;

        Fraction prod = f1 * f3;
        cout << "f1 * f3 = " << prod << endl;
    }

    // 3. Increment and decrement operators
    cout << "\n3. Increment/Decrement Operators - Counter" << endl;
    cout << "-------------------------------------------" << endl;
    {
        Counter c(5);
        cout << "Initial: " << c << endl;

        cout << "Pre-increment: " << ++c << endl;
        cout << "After pre-increment: " << c << endl;

        cout << "Post-increment: " << c++ << endl;
        cout << "After post-increment: " << c << endl;

        cout << "Pre-decrement: " << --c << endl;
        cout << "Post-decrement: " << c-- << endl;
        cout << "Final: " << c << endl;
    }

    // 4. Subscript operator
    cout << "\n4. Subscript Operator - Array" << endl;
    cout << "------------------------------" << endl;
    {
        Array arr(5);

        for (int i = 0; i < arr.getSize(); i++) {
            arr[i] = i * 10;
        }

        cout << "Array: " << arr << endl;

        cout << "arr[2] = " << arr[2] << endl;

        arr[3] = 100;
        cout << "After arr[3] = 100: " << arr << endl;
    }

    // 5. Function call operator
    cout << "\n5. Function Call Operator" << endl;
    cout << "--------------------------" << endl;
    {
        Multiplier times3(3);

        cout << "times3(5) = " << times3(5) << endl;
        cout << "times3(2, 4) = " << times3(2, 4) << endl;

        Matrix mat(3, 3);
        mat(0, 0) = 1;
        mat(0, 1) = 2;
        mat(0, 2) = 3;
        mat(1, 0) = 4;
        mat(1, 1) = 5;
        mat(1, 2) = 6;
        mat(2, 0) = 7;
        mat(2, 1) = 8;
        mat(2, 2) = 9;

        cout << "Matrix:" << endl;
        mat.display();
    }

    // 6. Type conversion operators
    cout << "\n6. Type Conversion Operators - Distance" << endl;
    cout << "----------------------------------------" << endl;
    {
        Distance d(12.5);
        cout << "Distance: " << d << endl;

        double meters = d;  // Implicit conversion to double
        cout << "As double: " << meters << endl;

        int wholeMters = d;  // Implicit conversion to int
        cout << "As int: " << wholeMters << endl;
    }

    // 7. Member access operators
    cout << "\n7. Member Access Operators - Smart Pointer" << endl;
    cout << "-------------------------------------------" << endl;
    {
        SmartPtr<Person> ptr(new Person("Alice", 30));

        if (ptr) {
            cout << "Pointer is valid" << endl;
            ptr->display();  // operator->
            (*ptr).display(); // operator*
        }
    }

    // 8. String operations
    cout << "\n8. String Operations" << endl;
    cout << "---------------------" << endl;
    {
        MyString s1("Hello");
        MyString s2(" World");

        cout << "s1 = " << s1 << endl;
        cout << "s2 = " << s2 << endl;

        MyString s3 = s1 + s2;
        cout << "s1 + s2 = " << s3 << endl;

        MyString s4 = s1;
        cout << "s4 = s1: " << s4 << endl;
        cout << "s1 == s4: " << (s1 == s4 ? "true" : "false") << endl;
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Arithmetic operators (+, -, *, /, unary -)" << endl;
    cout << "2. Comparison operators (==, !=, <, >, <=, >=)" << endl;
    cout << "3. Compound assignment operators (+=, -=)" << endl;
    cout << "4. Increment/decrement (++, --) - prefix and postfix" << endl;
    cout << "5. Stream operators (<<, >>)" << endl;
    cout << "6. Subscript operator ([])" << endl;
    cout << "7. Function call operator (())" << endl;
    cout << "8. Member access operators (*, ->)" << endl;
    cout << "9. Type conversion operators" << endl;
    cout << "10. Assignment operator (=)" << endl;
    cout << "11. Friend functions for operator overloading" << endl;

    return 0;
}
