/*
 * Program 156: Template Metaprogramming
 *
 * Demonstrates:
 * - Compile-time computation
 * - Recursive templates
 * - Template metaprogramming techniques
 * - Compile-time factorial, fibonacci
 * - Type computations
 * - constexpr vs template metaprogramming
 * - Template metafunctions
 * - Type list manipulation
 * - SFINAE and enable_if
 * - Practical metaprogramming patterns
 */

#include <iostream>
#include <type_traits>
#include <string>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Compile-time factorial
template<int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};

template<>
struct Factorial<0> {
    static constexpr int value = 1;
};

// Compile-time fibonacci
template<int N>
struct Fibonacci {
    static constexpr int value = Fibonacci<N - 1>::value + Fibonacci<N - 2>::value;
};

template<>
struct Fibonacci<0> {
    static constexpr int value = 0;
};

template<>
struct Fibonacci<1> {
    static constexpr int value = 1;
};

// Compile-time power
template<int Base, int Exp>
struct Power {
    static constexpr int value = Base * Power<Base, Exp - 1>::value;
};

template<int Base>
struct Power<Base, 0> {
    static constexpr int value = 1;
};

void compileTimeComputation() {
    printSection("1. COMPILE-TIME COMPUTATION");

    cout << "\nFactorial (computed at compile time):\n";
    cout << "  Factorial<5>::value = " << Factorial<5>::value << "\n";
    cout << "  Factorial<10>::value = " << Factorial<10>::value << "\n";

    cout << "\nFibonacci:\n";
    cout << "  Fibonacci<10>::value = " << Fibonacci<10>::value << "\n";
    cout << "  Fibonacci<15>::value = " << Fibonacci<15>::value << "\n";

    cout << "\nPower:\n";
    cout << "  Power<2, 8>::value = " << Power<2, 8>::value << "\n";
    cout << "  Power<3, 4>::value = " << Power<3, 4>::value << "\n";

    cout << "\nCompile-time arrays:\n";
    int fact_array[Factorial<5>::value];  // Array of size 120
    cout << "  Array size: " << sizeof(fact_array) / sizeof(int) << "\n";
}

// Type computations
template<typename T>
struct RemovePointer {
    using type = T;
};

template<typename T>
struct RemovePointer<T*> {
    using type = T;
};

template<typename T>
struct RemoveConst {
    using type = T;
};

template<typename T>
struct RemoveConst<const T> {
    using type = T;
};

template<typename T>
struct AddPointer {
    using type = T*;
};

template<typename T>
struct AddConst {
    using type = const T;
};

void typeComputations() {
    printSection("2. TYPE COMPUTATIONS");

    cout << "\nType transformations:\n";
    cout << "  int* -> int: "
         << is_same<RemovePointer<int*>::type, int>::value << "\n";
    cout << "  int** -> int*: "
         << is_same<RemovePointer<int**>::type, int*>::value << "\n";

    cout << "\nConst removal:\n";
    cout << "  const int -> int: "
         << is_same<RemoveConst<const int>::type, int>::value << "\n";

    cout << "\nAdding qualifiers:\n";
    cout << "  int -> int*: "
         << is_same<AddPointer<int>::type, int*>::value << "\n";
    cout << "  int -> const int: "
         << is_same<AddConst<int>::type, const int>::value << "\n";
}

// Conditional types
template<bool Condition, typename TrueType, typename FalseType>
struct Conditional {
    using type = TrueType;
};

template<typename TrueType, typename FalseType>
struct Conditional<false, TrueType, FalseType> {
    using type = FalseType;
};

// Select larger type
template<typename T, typename U>
struct LargerType {
    using type = typename Conditional<(sizeof(T) > sizeof(U)), T, U>::type;
};

void conditionalTypes() {
    printSection("3. CONDITIONAL TYPES");

    cout << "\nConditional type selection:\n";
    using Type1 = Conditional<true, int, double>::type;
    using Type2 = Conditional<false, int, double>::type;

    cout << "  Conditional<true, int, double>: "
         << is_same<Type1, int>::value << " (is int)\n";
    cout << "  Conditional<false, int, double>: "
         << is_same<Type2, double>::value << " (is double)\n";

    cout << "\nLarger type selection:\n";
    using Larger1 = LargerType<int, long>::type;
    using Larger2 = LargerType<char, int>::type;

    cout << "  LargerType<int, long>: sizeof = " << sizeof(Larger1) << "\n";
    cout << "  LargerType<char, int>: sizeof = " << sizeof(Larger2) << "\n";
}

