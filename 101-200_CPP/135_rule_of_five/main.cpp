/*
 * Program 135: Rule of Five in C++ (C++11)
 *
 * This program demonstrates:
 * - Rule of Three (C++98): Destructor, Copy Constructor, Copy Assignment
 * - Rule of Five (C++11): + Move Constructor, Move Assignment
 * - Rule of Zero: Use smart pointers and standard library
 * - When to implement special member functions
 * - Default and delete keywords
 * - Proper resource management
 */

#include <iostream>
#include <string>
#include <algorithm>
#include <utility>

using namespace std;

// ===== RULE OF THREE (C++98) =====

class RuleOfThree {
private:
    int* data;
    size_t size;

public:
    // Constructor
    RuleOfThree(size_t s) : size(s) {
        data = new int[size];
        for (size_t i = 0; i < size; i++) {
            data[i] = i;
        }
        cout << "RuleOfThree Constructor: size " << size << endl;
    }

    // 1. Destructor
    ~RuleOfThree() {
        cout << "RuleOfThree Destructor: size " << size << endl;
        delete[] data;
    }

    // 2. Copy Constructor
    RuleOfThree(const RuleOfThree& other) : size(other.size) {
        data = new int[size];
        copy(other.data, other.data + size, data);
        cout << "RuleOfThree Copy Constructor: size " << size << endl;
    }

    // 3. Copy Assignment Operator
    RuleOfThree& operator=(const RuleOfThree& other) {
        cout << "RuleOfThree Copy Assignment: size " << other.size << endl;
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new int[size];
            copy(other.data, other.data + size, data);
        }
        return *this;
    }

    void display() const {
        cout << "Data [";
        for (size_t i = 0; i < size && i < 5; i++) {
            cout << data[i];
            if (i < size - 1 && i < 4) cout << ", ";
        }
        if (size > 5) cout << ", ...";
        cout << "]" << endl;
    }
};

// ===== RULE OF FIVE (C++11) =====

class RuleOfFive {
private:
    int* data;
    size_t size;
    string name;

public:
    // Constructor
    RuleOfFive(const string& n, size_t s) : name(n), size(s) {
        data = new int[size];
        for (size_t i = 0; i < size; i++) {
            data[i] = i * 10;
        }
        cout << "RuleOfFive Constructor: " << name
             << " (size " << size << ")" << endl;
    }

    // 1. Destructor
    ~RuleOfFive() {
        cout << "RuleOfFive Destructor: " << name
             << " (size " << size << ")" << endl;
        delete[] data;
    }

    // 2. Copy Constructor
    RuleOfFive(const RuleOfFive& other)
        : name(other.name + "_copy"), size(other.size) {
        data = new int[size];
        copy(other.data, other.data + size, data);
        cout << "RuleOfFive Copy Constructor: " << name << endl;
    }

    // 3. Copy Assignment Operator
    RuleOfFive& operator=(const RuleOfFive& other) {
        cout << "RuleOfFive Copy Assignment: " << other.name << endl;
        if (this != &other) {
            delete[] data;
            name = other.name + "_assigned";
            size = other.size;
            data = new int[size];
            copy(other.data, other.data + size, data);
        }
        return *this;
    }

    // 4. Move Constructor
    RuleOfFive(RuleOfFive&& other) noexcept
        : data(other.data), size(other.size), name(move(other.name)) {
        other.data = nullptr;
        other.size = 0;
        cout << "RuleOfFive Move Constructor: " << name << endl;
    }

    // 5. Move Assignment Operator
    RuleOfFive& operator=(RuleOfFive&& other) noexcept {
        cout << "RuleOfFive Move Assignment: " << other.name << endl;
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            name = move(other.name);
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }

    void display() const {
        cout << name << " [";
        if (data) {
            for (size_t i = 0; i < size && i < 5; i++) {
                cout << data[i];
                if (i < size - 1 && i < 4) cout << ", ";
            }
            if (size > 5) cout << ", ...";
        } else {
            cout << "moved";
        }
        cout << "]" << endl;
    }

    const string& getName() const { return name; }
    size_t getSize() const { return size; }
};

// ===== RULE OF ZERO (PREFERRED) =====

#include <memory>
#include <vector>

class RuleOfZero {
private:
    unique_ptr<int[]> data;  // Smart pointer manages memory
    size_t size;
    string name;  // string manages its own memory
    vector<int> metadata;  // vector manages its own memory

public:
    // Only need constructor
    RuleOfZero(const string& n, size_t s)
        : data(make_unique<int[]>(s)), size(s), name(n) {
        for (size_t i = 0; i < size; i++) {
            data[i] = i * 5;
        }
        metadata = {1, 2, 3};
        cout << "RuleOfZero Constructor: " << name << endl;
    }

    // Compiler-generated special members work correctly!
    // ~RuleOfZero() = default;  // Not needed, implicit is fine
    // Copy constructor and assignment would work if data was shared_ptr
    // Move constructor and assignment are automatically efficient

