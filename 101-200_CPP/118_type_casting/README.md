# Program 118: Type Casting in C++

## Description
Comprehensive exploration of type casting in C++ covering C-style casts, static_cast, dynamic_cast, const_cast, reinterpret_cast, and casting best practices. This program demonstrates safe and appropriate type conversion techniques in modern C++.

## Learning Objectives
- Understand different casting operators
- Master static_cast for compile-time casts
- Use dynamic_cast for runtime type checking
- Apply const_cast appropriately
- Understand reinterpret_cast use cases
- Avoid dangerous C-style casts
- Follow casting best practices

## Features
- C-style casting (legacy)
- static_cast demonstrations
- dynamic_cast with polymorphism
- const_cast for const removal
- reinterpret_cast for low-level casts
- Implicit vs explicit conversions
- User-defined conversions
- Safe casting patterns

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/118_type_casting
g++ -std=c++20 -Wall -Wextra -o type_casting main.cpp
```

### Execution
```bash
./type_casting
```

## Key Concepts

### 1. C-Style Cast (Avoid in Modern C++)
```cpp
// C-style cast (not type-safe)
int i = 10;
double d = (double)i;           // C-style
float f = (float)d;             // C-style

void* ptr = &i;
int* iptr = (int*)ptr;          // Dangerous!

// Problems with C-style casts:
// - Not searchable in code
// - No compile-time type checking
// - Can perform dangerous conversions
// - Unclear intent
```

### 2. static_cast
```cpp
// Safe compile-time conversions
int i = 10;
double d = static_cast<double>(i);

// Numeric conversions
float f = static_cast<float>(d);
int j = static_cast<int>(f);    // Truncates

// Pointer conversions (related types)
class Base {};
class Derived : public Base {};

Derived* derived = new Derived();
Base* base = static_cast<Base*>(derived);      // Upcast (safe)
Derived* d2 = static_cast<Derived*>(base);     // Downcast (not checked!)

// Void pointer conversions
void* vptr = &i;
int* iptr = static_cast<int*>(vptr);

// Enum conversions
enum Color { RED, GREEN, BLUE };
int colorValue = static_cast<int>(RED);
Color color = static_cast<Color>(1);

// Cannot cast away const
const int ci = 10;
// int* pi = static_cast<int*>(&ci);  // Error!

delete derived;
```

### 3. dynamic_cast
```cpp
// Runtime type checking (requires polymorphic base class)
class Base {
public:
    virtual ~Base() {}
    virtual void print() { std::cout << "Base\n"; }
};

class Derived : public Base {
public:
    void print() override { std::cout << "Derived\n"; }
    void derivedMethod() { std::cout << "Derived method\n"; }
};

void useDynamicCast() {
    Base* base = new Derived();

    // Safe downcast with runtime checking
    Derived* derived = dynamic_cast<Derived*>(base);
    if (derived) {
        derived->derivedMethod();  // Safe to call
    } else {
        std::cout << "Cast failed\n";
    }

    // Reference dynamic_cast (throws on failure)
    try {
        Derived& derivedRef = dynamic_cast<Derived&>(*base);
        derivedRef.derivedMethod();
    } catch (std::bad_cast& e) {
        std::cout << "Cast failed: " << e.what() << '\n';
    }

    delete base;
}

// dynamic_cast returns nullptr for failed pointer casts
Base* base = new Base();
Derived* derived = dynamic_cast<Derived*>(base);
if (!derived) {
    std::cout << "Not a Derived object\n";
}
delete base;
```

### 4. const_cast
```cpp
// Add or remove const (use carefully!)

// Remove const
const int ci = 10;
int* pi = const_cast<int*>(&ci);
*pi = 20;  // Undefined behavior if ci was originally const!

// Safe use case: calling non-const function with const object
void legacyFunction(int* ptr) {
    std::cout << *ptr << '\n';
}

void wrapper(const int* ptr) {
    // Remove const to call legacy API (read-only operation)
    legacyFunction(const_cast<int*>(ptr));
}

// Add const (less common)
int i = 10;
const int* cpi = const_cast<const int*>(&i);

// Common pattern: const and non-const accessors
class Container {
    int data[10];
public:
    // Non-const version
    int& at(size_t index) {
        return data[index];
    }

    // Const version using const_cast
    const int& at(size_t index) const {
        return const_cast<Container*>(this)->at(index);
    }
};
```

### 5. reinterpret_cast
```cpp
// Low-level reinterpretation (dangerous!)

// Pointer to integer
int* ptr = new int(42);
uintptr_t addr = reinterpret_cast<uintptr_t>(ptr);
std::cout << "Address: " << std::hex << addr << '\n';

// Integer to pointer
int* ptr2 = reinterpret_cast<int*>(addr);
std::cout << *ptr2 << '\n';  // 42

