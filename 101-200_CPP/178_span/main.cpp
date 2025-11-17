/*
 * Program 178: std::span - Non-Owning Array View (C++20)
 *
 * This program demonstrates:
 * - std::span basics (C++20)
 * - Non-owning view of contiguous sequences
 * - Static and dynamic extents
 * - Subspans and operations
 * - Practical use cases
 *
 * Note: Requires C++20 compiler support
 * Compile with: g++ -std=c++20
 */

#include <iostream>
#include <span>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>

// ==============================================
// 1. std::span Basics
// ==============================================

void printSpan(std::span<const int> data) {
    std::cout << "Span [size=" << data.size() << "]: ";
    for (int value : data) {
        std::cout << value << " ";
    }
    std::cout << "\n";
}

void spanBasicsDemo() {
    std::cout << "\n=== 1. std::span Basics ===\n";

    // From C-array
    int arr[] = {1, 2, 3, 4, 5};
    std::span<int> span1(arr);
    printSpan(span1);

    // From std::array
    std::array<int, 5> stdArr = {10, 20, 30, 40, 50};
    std::span<int> span2(stdArr);
    printSpan(span2);

    // From std::vector
    std::vector<int> vec = {100, 200, 300, 400, 500};
    std::span<int> span3(vec);
    printSpan(span3);

    // From pointer and size
    std::span<int> span4(arr, 3); // First 3 elements
    printSpan(span4);
}

// ==============================================
// 2. Static vs Dynamic Extent
// ==============================================

void extentDemo() {
    std::cout << "\n=== 2. Static vs Dynamic Extent ===\n";

    std::array<int, 5> arr = {1, 2, 3, 4, 5};

    // Static extent (size known at compile-time)
    std::span<int, 5> staticSpan(arr);
    std::cout << "Static extent: " << staticSpan.extent << "\n";
    std::cout << "Size: " << staticSpan.size() << "\n";

    // Dynamic extent (size known at runtime)
    std::span<int> dynamicSpan(arr);
    std::cout << "Dynamic extent: " << dynamicSpan.extent << "\n"; // std::dynamic_extent
    std::cout << "Size: " << dynamicSpan.size() << "\n";

    std::vector<int> vec = {10, 20, 30};
    std::span<int> vecSpan(vec); // Must be dynamic extent
    std::cout << "Vector span size: " << vecSpan.size() << "\n";
}

// ==============================================
// 3. Accessing Elements
// ==============================================

void accessDemo() {
    std::cout << "\n=== 3. Accessing Elements ===\n";

    int arr[] = {10, 20, 30, 40, 50};
    std::span<int> span(arr);

    // Index access
    std::cout << "span[0]: " << span[0] << "\n";
    std::cout << "span[4]: " << span[4] << "\n";

    // front() and back()
    std::cout << "front(): " << span.front() << "\n";
    std::cout << "back(): " << span.back() << "\n";

    // data() pointer
    std::cout << "data(): " << span.data() << " -> " << *span.data() << "\n";

    // Modification through span
    span[0] = 100;
    std::cout << "After span[0] = 100: " << arr[0] << "\n";
}

// ==============================================
// 4. Iterators
// ==============================================

