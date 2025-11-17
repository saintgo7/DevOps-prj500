# Program 116: Memory Management in C++

## Description
Comprehensive exploration of dynamic memory management in C++ covering stack vs heap, new/delete operators, memory allocation strategies, memory leaks, dangling pointers, and modern memory management techniques. This program demonstrates manual and automatic memory management approaches.

## Learning Objectives
- Understand stack vs heap memory
- Master new and delete operators
- Prevent memory leaks and dangling pointers
- Use placement new and custom allocators
- Apply RAII principles for memory management
- Work with memory pools
- Understand modern alternatives (smart pointers)

## Features
- Stack vs heap memory comparison
- Dynamic memory allocation (new/delete)
- Array allocation (new[]/delete[])
- Placement new
- Memory leak detection
- Dangling pointer prevention
- Custom memory allocators
- Memory pool implementation
- RAII for automatic cleanup

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/116_memory_management
g++ -std=c++20 -Wall -Wextra -o memory_management main.cpp
```

### Execution
```bash
./memory_management
```

## Key Concepts

### 1. Stack vs Heap Memory
```cpp
void demonstrateMemory() {
    // Stack allocation (automatic)
    int stackVar = 42;              // Allocated on stack
    int stackArray[100];            // Fixed size, stack
    // Fast, automatic cleanup, limited size

    // Heap allocation (dynamic)
    int* heapVar = new int(42);     // Allocated on heap
    int* heapArray = new int[100];  // Dynamic size, heap
    // Slower, manual cleanup, large size possible

    delete heapVar;
    delete[] heapArray;

    // Stack characteristics:
    // - Fast allocation/deallocation
    // - Limited size (typically 1-8 MB)
    // - Automatic cleanup
    // - LIFO structure

    // Heap characteristics:
    // - Slower allocation/deallocation
    // - Large size available
    // - Manual cleanup required
    // - Fragmentation possible
}
```

### 2. Dynamic Memory Allocation
```cpp
// Allocate single object
int* ptr = new int;                  // Uninitialized
int* ptr2 = new int(42);             // Initialized
int* ptr3 = new int{42};             // C++11 uniform initialization

// Allocate array
int* arr = new int[10];              // Uninitialized
int* arr2 = new int[10]();           // Zero-initialized
int* arr3 = new int[10]{1,2,3};      // Partial initialization

// Delete
delete ptr;
delete ptr2;
delete ptr3;
delete[] arr;    // Must use delete[] for arrays
delete[] arr2;
delete[] arr3;

// Nothrow allocation
int* safe = new(std::nothrow) int[1000000000];
if (safe == nullptr) {
    std::cerr << "Allocation failed\n";
} else {
    delete[] safe;
}
```

### 3. Common Memory Problems
```cpp
// 1. Memory Leak
void memoryLeak() {
    int* ptr = new int(42);
    // Forgot to delete!
}  // Memory leaked

// 2. Dangling Pointer
void danglingPointer() {
    int* ptr = new int(42);
    delete ptr;
    // *ptr = 10;  // Undefined behavior! Dangling pointer
    ptr = nullptr;  // Good practice
}

// 3. Double Delete
void doubleDelete() {
    int* ptr = new int(42);
    delete ptr;
    // delete ptr;  // Undefined behavior!
}

// 4. Delete mismatch
void deleteMismatch() {
    int* arr = new int[10];
    // delete arr;  // Wrong! Should be delete[]
    delete[] arr;  // Correct
}

// 5. Wild Pointer
void wildPointer() {
    int* ptr;  // Uninitialized
    // *ptr = 42;  // Undefined behavior!
}
```

### 4. RAII Pattern
```cpp
// Resource Acquisition Is Initialization
class ResourceManager {
    int* data;
    size_t size;
public:
    // Constructor acquires resource
    ResourceManager(size_t n) : size(n) {
        data = new int[n];
        std::cout << "Resource acquired\n";
    }

    // Destructor releases resource
    ~ResourceManager() {
        delete[] data;
        std::cout << "Resource released\n";
    }

    // Delete copy operations
    ResourceManager(const ResourceManager&) = delete;
    ResourceManager& operator=(const ResourceManager&) = delete;

    // Access methods
    int& operator[](size_t i) { return data[i]; }
};

void useRAII() {
    ResourceManager rm(100);
    rm[0] = 42;
    // No need to manually delete - destructor handles it
}  // Automatic cleanup
```

### 5. Placement New
```cpp
#include <new>

