/*
 * Program 148: Iterators
 *
 * Demonstrates:
 * - Iterator categories (input, output, forward, bidirectional, random access)
 * - Iterator operations and traits
 * - Iterator adapters (reverse, insert, move, stream)
 * - const_iterator and iterator
 * - Custom iterators
 * - Iterator helper functions (advance, distance, next, prev)
 * - Iterator invalidation
 * - Best practices
 */

#include <iostream>
#include <vector>
#include <list>
#include <set>
#include <iterator>
#include <algorithm>
#include <sstream>
#include <string>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Iterator categories demonstration
void iteratorCategories() {
    printSection("1. ITERATOR CATEGORIES");

    cout << "\nInput Iterator (read, single-pass):\n";
    cout << "  - Can read (*it)\n";
    cout << "  - Can increment (++it)\n";
    cout << "  - Single pass only\n";
    cout << "  - Example: istream_iterator\n";

    cout << "\nOutput Iterator (write, single-pass):\n";
    cout << "  - Can write (*it = value)\n";
    cout << "  - Can increment (++it)\n";
    cout << "  - Single pass only\n";
    cout << "  - Example: ostream_iterator, back_inserter\n";

    cout << "\nForward Iterator (multi-pass):\n";
    cout << "  - Read and write\n";
    cout << "  - Multi-pass (can iterate multiple times)\n";
    cout << "  - Example: forward_list::iterator\n";

    cout << "\nBidirectional Iterator:\n";
    cout << "  - Forward + can decrement (--it)\n";
    cout << "  - Example: list::iterator, set::iterator\n";

    cout << "\nRandom Access Iterator:\n";
    cout << "  - Bidirectional + random access\n";
    cout << "  - Can jump: it + n, it - n, it[n]\n";
    cout << "  - Can compare: it1 < it2\n";
    cout << "  - Example: vector::iterator, deque::iterator, array pointers\n";
}

