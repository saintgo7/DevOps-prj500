/*
 * Program 159: Type Traits
 *
 * Demonstrates:
 * - Type trait categories
 * - Primary type categories (is_integral, is_floating_point, etc.)
 * - Composite type categories (is_arithmetic, is_fundamental, etc.)
 * - Type properties (is_const, is_reference, etc.)
 * - Type relationships (is_same, is_base_of, etc.)
 * - Type transformations (remove_const, add_pointer, etc.)
 * - SFINAE helpers (enable_if, conditional, etc.)
 * - Custom type traits
 * - Practical applications
 */

#include <iostream>
#include <type_traits>
#include <string>
#include <vector>

using namespace std;

void printSection(const string& title) {
    cout << "\n" << string(60, '=') << "\n";
    cout << title << "\n";
    cout << string(60, '=') << "\n";
}

// Primary type categories
void primaryTypeCategories() {
    printSection("1. PRIMARY TYPE CATEGORIES");

    cout << "\nis_void:\n";
    cout << "  is_void<void>: " << is_void<void>::value << "\n";
    cout << "  is_void<int>: " << is_void<int>::value << "\n";

    cout << "\nis_integral:\n";
    cout << "  is_integral<int>: " << is_integral<int>::value << "\n";
    cout << "  is_integral<char>: " << is_integral<char>::value << "\n";
    cout << "  is_integral<bool>: " << is_integral<bool>::value << "\n";
    cout << "  is_integral<double>: " << is_integral<double>::value << "\n";

    cout << "\nis_floating_point:\n";
    cout << "  is_floating_point<float>: " << is_floating_point<float>::value << "\n";
    cout << "  is_floating_point<double>: " << is_floating_point<double>::value << "\n";
    cout << "  is_floating_point<int>: " << is_floating_point<int>::value << "\n";

    cout << "\nis_array:\n";
    cout << "  is_array<int[]>: " << is_array<int[]>::value << "\n";
    cout << "  is_array<int[10]>: " << is_array<int[10]>::value << "\n";
    cout << "  is_array<vector<int>>: " << is_array<vector<int>>::value << "\n";

    cout << "\nis_pointer:\n";
    cout << "  is_pointer<int*>: " << is_pointer<int*>::value << "\n";
    cout << "  is_pointer<int**>: " << is_pointer<int**>::value << "\n";
    cout << "  is_pointer<int>: " << is_pointer<int>::value << "\n";

    cout << "\nis_reference:\n";
    cout << "  is_reference<int&>: " << is_reference<int&>::value << "\n";
    cout << "  is_reference<int&&>: " << is_reference<int&&>::value << "\n";
    cout << "  is_reference<int>: " << is_reference<int>::value << "\n";

    cout << "\nis_class:\n";
    cout << "  is_class<string>: " << is_class<string>::value << "\n";
    cout << "  is_class<int>: " << is_class<int>::value << "\n";

    cout << "\nis_function:\n";
    cout << "  is_function<int(int)>: " << is_function<int(int)>::value << "\n";
    cout << "  is_function<int>: " << is_function<int>::value << "\n";
}

// Composite type categories
void compositeTypeCategories() {
    printSection("2. COMPOSITE TYPE CATEGORIES");

    cout << "\nis_arithmetic (integral || floating_point):\n";
    cout << "  is_arithmetic<int>: " << is_arithmetic<int>::value << "\n";
    cout << "  is_arithmetic<double>: " << is_arithmetic<double>::value << "\n";
    cout << "  is_arithmetic<string>: " << is_arithmetic<string>::value << "\n";

    cout << "\nis_fundamental:\n";
    cout << "  is_fundamental<int>: " << is_fundamental<int>::value << "\n";
    cout << "  is_fundamental<void>: " << is_fundamental<void>::value << "\n";
    cout << "  is_fundamental<string>: " << is_fundamental<string>::value << "\n";

    cout << "\nis_compound:\n";
    cout << "  is_compound<int*>: " << is_compound<int*>::value << "\n";
    cout << "  is_compound<string>: " << is_compound<string>::value << "\n";
    cout << "  is_compound<int>: " << is_compound<int>::value << "\n";

    cout << "\nis_object:\n";
    cout << "  is_object<int>: " << is_object<int>::value << "\n";
    cout << "  is_object<int&>: " << is_object<int&>::value << "\n";
    cout << "  is_object<void>: " << is_object<void>::value << "\n";

    cout << "\nis_scalar:\n";
    cout << "  is_scalar<int>: " << is_scalar<int>::value << "\n";
    cout << "  is_scalar<int*>: " << is_scalar<int*>::value << "\n";
    cout << "  is_scalar<string>: " << is_scalar<string>::value << "\n";
}

