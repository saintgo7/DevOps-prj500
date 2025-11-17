/*
 * Program 155: Variadic Templates
 *
 * Demonstrates:
 * - Variadic template syntax
 * - Parameter packs
 * - Pack expansion
 * - Recursive variadic templates
 * - Fold expressions (C++17)
 * - sizeof... operator
 * - Perfect forwarding with variadic templates
 * - Variadic class templates
 * - Practical applications
 */

#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <memory>
#include <type_traits>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic variadic template
template<typename... Args>
void print_types() {
    cout << "  Number of types: " << sizeof...(Args) << "\n";
}

template<typename T>
void print_single(T value) {
    cout << value << " ";
}

template<typename... Args>
void print_all(Args... args) {
    (print_single(args), ...);  // Fold expression (C++17)
    cout << "\n";
}

void basicVariadicTemplates() {
    printSection("1. BASIC VARIADIC TEMPLATES");

    cout << "\nsizeof... operator:\n";
    print_types<>();
    print_types<int>();
    print_types<int, double>();
    print_types<int, double, string>();

    cout << "\nPrinting multiple arguments:\n";
    cout << "  ";
    print_all(1, 2, 3, 4, 5);
    cout << "  ";
    print_all("hello", "world", "foo");
    cout << "  ";
    print_all(1, 3.14, "mixed", true);
}

// Recursive variadic templates
template<typename T>
T sum(T value) {
    return value;
}

template<typename T, typename... Args>
T sum(T first, Args... rest) {
    return first + sum(rest...);
}

// Print with recursion
void print_recursive() {
    cout << "\n";
}

template<typename T, typename... Args>
void print_recursive(T first, Args... rest) {
    cout << first << " ";
    print_recursive(rest...);
}

void recursiveVariadicTemplates() {
    printSection("2. RECURSIVE VARIADIC TEMPLATES");

    cout << "\nVariadic sum:\n";
    cout << "  sum(1) = " << sum(1) << "\n";
    cout << "  sum(1, 2, 3) = " << sum(1, 2, 3) << "\n";
    cout << "  sum(1, 2, 3, 4, 5) = " << sum(1, 2, 3, 4, 5) << "\n";
    cout << "  sum(1.5, 2.5, 3.0) = " << sum(1.5, 2.5, 3.0) << "\n";

    cout << "\nRecursive print:\n";
    cout << "  ";
    print_recursive(1, 2, 3, 4, 5);
    cout << "  ";
    print_recursive("hello", "world", "foo", "bar");
    cout << "  ";
    print_recursive(1, "two", 3.0, "four", 5);
}

// Fold expressions (C++17)
template<typename... Args>
auto sum_fold(Args... args) {
    return (args + ...);  // Unary right fold
}

template<typename... Args>
auto product_fold(Args... args) {
    return (args * ...);
}

template<typename... Args>
bool all_true(Args... args) {
    return (args && ...);
}

template<typename... Args>
bool any_true(Args... args) {
    return (args || ...);
}

template<typename... Args>
void print_fold(Args... args) {
    ((cout << args << " "), ...);  // Fold with comma operator
    cout << "\n";
}

void foldExpressions() {
    printSection("3. FOLD EXPRESSIONS (C++17)");

    cout << "\nUnary fold expressions:\n";
    cout << "  sum_fold(1, 2, 3, 4, 5) = " << sum_fold(1, 2, 3, 4, 5) << "\n";
    cout << "  product_fold(1, 2, 3, 4, 5) = " << product_fold(1, 2, 3, 4, 5) << "\n";

    cout << "\nLogical folds:\n";
    cout << "  all_true(true, true, true) = " << all_true(true, true, true) << "\n";
    cout << "  all_true(true, false, true) = " << all_true(true, false, true) << "\n";
    cout << "  any_true(false, false, true) = " << any_true(false, false, true) << "\n";
    cout << "  any_true(false, false, false) = " << any_true(false, false, false) << "\n";

    cout << "\nFold with comma operator:\n";
    cout << "  ";
    print_fold(1, 2, 3, 4, 5);
    cout << "  ";
    print_fold("hello", "world", "foo");
}