// Type list
template<typename... Types>
struct TypeList {};

// Get size of type list
template<typename List>
struct TypeListSize;

template<typename... Types>
struct TypeListSize<TypeList<Types...>> {
    static constexpr size_t value = sizeof...(Types);
};

// Get first type
template<typename List>
struct TypeListFront;

template<typename Head, typename... Tail>
struct TypeListFront<TypeList<Head, Tail...>> {
    using type = Head;
};

// Append type
template<typename List, typename T>
struct TypeListAppend;

template<typename... Types, typename T>
struct TypeListAppend<TypeList<Types...>, T> {
    using type = TypeList<Types..., T>;
};

void typeList() {
    printSection("4. TYPE LIST MANIPULATION");

    cout << "\nTypeList operations:\n";

    using List1 = TypeList<int, double, string>;
    cout << "  List size: " << TypeListSize<List1>::value << "\n";

    using Front = TypeListFront<List1>::type;
    cout << "  Front type is int: " << is_same<Front, int>::value << "\n";

    using List2 = TypeListAppend<List1, bool>::type;
    cout << "  After append bool, size: " << TypeListSize<List2>::value << "\n";
}

// constexpr vs template metaprogramming
constexpr int factorial_constexpr(int n) {
    return n <= 1 ? 1 : n * factorial_constexpr(n - 1);
}

void constexprVsTemplate() {
    printSection("5. CONSTEXPR vs TEMPLATE METAPROGRAMMING");

    cout << "\nTemplate metaprogramming:\n";
    cout << "  Factorial<5>::value = " << Factorial<5>::value << "\n";
    cout << "  - Computed at compile time\n";
    cout << "  - Only works with constants\n";
    cout << "  - Uses recursive type instantiation\n";

    cout << "\nconstexpr functions:\n";
    constexpr int fact5 = factorial_constexpr(5);
    cout << "  factorial_constexpr(5) = " << fact5 << "\n";
    cout << "  - Can be compile-time or runtime\n";
    cout << "  - Works with variables\n";
    cout << "  - More readable syntax\n";

    int n = 5;
    int runtime_fact = factorial_constexpr(n);
    cout << "  Runtime: factorial_constexpr(" << n << ") = " << runtime_fact << "\n";

    cout << "\nPrefer constexpr in modern C++ (C++11+)\n";
}

// SFINAE and enable_if
template<typename T>
typename enable_if<is_integral<T>::value, T>::type
safe_divide(T a, T b) {
    return b != 0 ? a / b : 0;
}

template<typename T>
typename enable_if<is_floating_point<T>::value, T>::type
safe_divide(T a, T b) {
    return b != 0.0 ? a / b : 0.0;
}

// is_same_template
template<typename T, typename U>
struct is_same_template : false_type {};

template<typename T>
struct is_same_template<T, T> : true_type {};

void sfinaeAndEnableIf() {
    printSection("6. SFINAE AND ENABLE_IF");

    cout << "\nSFINAE (Substitution Failure Is Not An Error):\n";
    cout << "  Allows function overloading based on type traits\n";

    cout << "\nType-safe division:\n";
    cout << "  safe_divide(10, 2) = " << safe_divide(10, 2) << "\n";
    cout << "  safe_divide(10, 0) = " << safe_divide(10, 0) << "\n";
    cout << "  safe_divide(10.0, 2.5) = " << safe_divide(10.0, 2.5) << "\n";

    cout << "\nCustom type traits:\n";
    cout << "  is_same_template<int, int>: "
         << is_same_template<int, int>::value << "\n";
    cout << "  is_same_template<int, double>: "
         << is_same_template<int, double>::value << "\n";
}

// Compile-time string length
template<size_t N>
constexpr size_t string_length(const char (&)[N]) {
    return N - 1;  // Exclude null terminator
}

// Compile-time is_prime
template<int N, int Divisor = N - 1>
struct IsPrime {
    static constexpr bool value =
        (N % Divisor != 0) && IsPrime<N, Divisor - 1>::value;
};

template<int N>
struct IsPrime<N, 1> {
    static constexpr bool value = true;
};

template<>
struct IsPrime<1, 0> {
    static constexpr bool value = false;
};

