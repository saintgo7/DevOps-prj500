/*
 * Program 150: Lambda Expressions
 *
 * Demonstrates:
 * - Lambda syntax and basics
 * - Capture modes (by value, by reference)
 * - Mutable lambdas
 * - Generic lambdas (auto parameters)
 * - Lambda return type deduction
 * - Immediately invoked lambdas
 * - Lambdas in STL algorithms
 * - Lambdas vs functors
 * - C++14 and C++17 lambda features
 * - C++20 template lambdas
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
#include <string>
#include <numeric>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Lambda basics
void lambdaBasics() {
    printSection("1. LAMBDA BASICS");

    // Simplest lambda
    cout << "\nSimplest lambda:\n";
    auto hello = []() { cout << "  Hello from lambda!\n"; };
    hello();

    // Lambda with parameters
    cout << "\nLambda with parameters:\n";
    auto add = [](int a, int b) { return a + b; };
    cout << "  add(3, 4) = " << add(3, 4) << "\n";

    // Lambda with explicit return type
    cout << "\nExplicit return type:\n";
    auto divide = [](int a, int b) -> double {
        return static_cast<double>(a) / b;
    };
    cout << "  divide(7, 2) = " << divide(7, 2) << "\n";

    // Immediately invoked lambda
    cout << "\nImmediately invoked lambda:\n";
    int result = [](int x) { return x * x; }(5);
    cout << "  Square of 5: " << result << "\n";

    // Multi-statement lambda
    cout << "\nMulti-statement lambda:\n";
    auto factorial = [](int n) {
        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    };
    cout << "  factorial(5) = " << factorial(5) << "\n";
}

// Capture modes
void captureModes() {
    printSection("2. CAPTURE MODES");

    int x = 10;
    int y = 20;

    // Capture by value
    cout << "\nCapture by value [=]:\n";
    auto lambda1 = [=]() {
        cout << "  x = " << x << ", y = " << y << "\n";
        // x = 30; // Error: cannot modify captured by value
    };
    lambda1();
    x = 100;
    cout << "  After x = 100:\n";
    lambda1();  // Still sees old value

    x = 10;  // Reset

    // Capture by reference
    cout << "\nCapture by reference [&]:\n";
    auto lambda2 = [&]() {
        cout << "  x = " << x << ", y = " << y << "\n";
        x = 30;  // Can modify
    };
    lambda2();
    cout << "  After lambda modified x:\n";
    lambda2();

    x = 10;  // Reset

    // Selective capture
    cout << "\nSelective capture:\n";
    auto lambda3 = [x, &y]() {
        cout << "  x (by value) = " << x << "\n";
        cout << "  y (by ref) = " << y << "\n";
        y = 200;  // Can modify y
    };
    lambda3();
    cout << "  After lambda, y = " << y << "\n";

    y = 20;  // Reset

    // Default capture with exceptions
    cout << "\nDefault capture with exceptions:\n";
    int z = 30;
    auto lambda4 = [=, &z]() {  // Capture all by value except z by reference
        cout << "  x = " << x << ", y = " << y << ", z = " << z << "\n";
        z = 300;
    };
    lambda4();
    cout << "  After lambda, z = " << z << "\n";

    // Capture this
    cout << "\nCapture this (for member functions):\n";
    struct MyClass {
        int value = 42;

        void demonstrate() {
            auto lambda = [this]() {
                cout << "    value = " << value << "\n";
                value = 100;
            };
            lambda();
            cout << "    After lambda, value = " << value << "\n";
        }
    };

    MyClass obj;
    obj.demonstrate();
}

// Mutable lambdas
void mutableLambdas() {
    printSection("3. MUTABLE LAMBDAS");

    int x = 10;

    cout << "\nNon-mutable lambda (error if uncommented):\n";
    auto lambda1 = [x]() {
        cout << "  x = " << x << "\n";
        // x = 20; // Error: cannot modify captured by value
    };
    lambda1();

    cout << "\nMutable lambda:\n";
    auto lambda2 = [x]() mutable {
        cout << "  Before: x = " << x << "\n";
        x = 20;
        cout << "  After: x = " << x << "\n";
    };
    lambda2();
    cout << "  Original x = " << x << " (unchanged)\n";

    cout << "\nMutable lambda as counter:\n";
    auto counter = [count = 0]() mutable {
        return ++count;
    };
    cout << "  Call 1: " << counter() << "\n";
    cout << "  Call 2: " << counter() << "\n";
    cout << "  Call 3: " << counter() << "\n";

    cout << "\nMutable vs reference capture:\n";
    int y = 10;
    auto by_value_mutable = [y]() mutable {
        y++;
        return y;
    };
    auto by_reference = [&y]() {
        y++;
        return y;
    };

    cout << "  Initial y = " << y << "\n";
    cout << "  by_value_mutable() = " << by_value_mutable() << ", y = " << y << "\n";
    cout << "  by_reference() = " << by_reference() << ", y = " << y << "\n";
}

// Generic lambdas (C++14)
void genericLambdas() {
    printSection("4. GENERIC LAMBDAS (C++14)");

    cout << "\nAuto parameters:\n";
    auto print = [](auto x) {
        cout << "  Value: " << x << "\n";
    };
    print(42);
    print(3.14);
    print("Hello");

    cout << "\nGeneric operations:\n";
    auto add = [](auto a, auto b) {
        return a + b;
    };
    cout << "  add(3, 4) = " << add(3, 4) << "\n";
    cout << "  add(3.5, 2.5) = " << add(3.5, 2.5) << "\n";
    cout << "  add(string(\"Hello\"), string(\" World\")) = "
         << add(string("Hello"), string(" World")) << "\n";

    cout << "\nGeneric container operations:\n";
    auto print_container = [](const auto& container) {
        cout << "  ";
        for (const auto& elem : container) {
            cout << elem << " ";
        }
        cout << "\n";
    };

    vector<int> v = {1, 2, 3, 4, 5};
    vector<string> words = {"hello", "world"};

    print_container(v);
    print_container(words);

    cout << "\nPerfect forwarding in lambdas:\n";
    auto forward_call = [](auto&& func, auto&&... args) {
        return func(forward<decltype(args)>(args)...);
    };

    auto square = [](int x) { return x * x; };
    cout << "  forward_call(square, 5) = " << forward_call(square, 5) << "\n";
}

// Lambdas with STL algorithms
void lambdasWithSTL() {
    printSection("5. LAMBDAS WITH STL ALGORITHMS");

    vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    cout << "\nOriginal vector: ";
    for (int x : v) cout << x << " ";
    cout << "\n";

    // for_each
    cout << "\nfor_each (print squares):\n  ";
    for_each(v.begin(), v.end(), [](int x) { cout << x * x << " "; });
    cout << "\n";

    // count_if
    cout << "\ncount_if (count evens):\n";
    int even_count = count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    cout << "  Even count: " << even_count << "\n";

    // find_if
    cout << "\nfind_if (first > 5):\n";
    auto it = find_if(v.begin(), v.end(), [](int x) { return x > 5; });
    cout << "  Found: " << (it != v.end() ? to_string(*it) : "not found") << "\n";

    // transform
    cout << "\ntransform (double each):\n";
    vector<int> doubled(v.size());
    transform(v.begin(), v.end(), doubled.begin(), [](int x) { return x * 2; });
    cout << "  Doubled: ";
    for (int x : doubled) cout << x << " ";
    cout << "\n";

    // remove_if
    cout << "\nremove_if (remove odds):\n";
    vector<int> v2 = v;
    v2.erase(remove_if(v2.begin(), v2.end(), [](int x) { return x % 2 == 1; }), v2.end());
    cout << "  After removing odds: ";
    for (int x : v2) cout << x << " ";
    cout << "\n";

    // sort with custom comparator
    cout << "\nsort (descending):\n";
    vector<int> v3 = v;
    sort(v3.begin(), v3.end(), [](int a, int b) { return a > b; });
    cout << "  Sorted: ";
    for (int x : v3) cout << x << " ";
    cout << "\n";

    // accumulate with lambda
    cout << "\naccumulate (product):\n";
    int product = accumulate(v.begin(), v.end(), 1,
                            [](int acc, int x) { return acc * x; });
    cout << "  Product: " << product << "\n";

    // Sorting strings by length
    cout << "\nSort strings by length:\n";
    vector<string> words = {"apple", "pie", "a", "to", "hello", "world"};
    sort(words.begin(), words.end(),
         [](const string& a, const string& b) { return a.length() < b.length(); });
    cout << "  Sorted: ";
    for (const auto& w : words) cout << w << " ";
    cout << "\n";
}

// Lambda as return value
void lambdaReturnValue() {
    printSection("6. RETURNING LAMBDAS");

    cout << "\nReturning lambda from function:\n";
    auto make_adder = [](int n) {
        return [n](int x) { return x + n; };
    };

    auto add_10 = make_adder(10);
    auto add_100 = make_adder(100);

    cout << "  add_10(5) = " << add_10(5) << "\n";
    cout << "  add_100(5) = " << add_100(5) << "\n";

    cout << "\nFactory function pattern:\n";
    auto make_multiplier = [](int factor) {
        return [factor](int x) { return x * factor; };
    };

    auto double_it = make_multiplier(2);
    auto triple_it = make_multiplier(3);

    cout << "  double_it(7) = " << double_it(7) << "\n";
    cout << "  triple_it(7) = " << triple_it(7) << "\n";

    cout << "\nPredicate factory:\n";
    auto make_range_checker = [](int min, int max) {
        return [min, max](int x) { return x >= min && x <= max; };
    };

    auto in_range = make_range_checker(10, 20);
    cout << "  in_range(15) = " << in_range(15) << "\n";
    cout << "  in_range(25) = " << in_range(25) << "\n";
}

// Init capture (C++14)
void initCapture() {
    printSection("7. INIT CAPTURE (C++14)");

    cout << "\nInit capture (capture by move):\n";
    auto ptr = make_unique<int>(42);
    auto lambda = [ptr = move(ptr)]() {
        cout << "  Value: " << *ptr << "\n";
    };
    lambda();
    // ptr is now null

    cout << "\nCapture with modification:\n";
    int x = 10;
    auto lambda2 = [y = x * 2]() {
        cout << "  y (x * 2) = " << y << "\n";
    };
    lambda2();

    cout << "\nCapture with computation:\n";
    vector<int> v = {1, 2, 3, 4, 5};
    auto lambda3 = [sum = accumulate(v.begin(), v.end(), 0)]() {
        cout << "  Captured sum = " << sum << "\n";
    };
    lambda3();

    cout << "\nCapture unique_ptr:\n";
    auto make_processor = []() {
        auto data = make_unique<string>("Important data");
        return [data = move(data)]() {
            cout << "  Processing: " << *data << "\n";
        };
    };
    auto processor = make_processor();
    processor();
}

// Constexpr lambdas (C++17)
void constexprLambdas() {
    printSection("8. CONSTEXPR LAMBDAS (C++17)");

    cout << "\nConstexpr lambda:\n";
    constexpr auto square = [](int x) { return x * x; };

    constexpr int result = square(5);
    cout << "  constexpr square(5) = " << result << "\n";

    // Can be used in compile-time contexts
    int arr[square(3)];
    cout << "  Array size (square(3)): " << sizeof(arr) / sizeof(int) << "\n";

    cout << "\nConstexpr factorial:\n";
    constexpr auto factorial = [](int n) {
        auto impl = [](int n, auto& self) -> int {
            return n <= 1 ? 1 : n * self(n - 1, self);
        };
        return impl(n, impl);
    };

    constexpr int fact5 = factorial(5);
    cout << "  factorial(5) = " << fact5 << "\n";
}

// Template lambdas (C++20)
void templateLambdas() {
    printSection("9. TEMPLATE LAMBDAS (C++20)");

    cout << "\nTemplate lambda (C++20 feature):\n";
    cout << "  Note: Requires C++20 compiler support\n";

    // C++20 syntax (may not compile on older compilers):
    // auto print = []<typename T>(T value) {
    //     cout << "  Value: " << value << " (type: " << typeid(T).name() << ")\n";
    // };

    cout << "  Example would show explicit template syntax in lambda\n";
}

// Practical examples
void practicalExamples() {
    printSection("10. PRACTICAL EXAMPLES");

    // Example 1: Filtering and transforming
    cout << "\nExample 1: Filter evens and square them\n";
    vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    vector<int> result;
    copy_if(nums.begin(), nums.end(), back_inserter(result),
            [](int x) { return x % 2 == 0; });
    transform(result.begin(), result.end(), result.begin(),
              [](int x) { return x * x; });

    cout << "  Result: ";
    for (int x : result) cout << x << " ";
    cout << "\n";

    // Example 2: Custom comparison for sorting
    cout << "\nExample 2: Sort people by age, then name\n";
    struct Person {
        string name;
        int age;
    };

    vector<Person> people = {
        {"Alice", 30}, {"Bob", 25}, {"Charlie", 30}, {"David", 25}
    };

    sort(people.begin(), people.end(), [](const Person& a, const Person& b) {
        if (a.age != b.age) return a.age < b.age;
        return a.name < b.name;
    });

    for (const auto& p : people) {
        cout << "  " << p.name << " (" << p.age << ")\n";
    }

    // Example 3: Recursive lambda
    cout << "\nExample 3: Recursive Fibonacci\n";
    function<int(int)> fib = [&fib](int n) -> int {
        return n <= 1 ? n : fib(n - 1) + fib(n - 2);
    };

    cout << "  fib(10) = " << fib(10) << "\n";

    // Example 4: State machine
    cout << "\nExample 4: Simple state machine\n";
    auto make_toggle = []() {
        return [state = false]() mutable {
            state = !state;
            return state;
        };
    };

    auto toggle = make_toggle();
    cout << "  Toggle: " << toggle() << "\n";
    cout << "  Toggle: " << toggle() << "\n";
    cout << "  Toggle: " << toggle() << "\n";
}

int main() {
    cout << "LAMBDA EXPRESSIONS COMPREHENSIVE GUIDE\n";
    cout << "======================================\n";

    lambdaBasics();
    captureModes();
    mutableLambdas();
    genericLambdas();
    lambdasWithSTL();
    lambdaReturnValue();
    initCapture();
    constexprLambdas();
    templateLambdas();
    practicalExamples();

    printSection("SUMMARY");
    cout << "\nLambda expressions:\n";
    cout << "- Syntax: [capture](params) { body }\n";
    cout << "- Capture: [=] by value, [&] by reference\n";
    cout << "- mutable: allows modification of captured values\n";
    cout << "- Generic lambdas: auto parameters (C++14)\n";
    cout << "- Init capture: [x = expr] (C++14)\n";
    cout << "- constexpr lambdas (C++17)\n";
    cout << "- Template lambdas (C++20)\n";
    cout << "- Perfect for STL algorithms and callbacks\n";

    return 0;
}