// Pack expansion patterns
template<typename... Args>
void print_sizes(Args... args) {
    cout << "  Sizes: ";
    ((cout << sizeof(args) << " "), ...);
    cout << "\n";
}

template<typename... Args>
void print_doubled(Args... args) {
    cout << "  Doubled: ";
    ((cout << args * 2 << " "), ...);
    cout << "\n";
}

template<typename... Args>
auto make_vector(Args... args) {
    return vector<common_type_t<Args...>>{args...};
}

void packExpansion() {
    printSection("4. PACK EXPANSION");

    cout << "\nExpanding pack in different contexts:\n";
    print_sizes(1, 2.0, 3L, 4LL);

    cout << "\nExpanding with operations:\n";
    print_doubled(1, 2, 3, 4, 5);

    cout << "\nPack expansion in initializer list:\n";
    auto v = make_vector(1, 2, 3, 4, 5);
    cout << "  Vector: ";
    for (int x : v) cout << x << " ";
    cout << "\n";
}

// Perfect forwarding
template<typename... Args>
void forward_to_print(Args&&... args) {
    print_all(forward<Args>(args)...);
}

template<typename T, typename... Args>
unique_ptr<T> make_unique_variadic(Args&&... args) {
    return unique_ptr<T>(new T(forward<Args>(args)...));
}

void perfectForwarding() {
    printSection("5. PERFECT FORWARDING");

    cout << "\nForwarding arguments:\n";
    cout << "  ";
    forward_to_print(1, 2, 3, 4, 5);

    cout << "\nForwarding to constructor:\n";
    struct Point {
        int x, y;
        Point(int x, int y) : x(x), y(y) {}
    };

    auto ptr = make_unique_variadic<Point>(10, 20);
    cout << "  Created Point(" << ptr->x << ", " << ptr->y << ")\n";

    auto str_ptr = make_unique_variadic<string>("Hello, World!");
    cout << "  Created string: " << *str_ptr << "\n";
}

// Variadic class templates
template<typename... Types>
class Tuple;

template<>
class Tuple<> {
public:
    void print() const {
        cout << "  Empty tuple\n";
    }
};

template<typename Head, typename... Tail>
class Tuple<Head, Tail...> : private Tuple<Tail...> {
private:
    Head head;
public:
    Tuple(Head h, Tail... t) : Tuple<Tail...>(t...), head(h) {}

    void print() const {
        cout << head << " ";
        Tuple<Tail...>::print();
    }

    Head getHead() const { return head; }
};

template<typename... Types>
class TypeList {
public:
    static constexpr size_t size = sizeof...(Types);

    static void print_info() {
        cout << "  TypeList with " << size << " types\n";
    }
};

void variadicClassTemplates() {
    printSection("6. VARIADIC CLASS TEMPLATES");

    cout << "\nCustom Tuple implementation:\n";
    Tuple<int, double, string> t1(42, 3.14, "hello");
    cout << "  ";
    t1.print();

    Tuple<int> t2(100);
    cout << "  ";
    t2.print();

    cout << "\nTypeList:\n";
    TypeList<int, double, string>::print_info();
    TypeList<int, int, int, int>::print_info();
}

// Index sequence
template<size_t... Indices>
void print_indices() {
    cout << "  Indices: ";
    ((cout << Indices << " "), ...);
    cout << "\n";
}

template<typename Tuple, size_t... Indices>
void print_tuple_impl(const Tuple& t, index_sequence<Indices...>) {
    ((cout << get<Indices>(t) << " "), ...);
    cout << "\n";
}

template<typename... Args>
void print_tuple(const tuple<Args...>& t) {
    cout << "  ";
    print_tuple_impl(t, index_sequence_for<Args...>{});
}

