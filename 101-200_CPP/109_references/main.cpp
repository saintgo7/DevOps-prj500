/*
 * Program 109: References in C++
 *
 * Topics Covered:
 * - Lvalue references
 * - Reference initialization
 * - References vs pointers
 * - Const references
 * - References as function parameters
 * - References as return values
 * - Reference to array
 * - Rvalue references (C++11)
 * - std::move and move semantics
 * - Reference collapsing
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o references main.cpp
 */

#include <iostream>
#include <string>
#include <vector>
#include <utility>  // std::move

void demonstrateBasicReferences();
void demonstrateReferencesVsPointers();
void demonstrateConstReferences();
void demonstrateFunctionParameters();
void demonstrateReturnReferences();
void demonstrateRvalueReferences();

int main() {
    std::cout << "=== C++ References ===" << std::endl << std::endl;

    demonstrateBasicReferences();
    demonstrateReferencesVsPointers();
    demonstrateConstReferences();
    demonstrateFunctionParameters();
    demonstrateReturnReferences();
    demonstrateRvalueReferences();

    return 0;
}

void demonstrateBasicReferences() {
    std::cout << "--- Basic References ---" << std::endl;

    int value = 42;
    int& ref = value;  // Reference (alias) to value

    std::cout << "value = " << value << std::endl;
    std::cout << "ref = " << ref << std::endl;
    std::cout << "Addresses: &value = " << &value << ", &ref = " << &ref << std::endl;

    // Modifying through reference
    ref = 100;
    std::cout << "\nAfter ref = 100:" << std::endl;
    std::cout << "value = " << value << " (modified)" << std::endl;

    // References must be initialized
    // int& badRef;  // Error: must be initialized

    // References cannot be reseated
    int other = 200;
    ref = other;  // This assigns value of other to ref (and thus to value)
    std::cout << "\nAfter ref = other (value assignment, not rebinding):" << std::endl;
    std::cout << "value = " << value << ", other = " << other << std::endl;

    std::cout << std::endl;
}

void demonstrateReferencesVsPointers() {
    std::cout << "--- References vs Pointers ---" << std::endl;

    int value = 42;

    // Reference
    int& ref = value;
    // Pointer
    int* ptr = &value;

    std::cout << "Original value = " << value << std::endl;
    std::cout << "ref = " << ref << std::endl;
    std::cout << "*ptr = " << *ptr << std::endl;

    // Similarities:
    std::cout << "\nBoth can modify the original:" << std::endl;
    ref = 100;
    std::cout << "After ref = 100: value = " << value << std::endl;
    *ptr = 200;
    std::cout << "After *ptr = 200: value = " << value << std::endl;

    // Differences:
    std::cout << "\nDifferences:" << std::endl;
    std::cout << "1. References must be initialized, pointers can be null" << std::endl;
    std::cout << "2. References cannot be reseated, pointers can" << std::endl;
    std::cout << "3. No need to dereference references" << std::endl;
    std::cout << "4. References are syntactically cleaner" << std::endl;

    int value2 = 300;
    ptr = &value2;  // Pointer can be reassigned
    std::cout << "*ptr after reassignment = " << *ptr << std::endl;

    std::cout << std::endl;
}

void demonstrateConstReferences() {
    std::cout << "--- Const References ---" << std::endl;

    int value = 42;
    const int& cref = value;

    std::cout << "value = " << value << std::endl;
    std::cout << "cref = " << cref << std::endl;

    // Cannot modify through const reference
    // cref = 100;  // Error!

    // But original can still be modified
    value = 100;
    std::cout << "After value = 100: cref = " << cref << std::endl;

    // Const reference can bind to rvalue
    const int& literalRef = 42;
    std::cout << "literalRef = " << literalRef << std::endl;

    // Const reference extends lifetime of temporary
    const std::string& tempRef = std::string("temporary");
    std::cout << "tempRef = " << tempRef << std::endl;

    std::cout << std::endl;
}

void passByValue(int x) {
    x = 100;
}

void passByReference(int& x) {
    x = 100;
}

void passByConstReference(const int& x) {
    // x = 100;  // Error: cannot modify
    std::cout << "Value: " << x << std::endl;
}

