# Program 108: Pointers in C++

## Description
Comprehensive exploration of pointers in C++ covering pointer basics, pointer arithmetic, pointer types, null pointers, void pointers, pointer to pointer, function pointers, and dynamic memory allocation. This program demonstrates fundamental pointer concepts essential for memory management and advanced C++ programming.

## Learning Objectives
- Understand pointer fundamentals and memory addresses
- Master pointer declaration and initialization
- Work with pointer arithmetic and dereferencing
- Use different pointer types (null, void, function pointers)
- Understand pointer-to-pointer (double pointers)
- Apply pointers with arrays and functions
- Practice dynamic memory allocation

## Features
- Basic pointer operations (declaration, initialization, dereferencing)
- Pointer arithmetic demonstrations
- Null pointer and nullptr (C++11)
- Void pointers and type casting
- Pointer to pointer (multilevel indirection)
- Pointers and arrays relationship
- Function pointers and callbacks
- Dynamic memory allocation with new/delete
- Pointer best practices and common pitfalls

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/108_pointers
g++ -std=c++20 -Wall -Wextra -o pointers main.cpp
```

### Execution
```bash
./pointers
```

## Key Concepts

### 1. Pointer Basics
```cpp
// Declaration
int* ptr;        // Pointer to int
double* dptr;    // Pointer to double
char* cptr;      // Pointer to char

// Initialization
int x = 10;
int* ptr = &x;   // Address-of operator (&)

// Dereferencing (access value at address)
std::cout << *ptr;  // 10
*ptr = 20;          // Modify through pointer
std::cout << x;     // 20
```

### 2. Null Pointers
```cpp
// C-style null pointer (avoid)
int* ptr1 = NULL;

// Modern C++11 nullptr
int* ptr2 = nullptr;

// Check before use
if (ptr2 != nullptr) {
    *ptr2 = 10;
}

// Safe practice
int* ptr3 = nullptr;
// ... later ...
if (ptr3) {  // Implicit check
    *ptr3 = 5;
}
```

### 3. Pointer Arithmetic
```cpp
int arr[] = {10, 20, 30, 40, 50};
int* ptr = arr;

// Moving through array
ptr++;           // Points to arr[1]
ptr += 2;        // Points to arr[3]
ptr--;           // Points to arr[2]

// Accessing with arithmetic
*(ptr + 1);      // Access next element

// Pointer difference
int* start = arr;
int* end = arr + 5;
int size = end - start;  // 5
```

### 4. Pointers and Arrays
```cpp
int arr[] = {1, 2, 3, 4, 5};

// Array name is pointer to first element
int* ptr = arr;  // Same as &arr[0]

// These are equivalent:
arr[2]      // 3
ptr[2]      // 3
*(arr + 2)  // 3
*(ptr + 2)  // 3
```

### 5. Pointer to Pointer
```cpp
int x = 10;
int* ptr = &x;       // Pointer to int
int** pptr = &ptr;   // Pointer to pointer

// Access value
std::cout << **pptr;  // 10

// Modify through double pointer
**pptr = 20;
std::cout << x;       // 20

// Use case: 2D arrays, arrays of strings
char* names[] = {"Alice", "Bob", "Charlie"};
char** namePtr = names;
```

### 6. Void Pointers
```cpp
void* vptr;   // Generic pointer

int x = 10;
vptr = &x;    // Can point to any type

// Must cast to use
int* iptr = static_cast<int*>(vptr);
std::cout << *iptr;  // 10

// Useful for generic functions
void printBytes(void* ptr, size_t size) {
    unsigned char* bytePtr = static_cast<unsigned char*>(ptr);
    for (size_t i = 0; i < size; i++) {
        std::cout << std::hex << (int)bytePtr[i] << " ";
    }
}
```

### 7. Function Pointers
```cpp
// Function pointer declaration
int (*funcPtr)(int, int);

// Assign function to pointer
int add(int a, int b) { return a + b; }
funcPtr = &add;  // or just: funcPtr = add;

// Call through pointer
int result = funcPtr(5, 3);  // 8

// Callback pattern
void processArray(int arr[], int size, int (*operation)(int)) {
    for (int i = 0; i < size; i++) {
        arr[i] = operation(arr[i]);
    }
}

int square(int x) { return x * x; }
int numbers[] = {1, 2, 3, 4, 5};
processArray(numbers, 5, square);
```

### 8. Dynamic Memory Allocation
```cpp
// Allocate single value
int* ptr = new int;
*ptr = 42;
delete ptr;      // Must delete!
ptr = nullptr;   // Good practice

// Allocate with initialization
int* ptr2 = new int(100);
delete ptr2;

// Allocate array
int size = 5;
int* arr = new int[size];
for (int i = 0; i < size; i++) {
    arr[i] = i * 10;
}
delete[] arr;    // Use delete[] for arrays
arr = nullptr;

// Check allocation success
int* largeArray = new(std::nothrow) int[1000000000];
if (largeArray == nullptr) {
    std::cerr << "Allocation failed!\n";
}
```

### 9. Const Pointers
```cpp
int x = 10, y = 20;

// Pointer to const (can't modify value)
const int* ptr1 = &x;
// *ptr1 = 20;  // Error!
ptr1 = &y;      // OK

// Const pointer (can't change address)
int* const ptr2 = &x;
*ptr2 = 30;     // OK
// ptr2 = &y;   // Error!

// Const pointer to const
const int* const ptr3 = &x;
// *ptr3 = 40;  // Error!
// ptr3 = &y;   // Error!
```

## Best Practices
1. **Always initialize pointers** - Use nullptr for uninitialized pointers
2. **Check for nullptr** before dereferencing
3. **Set to nullptr after delete** to avoid dangling pointers
4. **Match new with delete** and new[] with delete[]
5. **Use smart pointers** (modern C++) instead of raw pointers when possible
6. **Avoid pointer arithmetic** unless necessary (use iterators instead)
7. **Be careful with pointer scope** - don't return pointers to local variables
8. **Use const correctness** with pointers
9. **Prefer references** over pointers when ownership isn't transferred
10. **Document pointer ownership** clearly in APIs

## Common Pitfalls
- **Memory leaks**: Forgetting to delete allocated memory
- **Dangling pointers**: Using pointers after deletion
- **Double deletion**: Deleting same memory twice
- **Wild pointers**: Using uninitialized pointers
- **Array bounds**: Pointer arithmetic beyond array bounds
- **Mixing new/delete**: Using delete on new[] or vice versa

## Resources and References
- [cppreference.com - Pointers](https://en.cppreference.com/w/cpp/language/pointer)
- [cppreference.com - nullptr](https://en.cppreference.com/w/cpp/language/nullptr)
- [C++ Core Guidelines - Pointers](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r-resource-management)

## Navigation
- **Previous Program**: [107 - Arrays](../107_arrays/README.md)
- **Next Program**: [109 - References](../109_references/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