    void display() const {
        cout << name << " [";
        for (size_t i = 0; i < size && i < 5; i++) {
            cout << data[i];
            if (i < size - 1 && i < 4) cout << ", ";
        }
        if (size > 5) cout << ", ...";
        cout << "]" << endl;
    }

    // Note: This class is move-only because unique_ptr is move-only
    // To make it copyable, use shared_ptr instead
};

// ===== EXPLICIT CONTROL WITH DEFAULT AND DELETE =====

class ExplicitControl {
private:
    int* data;

public:
    ExplicitControl() : data(new int(42)) {
        cout << "ExplicitControl Constructor" << endl;
    }

    ~ExplicitControl() {
        cout << "ExplicitControl Destructor" << endl;
        delete data;
    }

    // Explicitly use default copy constructor
    ExplicitControl(const ExplicitControl& other) = default;

    // Explicitly delete copy assignment
    ExplicitControl& operator=(const ExplicitControl&) = delete;

    // Explicitly use default move constructor
    ExplicitControl(ExplicitControl&&) = default;

    // Explicitly use default move assignment
    ExplicitControl& operator=(ExplicitControl&&) = default;
};

// ===== IMPLEMENTING COPY-AND-SWAP IDIOM =====

class CopyAndSwap {
private:
    int* data;
    size_t size;

public:
    CopyAndSwap(size_t s) : size(s) {
        data = new int[size];
        cout << "CopyAndSwap Constructor" << endl;
    }

    ~CopyAndSwap() {
        cout << "CopyAndSwap Destructor" << endl;
        delete[] data;
    }

    // Copy constructor
    CopyAndSwap(const CopyAndSwap& other) : size(other.size) {
        data = new int[size];
        copy(other.data, other.data + size, data);
        cout << "CopyAndSwap Copy Constructor" << endl;
    }

    // Move constructor
    CopyAndSwap(CopyAndSwap&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
        cout << "CopyAndSwap Move Constructor" << endl;
    }

    // Swap function
    void swap(CopyAndSwap& other) noexcept {
        using std::swap;
        swap(data, other.data);
        swap(size, other.size);
    }

    // Unified assignment operator using copy-and-swap
    CopyAndSwap& operator=(CopyAndSwap other) {  // Pass by value
        cout << "CopyAndSwap Assignment (copy-and-swap)" << endl;
        swap(other);
        return *this;
    }
};

// ===== PROPER STRING CLASS WITH RULE OF FIVE =====

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
        cout << "MyString Constructor: \"" << str << "\"" << endl;
    }

    // Destructor
    ~MyString() {
        cout << "MyString Destructor: \"" << (str ? str : "moved") << "\"" << endl;
        delete[] str;
    }

    // Copy Constructor
    MyString(const MyString& other) {
        len = other.len;
        str = new char[len + 1];
        strcpy(str, other.str);
        cout << "MyString Copy Constructor: \"" << str << "\"" << endl;
    }

    // Move Constructor
    MyString(MyString&& other) noexcept : str(other.str), len(other.len) {
        cout << "MyString Move Constructor: \"" << str << "\"" << endl;
        other.str = nullptr;
        other.len = 0;
    }

    // Copy Assignment
    MyString& operator=(const MyString& other) {
        cout << "MyString Copy Assignment: \"" << other.str << "\"" << endl;
        if (this != &other) {
            delete[] str;
            len = other.len;
            str = new char[len + 1];
            strcpy(str, other.str);
        }
        return *this;
    }

    // Move Assignment
    MyString& operator=(MyString&& other) noexcept {
        cout << "MyString Move Assignment: \"" << other.str << "\"" << endl;
        if (this != &other) {
            delete[] str;
            str = other.str;
            len = other.len;
            other.str = nullptr;
            other.len = 0;
        }
        return *this;
    }

    const char* c_str() const { return str ? str : ""; }

    friend ostream& operator<<(ostream& os, const MyString& s) {
        if (s.str) os << s.str;
        return os;
    }
};

// ===== HELPER FUNCTIONS =====

RuleOfFive createRuleOfFive(const string& name, size_t size) {
    return RuleOfFive(name, size);
}

// ===== DEMONSTRATIONS =====

void demonstrateRuleOfThree() {
    cout << "\n=== Rule of Three (C++98) ===" << endl;
    cout << "------------------------------" << endl;

    RuleOfThree obj1(5);
    obj1.display();

    cout << "\nCopy constructor:" << endl;
    RuleOfThree obj2 = obj1;
    obj2.display();

    cout << "\nCopy assignment:" << endl;
    RuleOfThree obj3(3);
    obj3 = obj1;
    obj3.display();

    cout << "\nLeaving scope..." << endl;
}

