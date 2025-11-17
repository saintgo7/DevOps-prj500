/*
 * Program 154: Template Specialization
 *
 * Demonstrates:
 * - Full (explicit) template specialization
 * - Partial template specialization
 * - Function template specialization
 * - Class template specialization
 * - Member function specialization
 * - Specialization for pointers
 * - Tag dispatch pattern
 * - SFINAE basics
 * - When to use specialization
 */

#include <iostream>
#include <string>
#include <vector>
#include <type_traits>
#include <cstring>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Full function template specialization
template<typename T>
T absolute(T value) {
    return value < 0 ? -value : value;
}

template<>
int absolute<int>(int value) {
    cout << "  [Specialized for int]\n";
    return value < 0 ? -value : value;
}

template<>
string absolute<string>(string value) {
    cout << "  [Specialized for string]\n";
    return "String has no absolute value: " + value;
}

void functionSpecialization() {
    printSection("1. FUNCTION TEMPLATE SPECIALIZATION");

    cout << "\nGeneric absolute:\n";
    cout << "  absolute(-10.5) = " << absolute(-10.5) << "\n";
    cout << "  absolute(-42L) = " << absolute(-42L) << "\n";

    cout << "\nSpecialized absolute:\n";
    cout << "  absolute(-10) = " << absolute(-10) << "\n";
    cout << "  absolute(\"hello\") = " << absolute(string("hello")) << "\n";
}

// Class template full specialization
template<typename T>
class Storage {
private:
    T data;
public:
    Storage(T value) : data(value) {}

    void print() const {
        cout << "  Generic Storage: " << data << "\n";
    }

    T get() const { return data; }
};

template<>
class Storage<bool> {
private:
    bool data;
public:
    Storage(bool value) : data(value) {}

    void print() const {
        cout << "  Boolean Storage: " << (data ? "true" : "false") << "\n";
    }

    bool get() const { return data; }

    void toggle() {
        data = !data;
    }
};

template<>
class Storage<const char*> {
private:
    string data;
public:
    Storage(const char* value) : data(value) {}

    void print() const {
        cout << "  C-String Storage: \"" << data << "\"\n";
    }

    string get() const { return data; }

    void append(const char* str) {
        data += str;
    }
};

void classSpecialization() {
    printSection("2. CLASS TEMPLATE SPECIALIZATION");

    cout << "\nGeneric Storage:\n";
    Storage<int> intStore(42);
    Storage<double> doubleStore(3.14);
    intStore.print();
    doubleStore.print();

    cout << "\nSpecialized for bool:\n";
    Storage<bool> boolStore(true);
    boolStore.print();
    boolStore.toggle();
    cout << "  After toggle:\n";
    boolStore.print();

    cout << "\nSpecialized for const char*:\n";
    Storage<const char*> strStore("Hello");
    strStore.print();
    strStore.append(" World");
    cout << "  After append:\n";
    strStore.print();
}

// Partial specialization (only for classes, not functions)
template<typename T, typename U>
class Pair {
public:
    T first;
    U second;

    Pair(T f, U s) : first(f), second(s) {}

    void print() const {
        cout << "  Generic Pair: (" << first << ", " << second << ")\n";
    }
};

// Partial specialization: both types are the same
template<typename T>
class Pair<T, T> {
public:
    T first;
    T second;

    Pair(T f, T s) : first(f), second(s) {}

    void print() const {
        cout << "  Same-Type Pair: (" << first << ", " << second << ")\n";
    }

    bool areSame() const {
        return first == second;
    }
};

// Partial specialization: second type is pointer
template<typename T, typename U>
class Pair<T, U*> {
public:
    T first;
    U* second;

    Pair(T f, U* s) : first(f), second(s) {}

    void print() const {
        cout << "  Pointer Pair: (" << first << ", " << *second << ")\n";
    }
};

void partialSpecialization() {
    printSection("3. PARTIAL SPECIALIZATION");

    cout << "\nGeneric Pair:\n";
    Pair<int, string> p1(1, "one");
    p1.print();

    cout << "\nSame-type Pair specialization:\n";
    Pair<int, int> p2(10, 20);
    p2.print();
    cout << "  areSame(): " << (p2.areSame() ? "Yes" : "No") << "\n";

    Pair<string, string> p3("hello", "hello");
    p3.print();
    cout << "  areSame(): " << (p3.areSame() ? "Yes" : "No") << "\n";

    cout << "\nPointer Pair specialization:\n";
    int value = 42;
    Pair<string, int> p4("answer", &value);
    p4.print();
}

