/*
 * Program 141: STL Containers Overview
 *
 * Demonstrates:
 * - Overview of STL container categories
 * - Sequence containers (vector, deque, list, array, forward_list)
 * - Associative containers (set, map, multiset, multimap)
 * - Unordered containers (unordered_set, unordered_map, etc.)
 * - Container adapters (stack, queue, priority_queue)
 * - Container characteristics and performance
 * - Common operations across containers
 */

#include <iostream>
#include <vector>
#include <deque>
#include <list>
#include <array>
#include <forward_list>
#include <set>
#include <map>
#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <queue>
#include <algorithm>
#include <string>
#include <iomanip>

using namespace std;

// Helper function to print section headers
void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Demonstrate sequence containers
void demonstrateSequenceContainers() {
    printSection("1. SEQUENCE CONTAINERS");

    // Vector - dynamic array, random access
    cout << "\n--- Vector (Dynamic Array) ---\n";
    vector<int> vec = {1, 2, 3, 4, 5};
    cout << "Vector: ";
    for (int x : vec) cout << x << " ";
    cout << "\nRandom access: vec[2] = " << vec[2] << "\n";
    cout << "Characteristics: Fast random access, efficient at end\n";

    // Deque - double-ended queue
    cout << "\n--- Deque (Double-Ended Queue) ---\n";
    deque<int> dq = {1, 2, 3, 4, 5};
    dq.push_front(0);
    dq.push_back(6);
    cout << "Deque: ";
    for (int x : dq) cout << x << " ";
    cout << "\nCharacteristics: Fast insertion at both ends\n";

    // List - doubly linked list
    cout << "\n--- List (Doubly Linked List) ---\n";
    list<int> lst = {1, 2, 3, 4, 5};
    lst.push_front(0);
    lst.push_back(6);
    cout << "List: ";
    for (int x : lst) cout << x << " ";
    cout << "\nCharacteristics: Fast insertion/deletion anywhere\n";

    // Array - fixed-size array
    cout << "\n--- Array (Fixed-Size Array) ---\n";
    array<int, 5> arr = {1, 2, 3, 4, 5};
    cout << "Array: ";
    for (int x : arr) cout << x << " ";
    cout << "\nCharacteristics: Fixed size, stack allocated\n";

    // Forward List - singly linked list
    cout << "\n--- Forward List (Singly Linked List) ---\n";
    forward_list<int> flst = {1, 2, 3, 4, 5};
    cout << "Forward List: ";
    for (int x : flst) cout << x << " ";
    cout << "\nCharacteristics: Memory efficient, forward iteration only\n";
}

// Demonstrate associative containers
void demonstrateAssociativeContainers() {
    printSection("2. ASSOCIATIVE CONTAINERS (Ordered)");

    // Set - unique sorted elements
    cout << "\n--- Set (Unique Sorted Elements) ---\n";
    set<int> s = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Set: ";
    for (int x : s) cout << x << " ";
    cout << "\nCharacteristics: Unique elements, O(log n) operations\n";

    // Multiset - sorted elements with duplicates
    cout << "\n--- Multiset (Sorted with Duplicates) ---\n";
    multiset<int> ms = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Multiset: ";
    for (int x : ms) cout << x << " ";
    cout << "\nCharacteristics: Allows duplicates, sorted\n";

    // Map - key-value pairs, unique keys
    cout << "\n--- Map (Key-Value Pairs) ---\n";
    map<string, int> m = {{"apple", 3}, {"banana", 2}, {"cherry", 5}};
    cout << "Map:\n";
    for (const auto& [key, value] : m) {
        cout << "  " << key << ": " << value << "\n";
    }
    cout << "Characteristics: Unique keys, sorted by key\n";

    // Multimap - key-value pairs, duplicate keys allowed
    cout << "\n--- Multimap (Multiple Values per Key) ---\n";
    multimap<string, int> mm = {{"fruit", 1}, {"fruit", 2}, {"veg", 3}};
    cout << "Multimap:\n";
    for (const auto& [key, value] : mm) {
        cout << "  " << key << ": " << value << "\n";
    }
    cout << "Characteristics: Allows duplicate keys\n";
}

// Demonstrate unordered containers
void demonstrateUnorderedContainers() {
    printSection("3. UNORDERED CONTAINERS (Hash-Based)");

    // Unordered Set
    cout << "\n--- Unordered Set ---\n";
    unordered_set<int> us = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Unordered Set: ";
    for (int x : us) cout << x << " ";
    cout << "\nCharacteristics: Unique elements, O(1) average operations\n";

    // Unordered Map
    cout << "\n--- Unordered Map ---\n";
    unordered_map<string, int> um = {{"apple", 3}, {"banana", 2}};
    cout << "Unordered Map:\n";
    for (const auto& [key, value] : um) {
        cout << "  " << key << ": " << value << "\n";
    }
    cout << "Characteristics: Fast lookup, no ordering guarantee\n";
}

