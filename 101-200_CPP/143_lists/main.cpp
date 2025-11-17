/*
 * Program 143: Lists (Doubly and Singly Linked Lists)
 *
 * Demonstrates:
 * - std::list (doubly linked list)
 * - std::forward_list (singly linked list)
 * - List operations (insert, erase, splice, merge)
 * - List-specific algorithms (sort, reverse, unique)
 * - Bidirectional vs forward-only iteration
 * - Performance characteristics
 * - When to use lists vs vectors
 */

#include <iostream>
#include <list>
#include <forward_list>
#include <algorithm>
#include <string>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

template<typename T>
void printList(const list<T>& lst, const string& label = "List") {
    cout << label << ": ";
    for (const auto& elem : lst) {
        cout << elem << " ";
    }
    cout << "\n";
}

template<typename T>
void printForwardList(const forward_list<T>& flst, const string& label = "FList") {
    cout << label << ": ";
    for (const auto& elem : flst) {
        cout << elem << " ";
    }
    cout << "\n";
}

// Demonstrate list initialization
void listInitialization() {
    printSection("1. LIST INITIALIZATION");

    // Default construction
    list<int> l1;
    cout << "Default: size = " << l1.size() << "\n";

    // Size constructor
    list<int> l2(5);
    printList(l2, "Size(5)");

    // Size with value
    list<int> l3(5, 10);
    printList(l3, "Size+value(5,10)");

    // Initializer list
    list<int> l4 = {1, 2, 3, 4, 5};
    printList(l4, "Initializer list");

    // Copy construction
    list<int> l5(l4);
    printList(l5, "Copy");

    // Range construction
    list<int> l6(l4.begin(), next(l4.begin(), 3));
    printList(l6, "Range");
}

// Demonstrate list element access and modifiers
void listModifiers() {
    printSection("2. LIST MODIFIERS");

    list<int> lst = {1, 2, 3, 4, 5};

    cout << "\nBasic access:\n";
    cout << "  front(): " << lst.front() << "\n";
    cout << "  back(): " << lst.back() << "\n";

    cout << "\npush/pop operations:\n";
    printList(lst, "Initial");
    lst.push_back(6);
    printList(lst, "After push_back(6)");
    lst.push_front(0);
    printList(lst, "After push_front(0)");
    lst.pop_back();
    printList(lst, "After pop_back()");
    lst.pop_front();
    printList(lst, "After pop_front()");

    cout << "\nemplace operations:\n";
    lst.emplace_back(6);
    lst.emplace_front(0);
    printList(lst, "After emplace_back/front");

    cout << "\ninsert operations:\n";
    auto it = lst.begin();
    advance(it, 2);
    lst.insert(it, 99);
    printList(lst, "Insert 99 at position 2");

    lst.insert(lst.begin(), 3, -1);
    printList(lst, "Insert 3x(-1) at begin");

    cout << "\nerase operations:\n";
    lst.erase(lst.begin());
    printList(lst, "Erase first");

    it = lst.begin();
    advance(it, 2);
    auto it2 = it;
    advance(it2, 3);
    lst.erase(it, it2);
    printList(lst, "Erase range");

    cout << "\nresize operation:\n";
    lst.resize(10, 7);
    printList(lst, "Resize to 10 (fill with 7)");

    cout << "\nclear operation:\n";
    lst.clear();
    cout << "After clear: size = " << lst.size() << "\n";
}

// Demonstrate list-specific operations
void listSpecificOperations() {
    printSection("3. LIST-SPECIFIC OPERATIONS");

    // Remove
    cout << "\nremove operation:\n";
    list<int> lst = {1, 2, 3, 2, 4, 2, 5};
    printList(lst, "Original");
    lst.remove(2);
    printList(lst, "After remove(2)");

    // Remove_if
    cout << "\nremove_if operation:\n";
    lst = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    printList(lst, "Original");
    lst.remove_if([](int x) { return x % 2 == 0; });
    printList(lst, "After remove_if (evens)");

    // Unique
    cout << "\nunique operation:\n";
    lst = {1, 1, 2, 2, 2, 3, 4, 4, 5};
    printList(lst, "Original");
    lst.unique();
    printList(lst, "After unique()");

    // Sort
    cout << "\nsort operation:\n";
    lst = {5, 2, 8, 1, 9, 3};
    printList(lst, "Original");
    lst.sort();
    printList(lst, "After sort()");
    lst.sort(greater<int>());
    printList(lst, "After sort(greater)");

    // Reverse
    cout << "\nreverse operation:\n";
    lst.reverse();
    printList(lst, "After reverse()");
}

