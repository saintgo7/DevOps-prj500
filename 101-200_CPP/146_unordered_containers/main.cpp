/*
 * Program 146: Unordered Containers
 *
 * Demonstrates:
 * - std::unordered_set and std::unordered_multiset
 * - std::unordered_map and std::unordered_multimap
 * - Hash tables implementation
 * - Hash functions and custom hashers
 * - Bucket interface
 * - Load factor and rehashing
 * - Performance characteristics
 * - When to use vs ordered containers
 */

#include <iostream>
#include <unordered_set>
#include <unordered_map>
#include <string>
#include <functional>
#include <iomanip>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Demonstrate unordered_set
void unorderedSetOperations() {
    printSection("1. UNORDERED_SET OPERATIONS");

    // Initialization
    cout << "\nUnordered set initialization:\n";
    unordered_set<int> us = {5, 2, 8, 1, 9, 3, 7, 4, 6};

    cout << "Elements (no guaranteed order): ";
    for (int x : us) cout << x << " ";
    cout << "\n";

    // Insert
    cout << "\nInsert operations:\n";
    auto [it1, success1] = us.insert(10);
    cout << "  Insert 10: " << (success1 ? "Success" : "Failed") << "\n";
    auto [it2, success2] = us.insert(10);
    cout << "  Insert 10 again: " << (success2 ? "Success" : "Failed (duplicate)") << "\n";

    // Find - O(1) average
    cout << "\nFind operations (O(1) average):\n";
    auto found = us.find(5);
    cout << "  find(5): " << (found != us.end() ? "Found" : "Not found") << "\n";
    found = us.find(100);
    cout << "  find(100): " << (found != us.end() ? "Found" : "Not found") << "\n";

    // Count
    cout << "\nCount: " << us.count(5) << "\n";

    // Erase
    cout << "\nErase operations:\n";
    us.erase(5);
    cout << "  After erase(5), count(5): " << us.count(5) << "\n";

    // Size
    cout << "\nSize: " << us.size() << "\n";
}

// Demonstrate unordered_multiset
void unorderedMultisetOperations() {
    printSection("2. UNORDERED_MULTISET");

    unordered_multiset<int> ums = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4};

    cout << "\nElements: ";
    for (int x : ums) cout << x << " ";
    cout << "\n";

    cout << "\nCount of elements:\n";
    for (int i = 1; i <= 5; i++) {
        cout << "  count(" << i << "): " << ums.count(i) << "\n";
    }

    cout << "\nEqual range:\n";
    auto range = ums.equal_range(3);
    cout << "  Elements equal to 3: ";
    for (auto it = range.first; it != range.second; ++it) {
        cout << *it << " ";
    }
    cout << "\n";
}

// Demonstrate unordered_map
void unorderedMapOperations() {
    printSection("3. UNORDERED_MAP OPERATIONS");

    // Word frequency counter
    cout << "\nWord frequency counter:\n";
    string text = "the quick brown fox jumps over the lazy dog the fox";
    unordered_map<string, int> freq;

    // Count words
    string word;
    size_t pos = 0;
    while (pos < text.length()) {
        size_t next = text.find(' ', pos);
        if (next == string::npos) next = text.length();
        word = text.substr(pos, next - pos);
        freq[word]++;
        pos = next + 1;
    }

    cout << "Frequencies:\n";
    for (const auto& [w, count] : freq) {
        cout << "  " << setw(10) << w << ": " << count << "\n";
    }

    // Insert
    cout << "\nInsert operations:\n";
    auto [it, success] = freq.insert({"cat", 1});
    cout << "  Insert 'cat': " << (success ? "Success" : "Failed") << "\n";

    freq.insert_or_assign("dog", 5);
    cout << "  insert_or_assign 'dog' = 5\n";

    // Access
    cout << "\nAccess methods:\n";
    cout << "  freq[\"fox\"] = " << freq["fox"] << "\n";
    cout << "  freq.at(\"the\") = " << freq.at("the") << "\n";

    // Find
    auto found = freq.find("quick");
    if (found != freq.end()) {
        cout << "  Found 'quick': " << found->second << "\n";
    }

    // Erase
    freq.erase("lazy");
    cout << "\nAfter erase('lazy'), count: " << freq.count("lazy") << "\n";
}

// Demonstrate unordered_multimap
void unorderedMultimapOperations() {
    printSection("4. UNORDERED_MULTIMAP");

    unordered_multimap<string, string> synonyms;

    // Add synonyms
    synonyms.insert({"happy", "joyful"});
    synonyms.insert({"happy", "cheerful"});
    synonyms.insert({"happy", "glad"});
    synonyms.insert({"sad", "unhappy"});
    synonyms.insert({"sad", "sorrowful"});

    cout << "\nSynonyms:\n";
    for (const auto& [word, syn] : synonyms) {
        cout << "  " << word << " -> " << syn << "\n";
    }

    cout << "\nAll synonyms for 'happy':\n";
    auto range = synonyms.equal_range("happy");
    for (auto it = range.first; it != range.second; ++it) {
        cout << "  " << it->second << "\n";
    }

    cout << "\nCount for 'happy': " << synonyms.count("happy") << "\n";
}

