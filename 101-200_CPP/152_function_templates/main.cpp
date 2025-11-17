/*
 * Program 152: Function Templates
 *
 * Demonstrates:
 * - Function template syntax and usage
 * - Template argument deduction
 * - Explicit template arguments
 * - Function template overloading
 * - Template argument forwarding
 * - Perfect forwarding
 * - Function template specialization
 * - Auto return type deduction
 * - Variadic function templates (preview)
 */

#include <iostream>
#include <string>
#include <vector>
#include <type_traits>
#include <utility>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Basic function templates
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

template<typename T>
T minimum(T a, T b) {
    return (a < b) ? a : b;
}

template<typename T>
void swap_values(T& a, T& b) {
    T temp = a;
    a = b;
    b = temp;
}

void basicFunctionTemplates() {
    printSection("1. BASIC FUNCTION TEMPLATES");

    cout << "\nSimple function templates:\n";
    cout << "  maximum(10, 20) = " << maximum(10, 20) << "\n";
    cout << "  maximum(3.5, 2.1) = " << maximum(3.5, 2.1) << "\n";
    cout << "  maximum('a', 'z') = " << maximum('a', 'z') << "\n";

    cout << "\nminimum function:\n";
    cout << "  minimum(10, 20) = " << minimum(10, 20) << "\n";
    cout << "  minimum(3.5, 2.1) = " << minimum(3.5, 2.1) << "\n";

    cout << "\nswap_values:\n";
    int x = 10, y = 20;
    cout << "  Before: x = " << x << ", y = " << y << "\n";
    swap_values(x, y);
    cout << "  After: x = " << x << ", y = " << y << "\n";

    string s1 = "hello", s2 = "world";
    cout << "  Before: s1 = " << s1 << ", s2 = " << s2 << "\n";
    swap_values(s1, s2);
    cout << "  After: s1 = " << s1 << ", s2 = " << s2 << "\n";
}

// Multiple template parameters
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

template<typename T, typename U, typename V>
auto sum3(T a, U b, V c) -> decltype(a + b + c) {
    return a + b + c;
}

template<typename T, typename U>
pair<T, U> make_ordered_pair(T first, U second) {
    return pair<T, U>(first, second);
}

void multipleTypeParameters() {
    printSection("2. MULTIPLE TYPE PARAMETERS");

    cout << "\nTwo type parameters:\n";
    cout << "  add(10, 3.5) = " << add(10, 3.5) << "\n";
    cout << "  add(3.5, 10) = " << add(3.5, 10) << "\n";
    cout << "  add(string(\"Hello \"), string(\"World\")) = "
         << add(string("Hello "), string("World")) << "\n";

    cout << "\nThree type parameters:\n";
    cout << "  sum3(1, 2.5, 3) = " << sum3(1, 2.5, 3) << "\n";

    cout << "\nReturning pairs:\n";
    auto p1 = make_ordered_pair(10, 3.14);
    cout << "  Pair<int, double>: (" << p1.first << ", " << p1.second << ")\n";

    auto p2 = make_ordered_pair(string("name"), 42);
    cout << "  Pair<string, int>: (" << p2.first << ", " << p2.second << ")\n";
}

// Template argument deduction
template<typename T>
void printType(const T& value) {
    cout << "  Value: " << value << ", Type: " << typeid(T).name() << "\n";
}

template<typename T>
void printTypeInfo(T value) {
    cout << "  Type: " << typeid(T).name()
         << ", Size: " << sizeof(T) << " bytes\n";
}

void templateArgumentDeduction() {
    printSection("3. TEMPLATE ARGUMENT DEDUCTION");

    cout << "\nAutomatic deduction:\n";
    printType(42);
    printType(3.14);
    printType("Hello");
    printType(string("World"));

    cout << "\nDeduction with references:\n";
    int x = 10;
    const int y = 20;
    printType(x);   // T = int
    printType(y);   // T = int (const removed)

    int& ref = x;
    printType(ref);  // T = int (reference removed)

    cout << "\nExplicit template arguments:\n";
    printType<int>(42);
    printType<double>(3.14);
    printType<const char*>("Hello");

    cout << "\nForcing specific types:\n";
    printTypeInfo(42);          // int
    printTypeInfo<long>(42);    // long
    printTypeInfo<double>(42);  // double
}

// Function template overloading
template<typename T>
void print(T value) {
    cout << "  Generic: " << value << "\n";
}

