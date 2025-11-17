/*
 * Program 149: Function Objects (Functors)
 *
 * Demonstrates:
 * - Function objects (functors) basics
 * - Predefined function objects (plus, minus, multiplies, etc.)
 * - Custom functors
 * - std::function wrapper
 * - Function pointers vs functors
 * - Stateful functors
 * - Callable objects
 * - Bind and placeholders
 * - Function composition
 */

#include <iostream>
#include <functional>
#include <algorithm>
#include <vector>
#include <string>
#include <numeric>

using namespace std;
using namespace std::placeholders;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic functor
void basicFunctors() {
    printSection("1. BASIC FUNCTORS");

    // Simple functor class
    struct Add {
        int operator()(int a, int b) const {
            return a + b;
        }
    };

    cout << "\nSimple functor:\n";
    Add add;
    cout << "  add(3, 4) = " << add(3, 4) << "\n";

    // Using with algorithms
    vector<int> v = {1, 2, 3, 4, 5};
    cout << "\n  Vector: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    int sum = accumulate(v.begin(), v.end(), 0, add);
    cout << "  Sum using functor: " << sum << "\n";

    // Generic functor template
    template<typename T>
    struct Multiply {
        T operator()(T a, T b) const {
            return a * b;
        }
    };

    Multiply<int> mult_int;
    Multiply<double> mult_double;

    cout << "\nGeneric functor:\n";
    cout << "  mult_int(3, 4) = " << mult_int(3, 4) << "\n";
    cout << "  mult_double(3.5, 2.0) = " << mult_double(3.5, 2.0) << "\n";
}

// Predefined function objects
void predefinedFunctors() {
    printSection("2. PREDEFINED FUNCTION OBJECTS");

    cout << "\nArithmetic operations:\n";
    cout << "  plus<int>()(3, 4) = " << plus<int>()(3, 4) << "\n";
    cout << "  minus<int>()(10, 3) = " << minus<int>()(10, 3) << "\n";
    cout << "  multiplies<int>()(3, 4) = " << multiplies<int>()(3, 4) << "\n";
    cout << "  divides<int>()(12, 3) = " << divides<int>()(12, 3) << "\n";
    cout << "  modulus<int>()(10, 3) = " << modulus<int>()(10, 3) << "\n";
    cout << "  negate<int>()(5) = " << negate<int>()(5) << "\n";

    cout << "\nComparison operations:\n";
    cout << "  equal_to<int>()(5, 5) = " << equal_to<int>()(5, 5) << "\n";
    cout << "  not_equal_to<int>()(5, 3) = " << not_equal_to<int>()(5, 3) << "\n";
    cout << "  greater<int>()(5, 3) = " << greater<int>()(5, 3) << "\n";
    cout << "  less<int>()(5, 3) = " << less<int>()(5, 3) << "\n";
    cout << "  greater_equal<int>()(5, 5) = " << greater_equal<int>()(5, 5) << "\n";
    cout << "  less_equal<int>()(3, 5) = " << less_equal<int>()(3, 5) << "\n";

    cout << "\nLogical operations:\n";
    cout << "  logical_and<bool>()(true, true) = " << logical_and<bool>()(true, true) << "\n";
    cout << "  logical_or<bool>()(true, false) = " << logical_or<bool>()(true, false) << "\n";
    cout << "  logical_not<bool>()(false) = " << logical_not<bool>()(false) << "\n";

    cout << "\nUsing with algorithms:\n";
    vector<int> v = {5, 2, 8, 1, 9, 3};
    cout << "  Original: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    sort(v.begin(), v.end(), greater<int>());
    cout << "  Sorted (descending): ";
    for (int x : v) cout << x << " ";
    cout << "\n";
}

// Custom functors
void customFunctors() {
    printSection("3. CUSTOM FUNCTORS");

    // Comparison functor
    struct CompareByLength {
        bool operator()(const string& a, const string& b) const {
            return a.length() < b.length();
        }
    };

    cout << "\nCustom comparison functor:\n";
    vector<string> words = {"apple", "pie", "a", "to", "hello", "world"};
    cout << "  Original: ";
    for (const auto& w : words) cout << w << " ";
    cout << "\n";

    sort(words.begin(), words.end(), CompareByLength());
    cout << "  Sorted by length: ";
    for (const auto& w : words) cout << w << " ";
    cout << "\n";

    // Predicate functor
    struct IsEven {
        bool operator()(int x) const {
            return x % 2 == 0;
        }
    };

    cout << "\nPredicate functor:\n";
    vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int even_count = count_if(nums.begin(), nums.end(), IsEven());
    cout << "  Count of evens: " << even_count << "\n";

    // Transformation functor
    struct Square {
        int operator()(int x) const {
            return x * x;
        }
    };

    cout << "\nTransformation functor:\n";
    vector<int> v = {1, 2, 3, 4, 5};
    vector<int> squared(5);
    transform(v.begin(), v.end(), squared.begin(), Square());
    cout << "  Original: ";
    for (int x : v) cout << x << " ";
    cout << "\n  Squared: ";
    for (int x : squared) cout << x << " ";
    cout << "\n";
}

