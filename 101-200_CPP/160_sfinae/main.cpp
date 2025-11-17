/*
 * Program 160: SFINAE (Substitution Failure Is Not An Error)
 *
 * Demonstrates:
 * - SFINAE principle
 * - enable_if patterns
 * - SFINAE with function overloading
 * - SFINAE with class templates
 * - decltype and declval
 * - void_t idiom
 * - Detection idiom
 * - Tag dispatching
 * - SFINAE vs Concepts
 * - Practical SFINAE applications
 */

#include <iostream>
#include <type_traits>
#include <string>
#include <vector>
#include <iterator>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic SFINAE principle
void sfinaePrinciple() {
    printSection("1. SFINAE PRINCIPLE");

    cout << "\nSFINAE = Substitution Failure Is Not An Error\n";
    cout << "\nKey concept:\n";
    cout << "  - When template substitution fails, it's not a compiler error\n";
    cout << "  - The candidate is simply removed from overload set\n";
    cout << "  - Enables compile-time conditional compilation\n";
    cout << "  - Foundation of template metaprogramming\n";

    cout << "\nExample: Function enabled only for integers\n";
    cout << "  template<typename T>\n";
    cout << "  typename enable_if<is_integral<T>::value, T>::type\n";
    cout << "  func(T value) { return value * 2; }\n";

    cout << "\nIf T is not integral:\n";
    cout << "  - Substitution fails\n";
    cout << "  - Function removed from candidates\n";
    cout << "  - No error (unless no other overload matches)\n";
}

// enable_if patterns
template<typename T>
typename enable_if<is_integral<T>::value, T>::type
process_integral(T value) {
    cout << "  Processing integer: " << value << "\n";
    return value * 2;
}

template<typename T>
typename enable_if<is_floating_point<T>::value, T>::type
process_integral(T value) {
    cout << "  Processing floating-point: " << value << "\n";
    return value * 3.0;
}

// C++14 enable_if_t shorthand
template<typename T>
enable_if_t<is_same<T, string>::value, void>
process_integral(T value) {
    cout << "  Processing string: " << value << "\n";
}

void enableIfPatterns() {
    printSection("2. ENABLE_IF PATTERNS");

    cout << "\nBasic enable_if:\n";
    process_integral(42);
    process_integral(3.14);
    process_integral(string("hello"));

    cout << "\nThree ways to use enable_if:\n";
    cout << "  1. Return type: enable_if<Cond, T>::type\n";
    cout << "  2. Template parameter: enable_if<Cond, T>::type* = nullptr\n";
    cout << "  3. Function parameter: enable_if<Cond, T>::type* = nullptr\n";

    cout << "\nC++14 shorthand:\n";
    cout << "  enable_if_t<Cond, T> instead of enable_if<Cond, T>::type\n";
}

// Function template overloading with SFINAE
template<typename T>
enable_if_t<is_arithmetic<T>::value, T>
safe_divide(T a, T b) {
    return b != 0 ? a / b : 0;
}

template<typename Iter>
enable_if_t<
    is_same<typename iterator_traits<Iter>::iterator_category, random_access_iterator_tag>::value,
    void
>
advance_impl(Iter& it, int n) {
    cout << "  Random access advance (O(1))\n";
    it += n;
}

template<typename Iter>
enable_if_t<
    !is_same<typename iterator_traits<Iter>::iterator_category, random_access_iterator_tag>::value,
    void
>
advance_impl(Iter& it, int n) {
    cout << "  Sequential advance (O(n))\n";
    while (n-- > 0) ++it;
}

void functionOverloadingSFINAE() {
    printSection("3. FUNCTION OVERLOADING WITH SFINAE");

    cout << "\nType-safe division:\n";
    cout << "  safe_divide(10, 2) = " << safe_divide(10, 2) << "\n";
    cout << "  safe_divide(10.0, 3.0) = " << safe_divide(10.0, 3.0) << "\n";

    cout << "\nIterator category dispatch:\n";
    vector<int> v = {1, 2, 3, 4, 5};
    auto it1 = v.begin();
    advance_impl(it1, 2);
    cout << "  Value after advance: " << *it1 << "\n";
}

// SFINAE with class templates
template<typename T, typename Enable = void>
class Container {
public:
    void info() {
        cout << "  Generic container\n";
    }
};

