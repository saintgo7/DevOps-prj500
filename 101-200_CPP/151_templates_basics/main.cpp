/*
 * Program 151: Templates Basics
 *
 * Demonstrates:
 * - Template syntax and concepts
 * - Template parameters (type and non-type)
 * - Template instantiation
 * - Template argument deduction
 * - Default template arguments
 * - Template compilation model
 * - typename vs class keyword
 * - Common template patterns
 * - Template best practices
 */

#include <iostream>
#include <vector>
#include <string>
#include <typeinfo>
#include <type_traits>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic function template
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

// Template with multiple type parameters
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

// Class template
template<typename T>
class Box {
private:
    T value;
public:
    Box(T v) : value(v) {}

    T getValue() const { return value; }
    void setValue(T v) { value = v; }

    void print() const {
        cout << "  Box contains: " << value << "\n";
    }
};

// Template basics
void templateBasics() {
    printSection("1. TEMPLATE BASICS");

    cout << "\nFunction template:\n";
    cout << "  maximum(10, 20) = " << maximum(10, 20) << "\n";
    cout << "  maximum(3.5, 2.1) = " << maximum(3.5, 2.1) << "\n";
    cout << "  maximum('a', 'z') = " << maximum('a', 'z') << "\n";
    cout << "  maximum(string(\"hello\"), string(\"world\")) = "
         << maximum(string("hello"), string("world")) << "\n";

    cout << "\nClass template:\n";
    Box<int> intBox(42);
    Box<string> stringBox("Hello");
    Box<double> doubleBox(3.14);

    intBox.print();
    stringBox.print();
    doubleBox.print();

    cout << "\nMultiple type parameters:\n";
    cout << "  add(10, 3.5) = " << add(10, 3.5) << "\n";
    cout << "  add(3.5, 10) = " << add(3.5, 10) << "\n";
}

// Template argument deduction
template<typename T>
void printType(T value) {
    cout << "  Value: " << value << ", Type: " << typeid(T).name() << "\n";
}

template<typename T>
void printArray(T arr[], int size) {
    cout << "  Array: ";
    for (int i = 0; i < size; i++) {
        cout << arr[i] << " ";
    }
    cout << "\n";
}

void templateDeduction() {
    printSection("2. TEMPLATE ARGUMENT DEDUCTION");

    cout << "\nAutomatic type deduction:\n";
    printType(42);
    printType(3.14);
    printType("Hello");
    printType(string("World"));

    cout << "\nExplicit template arguments:\n";
    printType<int>(42);
    printType<double>(3.14);

    cout << "\nArray template deduction:\n";
    int arr[] = {1, 2, 3, 4, 5};
    printArray(arr, 5);

    cout << "\nMixed deduction and explicit:\n";
    auto result1 = add<int>(10, 3.5);  // T=int, U deduced as double
    cout << "  add<int>(10, 3.5) = " << result1 << "\n";
}

// Non-type template parameters
template<typename T, int Size>
class Array {
private:
    T data[Size];
public:
    Array() {
        for (int i = 0; i < Size; i++) {
            data[i] = T();
        }
    }

    T& operator[](int index) { return data[index]; }
    const T& operator[](int index) const { return data[index]; }

    int size() const { return Size; }

    void print() const {
        cout << "  Array[" << Size << "]: ";
        for (int i = 0; i < Size; i++) {
            cout << data[i] << " ";
        }
        cout << "\n";
    }
};

template<int N>
int factorial() {
    return N * factorial<N-1>();
}

template<>
int factorial<0>() {
    return 1;
}

void nonTypeParameters() {
    printSection("3. NON-TYPE TEMPLATE PARAMETERS");

    cout << "\nArray with size as template parameter:\n";
    Array<int, 5> arr1;
    for (int i = 0; i < arr1.size(); i++) {
        arr1[i] = i * 10;
    }
    arr1.print();

    Array<double, 3> arr2;
    for (int i = 0; i < arr2.size(); i++) {
        arr2[i] = i * 1.5;
    }
    arr2.print();

    cout << "\nCompile-time factorial:\n";
    cout << "  factorial<5>() = " << factorial<5>() << "\n";
    cout << "  factorial<10>() = " << factorial<10>() << "\n";

    cout << "\nCompile-time constants:\n";
    constexpr int fact5 = factorial<5>();
    cout << "  constexpr fact5 = " << fact5 << "\n";
}