// Type properties
void typeProperties() {
    printSection("3. TYPE PROPERTIES");

    cout << "\nis_const:\n";
    cout << "  is_const<const int>: " << is_const<const int>::value << "\n";
    cout << "  is_const<int>: " << is_const<int>::value << "\n";
    cout << "  is_const<const int*>: " << is_const<const int*>::value << "\n";
    cout << "  is_const<int* const>: " << is_const<int* const>::value << "\n";

    cout << "\nis_volatile:\n";
    cout << "  is_volatile<volatile int>: " << is_volatile<volatile int>::value << "\n";
    cout << "  is_volatile<int>: " << is_volatile<int>::value << "\n";

    cout << "\nis_signed/is_unsigned:\n";
    cout << "  is_signed<int>: " << is_signed<int>::value << "\n";
    cout << "  is_unsigned<unsigned int>: " << is_unsigned<unsigned int>::value << "\n";
    cout << "  is_signed<unsigned int>: " << is_signed<unsigned int>::value << "\n";

    cout << "\nis_lvalue_reference/is_rvalue_reference:\n";
    cout << "  is_lvalue_reference<int&>: " << is_lvalue_reference<int&>::value << "\n";
    cout << "  is_rvalue_reference<int&&>: " << is_rvalue_reference<int&&>::value << "\n";
    cout << "  is_lvalue_reference<int>: " << is_lvalue_reference<int>::value << "\n";
}

// Type relationships
void typeRelationships() {
    printSection("4. TYPE RELATIONSHIPS");

    cout << "\nis_same:\n";
    cout << "  is_same<int, int>: " << is_same<int, int>::value << "\n";
    cout << "  is_same<int, long>: " << is_same<int, long>::value << "\n";
    cout << "  is_same<int, const int>: " << is_same<int, const int>::value << "\n";

    struct Base {};
    struct Derived : Base {};
    struct Other {};

    cout << "\nis_base_of:\n";
    cout << "  is_base_of<Base, Derived>: " << is_base_of<Base, Derived>::value << "\n";
    cout << "  is_base_of<Derived, Base>: " << is_base_of<Derived, Base>::value << "\n";
    cout << "  is_base_of<Base, Other>: " << is_base_of<Base, Other>::value << "\n";

    cout << "\nis_convertible:\n";
    cout << "  is_convertible<int, double>: " << is_convertible<int, double>::value << "\n";
    cout << "  is_convertible<Derived*, Base*>: " << is_convertible<Derived*, Base*>::value << "\n";
    cout << "  is_convertible<Base*, Derived*>: " << is_convertible<Base*, Derived*>::value << "\n";
}