template<typename T>
class Container<T, enable_if_t<is_integral<T>::value>> {
public:
    void info() {
        cout << "  Integer container (optimized)\n";
    }
};

template<typename T>
class Container<T, enable_if_t<is_floating_point<T>::value>> {
public:
    void info() {
        cout << "  Floating-point container (optimized)\n";
    }
};

void classTemplateSFINAE() {
    printSection("4. CLASS TEMPLATE SFINAE");

    cout << "\nSpecialized containers based on type:\n";
    Container<string> c1;
    c1.info();

    Container<int> c2;
    c2.info();

    Container<double> c3;
    c3.info();

    cout << "\nSFINAE enables partial specialization-like behavior\n";
}

// decltype and declval
template<typename T>
auto get_size(T& container) -> decltype(container.size()) {
    return container.size();
}

template<typename T>
auto add_values(T a, T b) -> decltype(a + b) {
    return a + b;
}

void decltypeAndDeclval() {
    printSection("5. DECLTYPE AND DECLVAL");

    cout << "\ndecltype - deduces expression type:\n";
    vector<int> v = {1, 2, 3};
    cout << "  get_size(vector) = " << get_size(v) << "\n";
    cout << "  add_values(1, 2) = " << add_values(1, 2) << "\n";
    cout << "  add_values(1.5, 2.5) = " << add_values(1.5, 2.5) << "\n";

    cout << "\ndeclval - creates value of type without constructing:\n";
    cout << "  Used in unevaluated contexts\n";
    cout << "  declval<T>() returns T&& without constructor\n";
    cout << "  Essential for SFINAE with complex types\n";
}

// void_t idiom (C++17)
template<typename, typename = void>
struct has_size : false_type {};

template<typename T>
struct has_size<T, void_t<decltype(declval<T>().size())>> : true_type {};

template<typename, typename = void>
struct has_begin_end : false_type {};

template<typename T>
struct has_begin_end<T, void_t<
    decltype(declval<T>().begin()),
    decltype(declval<T>().end())
>> : true_type {};

void voidTIdiom() {
    printSection("6. VOID_T IDIOM");

    cout << "\nvoid_t simplifies SFINAE detection:\n";

    cout << "\nhas_size trait:\n";
    cout << "  has_size<vector<int>>: " << has_size<vector<int>>::value << "\n";
    cout << "  has_size<string>: " << has_size<string>::value << "\n";
    cout << "  has_size<int>: " << has_size<int>::value << "\n";

    cout << "\nhas_begin_end trait:\n";
    cout << "  has_begin_end<vector<int>>: " << has_begin_end<vector<int>>::value << "\n";
    cout << "  has_begin_end<int>: " << has_begin_end<int>::value << "\n";

    cout << "\nvoid_t definition:\n";
    cout << "  template<typename...> using void_t = void;\n";
    cout << "  Maps any types to void, enabling SFINAE\n";
}

// Detection idiom
template<typename T>
using size_type_t = typename T::size_type;

template<typename T>
using value_type_t = typename T::value_type;

template<typename T, typename = void>
struct has_value_type : false_type {};

template<typename T>
struct has_value_type<T, void_t<value_type_t<T>>> : true_type {};

void detectionIdiom() {
    printSection("7. DETECTION IDIOM");

    cout << "\nDetecting nested types:\n";

    cout << "\nhas_value_type:\n";
    cout << "  has_value_type<vector<int>>: " << has_value_type<vector<int>>::value << "\n";
    cout << "  has_value_type<int>: " << has_value_type<int>::value << "\n";

    cout << "\nDetection idiom pattern:\n";
    cout << "  1. Define alias template for what to detect\n";
    cout << "  2. Create trait with void_t\n";
    cout << "  3. Specialize for detection\n";
}

// Tag dispatching
struct has_fast_size {};
struct no_fast_size {};

template<typename T>
using size_tag = conditional_t<has_size<T>::value, has_fast_size, no_fast_size>;

template<typename T>
size_t get_size_impl(const T& container, has_fast_size) {
    cout << "  Using fast size() method\n";
    return container.size();
}

template<typename T>
size_t get_size_impl(const T& container, no_fast_size) {
    cout << "  Counting with distance()\n";
    return distance(container.begin(), container.end());
}