void placementNew() {
    // Allocate raw memory
    char buffer[sizeof(int) * 10];

    // Construct object in specific location
    int* ptr = new(buffer) int(42);

    std::cout << *ptr << '\n';

    // Must manually call destructor
    ptr->~int();  // Not needed for int, but required for classes

    // Example with class
    class MyClass {
    public:
        MyClass() { std::cout << "Constructor\n"; }
        ~MyClass() { std::cout << "Destructor\n"; }
    };

    alignas(MyClass) char objBuffer[sizeof(MyClass)];
    MyClass* obj = new(objBuffer) MyClass();
    obj->~MyClass();  // Must call destructor
}
```

### 6. Custom Allocator
```cpp
class SimpleAllocator {
public:
    void* allocate(size_t size) {
        std::cout << "Allocating " << size << " bytes\n";
        return ::operator new(size);
    }

    void deallocate(void* ptr) {
        std::cout << "Deallocating\n";
        ::operator delete(ptr);
    }
};

// Overload new/delete for a class
class CustomNew {
public:
    void* operator new(size_t size) {
        std::cout << "Custom new: " << size << " bytes\n";
        return ::operator new(size);
    }

    void operator delete(void* ptr) {
        std::cout << "Custom delete\n";
        ::operator delete(ptr);
    }
};
```

### 7. Memory Pool
```cpp
template<typename T, size_t BlockSize = 4096>
class MemoryPool {
    union Block {
        T element;
        Block* next;
    };

    Block* freeBlocks;

public:
    MemoryPool() : freeBlocks(nullptr) {}

    ~MemoryPool() {
        // Clean up allocated blocks
    }

    T* allocate() {
        if (freeBlocks == nullptr) {
            // Allocate new block
            Block* newBlock = static_cast<Block*>(
                ::operator new(BlockSize * sizeof(Block))
            );

            // Link blocks
            for (size_t i = 0; i < BlockSize - 1; ++i) {
                newBlock[i].next = &newBlock[i + 1];
            }
            newBlock[BlockSize - 1].next = nullptr;

            freeBlocks = newBlock;
        }

        Block* block = freeBlocks;
        freeBlocks = block->next;
        return &block->element;
    }

    void deallocate(T* ptr) {
        Block* block = reinterpret_cast<Block*>(ptr);
        block->next = freeBlocks;
        freeBlocks = block;
    }
};
```

### 8. Memory Debugging
```cpp
// Track allocations
class MemoryTracker {
    static size_t totalAllocated;
    static size_t totalDeallocated;

public:
    static void* allocate(size_t size) {
        totalAllocated += size;
        return malloc(size);
    }

    static void deallocate(void* ptr, size_t size) {
        totalDeallocated += size;
        free(ptr);
    }

    static void report() {
        std::cout << "Total allocated: " << totalAllocated << '\n';
        std::cout << "Total deallocated: " << totalDeallocated << '\n';
        std::cout << "Leaked: " << (totalAllocated - totalDeallocated) << '\n';
    }
};

size_t MemoryTracker::totalAllocated = 0;
size_t MemoryTracker::totalDeallocated = 0;
```

## Best Practices
1. **Prefer smart pointers** over raw pointers for ownership
2. **Follow RAII principles** for automatic resource management
3. **Initialize pointers** to nullptr
4. **Set pointers to nullptr** after delete
5. **Match new with delete** and new[] with delete[]
6. **Check allocation success** for large allocations
7. **Avoid manual memory management** when possible
8. **Use containers** (vector, string) instead of arrays
9. **Profile memory usage** to detect leaks
10. **Consider memory pools** for frequent allocations

## Modern Alternatives
```cpp
// Instead of raw pointers
// Old:
int* ptr = new int(42);
delete ptr;

// Modern:
auto ptr = std::make_unique<int>(42);  // Automatic cleanup

// Instead of arrays
// Old:
int* arr = new int[100];
delete[] arr;

// Modern:
std::vector<int> arr(100);  // Automatic management
```

## Resources and References
- [cppreference.com - Memory Management](https://en.cppreference.com/w/cpp/memory)
- [cppreference.com - new/delete](https://en.cppreference.com/w/cpp/memory/new/operator_new)
- [C++ Core Guidelines - Memory](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r-resource-management)

## Navigation
- **Previous Program**: [115 - Namespaces](../115_namespaces/README.md)
- **Next Program**: [117 - const and constexpr](../117_const_constexpr/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
