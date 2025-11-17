/*
 * Program 157: C++20 Concepts
 *
 * Demonstrates:
 * - Concept syntax and definition
 * - requires clause
 * - requires expression
 * - Standard library concepts
 * - Custom concepts
 * - Concept composition
 * - Type constraints
 * - Abbreviated function templates
 * - Concepts vs SFINAE
 * - Practical concept applications
 */

#include <iostream>
#include <concepts>
#include <string>
#include <vector>
#include <type_traits>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic concept definition
template<typename T>
concept Numeric = integral<T> || floating_point<T>;

template<typename T>
concept Printable = requires(T t) {
    { cout << t } -> convertible_to<ostream&>;
};

template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> same_as<T>;
};

void basicConcepts() {
    printSection("1. BASIC CONCEPTS");

    cout << "\nNumeric concept:\n";
    cout << "  Numeric<int>: " << Numeric<int> << "\n";
    cout << "  Numeric<double>: " << Numeric<double> << "\n";
    cout << "  Numeric<string>: " << Numeric<string> << "\n";

    cout << "\nPrintable concept:\n";
    cout << "  Printable<int>: " << Printable<int> << "\n";
    cout << "  Printable<string>: " << Printable<string> << "\n";

    cout << "\nAddable concept:\n";
    cout << "  Addable<int>: " << Addable<int> << "\n";
    cout << "  Addable<string>: " << Addable<string> << "\n";
}

// Using concepts in function templates
template<Numeric T>
T add(T a, T b) {
    return a + b;
}

template<typename T>
requires Numeric<T>
T multiply(T a, T b) {
    return a * b;
}

template<typename T>
T subtract(T a, T b) requires Numeric<T> {
    return a - b;
}

void conceptsInFunctions() {
    printSection("2. CONCEPTS IN FUNCTION TEMPLATES");

    cout << "\nThree equivalent syntaxes:\n";

    cout << "\n1. Concept as template parameter:\n";
    cout << "   template<Numeric T>\n";
    cout << "   add(10, 20) = " << add(10, 20) << "\n";
    cout << "   add(3.14, 2.86) = " << add(3.14, 2.86) << "\n";

    cout << "\n2. requires clause after template:\n";
    cout << "   template<typename T> requires Numeric<T>\n";
    cout << "   multiply(5, 6) = " << multiply(5, 6) << "\n";

    cout << "\n3. requires clause after parameter list:\n";
    cout << "   subtract(100, 30) = " << subtract(100, 30) << "\n";

    // These would cause compile errors:
    // add(string("hello"), string("world"));
}

// Abbreviated function templates (C++20)
void print(Printable auto value) {
    cout << "  " << value << "\n";
}

auto square(Numeric auto x) {
    return x * x;
}

void abbreviatedTemplates() {
    printSection("3. ABBREVIATED FUNCTION TEMPLATES");

    cout << "\nAbbreviated syntax:\n";
    cout << "  void print(Printable auto value)\n";
    cout << "  Equivalent to: template<Printable T> void print(T value)\n";

    cout << "\nUsing abbreviated templates:\n";
    print(42);
    print(3.14);
    print("Hello");

    cout << "\nsquare function:\n";
    cout << "  square(5) = " << square(5) << "\n";
    cout << "  square(3.5) = " << square(3.5) << "\n";
}

// Standard library concepts
void standardConcepts() {
    printSection("4. STANDARD LIBRARY CONCEPTS");

    cout << "\nCore language concepts:\n";
    cout << "  same_as<int, int>: " << same_as<int, int> << "\n";
    cout << "  derived_from<string, basic_string<char>>: "
         << derived_from<string, basic_string<char>> << "\n";
    cout << "  convertible_to<int, double>: " << convertible_to<int, double> << "\n";

    cout << "\nComparison concepts:\n";
    cout << "  equality_comparable<int>: " << equality_comparable<int> << "\n";
    cout << "  totally_ordered<string>: " << totally_ordered<string> << "\n";

    cout << "\nObject concepts:\n";
    cout << "  movable<vector<int>>: " << movable<vector<int>> << "\n";
    cout << "  copyable<string>: " << copyable<string> << "\n";
    cout << "  semiregular<int>: " << semiregular<int> << "\n";
    cout << "  regular<int>: " << regular<int> << "\n";

    cout << "\nCallable concepts:\n";
    cout << "  invocable<decltype([](int x){return x*2;}), int>: "
         << invocable<decltype([](int x){return x*2;}), int> << "\n";

    cout << "\nIterator concepts:\n";
    cout << "  forward_iterator<vector<int>::iterator>: "
         << forward_iterator<vector<int>::iterator> << "\n";
    cout << "  random_access_iterator<vector<int>::iterator>: "
         << random_access_iterator<vector<int>::iterator> << "\n";
}

