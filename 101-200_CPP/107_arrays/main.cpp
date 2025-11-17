/*
 * Program 107: Arrays in C++
 *
 * Topics Covered:
 * - Static arrays (C-style arrays)
 * - Array declaration and initialization
 * - Accessing array elements
 * - Multidimensional arrays
 * - Arrays and pointers relationship
 * - Array size calculation
 * - Passing arrays to functions
 * - std::array (C++11)
 * - Array algorithms
 * - Common array operations
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o arrays main.cpp
 */

#include <iostream>
#include <array>      // std::array
#include <algorithm>  // std::sort, std::find, etc.
#include <numeric>    // std::accumulate
#include <cstring>    // memset, memcpy

void demonstrateBasicArrays();
void demonstrateArrayInitialization();
void demonstrateMultidimensionalArrays();
void demonstrateArraysAndPointers();
void demonstratePassingArrays();
void demonstrateStdArray();
void demonstrateArrayAlgorithms();
void demonstrateCommonOperations();

int main() {
    std::cout << "=== C++ Arrays ===" << std::endl;
    std::cout << std::endl;

    demonstrateBasicArrays();
    demonstrateArrayInitialization();
    demonstrateMultidimensionalArrays();
    demonstrateArraysAndPointers();
    demonstratePassingArrays();
    demonstrateStdArray();
    demonstrateArrayAlgorithms();
    demonstrateCommonOperations();

    return 0;
}

void demonstrateBasicArrays() {
    std::cout << "--- Basic Arrays ---" << std::endl;

    // Array declaration
    int numbers[5];  // Uninitialized array of 5 integers

    // Assigning values
    numbers[0] = 10;
    numbers[1] = 20;
    numbers[2] = 30;
    numbers[3] = 40;
    numbers[4] = 50;

    // Accessing elements
    std::cout << "Array elements: ";
    for (int i = 0; i < 5; i++) {
        std::cout << numbers[i] << " ";
    }
    std::cout << std::endl;

    // Array size
    int size = sizeof(numbers) / sizeof(numbers[0]);
    std::cout << "Array size: " << size << std::endl;

    // Modifying elements
    numbers[2] = 300;
    std::cout << "After modification: numbers[2] = " << numbers[2] << std::endl;

    std::cout << std::endl;
}

void demonstrateArrayInitialization() {
    std::cout << "--- Array Initialization ---" << std::endl;

    // Initialize with values
    int arr1[5] = {1, 2, 3, 4, 5};

    // Partial initialization (rest are zero)
    int arr2[5] = {1, 2};  // {1, 2, 0, 0, 0}

    // Initialize all to zero
    int arr3[5] = {0};  // {0, 0, 0, 0, 0}
    int arr4[5] = {};   // C++11: same as above

    // Omit size (compiler deduces)
    int arr5[] = {10, 20, 30, 40, 50};

    // Uniform initialization (C++11)
    int arr6[5]{1, 2, 3, 4, 5};

    std::cout << "arr1: ";
    for (int val : arr1) std::cout << val << " ";
    std::cout << std::endl;

    std::cout << "arr2 (partial): ";
    for (int val : arr2) std::cout << val << " ";
    std::cout << std::endl;

    std::cout << "arr3 (zeros): ";
    for (int val : arr3) std::cout << val << " ";
    std::cout << std::endl;

    std::cout << "arr5 (deduced size): ";
    for (int val : arr5) std::cout << val << " ";
    std::cout << std::endl;

    std::cout << std::endl;
}

void demonstrateMultidimensionalArrays() {
    std::cout << "--- Multidimensional Arrays ---" << std::endl;

    // 2D array (matrix)
    int matrix[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    std::cout << "2D Array (3x3 matrix):" << std::endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }

    // Partial initialization
    int matrix2[3][3] = {{1}, {4}, {7}};  // First column only
    std::cout << "\nPartially initialized matrix:" << std::endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            std::cout << matrix2[i][j] << " ";
        }
        std::cout << std::endl;
    }

    // 3D array
    int cube[2][2][2] = {
        {{1, 2}, {3, 4}},
        {{5, 6}, {7, 8}}
    };

    std::cout << "\n3D Array:" << std::endl;
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 2; k++) {
                std::cout << "cube[" << i << "][" << j << "][" << k << "] = " << cube[i][j][k] << std::endl;
            }
        }
    }

    std::cout << std::endl;
}

