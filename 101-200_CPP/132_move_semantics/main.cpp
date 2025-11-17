/*
 * Program 132: Move Semantics in C++ (C++11)
 *
 * This program demonstrates:
 * - Move constructor
 * - Move assignment operator
 * - Rvalue references (&&)
 * - std::move
 * - Perfect forwarding
 * - Lvalues vs rvalues
 * - Move-only types
 * - Performance benefits of move semantics
 */

#include <iostream>
#include <string>
#include <vector>
#include <utility>  // for std::move
#include <algorithm>

using namespace std;

// ===== BASIC MOVE SEMANTICS =====

class DynamicArray {
private:
    int* data;
    size_t size;

public:
    // Constructor
    DynamicArray(size_t s) : size(s) {
        data = new int[size];
        for (size_t i = 0; i < size; i++) {
            data[i] = i * 10;
        }
        cout << "Constructor: created array of size " << size
             << " at " << data << endl;
    }

    // Copy constructor (expensive)
    DynamicArray(const DynamicArray& other) : size(other.size) {
        data = new int[size];
        copy(other.data, other.data + size, data);
        cout << "Copy Constructor: copied " << size
             << " elements to " << data << endl;
    }

    // Move constructor (efficient)
    DynamicArray(DynamicArray&& other) noexcept
        : data(other.data), size(other.size) {
        // "Steal" the resources
        other.data = nullptr;
        other.size = 0;
        cout << "Move Constructor: moved " << size
             << " elements from " << &other << endl;
    }

    // Copy assignment
    DynamicArray& operator=(const DynamicArray& other) {
        cout << "Copy Assignment" << endl;
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new int[size];
            copy(other.data, other.data + size, data);
        }
        return *this;
    }

    // Move assignment
    DynamicArray& operator=(DynamicArray&& other) noexcept {
        cout << "Move Assignment" << endl;
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }

    ~DynamicArray() {
        cout << "Destructor: deleting " << size << " elements at " << data << endl;
        delete[] data;
    }

    void display() const {
        if (data) {
            cout << "Array [";
            for (size_t i = 0; i < size && i < 5; i++) {
                cout << data[i];
                if (i < size - 1 && i < 4) cout << ", ";
            }
            if (size > 5) cout << ", ...";
            cout << "]" << endl;
        } else {
            cout << "Array is empty (moved from)" << endl;
        }
    }

    size_t getSize() const { return size; }
};

// ===== STRING CLASS WITH MOVE SEMANTICS =====

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
    MyString(const MyString& other) : len(other.len) {
        str = new char[len + 1];
        strcpy(str, other.str);
        cout << "String Copy Constructor: \"" << str << "\"" << endl;
    }

    // Move constructor
    MyString(MyString&& other) noexcept : str(other.str), len(other.len) {
        cout << "String Move Constructor: \"" << str << "\"" << endl;
        other.str = nullptr;
        other.len = 0;
    }

    // Copy assignment
    MyString& operator=(const MyString& other) {
        cout << "String Copy Assignment" << endl;
        if (this != &other) {
            delete[] str;
            len = other.len;
            str = new char[len + 1];
            strcpy(str, other.str);
        }
        return *this;
    }

    // Move assignment
    MyString& operator=(MyString&& other) noexcept {
        cout << "String Move Assignment" << endl;
        if (this != &other) {
            delete[] str;
            str = other.str;
            len = other.len;
            other.str = nullptr;
            other.len = 0;
        }
        return *this;
    }

    ~MyString() {
        cout << "String Destructor: ";
        if (str) cout << "\"" << str << "\"";
        else cout << "(moved)";
        cout << endl;
        delete[] str;
    }

    const char* c_str() const { return str ? str : ""; }

    friend ostream& operator<<(ostream& os, const MyString& s) {
        if (s.str) os << s.str;
        return os;
    }
};

// ===== LVALUE VS RVALUE DEMONSTRATION =====

void demonstrateLvalueRvalue() {
    cout << "\nLvalue vs Rvalue Demonstration:" << endl;
    cout << "--------------------------------" << endl;

    int x = 10;  // x is an lvalue
    int y = 20;  // y is an lvalue

    // x and y are lvalues (have names, can take address)
    int* px = &x;
    cout << "x = " << x << ", address: " << px << endl;

    // (x + y) is an rvalue (temporary, no name, can't take address)
    int z = x + y;  // rvalue on right side
    // int* pr = &(x + y);  // Error: can't take address of rvalue

    cout << "z = x + y = " << z << endl;
}

// ===== MOVE-ONLY TYPE =====