// Default template arguments
template<typename T = int, int Size = 10>
class Container {
private:
    T data[Size];
    int count;
public:
    Container() : count(0) {}

    void add(T value) {
        if (count < Size) {
            data[count++] = value;
        }
    }

    void print() const {
        cout << "  Container[" << Size << "]: ";
        for (int i = 0; i < count; i++) {
            cout << data[i] << " ";
        }
        cout << "\n";
    }
};

template<typename T, typename U = T>
U convert(T value) {
    return static_cast<U>(value);
}

void defaultTemplateArguments() {
    printSection("4. DEFAULT TEMPLATE ARGUMENTS");

    cout << "\nDefault type and size:\n";
    Container<> c1;  // int, size 10
    c1.add(1);
    c1.add(2);
    c1.add(3);
    c1.print();

    cout << "\nCustom type, default size:\n";
    Container<double> c2;  // double, size 10
    c2.add(1.1);
    c2.add(2.2);
    c2.print();

    cout << "\nCustom type and size:\n";
    Container<string, 5> c3;
    c3.add("hello");
    c3.add("world");
    c3.print();

    cout << "\nFunction template with default:\n";
    cout << "  convert(3.14) = " << convert(3.14) << "\n";
    cout << "  convert<double, int>(3.14) = " << convert<double, int>(3.14) << "\n";
}

// typename vs class
template<typename T>  // typename keyword
class TypenameExample {
public:
    using value_type = T;
    typename T::value_type getValue(const T& container) {
        return container.front();
    }
};

template<class T>  // class keyword (equivalent)
class ClassExample {
public:
    T value;
};

void typenameVsClass() {
    printSection("5. TYPENAME vs CLASS");

    cout << "\nNo functional difference between:\n";
    cout << "  template<typename T> and template<class T>\n";
    cout << "\nBut 'typename' is preferred for clarity\n";

    cout << "\ntypename for dependent types:\n";
    cout << "  typename T::value_type  // Tells compiler it's a type\n";
    cout << "  Required when T is a template parameter\n";

    vector<int> v = {1, 2, 3};
    TypenameExample<vector<int>> example;
    cout << "  First element: " << example.getValue(v) << "\n";
}

// Template specialization preview
template<typename T>
class Printer {
public:
    void print(const T& value) {
        cout << "  Generic: " << value << "\n";
    }
};

template<>
class Printer<bool> {
public:
    void print(const bool& value) {
        cout << "  Boolean: " << (value ? "true" : "false") << "\n";
    }
};

void templateSpecializationPreview() {
    printSection("6. TEMPLATE SPECIALIZATION (PREVIEW)");

    cout << "\nGeneric template:\n";
    Printer<int> intPrinter;
    intPrinter.print(42);

    Printer<string> stringPrinter;
    stringPrinter.print("Hello");

    cout << "\nSpecialized for bool:\n";
    Printer<bool> boolPrinter;
    boolPrinter.print(true);
    boolPrinter.print(false);
}

// Template compilation model
void templateCompilationModel() {
    printSection("7. TEMPLATE COMPILATION MODEL");

    cout << "\nTemplate compilation:\n";
    cout << "  1. Templates are NOT compiled when defined\n";
    cout << "  2. Compiled when instantiated with specific types\n";
    cout << "  3. Must be visible at point of instantiation\n";
    cout << "  4. Usually defined in header files\n";

    cout << "\nInstantiation:\n";
    cout << "  Implicit: maximum(10, 20) instantiates maximum<int>\n";
    cout << "  Explicit: maximum<double>(10, 20)\n";

    cout << "\nExplicit instantiation:\n";
    cout << "  template class Box<int>;  // Force instantiation\n";
    cout << "  template int maximum<int>(int, int);\n";

    cout << "\nTwo-phase lookup:\n";
    cout << "  Phase 1: Non-dependent names resolved at definition\n";
    cout << "  Phase 2: Dependent names resolved at instantiation\n";
}

// Common template patterns
template<typename T>
class RAII_Wrapper {
private:
    T* ptr;
public:
    RAII_Wrapper(T* p) : ptr(p) {}
    ~RAII_Wrapper() { delete ptr; }

    T& operator*() { return *ptr; }
    T* operator->() { return ptr; }

    // Prevent copying
    RAII_Wrapper(const RAII_Wrapper&) = delete;
    RAII_Wrapper& operator=(const RAII_Wrapper&) = delete;
};