// Custom concepts
template<typename T>
concept Arithmetic = Numeric<T> && requires(T a, T b) {
    { a + b } -> same_as<T>;
    { a - b } -> same_as<T>;
    { a * b } -> same_as<T>;
    { a / b } -> same_as<T>;
};

template<typename T>
concept Container = requires(T t) {
    typename T::value_type;
    typename T::iterator;
    { t.begin() } -> same_as<typename T::iterator>;
    { t.end() } -> same_as<typename T::iterator>;
    { t.size() } -> convertible_to<size_t>;
};

template<typename T>
concept StringLike = convertible_to<T, string> || same_as<T, const char*>;

void customConcepts() {
    printSection("5. CUSTOM CONCEPTS");

    cout << "\nArithmetic concept:\n";
    cout << "  Arithmetic<int>: " << Arithmetic<int> << "\n";
    cout << "  Arithmetic<double>: " << Arithmetic<double> << "\n";

    cout << "\nContainer concept:\n";
    cout << "  Container<vector<int>>: " << Container<vector<int>> << "\n";
    cout << "  Container<string>: " << Container<string> << "\n";
    cout << "  Container<int>: " << Container<int> << "\n";

    cout << "\nStringLike concept:\n";
    cout << "  StringLike<string>: " << StringLike<string> << "\n";
    cout << "  StringLike<const char*>: " << StringLike<const char*> << "\n";
    cout << "  StringLike<int>: " << StringLike<int> << "\n";
}

// Concept composition
template<typename T>
concept SignedNumeric = Numeric<T> && signed_integral<T>;

template<typename T>
concept UnsignedNumeric = Numeric<T> && unsigned_integral<T>;

template<typename T>
concept Incrementable = requires(T t) {
    { ++t } -> same_as<T&>;
    { t++ } -> same_as<T>;
};

template<typename T>
concept Decrementable = requires(T t) {
    { --t } -> same_as<T&>;
    { t-- } -> same_as<T>;
};

template<typename T>
concept Bidirectional = Incrementable<T> && Decrementable<T>;

void conceptComposition() {
    printSection("6. CONCEPT COMPOSITION");

    cout << "\nSigned vs Unsigned:\n";
    cout << "  SignedNumeric<int>: " << SignedNumeric<int> << "\n";
    cout << "  SignedNumeric<unsigned int>: " << SignedNumeric<unsigned int> << "\n";
    cout << "  UnsignedNumeric<unsigned int>: " << UnsignedNumeric<unsigned int> << "\n";

    cout << "\nBidirectional (requires Incrementable AND Decrementable):\n";
    cout << "  Bidirectional<int>: " << Bidirectional<int> << "\n";

    cout << "\nConcept composition with &&, ||:\n";
    cout << "  - Use && for conjunction (all must be true)\n";
    cout << "  - Use || for disjunction (at least one true)\n";
    cout << "  - Use ! for negation\n";
}

// requires expression details
template<typename T>
concept HasSize = requires(T t) {
    { t.size() } -> convertible_to<size_t>;
};

template<typename T>
concept Iterable = requires(T t) {
    { t.begin() };
    { t.end() };
    requires same_as<decltype(t.begin()), decltype(t.end())>;
};

template<typename T>
concept Comparable = requires(T a, T b) {
    { a == b } -> convertible_to<bool>;
    { a != b } -> convertible_to<bool>;
    { a < b } -> convertible_to<bool>;
    { a > b } -> convertible_to<bool>;
    { a <= b } -> convertible_to<bool>;
    { a >= b } -> convertible_to<bool>;
};

void requiresExpression() {
    printSection("7. REQUIRES EXPRESSION");

    cout << "\nrequires expression components:\n";
    cout << "  1. Simple requirements: { expression };\n";
    cout << "  2. Type requirements: typename T::type;\n";
    cout << "  3. Compound requirements: { expression } -> constraint;\n";
    cout << "  4. Nested requirements: requires constraint;\n";

    cout << "\nHasSize concept:\n";
    cout << "  HasSize<vector<int>>: " << HasSize<vector<int>> << "\n";
    cout << "  HasSize<int>: " << HasSize<int> << "\n";

    cout << "\nComparable concept:\n";
    cout << "  Comparable<int>: " << Comparable<int> << "\n";
    cout << "  Comparable<string>: " << Comparable<string> << "\n";
}

