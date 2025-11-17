/*
 * Program 147: STL Algorithms
 *
 * Demonstrates:
 * - Non-modifying algorithms (find, count, search, etc.)
 * - Modifying algorithms (copy, transform, replace, etc.)
 * - Sorting and related (sort, partial_sort, nth_element)
 * - Binary search algorithms (lower_bound, upper_bound, binary_search)
 * - Set operations (union, intersection, difference)
 * - Heap algorithms (make_heap, push_heap, pop_heap)
 * - Numeric algorithms (accumulate, inner_product, etc.)
 * - Algorithm complexity and best practices
 */

#include <iostream>
#include <algorithm>
#include <numeric>
#include <vector>
#include <string>
#include <iterator>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

template<typename T>
void printVector(const vector<T>& v, const string& label = "Vector") {
    cout << label << ": ";
    for (const auto& x : v) cout << x << " ";
    cout << "\n";
}

// Non-modifying sequence operations
void nonModifyingAlgorithms() {
    printSection("1. NON-MODIFYING ALGORITHMS");

    vector<int> v = {1, 2, 3, 4, 5, 3, 6, 7, 3, 8};
    printVector(v);

    // find
    cout << "\nfind:\n";
    auto it = find(v.begin(), v.end(), 5);
    cout << "  find(5): " << (it != v.end() ? "Found at pos " + to_string(it - v.begin()) : "Not found") << "\n";

    // find_if
    cout << "\nfind_if (first even):\n";
    it = find_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    cout << "  Result: " << (it != v.end() ? to_string(*it) : "Not found") << "\n";

    // count
    cout << "\ncount:\n";
    cout << "  count(3): " << count(v.begin(), v.end(), 3) << "\n";

    // count_if
    cout << "\ncount_if (evens):\n";
    cout << "  Result: " << count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; }) << "\n";

    // all_of, any_of, none_of
    cout << "\nall_of, any_of, none_of:\n";
    cout << "  all_of positive: " << all_of(v.begin(), v.end(), [](int x) { return x > 0; }) << "\n";
    cout << "  any_of > 5: " << any_of(v.begin(), v.end(), [](int x) { return x > 5; }) << "\n";
    cout << "  none_of negative: " << none_of(v.begin(), v.end(), [](int x) { return x < 0; }) << "\n";

    // for_each
    cout << "\nfor_each (print each * 2):\n  ";
    for_each(v.begin(), v.end(), [](int x) { cout << x * 2 << " "; });
    cout << "\n";

    // adjacent_find
    vector<int> v2 = {1, 2, 3, 3, 4, 5};
    cout << "\nadjacent_find (consecutive duplicates):\n";
    printVector(v2, "Vector");
    it = adjacent_find(v2.begin(), v2.end());
    cout << "  Result: " << (it != v2.end() ? to_string(*it) : "Not found") << "\n";

    // search
    vector<int> v3 = {1, 2, 3, 4, 5};
    vector<int> pattern = {3, 4};
    cout << "\nsearch (find subsequence):\n";
    printVector(v3, "Haystack");
    printVector(pattern, "Needle");
    it = search(v3.begin(), v3.end(), pattern.begin(), pattern.end());
    cout << "  Found at position: " << (it != v3.end() ? to_string(it - v3.begin()) : "Not found") << "\n";
}