// Demonstrate splice operation
void spliceOperations() {
    printSection("4. SPLICE OPERATIONS");

    // Splice entire list
    cout << "\nSplice entire list:\n";
    list<int> l1 = {1, 2, 3};
    list<int> l2 = {4, 5, 6};
    printList(l1, "l1 before");
    printList(l2, "l2 before");
    l1.splice(l1.end(), l2);
    printList(l1, "l1 after splice");
    printList(l2, "l2 after splice");

    // Splice single element
    cout << "\nSplice single element:\n";
    l1 = {1, 2, 3, 4, 5};
    l2 = {10, 20, 30};
    auto it = l2.begin();
    advance(it, 1);  // Point to 20
    l1.splice(l1.begin(), l2, it);
    printList(l1, "l1 after splice element");
    printList(l2, "l2 after splice element");

    // Splice range
    cout << "\nSplice range:\n";
    l1 = {1, 2, 3};
    l2 = {10, 20, 30, 40, 50};
    auto first = l2.begin();
    auto last = l2.begin();
    advance(first, 1);  // Point to 20
    advance(last, 4);   // Point to 50
    l1.splice(l1.end(), l2, first, last);
    printList(l1, "l1 after splice range");
    printList(l2, "l2 after splice range");
}

// Demonstrate merge operation
void mergeOperations() {
    printSection("5. MERGE OPERATIONS");

    cout << "\nMerge two sorted lists:\n";
    list<int> l1 = {1, 3, 5, 7};
    list<int> l2 = {2, 4, 6, 8};
    printList(l1, "l1 (sorted)");
    printList(l2, "l2 (sorted)");
    l1.merge(l2);
    printList(l1, "After merge");
    printList(l2, "l2 (now empty)");

    cout << "\nMerge with custom comparator:\n";
    l1 = {7, 5, 3, 1};
    l2 = {8, 6, 4, 2};
    printList(l1, "l1 (sorted desc)");
    printList(l2, "l2 (sorted desc)");
    l1.merge(l2, greater<int>());
    printList(l1, "After merge (desc)");
}

// Demonstrate forward_list
void forwardListOperations() {
    printSection("6. FORWARD_LIST (Singly Linked List)");

    cout << "\nInitialization:\n";
    forward_list<int> flst = {1, 2, 3, 4, 5};
    printForwardList(flst, "Initial");

    cout << "\nfront operations (no back()):\n";
    cout << "  front(): " << flst.front() << "\n";
    flst.push_front(0);
    printForwardList(flst, "After push_front(0)");
    flst.pop_front();
    printForwardList(flst, "After pop_front()");

    cout << "\ninsert_after and erase_after:\n";
    auto it = flst.begin();
    flst.insert_after(it, 99);
    printForwardList(flst, "Insert 99 after begin");

    flst.erase_after(it);
    printForwardList(flst, "Erase after begin");

    cout << "\nforward_list specific operations:\n";
    flst = {1, 2, 2, 3, 3, 3, 4};
    printForwardList(flst, "Original");
    flst.unique();
    printForwardList(flst, "After unique()");

    flst.remove(3);
    printForwardList(flst, "After remove(3)");

    flst = {5, 2, 8, 1, 9};
    flst.sort();
    printForwardList(flst, "After sort()");

    flst.reverse();
    printForwardList(flst, "After reverse()");

    cout << "\nbefore_begin() iterator:\n";
    cout << "  Allows insertion at true beginning\n";
    flst.insert_after(flst.before_begin(), -1);
    printForwardList(flst, "Insert after before_begin");
}