// Specialization for pointer types
template<typename T>
class SmartPtr {
private:
    T value;
public:
    SmartPtr(T v) : value(v) {}

    void print() const {
        cout << "  Value: " << value << "\n";
    }
};

template<typename T>
class SmartPtr<T*> {
private:
    T* ptr;
    bool owner;
public:
    SmartPtr(T* p, bool own = true) : ptr(p), owner(own) {}

    ~SmartPtr() {
        if (owner && ptr) {
            delete ptr;
        }
    }

    void print() const {
        cout << "  Pointer to: " << (ptr ? to_string(*ptr) : "null") << "\n";
    }

    T* get() const { return ptr; }
    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }
};

void pointerSpecialization() {
    printSection("4. POINTER SPECIALIZATION");

    cout << "\nRegular SmartPtr:\n";
    SmartPtr<int> sp1(42);
    sp1.print();

    cout << "\nPointer SmartPtr (auto-deletes):\n";
    SmartPtr<int*> sp2(new int(100));
    sp2.print();
    cout << "  Dereferenced: " << *sp2 << "\n";

    SmartPtr<string*> sp3(new string("Hello"));
    sp3.print();
    cout << "  Dereferenced: " << *sp3 << "\n";
}

// Member function specialization
template<typename T>
class Array {
private:
    T* data;
    int size;
public:
    Array(int s) : size(s) {
        data = new T[size];
        for (int i = 0; i < size; i++) {
            data[i] = T();
        }
    }

    ~Array() {
        delete[] data;
    }

    void clear();

    T& operator[](int i) { return data[i]; }

    void print() const {
        cout << "  Array: ";
        for (int i = 0; i < size; i++) {
            cout << data[i] << " ";
        }
        cout << "\n";
    }
};

template<typename T>
void Array<T>::clear() {
    for (int i = 0; i < size; i++) {
        data[i] = T();
    }
}

template<>
void Array<bool>::clear() {
    cout << "  [Specialized clear for bool array]\n";
    for (int i = 0; i < size; i++) {
        data[i] = false;
    }
}

void memberFunctionSpecialization() {
    printSection("5. MEMBER FUNCTION SPECIALIZATION");

    cout << "\nGeneric Array clear:\n";
    Array<int> arr1(5);
    for (int i = 0; i < 5; i++) arr1[i] = i + 1;
    arr1.print();
    arr1.clear();
    arr1.print();

    cout << "\nSpecialized clear for bool:\n";
    Array<bool> arr2(5);
    arr2.clear();
    arr2.print();
}

// Tag dispatch pattern
struct int_tag {};
struct float_tag {};

template<typename T>
struct type_tag {
    using type = int_tag;
};

template<>
struct type_tag<float> {
    using type = float_tag;
};

template<>
struct type_tag<double> {
    using type = float_tag;
};

template<typename T>
void process_impl(T value, int_tag) {
    cout << "  Processing integer: " << value << "\n";
}

template<typename T>
void process_impl(T value, float_tag) {
    cout << "  Processing floating-point: " << value << "\n";
}

template<typename T>
void process(T value) {
    process_impl(value, typename type_tag<T>::type());
}

void tagDispatch() {
    printSection("6. TAG DISPATCH PATTERN");

    cout << "\nTag dispatch based on type:\n";
    process(42);
    process(3.14f);
    process(2.71);
    process(100L);
}

// SFINAE basics
template<typename T>
typename enable_if<is_integral<T>::value, void>::type
print_value(T value) {
    cout << "  Integer value: " << value << "\n";
}

template<typename T>
typename enable_if<is_floating_point<T>::value, void>::type
print_value(T value) {
    cout << "  Floating-point value: " << value << "\n";
}

template<typename T>
typename enable_if<!is_arithmetic<T>::value, void>::type
print_value(T value) {
    cout << "  Non-numeric value: " << value << "\n";
}

void sfinaeBasics() {
    printSection("7. SFINAE BASICS");

    cout << "\nSubstitution Failure Is Not An Error:\n";
    cout << "  Enables function overloading based on type traits\n";

    cout << "\nSFINAE-enabled print_value:\n";
    print_value(42);
    print_value(3.14);
    print_value(string("Hello"));
}

