/*
 * Program 144: Deque (Double-Ended Queue)
 *
 * Demonstrates:
 * - Deque creation and initialization
 * - Double-ended operations (push/pop at both ends)
 * - Random access capabilities
 * - Deque vs vector vs list comparison
 * - Memory layout and performance
 * - Use cases for deques
 * - Iterator operations
 */

#include <iostream>
#include <deque>
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

template<typename T>
void printDeque(const deque<T>& dq, const string& label = "Deque") {
    cout << label << ": ";
    for (const auto& elem : dq) {
        cout << elem << " ";
    }
    cout << "\n";
}

// Demonstrate deque initialization
void dequeInitialization() {
    printSection("1. DEQUE INITIALIZATION");

    // Default construction
    deque<int> d1;
    cout << "Default: size = " << d1.size() << "\n";

    // Size constructor
    deque<int> d2(5);
    printDeque(d2, "Size(5)");

    // Size with value
    deque<int> d3(5, 10);
    printDeque(d3, "Size+value(5,10)");

    // Initializer list
    deque<int> d4 = {1, 2, 3, 4, 5};
    printDeque(d4, "Initializer list");

    // Copy construction
    deque<int> d5(d4);
    printDeque(d5, "Copy");

    // Range construction
    deque<int> d6(d4.begin(), d4.begin() + 3);
    printDeque(d6, "Range [0,3)");
}

// Demonstrate double-ended operations
void doubleEndedOperations() {
    printSection("2. DOUBLE-ENDED OPERATIONS");

    deque<int> dq = {3, 4, 5};
    printDeque(dq, "Initial");

    cout << "\nPush operations at both ends:\n";
    dq.push_back(6);
    printDeque(dq, "After push_back(6)");

    dq.push_back(7);
    printDeque(dq, "After push_back(7)");

    dq.push_front(2);
    printDeque(dq, "After push_front(2)");

    dq.push_front(1);
    printDeque(dq, "After push_front(1)");

    dq.push_front(0);
    printDeque(dq, "After push_front(0)");

    cout << "\nEmplace operations (construct in-place):\n";
    dq.emplace_back(8);
    printDeque(dq, "After emplace_back(8)");

    dq.emplace_front(-1);
    printDeque(dq, "After emplace_front(-1)");

    cout << "\nPop operations at both ends:\n";
    dq.pop_back();
    printDeque(dq, "After pop_back()");

    dq.pop_front();
    printDeque(dq, "After pop_front()");

    cout << "\nAccess front and back:\n";
    cout << "  front(): " << dq.front() << "\n";
    cout << "  back(): " << dq.back() << "\n";
}

// Demonstrate random access
void randomAccessOperations() {
    printSection("3. RANDOM ACCESS OPERATIONS");

    deque<int> dq = {10, 20, 30, 40, 50, 60, 70};
    printDeque(dq);

    cout << "\nRandom access methods:\n";
    cout << "  dq[3] = " << dq[3] << "\n";
    cout << "  dq.at(3) = " << dq.at(3) << "\n";

    cout << "\nModifying via random access:\n";
    dq[3] = 400;
    dq.at(5) = 600;
    printDeque(dq, "After modification");

    cout << "\nBounds checking with at():\n";
    try {
        cout << "  Accessing dq.at(100)...\n";
        int x = dq.at(100);
        cout << "  Value: " << x << "\n";
    } catch (const out_of_range& e) {
        cout << "  Exception: " << e.what() << "\n";
    }

    cout << "\nIterator arithmetic (random access):\n";
    auto it = dq.begin();
    cout << "  *(begin()) = " << *it << "\n";
    cout << "  *(begin() + 3) = " << *(it + 3) << "\n";
    cout << "  *(end() - 1) = " << *(dq.end() - 1) << "\n";
    cout << "  Distance: " << (dq.end() - dq.begin()) << "\n";
}

// Demonstrate insert and erase
void insertEraseOperations() {
    printSection("4. INSERT AND ERASE OPERATIONS");

    deque<int> dq = {1, 2, 3, 4, 5};

    cout << "\nInsert operations:\n";
    printDeque(dq, "Initial");

    dq.insert(dq.begin(), 0);
    printDeque(dq, "Insert 0 at begin");

    auto it = dq.begin() + 3;
    dq.insert(it, 99);
    printDeque(dq, "Insert 99 at pos 3");

    dq.insert(dq.end(), 3, 100);
    printDeque(dq, "Insert 3x100 at end");

    deque<int> extras = {-1, -2, -3};
    dq.insert(dq.begin(), extras.begin(), extras.end());
    printDeque(dq, "Insert range at begin");

    cout << "\nErase operations:\n";
    dq.erase(dq.begin());
    printDeque(dq, "Erase first element");

    it = dq.begin() + 2;
    auto it2 = it + 3;
    dq.erase(it, it2);
    printDeque(dq, "Erase range [2,5)");

    cout << "\nResize operations:\n";
    dq.resize(10, 7);
    printDeque(dq, "Resize to 10 (fill 7)");

    dq.resize(5);
    printDeque(dq, "Resize to 5 (truncate)");
}