void iteratorDemo() {
    std::cout << "\n=== 4. Iterators ===\n";

    std::vector<int> vec = {1, 2, 3, 4, 5};
    std::span<int> span(vec);

    // Range-based for
    std::cout << "Range-for: ";
    for (int val : span) {
        std::cout << val << " ";
    }
    std::cout << "\n";

    // Iterator loop
    std::cout << "Iterators: ";
    for (auto it = span.begin(); it != span.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";

    // Reverse iterators
    std::cout << "Reverse: ";
    for (auto it = span.rbegin(); it != span.rend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
}

// ==============================================
// 5. Subspans
// ==============================================

void subspanDemo() {
    std::cout << "\n=== 5. Subspans ===\n";

    std::array<int, 10> arr = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::span<int> span(arr);

    // first(n) - first n elements
    auto first3 = span.first(3);
    std::cout << "first(3): ";
    printSpan(first3);

    // last(n) - last n elements
    auto last3 = span.last(3);
    std::cout << "last(3): ";
    printSpan(last3);

    // subspan(offset, count)
    auto middle = span.subspan(3, 4); // 4 elements starting at index 3
    std::cout << "subspan(3, 4): ";
    printSpan(middle);

    // subspan(offset) - from offset to end
    auto fromOffset = span.subspan(7);
    std::cout << "subspan(7): ";
    printSpan(fromOffset);
}

// ==============================================
// 6. Const Spans
// ==============================================

void constSpanDemo() {
    std::cout << "\n=== 6. Const Spans ===\n";

    std::vector<int> vec = {1, 2, 3, 4, 5};

    // Mutable span
    std::span<int> mutableSpan(vec);
    mutableSpan[0] = 100;
    std::cout << "After mutable modification: " << vec[0] << "\n";

    // Const span (read-only)
    std::span<const int> constSpan(vec);
    std::cout << "Const span[0]: " << constSpan[0] << "\n";
    // constSpan[0] = 200; // Error: cannot modify through const span
}

// ==============================================
// 7. Span as Function Parameter
// ==============================================

// Old way - multiple overloads needed
void processArrayOld(const int* data, size_t size) {
    std::cout << "Processing " << size << " elements (old way)\n";
}

void processVectorOld(const std::vector<int>& vec) {
    std::cout << "Processing vector (old way)\n";
}

// New way - single function for all contiguous containers
void processData(std::span<const int> data) {
    std::cout << "Processing " << data.size() << " elements: ";
    int sum = std::accumulate(data.begin(), data.end(), 0);
    std::cout << "sum = " << sum << "\n";
}

void functionParameterDemo() {
    std::cout << "\n=== 7. Span as Function Parameter ===\n";

    int arr[] = {1, 2, 3, 4, 5};
    std::array<int, 5> stdArr = {10, 20, 30, 40, 50};
    std::vector<int> vec = {100, 200, 300};

    // All work with single function!
    processData(arr);
    processData(stdArr);
    processData(vec);

    std::cout << "One function handles all container types!\n";
}

// ==============================================
// 8. Algorithms with Span
// ==============================================

void algorithmsDemo() {
    std::cout << "\n=== 8. Algorithms with Span ===\n";

    std::vector<int> vec = {5, 2, 8, 1, 9, 3, 7};
    std::span<int> span(vec);

    // Sort
    std::sort(span.begin(), span.end());
    std::cout << "After sort: ";
    printSpan(span);

    // Find
    auto it = std::find(span.begin(), span.end(), 8);
    if (it != span.end()) {
        std::cout << "Found 8 at index: " << std::distance(span.begin(), it) << "\n";
    }

    // Transform
    std::transform(span.begin(), span.end(), span.begin(),
                  [](int x) { return x * 2; });
    std::cout << "After *2: ";
    printSpan(span);

    // Accumulate
    int sum = std::accumulate(span.begin(), span.end(), 0);
    std::cout << "Sum: " << sum << "\n";
}

// ==============================================
// 9. Multi-dimensional Data
// ==============================================

class Matrix {
private:
    std::vector<int> data;
    size_t rows, cols;

public:
    Matrix(size_t r, size_t c) : data(r * c), rows(r), cols(c) {}

    void fill(int value) {
        std::fill(data.begin(), data.end(), value);
    }

    std::span<int> getRow(size_t row) {
        return std::span<int>(data.data() + row * cols, cols);
    }

    std::span<const int> getRow(size_t row) const {
        return std::span<const int>(data.data() + row * cols, cols);
    }

    void print() const {
        for (size_t r = 0; r < rows; ++r) {
            auto row = getRow(r);
            std::cout << "  Row " << r << ": ";
            for (int val : row) {
                std::cout << val << " ";
            }
            std::cout << "\n";
        }
    }
};

void multiDimensionalDemo() {
    std::cout << "\n=== 9. Multi-dimensional Data ===\n";

    Matrix mat(3, 4);
    mat.fill(0);

    // Modify specific rows
    auto row0 = mat.getRow(0);
    std::iota(row0.begin(), row0.end(), 1);

    auto row1 = mat.getRow(1);
    std::iota(row1.begin(), row1.end(), 10);

    auto row2 = mat.getRow(2);
    std::iota(row2.begin(), row2.end(), 100);

    std::cout << "Matrix:\n";
    mat.print();
}

// ==============================================
// 10. Bytes Span
// ==============================================

void bytesSpanDemo() {
    std::cout << "\n=== 10. Bytes Span ===\n";

    struct Data {
        int x;
        double y;
        char z;
    };

    Data data{42, 3.14, 'A'};

    // View as bytes
    auto bytes = std::as_bytes(std::span(&data, 1));

    std::cout << "Size in bytes: " << bytes.size() << "\n";
    std::cout << "Bytes (hex): ";
    for (std::byte b : bytes) {
        printf("%02X ", static_cast<unsigned char>(b));
    }
    std::cout << "\n";

    // Writable bytes
    std::vector<int> vec = {1, 2, 3};
    auto writableBytes = std::as_writable_bytes(std::span(vec));
    std::cout << "Writable bytes size: " << writableBytes.size() << "\n";
}

// ==============================================
// 11. Performance Benefits
// ==============================================

// Old way - takes vector by const reference
void processOld(const std::vector<int>& data) {
    int sum = 0;
    for (int val : data) {
        sum += val;
    }
}

// New way - works with any contiguous container
void processNew(std::span<const int> data) {
    int sum = 0;
    for (int val : data) {
        sum += val;
    }
}

void performanceDemo() {
    std::cout << "\n=== 11. Performance Benefits ===\n";

    std::cout << "Benefits of std::span:\n";
    std::cout << "  1. Zero-overhead abstraction\n";
    std::cout << "  2. No copies or allocations\n";
    std::cout << "  3. Works with C-arrays, std::array, std::vector, etc.\n";
    std::cout << "  4. Type-safe alternative to pointer+size\n";
    std::cout << "  5. Bounds checking in debug mode\n";
    std::cout << "  6. Standard algorithms compatible\n";
}

// ==============================================
// 12. Practical Use Cases
// ==============================================

// Image processing with span
void processImageRow(std::span<unsigned char> row) {
    for (auto& pixel : row) {
        pixel = 255 - pixel; // Invert
    }
}

// Configuration reader
struct Config {
    int settings[10];
};

void applyConfig(std::span<const int> settings) {
    std::cout << "Applying " << settings.size() << " settings\n";
    for (size_t i = 0; i < settings.size(); ++i) {
        std::cout << "  Setting[" << i << "] = " << settings[i] << "\n";
    }
}

// Buffer operations
void fillBuffer(std::span<char> buffer, char value) {
    std::fill(buffer.begin(), buffer.end(), value);
}

void useCasesDemo() {
    std::cout << "\n=== 12. Practical Use Cases ===\n";

    // Image row processing
    std::cout << "\n1. Image processing:\n";
    std::vector<unsigned char> imageRow(10, 128);
    std::cout << "Before: ";
    for (auto p : imageRow) std::cout << (int)p << " ";
    std::cout << "\n";

    processImageRow(imageRow);
    std::cout << "After invert: ";
    for (auto p : imageRow) std::cout << (int)p << " ";
    std::cout << "\n";

    // Configuration
    std::cout << "\n2. Configuration:\n";
    Config config{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}};
    applyConfig(std::span(config.settings, 5)); // Apply first 5

    // Buffer operations
    std::cout << "\n3. Buffer operations:\n";
    char buffer[20];
    fillBuffer(buffer, 'X');
    std::cout << "Buffer: " << std::string_view(buffer, 20) << "\n";
}

// ==============================================
// 13. Best Practices
// ==============================================

void bestPracticesDemo() {
    std::cout << "\n=== 13. Best Practices ===\n\n";

    std::cout << "Use std::span for:\n";
    std::cout << "  - Function parameters (contiguous data)\n";
    std::cout << "  - Replacing pointer + size pairs\n";
    std::cout << "  - Generic container algorithms\n";
    std::cout << "  - Zero-copy views of data\n\n";

    std::cout << "Don't use std::span for:\n";
    std::cout << "  - Storing data (use vector, array, etc.)\n";
    std::cout << "  - Non-contiguous containers (list, map, etc.)\n";
    std::cout << "  - Owning resources\n\n";

    std::cout << "Remember:\n";
    std::cout << "  - span is non-owning (like string_view)\n";
    std::cout << "  - Beware dangling references\n";
    std::cout << "  - Use const span for read-only access\n";
    std::cout << "  - Static extent when size is known at compile-time\n";
}

int main() {
    std::cout << "=== C++20 std::span - Non-Owning Array View ===\n";

    // 1. Basics
    spanBasicsDemo();

    // 2. Extents
    extentDemo();

    // 3. Access
    accessDemo();

    // 4. Iterators
    iteratorDemo();

    // 5. Subspans
    subspanDemo();

    // 6. Const spans
    constSpanDemo();

    // 7. Function parameters
    functionParameterDemo();

    // 8. Algorithms
    algorithmsDemo();

    // 9. Multi-dimensional
    multiDimensionalDemo();

    // 10. Bytes
    bytesSpanDemo();

    // 11. Performance
    performanceDemo();

    // 12. Use cases
    useCasesDemo();

    // 13. Best practices
    bestPracticesDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::span is non-owning view of contiguous data (C++20)\n";
    std::cout << "2. Works with arrays, std::array, std::vector, etc.\n";
    std::cout << "3. Static extent (compile-time) or dynamic extent (runtime)\n";
    std::cout << "4. Zero-overhead, type-safe alternative to pointer+size\n";
    std::cout << "5. Supports subspans: first(), last(), subspan()\n";
    std::cout << "6. Perfect for function parameters accepting arrays\n";
    std::cout << "7. Compatible with standard algorithms\n";

    return 0;
}