template<typename T>
void print(T* ptr) {
    cout << "  Pointer: " << (ptr ? "valid" : "null") << "\n";
}

void print(int value) {
    cout << "  Specialized int: " << value << "\n";
}

void print(const char* str) {
    cout << "  C-string: " << str << "\n";
}

template<typename T, typename U>
void print(T first, U second) {
    cout << "  Pair: (" << first << ", " << second << ")\n";
}

void functionTemplateOverloading() {
    printSection("4. FUNCTION TEMPLATE OVERLOADING");

    cout << "\nOverload resolution:\n";
    print(3.14);           // Generic template
    print(42);             // Non-template int (exact match preferred)
    print("Hello");        // Non-template const char*

    int x = 10;
    int* ptr = &x;
    print(ptr);            // Pointer template

    print(10, 3.14);       // Two-parameter template
    print("name", 42);     // Two-parameter template

    cout << "\nOverload priority:\n";
    cout << "  1. Non-template functions (exact match)\n";
    cout << "  2. Template specializations\n";
    cout << "  3. Generic templates\n";
}

// Template specialization
template<typename T>
T absolute(T value) {
    return value < 0 ? -value : value;
}

template<>
string absolute<string>(string value) {
    return "String has no absolute value: " + value;
}

template<typename T>
string toString(T value) {
    return to_string(value);
}

template<>
string toString<bool>(bool value) {
    return value ? "true" : "false";
}

template<>
string toString<string>(string value) {
    return value;
}

void functionTemplateSpecialization() {
    printSection("5. FUNCTION TEMPLATE SPECIALIZATION");

    cout << "\nGeneric absolute:\n";
    cout << "  absolute(-10) = " << absolute(-10) << "\n";
    cout << "  absolute(-3.5) = " << absolute(-3.5) << "\n";

    cout << "\nSpecialized for string:\n";
    cout << "  absolute(\"hello\") = " << absolute(string("hello")) << "\n";

    cout << "\nGeneric toString:\n";
    cout << "  toString(42) = " << toString(42) << "\n";
    cout << "  toString(3.14) = " << toString(3.14) << "\n";

    cout << "\nSpecialized toString:\n";
    cout << "  toString(true) = " << toString(true) << "\n";
    cout << "  toString(false) = " << toString(false) << "\n";
    cout << "  toString(string(\"hello\")) = " << toString(string("hello")) << "\n";
}

// Perfect forwarding
template<typename T>
void wrapper_by_value(T arg) {
    cout << "  Received by value: " << arg << "\n";
}

template<typename T>
void wrapper_by_ref(T& arg) {
    cout << "  Received by reference: " << arg << "\n";
    arg += 10;
}

template<typename T>
void wrapper_perfect(T&& arg) {
    cout << "  Perfect forwarding: " << arg << "\n";
    // Forward to another function preserving value category
}

template<typename Func, typename... Args>
auto call_function(Func&& func, Args&&... args) -> decltype(func(forward<Args>(args)...)) {
    cout << "  Calling function...\n";
    return func(forward<Args>(args)...);
}

void perfectForwarding() {
    printSection("6. PERFECT FORWARDING");

    cout << "\nForwarding examples:\n";
    int x = 10;

    wrapper_by_value(x);
    cout << "  x after by_value: " << x << "\n";

    wrapper_by_ref(x);
    cout << "  x after by_ref: " << x << "\n";

    cout << "\nPerfect forwarding with call_function:\n";
    auto sum = [](int a, int b) { return a + b; };

    int result = call_function(sum, 10, 20);
    cout << "  Result: " << result << "\n";

    auto print_msg = [](const string& msg) {
        cout << "  Message: " << msg << "\n";
    };
    call_function(print_msg, "Hello, World!");
}

// Auto return type deduction
template<typename T, typename U>
auto multiply(T a, U b) {
    return a * b;
}

template<typename Container>
auto getFirst(const Container& c) -> decltype(c.front()) {
    return c.front();
}

template<typename Container>
auto getLast(Container& c) {
    return c.back();
}

void autoReturnType() {
    printSection("7. AUTO RETURN TYPE DEDUCTION");

    cout << "\nAuto return type:\n";
    cout << "  multiply(10, 3.5) = " << multiply(10, 3.5) << "\n";
    cout << "  multiply(2.5, 4.0) = " << multiply(2.5, 4.0) << "\n";

    cout << "\nAuto with containers:\n";
    vector<int> v = {1, 2, 3, 4, 5};
    cout << "  getFirst(vector) = " << getFirst(v) << "\n";
    cout << "  getLast(vector) = " << getLast(v) << "\n";

    vector<string> words = {"hello", "world", "foo"};
    cout << "  getFirst(strings) = " << getFirst(words) << "\n";
    cout << "  getLast(strings) = " << getLast(words) << "\n";
}

