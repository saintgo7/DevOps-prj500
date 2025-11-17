/*
 * Program 145: Sets and Maps
 *
 * Demonstrates:
 * - std::set and std::multiset
 * - std::map and std::multimap
 * - Ordered associative containers
 * - Red-black tree implementation
 * - Custom comparators
 * - Find, insert, erase operations
 * - Lower/upper bound operations
 * - Use cases and performance
 */

#include <iostream>
#include <set>
#include <map>
#include <string>
#include <algorithm>
#include <iomanip>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

template<typename T>
void printSet(const set<T>& s, const string& label = "Set") {
    cout << label << ": ";
    for (const auto& elem : s) {
        cout << elem << " ";
    }
    cout << "\n";
}

// Demonstrate set operations
void setOperations() {
    printSection("1. SET OPERATIONS");

    // Initialization
    cout << "\nSet initialization:\n";
    set<int> s1;
    set<int> s2 = {5, 2, 8, 1, 9, 3};
    set<int> s3(s2);
    printSet(s2, "Initializer list");

    // Insert
    cout << "\nInsert operations:\n";
    auto [it1, success1] = s1.insert(10);
    cout << "  Insert 10: " << (success1 ? "Success" : "Failed") << "\n";
    auto [it2, success2] = s1.insert(10);
    cout << "  Insert 10 again: " << (success2 ? "Success" : "Failed (duplicate)") << "\n";

    s1.insert({1, 2, 3, 4, 5});
    printSet(s1, "After insert range");

    s1.emplace(6);
    printSet(s1, "After emplace(6)");

    // Find
    cout << "\nFind operations:\n";
    auto found = s1.find(3);
    if (found != s1.end()) {
        cout << "  Found: " << *found << "\n";
    }

    found = s1.find(100);
    cout << "  Find(100): " << (found == s1.end() ? "Not found" : "Found") << "\n";

    // Count
    cout << "\nCount operations:\n";
    cout << "  count(3): " << s1.count(3) << "\n";
    cout << "  count(100): " << s1.count(100) << "\n";

    // Erase
    cout << "\nErase operations:\n";
    printSet(s1, "Before erase");
    s1.erase(3);
    printSet(s1, "After erase(3)");

    auto it = s1.find(5);
    if (it != s1.end()) {
        s1.erase(it);
        printSet(s1, "After erase(iterator)");
    }

    // Clear
    cout << "\nClear:\n";
    cout << "  Size before clear: " << s1.size() << "\n";
    s1.clear();
    cout << "  Size after clear: " << s1.size() << "\n";
}

// Demonstrate multiset
void multisetOperations() {
    printSection("2. MULTISET OPERATIONS");

    multiset<int> ms = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4};

    cout << "\nMultiset (allows duplicates):\n";
    cout << "Elements: ";
    for (int x : ms) cout << x << " ";
    cout << "\n";

    cout << "\nCount of each element:\n";
    for (int i = 1; i <= 5; i++) {
        cout << "  count(" << i << "): " << ms.count(i) << "\n";
    }

    cout << "\nInsert duplicate:\n";
    ms.insert(3);
    cout << "After insert(3), count(3): " << ms.count(3) << "\n";

    cout << "\nEqual range:\n";
    auto range = ms.equal_range(3);
    cout << "  Elements equal to 3: ";
    for (auto it = range.first; it != range.second; ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nErase all occurrences:\n";
    size_t erased = ms.erase(3);
    cout << "  Erased " << erased << " elements with value 3\n";
    cout << "  count(3): " << ms.count(3) << "\n";
}

// Demonstrate set bounds
void setBounds() {
    printSection("3. LOWER_BOUND AND UPPER_BOUND");

    set<int> s = {10, 20, 30, 40, 50};
    printSet(s);

    cout << "\nLower bound (first >= value):\n";
    auto lb = s.lower_bound(25);
    cout << "  lower_bound(25): " << (lb != s.end() ? to_string(*lb) : "end") << "\n";
    lb = s.lower_bound(30);
    cout << "  lower_bound(30): " << (lb != s.end() ? to_string(*lb) : "end") << "\n";

    cout << "\nUpper bound (first > value):\n";
    auto ub = s.upper_bound(25);
    cout << "  upper_bound(25): " << (ub != s.end() ? to_string(*ub) : "end") << "\n";
    ub = s.upper_bound(30);
    cout << "  upper_bound(30): " << (ub != s.end() ? to_string(*ub) : "end") << "\n";

    cout << "\nEqual range:\n";
    auto [first, last] = s.equal_range(30);
    cout << "  equal_range(30): [";
    cout << (first != s.end() ? to_string(*first) : "end") << ", ";
    cout << (last != s.end() ? to_string(*last) : "end") << ")\n";
}