// Unrelated pointer types
struct A { int x; };
struct B { float f; };

A a{10};
B* b = reinterpret_cast<B*>(&a);  // Very dangerous!

// Common use: type punning (undefined behavior, use carefully)
float f = 3.14f;
uint32_t bits = *reinterpret_cast<uint32_t*>(&f);

// Safe alternative for type punning
uint32_t safeBits;
std::memcpy(&safeBits, &f, sizeof(f));

delete ptr;
```

### 6. Implicit Conversions
```cpp
// Automatic type conversions

// Numeric promotions
int i = 10;
double d = i;      // Implicit conversion int to double

// Narrowing (potential data loss)
double d2 = 3.14;
int i2 = d2;       // Implicit, truncates to 3

// Prevent narrowing with braces (C++11)
// int i3{d2};     // Error! Narrowing not allowed

// Boolean conversions
int x = 5;
if (x) {  // Implicit conversion to bool
    std::cout << "Non-zero\n";
}

// Pointer conversions
Derived* derived = new Derived();
Base* base = derived;  // Implicit upcast

delete derived;
```

### 7. User-Defined Conversions
```cpp
class Fraction {
    int numerator, denominator;
public:
    Fraction(int num, int den = 1)
        : numerator(num), denominator(den) {}

    // Conversion operator to double
    operator double() const {
        return static_cast<double>(numerator) / denominator;
    }

    // Explicit conversion (C++11) - prevents implicit conversion
    explicit operator bool() const {
        return numerator != 0;
    }
};

void useConversions() {
    Fraction f(3, 4);

    // Implicit conversion via operator double()
    double d = f;  // 0.75

    // Explicit conversion required for bool
    if (f) {  // OK in boolean context
        std::cout << "Non-zero fraction\n";
    }

    // bool b = f;  // Error! Explicit conversion required
    bool b = static_cast<bool>(f);  // OK
}

// Conversion constructor
class MyString {
    std::string data;
public:
    // Converting constructor
    MyString(const char* str) : data(str) {}

    // Prevent implicit conversion with explicit
    explicit MyString(int size) : data(size, ' ') {}
};

void useMyString() {
    MyString s1 = "Hello";   // OK, implicit
    // MyString s2 = 100;    // Error! Explicit constructor
    MyString s2(100);        // OK, explicit call
}
```

### 8. Safe Casting Patterns
```cpp
// Pattern 1: Check before dynamic_cast
Base* base = getBase();
if (Derived* derived = dynamic_cast<Derived*>(base)) {
    derived->derivedMethod();
}

// Pattern 2: Visitor pattern (alternative to dynamic_cast)
class Visitor;
class Base {
public:
    virtual void accept(Visitor& v) = 0;
};

// Pattern 3: Type-safe union (std::variant in C++17)
std::variant<int, double, std::string> value = 42;
if (auto* i = std::get_if<int>(&value)) {
    std::cout << "int: " << *i << '\n';
}

// Pattern 4: Template-based type safety
template<typename Target, typename Source>
Target safe_cast(Source source) {
    static_assert(std::is_convertible_v<Source, Target>,
                  "Invalid conversion");
    return static_cast<Target>(source);
}
```

## Best Practices
1. **Prefer static_cast** for most conversions
2. **Use dynamic_cast** only when runtime type checking is needed
3. **Avoid const_cast** except for interfacing with legacy code
4. **Use reinterpret_cast** only for low-level operations
5. **Never use C-style casts** in new code
6. **Check dynamic_cast results** before using
7. **Use explicit** for single-argument constructors
8. **Prefer implicit conversions** when intent is clear
9. **Document why casting** is necessary
10. **Consider alternatives** to casting (templates, virtual functions)

## Common Pitfalls
```cpp
// 1. Dangerous downcast without checking
Base* base = new Base();
Derived* derived = static_cast<Derived*>(base);  // Undefined behavior!
// Use dynamic_cast instead

// 2. Casting away const and modifying
const int ci = 10;
int* pi = const_cast<int*>(&ci);
*pi = 20;  // Undefined behavior!

// 3. Slicing with casts
Derived d;
Base b = static_cast<Base>(d);  // Slicing! Derived part lost

// 4. Incorrect reinterpret_cast usage
float f = 3.14f;
int i = *reinterpret_cast<int*>(&f);  // Type punning, undefined behavior
```

## Resources and References
- [cppreference.com - Explicit type conversion](https://en.cppreference.com/w/cpp/language/explicit_cast)
- [cppreference.com - Implicit conversions](https://en.cppreference.com/w/cpp/language/implicit_conversion)
- [C++ Core Guidelines - Casts](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-casts)

## Navigation
- **Previous Program**: [117 - const and constexpr](../117_const_constexpr/README.md)
- **Next Program**: [119 - Error Handling](../119_error_handling/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