void demonstrateFunctionParameters() {
    std::cout << "--- Function Parameters ---" << std::endl;

    int value = 42;

    std::cout << "Original value: " << value << std::endl;

    passByValue(value);
    std::cout << "After passByValue: " << value << " (unchanged)" << std::endl;

    passByReference(value);
    std::cout << "After passByReference: " << value << " (changed)" << std::endl;

    // Const reference: efficient for large objects
    std::vector<int> largeVector(1000000, 42);
    auto processByValue = [](std::vector<int> vec) {
        // Expensive copy!
        return vec.size();
    };

    auto processByConstRef = [](const std::vector<int>& vec) {
        // No copy!
        return vec.size();
    };

    std::cout << "\nProcessing large vector:" << std::endl;
    std::cout << "By const reference (efficient): " << processByConstRef(largeVector) << std::endl;

    std::cout << std::endl;
}

int& getElement(int arr[], int index) {
    return arr[index];
}

int globalValue = 42;

int& getGlobal() {
    return globalValue;
}

void demonstrateReturnReferences() {
    std::cout << "--- Return References ---" << std::endl;

    int arr[] = {10, 20, 30, 40, 50};

    std::cout << "Array: ";
    for (int val : arr) std::cout << val << " ";
    std::cout << std::endl;

    // Modify through returned reference
    getElement(arr, 2) = 300;

    std::cout << "After getElement(arr, 2) = 300: ";
    for (int val : arr) std::cout << val << " ";
    std::cout << std::endl;

    // Chaining
    getElement(arr, 0) = getElement(arr, 4);
    std::cout << "After arr[0] = arr[4]: ";
    for (int val : arr) std::cout << val << " ";
    std::cout << std::endl;

    // Global variable
    std::cout << "\nglobalValue = " << globalValue << std::endl;
    getGlobal() = 100;
    std::cout << "After getGlobal() = 100: globalValue = " << globalValue << std::endl;

    // WARNING: Never return reference to local variable
    // auto badFunction = []() -> int& {
    //     int local = 42;
    //     return local;  // Dangling reference!
    // };

    std::cout << std::endl;
}

void demonstrateRvalueReferences() {
    std::cout << "--- Rvalue References (C++11) ---" << std::endl;

    // Lvalue: has a name, can take address
    int lvalue = 42;
    int& lref = lvalue;  // Lvalue reference

    // Rvalue: temporary, no name, cannot take address
    // int& badRef = 42;  // Error: cannot bind lvalue ref to rvalue
    const int& okRef = 42;  // OK: const lvalue ref can bind to rvalue

    // Rvalue reference
    int&& rref = 42;  // Binds to rvalue
    std::cout << "rref = " << rref << std::endl;

    // Can modify rvalue reference
    rref = 100;
    std::cout << "After rref = 100: rref = " << rref << std::endl;

    // std::move converts lvalue to rvalue
    std::string str1 = "Hello";
    std::string str2 = std::move(str1);  // Move, not copy

    std::cout << "\nAfter move:" << std::endl;
    std::cout << "str1: \"" << str1 << "\" (moved-from state)" << std::endl;
    std::cout << "str2: \"" << str2 << "\"" << std::endl;

    // Move semantics with vector
    std::vector<int> vec1 = {1, 2, 3, 4, 5};
    std::cout << "\nvec1 size before move: " << vec1.size() << std::endl;

    std::vector<int> vec2 = std::move(vec1);
    std::cout << "vec1 size after move: " << vec1.size() << std::endl;
    std::cout << "vec2 size: " << vec2.size() << std::endl;

    // Perfect forwarding example
    auto processValue = [](int&& val) {
        std::cout << "Processing rvalue: " << val << std::endl;
    };

    auto processRef = [](int& val) {
        std::cout << "Processing lvalue: " << val << std::endl;
    };

    int x = 10;
    processRef(x);  // Lvalue
    processValue(std::move(x));  // Rvalue after move

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Prefer references over pointers when possible
 * 2. Use const references for large objects passed to functions
 * 3. Never return reference to local variable
 * 4. Use references to avoid unnecessary copies
 * 5. Understand lvalue vs rvalue references
 * 6. Use std::move for explicit move semantics
 * 7. Be careful when returning references
 * 8. Use auto&& for universal references in templates
 * 9. References make code more readable than pointers
 * 10. Use references for operator overloading
 */
