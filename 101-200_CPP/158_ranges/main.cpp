/*
 * Program 158: C++20 Ranges
 *
 * Demonstrates:
 * - Ranges library overview
 * - Range views (filter, transform, take, drop, etc.)
 * - Range adaptors
 * - Range algorithms
 * - Lazy evaluation
 * - Range composition
 * - Projection in algorithms
 * - Range factories
 * - Practical range applications
 */

#include <iostream>
#include <vector>
#include <ranges>
#include <algorithm>
#include <string>
#include <numeric>

using namespace std;
namespace views = ranges::views;
namespace rng = ranges;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic ranges
void basicRanges() {
    printSection("1. BASIC RANGES");

    cout << "\nRange concept:\n";
    cout << "  - Object with begin() and end()\n";
    cout << "  - Containers are ranges\n";
    cout << "  - Arrays are ranges\n";
    cout << "  - Views are lightweight ranges\n";

    vector<int> v = {1, 2, 3, 4, 5};

    cout << "\nDirect iteration:\n";
    cout << "  ";
    for (int x : v) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nUsing ranges::for_each:\n";
    cout << "  ";
    rng::for_each(v, [](int x) { cout << x << " "; });
    cout << "\n";
}

// Range views - filter
void rangeViewsFilter() {
    printSection("2. RANGE VIEWS - FILTER");

    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    cout << "\nOriginal vector:\n";
    cout << "  ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\nFilter evens:\n";
    cout << "  ";
    auto evens = v | views::filter([](int x) { return x % 2 == 0; });
    for (int x : evens) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nFilter odds:\n";
    cout << "  ";
    auto odds = v | views::filter([](int x) { return x % 2 == 1; });
    for (int x : odds) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nFilter > 5:\n";
    cout << "  ";
    auto greater_than_5 = v | views::filter([](int x) { return x > 5; });
    for (int x : greater_than_5) {
        cout << x << " ";
    }
    cout << "\n";
}

// Range views - transform
void rangeViewsTransform() {
    printSection("3. RANGE VIEWS - TRANSFORM");

    vector<int> v = {1, 2, 3, 4, 5};

    cout << "\nOriginal:\n";
    cout << "  ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\nTransform (square each):\n";
    cout << "  ";
    auto squared = v | views::transform([](int x) { return x * x; });
    for (int x : squared) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nTransform (double each):\n";
    cout << "  ";
    auto doubled = v | views::transform([](int x) { return x * 2; });
    for (int x : doubled) {
        cout << x << " ";
    }
    cout << "\n";

    vector<string> words = {"hello", "world", "foo"};
    cout << "\nTransform strings (to uppercase first char):\n";
    cout << "  ";
    auto capitalized = words | views::transform([](string s) {
        if (!s.empty()) s[0] = toupper(s[0]);
        return s;
    });
    for (const auto& s : capitalized) {
        cout << s << " ";
    }
    cout << "\n";
}

// Range views - take, drop
void rangeViewsTakeDrop() {
    printSection("4. RANGE VIEWS - TAKE/DROP");

    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    cout << "\nOriginal:\n";
    cout << "  ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\nTake first 5:\n";
    cout << "  ";
    auto first_5 = v | views::take(5);
    for (int x : first_5) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nDrop first 5:\n";
    cout << "  ";
    auto after_5 = v | views::drop(5);
    for (int x : after_5) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\ntake_while (< 6):\n";
    cout << "  ";
    auto until_6 = v | views::take_while([](int x) { return x < 6; });
    for (int x : until_6) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\ndrop_while (< 6):\n";
    cout << "  ";
    auto from_6 = v | views::drop_while([](int x) { return x < 6; });
    for (int x : from_6) {
        cout << x << " ";
    }
    cout << "\n";
}

