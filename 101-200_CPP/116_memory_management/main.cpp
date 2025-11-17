/*
 * Program 116: Memory Management
 *
 * Topics Covered:
 * - Stack vs Heap memory
 * - new and delete operators
 * - new[] and delete[] for arrays
 * - Memory leaks
 * - malloc/free (C-style, avoid in C++)
 * - Smart pointers (unique_ptr, shared_ptr, weak_ptr)
 * - RAII (Resource Acquisition Is Initialization)
 * - Memory allocation failures
 * - Placement new
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o memory_management main.cpp
 */

#include <iostream>
#include <memory>  // Smart pointers
#include <vector>
#include <cstdlib>  // malloc, free

void demonstrateStackVsHeap();
void demonstrateNewDelete();
void demonstrateMemoryLeaks();
void demonstrateSmartPointers();
void demonstrateRAII();

int main() {
    std::cout << "=== C++ Memory Management ===" << std::endl << std::endl;

    demonstrateStackVsHeap();
    demonstrateNewDelete();
    demonstrateMemoryLeaks();
    demonstrateSmartPointers();
    demonstrateRAII();

    return 0;
}

void demonstrateStackVsHeap() {
    std::cout << "--- Stack vs Heap Memory ---" << std::endl;

    // Stack allocation (automatic)
    int stackVar = 42;
    int stackArray[5] = {1, 2, 3, 4, 5};

    std::cout << "Stack variable: " << stackVar << std::endl;
    std::cout << "Stack array size: " << sizeof(stackArray) / sizeof(stackArray[0]) << std::endl;

    // Stack memory:
    // - Fast allocation/deallocation
    // - Limited size (typically 1-8 MB)
    // - Automatic cleanup
    // - LIFO (Last In First Out)

    // Heap allocation (dynamic)
    int* heapVar = new int(100);
    int* heapArray = new int[5]{10, 20, 30, 40, 50};

    std::cout << "Heap variable: " << *heapVar << std::endl;
    std::cout << "Heap array[0]: " << heapArray[0] << std::endl;

    // Heap memory:
    // - Slower allocation/deallocation
    // - Large size (system dependent)
    // - Manual cleanup required
    // - Flexible lifetime

    // Must delete heap memory
    delete heapVar;
    delete[] heapArray;

    std::cout << "\nStack memory is preferred when size is known at compile time" << std::endl;
    std::cout << "Heap memory is used for dynamic sizing and long lifetimes" << std::endl;

    std::cout << std::endl;
}

void demonstrateNewDelete() {
    std::cout << "--- new and delete Operators ---" << std::endl;

    // Single object allocation
    int* ptr = new int;  // Uninitialized
    *ptr = 42;
    std::cout << "Allocated int: " << *ptr << std::endl;
    delete ptr;

    // Single object with initialization
    int* ptr2 = new int(100);
    std::cout << "Initialized int: " << *ptr2 << std::endl;
    delete ptr2;

    // Array allocation
    int* arr = new int[5];
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
    }
    std::cout << "Dynamic array: ";
    for (int i = 0; i < 5; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    delete[] arr;  // Must use delete[] for arrays

    // Array with initialization (C++11)
    int* arr2 = new int[5]{1, 2, 3, 4, 5};
    std::cout << "Initialized array: ";
    for (int i = 0; i < 5; i++) {
        std::cout << arr2[i] << " ";
    }
    std::cout << std::endl;
    delete[] arr2;

    // Dynamic struct/class
    struct Point {
        int x, y;
    };

    Point* point = new Point{10, 20};
    std::cout << "Point: (" << point->x << ", " << point->y << ")" << std::endl;
    delete point;

    // nothrow version (returns nullptr on failure)
    int* safe = new(std::nothrow) int[1000000000];  // May fail
    if (safe == nullptr) {
        std::cout << "Allocation failed (returned nullptr)" << std::endl;
    } else {
        delete[] safe;
    }

    // malloc/free (C-style, avoid in C++)
    std::cout << "\n--- malloc/free (C-style) ---" << std::endl;
    int* cPtr = (int*)malloc(sizeof(int) * 5);
    if (cPtr != nullptr) {
        cPtr[0] = 100;
        std::cout << "malloc'd memory: " << cPtr[0] << std::endl;
        free(cPtr);
    }
    std::cout << "Prefer new/delete over malloc/free in C++" << std::endl;

    std::cout << std::endl;
}

void demonstrateMemoryLeaks() {
    std::cout << "--- Memory Leaks ---" << std::endl;

    // Memory leak example (DON'T DO THIS)
    auto leakMemory = []() {
        int* leak = new int(42);
        // Forgot to delete - memory leak!
    };

    std::cout << "Memory leak: Allocating without freeing" << std::endl;
    // leakMemory();  // Commented to avoid actual leak

    // Double delete (undefined behavior)
    std::cout << "\nDouble delete is undefined behavior:" << std::endl;
    int* ptr = new int(10);
    delete ptr;
    // delete ptr;  // DANGER! Undefined behavior

    // Set to nullptr after delete to avoid double delete
    ptr = nullptr;
    delete ptr;  // Safe - deleting nullptr is OK
    std::cout << "Deleting nullptr is safe" << std::endl;

    // Dangling pointer
    std::cout << "\nDangling pointer:" << std::endl;
    int* dangling = new int(100);
    delete dangling;
    // *dangling = 200;  // DANGER! Accessing freed memory
    dangling = nullptr;  // Good practice

    // Memory leak with arrays
    std::cout << "\nAlways match new with delete, new[] with delete[]" << std::endl;
    int* arr = new int[10];
    // delete arr;  // WRONG! Should be delete[]
    delete[] arr;  // Correct

    std::cout << std::endl;
}