// Concepts with class templates
template<typename T>
requires Numeric<T>
class Calculator {
private:
    T value;
public:
    Calculator(T v) : value(v) {}

    T add(T x) { return value + x; }
    T multiply(T x) { return value * x; }

    void print() const {
        cout << "  Value: " << value << "\n";
    }
};

template<Container C>
void print_container(const C& container) {
    cout << "  Container: ";
    for (const auto& elem : container) {
        cout << elem << " ";
    }
    cout << "\n";
}

void conceptsWithClasses() {
    printSection("8. CONCEPTS WITH CLASS TEMPLATES");

    cout << "\nCalculator with Numeric constraint:\n";
    Calculator<int> calc1(10);
    calc1.print();
    cout << "  add(5) = " << calc1.add(5) << "\n";

    Calculator<double> calc2(3.14);
    cout << "  multiply(2.0) = " << calc2.multiply(2.0) << "\n";

    // Would fail: Calculator<string> calc3("hello");

    cout << "\nConstrained function templates:\n";
    vector<int> v = {1, 2, 3, 4, 5};
    print_container(v);

    vector<string> words = {"hello", "world"};
    print_container(words);
}

// Concepts vs SFINAE
// SFINAE version (old way)
template<typename T>
typename enable_if<is_integral<T>::value, T>::type
old_add(T a, T b) {
    return a + b;
}

// Concepts version (new way)
template<typename T>
requires integral<T>
T new_add(T a, T b) {
    return a + b;
}

void conceptsVsSFINAE() {
    printSection("9. CONCEPTS vs SFINAE");

    cout << "\nSFINAE (old way):\n";
    cout << "  template<typename T>\n";
    cout << "  typename enable_if<is_integral<T>::value, T>::type\n";
    cout << "  - Complex syntax\n";
    cout << "  - Poor error messages\n";
    cout << "  - Hard to read and maintain\n";

    cout << "\nConcepts (new way):\n";
    cout << "  template<typename T> requires integral<T>\n";
    cout << "  - Clear and concise\n";
    cout << "  - Better error messages\n";
    cout << "  - Self-documenting\n";
    cout << "  - Compile faster\n";

    cout << "\nBoth produce same result:\n";
    cout << "  old_add(10, 20) = " << old_add(10, 20) << "\n";
    cout << "  new_add(10, 20) = " << new_add(10, 20) << "\n";
}

// Practical example: Type-safe container operations
template<typename C>
requires Container<C> && Numeric<typename C::value_type>
auto sum_container(const C& container) {
    typename C::value_type result = 0;
    for (const auto& elem : container) {
        result += elem;
    }
    return result;
}

template<typename C>
requires Container<C>
void print_first_last(const C& container) {
    if (container.size() > 0) {
        cout << "  First: " << *container.begin() << "\n";
        cout << "  Last: " << *prev(container.end()) << "\n";
    }
}

void practicalExample() {
    printSection("10. PRACTICAL EXAMPLE");

    cout << "\nType-safe container operations:\n";

    vector<int> nums = {1, 2, 3, 4, 5};
    cout << "  sum_container(nums) = " << sum_container(nums) << "\n";

    vector<double> values = {1.5, 2.5, 3.0};
    cout << "  sum_container(values) = " << sum_container(values) << "\n";

    cout << "\nPrint first and last:\n";
    vector<string> words = {"hello", "world", "foo", "bar"};
    print_first_last(words);

    cout << "\nAdvantages:\n";
    cout << "  - Compile-time type checking\n";
    cout << "  - Clear requirements in code\n";
    cout << "  - Better error messages\n";
    cout << "  - Self-documenting interfaces\n";
}

int main() {
    cout << "C++20 CONCEPTS COMPREHENSIVE GUIDE\n";
    cout << "==================================\n";

    basicConcepts();
    conceptsInFunctions();
    abbreviatedTemplates();
    standardConcepts();
    customConcepts();
    conceptComposition();
    requiresExpression();
    conceptsWithClasses();
    conceptsVsSFINAE();
    practicalExample();

    printSection("SUMMARY");
    cout << "\nC++20 Concepts:\n";
    cout << "- Named constraints on template parameters\n";
    cout << "- Clearer than SFINAE\n";
    cout << "- Better compile-time error messages\n";
    cout << "- Self-documenting code\n";
    cout << "- Three syntaxes: template param, requires clause, trailing\n";
    cout << "- Standard library concepts available\n";
    cout << "- Can compose with &&, ||, !\n";
    cout << "- Abbreviated function templates\n";
    cout << "\nConcepts make generic programming more accessible!\n";

    return 0;
}