template<typename T>
struct Pair {
    T first;
    T second;

    Pair(T f, T s) : first(f), second(s) {}
};

// Template template parameter
template<template<typename> class Container, typename T>
class Adapter {
private:
    Container<T> data;
public:
    void add(T value) {
        data.push_back(value);
    }

    void print() const {
        cout << "  ";
        for (const auto& x : data) {
            cout << x << " ";
        }
        cout << "\n";
    }
};

void commonTemplatePatterns() {
    printSection("8. COMMON TEMPLATE PATTERNS");

    cout << "\nRAII wrapper:\n";
    RAII_Wrapper<int> wrapper(new int(42));
    cout << "  Value: " << *wrapper << "\n";

    cout << "\nPair template:\n";
    Pair<int> p1(10, 20);
    cout << "  Pair: (" << p1.first << ", " << p1.second << ")\n";

    Pair<string> p2("hello", "world");
    cout << "  Pair: (" << p2.first << ", " << p2.second << ")\n";

    cout << "\nTemplate template parameter:\n";
    Adapter<vector, int> adapter;
    adapter.add(1);
    adapter.add(2);
    adapter.add(3);
    adapter.print();
}

// Type traits preview
void typeTraitsPreview() {
    printSection("9. TYPE TRAITS (PREVIEW)");

    cout << "\nType information at compile time:\n";
    cout << "  is_integral<int>: " << is_integral<int>::value << "\n";
    cout << "  is_integral<double>: " << is_integral<double>::value << "\n";
    cout << "  is_floating_point<double>: " << is_floating_point<double>::value << "\n";
    cout << "  is_pointer<int*>: " << is_pointer<int*>::value << "\n";
    cout << "  is_same<int, int>: " << is_same<int, int>::value << "\n";
    cout << "  is_same<int, double>: " << is_same<int, double>::value << "\n";

    cout << "\nType transformations:\n";
    cout << "  remove_const<const int>::type is int\n";
    cout << "  add_pointer<int>::type is int*\n";
    cout << "  remove_reference<int&>::type is int\n";
}

// Best practices
void bestPractices() {
    printSection("10. TEMPLATE BEST PRACTICES");

    cout << "\n1. Use templates for generic code:\n";
    cout << "   - Write once, works for multiple types\n";
    cout << "   - Type-safe and efficient\n";

    cout << "\n2. Prefer typename over class:\n";
    cout << "   template<typename T> (more clear)\n";

    cout << "\n3. Use const and references:\n";
    cout << "   template<typename T>\n";
    cout << "   void func(const T& value);  // Avoid copying\n";

    cout << "\n4. Provide meaningful constraints:\n";
    cout << "   - Use static_assert for compile-time checks\n";
    cout << "   - Document template requirements\n";

    cout << "\n5. Define templates in headers:\n";
    cout << "   - Template definitions must be visible\n";
    cout << "   - Use include guards or #pragma once\n";

    cout << "\n6. Use explicit instantiation when needed:\n";
    cout << "   - Reduce compilation time\n";
    cout << "   - Control which types are supported\n";

    cout << "\n7. Consider template aliases:\n";
    cout << "   template<typename T>\n";
    cout << "   using Vec = vector<T>;\n";

    cout << "\n8. Use SFINAE or concepts for constraints:\n";
    cout << "   - Enable/disable based on type properties\n";
    cout << "   - Better error messages\n";
}

int main() {
    cout << "TEMPLATES BASICS COMPREHENSIVE GUIDE\n";
    cout << "====================================\n";

    templateBasics();
    templateDeduction();
    nonTypeParameters();
    defaultTemplateArguments();
    typenameVsClass();
    templateSpecializationPreview();
    templateCompilationModel();
    commonTemplatePatterns();
    typeTraitsPreview();
    bestPractices();

    printSection("SUMMARY");
    cout << "\nTemplate fundamentals:\n";
    cout << "- Generic programming mechanism\n";
    cout << "- Compile-time code generation\n";
    cout << "- Type and non-type parameters\n";
    cout << "- Automatic type deduction\n";
    cout << "- Default arguments supported\n";
    cout << "- Defined in headers (visibility required)\n";
    cout << "- Foundation for modern C++ features\n";
    cout << "\nTemplates enable type-safe, reusable code!\n";

    return 0;
}