// Constexpr function templates
template<typename T>
constexpr T square(T value) {
    return value * value;
}

template<typename T>
constexpr T cube(T value) {
    return value * value * value;
}

template<int N>
constexpr int fibonacci() {
    if constexpr (N <= 1) {
        return N;
    } else {
        return fibonacci<N-1>() + fibonacci<N-2>();
    }
}

void constexprTemplates() {
    printSection("8. CONSTEXPR FUNCTION TEMPLATES");

    cout << "\nConstexpr templates:\n";
    constexpr int sq5 = square(5);
    cout << "  constexpr square(5) = " << sq5 << "\n";

    constexpr double sq3_14 = square(3.14);
    cout << "  constexpr square(3.14) = " << sq3_14 << "\n";

    cout << "\nUsing in array sizes:\n";
    int arr1[square(3)];  // Array of size 9
    cout << "  Array size: " << sizeof(arr1) / sizeof(int) << "\n";

    cout << "\nConstexpr fibonacci:\n";
    constexpr int fib10 = fibonacci<10>();
    cout << "  fibonacci<10>() = " << fib10 << "\n";
}

// Template with constraints (preview)
template<typename T>
typename enable_if<is_integral<T>::value, T>::type
safe_divide(T a, T b) {
    if (b == 0) {
        cout << "  Division by zero!\n";
        return 0;
    }
    return a / b;
}

template<typename T>
void print_if_numeric(T value) {
    if constexpr (is_arithmetic<T>::value) {
        cout << "  Numeric value: " << value << "\n";
    } else {
        cout << "  Non-numeric type\n";
    }
}

void templateConstraints() {
    printSection("9. TEMPLATE CONSTRAINTS (PREVIEW)");

    cout << "\nSFINAE with enable_if:\n";
    cout << "  safe_divide(10, 2) = " << safe_divide(10, 2) << "\n";
    cout << "  safe_divide(10, 0) = " << safe_divide(10, 0) << "\n";

    cout << "\nif constexpr for compile-time branching:\n";
    print_if_numeric(42);
    print_if_numeric(3.14);
    print_if_numeric("Hello");
}

// Variadic templates preview
template<typename T>
T sum(T value) {
    return value;
}

template<typename T, typename... Args>
T sum(T first, Args... args) {
    return first + sum(args...);
}

template<typename... Args>
void print_all(Args... args) {
    cout << "  ";
    ((cout << args << " "), ...);  // C++17 fold expression
    cout << "\n";
}

void variadicTemplatesPreview() {
    printSection("10. VARIADIC TEMPLATES (PREVIEW)");

    cout << "\nVariadic sum:\n";
    cout << "  sum(1) = " << sum(1) << "\n";
    cout << "  sum(1, 2, 3) = " << sum(1, 2, 3) << "\n";
    cout << "  sum(1, 2, 3, 4, 5) = " << sum(1, 2, 3, 4, 5) << "\n";

    cout << "\nVariadic print:\n";
    print_all(1, 2, 3, 4, 5);
    print_all("hello", "world", "foo");
    print_all(1, "two", 3.0, "four");
}

int main() {
    cout << "FUNCTION TEMPLATES COMPREHENSIVE GUIDE\n";
    cout << "======================================\n";

    basicFunctionTemplates();
    multipleTypeParameters();
    templateArgumentDeduction();
    functionTemplateOverloading();
    functionTemplateSpecialization();
    perfectForwarding();
    autoReturnType();
    constexprTemplates();
    templateConstraints();
    variadicTemplatesPreview();

    printSection("SUMMARY");
    cout << "\nFunction template features:\n";
    cout << "- Generic functions for any type\n";
    cout << "- Automatic type deduction\n";
    cout << "- Can be overloaded and specialized\n";
    cout << "- Perfect forwarding with &&\n";
    cout << "- Auto return type deduction\n";
    cout << "- constexpr for compile-time evaluation\n";
    cout << "- Can use SFINAE for constraints\n";
    cout << "- Variadic templates for any number of arguments\n";
    cout << "\nFunction templates are the foundation of generic algorithms!\n";

    return 0;
}