// Modifying sequence operations
void modifyingAlgorithms() {
    printSection("2. MODIFYING ALGORITHMS");

    // copy
    cout << "\ncopy:\n";
    vector<int> src = {1, 2, 3, 4, 5};
    vector<int> dst(5);
    copy(src.begin(), src.end(), dst.begin());
    printVector(src, "Source");
    printVector(dst, "Destination");

    // copy_if
    cout << "\ncopy_if (evens only):\n";
    vector<int> evens;
    copy_if(src.begin(), src.end(), back_inserter(evens),
            [](int x) { return x % 2 == 0; });
    printVector(evens, "Evens");

    // transform
    cout << "\ntransform (square each):\n";
    vector<int> v = {1, 2, 3, 4, 5};
    vector<int> squared(5);
    transform(v.begin(), v.end(), squared.begin(),
              [](int x) { return x * x; });
    printVector(v, "Original");
    printVector(squared, "Squared");

    // transform (binary)
    cout << "\ntransform (add two vectors):\n";
    vector<int> v1 = {1, 2, 3, 4, 5};
    vector<int> v2 = {10, 20, 30, 40, 50};
    vector<int> sum(5);
    transform(v1.begin(), v1.end(), v2.begin(), sum.begin(),
              [](int a, int b) { return a + b; });
    printVector(sum, "Sum");

    // fill and fill_n
    cout << "\nfill:\n";
    vector<int> v3(5);
    fill(v3.begin(), v3.end(), 7);
    printVector(v3, "After fill(7)");

    // generate
    cout << "\ngenerate:\n";
    int n = 0;
    generate(v3.begin(), v3.end(), [&n]() { return n++; });
    printVector(v3, "Generated");

    // replace
    cout << "\nreplace:\n";
    vector<int> v4 = {1, 2, 3, 2, 4, 2, 5};
    printVector(v4, "Before replace(2, 99)");
    replace(v4.begin(), v4.end(), 2, 99);
    printVector(v4, "After replace");

    // replace_if
    cout << "\nreplace_if (evens -> 0):\n";
    vector<int> v5 = {1, 2, 3, 4, 5, 6};
    printVector(v5, "Before");
    replace_if(v5.begin(), v5.end(), [](int x) { return x % 2 == 0; }, 0);
    printVector(v5, "After");

    // remove and erase idiom
    cout << "\nremove-erase idiom:\n";
    vector<int> v6 = {1, 2, 3, 2, 4, 2, 5};
    printVector(v6, "Before remove(2)");
    v6.erase(remove(v6.begin(), v6.end(), 2), v6.end());
    printVector(v6, "After remove-erase");

    // unique
    cout << "\nunique (remove consecutive duplicates):\n";
    vector<int> v7 = {1, 1, 2, 2, 2, 3, 3, 4, 5, 5};
    printVector(v7, "Before unique");
    v7.erase(unique(v7.begin(), v7.end()), v7.end());
    printVector(v7, "After unique");

    // reverse
    cout << "\nreverse:\n";
    vector<int> v8 = {1, 2, 3, 4, 5};
    printVector(v8, "Before");
    reverse(v8.begin(), v8.end());
    printVector(v8, "After");

    // rotate
    cout << "\nrotate (rotate left by 2):\n";
    vector<int> v9 = {1, 2, 3, 4, 5};
    printVector(v9, "Before");
    rotate(v9.begin(), v9.begin() + 2, v9.end());
    printVector(v9, "After");

    // shuffle
    cout << "\nrandom_shuffle (deprecated in C++14, use shuffle):\n";
    vector<int> v10 = {1, 2, 3, 4, 5};
    printVector(v10, "Original");
    // shuffle requires random engine (not shown for simplicity)
}

// Sorting and related operations
void sortingAlgorithms() {
    printSection("3. SORTING ALGORITHMS");

    // sort
    cout << "\nsort:\n";
    vector<int> v = {5, 2, 8, 1, 9, 3};
    printVector(v, "Before sort");
    sort(v.begin(), v.end());
    printVector(v, "After sort");

    // sort with custom comparator
    cout << "\nsort (descending):\n";
    sort(v.begin(), v.end(), greater<int>());
    printVector(v, "Descending");

    // stable_sort
    cout << "\nstable_sort (preserves relative order):\n";
    vector<pair<int, char>> pairs = {{3, 'a'}, {1, 'b'}, {3, 'c'}, {2, 'd'}, {1, 'e'}};
    stable_sort(pairs.begin(), pairs.end(),
                [](auto& a, auto& b) { return a.first < b.first; });
    cout << "  Result: ";
    for (auto [num, ch] : pairs) cout << "(" << num << "," << ch << ") ";
    cout << "\n";

    // partial_sort
    cout << "\npartial_sort (first 3 elements):\n";
    vector<int> v2 = {5, 2, 8, 1, 9, 3, 7, 4, 6};
    printVector(v2, "Before");
    partial_sort(v2.begin(), v2.begin() + 3, v2.end());
    printVector(v2, "After (first 3 sorted)");

    // nth_element
    cout << "\nnth_element (5th element in sorted position):\n";
    vector<int> v3 = {5, 2, 8, 1, 9, 3, 7, 4, 6};
    printVector(v3, "Before");
    nth_element(v3.begin(), v3.begin() + 4, v3.end());
    printVector(v3, "After (v[4] in correct position)");
    cout << "  5th element: " << v3[4] << "\n";

    // is_sorted
    cout << "\nis_sorted:\n";
    cout << "  {1,2,3,4,5}: " << is_sorted(vector<int>{1,2,3,4,5}.begin(),
                                           vector<int>{1,2,3,4,5}.end()) << "\n";
    cout << "  {5,2,3,4,1}: " << is_sorted(vector<int>{5,2,3,4,1}.begin(),
                                           vector<int>{5,2,3,4,1}.end()) << "\n";

    // partition
    cout << "\npartition (odds first):\n";
    vector<int> v4 = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    printVector(v4, "Before");
    auto pivot = partition(v4.begin(), v4.end(), [](int x) { return x % 2 == 1; });
    printVector(v4, "After partition");
    cout << "  Pivot at position: " << (pivot - v4.begin()) << "\n";
}

