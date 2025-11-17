/*
 * Program 142: Vector Operations
 *
 * Demonstrates:
 * - Vector creation and initialization
 * - Capacity vs size
 * - Element access methods
 * - Modifiers (push_back, pop_back, insert, erase, etc.)
 * - Iterators (begin, end, rbegin, rend)
 * - Vector algorithms
 * - Memory management
 * - Performance considerations
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <string>
#include <iomanip>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Print vector contents
template<typename T>
void printVector(const vector<T>& vec, const string& label = "Vector") {
    cout << label << ": ";
    for (const auto& elem : vec) {
        cout << elem << " ";
    }
    cout << "\n";
}

// Demonstrate vector initialization
void vectorInitialization() {
    printSection("1. VECTOR INITIALIZATION");

    // Default construction
    vector<int> v1;
    cout << "Default construction: size = " << v1.size() << "\n";

    // Construction with size
    vector<int> v2(5);
    printVector(v2, "Size constructor (5)");

    // Construction with size and value
    vector<int> v3(5, 10);
    printVector(v3, "Size+value (5, 10)");

    // Initializer list
    vector<int> v4 = {1, 2, 3, 4, 5};
    printVector(v4, "Initializer list");

    // Copy construction
    vector<int> v5(v4);
    printVector(v5, "Copy constructor");

    // Range construction
    vector<int> v6(v4.begin(), v4.begin() + 3);
    printVector(v6, "Range constructor");

    // Fill constructor
    vector<string> v7(3, "hello");
    printVector(v7, "String vector");
}

// Demonstrate capacity operations
void capacityOperations() {
    printSection("2. CAPACITY vs SIZE");

    vector<int> v;

    cout << "\nInitial state:\n";
    cout << "  size: " << v.size() << ", capacity: " << v.capacity() << "\n";

    cout << "\nAdding elements:\n";
    for (int i = 1; i <= 10; i++) {
        v.push_back(i);
        cout << "  After push_back(" << i << "): "
             << "size=" << v.size() << ", capacity=" << v.capacity() << "\n";
    }

    // Reserve capacity
    cout << "\nReserving capacity for 100 elements:\n";
    v.reserve(100);
    cout << "  size: " << v.size() << ", capacity: " << v.capacity() << "\n";

    // Shrink to fit
    cout << "\nShrinking to fit:\n";
    v.shrink_to_fit();
    cout << "  size: " << v.size() << ", capacity: " << v.capacity() << "\n";

    // Resize
    cout << "\nResizing to 15:\n";
    v.resize(15, 99);
    printVector(v, "After resize");
    cout << "  size: " << v.size() << ", capacity: " << v.capacity() << "\n";

    // Check if empty
    cout << "\nIs empty: " << (v.empty() ? "Yes" : "No") << "\n";
}

// Demonstrate element access
void elementAccess() {
    printSection("3. ELEMENT ACCESS");

    vector<int> v = {10, 20, 30, 40, 50};
    printVector(v);

    cout << "\nDifferent access methods:\n";
    cout << "  v[2] = " << v[2] << "\n";
    cout << "  v.at(2) = " << v.at(2) << "\n";
    cout << "  v.front() = " << v.front() << "\n";
    cout << "  v.back() = " << v.back() << "\n";

    // Direct data access
    cout << "  v.data()[2] = " << v.data()[2] << "\n";

    // Range checking with at()
    cout << "\nRange checking:\n";
    try {
        cout << "  Accessing v.at(10)...\n";
        int x = v.at(10);  // Will throw exception
        cout << "  Value: " << x << "\n";
    } catch (const out_of_range& e) {
        cout << "  Exception caught: " << e.what() << "\n";
    }

    // Modifying through access
    cout << "\nModifying elements:\n";
    v[2] = 300;
    v.at(3) = 400;
    printVector(v, "After modification");
}

// Demonstrate modifiers
void modifierOperations() {
    printSection("4. MODIFIER OPERATIONS");

    vector<int> v = {1, 2, 3};

    // push_back and pop_back
    cout << "\npush_back and pop_back:\n";
    printVector(v, "Initial");
    v.push_back(4);
    v.push_back(5);
    printVector(v, "After push_back(4, 5)");
    v.pop_back();
    printVector(v, "After pop_back()");

    // emplace_back (constructs in place)
    cout << "\nemplace_back:\n";
    v.emplace_back(6);
    printVector(v, "After emplace_back(6)");

    // insert
    cout << "\ninsert operations:\n";
    v.insert(v.begin(), 0);
    printVector(v, "Insert at begin");
    v.insert(v.begin() + 3, 99);
    printVector(v, "Insert at position 3");
    v.insert(v.end(), 3, 100);
    printVector(v, "Insert 3x100 at end");

    // erase
    cout << "\nerase operations:\n";
    v.erase(v.begin());
    printVector(v, "Erase first element");
    v.erase(v.begin() + 2, v.begin() + 5);
    printVector(v, "Erase range [2, 5)");

    // assign
    cout << "\nassign operations:\n";
    v.assign(5, 7);
    printVector(v, "Assign 5x7");
    v.assign({1, 2, 3, 4, 5});
    printVector(v, "Assign initializer list");

    // swap
    cout << "\nswap operation:\n";
    vector<int> v2 = {9, 8, 7};
    printVector(v, "v before swap");
    printVector(v2, "v2 before swap");
    v.swap(v2);
    printVector(v, "v after swap");
    printVector(v2, "v2 after swap");

    // clear
    cout << "\nclear operation:\n";
    v.clear();
    cout << "After clear: size = " << v.size()
         << ", capacity = " << v.capacity() << "\n";
}

// Demonstrate iterators
void iteratorOperations() {
    printSection("5. ITERATORS");

    vector<int> v = {1, 2, 3, 4, 5};

    // Forward iteration
    cout << "\nForward iteration (begin to end):\n  ";
    for (auto it = v.begin(); it != v.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    // Reverse iteration
    cout << "\nReverse iteration (rbegin to rend):\n  ";
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    // Const iterators
    cout << "\nConst iteration (cbegin to cend):\n  ";
    for (auto it = v.cbegin(); it != v.cend(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    // Iterator arithmetic
    cout << "\nIterator arithmetic:\n";
    auto it = v.begin();
    cout << "  *begin() = " << *it << "\n";
    cout << "  *(begin() + 2) = " << *(it + 2) << "\n";
    cout << "  *(end() - 1) = " << *(v.end() - 1) << "\n";

    // Distance between iterators
    cout << "  distance(begin, end) = " << (v.end() - v.begin()) << "\n";

    // Modifying through iterators
    cout << "\nModifying through iterators:\n";
    for (auto it = v.begin(); it != v.end(); ++it) {
        *it *= 2;
    }
    printVector(v, "After doubling each element");
}

// Demonstrate algorithms with vectors
void vectorAlgorithms() {
    printSection("6. ALGORITHMS WITH VECTORS");

    vector<int> v = {5, 2, 8, 1, 9, 3, 7, 4, 6};

    // Sort
    cout << "\nSorting:\n";
    printVector(v, "Original");
    sort(v.begin(), v.end());
    printVector(v, "After sort (ascending)");
    sort(v.begin(), v.end(), greater<int>());
    printVector(v, "After sort (descending)");

    // Reverse
    cout << "\nReverse:\n";
    reverse(v.begin(), v.end());
    printVector(v, "After reverse");

    // Find
    cout << "\nFind:\n";
    auto it = find(v.begin(), v.end(), 5);
    if (it != v.end()) {
        cout << "  Found 5 at position " << (it - v.begin()) << "\n";
    }

    // Binary search (requires sorted)
    cout << "\nBinary search (on sorted vector):\n";
    sort(v.begin(), v.end());
    printVector(v, "Sorted");
    bool found = binary_search(v.begin(), v.end(), 5);
    cout << "  binary_search for 5: " << (found ? "Found" : "Not found") << "\n";

    // Min/Max
    cout << "\nMin/Max:\n";
    cout << "  min_element: " << *min_element(v.begin(), v.end()) << "\n";
    cout << "  max_element: " << *max_element(v.begin(), v.end()) << "\n";

    // Count
    v.push_back(5);
    v.push_back(5);
    cout << "\nCount:\n";
    printVector(v);
    cout << "  count of 5: " << count(v.begin(), v.end(), 5) << "\n";

    // Accumulate (sum)
    cout << "\nAccumulate:\n";
    int sum = accumulate(v.begin(), v.end(), 0);
    cout << "  Sum of all elements: " << sum << "\n";

    // Transform
    cout << "\nTransform (square each element):\n";
    vector<int> squared(v.size());
    transform(v.begin(), v.end(), squared.begin(),
              [](int x) { return x * x; });
    printVector(squared, "Squared");

    // Remove and erase idiom
    cout << "\nRemove-erase idiom (remove all 5s):\n";
    printVector(v, "Before");
    v.erase(remove(v.begin(), v.end(), 5), v.end());
    printVector(v, "After remove-erase");
}

// Demonstrate 2D vectors
void twoDimensionalVectors() {
    printSection("7. 2D VECTORS (Vector of Vectors)");

    // Create 3x4 matrix
    vector<vector<int>> matrix(3, vector<int>(4, 0));

    // Fill with values
    int value = 1;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            matrix[i][j] = value++;
        }
    }

    // Print matrix
    cout << "\n3x4 Matrix:\n";
    for (const auto& row : matrix) {
        for (int val : row) {
            cout << setw(3) << val << " ";
        }
        cout << "\n";
    }

    // Jagged array (rows of different sizes)
    cout << "\nJagged array:\n";
    vector<vector<int>> jagged;
    jagged.push_back({1});
    jagged.push_back({2, 3});
    jagged.push_back({4, 5, 6});

    for (size_t i = 0; i < jagged.size(); i++) {
        cout << "  Row " << i << ": ";
        for (int val : jagged[i]) {
            cout << val << " ";
        }
        cout << "\n";
    }
}

// Performance tips
void performanceTips() {
    printSection("8. PERFORMANCE TIPS");

    cout << "\n1. Reserve capacity when size is known:\n";
    cout << "   v.reserve(1000);  // Avoid multiple reallocations\n";

    cout << "\n2. Use emplace_back instead of push_back:\n";
    cout << "   v.emplace_back(args...);  // Constructs in place\n";

    cout << "\n3. Pass vectors by const reference:\n";
    cout << "   void func(const vector<int>& v);  // Avoid copying\n";

    cout << "\n4. Use shrink_to_fit to free excess capacity:\n";
    cout << "   v.shrink_to_fit();  // After many deletions\n";

    cout << "\n5. Prefer range-based for loops:\n";
    cout << "   for (const auto& elem : v) { }  // More readable\n";

    cout << "\n6. Use algorithms instead of manual loops:\n";
    cout << "   sort(v.begin(), v.end());  // Optimized implementation\n";

    cout << "\n7. Avoid frequent insertions in the middle:\n";
    cout << "   Consider list or deque if needed\n";
}

int main() {
    cout << "VECTOR OPERATIONS COMPREHENSIVE GUIDE\n";
    cout << "=====================================\n";

    vectorInitialization();
    capacityOperations();
    elementAccess();
    modifierOperations();
    iteratorOperations();
    vectorAlgorithms();
    twoDimensionalVectors();
    performanceTips();

    printSection("SUMMARY");
    cout << "\nVector is the most commonly used STL container:\n";
    cout << "- Dynamic array with automatic memory management\n";
    cout << "- Fast random access O(1)\n";
    cout << "- Efficient insertion/deletion at end O(1) amortized\n";
    cout << "- Use reserve() to optimize performance\n";
    cout << "- Rich set of algorithms available\n";

    return 0;
}