// Basic iterator operations
void basicIteratorOperations() {
    printSection("2. BASIC ITERATOR OPERATIONS");

    vector<int> v = {1, 2, 3, 4, 5};

    cout << "\nForward iteration:\n";
    cout << "  ";
    for (auto it = v.begin(); it != v.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nReverse iteration:\n";
    cout << "  ";
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nConst iteration:\n";
    cout << "  ";
    for (auto it = v.cbegin(); it != v.cend(); ++it) {
        cout << *it << " ";
        // *it = 10; // Error: cannot modify through const_iterator
    }
    cout << "\n";

    cout << "\nIterator arithmetic (random access):\n";
    auto it = v.begin();
    cout << "  *begin(): " << *it << "\n";
    cout << "  *(begin() + 2): " << *(it + 2) << "\n";
    cout << "  *(end() - 1): " << *(v.end() - 1) << "\n";

    cout << "\nIterator comparison:\n";
    auto it1 = v.begin();
    auto it2 = v.begin() + 2;
    cout << "  it1 < it2: " << (it1 < it2) << "\n";
    cout << "  it1 == v.begin(): " << (it1 == v.begin()) << "\n";

    cout << "\nSubscript operator:\n";
    cout << "  it[2]: " << it[2] << "\n";
}

// Iterator helper functions
void iteratorHelpers() {
    printSection("3. ITERATOR HELPER FUNCTIONS");

    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    cout << "\nadvance (move iterator):\n";
    auto it = v.begin();
    cout << "  Initial: " << *it << "\n";
    advance(it, 3);
    cout << "  After advance(3): " << *it << "\n";

    list<int> lst = {1, 2, 3, 4, 5};
    auto lit = lst.begin();
    advance(lit, 2);
    cout << "  List advance(2): " << *lit << "\n";

    cout << "\ndistance (count between iterators):\n";
    auto first = v.begin();
    auto last = v.end();
    cout << "  distance(begin, end): " << distance(first, last) << "\n";

    first = v.begin();
    last = v.begin() + 5;
    cout << "  distance(begin, begin+5): " << distance(first, last) << "\n";

    cout << "\nnext (get next iterator):\n";
    it = v.begin();
    auto next_it = next(it);
    cout << "  *begin(): " << *it << "\n";
    cout << "  *next(begin()): " << *next_it << "\n";
    cout << "  *next(begin(), 3): " << *next(it, 3) << "\n";

    cout << "\nprev (get previous iterator):\n";
    it = v.end();
    auto prev_it = prev(it);
    cout << "  *prev(end()): " << *prev_it << "\n";
    cout << "  *prev(end(), 3): " << *prev(it, 3) << "\n";
}

// Reverse iterators
void reverseIterators() {
    printSection("4. REVERSE ITERATORS");

    vector<int> v = {1, 2, 3, 4, 5};

    cout << "\nReverse iteration:\n";
    cout << "  Forward: ";
    for (auto it = v.begin(); it != v.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n  Reverse: ";
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "\nReverse iterator from regular iterator:\n";
    auto it = v.begin() + 3;  // Points to 4
    cout << "  Iterator value: " << *it << "\n";

    auto rit = make_reverse_iterator(it);
    cout << "  Reverse iterator value: " << *rit << "\n";

    cout << "\nbase() to get underlying iterator:\n";
    auto rit2 = v.rbegin();
    cout << "  *rbegin(): " << *rit2 << "\n";
    auto base = rit2.base();
    cout << "  *rbegin().base(): " << (base == v.end() ? "end()" : to_string(*base)) << "\n";
}

// Insert iterators
void insertIterators() {
    printSection("5. INSERT ITERATORS");

    // back_inserter
    cout << "\nback_inserter:\n";
    vector<int> v = {1, 2, 3};
    vector<int> src = {4, 5, 6};
    cout << "  Before: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    copy(src.begin(), src.end(), back_inserter(v));
    cout << "  After copy with back_inserter: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    // front_inserter
    cout << "\nfront_inserter (list/deque):\n";
    list<int> lst = {1, 2, 3};
    list<int> src2 = {4, 5, 6};
    cout << "  Before: ";
    for (int x : lst) cout << x << " ";
    cout << "\n";

    copy(src2.begin(), src2.end(), front_inserter(lst));
    cout << "  After copy with front_inserter: ";
    for (int x : lst) cout << x << " ";
    cout << "\n";

    // inserter
    cout << "\ninserter (insert at position):\n";
    vector<int> v2 = {1, 2, 5, 6};
    vector<int> mid = {3, 4};
    cout << "  Before: ";
    for (int x : v2) cout << x << " ";
    cout << "\n";

    auto pos = v2.begin() + 2;
    copy(mid.begin(), mid.end(), inserter(v2, pos));
    cout << "  After inserter at pos 2: ";
    for (int x : v2) cout << x << " ";
    cout << "\n";
}

// Stream iterators
void streamIterators() {
    printSection("6. STREAM ITERATORS");

    // ostream_iterator
    cout << "\nostream_iterator (output):\n";
    vector<int> v = {1, 2, 3, 4, 5};
    cout << "  Vector: ";
    copy(v.begin(), v.end(), ostream_iterator<int>(cout, " "));
    cout << "\n";

    // istream_iterator
    cout << "\nistream_iterator (input):\n";
    cout << "  Enter numbers (Ctrl+D or non-number to stop):\n";
    cout << "  (Skipping interactive input for demo)\n";

    // Simulated with string stream
    stringstream ss("10 20 30 40 50");
    vector<int> nums;
    copy(istream_iterator<int>(ss), istream_iterator<int>(),
         back_inserter(nums));
    cout << "  Read from stream: ";
    for (int x : nums) cout << x << " ";
    cout << "\n";

    // Sum using istream_iterator
    cout << "\nSum with istream_iterator:\n";
    stringstream ss2("1 2 3 4 5");
    int sum = accumulate(istream_iterator<int>(ss2), istream_iterator<int>(), 0);
    cout << "  Sum: " << sum << "\n";
}

// Move iterators
void moveIterators() {
    printSection("7. MOVE ITERATORS");

    cout << "\nMove semantics with iterators:\n";
    vector<string> src = {"hello", "world", "foo", "bar"};
    vector<string> dst;

    cout << "  Source before move: ";
    for (const auto& s : src) cout << s << " ";
    cout << "\n";

    // Move elements instead of copying
    copy(make_move_iterator(src.begin()),
         make_move_iterator(src.end()),
         back_inserter(dst));

    cout << "  Source after move: ";
    for (const auto& s : src) cout << "\"" << s << "\" ";
    cout << "\n";

    cout << "  Destination: ";
    for (const auto& s : dst) cout << s << " ";
    cout << "\n";
}

// Custom iterator example
void customIterator() {
    printSection("8. CUSTOM ITERATOR");

    cout << "\nSimple custom range class:\n";

    // Range class with custom iterator
    class Range {
        int from, to;
    public:
        Range(int from, int to) : from(from), to(to) {}

        class Iterator {
            int current;
        public:
            using iterator_category = forward_iterator_tag;
            using value_type = int;
            using difference_type = ptrdiff_t;
            using pointer = int*;
            using reference = int&;

            Iterator(int val) : current(val) {}

            int operator*() const { return current; }
            Iterator& operator++() { ++current; return *this; }
            Iterator operator++(int) { Iterator tmp = *this; ++current; return tmp; }
            bool operator==(const Iterator& other) const { return current == other.current; }
            bool operator!=(const Iterator& other) const { return current != other.current; }
        };

        Iterator begin() const { return Iterator(from); }
        Iterator end() const { return Iterator(to); }
    };

    Range r(1, 10);
    cout << "  Range(1, 10): ";
    for (int x : r) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "  Using with algorithms:\n";
    auto it = find(r.begin(), r.end(), 5);
    cout << "  find(5): " << (it != r.end() ? to_string(*it) : "not found") << "\n";

    int sum = accumulate(r.begin(), r.end(), 0);
    cout << "  sum: " << sum << "\n";
}

// Iterator invalidation
void iteratorInvalidation() {
    printSection("9. ITERATOR INVALIDATION");

    cout << "\nVector iterator invalidation:\n";
    vector<int> v = {1, 2, 3, 4, 5};
    auto it = v.begin() + 2;
    cout << "  Initial *it: " << *it << "\n";

    cout << "  After push_back (may invalidate all):\n";
    v.push_back(6);
    cout << "  (Iterator may be invalid if reallocation occurred)\n";

    cout << "\nList iterator stability:\n";
    list<int> lst = {1, 2, 3, 4, 5};
    auto lit = lst.begin();
    advance(lit, 2);
    cout << "  Initial *it: " << *lit << "\n";

    lst.push_back(6);
    lst.push_front(0);
    cout << "  After push_back/front, *it: " << *lit << " (still valid)\n";

    cout << "\nSafe erasure pattern:\n";
    v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    cout << "  Remove all evens:\n";
    cout << "  Before: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    for (auto it = v.begin(); it != v.end(); ) {
        if (*it % 2 == 0) {
            it = v.erase(it);  // erase returns next valid iterator
        } else {
            ++it;
        }
    }

    cout << "  After: ";
    for (int x : v) cout << x << " ";
    cout << "\n";
}

// Best practices
void bestPractices() {
    printSection("10. BEST PRACTICES");

    cout << "\n1. Prefer range-based for loops when possible:\n";
    cout << "   for (const auto& elem : container) { }\n";

    cout << "\n2. Use const_iterator when not modifying:\n";
    cout << "   for (auto it = v.cbegin(); it != v.cend(); ++it)\n";

    cout << "\n3. Use algorithms instead of manual iteration:\n";
    cout << "   auto it = find(v.begin(), v.end(), value);\n";

    cout << "\n4. Be aware of iterator invalidation:\n";
    cout << "   - Vector: insertion/deletion may invalidate all\n";
    cout << "   - List: only erased elements invalidated\n";
    cout << "   - Set/Map: only erased elements invalidated\n";

    cout << "\n5. Use helper functions:\n";
    cout << "   - next(it, n) instead of it + n for non-random access\n";
    cout << "   - distance(first, last) to count elements\n";

    cout << "\n6. Check for end() before dereferencing:\n";
    cout << "   auto it = find(...);\n";
    cout << "   if (it != v.end()) { use *it; }\n";

    cout << "\n7. Use appropriate iterator category:\n";
    cout << "   - Input/Output for streams\n";
    cout << "   - Random access for vectors/arrays\n";
    cout << "   - Bidirectional for lists/sets\n";
}

int main() {
    cout << "ITERATORS COMPREHENSIVE GUIDE\n";
    cout << "=============================\n";

    iteratorCategories();
    basicIteratorOperations();
    iteratorHelpers();
    reverseIterators();
    insertIterators();
    streamIterators();
    moveIterators();
    customIterator();
    iteratorInvalidation();
    bestPractices();

    printSection("SUMMARY");
    cout << "\nIterators provide unified interface for container traversal:\n";
    cout << "- 5 categories: input, output, forward, bidirectional, random\n";
    cout << "- Adapters: reverse, insert, stream, move iterators\n";
    cout << "- Helpers: advance, distance, next, prev\n";
    cout << "- Enable generic algorithms\n";
    cout << "- Be aware of invalidation rules\n";
    cout << "\nIterators are the glue between containers and algorithms!\n";

    return 0;
}