// Demonstrate map operations
void mapOperations() {
    printSection("4. MAP OPERATIONS");

    // Initialization
    cout << "\nMap initialization:\n";
    map<string, int> ages;
    map<string, int> scores = {{"Alice", 95}, {"Bob", 87}, {"Charlie", 92}};

    cout << "Scores:\n";
    for (const auto& [name, score] : scores) {
        cout << "  " << name << ": " << score << "\n";
    }

    // Insert
    cout << "\nInsert operations:\n";
    auto [it1, success1] = scores.insert({"David", 88});
    cout << "  Insert David: " << (success1 ? "Success" : "Failed") << "\n";

    auto [it2, success2] = scores.insert({"Alice", 100});
    cout << "  Insert Alice again: " << (success2 ? "Success" : "Failed (exists)") << "\n";

    scores.insert(make_pair("Eve", 91));
    scores.emplace("Frank", 85);

    cout << "\nAll scores:\n";
    for (const auto& [name, score] : scores) {
        cout << "  " << name << ": " << score << "\n";
    }

    // Access with []
    cout << "\nAccess with operator[]:\n";
    cout << "  scores[\"Alice\"] = " << scores["Alice"] << "\n";
    cout << "  scores[\"NewPerson\"] = " << scores["NewPerson"]
         << " (default constructed)\n";

    // Access with at()
    cout << "\nAccess with at():\n";
    cout << "  scores.at(\"Bob\") = " << scores.at("Bob") << "\n";
    try {
        cout << "  scores.at(\"Nobody\")...\n";
        int x = scores.at("Nobody");
        cout << "  Value: " << x << "\n";
    } catch (const out_of_range& e) {
        cout << "  Exception: " << e.what() << "\n";
    }

    // Find
    cout << "\nFind operations:\n";
    auto found = scores.find("Charlie");
    if (found != scores.end()) {
        cout << "  Found Charlie: " << found->second << "\n";
    }

    // Erase
    cout << "\nErase operations:\n";
    scores.erase("NewPerson");
    scores.erase(scores.find("Frank"));

    cout << "After erasing:\n";
    for (const auto& [name, score] : scores) {
        cout << "  " << name << ": " << score << "\n";
    }

    // Modify values
    cout << "\nModify values:\n";
    scores["Alice"] = 100;
    scores.at("Bob") = 90;
    cout << "  Alice: " << scores["Alice"] << "\n";
    cout << "  Bob: " << scores["Bob"] << "\n";
}

// Demonstrate multimap
void multimapOperations() {
    printSection("5. MULTIMAP OPERATIONS");

    multimap<string, int> phone_book;

    // Insert multiple values for same key
    phone_book.insert({"Alice", 1234});
    phone_book.insert({"Alice", 5678});
    phone_book.insert({"Bob", 9999});
    phone_book.insert({"Alice", 4321});
    phone_book.insert({"Charlie", 1111});

    cout << "\nPhone book (multiple numbers per person):\n";
    for (const auto& [name, number] : phone_book) {
        cout << "  " << name << ": " << number << "\n";
    }

    cout << "\nFind all numbers for Alice:\n";
    auto range = phone_book.equal_range("Alice");
    for (auto it = range.first; it != range.second; ++it) {
        cout << "  " << it->second << "\n";
    }

    cout << "\nCount entries:\n";
    cout << "  Alice has " << phone_book.count("Alice") << " numbers\n";
    cout << "  Bob has " << phone_book.count("Bob") << " numbers\n";

    // Erase all entries for a key
    cout << "\nErase all of Alice's numbers:\n";
    size_t erased = phone_book.erase("Alice");
    cout << "  Erased " << erased << " entries\n";

    cout << "After erase:\n";
    for (const auto& [name, number] : phone_book) {
        cout << "  " << name << ": " << number << "\n";
    }
}