void demonstrateArraysAndPointers() {
    std::cout << "--- Arrays and Pointers ---" << std::endl;

    int arr[] = {10, 20, 30, 40, 50};

    // Array name is pointer to first element
    int* ptr = arr;
    std::cout << "arr[0] = " << arr[0] << std::endl;
    std::cout << "*ptr = " << *ptr << std::endl;
    std::cout << "arr and ptr are " << (arr == ptr ? "equal" : "not equal") << std::endl;

    // Pointer arithmetic
    std::cout << "\nPointer arithmetic:" << std::endl;
    std::cout << "*(ptr + 0) = " << *(ptr + 0) << std::endl;
    std::cout << "*(ptr + 1) = " << *(ptr + 1) << std::endl;
    std::cout << "*(ptr + 2) = " << *(ptr + 2) << std::endl;

    // Subscript notation with pointers
    std::cout << "\nSubscript with pointer:" << std::endl;
    std::cout << "ptr[0] = " << ptr[0] << std::endl;
    std::cout << "ptr[1] = " << ptr[1] << std::endl;

    // Address arithmetic
    std::cout << "\nAddresses:" << std::endl;
    for (int i = 0; i < 5; i++) {
        std::cout << "&arr[" << i << "] = " << &arr[i] << std::endl;
    }

    std::cout << std::endl;
}

void printArray(int arr[], int size) {
    // Note: size must be passed separately
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

void modifyArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] *= 2;
    }
}

