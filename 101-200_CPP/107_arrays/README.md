# Program 107: Arrays in C++

## Description
Comprehensive exploration of arrays in C++ covering C-style static arrays, multidimensional arrays, std::array (C++11), array algorithms, and common array operations. This program demonstrates both traditional and modern approaches to working with arrays.

## Learning Objectives
- Master static array declaration and initialization
- Understand array access and memory layout
- Work with multidimensional arrays
- Use std::array for type-safe arrays (C++11)
- Apply STL algorithms to arrays
- Understand arrays and pointers relationship

## Features
- Basic array operations (declaration, initialization, access)
- Multiple initialization techniques
- Multidimensional arrays (2D, 3D)
- Arrays and pointers relationship
- Passing arrays to functions
- std::array demonstrations
- STL algorithms on arrays
- Common array patterns (sum, min/max, search, reverse)

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/107_arrays
g++ -std=c++20 -Wall -Wextra -o arrays main.cpp
```

### Execution
```bash
./arrays
```

## Key Concepts

### 1. Array Declaration and Initialization
```cpp
// Declaration
int numbers[5];  // Uninitialized

// Initialize with values
int arr1[5] = {1, 2, 3, 4, 5};

// Partial initialization (rest are zero)
int arr2[5] = {1, 2};  // {1, 2, 0, 0, 0}

// Initialize all to zero
int arr3[5] = {0};
int arr4[5] = {};  // C++11

// Omit size (compiler deduces)
int arr5[] = {10, 20, 30, 40, 50};

// Uniform initialization (C++11)
int arr6[5]{1, 2, 3, 4, 5};
```

### 2. Multidimensional Arrays
```cpp
// 2D array (matrix)
int matrix[3][3] = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Access elements
std::cout << matrix[1][2];  // 6

// 3D array
int cube[2][2][2] = {
    {{1, 2}, {3, 4}},
    {{5, 6}, {7, 8}}
};
```

### 3. Arrays and Pointers
```cpp
int arr[] = {10, 20, 30, 40, 50};
int* ptr = arr;  // Array name is pointer to first element

// These are equivalent:
arr[2]      // 30
*(arr + 2)  // 30
ptr[2]      // 30
*(ptr + 2)  // 30
```

### 4. Passing Arrays to Functions
```cpp
// Array decays to pointer
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
}

// Template preserves size
template<size_t N>
void printArrayByRef(int (&arr)[N]) {
    for (size_t i = 0; i < N; i++) {
        std::cout << arr[i] << " ";
    }
}
```

### 5. std::array (C++11)
```cpp
#include <array>

// Fixed-size array with bounds checking
std::array<int, 5> arr1 = {1, 2, 3, 4, 5};

// Access
arr1[0];      // No bounds checking
arr1.at(1);   // With bounds checking

// Properties
arr1.size();   // 5
arr1.front();  // 1
arr1.back();   // 5
arr1.empty();  // false

// Iterators
for (auto it = arr1.begin(); it != arr1.end(); ++it) {
    std::cout << *it << " ";
}

// Range-based for
for (int val : arr1) {
    std::cout << val << " ";
}

// Fill
arr1.fill(10);  // All elements = 10
```

### 6. Array Algorithms
```cpp
#include <algorithm>
#include <numeric>

std::array<int, 7> arr = {64, 34, 25, 12, 22, 11, 90};

// Sort
std::sort(arr.begin(), arr.end());

// Binary search (requires sorted)
bool found = std::binary_search(arr.begin(), arr.end(), 22);

// Find
auto it = std::find(arr.begin(), arr.end(), 25);

// Min/Max
auto minIt = std::min_element(arr.begin(), arr.end());
auto maxIt = std::max_element(arr.begin(), arr.end());

// Sum
int sum = std::accumulate(arr.begin(), arr.end(), 0);

// Reverse
std::reverse(arr.begin(), arr.end());
```

## Best Practices
1. **Prefer std::array** over C-style arrays
2. **Always pass size** when passing C-style arrays to functions
3. **Use range-based for loops** when possible
4. **Initialize arrays** to avoid garbage values
5. **Use std::vector** for dynamic-size arrays
6. **Prefer STL algorithms** over hand-written loops
7. **Use const** when arrays shouldn't be modified
8. **Remember array decay** to pointers
9. **Consider std::span** (C++20) for array views
10. **Be careful with bounds** - no automatic checking in C-style arrays

## Resources and References
- [cppreference.com - Arrays](https://en.cppreference.com/w/cpp/language/array)
- [cppreference.com - std::array](https://en.cppreference.com/w/cpp/container/array)
- [C++ Core Guidelines - Arrays](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#SS-containers)

## Navigation
- **Previous Program**: [106 - Functions](../106_functions/README.md)
- **Next Program**: [108 - Pointers](../108_pointers/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
