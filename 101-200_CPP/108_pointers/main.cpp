/*
 * Program 108: Pointers in C++
 *
 * Topics Covered:
 * - Pointer basics and declaration
 * - Address-of operator (&) and dereference operator (*)
 * - Null pointers (nullptr in C++11)
 * - Pointer arithmetic
 * - Pointers and arrays
 * - Pointer to pointer (double pointers)
 * - Void pointers
 * - Function pointers
 * - Const pointers and pointers to const
 * - Dynamic memory allocation
 * - Common pointer pitfalls
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o pointers main.cpp
 */

#include <iostream>
#include <cstring>

void demonstratePointerBasics();
void demonstrateNullPointers();
void demonstratePointerArithmetic();
void demonstratePointersAndArrays();
void demonstrateDoublePointers();
void demonstrateVoidPointers();
void demonstrateFunctionPointers();
void demonstrateConstPointers();
void demonstrateDynamicMemory();
void demonstrateCommonPatterns();

int main() {
    std::cout << "=== C++ Pointers ===" << std::endl;
    std::cout << std::endl;

    demonstratePointerBasics();
    demonstrateNullPointers();
    demonstratePointerArithmetic();
    demonstratePointersAndArrays();
    demonstrateDoublePointers();
    demonstrateVoidPointers();
    demonstrateFunctionPointers();
    demonstrateConstPointers();
    demonstrateDynamicMemory();
    demonstrateCommonPatterns();

    return 0;
}

void demonstratePointerBasics() {
    std::cout << "--- Pointer Basics ---" << std::endl;

    int value = 42;
    int* ptr;  // Pointer declaration

    // Address-of operator (&)
    ptr = &value;  // ptr now holds the address of value

    std::cout << "value = " << value << std::endl;
    std::cout << "Address of value (&value) = " << &value << std::endl;
    std::cout << "ptr = " << ptr << std::endl;
    std::cout << "Dereferenced ptr (*ptr) = " << *ptr << std::endl;

    // Modifying through pointer
    *ptr = 100;
    std::cout << "\nAfter *ptr = 100:" << std::endl;
    std::cout << "value = " << value << std::endl;
    std::cout << "*ptr = " << *ptr << std::endl;

    // Multiple pointers to same variable
    int* ptr2 = &value;
    std::cout << "\nMultiple pointers:" << std::endl;
    std::cout << "*ptr = " << *ptr << ", *ptr2 = " << *ptr2 << std::endl;

    *ptr2 = 200;
    std::cout << "After *ptr2 = 200:" << std::endl;
    std::cout << "value = " << value << ", *ptr = " << *ptr << std::endl;

    std::cout << std::endl;
}

void demonstrateNullPointers() {
    std::cout << "--- Null Pointers ---" << std::endl;

    // nullptr (C++11) - preferred
    int* ptr1 = nullptr;
    std::cout << "ptr1 = " << ptr1 << " (nullptr)" << std::endl;

    // NULL (C-style, avoid in C++)
    int* ptr2 = NULL;
    std::cout << "ptr2 = " << ptr2 << " (NULL)" << std::endl;

    // 0 (old style, avoid)
    int* ptr3 = 0;
    std::cout << "ptr3 = " << ptr3 << " (0)" << std::endl;

    // Checking for null
    if (ptr1 == nullptr) {
        std::cout << "ptr1 is null" << std::endl;
    }

    if (!ptr2) {
        std::cout << "ptr2 is null (using implicit bool conversion)" << std::endl;
    }

    // Safe dereferencing
    int value = 42;
    int* ptr4 = &value;

    if (ptr4 != nullptr) {
        std::cout << "Safe to dereference: *ptr4 = " << *ptr4 << std::endl;
    }

    // Danger: dereferencing null pointer
    // *ptr1 = 10;  // Undefined behavior! Segmentation fault

    std::cout << std::endl;
}

