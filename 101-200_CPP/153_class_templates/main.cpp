/*
 * Program 153: Class Templates
 *
 * Demonstrates:
 * - Class template syntax
 * - Template member functions
 * - Template member variables
 * - Nested classes in templates
 * - Static members in templates
 * - Friend functions in templates
 * - Template class inheritance
 * - Template aliases
 * - Template instantiation
 * - Practical class template examples
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic class template
template<typename T>
class Box {
private:
    T value;
public:
    Box() : value(T()) {}
    Box(T v) : value(v) {}

    void setValue(T v) { value = v; }
    T getValue() const { return value; }

    void print() const {
        cout << "  Box contains: " << value << "\n";
    }
};

void basicClassTemplate() {
    printSection("1. BASIC CLASS TEMPLATE");

    cout << "\nCreating boxes of different types:\n";
    Box<int> intBox(42);
    Box<double> doubleBox(3.14);
    Box<string> stringBox("Hello");

    intBox.print();
    doubleBox.print();
    stringBox.print();

    cout << "\nModifying values:\n";
    intBox.setValue(100);
    stringBox.setValue("World");

    cout << "  intBox: " << intBox.getValue() << "\n";
    cout << "  stringBox: " << stringBox.getValue() << "\n";
}

// Class with multiple template parameters
template<typename T, typename U>
class Pair {
private:
    T first;
    U second;
public:
    Pair(T f, U s) : first(f), second(s) {}

    T getFirst() const { return first; }
    U getSecond() const { return second; }

    void setFirst(T f) { first = f; }
    void setSecond(U s) { second = s; }

    void print() const {
        cout << "  Pair: (" << first << ", " << second << ")\n";
    }
};

void multipleTemplateParameters() {
    printSection("2. MULTIPLE TEMPLATE PARAMETERS");

    cout << "\nPair<int, string>:\n";
    Pair<int, string> p1(1, "one");
    p1.print();

    cout << "\nPair<string, double>:\n";
    Pair<string, double> p2("pi", 3.14159);
    p2.print();

    cout << "\nPair<int, int>:\n";
    Pair<int, int> point(10, 20);
    point.print();

    cout << "\nModifying pair:\n";
    p1.setFirst(2);
    p1.setSecond("two");
    p1.print();
}

// Class with non-type template parameters
template<typename T, int Size>
class StaticArray {
private:
    T data[Size];
public:
    StaticArray() {
        for (int i = 0; i < Size; i++) {
            data[i] = T();
        }
    }

    T& operator[](int index) {
        if (index < 0 || index >= Size) {
            throw out_of_range("Index out of range");
        }
        return data[index];
    }

    const T& operator[](int index) const {
        if (index < 0 || index >= Size) {
            throw out_of_range("Index out of range");
        }
        return data[index];
    }

    int size() const { return Size; }

    void print() const {
        cout << "  Array[" << Size << "]: ";
        for (int i = 0; i < Size; i++) {
            cout << data[i] << " ";
        }
        cout << "\n";
    }
};

void nonTypeTemplateParameters() {
    printSection("3. NON-TYPE TEMPLATE PARAMETERS");

    cout << "\nStaticArray<int, 5>:\n";
    StaticArray<int, 5> arr1;
    for (int i = 0; i < arr1.size(); i++) {
        arr1[i] = i * 10;
    }
    arr1.print();

    cout << "\nStaticArray<double, 3>:\n";
    StaticArray<double, 3> arr2;
    for (int i = 0; i < arr2.size(); i++) {
        arr2[i] = i * 1.5;
    }
    arr2.print();

    cout << "\nBounds checking:\n";
    try {
        arr1[10] = 100;
    } catch (const out_of_range& e) {
        cout << "  Exception: " << e.what() << "\n";
    }
}

// Template member functions
template<typename T>
class Container {
private:
    vector<T> data;
public:
    void add(const T& item) {
        data.push_back(item);
    }

    void remove(const T& item) {
        data.erase(remove(data.begin(), data.end(), item), data.end());
    }

    template<typename U>
    void addConverted(const U& item) {
        data.push_back(static_cast<T>(item));
    }

    bool contains(const T& item) const {
        return find(data.begin(), data.end(), item) != data.end();
    }

    void print() const {
        cout << "  Container: ";
        for (const auto& item : data) {
            cout << item << " ";
        }
        cout << "\n";
    }

    int size() const { return data.size(); }
};

void templateMemberFunctions() {
    printSection("4. TEMPLATE MEMBER FUNCTIONS");

    cout << "\nContainer operations:\n";
    Container<int> c;
    c.add(10);
    c.add(20);
    c.add(30);
    c.print();

    cout << "\nTemplate member function:\n";
    c.addConverted(3.14);  // Converts double to int
    c.addConverted(5.9);
    c.print();

    cout << "\nContains check:\n";
    cout << "  contains(20): " << (c.contains(20) ? "Yes" : "No") << "\n";
    cout << "  contains(100): " << (c.contains(100) ? "Yes" : "No") << "\n";

    cout << "\nRemove operation:\n";
    c.remove(20);
    c.print();
}

// Static members in template classes
template<typename T>
class Counter {
private:
    static int count;
    T value;
public:
    Counter(T v) : value(v) {
        count++;
    }

    ~Counter() {
        count--;
    }

    static int getCount() {
        return count;
    }

    void print() const {
        cout << "  Value: " << value << ", Count: " << count << "\n";
    }
};

// Static member definition
template<typename T>
int Counter<T>::count = 0;

void staticMembers() {
    printSection("5. STATIC MEMBERS");

    cout << "\nCounter<int> instances:\n";
    cout << "  Initial count: " << Counter<int>::getCount() << "\n";

    Counter<int> c1(10);
    cout << "  After c1: " << Counter<int>::getCount() << "\n";

    Counter<int> c2(20);
    cout << "  After c2: " << Counter<int>::getCount() << "\n";

    {
        Counter<int> c3(30);
        cout << "  After c3 (in scope): " << Counter<int>::getCount() << "\n";
    }

    cout << "  After c3 destroyed: " << Counter<int>::getCount() << "\n";

    cout << "\nCounter<double> instances (separate count):\n";
    Counter<double> d1(3.14);
    cout << "  Counter<int>: " << Counter<int>::getCount() << "\n";
    cout << "  Counter<double>: " << Counter<double>::getCount() << "\n";
}

// Nested classes
template<typename T>
class Tree {
public:
    struct Node {
        T data;
        Node* left;
        Node* right;

        Node(T d) : data(d), left(nullptr), right(nullptr) {}
    };

private:
    Node* root;

public:
    Tree() : root(nullptr) {}

    void insert(T value) {
        if (!root) {
            root = new Node(value);
            cout << "  Inserted " << value << " as root\n";
        } else {
            cout << "  Inserted " << value << "\n";
            // Simplified insertion
        }
    }

    ~Tree() {
        // Simplified cleanup
        delete root;
    }
};

void nestedClasses() {
    printSection("6. NESTED CLASSES");

    cout << "\nTree with nested Node:\n";
    Tree<int> intTree;
    intTree.insert(10);
    intTree.insert(5);
    intTree.insert(15);

    cout << "\nTree<string>:\n";
    Tree<string> stringTree;
    stringTree.insert("root");
    stringTree.insert("left");
    stringTree.insert("right");
}

// Friend functions
template<typename T>
class Point {
private:
    T x, y;
public:
    Point(T x, T y) : x(x), y(y) {}

    template<typename U>
    friend ostream& operator<<(ostream& os, const Point<U>& p);

    T getX() const { return x; }
    T getY() const { return y; }
};

template<typename T>
ostream& operator<<(ostream& os, const Point<T>& p) {
    os << "(" << p.x << ", " << p.y << ")";
    return os;
}

void friendFunctions() {
    printSection("7. FRIEND FUNCTIONS");

    cout << "\nPoint with friend operator<<:\n";
    Point<int> p1(10, 20);
    Point<double> p2(3.14, 2.71);

    cout << "  p1: " << p1 << "\n";
    cout << "  p2: " << p2 << "\n";
}

// Template inheritance
template<typename T>
class Base {
protected:
    T value;
public:
    Base(T v) : value(v) {}

    void printBase() const {
        cout << "  Base value: " << value << "\n";
    }
};

template<typename T>
class Derived : public Base<T> {
private:
    T extra;
public:
    Derived(T v, T e) : Base<T>(v), extra(e) {}

    void printDerived() const {
        cout << "  Base value: " << this->value << ", Extra: " << extra << "\n";
    }
};

template<typename T, typename U>
class MultiDerived : public Base<T> {
private:
    U additional;
public:
    MultiDerived(T v, U a) : Base<T>(v), additional(a) {}

    void print() const {
        cout << "  Base<T>: " << this->value << ", Additional<U>: " << additional << "\n";
    }
};

void templateInheritance() {
    printSection("8. TEMPLATE INHERITANCE");

    cout << "\nDerived from Base:\n";
    Derived<int> d1(10, 20);
    d1.printBase();
    d1.printDerived();

    cout << "\nMultiDerived with different types:\n";
    MultiDerived<int, string> md(42, "extra data");
    md.printBase();
    md.print();
}

// Template aliases (C++11)
template<typename T>
using Vec = vector<T>;

template<typename T>
using Ptr = shared_ptr<T>;

template<typename Key, typename Value>
using StringMap = Pair<Key, Value>;

void templateAliases() {
    printSection("9. TEMPLATE ALIASES");

    cout << "\nUsing Vec alias:\n";
    Vec<int> v = {1, 2, 3, 4, 5};
    cout << "  Vec<int>: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\nUsing Ptr alias:\n";
    Ptr<int> ptr = make_shared<int>(42);
    cout << "  Ptr<int>: " << *ptr << "\n";

    cout << "\nUsing StringMap alias:\n";
    StringMap<string, int> sm("age", 30);
    sm.print();
}

// Smart container example
template<typename T>
class SmartVector {
private:
    T* data;
    int capacity;
    int count;

    void resize() {
        capacity *= 2;
        T* newData = new T[capacity];
        for (int i = 0; i < count; i++) {
            newData[i] = data[i];
        }
        delete[] data;
        data = newData;
    }

public:
    SmartVector() : data(new T[2]), capacity(2), count(0) {}

    ~SmartVector() {
        delete[] data;
    }

    void push_back(const T& value) {
        if (count == capacity) {
            resize();
        }
        data[count++] = value;
    }

    T& operator[](int index) {
        return data[index];
    }

    int size() const { return count; }

    void print() const {
        cout << "  SmartVector[" << count << "]: ";
        for (int i = 0; i < count; i++) {
            cout << data[i] << " ";
        }
        cout << "\n";
    }
};

void practicalExample() {
    printSection("10. PRACTICAL EXAMPLE: SMART VECTOR");

    cout << "\nSmartVector with dynamic resizing:\n";
    SmartVector<int> sv;

    cout << "  Adding elements:\n";
    for (int i = 1; i <= 10; i++) {
        sv.push_back(i * 10);
        cout << "    Size: " << sv.size() << "\n";
    }

    sv.print();

    cout << "\nAccessing elements:\n";
    cout << "  sv[0] = " << sv[0] << "\n";
    cout << "  sv[5] = " << sv[5] << "\n";

    cout << "\nSmartVector<string>:\n";
    SmartVector<string> svs;
    svs.push_back("hello");
    svs.push_back("world");
    svs.push_back("foo");
    svs.push_back("bar");
    svs.print();
}

int main() {
    cout << "CLASS TEMPLATES COMPREHENSIVE GUIDE\n";
    cout << "===================================\n";

    basicClassTemplate();
    multipleTemplateParameters();
    nonTypeTemplateParameters();
    templateMemberFunctions();
    staticMembers();
    nestedClasses();
    friendFunctions();
    templateInheritance();
    templateAliases();
    practicalExample();

    printSection("SUMMARY");
    cout << "\nClass template features:\n";
    cout << "- Generic classes for any type\n";
    cout << "- Multiple template parameters (type and non-type)\n";
    cout << "- Template member functions\n";
    cout << "- Static members are per-instantiation\n";
    cout << "- Can contain nested types\n";
    cout << "- Support friend functions and operators\n";
    cout << "- Can be inherited from or inherit\n";
    cout << "- Template aliases simplify complex types\n";
    cout << "\nClass templates are the foundation of STL containers!\n";

    return 0;
}