class UniqueResource {
private:
    int* resource;
    int id;
    static int nextId;

public:
    UniqueResource() {
        id = nextId++;
        resource = new int(100);
        cout << "UniqueResource " << id << " created" << endl;
    }

    // Delete copy operations (move-only type)
    UniqueResource(const UniqueResource&) = delete;
    UniqueResource& operator=(const UniqueResource&) = delete;

    // Move constructor
    UniqueResource(UniqueResource&& other) noexcept
        : resource(other.resource), id(other.id) {
        other.resource = nullptr;
        cout << "UniqueResource " << id << " moved" << endl;
    }

    // Move assignment
    UniqueResource& operator=(UniqueResource&& other) noexcept {
        if (this != &other) {
            delete resource;
            resource = other.resource;
            id = other.id;
            other.resource = nullptr;
            cout << "UniqueResource " << id << " move-assigned" << endl;
        }
        return *this;
    }

    ~UniqueResource() {
        cout << "UniqueResource " << id << " destroyed" << endl;
        delete resource;
    }

    int getId() const { return id; }
};

int UniqueResource::nextId = 1;

// ===== FACTORY FUNCTION RETURNING BY VALUE =====

DynamicArray createLargeArray(size_t size) {
    cout << "\nInside factory function:" << endl;
    DynamicArray arr(size);
    return arr;  // Move semantics (or RVO)
}

MyString createString(const char* s) {
    cout << "\nInside string factory:" << endl;
    MyString str(s);
    return str;  // Move semantics (or RVO)
}

// ===== PERFECT FORWARDING EXAMPLE =====

void processValue(int& x) {
    cout << "Processing lvalue: " << x << endl;
}

void processValue(int&& x) {
    cout << "Processing rvalue: " << x << endl;
}

template<typename T>
void forwardValue(T&& x) {
    // Without forward, always calls lvalue version
    // processValue(x);

    // With forward, preserves value category
    processValue(std::forward<T>(x));
}

// ===== VECTOR-LIKE CONTAINER WITH MOVE =====

template<typename T>
class Container {
private:
    T* data;
    size_t capacity;
    size_t count;

public:
    Container() : data(nullptr), capacity(0), count(0) {
        cout << "Container Default Constructor" << endl;
    }

    explicit Container(size_t cap) : capacity(cap), count(0) {
        data = new T[capacity];
        cout << "Container Constructor (capacity " << capacity << ")" << endl;
    }

    // Copy constructor
    Container(const Container& other)
        : capacity(other.capacity), count(other.count) {
        data = new T[capacity];
        for (size_t i = 0; i < count; i++) {
            data[i] = other.data[i];
        }
        cout << "Container Copy Constructor" << endl;
    }

    // Move constructor
    Container(Container&& other) noexcept
        : data(other.data), capacity(other.capacity), count(other.count) {
        other.data = nullptr;
        other.capacity = 0;
        other.count = 0;
        cout << "Container Move Constructor" << endl;
    }