class Resource {
public:
    Resource(const std::string& name) : name_(name) {
        std::cout << "Resource '" << name_ << "' acquired" << std::endl;
    }

    ~Resource() {
        std::cout << "Resource '" << name_ << "' released" << std::endl;
    }

    void use() {
        std::cout << "Using resource '" << name_ << "'" << std::endl;
    }

private:
    std::string name_;
};

void demonstrateSmartPointers() {
    std::cout << "--- Smart Pointers (C++11) ---" << std::endl;

    // unique_ptr: Exclusive ownership
    std::cout << "unique_ptr (exclusive ownership):" << std::endl;
    {
        std::unique_ptr<Resource> ptr1 = std::make_unique<Resource>("unique1");
        ptr1->use();

        // Cannot copy unique_ptr
        // std::unique_ptr<Resource> ptr2 = ptr1;  // Error!

        // Can move unique_ptr
        std::unique_ptr<Resource> ptr2 = std::move(ptr1);
        // ptr1 is now null
        ptr2->use();
    }  // Automatically deleted when out of scope

    // shared_ptr: Shared ownership
    std::cout << "\nshared_ptr (shared ownership):" << std::endl;
    {
        std::shared_ptr<Resource> ptr1 = std::make_shared<Resource>("shared1");
        std::cout << "Reference count: " << ptr1.use_count() << std::endl;

        {
            std::shared_ptr<Resource> ptr2 = ptr1;  // Share ownership
            std::cout << "Reference count: " << ptr1.use_count() << std::endl;
            ptr2->use();
        }  // ptr2 destroyed, but resource still alive

        std::cout << "Reference count after ptr2 destroyed: " << ptr1.use_count() << std::endl;
    }  // Resource deleted when last shared_ptr destroyed

    // weak_ptr: Non-owning reference
    std::cout << "\nweak_ptr (non-owning reference):" << std::endl;
    std::weak_ptr<Resource> weakPtr;
    {
        std::shared_ptr<Resource> sharedPtr = std::make_shared<Resource>("weak1");
        weakPtr = sharedPtr;  // weak_ptr doesn't increase ref count

        std::cout << "shared_ptr count: " << sharedPtr.use_count() << std::endl;

        if (auto locked = weakPtr.lock()) {  // Get shared_ptr if still alive
            locked->use();
        }
    }  // Resource deleted

    if (weakPtr.expired()) {
        std::cout << "Resource no longer exists" << std::endl;
    }

    // Smart pointer with arrays
    std::cout << "\nSmart pointers with arrays:" << std::endl;
    std::unique_ptr<int[]> arrPtr = std::make_unique<int[]>(5);
    for (int i = 0; i < 5; i++) {
        arrPtr[i] = i * 10;
    }
    std::cout << "Smart pointer array[0]: " << arrPtr[0] << std::endl;

    std::cout << std::endl;
}

class FileHandler {
public:
    FileHandler(const std::string& filename) {
        std::cout << "Opening file: " << filename << std::endl;
        // In real code: open file
    }

    ~FileHandler() {
        std::cout << "Closing file" << std::endl;
        // In real code: close file
    }

    void write(const std::string& data) {
        std::cout << "Writing: " << data << std::endl;
    }
};

void demonstrateRAII() {
    std::cout << "--- RAII (Resource Acquisition Is Initialization) ---" << std::endl;

    {
        FileHandler file("data.txt");
        file.write("Hello, RAII!");
        // File automatically closed when file goes out of scope
    }

    std::cout << "\nRAII ensures resources are properly released" << std::endl;
    std::cout << "Even in the presence of exceptions" << std::endl;

    // RAII with smart pointers
    {
        auto resource = std::make_unique<Resource>("RAII");
        resource->use();
        // throw std::runtime_error("Error!");  // Resource still cleaned up
    }

    // Vector uses RAII
    {
        std::vector<int> vec = {1, 2, 3, 4, 5};
        // Memory automatically managed
    }  // Vector's destructor frees memory

    std::cout << std::endl;
}

/*
 * Memory Management Best Practices:
 *
 * 1. Prefer stack allocation over heap when possible
 * 2. Use smart pointers instead of raw pointers
 * 3. Prefer std::make_unique and std::make_shared
 * 4. Match new with delete, new[] with delete[]
 * 5. Set pointers to nullptr after delete
 * 6. Use RAII for resource management
 * 7. Avoid manual memory management when possible
 * 8. Use std::vector instead of dynamic arrays
 * 9. Check for nullptr before dereferencing
 * 10. Use valgrind or sanitizers to detect memory issues
 *
 * Smart Pointer Selection:
 * - unique_ptr: Default choice, exclusive ownership
 * - shared_ptr: When shared ownership is needed
 * - weak_ptr: To break circular references
 * - Avoid raw owning pointers in modern C++
 *
 * Common Memory Issues:
 * - Memory leaks (forgetting to delete)
 * - Double delete
 * - Dangling pointers (using after delete)
 * - Buffer overflows
 * - Accessing uninitialized memory
 * - Mixing new/delete with malloc/free
 */