// Type transformations - removing qualifiers
void typeTransformationsRemove() {
    printSection("5. TYPE TRANSFORMATIONS - REMOVING");

    cout << "\nremove_const:\n";
    cout << "  remove_const<const int> = int: "
         << is_same<remove_const<const int>::type, int>::value << "\n";

    cout << "\nremove_volatile:\n";
    cout << "  remove_volatile<volatile int> = int: "
         << is_same<remove_volatile<volatile int>::type, int>::value << "\n";

    cout << "\nremove_cv (const and volatile):\n";
    cout << "  remove_cv<const volatile int> = int: "
         << is_same<remove_cv<const volatile int>::type, int>::value << "\n";

    cout << "\nremove_reference:\n";
    cout << "  remove_reference<int&> = int: "
         << is_same<remove_reference<int&>::type, int>::value << "\n";
    cout << "  remove_reference<int&&> = int: "
         << is_same<remove_reference<int&&>::type, int>::value << "\n";

    cout << "\nremove_pointer:\n";
    cout << "  remove_pointer<int*> = int: "
         << is_same<remove_pointer<int*>::type, int>::value << "\n";
    cout << "  remove_pointer<int**> = int*: "
         << is_same<remove_pointer<int**>::type, int*>::value << "\n";

    cout << "\nremove_extent (array):\n";
    cout << "  remove_extent<int[10]> = int: "
         << is_same<remove_extent<int[10]>::type, int>::value << "\n";
    cout << "  remove_extent<int[10][20]> = int[20]: "
         << is_same<remove_extent<int[10][20]>::type, int[20]>::value << "\n";
}

// Type transformations - adding qualifiers
void typeTransformationsAdd() {
    printSection("6. TYPE TRANSFORMATIONS - ADDING");

    cout << "\nadd_const:\n";
    cout << "  add_const<int> = const int: "
         << is_same<add_const<int>::type, const int>::value << "\n";

    cout << "\nadd_volatile:\n";
    cout << "  add_volatile<int> = volatile int: "
         << is_same<add_volatile<int>::type, volatile int>::value << "\n";

    cout << "\nadd_cv:\n";
    cout << "  add_cv<int> = const volatile int: "
         << is_same<add_cv<int>::type, const volatile int>::value << "\n";

    cout << "\nadd_lvalue_reference:\n";
    cout << "  add_lvalue_reference<int> = int&: "
         << is_same<add_lvalue_reference<int>::type, int&>::value << "\n";

    cout << "\nadd_rvalue_reference:\n";
    cout << "  add_rvalue_reference<int> = int&&: "
         << is_same<add_rvalue_reference<int>::type, int&&>::value << "\n";

    cout << "\nadd_pointer:\n";
    cout << "  add_pointer<int> = int*: "
         << is_same<add_pointer<int>::type, int*>::value << "\n";
    cout << "  add_pointer<int*> = int**: "
         << is_same<add_pointer<int*>::type, int**>::value << "\n";
}

// enable_if and conditional
void enableIfConditional() {
    printSection("7. ENABLE_IF AND CONDITIONAL");

    cout << "\nenable_if (SFINAE helper):\n";
    cout << "  Used for conditional template instantiation\n";

    // Example with enable_if
    auto print_int = []<typename T>
        (T value, typename enable_if<is_integral<T>::value>::type* = nullptr) {
        cout << "    Integer: " << value << "\n";
    };

    auto print_float = []<typename T>
        (T value, typename enable_if<is_floating_point<T>::value>::type* = nullptr) {
        cout << "    Floating-point: " << value << "\n";
    };

    print_int(42);
    print_float(3.14);

    cout << "\nconditional:\n";
    using Type1 = conditional<true, int, double>::type;
    using Type2 = conditional<false, int, double>::type;

    cout << "  conditional<true, int, double> = int: "
         << is_same<Type1, int>::value << "\n";
    cout << "  conditional<false, int, double> = double: "
         << is_same<Type2, double>::value << "\n";
}

// decay
void typeDecay() {
    printSection("8. DECAY");

    cout << "\ndecay (mimics pass-by-value):\n";
    cout << "  decay<int&> = int: "
         << is_same<decay<int&>::type, int>::value << "\n";
    cout << "  decay<const int&> = int: "
         << is_same<decay<const int&>::type, int>::value << "\n";
    cout << "  decay<int[10]> = int*: "
         << is_same<decay<int[10]>::type, int*>::value << "\n";
    cout << "  decay<int(int)> = int(*)(int): "
         << is_same<decay<int(int)>::type, int(*)(int)>::value << "\n";

    cout << "\nDecay removes:\n";
    cout << "  - References\n";
    cout << "  - cv-qualifiers\n";
    cout << "  - Converts arrays to pointers\n";
    cout << "  - Converts functions to function pointers\n";
}