template<typename T>
size_t get_size_dispatch(const T& container) {
    return get_size_impl(container, size_tag<T>{});
}

void tagDispatching() {
    printSection("8. TAG DISPATCHING");

    cout << "\nTag dispatching with SFINAE:\n";

    vector<int> v = {1, 2, 3, 4, 5};
    cout << "  Vector size: " << get_size_dispatch(v) << "\n";

    cout << "\nTag dispatch advantages:\n";
    cout << "  - Cleaner than multiple SFINAE overloads\n";
    cout << "  - Better compile-time performance\n";
    cout << "  - Used extensively in STL algorithms\n";
    cout << "  - Example: iterator category tags\n";
}

// SFINAE vs Concepts
// SFINAE version
template<typename T>
enable_if_t<is_integral<T>::value, T>
double_value_sfinae(T value) {
    return value * 2;
}

// C++20 Concepts version (requires C++20)
#if __cplusplus >= 202002L
template<typename T>
requires integral<T>
T double_value_concepts(T value) {
    return value * 2;
}
#endif

void sfinaeVsConcepts() {
    printSection("9. SFINAE vs CONCEPTS");

    cout << "\nSFINAE approach:\n";
    cout << "  template<typename T>\n";
    cout << "  enable_if_t<is_integral<T>::value, T>\n";
    cout << "  double_value(T value);\n";
    cout << "\n  double_value(5) = " << double_value_sfinae(5) << "\n";

    cout << "\nConcepts approach (C++20):\n";
    cout << "  template<typename T>\n";
    cout << "  requires integral<T>\n";
    cout << "  T double_value(T value);\n";

    cout << "\nSFINAE:\n";
    cout << "  + Works in C++11/14/17\n";
    cout << "  - Complex syntax\n";
    cout << "  - Poor error messages\n";
    cout << "  - Harder to read\n";

    cout << "\nConcepts:\n";
    cout << "  + Clear, readable syntax\n";
    cout << "  + Better error messages\n";
    cout << "  + Faster compilation\n";
    cout << "  - Requires C++20\n";
}

// Practical application: Generic print function
template<typename T>
enable_if_t<has_begin_end<T>::value && !is_same<T, string>::value, void>
print_generic(const T& container) {
    cout << "  Container: ";
    for (const auto& elem : container) {
        cout << elem << " ";
    }
    cout << "\n";
}

template<typename T>
enable_if_t<!has_begin_end<T>::value || is_same<T, string>::value, void>
print_generic(const T& value) {
    cout << "  Value: " << value << "\n";
}

void practicalApplication() {
    printSection("10. PRACTICAL APPLICATION");

    cout << "\nGeneric print with SFINAE:\n";

    vector<int> v = {1, 2, 3, 4, 5};
    print_generic(v);

    vector<string> words = {"hello", "world"};
    print_generic(words);

    print_generic(42);
    print_generic(3.14);
    print_generic(string("hello"));

    cout << "\nSFINAE enables:\n";
    cout << "  - Type-safe generic code\n";
    cout << "  - Compile-time dispatch\n";
    cout << "  - Zero runtime overhead\n";
    cout << "  - Elegant API design\n";
}

int main() {
    cout << "SFINAE COMPREHENSIVE GUIDE\n";
    cout << "==========================\n";

    sfinaePrinciple();
    enableIfPatterns();
    functionOverloadingSFINAE();
    classTemplateSFINAE();
    decltypeAndDeclval();
    voidTIdiom();
    detectionIdiom();
    tagDispatching();
    sfinaeVsConcepts();
    practicalApplication();

    printSection("SUMMARY");
    cout << "\nSFINAE (Substitution Failure Is Not An Error):\n";
    cout << "- Core template metaprogramming technique\n";
    cout << "- Enables conditional compilation\n";
    cout << "- enable_if for type constraints\n";
    cout << "- void_t simplifies detection\n";
    cout << "- Detection idiom for capabilities\n";
    cout << "- Tag dispatch for cleaner code\n";
    cout << "- Foundation for C++20 concepts\n";
    cout << "- Essential for generic library design\n";
    cout << "\nSFINAE: Powerful but complex. Prefer concepts in C++20!\n";

    return 0;
}
