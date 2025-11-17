/*
 * Program 131: Copy Semantics in C++
 *
 * This program demonstrates:
 * - Copy constructor
 * - Copy assignment operator
 * - Shallow copy vs deep copy
 * - Default copy behavior
 * - Preventing copies (deleted copy functions)
 * - Copy-and-swap idiom
 * - Self-assignment handling
 */

#include <iostream>
#include <string>
#include <cstring>
#include <algorithm>

using namespace std;

// ===== SHALLOW COPY PROBLEM =====

class ShallowCopyExample {
private:
    int* data;
    int size;

public:
    ShallowCopyExample(int s) : size(s) {
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = i * 10;
        }
        cout << "Constructor: allocated array at " << data << endl;
    }

    // Compiler-generated copy constructor (shallow copy)
    // ShallowCopyExample(const ShallowCopyExample& other) = default;

    ~ShallowCopyExample() {
        cout << "Destructor: deleting array at " << data << endl;
        delete[] data;
    }

    void display() const {
        cout << "Data: ";
        for (int i = 0; i < size; i++) {
            cout << data[i] << " ";
        }
        cout << endl;
    }

    void modify(int index, int value) {
        if (index >= 0 && index < size) {
            data[index] = value;
        }
    }
};

// ===== DEEP COPY IMPLEMENTATION =====

class DeepCopyExample {
private:
    int* data;
    int size;

public:
    // Constructor
    DeepCopyExample(int s) : size(s) {
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = i * 10;
        }
        cout << "DeepCopy Constructor: allocated array at " << data << endl;
    }

    // Copy constructor - performs deep copy
    DeepCopyExample(const DeepCopyExample& other) : size(other.size) {
        data = new int[size];  // Allocate new memory
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];  // Copy elements
        }
        cout << "DeepCopy Copy Constructor: copied to new array at " << data << endl;
    }

    // Copy assignment operator - performs deep copy
    DeepCopyExample& operator=(const DeepCopyExample& other) {
        cout << "DeepCopy Assignment Operator called" << endl;

        // 1. Self-assignment check
        if (this == &other) {
            cout << "Self-assignment detected, returning" << endl;
            return *this;
        }

        // 2. Free existing resource
        delete[] data;

        // 3. Copy new data
        size = other.size;
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];
        }

        cout << "Assignment: copied to new array at " << data << endl;
        return *this;
    }

    ~DeepCopyExample() {
        cout << "DeepCopy Destructor: deleting array at " << data << endl;
        delete[] data;
    }

    void display() const {
        cout << "Data at " << data << ": ";
        for (int i = 0; i < size; i++) {
            cout << data[i] << " ";
        }
        cout << endl;
    }

    void modify(int index, int value) {
        if (index >= 0 && index < size) {
            data[index] = value;
        }
    }
};

// ===== COPY-AND-SWAP IDIOM =====

class CopyAndSwap {
private:
    int* data;
    int size;

public:
    CopyAndSwap(int s) : size(s) {
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = i;
        }
        cout << "CopyAndSwap Constructor" << endl;
    }

    // Copy constructor
    CopyAndSwap(const CopyAndSwap& other) : size(other.size) {
        data = new int[size];
        copy(other.data, other.data + size, data);
        cout << "CopyAndSwap Copy Constructor" << endl;
    }

    // Destructor
    ~CopyAndSwap() {
        cout << "CopyAndSwap Destructor" << endl;
        delete[] data;
    }

    // Swap function
    void swap(CopyAndSwap& other) noexcept {
        using std::swap;  // Enable ADL
        swap(data, other.data);
        swap(size, other.size);
    }

    // Copy assignment using copy-and-swap idiom
    CopyAndSwap& operator=(CopyAndSwap other) {  // Note: pass by value
        cout << "CopyAndSwap Assignment (copy-and-swap)" << endl;
        swap(other);
        return *this;
    }

    void display() const {
        cout << "Data: ";
        for (int i = 0; i < size; i++) {
            cout << data[i] << " ";
        }
        cout << endl;
    }
};

// ===== STRING CLASS WITH COPY SEMANTICS =====

class MyString {
private:
    char* str;
    size_t len;

public:
    // Constructor
    MyString(const char* s = "") {
        len = strlen(s);
        str = new char[len + 1];
        strcpy(str, s);
        cout << "String Constructor: \"" << str << "\"" << endl;
    }

    // Copy constructor
    MyString(const MyString& other) {
        len = other.len;
        str = new char[len + 1];
        strcpy(str, other.str);
        cout << "String Copy Constructor: \"" << str << "\"" << endl;
    }

    // Copy assignment operator
    MyString& operator=(const MyString& other) {
        cout << "String Assignment Operator" << endl;

        if (this != &other) {
            // Free old memory
            delete[] str;

            // Allocate and copy
            len = other.len;
            str = new char[len + 1];
            strcpy(str, other.str);
        }

        return *this;
    }

    ~MyString() {
        cout << "String Destructor: \"" << str << "\"" << endl;
        delete[] str;
    }