// Range composition
void rangeComposition() {
    printSection("5. RANGE COMPOSITION");

    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    cout << "\nChaining operations:\n";
    cout << "  Original: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\n  Filter evens | Transform (square) | Take first 3:\n";
    cout << "  ";
    auto result = v
        | views::filter([](int x) { return x % 2 == 0; })
        | views::transform([](int x) { return x * x; })
        | views::take(3);

    for (int x : result) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\n  Drop 5 | Filter odds | Transform (*10):\n";
    cout << "  ";
    auto result2 = v
        | views::drop(5)
        | views::filter([](int x) { return x % 2 == 1; })
        | views::transform([](int x) { return x * 10; });

    for (int x : result2) {
        cout << x << " ";
    }
    cout << "\n";
}

// Lazy evaluation
void lazyEvaluation() {
    printSection("6. LAZY EVALUATION");

    cout << "\nRanges are lazy - operations not executed until iteration\n";

    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    cout << "\nDefining pipeline (no execution yet):\n";
    auto pipeline = v
        | views::filter([](int x) {
            cout << "    Filtering " << x << "\n";
            return x % 2 == 0;
          })
        | views::transform([](int x) {
            cout << "    Transforming " << x << "\n";
            return x * x;
          });

    cout << "\nIterating (execution happens now):\n";
    cout << "  First element: ";
    auto it = pipeline.begin();
    cout << *it << "\n";

    cout << "\n  Second element: ";
    ++it;
    cout << *it << "\n";

    cout << "\nOnly processes elements as needed!\n";
}

// Range algorithms
void rangeAlgorithms() {
    printSection("7. RANGE ALGORITHMS");

    vector<int> v = {5, 2, 8, 1, 9, 3, 7, 4, 6};

    cout << "\nOriginal:\n";
    cout << "  ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\nranges::sort:\n";
    rng::sort(v);
    cout << "  ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\nranges::reverse:\n";
    rng::reverse(v);
    cout << "  ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    cout << "\nranges::find:\n";
    auto it = rng::find(v, 5);
    cout << "  Found 5: " << (it != v.end() ? "Yes" : "No") << "\n";

    cout << "\nranges::count:\n";
    v.push_back(5);
    v.push_back(5);
    cout << "  Count of 5: " << rng::count(v, 5) << "\n";

    cout << "\nranges::min/max:\n";
    cout << "  Min: " << rng::min(v) << "\n";
    cout << "  Max: " << rng::max(v) << "\n";
}

// Projection
void rangeProjection() {
    printSection("8. PROJECTION");

    struct Person {
        string name;
        int age;
    };

    vector<Person> people = {
        {"Alice", 30},
        {"Bob", 25},
        {"Charlie", 35},
        {"David", 28}
    };

    cout << "\nSort by age (using projection):\n";
    rng::sort(people, {}, &Person::age);

    for (const auto& p : people) {
        cout << "  " << p.name << ": " << p.age << "\n";
    }

    cout << "\nSort by name:\n";
    rng::sort(people, {}, &Person::name);

    for (const auto& p : people) {
        cout << "  " << p.name << ": " << p.age << "\n";
    }

    cout << "\nFind person with age > 30:\n";
    auto it = rng::find_if(people, [](int age) { return age > 30; }, &Person::age);
    if (it != people.end()) {
        cout << "  Found: " << it->name << " (" << it->age << ")\n";
    }
}