// Demonstrate iterators
void iteratorOperations() {
    printSection("7. ITERATOR OPERATIONS");

    list<int> lst = {1, 2, 3, 4, 5};

    cout << "\nBidirectional iteration (list):\n";
    cout << "  Forward: ";
    for (auto it = lst.begin(); it != lst.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "  Reverse: ";
    for (auto it = lst.rbegin(); it != lst.rend(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nadvance and distance:\n";
    auto it = lst.begin();
    advance(it, 2);
    cout << "  After advance(2): " << *it << "\n";
    cout << "  Distance from begin: " << distance(lst.begin(), it) << "\n";

    cout << "\nForward-only iteration (forward_list):\n";
    forward_list<int> flst = {1, 2, 3, 4, 5};
    cout << "  Forward: ";
    for (auto it = flst.begin(); it != flst.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n  (No reverse iteration available)\n";
}

// Compare list vs vector
void listVsVector() {
    printSection("8. LIST vs VECTOR COMPARISON");

    cout << "\nChoose LIST when:\n";
    cout << "  - Frequent insertions/deletions in middle\n";
    cout << "  - Iterator stability required (iterators don't invalidate)\n";
    cout << "  - No need for random access\n";
    cout << "  - Splicing operations needed\n";

    cout << "\nChoose VECTOR when:\n";
    cout << "  - Random access needed (O(1))\n";
    cout << "  - Mostly append operations\n";
    cout << "  - Better cache locality (contiguous memory)\n";
    cout << "  - Smaller memory footprint per element\n";

    cout << "\nPerformance characteristics:\n";
    cout << "  List insertion/deletion: O(1) with iterator\n";
    cout << "  List access: O(n) (must traverse)\n";
    cout << "  List memory: Extra overhead for pointers\n";

    cout << "\nChoose FORWARD_LIST when:\n";
    cout << "  - Memory is extremely constrained\n";
    cout << "  - Only forward iteration needed\n";
    cout << "  - Smallest possible linked list overhead\n";
}

// Advanced list techniques
void advancedTechniques() {
    printSection("9. ADVANCED TECHNIQUES");

    // Custom sorting
    cout << "\nCustom sorting with lambda:\n";
    list<string> words = {"apple", "pie", "a", "to", "hello"};
    printList(words, "Original");
    words.sort([](const string& a, const string& b) {
        return a.length() < b.length();
    });
    printList(words, "Sorted by length");

    // Partitioning
    cout << "\nPartitioning with splice:\n";
    list<int> nums = {1, 6, 2, 8, 3, 9, 4, 7, 5};
    list<int> evens;
    printList(nums, "Original");

    for (auto it = nums.begin(); it != nums.end(); ) {
        if (*it % 2 == 0) {
            auto next = std::next(it);
            evens.splice(evens.end(), nums, it);
            it = next;
        } else {
            ++it;
        }
    }
    printList(nums, "Odds");
    printList(evens, "Evens");

    // Stable partitioning alternative
    cout << "\nUsing remove_if for filtering:\n";
    list<int> all = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    printList(all, "Original");
    all.remove_if([](int x) { return x > 5; });
    printList(all, "After remove_if (>5)");
}

int main() {
    cout << "LIST OPERATIONS COMPREHENSIVE GUIDE\n";
    cout << "===================================\n";

    listInitialization();
    listModifiers();
    listSpecificOperations();
    spliceOperations();
    mergeOperations();
    forwardListOperations();
    iteratorOperations();
    listVsVector();
    advancedTechniques();

    printSection("SUMMARY");
    cout << "\nList (doubly linked) features:\n";
    cout << "- Bidirectional iteration\n";
    cout << "- O(1) insertion/deletion with iterator\n";
    cout << "- Special operations: splice, merge, sort, unique\n";
    cout << "- Iterator stability (never invalidated)\n";

    cout << "\nForward_list (singly linked) features:\n";
    cout << "- Forward-only iteration\n";
    cout << "- Minimal memory overhead\n";
    cout << "- insert_after/erase_after instead of insert/erase\n";
    cout << "- No size() method (performance consideration)\n";

    return 0;
}