// Binary search algorithms
void binarySearchAlgorithms() {
    printSection("4. BINARY SEARCH ALGORITHMS");

    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    printVector(v, "Sorted vector");

    // binary_search
    cout << "\nbinary_search:\n";
    cout << "  binary_search(5): " << binary_search(v.begin(), v.end(), 5) << "\n";
    cout << "  binary_search(11): " << binary_search(v.begin(), v.end(), 11) << "\n";

    // lower_bound
    cout << "\nlower_bound (first >= value):\n";
    auto lb = lower_bound(v.begin(), v.end(), 5);
    cout << "  lower_bound(5): " << (lb != v.end() ? to_string(*lb) : "end") << "\n";

    // upper_bound
    cout << "\nupper_bound (first > value):\n";
    auto ub = upper_bound(v.begin(), v.end(), 5);
    cout << "  upper_bound(5): " << (ub != v.end() ? to_string(*ub) : "end") << "\n";

    // equal_range
    cout << "\nequal_range:\n";
    auto [first, last] = equal_range(v.begin(), v.end(), 5);
    cout << "  equal_range(5): [" << *first << ", " << *last << ")\n";
}

// Set operations
void setOperations() {
    printSection("5. SET OPERATIONS (on sorted ranges)");

    vector<int> v1 = {1, 2, 3, 4, 5};
    vector<int> v2 = {3, 4, 5, 6, 7};
    printVector(v1, "Set 1");
    printVector(v2, "Set 2");

    // set_union
    cout << "\nset_union:\n";
    vector<int> result;
    set_union(v1.begin(), v1.end(), v2.begin(), v2.end(),
              back_inserter(result));
    printVector(result, "Union");

    // set_intersection
    cout << "\nset_intersection:\n";
    result.clear();
    set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(),
                     back_inserter(result));
    printVector(result, "Intersection");

    // set_difference
    cout << "\nset_difference:\n";
    result.clear();
    set_difference(v1.begin(), v1.end(), v2.begin(), v2.end(),
                   back_inserter(result));
    printVector(result, "v1 - v2");

    // set_symmetric_difference
    cout << "\nset_symmetric_difference:\n";
    result.clear();
    set_symmetric_difference(v1.begin(), v1.end(), v2.begin(), v2.end(),
                            back_inserter(result));
    printVector(result, "Symmetric diff");

    // includes
    cout << "\nincludes:\n";
    vector<int> subset = {2, 3, 4};
    bool is_subset = includes(v1.begin(), v1.end(), subset.begin(), subset.end());
    cout << "  {2,3,4} subset of v1: " << is_subset << "\n";
}

// Heap operations
void heapOperations() {
    printSection("6. HEAP OPERATIONS");

    vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};
    printVector(v, "Original");

    // make_heap
    cout << "\nmake_heap:\n";
    make_heap(v.begin(), v.end());
    printVector(v, "After make_heap");
    cout << "  Top (max): " << v.front() << "\n";

    // push_heap
    cout << "\npush_heap:\n";
    v.push_back(10);
    push_heap(v.begin(), v.end());
    printVector(v, "After push_heap(10)");
    cout << "  Top (max): " << v.front() << "\n";

    // pop_heap
    cout << "\npop_heap:\n";
    pop_heap(v.begin(), v.end());
    int max_val = v.back();
    v.pop_back();
    cout << "  Popped value: " << max_val << "\n";
    printVector(v, "After pop_heap");

    // sort_heap
    cout << "\nsort_heap:\n";
    sort_heap(v.begin(), v.end());
    printVector(v, "After sort_heap (ascending)");

    // is_heap
    cout << "\nis_heap:\n";
    vector<int> v2 = {9, 5, 6, 1, 4, 2, 3};
    make_heap(v2.begin(), v2.end());
    cout << "  After make_heap: " << is_heap(v2.begin(), v2.end()) << "\n";
    cout << "  After sort: " << is_heap(v.begin(), v.end()) << "\n";
}