template<size_t N>
void printArrayByRef(int (&arr)[N]) {
    // Size is preserved with reference
    std::cout << "Array size in function: " << N << std::endl;
    for (size_t i = 0; i < N; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

void demonstratePassingArrays() {
    std::cout << "--- Passing Arrays to Functions ---" << std::endl;

    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    std::cout << "Original array: ";
    printArray(numbers, size);

    modifyArray(numbers, size);
    std::cout << "After modification: ";
    printArray(numbers, size);

    // Passing by reference (preserves size)
    int arr[5] = {10, 20, 30, 40, 50};
    std::cout << "\nPassing by reference:" << std::endl;
    printArrayByRef(arr);

    std::cout << std::endl;
}

void demonstrateStdArray() {
    std::cout << "--- std::array (C++11) ---" << std::endl;

    // std::array: fixed-size array with bounds checking
    std::array<int, 5> arr1 = {1, 2, 3, 4, 5};

    // Access elements
    std::cout << "arr1[0] = " << arr1[0] << std::endl;
    std::cout << "arr1.at(1) = " << arr1.at(1) << " (with bounds checking)" << std::endl;

    // Size
    std::cout << "Size: " << arr1.size() << std::endl;

    // Iterators
    std::cout << "Using iterators: ";
    for (auto it = arr1.begin(); it != arr1.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    // Range-based for
    std::cout << "Range-based for: ";
    for (int val : arr1) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    // Front and back
    std::cout << "Front: " << arr1.front() << std::endl;
    std::cout << "Back: " << arr1.back() << std::endl;

    // Fill
    std::array<int, 5> arr2;
    arr2.fill(10);
    std::cout << "After fill(10): ";
    for (int val : arr2) std::cout << val << " ";
    std::cout << std::endl;

    // Swap
    std::cout << "\nBefore swap:" << std::endl;
    std::cout << "arr1: ";
    for (int val : arr1) std::cout << val << " ";
    std::cout << std::endl;
    std::cout << "arr2: ";
    for (int val : arr2) std::cout << val << " ";
    std::cout << std::endl;

    arr1.swap(arr2);

    std::cout << "After swap:" << std::endl;
    std::cout << "arr1: ";
    for (int val : arr1) std::cout << val << " ";
    std::cout << std::endl;
    std::cout << "arr2: ";
    for (int val : arr2) std::cout << val << " ";
    std::cout << std::endl;

    std::cout << std::endl;
}

void demonstrateArrayAlgorithms() {
    std::cout << "--- Array Algorithms ---" << std::endl;

    std::array<int, 7> arr = {64, 34, 25, 12, 22, 11, 90};

    std::cout << "Original: ";
    for (int val : arr) std::cout << val << " ";
    std::cout << std::endl;

    // Sort
    std::sort(arr.begin(), arr.end());
    std::cout << "After sort: ";
    for (int val : arr) std::cout << val << " ";
    std::cout << std::endl;

    // Binary search (requires sorted array)
    bool found = std::binary_search(arr.begin(), arr.end(), 22);
    std::cout << "Binary search for 22: " << (found ? "found" : "not found") << std::endl;

    // Find
    auto it = std::find(arr.begin(), arr.end(), 25);
    if (it != arr.end()) {
        std::cout << "Found 25 at index: " << std::distance(arr.begin(), it) << std::endl;
    }

    // Count
    int count = std::count(arr.begin(), arr.end(), 22);
    std::cout << "Count of 22: " << count << std::endl;

    // Min and Max
    auto minIt = std::min_element(arr.begin(), arr.end());
    auto maxIt = std::max_element(arr.begin(), arr.end());
    std::cout << "Min: " << *minIt << ", Max: " << *maxIt << std::endl;

    // Sum
    int sum = std::accumulate(arr.begin(), arr.end(), 0);
    std::cout << "Sum: " << sum << std::endl;

    // Reverse
    std::reverse(arr.begin(), arr.end());
    std::cout << "After reverse: ";
    for (int val : arr) std::cout << val << " ";
    std::cout << std::endl;

    std::cout << std::endl;
}

void demonstrateCommonOperations() {
    std::cout << "--- Common Array Operations ---" << std::endl;

    int arr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int size = sizeof(arr) / sizeof(arr[0]);

    // Sum
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    std::cout << "Sum: " << sum << std::endl;

    // Average
    double avg = static_cast<double>(sum) / size;
    std::cout << "Average: " << avg << std::endl;

    // Find maximum
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    std::cout << "Maximum: " << max << std::endl;

    // Find minimum
    int min = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] < min) {
            min = arr[i];
        }
    }
    std::cout << "Minimum: " << min << std::endl;

    // Linear search
    int target = 7;
    int index = -1;
    for (int i = 0; i < size; i++) {
        if (arr[i] == target) {
            index = i;
            break;
        }
    }
    std::cout << "Index of " << target << ": " << index << std::endl;

    // Reverse array
    int reversed[10];
    for (int i = 0; i < size; i++) {
        reversed[i] = arr[size - 1 - i];
    }
    std::cout << "Reversed: ";
    for (int i = 0; i < size; i++) {
        std::cout << reversed[i] << " ";
    }
    std::cout << std::endl;

    // Copy array
    int copy[10];
    std::copy(std::begin(arr), std::end(arr), std::begin(copy));
    std::cout << "Copy: ";
    for (int val : copy) std::cout << val << " ";
    std::cout << std::endl;

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Prefer std::array over C-style arrays
 * 2. Always pass size when passing C-style arrays to functions
 * 3. Use range-based for loops when possible
 * 4. Be careful with array bounds (no automatic checking in C-style arrays)
 * 5. Use std::vector for dynamic-size arrays
 * 6. Initialize arrays to avoid garbage values
 * 7. Prefer STL algorithms over hand-written loops
 * 8. Use const when arrays shouldn't be modified
 * 9. Remember: array names decay to pointers
 * 10. Consider using std::span (C++20) for passing array views
 */