// Stateful functors
void statefulFunctors() {
    printSection("4. STATEFUL FUNCTORS");

    // Counter functor
    class Counter {
        int count;
    public:
        Counter() : count(0) {}

        int operator()(int x) {
            count++;
            return x * count;
        }

        int getCount() const { return count; }
    };

    cout << "\nStateful counter functor:\n";
    vector<int> v = {1, 2, 3, 4, 5};
    vector<int> result(5);

    Counter counter;
    transform(v.begin(), v.end(), result.begin(), ref(counter));

    cout << "  Original: ";
    for (int x : v) cout << x << " ";
    cout << "\n  Transformed: ";
    for (int x : result) cout << x << " ";
    cout << "\n  Call count: " << counter.getCount() << "\n";

    // Accumulator functor
    class Accumulator {
        int sum;
    public:
        Accumulator() : sum(0) {}

        void operator()(int x) {
            sum += x;
        }

        int getSum() const { return sum; }
    };

    cout << "\nAccumulator functor:\n";
    Accumulator acc;
    acc = for_each(v.begin(), v.end(), acc);
    cout << "  Sum: " << acc.getSum() << "\n";

    // Threshold filter
    class ThresholdFilter {
        int threshold;
    public:
        ThresholdFilter(int t) : threshold(t) {}

        bool operator()(int x) const {
            return x > threshold;
        }

        void setThreshold(int t) { threshold = t; }
        int getThreshold() const { return threshold; }
    };

    cout << "\nThreshold filter:\n";
    vector<int> nums = {1, 5, 10, 15, 20, 25};
    ThresholdFilter filter(10);

    cout << "  Numbers > 10: ";
    for (int x : nums) {
        if (filter(x)) cout << x << " ";
    }
    cout << "\n";
}

// std::function wrapper
void stdFunction() {
    printSection("5. STD::FUNCTION WRAPPER");

    cout << "\nstd::function can hold any callable:\n";

    // Function pointer
    auto add_func = [](int a, int b) { return a + b; };
    function<int(int, int)> f1 = add_func;
    cout << "  Lambda: f1(3, 4) = " << f1(3, 4) << "\n";

    // Functor
    struct Multiply {
        int operator()(int a, int b) const { return a * b; }
    };
    function<int(int, int)> f2 = Multiply();
    cout << "  Functor: f2(3, 4) = " << f2(3, 4) << "\n";

    // Regular function
    function<int(int, int)> f3 = [](int a, int b) { return a - b; };
    cout << "  Lambda 2: f3(10, 3) = " << f3(10, 3) << "\n";

    // Storing in container
    cout << "\nStoring functions in container:\n";
    vector<function<int(int, int)>> operations;
    operations.push_back([](int a, int b) { return a + b; });
    operations.push_back([](int a, int b) { return a - b; });
    operations.push_back([](int a, int b) { return a * b; });
    operations.push_back([](int a, int b) { return a / b; });

    int a = 10, b = 3;
    vector<string> ops = {"+", "-", "*", "/"};
    for (size_t i = 0; i < operations.size(); i++) {
        cout << "  " << a << " " << ops[i] << " " << b << " = "
             << operations[i](a, b) << "\n";
    }

    // Callback pattern
    cout << "\nCallback pattern:\n";
    auto process = [](const vector<int>& v, function<void(int)> callback) {
        for (int x : v) callback(x);
    };

    vector<int> nums = {1, 2, 3, 4, 5};
    cout << "  Print squares: ";
    process(nums, [](int x) { cout << x * x << " "; });
    cout << "\n";
}