void demonstrateRuleOfFive() {
    cout << "\n=== Rule of Five (C++11) ===" << endl;
    cout << "-----------------------------" << endl;

    RuleOfFive obj1("original", 5);
    obj1.display();

    cout << "\nCopy constructor:" << endl;
    RuleOfFive obj2 = obj1;
    obj1.display();
    obj2.display();

    cout << "\nMove constructor:" << endl;
    RuleOfFive obj3 = std::move(obj2);
    obj2.display();
    obj3.display();

    cout << "\nCopy assignment:" << endl;
    RuleOfFive obj4("other", 3);
    obj4 = obj1;
    obj4.display();

    cout << "\nMove assignment:" << endl;
    RuleOfFive obj5("another", 2);
    obj5 = std::move(obj3);
    obj3.display();
    obj5.display();

    cout << "\nReturning from factory function:" << endl;
    RuleOfFive obj6 = createRuleOfFive("factory", 10);
    obj6.display();

    cout << "\nLeaving scope..." << endl;
}

void demonstrateRuleOfZero() {
    cout << "\n=== Rule of Zero (Preferred) ===" << endl;
    cout << "---------------------------------" << endl;

    RuleOfZero obj1("zero1", 5);
    obj1.display();

    cout << "\nMove constructor:" << endl;
    RuleOfZero obj2 = std::move(obj1);
    obj2.display();

    cout << "\nMove assignment:" << endl;
    RuleOfZero obj3("zero2", 3);
    obj3 = std::move(obj2);
    obj3.display();

    cout << "\nNo explicit special member functions needed!" << endl;
    cout << "Leaving scope..." << endl;
}

int main() {
    cout << "=== Program 135: Rule of Five ===" << endl;
    cout << "=================================\n" << endl;

    // 1. Rule of Three
    demonstrateRuleOfThree();

    // 2. Rule of Five
    demonstrateRuleOfFive();

    // 3. Rule of Zero
    demonstrateRuleOfZero();

    // 4. String class with Rule of Five
    cout << "\n=== String Class with Rule of Five ===" << endl;
    cout << "---------------------------------------" << endl;
    {
        MyString s1("Hello");
        MyString s2 = s1;              // Copy
        MyString s3 = std::move(s1);   // Move
        MyString s4("World");
        s4 = s2;                       // Copy assignment
        s4 = std::move(s3);            // Move assignment

        cout << "\nFinal strings:" << endl;
        cout << "s1: " << s1 << endl;
        cout << "s2: " << s2 << endl;
        cout << "s3: " << s3 << endl;
        cout << "s4: " << s4 << endl;
    }

    // 5. Copy-and-Swap idiom
    cout << "\n=== Copy-and-Swap Idiom ===" << endl;
    cout << "----------------------------" << endl;
    {
        CopyAndSwap obj1(10);
        CopyAndSwap obj2(5);

        cout << "\nCopy assignment (uses copy-and-swap):" << endl;
        obj2 = obj1;

        cout << "\nMove assignment (also uses copy-and-swap):" << endl;
        CopyAndSwap obj3(3);
        obj3 = std::move(obj1);
    }

    // 6. Performance comparison
    cout << "\n=== Performance Comparison ===" << endl;
    cout << "-------------------------------" << endl;
    {
        cout << "Creating large object with copy:" << endl;
        RuleOfFive obj1("large", 1000000);
        RuleOfFive obj2 = obj1;  // Expensive copy

        cout << "\nCreating large object with move:" << endl;
        RuleOfFive obj3("large2", 1000000);
        RuleOfFive obj4 = std::move(obj3);  // Cheap move

        cout << "\nMove is much faster for large objects!" << endl;
    }

    cout << "\n=== Summary ===" << endl;
    cout << "=================" << endl;
    cout << "\nRule of Three (C++98):" << endl;
    cout << "  If you define one of: Destructor, Copy Constructor, Copy Assignment" << endl;
    cout << "  You should define all three." << endl;

    cout << "\nRule of Five (C++11):" << endl;
    cout << "  If you define one of the Rule of Three," << endl;
    cout << "  You should also define: Move Constructor, Move Assignment" << endl;

    cout << "\nRule of Zero (Preferred):" << endl;
    cout << "  Use smart pointers and standard library classes" << endl;
    cout << "  Let compiler generate all special member functions" << endl;
    cout << "  Explicit special members only when necessary" << endl;

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. Destructor - cleanup resources" << endl;
    cout << "2. Copy constructor - deep copy for ownership" << endl;
    cout << "3. Copy assignment operator - assign with deep copy" << endl;
    cout << "4. Move constructor - transfer ownership efficiently" << endl;
    cout << "5. Move assignment operator - assign by moving" << endl;
    cout << "6. Rule of Zero - prefer smart pointers" << endl;
    cout << "7. Default and delete keywords" << endl;
    cout << "8. Copy-and-swap idiom - exception-safe assignment" << endl;
    cout << "9. noexcept for move operations" << endl;
    cout << "10. Performance benefits of move semantics" << endl;

    return 0;
}