    const char* c_str() const {
        return str;
    }

    friend ostream& operator<<(ostream& os, const MyString& s) {
        os << s.str;
        return os;
    }
};

// ===== PREVENTING COPIES =====

class NonCopyable {
private:
    int* data;

    // Delete copy constructor and assignment operator
    NonCopyable(const NonCopyable&) = delete;
    NonCopyable& operator=(const NonCopyable&) = delete;

public:
    NonCopyable(int value) {
        data = new int(value);
        cout << "NonCopyable created with value " << *data << endl;
    }

    ~NonCopyable() {
        cout << "NonCopyable destroyed" << endl;
        delete data;
    }

    int getValue() const {
        return *data;
    }
};

// ===== MEMBER-WISE COPY =====

class Point {
public:
    int x, y;

    Point(int xVal = 0, int yVal = 0) : x(xVal), y(yVal) {
        cout << "Point Constructor: (" << x << ", " << y << ")" << endl;
    }

    Point(const Point& other) : x(other.x), y(other.y) {
        cout << "Point Copy Constructor: (" << x << ", " << y << ")" << endl;
    }

    Point& operator=(const Point& other) {
        cout << "Point Assignment Operator" << endl;
        if (this != &other) {
            x = other.x;
            y = other.y;
        }
        return *this;
    }
};

class Shape {
private:
    Point center;
    string color;
    double* scale;

public:
    Shape(int x, int y, const string& c, double s)
        : center(x, y), color(c) {
        scale = new double(s);
        cout << "Shape Constructor" << endl;
    }

    // Copy constructor - must handle all members properly
    Shape(const Shape& other) : center(other.center), color(other.color) {
        scale = new double(*other.scale);  // Deep copy pointer
        cout << "Shape Copy Constructor" << endl;
    }

    // Copy assignment
    Shape& operator=(const Shape& other) {
        cout << "Shape Assignment Operator" << endl;
        if (this != &other) {
            center = other.center;  // Uses Point's assignment
            color = other.color;
            delete scale;
            scale = new double(*other.scale);
        }
        return *this;
    }

    ~Shape() {
        cout << "Shape Destructor" << endl;
        delete scale;
    }

    void display() const {
        cout << "Shape at (" << center.x << ", " << center.y
             << "), color: " << color << ", scale: " << *scale << endl;
    }
};

// ===== COPY ELISION AND RVO =====

class Heavy {
private:
    int* bigData;
    size_t size;

public:
    Heavy(size_t s) : size(s) {
        bigData = new int[size];
        cout << "Heavy Constructor (size: " << size << ")" << endl;
    }

    Heavy(const Heavy& other) : size(other.size) {
        bigData = new int[size];
        copy(other.bigData, other.bigData + size, bigData);
        cout << "Heavy Copy Constructor (EXPENSIVE!)" << endl;
    }

    Heavy& operator=(const Heavy& other) {
        cout << "Heavy Assignment Operator" << endl;
        if (this != &other) {
            delete[] bigData;
            size = other.size;
            bigData = new int[size];
            copy(other.bigData, other.bigData + size, bigData);
        }
        return *this;
    }

    ~Heavy() {
        cout << "Heavy Destructor" << endl;
        delete[] bigData;
    }
};

Heavy createHeavy() {
    cout << "Creating Heavy object in function" << endl;
    Heavy h(1000);
    return h;  // RVO (Return Value Optimization) may eliminate copy
}

// ===== VECTOR-LIKE CONTAINER WITH COPY =====

template<typename T>
class SimpleVector {
private:
    T* data;
    size_t capacity;
    size_t count;

public:
    SimpleVector() : data(nullptr), capacity(0), count(0) {
        cout << "SimpleVector Default Constructor" << endl;
    }

    explicit SimpleVector(size_t cap) : capacity(cap), count(0) {
        data = new T[capacity];
        cout << "SimpleVector Constructor (capacity: " << capacity << ")" << endl;
    }

    // Copy constructor
    SimpleVector(const SimpleVector& other)
        : capacity(other.capacity), count(other.count) {
        data = new T[capacity];
        for (size_t i = 0; i < count; i++) {
            data[i] = other.data[i];
        }
        cout << "SimpleVector Copy Constructor" << endl;
    }

    // Copy assignment
    SimpleVector& operator=(const SimpleVector& other) {
        cout << "SimpleVector Assignment Operator" << endl;
        if (this != &other) {
            delete[] data;
            capacity = other.capacity;
            count = other.count;
            data = new T[capacity];
            for (size_t i = 0; i < count; i++) {
                data[i] = other.data[i];
            }
        }
        return *this;
    }

    ~SimpleVector() {
        cout << "SimpleVector Destructor" << endl;
        delete[] data;
    }

    void push_back(const T& value) {
        if (count < capacity) {
            data[count++] = value;
        }
    }

    void display() const {
        cout << "Vector [";
        for (size_t i = 0; i < count; i++) {
            cout << data[i];
            if (i < count - 1) cout << ", ";
        }
        cout << "]" << endl;
    }
};