// Numeric algorithms
void numericAlgorithms() {
    printSection("7. NUMERIC ALGORITHMS");

    vector<int> v = {1, 2, 3, 4, 5};
    printVector(v);

    // accumulate
    cout << "\naccumulate (sum):\n";
    int sum = accumulate(v.begin(), v.end(), 0);
    cout << "  Sum: " << sum << "\n";

    // accumulate with custom operation
    cout << "\naccumulate (product):\n";
    int product = accumulate(v.begin(), v.end(), 1, multiplies<int>());
    cout << "  Product: " << product << "\n";

    // inner_product
    cout << "\ninner_product (dot product):\n";
    vector<int> v1 = {1, 2, 3};
    vector<int> v2 = {4, 5, 6};
    int dot = inner_product(v1.begin(), v1.end(), v2.begin(), 0);
    cout << "  {1,2,3} · {4,5,6} = " << dot << "\n";

    // partial_sum
    cout << "\npartial_sum (running sum):\n";
    vector<int> v3 = {1, 2, 3, 4, 5};
    vector<int> partial(5);
    partial_sum(v3.begin(), v3.end(), partial.begin());
    printVector(v3, "Original");
    printVector(partial, "Partial sums");

    // adjacent_difference
    cout << "\nadjacent_difference:\n";
    vector<int> v4 = {1, 3, 6, 10, 15};
    vector<int> diff(5);
    adjacent_difference(v4.begin(), v4.end(), diff.begin());
    printVector(v4, "Original");
    printVector(diff, "Differences");

    // iota (C++11)
    cout << "\niota (fill with incrementing values):\n";
    vector<int> v5(10);
    iota(v5.begin(), v5.end(), 1);
    printVector(v5, "After iota(1)");
}

// Min/Max operations
void minMaxOperations() {
    printSection("8. MIN/MAX OPERATIONS");

    vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};
    printVector(v);

    // min/max
    cout << "\nmin/max:\n";
    cout << "  min(3, 5): " << min(3, 5) << "\n";
    cout << "  max(3, 5): " << max(3, 5) << "\n";

    // min_element/max_element
    cout << "\nmin_element/max_element:\n";
    auto min_it = min_element(v.begin(), v.end());
    auto max_it = max_element(v.begin(), v.end());
    cout << "  min: " << *min_it << " at position " << (min_it - v.begin()) << "\n";
    cout << "  max: " << *max_it << " at position " << (max_it - v.begin()) << "\n";

    // minmax_element
    cout << "\nminmax_element:\n";
    auto [min_it2, max_it2] = minmax_element(v.begin(), v.end());
    cout << "  min: " << *min_it2 << ", max: " << *max_it2 << "\n";

    // clamp (C++17)
    cout << "\nclamp (limit value to range):\n";
    cout << "  clamp(3, 5, 10): " << clamp(3, 5, 10) << "\n";
    cout << "  clamp(7, 5, 10): " << clamp(7, 5, 10) << "\n";
    cout << "  clamp(12, 5, 10): " << clamp(12, 5, 10) << "\n";
}

int main() {
    cout << "STL ALGORITHMS COMPREHENSIVE GUIDE\n";
    cout << "==================================\n";

    nonModifyingAlgorithms();
    modifyingAlgorithms();
    sortingAlgorithms();
    binarySearchAlgorithms();
    setOperations();
    heapOperations();
    numericAlgorithms();
    minMaxOperations();

    printSection("SUMMARY");
    cout << "\nSTL provides 100+ algorithms for common operations:\n";
    cout << "- Non-modifying: find, count, search, for_each\n";
    cout << "- Modifying: copy, transform, replace, remove\n";
    cout << "- Sorting: sort, partial_sort, nth_element\n";
    cout << "- Binary search: lower_bound, upper_bound\n";
    cout << "- Set ops: union, intersection, difference\n";
    cout << "- Heap: make_heap, push_heap, pop_heap\n";
    cout << "- Numeric: accumulate, partial_sum, iota\n";
    cout << "\nAlways prefer algorithms over manual loops!\n";

    return 0;
}