// Bucket interface
void bucketInterface() {
    printSection("5. BUCKET INTERFACE");

    unordered_set<int> us = {1, 2, 3, 4, 5, 10, 20, 30};

    cout << "\nBucket information:\n";
    cout << "  Bucket count: " << us.bucket_count() << "\n";
    cout << "  Max bucket count: " << us.max_bucket_count() << "\n";
    cout << "  Load factor: " << us.load_factor() << "\n";
    cout << "  Max load factor: " << us.max_load_factor() << "\n";

    cout << "\nBucket distribution:\n";
    for (size_t i = 0; i < us.bucket_count(); ++i) {
        cout << "  Bucket " << i << " size: " << us.bucket_size(i);
        if (us.bucket_size(i) > 0) {
            cout << " [";
            for (auto it = us.begin(i); it != us.end(i); ++it) {
                cout << *it << " ";
            }
            cout << "]";
        }
        cout << "\n";
    }

    cout << "\nWhich bucket for each element:\n";
    for (int x : us) {
        cout << "  " << x << " -> bucket " << us.bucket(x) << "\n";
    }
}

// Load factor and rehashing
void loadFactorRehashing() {
    printSection("6. LOAD FACTOR AND REHASHING");

    unordered_set<int> us;

    cout << "\nInserting elements and observing rehashing:\n";
    for (int i = 1; i <= 20; i++) {
        size_t old_buckets = us.bucket_count();
        us.insert(i);
        size_t new_buckets = us.bucket_count();

        if (old_buckets != new_buckets) {
            cout << "  After insert(" << i << "): "
                 << "buckets: " << old_buckets << " -> " << new_buckets
                 << ", load: " << us.load_factor() << "\n";
        }
    }

    cout << "\nFinal state:\n";
    cout << "  Size: " << us.size() << "\n";
    cout << "  Buckets: " << us.bucket_count() << "\n";
    cout << "  Load factor: " << us.load_factor() << "\n";

    // Manual rehash
    cout << "\nManual rehash to 50 buckets:\n";
    us.rehash(50);
    cout << "  Buckets: " << us.bucket_count() << "\n";
    cout << "  Load factor: " << us.load_factor() << "\n";

    // Reserve
    cout << "\nReserve for 100 elements:\n";
    us.reserve(100);
    cout << "  Buckets: " << us.bucket_count() << "\n";
    cout << "  Load factor: " << us.load_factor() << "\n";

    // Set max load factor
    cout << "\nSet max load factor to 0.5:\n";
    us.max_load_factor(0.5);
    cout << "  Max load factor: " << us.max_load_factor() << "\n";
}

// Custom hash function
void customHashFunction() {
    printSection("7. CUSTOM HASH FUNCTIONS");

    // Struct for custom type
    struct Point {
        int x, y;
        Point(int x, int y) : x(x), y(y) {}
        bool operator==(const Point& other) const {
            return x == other.x && y == other.y;
        }
    };

    // Custom hash function
    struct PointHash {
        size_t operator()(const Point& p) const {
            // Combine hashes using XOR and bit shifting
            return hash<int>()(p.x) ^ (hash<int>()(p.y) << 1);
        }
    };

    cout << "\nUnordered set with custom type:\n";
    unordered_set<Point, PointHash> points;

    points.insert(Point(1, 2));
    points.insert(Point(3, 4));
    points.insert(Point(1, 2));  // Duplicate

    cout << "  Size: " << points.size() << " (duplicate eliminated)\n";

    // Custom hash for pair
    struct PairHash {
        template <typename T1, typename T2>
        size_t operator()(const pair<T1, T2>& p) const {
            auto h1 = hash<T1>()(p.first);
            auto h2 = hash<T2>()(p.second);
            return h1 ^ (h2 << 1);
        }
    };

    cout << "\nUnordered map with pair as key:\n";
    unordered_map<pair<int, int>, string, PairHash> coord_map;

    coord_map[{0, 0}] = "Origin";
    coord_map[{1, 0}] = "East";
    coord_map[{0, 1}] = "North";

    for (const auto& [coord, name] : coord_map) {
        cout << "  (" << coord.first << "," << coord.second
             << ") -> " << name << "\n";
    }

    // Lambda hash function
    cout << "\nUsing lambda for hash:\n";
    auto string_hash = [](const string& s) {
        return hash<string>()(s);
    };

    auto string_equal = [](const string& a, const string& b) {
        return a == b;
    };

    unordered_set<string, decltype(string_hash), decltype(string_equal)>
        custom_set(10, string_hash, string_equal);

    custom_set.insert("hello");
    custom_set.insert("world");

    cout << "  Size: " << custom_set.size() << "\n";
}