// std::bind
void stdBind() {
    printSection("6. STD::BIND");

    // Bind function arguments
    auto add = [](int a, int b, int c) { return a + b + c; };

    cout << "\nBinding arguments:\n";
    cout << "  add(1, 2, 3) = " << add(1, 2, 3) << "\n";

    auto add_with_10 = bind(add, 10, _1, _2);
    cout << "  bind(add, 10, _1, _2)(2, 3) = " << add_with_10(2, 3) << "\n";

    auto add_10_and_20 = bind(add, 10, 20, _1);
    cout << "  bind(add, 10, 20, _1)(3) = " << add_10_and_20(3) << "\n";

    // Reorder arguments
    cout << "\nReordering arguments:\n";
    auto subtract = [](int a, int b) { return a - b; };
    cout << "  subtract(10, 3) = " << subtract(10, 3) << "\n";

    auto subtract_reversed = bind(subtract, _2, _1);
    cout << "  bind(subtract, _2, _1)(10, 3) = " << subtract_reversed(10, 3) << "\n";

    // Bind with member functions
    cout << "\nBinding member functions:\n";
    struct Calculator {
        int value;
        Calculator(int v) : value(v) {}
        int add(int x) { return value + x; }
    };

    Calculator calc(100);
    auto bound_add = bind(&Calculator::add, &calc, _1);
    cout << "  calc.value = " << calc.value << "\n";
    cout << "  bound_add(50) = " << bound_add(50) << "\n";

    // Using bind with algorithms
    cout << "\nUsing bind with algorithms:\n";
    vector<int> v = {1, 5, 10, 15, 20};
    cout << "  Vector: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    auto greater_than_10 = bind(greater<int>(), _1, 10);
    int count = count_if(v.begin(), v.end(), greater_than_10);
    cout << "  Count > 10: " << count << "\n";
}

// Function vs function pointers
void functionVsPointer() {
    printSection("7. FUNCTORS vs FUNCTION POINTERS");

    // Function pointer
    int (*func_ptr)(int, int) = [](int a, int b) { return a + b; };

    cout << "\nFunction pointer:\n";
    cout << "  func_ptr(3, 4) = " << func_ptr(3, 4) << "\n";

    // Functor advantages
    cout << "\nFunctor advantages:\n";
    cout << "  1. Can maintain state\n";
    cout << "  2. Can be inlined (better performance)\n";
    cout << "  3. Can have multiple operator() overloads\n";
    cout << "  4. Type-safe\n";

    struct StatefulFunctor {
        int state;
        StatefulFunctor(int s) : state(s) {}

        int operator()(int x) {
            return x + state;
        }

        // Multiple overloads
        double operator()(double x) {
            return x * state;
        }
    };

    StatefulFunctor sf(10);
    cout << "  sf(5) [int] = " << sf(5) << "\n";
    cout << "  sf(3.5) [double] = " << sf(3.5) << "\n";

    cout << "\nInlining demonstration:\n";
    cout << "  Functors can be inlined by compiler\n";
    cout << "  Function pointers prevent inlining\n";
    cout << "  Result: Functors often faster in tight loops\n";
}

// Practical examples
void practicalExamples() {
    printSection("8. PRACTICAL EXAMPLES");

    // Example 1: Custom sorting
    cout << "\nExample 1: Custom sorting with functor\n";
    struct Person {
        string name;
        int age;
    };

    struct SortByAge {
        bool operator()(const Person& a, const Person& b) const {
            return a.age < b.age;
        }
    };

    vector<Person> people = {
        {"Alice", 30},
        {"Bob", 25},
        {"Charlie", 35}
    };

    sort(people.begin(), people.end(), SortByAge());

    cout << "  Sorted by age:\n";
    for (const auto& p : people) {
        cout << "    " << p.name << ": " << p.age << "\n";
    }

    // Example 2: Generator functor
    cout << "\nExample 2: Generator functor\n";
    class FibonacciGenerator {
        int a, b;
    public:
        FibonacciGenerator() : a(0), b(1) {}

        int operator()() {
            int result = a;
            int next = a + b;
            a = b;
            b = next;
            return result;
        }
    };

    FibonacciGenerator fib;
    cout << "  First 10 Fibonacci numbers: ";
    for (int i = 0; i < 10; i++) {
        cout << fib() << " ";
    }
    cout << "\n";

    // Example 3: Configurable predicate
    cout << "\nExample 3: Configurable range filter\n";
    class RangeFilter {
        int min, max;
    public:
        RangeFilter(int min, int max) : min(min), max(max) {}

        bool operator()(int x) const {
            return x >= min && x <= max;
        }
    };

    vector<int> nums = {1, 5, 10, 15, 20, 25, 30};
    RangeFilter filter(10, 20);

    cout << "  Numbers in [10, 20]: ";
    for (int x : nums) {
        if (filter(x)) cout << x << " ";
    }
    cout << "\n";
}

int main() {
    cout << "FUNCTION OBJECTS COMPREHENSIVE GUIDE\n";
    cout << "====================================\n";

    basicFunctors();
    predefinedFunctors();
    customFunctors();
    statefulFunctors();
    stdFunction();
    stdBind();
    functionVsPointer();
    practicalExamples();

    printSection("SUMMARY");
    cout << "\nFunction objects (functors):\n";
    cout << "- Objects that can be called like functions\n";
    cout << "- Define operator() to make class callable\n";
    cout << "- Can maintain state (unlike regular functions)\n";
    cout << "- Often faster than function pointers (inlining)\n";
    cout << "- std::function provides type-erased wrapper\n";
    cout << "- std::bind enables partial application\n";
    cout << "- Essential for generic programming with STL\n";

    return 0;
}