// Custom type traits
template<typename T>
struct is_string : false_type {};

template<>
struct is_string<string> : true_type {};

template<>
struct is_string<const char*> : true_type {};

template<typename T>
struct is_container {
private:
    template<typename U>
    static auto test(int) -> decltype(
        declval<U>().begin(),
        declval<U>().end(),
        true_type{}
    );

    template<typename>
    static false_type test(...);

public:
    static constexpr bool value = decltype(test<T>(0))::value;
};

void customTypeTraits() {
    printSection("9. CUSTOM TYPE TRAITS");

    cout << "\nCustom is_string trait:\n";
    cout << "  is_string<string>: " << is_string<string>::value << "\n";
    cout << "  is_string<const char*>: " << is_string<const char*>::value << "\n";
    cout << "  is_string<int>: " << is_string<int>::value << "\n";

    cout << "\nCustom is_container trait:\n";
    cout << "  is_container<vector<int>>: " << is_container<vector<int>>::value << "\n";
    cout << "  is_container<string>: " << is_container<string>::value << "\n";
    cout << "  is_container<int>: " << is_container<int>::value << "\n";
}

// Practical application: Type-safe function overloading
template<typename T>
enable_if_t<is_integral<T>::value, void>
print_value(T value) {
    cout << "  Integer: " << value << "\n";
}

template<typename T>
enable_if_t<is_floating_point<T>::value, void>
print_value(T value) {
    cout << "  Floating-point: " << value << "\n";
}

template<typename T>
enable_if_t<!is_arithmetic<T>::value, void>
print_value(T value) {
    cout << "  Other: " << value << "\n";
}

template<typename T>
auto safe_divide(T a, T b) -> enable_if_t<is_arithmetic<T>::value, T> {
    if constexpr (is_integral<T>::value) {
        return b != 0 ? a / b : 0;
    } else {
        return b != 0.0 ? a / b : 0.0;
    }
}

void practicalApplication() {
    printSection("10. PRACTICAL APPLICATION");

    cout << "\nType-safe function overloading:\n";
    print_value(42);
    print_value(3.14);
    print_value(string("hello"));

    cout << "\nType-safe division:\n";
    cout << "  safe_divide(10, 3) = " << safe_divide(10, 3) << "\n";
    cout << "  safe_divide(10, 0) = " << safe_divide(10, 0) << "\n";
    cout << "  safe_divide(10.0, 3.0) = " << safe_divide(10.0, 3.0) << "\n";

    cout << "\nCompile-time dispatch:\n";
    cout << "  - Zero runtime overhead\n";
    cout << "  - Type-safe\n";
    cout << "  - Clear error messages\n";
}

int main() {
    cout << "TYPE TRAITS COMPREHENSIVE GUIDE\n";
    cout << "===============================\n";

    primaryTypeCategories();
    compositeTypeCategories();
    typeProperties();
    typeRelationships();
    typeTransformationsRemove();
    typeTransformationsAdd();
    enableIfConditional();
    typeDecay();
    customTypeTraits();
    practicalApplication();

    printSection("SUMMARY");
    cout << "\nType traits:\n";
    cout << "- Compile-time type information\n";
    cout << "- Query type properties\n";
    cout << "- Transform types\n";
    cout << "- Enable SFINAE\n";
    cout << "- Foundation for generic programming\n";
    cout << "- Zero runtime overhead\n";
    cout << "- Used extensively in C++20 concepts\n";
    cout << "\nType traits enable powerful metaprogramming!\n";

    return 0;
}