// Custom comparators
void customComparators() {
    printSection("6. CUSTOM COMPARATORS");

    // Descending order set
    cout << "\nSet with descending order:\n";
    set<int, greater<int>> desc_set = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Elements: ";
    for (int x : desc_set) cout << x << " ";
    cout << "\n";

    // Custom comparator for strings (by length)
    struct CompareByLength {
        bool operator()(const string& a, const string& b) const {
            if (a.length() != b.length()) {
                return a.length() < b.length();
            }
            return a < b;  // Tie-breaker
        }
    };

    cout << "\nSet sorted by string length:\n";
    set<string, CompareByLength> words = {"apple", "pie", "a", "to", "hello", "world"};
    for (const auto& word : words) {
        cout << "  " << word << " (len=" << word.length() << ")\n";
    }

    // Lambda comparator
    cout << "\nMap with custom comparator (case-insensitive):\n";
    auto caseInsensitive = [](const string& a, const string& b) {
        string a_lower = a, b_lower = b;
        transform(a.begin(), a.end(), a_lower.begin(), ::tolower);
        transform(b.begin(), b.end(), b_lower.begin(), ::tolower);
        return a_lower < b_lower;
    };

    map<string, int, decltype(caseInsensitive)> ci_map(caseInsensitive);
    ci_map["Apple"] = 1;
    ci_map["banana"] = 2;
    ci_map["CHERRY"] = 3;

    for (const auto& [key, val] : ci_map) {
        cout << "  " << key << ": " << val << "\n";
    }
}

// Set operations (union, intersection, etc.)
void setAlgorithms() {
    printSection("7. SET ALGORITHMS");

    set<int> s1 = {1, 2, 3, 4, 5};
    set<int> s2 = {4, 5, 6, 7, 8};

    printSet(s1, "Set 1");
    printSet(s2, "Set 2");

    // Union
    cout << "\nUnion:\n";
    set<int> result;
    set_union(s1.begin(), s1.end(), s2.begin(), s2.end(),
              inserter(result, result.begin()));
    printSet(result, "s1 ∪ s2");

    // Intersection
    cout << "\nIntersection:\n";
    result.clear();
    set_intersection(s1.begin(), s1.end(), s2.begin(), s2.end(),
                     inserter(result, result.begin()));
    printSet(result, "s1 ∩ s2");

    // Difference
    cout << "\nDifference:\n";
    result.clear();
    set_difference(s1.begin(), s1.end(), s2.begin(), s2.end(),
                   inserter(result, result.begin()));
    printSet(result, "s1 - s2");

    // Symmetric difference
    cout << "\nSymmetric difference:\n";
    result.clear();
    set_symmetric_difference(s1.begin(), s1.end(), s2.begin(), s2.end(),
                            inserter(result, result.begin()));
    printSet(result, "s1 △ s2");

    // Includes
    cout << "\nIncludes:\n";
    set<int> subset = {2, 3, 4};
    bool is_subset = includes(s1.begin(), s1.end(), subset.begin(), subset.end());
    cout << "  {2,3,4} ⊆ s1: " << (is_subset ? "Yes" : "No") << "\n";
}

// Use cases
void useCases() {
    printSection("8. USE CASES");

    cout << "\nUse SET when:\n";
    cout << "  - Need unique elements\n";
    cout << "  - Need elements sorted\n";
    cout << "  - Fast lookup/insertion/deletion O(log n)\n";
    cout << "  - Set operations (union, intersection)\n";

    cout << "\nUse MULTISET when:\n";
    cout << "  - Need sorted elements with duplicates\n";
    cout << "  - Count occurrences efficiently\n";
    cout << "  - Priority queue with duplicates\n";

    cout << "\nUse MAP when:\n";
    cout << "  - Key-value associations\n";
    cout << "  - Unique keys required\n";
    cout << "  - Need keys sorted\n";
    cout << "  - Dictionary, phone book, index\n";

    cout << "\nUse MULTIMAP when:\n";
    cout << "  - One key maps to multiple values\n";
    cout << "  - Need sorted keys\n";
    cout << "  - One-to-many relationships\n";

    cout << "\nPerformance:\n";
    cout << "  - All operations: O(log n)\n";
    cout << "  - Implemented as red-black trees\n";
    cout << "  - Iterators remain valid (except erased)\n";
    cout << "  - Always sorted (in-order traversal)\n";
}

int main() {
    cout << "SETS AND MAPS COMPREHENSIVE GUIDE\n";
    cout << "==================================\n";

    setOperations();
    multisetOperations();
    setBounds();
    mapOperations();
    multimapOperations();
    customComparators();
    setAlgorithms();
    useCases();

    printSection("SUMMARY");
    cout << "\nOrdered associative containers:\n";
    cout << "- set: Unique sorted elements\n";
    cout << "- multiset: Sorted elements with duplicates\n";
    cout << "- map: Unique key-value pairs, sorted by key\n";
    cout << "- multimap: Key-value pairs, duplicate keys allowed\n";
    cout << "\nAll provide O(log n) operations via red-black trees\n";
    cout << "Always keep elements sorted for fast range queries\n";

    return 0;
}