void demonstratePointerArithmetic() {
    std::cout << "--- Pointer Arithmetic ---" << std::endl;

    int arr[] = {10, 20, 30, 40, 50};
    int* ptr = arr;  // Points to first element

    std::cout << "Array: ";
    for (int i = 0; i < 5; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    // Pointer increment
    std::cout << "\nPointer increment:" << std::endl;
    std::cout << "*ptr = " << *ptr << std::endl;
    ptr++;
    std::cout << "After ptr++: *ptr = " << *ptr << std::endl;
    ptr++;
    std::cout << "After ptr++: *ptr = " << *ptr << std::endl;

    // Pointer decrement
    ptr--;
    std::cout << "After ptr--: *ptr = " << *ptr << std::endl;

    // Pointer addition
    ptr = arr;  // Reset to first element
    std::cout << "\nPointer addition:" << std::endl;
    std::cout << "*(ptr + 0) = " << *(ptr + 0) << std::endl;
    std::cout << "*(ptr + 1) = " << *(ptr + 1) << std::endl;
    std::cout << "*(ptr + 2) = " << *(ptr + 2) << std::endl;
    std::cout << "*(ptr + 3) = " << *(ptr + 3) << std::endl;
    std::cout << "*(ptr + 4) = " << *(ptr + 4) << std::endl;

    // Pointer subtraction
    int* ptr1 = &arr[4];
    int* ptr2 = &arr[1];
    std::cout << "\nPointer subtraction:" << std::endl;
    std::cout << "ptr1 - ptr2 = " << (ptr1 - ptr2) << " elements" << std::endl;

    // Address differences
    std::cout << "\nAddress differences:" << std::endl;
    for (int i = 0; i < 5; i++) {
        std::cout << "&arr[" << i << "] = " << &arr[i] << std::endl;
    }

    std::cout << std::endl;
}

void demonstratePointersAndArrays() {
    std::cout << "--- Pointers and Arrays ---" << std::endl;

    int arr[] = {1, 2, 3, 4, 5};

    // Array name is a pointer to first element
    std::cout << "arr = " << arr << std::endl;
    std::cout << "&arr[0] = " << &arr[0] << std::endl;
    std::cout << "arr and &arr[0] are " << (arr == &arr[0] ? "equal" : "not equal") << std::endl;

    // Using pointers to traverse array
    std::cout << "\nTraversing with pointer:" << std::endl;
    int* ptr = arr;
    for (int i = 0; i < 5; i++) {
        std::cout << "ptr[" << i << "] = " << ptr[i] << std::endl;
    }

    // Array subscript is pointer arithmetic
    std::cout << "\nArray subscript vs pointer arithmetic:" << std::endl;
    std::cout << "arr[2] = " << arr[2] << std::endl;
    std::cout << "*(arr + 2) = " << *(arr + 2) << std::endl;
    std::cout << "2[arr] = " << 2[arr] << " (weird but valid!)" << std::endl;

    // Pointer-based iteration
    std::cout << "\nPointer-based iteration:" << std::endl;
    for (int* p = arr; p < arr + 5; p++) {
        std::cout << *p << " ";
    }
    std::cout << std::endl;

    std::cout << std::endl;
}

void demonstrateDoublePointers() {
    std::cout << "--- Pointer to Pointer (Double Pointers) ---" << std::endl;

    int value = 42;
    int* ptr = &value;
    int** ptrToPtr = &ptr;

    std::cout << "value = " << value << std::endl;
    std::cout << "&value = " << &value << std::endl;
    std::cout << std::endl;

    std::cout << "ptr = " << ptr << std::endl;
    std::cout << "*ptr = " << *ptr << std::endl;
    std::cout << "&ptr = " << &ptr << std::endl;
    std::cout << std::endl;

    std::cout << "ptrToPtr = " << ptrToPtr << std::endl;
    std::cout << "*ptrToPtr = " << *ptrToPtr << " (same as ptr)" << std::endl;
    std::cout << "**ptrToPtr = " << **ptrToPtr << " (same as value)" << std::endl;

    // Modifying through double pointer
    **ptrToPtr = 100;
    std::cout << "\nAfter **ptrToPtr = 100:" << std::endl;
    std::cout << "value = " << value << std::endl;

    // 2D array with pointers
    std::cout << "\n2D array with pointers:" << std::endl;
    int rows = 3;
    int cols = 4;
    int** matrix = new int*[rows];
    for (int i = 0; i < rows; i++) {
        matrix[i] = new int[cols];
    }

    // Fill and print
    int counter = 1;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = counter++;
        }
    }

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }

    // Cleanup
    for (int i = 0; i < rows; i++) {
        delete[] matrix[i];
    }
    delete[] matrix;

    std::cout << std::endl;
}

void demonstrateVoidPointers() {
    std::cout << "--- Void Pointers ---" << std::endl;

    int intVal = 42;
    double doubleVal = 3.14;
    char charVal = 'A';

    // void* can point to any type
    void* voidPtr;

    voidPtr = &intVal;
    std::cout << "voidPtr points to int: " << *(static_cast<int*>(voidPtr)) << std::endl;

    voidPtr = &doubleVal;
    std::cout << "voidPtr points to double: " << *(static_cast<double*>(voidPtr)) << std::endl;

    voidPtr = &charVal;
    std::cout << "voidPtr points to char: " << *(static_cast<char*>(voidPtr)) << std::endl;

    // Cannot dereference void* directly
    // std::cout << *voidPtr << std::endl;  // Error!

    // Must cast to appropriate type first
    char* charPtr = static_cast<char*>(voidPtr);
    std::cout << "After casting to char*: " << *charPtr << std::endl;

    std::cout << std::endl;
}

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