// Range factories
void rangeFactories() {
    printSection("9. RANGE FACTORIES");

    cout << "\nviews::iota (infinite sequence):\n";
    cout << "  First 10 numbers starting from 1:\n";
    cout << "  ";
    for (int x : views::iota(1) | views::take(10)) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nviews::iota with limit:\n";
    cout << "  ";
    for (int x : views::iota(1, 11)) {  // [1, 11)
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nviews::empty:\n";
    auto empty = views::empty<int>;
    cout << "  Size: " << rng::distance(empty) << "\n";

    cout << "\nviews::single:\n";
    cout << "  ";
    for (int x : views::single(42)) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nviews::repeat (C++23):\n";
    cout << "  Note: May not be available in all compilers yet\n";
}

// Practical example: Data processing pipeline
void practicalExample() {
    printSection("10. PRACTICAL EXAMPLE: DATA PROCESSING");

    struct Transaction {
        string type;
        double amount;
        string category;
    };

    vector<Transaction> transactions = {
        {"debit", 50.00, "food"},
        {"credit", 1000.00, "salary"},
        {"debit", 30.00, "transport"},
        {"debit", 100.00, "food"},
        {"debit", 20.00, "transport"},
        {"credit", 200.00, "refund"},
        {"debit", 75.00, "food"}
    };

    cout << "\nTotal debit amount for food:\n";
    auto food_debits = transactions
        | views::filter([](const Transaction& t) {
            return t.type == "debit" && t.category == "food";
          })
        | views::transform([](const Transaction& t) {
            return t.amount;
          });

    double total = 0;
    for (double amount : food_debits) {
        total += amount;
    }
    cout << "  Total: $" << total << "\n";

    cout << "\nTop 3 largest debits:\n";
    vector<Transaction> debits;
    rng::copy_if(transactions, back_inserter(debits),
                 [](const Transaction& t) { return t.type == "debit"; });

    rng::sort(debits, greater<>{}, &Transaction::amount);

    for (const auto& t : debits | views::take(3)) {
        cout << "  $" << t.amount << " (" << t.category << ")\n";
    }

    cout << "\nAdvantages of ranges:\n";
    cout << "  - Composable operations\n";
    cout << "  - Lazy evaluation (efficient)\n";
    cout << "  - Cleaner code (no manual loops)\n";
    cout << "  - Type-safe\n";
}

// More views
void moreViews() {
    printSection("11. MORE VIEWS");

    vector<int> v = {1, 2, 3, 4, 5};

    cout << "\nviews::reverse:\n";
    cout << "  ";
    for (int x : v | views::reverse) {
        cout << x << " ";
    }
    cout << "\n";

    cout << "\nviews::elements (for pairs/tuples):\n";
    vector<pair<int, string>> pairs = {{1, "one"}, {2, "two"}, {3, "three"}};
    cout << "  Keys: ";
    for (int x : pairs | views::elements<0>) {
        cout << x << " ";
    }
    cout << "\n  Values: ";
    for (const auto& s : pairs | views::elements<1>) {
        cout << s << " ";
    }
    cout << "\n";

    cout << "\nviews::keys and views::values:\n";
    cout << "  Keys: ";
    for (int x : pairs | views::keys) {
        cout << x << " ";
    }
    cout << "\n  Values: ";
    for (const auto& s : pairs | views::values) {
        cout << s << " ";
    }
    cout << "\n";

    cout << "\nviews::join (flatten):\n";
    vector<vector<int>> nested = {{1, 2}, {3, 4}, {5, 6}};
    cout << "  ";
    for (int x : nested | views::join) {
        cout << x << " ";
    }
    cout << "\n";
}

int main() {
    cout << "C++20 RANGES COMPREHENSIVE GUIDE\n";
    cout << "================================\n";

    basicRanges();
    rangeViewsFilter();
    rangeViewsTransform();
    rangeViewsTakeDrop();
    rangeComposition();
    lazyEvaluation();
    rangeAlgorithms();
    rangeProjection();
    rangeFactories();
    practicalExample();
    moreViews();

    printSection("SUMMARY");
    cout << "\nC++20 Ranges:\n";
    cout << "- Modern approach to working with sequences\n";
    cout << "- Views are lightweight, composable, lazy\n";
    cout << "- Pipe operator | for chaining\n";
    cout << "- Common views: filter, transform, take, drop\n";
    cout << "- Range algorithms work on any range\n";
    cout << "- Projection support in algorithms\n";
    cout << "- Factories: iota, empty, single\n";
    cout << "- Cleaner, more expressive code\n";
    cout << "\nRanges revolutionize STL algorithm usage!\n";

    return 0;
}