// Performance comparison
void performanceComparison() {
    printSection("8. ORDERED vs UNORDERED CONTAINERS");

    cout << "\n" << left << setw(25) << "Operation"
         << setw(20) << "Ordered (RB-Tree)"
         << setw(20) << "Unordered (Hash)" << "\n";
    cout << string(65, '-') << "\n";

    cout << setw(25) << "Insert"
         << setw(20) << "O(log n)"
         << setw(20) << "O(1) average" << "\n";

    cout << setw(25) << "Delete"
         << setw(20) << "O(log n)"
         << setw(20) << "O(1) average" << "\n";

    cout << setw(25) << "Find"
         << setw(20) << "O(log n)"
         << setw(20) << "O(1) average" << "\n";

    cout << setw(25) << "Iteration Order"
         << setw(20) << "Sorted"
         << setw(20) << "Unordered" << "\n";

    cout << setw(25) << "Range Queries"
         << setw(20) << "Efficient"
         << setw(20) << "Not supported" << "\n";

    cout << setw(25) << "Memory Overhead"
         << setw(20) << "Low (3 ptrs/node)"
         << setw(20) << "Higher (buckets)" << "\n";

    cout << setw(25) << "Worst Case"
         << setw(20) << "O(log n)"
         << setw(20) << "O(n)" << "\n";

    cout << "\nWhen to use UNORDERED:\n";
    cout << "  - Need fastest possible lookup\n";
    cout << "  - Don't need sorted order\n";
    cout << "  - No range queries needed\n";
    cout << "  - Have good hash function\n";

    cout << "\nWhen to use ORDERED:\n";
    cout << "  - Need sorted iteration\n";
    cout << "  - Need range queries (lower_bound, upper_bound)\n";
    cout << "  - Want guaranteed O(log n) worst case\n";
    cout << "  - Hash function is expensive\n";
}

// Practical examples
void practicalExamples() {
    printSection("9. PRACTICAL EXAMPLES");

    // Example 1: Find first non-repeating character
    cout << "\nExample 1: First non-repeating character\n";
    string s = "aabbcdeeff";
    unordered_map<char, int> char_count;

    for (char c : s) {
        char_count[c]++;
    }

    char first_unique = '\0';
    for (char c : s) {
        if (char_count[c] == 1) {
            first_unique = c;
            break;
        }
    }

    cout << "  String: " << s << "\n";
    cout << "  First non-repeating: " << first_unique << "\n";

    // Example 2: Two sum problem
    cout << "\nExample 2: Two sum (find pair that sums to target)\n";
    vector<int> nums = {2, 7, 11, 15};
    int target = 9;
    unordered_map<int, int> seen;

    cout << "  Array: ";
    for (int x : nums) cout << x << " ";
    cout << "\n  Target: " << target << "\n";

    for (size_t i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.count(complement)) {
            cout << "  Found: " << nums[seen[complement]]
                 << " + " << nums[i] << " = " << target << "\n";
            break;
        }
        seen[nums[i]] = i;
    }

    // Example 3: Group anagrams
    cout << "\nExample 3: Group anagrams\n";
    vector<string> words = {"eat", "tea", "tan", "ate", "nat", "bat"};
    unordered_map<string, vector<string>> anagram_groups;

    for (const string& word : words) {
        string sorted_word = word;
        sort(sorted_word.begin(), sorted_word.end());
        anagram_groups[sorted_word].push_back(word);
    }

    cout << "  Anagram groups:\n";
    for (const auto& [key, group] : anagram_groups) {
        cout << "    [";
        for (size_t i = 0; i < group.size(); i++) {
            cout << group[i];
            if (i < group.size() - 1) cout << ", ";
        }
        cout << "]\n";
    }
}

int main() {
    cout << "UNORDERED CONTAINERS COMPREHENSIVE GUIDE\n";
    cout << "========================================\n";

    unorderedSetOperations();
    unorderedMultisetOperations();
    unorderedMapOperations();
    unorderedMultimapOperations();
    bucketInterface();
    loadFactorRehashing();
    customHashFunction();
    performanceComparison();
    practicalExamples();

    printSection("SUMMARY");
    cout << "\nUnordered containers (hash tables):\n";
    cout << "- unordered_set: Unique elements, no order\n";
    cout << "- unordered_multiset: Duplicates allowed\n";
    cout << "- unordered_map: Key-value pairs, unique keys\n";
    cout << "- unordered_multimap: Multiple values per key\n";
    cout << "\nO(1) average operations, perfect for fast lookup!\n";
    cout << "Custom hash functions enable any type as key\n";

    return 0;
}