int main() {
    cout << "=== Program 131: Copy Semantics ===" << endl;
    cout << "===================================\n" << endl;

    // 1. Shallow copy problem (commented out to avoid double-free)
    cout << "1. Shallow Copy Problem (Demonstration)" << endl;
    cout << "----------------------------------------" << endl;
    cout << "NOTE: Shallow copy causes double-free error!" << endl;
    cout << "When two objects share the same pointer, both destructors" << endl;
    cout << "try to delete the same memory, causing a crash." << endl;
    cout << "This is why deep copy is essential for classes with pointers.\n" << endl;

    // 2. Deep copy implementation
    cout << "2. Deep Copy Implementation" << endl;
    cout << "----------------------------" << endl;
    {
        DeepCopyExample obj1(5);
        obj1.display();

        cout << "\nCopy constructor:" << endl;
        DeepCopyExample obj2 = obj1;  // Copy constructor
        obj2.display();

        cout << "\nModifying obj2:" << endl;
        obj2.modify(2, 999);
        cout << "obj1: ";
        obj1.display();
        cout << "obj2: ";
        obj2.display();

        cout << "\nCopy assignment:" << endl;
        DeepCopyExample obj3(3);
        obj3 = obj1;  // Copy assignment
        obj3.display();

        cout << "\nSelf-assignment test:" << endl;
        obj3 = obj3;  // Should handle self-assignment

        cout << "\nDestruction order:" << endl;
    }

    // 3. Copy-and-swap idiom
    cout << "\n3. Copy-and-Swap Idiom" << endl;
    cout << "-----------------------" << endl;
    {
        CopyAndSwap obj1(5);
        obj1.display();

        CopyAndSwap obj2(3);
        obj2.display();

        cout << "\nAssignment using copy-and-swap:" << endl;
        obj2 = obj1;
        obj2.display();
    }

    // 4. String class with copy semantics
    cout << "\n4. String Class with Copy Semantics" << endl;
    cout << "------------------------------------" << endl;
    {
        MyString s1("Hello");
        cout << "s1 = " << s1 << endl;

        MyString s2 = s1;  // Copy constructor
        cout << "s2 = " << s2 << endl;

        MyString s3("World");
        cout << "s3 = " << s3 << endl;

        s3 = s1;  // Copy assignment
        cout << "After s3 = s1, s3 = " << s3 << endl;
    }

    // 5. Preventing copies
    cout << "\n5. Preventing Copies (Deleted Functions)" << endl;
    cout << "-----------------------------------------" << endl;
    {
        NonCopyable obj1(42);
        cout << "obj1 value: " << obj1.getValue() << endl;

        // NonCopyable obj2 = obj1;  // Error: copy constructor deleted
        // NonCopyable obj3(10);
        // obj3 = obj1;               // Error: assignment operator deleted

        cout << "Copies successfully prevented by compiler" << endl;
    }

    // 6. Member-wise copy with composition
    cout << "\n6. Member-Wise Copy with Composition" << endl;
    cout << "-------------------------------------" << endl;
    {
        Shape shape1(10, 20, "red", 1.5);
        shape1.display();

        cout << "\nCopying shape:" << endl;
        Shape shape2 = shape1;
        shape2.display();

        cout << "\nAssigning shape:" << endl;
        Shape shape3(0, 0, "blue", 1.0);
        shape3 = shape1;
        shape3.display();
    }

    // 7. Copy elision and RVO
    cout << "\n7. Copy Elision and RVO" << endl;
    cout << "------------------------" << endl;
    {
        cout << "Returning Heavy object (may use RVO):" << endl;
        Heavy h = createHeavy();
        cout << "Object received" << endl;
    }

    // 8. Container with copy semantics
    cout << "\n8. Container with Copy Semantics" << endl;
    cout << "---------------------------------" << endl;
    {
        SimpleVector<int> vec1(5);
        vec1.push_back(10);
        vec1.push_back(20);
        vec1.push_back(30);

        cout << "vec1: ";
        vec1.display();

        cout << "\nCopy constructor:" << endl;
        SimpleVector<int> vec2 = vec1;
        cout << "vec2: ";
        vec2.display();

        cout << "\nCopy assignment:" << endl;
        SimpleVector<int> vec3(3);
        vec3 = vec1;
        cout << "vec3: ";
        vec3.display();
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Copy constructor - creates new object from existing one" << endl;
    cout << "2. Copy assignment operator - assigns existing object to another" << endl;
    cout << "3. Shallow copy - copies pointers (dangerous!)" << endl;
    cout << "4. Deep copy - allocates new memory and copies data" << endl;
    cout << "5. Self-assignment check - prevents issues with a = a" << endl;
    cout << "6. Copy-and-swap idiom - exception-safe assignment" << endl;
    cout << "7. Preventing copies - deleted copy functions" << endl;
    cout << "8. Member-wise copy - copying all data members" << endl;
    cout << "9. Copy elision/RVO - compiler optimization" << endl;
    cout << "10. Rule of Three - destructor, copy constructor, copy assignment" << endl;

    return 0;
}