// Demonstrate container adapters
void demonstrateContainerAdapters() {
    printSection("4. CONTAINER ADAPTERS");

    // Stack - LIFO
    cout << "\n--- Stack (LIFO) ---\n";
    stack<int> stk;
    for (int i = 1; i <= 5; i++) stk.push(i);
    cout << "Stack (top to bottom): ";
    stack<int> temp = stk;
    while (!temp.empty()) {
        cout << temp.top() << " ";
        temp.pop();
    }
    cout << "\nCharacteristics: Last In First Out\n";

    // Queue - FIFO
    cout << "\n--- Queue (FIFO) ---\n";
    queue<int> q;
    for (int i = 1; i <= 5; i++) q.push(i);
    cout << "Queue (front to back): ";
    queue<int> tempq = q;
    while (!tempq.empty()) {
        cout << tempq.front() << " ";
        tempq.pop();
    }
    cout << "\nCharacteristics: First In First Out\n";

    // Priority Queue - heap-based
    cout << "\n--- Priority Queue (Max Heap) ---\n";
    priority_queue<int> pq;
    for (int x : {3, 1, 4, 1, 5, 9, 2, 6}) pq.push(x);
    cout << "Priority Queue (highest to lowest): ";
    priority_queue<int> temppq = pq;
    while (!temppq.empty()) {
        cout << temppq.top() << " ";
        temppq.pop();
    }
    cout << "\nCharacteristics: Always provides highest priority element\n";
}

// Demonstrate common container operations
void demonstrateCommonOperations() {
    printSection("5. COMMON CONTAINER OPERATIONS");

    vector<int> v = {1, 2, 3, 4, 5};

    cout << "\nSize operations:\n";
    cout << "  size(): " << v.size() << "\n";
    cout << "  empty(): " << (v.empty() ? "true" : "false") << "\n";
    cout << "  max_size(): " << v.max_size() << "\n";

    cout << "\nElement access:\n";
    cout << "  front(): " << v.front() << "\n";
    cout << "  back(): " << v.back() << "\n";
    cout << "  at(2): " << v.at(2) << "\n";

    cout << "\nModifiers:\n";
    v.push_back(6);
    cout << "  After push_back(6): size = " << v.size() << "\n";
    v.pop_back();
    cout << "  After pop_back(): size = " << v.size() << "\n";

    cout << "\nIterators:\n";
    cout << "  Using iterators: ";
    for (auto it = v.begin(); it != v.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";
}

// Performance comparison
void performanceComparison() {
    printSection("6. PERFORMANCE CHARACTERISTICS");

    cout << "\n" << left << setw(25) << "Operation"
         << setw(12) << "Vector"
         << setw(12) << "Deque"
         << setw(12) << "List"
         << setw(12) << "Set/Map" << "\n";
    cout << string(60, '-') << "\n";

    cout << setw(25) << "Random Access"
         << setw(12) << "O(1)"
         << setw(12) << "O(1)"
         << setw(12) << "O(n)"
         << setw(12) << "O(log n)" << "\n";

    cout << setw(25) << "Insert/Delete at End"
         << setw(12) << "O(1)"
         << setw(12) << "O(1)"
         << setw(12) << "O(1)"
         << setw(12) << "O(log n)" << "\n";

    cout << setw(25) << "Insert/Delete at Begin"
         << setw(12) << "O(n)"
         << setw(12) << "O(1)"
         << setw(12) << "O(1)"
         << setw(12) << "O(log n)" << "\n";

    cout << setw(25) << "Insert/Delete Middle"
         << setw(12) << "O(n)"
         << setw(12) << "O(n)"
         << setw(12) << "O(1)*"
         << setw(12) << "O(log n)" << "\n";

    cout << setw(25) << "Search"
         << setw(12) << "O(n)"
         << setw(12) << "O(n)"
         << setw(12) << "O(n)"
         << setw(12) << "O(log n)" << "\n";

    cout << "\n* O(1) if iterator position is known\n";

    cout << "\nUnordered Containers (Hash-based):\n";
    cout << "  Average case: O(1) for insert, delete, search\n";
    cout << "  Worst case: O(n) when hash collisions occur\n";
}

// Container selection guidelines
void containerSelectionGuidelines() {
    printSection("7. CONTAINER SELECTION GUIDELINES");

    cout << "\nChoose Vector when:\n";
    cout << "  - You need random access\n";
    cout << "  - Elements are mostly added/removed at the end\n";
    cout << "  - Memory locality is important\n";

    cout << "\nChoose Deque when:\n";
    cout << "  - You need random access\n";
    cout << "  - Elements are added/removed at both ends\n";

    cout << "\nChoose List when:\n";
    cout << "  - Frequent insertion/deletion in the middle\n";
    cout << "  - No need for random access\n";
    cout << "  - Iterator stability is important\n";

    cout << "\nChoose Set/Map when:\n";
    cout << "  - You need sorted data\n";
    cout << "  - Fast search is required\n";
    cout << "  - Unique elements (set) or unique keys (map)\n";

    cout << "\nChoose Unordered Set/Map when:\n";
    cout << "  - Fastest possible lookup\n";
    cout << "  - Order doesn't matter\n";
    cout << "  - Have a good hash function\n";

    cout << "\nChoose Stack/Queue when:\n";
    cout << "  - You need LIFO (stack) or FIFO (queue) semantics\n";
    cout << "  - Limited interface is acceptable\n";
}

int main() {
    cout << "STL CONTAINERS COMPREHENSIVE OVERVIEW\n";
    cout << "=====================================\n";

    demonstrateSequenceContainers();
    demonstrateAssociativeContainers();
    demonstrateUnorderedContainers();
    demonstrateContainerAdapters();
    demonstrateCommonOperations();
    performanceComparison();
    containerSelectionGuidelines();

    printSection("SUMMARY");
    cout << "\nSTL provides a rich set of container types:\n";
    cout << "- Sequence: vector, deque, list, array, forward_list\n";
    cout << "- Associative: set, map, multiset, multimap\n";
    cout << "- Unordered: unordered_set, unordered_map, etc.\n";
    cout << "- Adapters: stack, queue, priority_queue\n";
    cout << "\nChoose based on your access patterns and performance needs!\n";

    return 0;
}