    // Copy assignment
    Container& operator=(const Container& other) {
        cout << "Container Copy Assignment" << endl;
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

    // Move assignment
    Container& operator=(Container&& other) noexcept {
        cout << "Container Move Assignment" << endl;
        if (this != &other) {
            delete[] data;
            data = other.data;
            capacity = other.capacity;
            count = other.count;
            other.data = nullptr;
            other.capacity = 0;
            other.count = 0;
        }
        return *this;
    }

    ~Container() {
        cout << "Container Destructor (count: " << count << ")" << endl;
        delete[] data;
    }

    void push_back(const T& value) {
        if (count < capacity) {
            data[count++] = value;
        }
    }

    // Move version of push_back
    void push_back(T&& value) {
        if (count < capacity) {
            data[count++] = std::move(value);
            cout << "push_back with move" << endl;
        }
    }

    size_t size() const { return count; }
};

// ===== SWAP WITH MOVE SEMANTICS =====

template<typename T>
void efficientSwap(T& a, T& b) {
    T temp = std::move(a);  // Move from a to temp
    a = std::move(b);        // Move from b to a
    b = std::move(temp);     // Move from temp to b
}

int main() {
    cout << "=== Program 132: Move Semantics ===" << endl;
    cout << "===================================\n" << endl;

    // 1. Basic move semantics
    cout << "1. Basic Move Semantics - DynamicArray" << endl;
    cout << "---------------------------------------" << endl;
    {
        DynamicArray arr1(5);
        arr1.display();

        cout << "\nMove constructor:" << endl;
        DynamicArray arr2 = std::move(arr1);
        cout << "arr1 after move: ";
        arr1.display();
        cout << "arr2: ";
        arr2.display();

        cout << "\nMove assignment:" << endl;
        DynamicArray arr3(3);
        arr3 = std::move(arr2);
        cout << "arr2 after move: ";
        arr2.display();
        cout << "arr3: ";
        arr3.display();
    }

    // 2. String with move semantics
    cout << "\n2. String with Move Semantics" << endl;
    cout << "------------------------------" << endl;
    {
        MyString s1("Hello World");
        cout << "s1: " << s1 << endl;

        cout << "\nMove constructor:" << endl;
        MyString s2 = std::move(s1);
        cout << "s1 after move: " << s1 << endl;
        cout << "s2: " << s2 << endl;

        cout << "\nMove assignment:" << endl;
        MyString s3("Temporary");
        s3 = std::move(s2);
        cout << "s2 after move: " << s2 << endl;
        cout << "s3: " << s3 << endl;
    }

    // 3. Lvalue vs Rvalue
    demonstrateLvalueRvalue();

    // 4. Move-only type
    cout << "\n4. Move-Only Type - UniqueResource" << endl;
    cout << "-----------------------------------" << endl;
    {
        UniqueResource r1;
        cout << "r1 ID: " << r1.getId() << endl;

        // UniqueResource r2 = r1;  // Error: copy deleted

        cout << "\nMoving resource:" << endl;
        UniqueResource r2 = std::move(r1);
        cout << "r2 ID: " << r2.getId() << endl;
    }

    // 5. Factory functions with move
    cout << "\n5. Factory Functions with Move" << endl;
    cout << "--------------------------------" << endl;
    {
        DynamicArray arr = createLargeArray(1000);
        cout << "Received array of size: " << arr.getSize() << endl;

        MyString str = createString("Factory Pattern");
        cout << "Received string: " << str << endl;
    }

    // 6. Perfect forwarding
    cout << "\n6. Perfect Forwarding" << endl;
    cout << "----------------------" << endl;
    {
        int x = 42;
        forwardValue(x);        // Lvalue
        forwardValue(100);      // Rvalue
        forwardValue(x + 10);   // Rvalue
    }

    // 7. Container with move semantics
    cout << "\n7. Container with Move Semantics" << endl;
    cout << "---------------------------------" << endl;
    {
        Container<MyString> cont(5);

        cout << "\nPushing strings:" << endl;
        cont.push_back(MyString("First"));
        cont.push_back(MyString("Second"));

        cout << "\nMoving container:" << endl;
        Container<MyString> cont2 = std::move(cont);
        cout << "Container size: " << cont2.size() << endl;
    }

    // 8. Efficient swap with move
    cout << "\n8. Efficient Swap with Move" << endl;
    cout << "----------------------------" << endl;
    {
        DynamicArray a(100);
        DynamicArray b(200);

        cout << "\nBefore swap:" << endl;
        cout << "a size: " << a.getSize() << endl;
        cout << "b size: " << b.getSize() << endl;

        cout << "\nSwapping:" << endl;
        efficientSwap(a, b);

        cout << "\nAfter swap:" << endl;
        cout << "a size: " << a.getSize() << endl;
        cout << "b size: " << b.getSize() << endl;
    }

    // 9. Vector operations with move
    cout << "\n9. Vector Operations with Move" << endl;
    cout << "-------------------------------" << endl;
    {
        vector<MyString> vec;
        vec.reserve(3);

        cout << "\nPushing temporary strings:" << endl;
        vec.push_back(MyString("First"));
        vec.push_back(MyString("Second"));
        vec.push_back(MyString("Third"));

        cout << "\nVector size: " << vec.size() << endl;
    }

    // 10. Return value optimization
    cout << "\n10. Return Value Optimization (RVO)" << endl;
    cout << "------------------------------------" << endl;
    {
        cout << "Creating array through factory:" << endl;
        DynamicArray arr = createLargeArray(50);
        cout << "Array created with size: " << arr.getSize() << endl;
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Move constructor - transfers resources efficiently" << endl;
    cout << "2. Move assignment operator - moves instead of copies" << endl;
    cout << "3. Rvalue references (&&) - bind to temporary objects" << endl;
    cout << "4. std::move - casts to rvalue reference" << endl;
    cout << "5. Move-only types - delete copy, allow move" << endl;
    cout << "6. Perfect forwarding with std::forward" << endl;
    cout << "7. Lvalues vs rvalues - value categories" << endl;
    cout << "8. Performance benefits - avoid unnecessary copies" << endl;
    cout << "9. noexcept - mark move operations as non-throwing" << endl;
    cout << "10. RVO - compiler optimization for return values" << endl;

    return 0;
}