// Type-specific optimizations
template<typename T>
class Vector {
private:
    T* data;
    int size;

public:
    Vector(int s) : size(s) {
        data = new T[size];
    }

    ~Vector() {
        delete[] data;
    }

    void copy_from(const T* source, int count) {
        copy_generic(source, count);
    }

private:
    void copy_generic(const T* source, int count) {
        cout << "  Generic copy (element-by-element)\n";
        for (int i = 0; i < count && i < size; i++) {
            data[i] = source[i];
        }
    }
};

template<>
void Vector<char>::copy_from(const char* source, int count) {
    cout << "  Optimized copy for char (memcpy)\n";
    memcpy(data, source, min(count, size));
}

void typeSpecificOptimizations() {
    printSection("8. TYPE-SPECIFIC OPTIMIZATIONS");

    cout << "\nGeneric copy:\n";
    Vector<int> v1(5);
    int arr1[] = {1, 2, 3, 4, 5};
    v1.copy_from(arr1, 5);

    cout << "\nOptimized copy for POD types:\n";
    Vector<char> v2(10);
    char arr2[] = "Hello";
    v2.copy_from(arr2, 5);
}

// When to use specialization
void whenToUseSpecialization() {
    printSection("9. WHEN TO USE SPECIALIZATION");

    cout << "\nUse full specialization when:\n";
    cout << "  - Completely different implementation needed\n";
    cout << "  - Type-specific behavior required\n";
    cout << "  - Optimization for specific types\n";
    cout << "  - Example: bool, pointers, strings\n";

    cout << "\nUse partial specialization when:\n";
    cout << "  - Pattern-based specialization\n";
    cout << "  - Constraining template parameters\n";
    cout << "  - Example: all pointer types, same-type pairs\n";

    cout << "\nUse tag dispatch when:\n";
    cout << "  - Runtime behavior differs by type category\n";
    cout << "  - Cleaner than multiple specializations\n";
    cout << "  - Example: iterator categories in STL\n";

    cout << "\nUse SFINAE when:\n";
    cout << "  - Conditional template instantiation\n";
    cout << "  - Function overloading based on traits\n";
    cout << "  - Example: enable_if for type constraints\n";

    cout << "\nAvoid specialization when:\n";
    cout << "  - Simple if statements would suffice\n";
    cout << "  - Overloading is clearer\n";
    cout << "  - Maintenance would be complicated\n";
}

// Practical example: type-safe printf
template<typename T>
void type_safe_print(T value) {
    cout << value;
}

template<>
void type_safe_print<bool>(bool value) {
    cout << (value ? "true" : "false");
}

template<>
void type_safe_print<const char*>(const char* value) {
    cout << "\"" << value << "\"";
}

template<typename T, typename... Args>
void print_formatted(T first, Args... args) {
    type_safe_print(first);
    if constexpr (sizeof...(args) > 0) {
        cout << " ";
        print_formatted(args...);
    }
}

void practicalExample() {
    printSection("10. PRACTICAL EXAMPLE");

    cout << "\nType-safe formatted printing:\n";
    cout << "  ";
    print_formatted(42, 3.14, "hello", true, string("world"));
    cout << "\n";

    cout << "\nEach type handled appropriately:\n";
    cout << "  - int: as number\n";
    cout << "  - double: as decimal\n";
    cout << "  - const char*: with quotes\n";
    cout << "  - bool: as true/false\n";
    cout << "  - string: as text\n";
}

int main() {
    cout << "TEMPLATE SPECIALIZATION COMPREHENSIVE GUIDE\n";
    cout << "===========================================\n";

    functionSpecialization();
    classSpecialization();
    partialSpecialization();
    pointerSpecialization();
    memberFunctionSpecialization();
    tagDispatch();
    sfinaeBasics();
    typeSpecificOptimizations();
    whenToUseSpecialization();
    practicalExample();

    printSection("SUMMARY");
    cout << "\nTemplate specialization techniques:\n";
    cout << "- Full specialization: complete override\n";
    cout << "- Partial specialization: pattern-based (classes only)\n";
    cout << "- Member function specialization\n";
    cout << "- Tag dispatch for type categories\n";
    cout << "- SFINAE for conditional compilation\n";
    cout << "- Enables type-specific optimizations\n";
    cout << "- Foundation for type traits and concepts\n";
    cout << "\nSpecialization makes templates more powerful and flexible!\n";

    return 0;
}