// Demonstrate iterators
void iteratorOperations() {
    printSection("5. ITERATOR OPERATIONS");

    deque<int> dq = {1, 2, 3, 4, 5};

    cout << "\nForward iteration:\n  ";
    for (auto it = dq.begin(); it != dq.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nReverse iteration:\n  ";
    for (auto it = dq.rbegin(); it != dq.rend(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nConst iteration:\n  ";
    for (auto it = dq.cbegin(); it != dq.cend(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nModifying through iterators:\n";
    for (auto it = dq.begin(); it != dq.end(); ++it) {
        *it *= 10;
    }
    printDeque(dq, "After multiplying by 10");

    cout << "\nRandom access with iterators:\n";
    auto it = dq.begin();
    cout << "  begin()[2] = " << it[2] << "\n";

    advance(it, 3);
    cout << "  After advance(3): " << *it << "\n";
}

// Demonstrate algorithms with deque
void dequeAlgorithms() {
    printSection("6. ALGORITHMS WITH DEQUE");

    deque<int> dq = {5, 2, 8, 1, 9, 3, 7, 4, 6};

    cout << "\nSorting:\n";
    printDeque(dq, "Original");
    sort(dq.begin(), dq.end());
    printDeque(dq, "Sorted ascending");

    sort(dq.begin(), dq.end(), greater<int>());
    printDeque(dq, "Sorted descending");

    cout << "\nReverse:\n";
    reverse(dq.begin(), dq.end());
    printDeque(dq, "After reverse");

    cout << "\nFind:\n";
    auto it = find(dq.begin(), dq.end(), 5);
    if (it != dq.end()) {
        cout << "  Found 5 at position " << (it - dq.begin()) << "\n";
    }

    cout << "\nBinary search (on sorted):\n";
    sort(dq.begin(), dq.end());
    printDeque(dq, "Sorted");
    bool found = binary_search(dq.begin(), dq.end(), 7);
    cout << "  binary_search(7): " << (found ? "Found" : "Not found") << "\n";

    cout << "\nMin/Max:\n";
    cout << "  min: " << *min_element(dq.begin(), dq.end()) << "\n";
    cout << "  max: " << *max_element(dq.begin(), dq.end()) << "\n";

    cout << "\nAccumulate:\n";
    int sum = accumulate(dq.begin(), dq.end(), 0);
    cout << "  Sum: " << sum << "\n";

    cout << "\nTransform (square each):\n";
    deque<int> squared(dq.size());
    transform(dq.begin(), dq.end(), squared.begin(),
              [](int x) { return x * x; });
    printDeque(squared, "Squared");

    cout << "\nPartition (odds first):\n";
    printDeque(dq, "Before partition");
    auto pivot = partition(dq.begin(), dq.end(),
                          [](int x) { return x % 2 == 1; });
    printDeque(dq, "After partition");
    cout << "  Pivot at position " << (pivot - dq.begin()) << "\n";
}

// Deque as a queue and stack
void dequeAsAdapter() {
    printSection("7. DEQUE AS QUEUE/STACK");

    cout << "\nUsing deque as QUEUE (FIFO):\n";
    deque<int> queue;
    cout << "  Enqueue: 1, 2, 3, 4, 5\n";
    for (int i = 1; i <= 5; i++) {
        queue.push_back(i);  // Enqueue at back
    }

    cout << "  Dequeue: ";
    while (!queue.empty()) {
        cout << queue.front() << " ";  // Dequeue from front
        queue.pop_front();
    }
    cout << "\n";

    cout << "\nUsing deque as STACK (LIFO):\n";
    deque<int> stack;
    cout << "  Push: 1, 2, 3, 4, 5\n";
    for (int i = 1; i <= 5; i++) {
        stack.push_back(i);  // Push at back
    }

    cout << "  Pop: ";
    while (!stack.empty()) {
        cout << stack.back() << " ";  // Pop from back
        stack.pop_back();
    }
    cout << "\n";

    cout << "\nSliding window pattern:\n";
    deque<int> window;
    deque<int> data = {1, 3, 2, 5, 4, 6, 8, 7, 9};
    int k = 3;  // Window size

    cout << "  Data: ";
    printDeque(data);
    cout << "  Window size: " << k << "\n";
    cout << "  Window maximums: ";

    for (size_t i = 0; i < data.size(); i++) {
        // Remove elements outside window
        while (!window.empty() && window.front() <= static_cast<int>(i) - k) {
            window.pop_front();
        }

        // Remove smaller elements (not needed)
        while (!window.empty() && data[window.back()] <= data[i]) {
            window.pop_back();
        }

        window.push_back(i);

        if (i >= static_cast<size_t>(k) - 1) {
            cout << data[window.front()] << " ";
        }
    }
    cout << "\n";
}

// Performance comparison
void performanceComparison() {
    printSection("8. DEQUE vs VECTOR vs LIST");

    cout << "\n" << left << setw(25) << "Operation"
         << setw(15) << "Vector"
         << setw(15) << "Deque"
         << setw(15) << "List" << "\n";
    cout << string(70, '-') << "\n";

    cout << setw(25) << "Random Access"
         << setw(15) << "O(1)"
         << setw(15) << "O(1)"
         << setw(15) << "O(n)" << "\n";

    cout << setw(25) << "Insert/Delete at End"
         << setw(15) << "O(1) amort"
         << setw(15) << "O(1)"
         << setw(15) << "O(1)" << "\n";

    cout << setw(25) << "Insert/Delete at Begin"
         << setw(15) << "O(n)"
         << setw(15) << "O(1)"
         << setw(15) << "O(1)" << "\n";

    cout << setw(25) << "Insert/Delete Middle"
         << setw(15) << "O(n)"
         << setw(15) << "O(n)"
         << setw(15) << "O(1)*" << "\n";

    cout << setw(25) << "Iterator Stability"
         << setw(15) << "No"
         << setw(15) << "No"
         << setw(15) << "Yes" << "\n";

    cout << setw(25) << "Memory Layout"
         << setw(15) << "Contiguous"
         << setw(15) << "Chunked"
         << setw(15) << "Scattered" << "\n";

    cout << "\n* With iterator position known\n";
}

// Use cases
void useCases() {
    printSection("9. WHEN TO USE DEQUE");

    cout << "\nChoose DEQUE when:\n";
    cout << "  1. Need to add/remove from both ends frequently\n";
    cout << "  2. Need random access capability\n";
    cout << "  3. Implementing queue or double-ended queue\n";
    cout << "  4. Sliding window algorithms\n";
    cout << "  5. No need for iterator stability\n";

    cout << "\nDEQUE advantages over VECTOR:\n";
    cout << "  - O(1) insertion/deletion at front\n";
    cout << "  - No need to move elements when growing\n";
    cout << "  - Better performance for frequent front operations\n";

    cout << "\nDEQUE advantages over LIST:\n";
    cout << "  - O(1) random access\n";
    cout << "  - Better cache locality (chunked allocation)\n";
    cout << "  - Less memory overhead per element\n";

    cout << "\nDEQUE disadvantages:\n";
    cout << "  - More complex implementation\n";
    cout << "  - Slightly slower than vector for random access\n";
    cout << "  - Iterators may be invalidated on insert/erase\n";
    cout << "  - Not contiguous in memory\n";

    cout << "\nTypical use cases:\n";
    cout << "  - Task scheduling queues\n";
    cout << "  - Browser history (back/forward)\n";
    cout << "  - Palindrome checkers\n";
    cout << "  - Sliding window problems\n";
    cout << "  - BFS algorithms\n";
}

int main() {
    cout << "DEQUE OPERATIONS COMPREHENSIVE GUIDE\n";
    cout << "====================================\n";

    dequeInitialization();
    doubleEndedOperations();
    randomAccessOperations();
    insertEraseOperations();
    iteratorOperations();
    dequeAlgorithms();
    dequeAsAdapter();
    performanceComparison();
    useCases();

    printSection("SUMMARY");
    cout << "\nDeque (Double-Ended Queue) combines:\n";
    cout << "- O(1) insertion/deletion at both ends\n";
    cout << "- O(1) random access like vector\n";
    cout << "- Chunked memory allocation\n";
    cout << "- Best choice for queue-like operations with random access\n";
    cout << "\nRemember: std::queue adapter uses deque by default!\n";

    return 0;
}