void demonstrateFunctionPointers() {
    std::cout << "--- Function Pointers ---" << std::endl;

    // Function pointer declaration
    int (*operation)(int, int);

    // Assign function to pointer
    operation = add;
    std::cout << "add(5, 3) = " << operation(5, 3) << std::endl;

    operation = subtract;
    std::cout << "subtract(5, 3) = " << operation(5, 3) << std::endl;

    operation = multiply;
    std::cout << "multiply(5, 3) = " << operation(5, 3) << std::endl;

    // Array of function pointers
    int (*operations[3])(int, int) = {add, subtract, multiply};
    const char* names[] = {"add", "subtract", "multiply"};

    std::cout << "\nUsing function pointer array:" << std::endl;
    for (int i = 0; i < 3; i++) {
        std::cout << names[i] << "(10, 5) = " << operations[i](10, 5) << std::endl;
    }

    // Callback pattern
    auto performOperation = [](int a, int b, int (*op)(int, int)) {
        return op(a, b);
    };

    std::cout << "\nCallback pattern:" << std::endl;
    std::cout << "Result: " << performOperation(7, 3, add) << std::endl;

    std::cout << std::endl;
}

void demonstrateConstPointers() {
    std::cout << "--- Const Pointers ---" << std::endl;

    int value1 = 10;
    int value2 = 20;

    // Pointer to const (cannot modify value through pointer)
    const int* ptr1 = &value1;
    std::cout << "Pointer to const: *ptr1 = " << *ptr1 << std::endl;
    // *ptr1 = 100;  // Error: cannot modify
    ptr1 = &value2;  // OK: can change what it points to
    std::cout << "After reassignment: *ptr1 = " << *ptr1 << std::endl;

    // Const pointer (cannot change what it points to)
    int* const ptr2 = &value1;
    std::cout << "\nConst pointer: *ptr2 = " << *ptr2 << std::endl;
    *ptr2 = 100;  // OK: can modify value
    std::cout << "After modification: *ptr2 = " << *ptr2 << std::endl;
    // ptr2 = &value2;  // Error: cannot reassign pointer

    // Const pointer to const (cannot modify value or reassign pointer)
    const int* const ptr3 = &value1;
    std::cout << "\nConst pointer to const: *ptr3 = " << *ptr3 << std::endl;
    // *ptr3 = 200;  // Error: cannot modify value
    // ptr3 = &value2;  // Error: cannot reassign pointer

    std::cout << std::endl;
}

void demonstrateDynamicMemory() {
    std::cout << "--- Dynamic Memory Allocation ---" << std::endl;

    // Single variable
    int* ptr1 = new int;
    *ptr1 = 42;
    std::cout << "Dynamically allocated int: " << *ptr1 << std::endl;
    delete ptr1;  // Free memory

    // Single variable with initialization
    int* ptr2 = new int(100);
    std::cout << "Initialized allocation: " << *ptr2 << std::endl;
    delete ptr2;

    // Array allocation
    int size = 5;
    int* arr = new int[size];
    for (int i = 0; i < size; i++) {
        arr[i] = i * 10;
    }

    std::cout << "Dynamically allocated array: ";
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    delete[] arr;  // Note: delete[] for arrays

    // Initialized array (C++11)
    int* arr2 = new int[5]{1, 2, 3, 4, 5};
    std::cout << "Initialized dynamic array: ";
    for (int i = 0; i < 5; i++) {
        std::cout << arr2[i] << " ";
    }
    std::cout << std::endl;
    delete[] arr2;

    std::cout << std::endl;
}

void demonstrateCommonPatterns() {
    std::cout << "--- Common Pointer Patterns ---" << std::endl;

    // 1. Swapping with pointers
    int a = 10, b = 20;
    std::cout << "Before swap: a = " << a << ", b = " << b << std::endl;

    int* ptr1 = &a;
    int* ptr2 = &b;
    int temp = *ptr1;
    *ptr1 = *ptr2;
    *ptr2 = temp;

    std::cout << "After swap: a = " << a << ", b = " << b << std::endl;

    // 2. Returning multiple values
    auto divmod = [](int dividend, int divisor, int* quotient, int* remainder) {
        *quotient = dividend / divisor;
        *remainder = dividend % divisor;
    };

    int q, r;
    divmod(17, 5, &q, &r);
    std::cout << "\n17 / 5 = " << q << " remainder " << r << std::endl;

    // 3. Linked list node (basic example)
    struct Node {
        int data;
        Node* next;
    };

    Node* head = new Node{1, nullptr};
    head->next = new Node{2, nullptr};
    head->next->next = new Node{3, nullptr};

    std::cout << "\nLinked list: ";
    Node* current = head;
    while (current != nullptr) {
        std::cout << current->data << " ";
        current = current->next;
    }
    std::cout << std::endl;

    // Cleanup
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Always initialize pointers (use nullptr for null)
 * 2. Check for nullptr before dereferencing
 * 3. Use delete for new, delete[] for new[]
 * 4. Avoid raw pointers; prefer smart pointers (unique_ptr, shared_ptr)
 * 5. Don't return pointers to local variables
 * 6. Be careful with pointer arithmetic
 * 7. Use const correctness with pointers
 * 8. Avoid void* unless necessary (lose type safety)
 * 9. Watch out for dangling pointers
 * 10. Set pointers to nullptr after delete
 * 11. Prefer references over pointers when possible
 * 12. Use RAII to manage resources
 */