void compileTimeAlgorithms() {
    printSection("7. COMPILE-TIME ALGORITHMS");

    cout << "\nString length at compile time:\n";
    constexpr size_t len1 = string_length("hello");
    constexpr size_t len2 = string_length("world!");
    cout << "  \"hello\": " << len1 << "\n";
    cout << "  \"world!\": " << len2 << "\n";

    cout << "\nPrime checking at compile time:\n";
    cout << "  IsPrime<2>::value = " << IsPrime<2>::value << "\n";
    cout << "  IsPrime<17>::value = " << IsPrime<17>::value << "\n";
    cout << "  IsPrime<18>::value = " << IsPrime<18>::value << "\n";
    cout << "  IsPrime<97>::value = " << IsPrime<97>::value << "\n";
}

// Template metafunction
template<typename T>
struct TypeInfo {
    static void print() {
        cout << "  Size: " << sizeof(T) << " bytes\n";
        cout << "  Is integral: " << is_integral<T>::value << "\n";
        cout << "  Is floating point: " << is_floating_point<T>::value << "\n";
        cout << "  Is pointer: " << is_pointer<T>::value << "\n";
        cout << "  Is const: " << is_const<T>::value << "\n";
    }
};

void templateMetafunctions() {
    printSection("8. TEMPLATE METAFUNCTIONS");

    cout << "\nTypeInfo<int>:\n";
    TypeInfo<int>::print();

    cout << "\nTypeInfo<double>:\n";
    TypeInfo<double>::print();

    cout << "\nTypeInfo<const int*>:\n";
    TypeInfo<const int*>::print();
}

// Static assertions
template<typename T>
struct OnlyIntegers {
    static_assert(is_integral<T>::value, "T must be an integral type");

    T value;

    OnlyIntegers(T v) : value(v) {}

    void print() {
        cout << "  Value: " << value << "\n";
    }
};

void staticAssertions() {
    printSection("9. STATIC ASSERTIONS");

    cout << "\nStatic assertions for compile-time checks:\n";

    OnlyIntegers<int> oi(42);
    oi.print();

    OnlyIntegers<long> ol(100L);
    ol.print();

    // This would cause compile error:
    // OnlyIntegers<double> od(3.14);

    cout << "\nstatic_assert ensures type safety at compile time\n";
}

// Practical example: Compile-time unit conversion
template<int Numerator, int Denominator>
struct Ratio {
    static constexpr int num = Numerator;
    static constexpr int den = Denominator;
};

template<typename FromRatio, typename ToRatio, int Value>
struct Convert {
    static constexpr int value =
        Value * FromRatio::num * ToRatio::den / (FromRatio::den * ToRatio::num);
};

using Inches = Ratio<1, 1>;
using Feet = Ratio<12, 1>;
using Yards = Ratio<36, 1>;

void practicalExample() {
    printSection("10. PRACTICAL EXAMPLE: UNIT CONVERSION");

    cout << "\nCompile-time unit conversion:\n";

    constexpr int feet_to_inches = Convert<Feet, Inches, 5>::value;
    cout << "  5 feet = " << feet_to_inches << " inches\n";

    constexpr int yards_to_inches = Convert<Yards, Inches, 2>::value;
    cout << "  2 yards = " << yards_to_inches << " inches\n";

    constexpr int inches_to_feet = Convert<Inches, Feet, 24>::value;
    cout << "  24 inches = " << inches_to_feet << " feet\n";

    cout << "\nAdvantages:\n";
    cout << "  - Zero runtime overhead\n";
    cout << "  - Compile-time error checking\n";
    cout << "  - Type-safe conversions\n";
}

int main() {
    cout << "TEMPLATE METAPROGRAMMING COMPREHENSIVE GUIDE\n";
    cout << "============================================\n";

    compileTimeComputation();
    typeComputations();
    conditionalTypes();
    typeList();
    constexprVsTemplate();
    sfinaeAndEnableIf();
    compileTimeAlgorithms();
    templateMetafunctions();
    staticAssertions();
    practicalExample();

    printSection("SUMMARY");
    cout << "\nTemplate metaprogramming:\n";
    cout << "- Computation at compile time\n";
    cout << "- Uses recursive template instantiation\n";
    cout << "- Type-level programming\n";
    cout << "- Zero runtime overhead\n";
    cout << "- Complex but powerful\n";
    cout << "- Prefer constexpr in modern C++\n";
    cout << "- Enables static_assert for compile-time checks\n";
    cout << "- Foundation for advanced generic programming\n";
    cout << "\nTemplate metaprogramming pushes C++ to its limits!\n";

    return 0;
}