void indexSequence() {
    printSection("7. INDEX SEQUENCE");

    cout << "\nGenerating index sequences:\n";
    print_indices<0, 1, 2, 3, 4>();

    cout << "\nUsing with std::tuple:\n";
    auto t = make_tuple(1, 3.14, "hello", true);
    print_tuple(t);
}

// Type traits with variadic templates
template<typename... Args>
struct are_all_integral {
    static constexpr bool value = (is_integral_v<Args> && ...);
};

template<typename... Args>
struct are_all_same : false_type {};

template<typename T, typename... Args>
struct are_all_same<T, Args...> {
    static constexpr bool value = (is_same_v<T, Args> && ...);
};

void typeTraitsWithVariadic() {
    printSection("8. TYPE TRAITS WITH VARIADIC");

    cout << "\nare_all_integral:\n";
    cout << "  <int, long, short>: "
         << are_all_integral<int, long, short>::value << "\n";
    cout << "  <int, double, long>: "
         << are_all_integral<int, double, long>::value << "\n";

    cout << "\nare_all_same:\n";
    cout << "  <int, int, int>: "
         << are_all_same<int, int, int>::value << "\n";
    cout << "  <int, int, double>: "
         << are_all_same<int, int, double>::value << "\n";
}

// Variadic min/max
template<typename T>
T min_variadic(T value) {
    return value;
}

template<typename T, typename... Args>
T min_variadic(T first, Args... rest) {
    T rest_min = min_variadic(rest...);
    return first < rest_min ? first : rest_min;
}

template<typename... Args>
auto min_fold(Args... args) {
    return (args < ... );  // Binary left fold
}

void variadicMinMax() {
    printSection("9. VARIADIC MIN/MAX");

    cout << "\nVariadic minimum:\n";
    cout << "  min(5) = " << min_variadic(5) << "\n";
    cout << "  min(5, 3, 8, 1, 9) = " << min_variadic(5, 3, 8, 1, 9) << "\n";
    cout << "  min(3.14, 2.71, 1.41) = " << min_variadic(3.14, 2.71, 1.41) << "\n";
}

// Practical example: Logger
template<typename... Args>
void log(const string& level, Args... args) {
    cout << "[" << level << "] ";
    ((cout << args << " "), ...);
    cout << "\n";
}

template<typename... Args>
void debug(Args... args) {
    log("DEBUG", args...);
}

template<typename... Args>
void info(Args... args) {
    log("INFO", args...);
}

template<typename... Args>
void error(Args... args) {
    log("ERROR", args...);
}

void practicalExample() {
    printSection("10. PRACTICAL EXAMPLE: LOGGER");

    cout << "\nVariadic logger:\n";
    debug("Application", "started", "at", "port", 8080);
    info("User", "logged", "in:", "user123");
    error("Connection", "failed:", "timeout", "after", 30, "seconds");

    cout << "\nAdvantages:\n";
    cout << "  - Type-safe\n";
    cout << "  - Flexible number of arguments\n";
    cout << "  - No format strings needed\n";
    cout << "  - Compile-time checking\n";
}

int main() {
    cout << "VARIADIC TEMPLATES COMPREHENSIVE GUIDE\n";
    cout << "======================================\n";

    basicVariadicTemplates();
    recursiveVariadicTemplates();
    foldExpressions();
    packExpansion();
    perfectForwarding();
    variadicClassTemplates();
    indexSequence();
    typeTraitsWithVariadic();
    variadicMinMax();
    practicalExample();

    printSection("SUMMARY");
    cout << "\nVariadic template features:\n";
    cout << "- Accept any number of template arguments\n";
    cout << "- Parameter packs: typename... Args\n";
    cout << "- Pack expansion: args...\n";
    cout << "- sizeof... for pack size\n";
    cout << "- Fold expressions (C++17): (args + ...)\n";
    cout << "- Perfect forwarding: Args&&... args\n";
    cout << "- Enables generic, flexible interfaces\n";
    cout << "- Foundation for std::tuple, std::variant, etc.\n";
    cout << "\nVariadic templates enable truly generic programming!\n";

    return 0;
}
