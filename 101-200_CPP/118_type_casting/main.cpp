/*
 * Program 118: Type Casting in C++
 *
 * Topics Covered:
 * - C-style casts
 * - static_cast
 * - dynamic_cast
 * - const_cast
 * - reinterpret_cast
 * - Implicit conversions
 * - Explicit conversions
 * - When to use each cast
 * - Type casting safety
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o type_casting main.cpp
 */

#include <iostream>
#include <string>
#include <typeinfo>

void demonstrateCStyleCasts();
void demonstrateStaticCast();
void demonstrateDynamicCast();
void demonstrateConstCast();
void demonstrateReinterpretCast();
void demonstrateImplicitConversions();

int main() {
    std::cout << "=== C++ Type Casting ===" << std::endl << std::endl;

    demonstrateCStyleCasts();
    demonstrateStaticCast();
    demonstrateDynamicCast();
    demonstrateConstCast();
    demonstrateReinterpretCast();
    demonstrateImplicitConversions();

    return 0;
}

void demonstrateCStyleCasts() {
    std::cout << "--- C-Style Casts (Avoid in C++) ---" << std::endl;

    // C-style cast: (type)value
    double pi = 3.14159;
    int truncated = (int)pi;
    std::cout << "C-style cast: (int)3.14159 = " << truncated << std::endl;

    // C++ style: type(value)
    int truncated2 = int(pi);
    std::cout << "C++ functional cast: int(3.14159) = " << truncated2 << std::endl;

    // Problems with C-style casts:
    // 1. Too powerful - can do almost any conversion
    // 2. Hard to find in code
    // 3. No compile-time safety
    // 4. Unclear intent

    std::cout << "\nC-style casts are discouraged in modern C++" << std::endl;
    std::cout << "Use specific C++ casts instead" << std::endl;

    std::cout << std::endl;
}

void demonstrateStaticCast() {
    std::cout << "--- static_cast ---" << std::endl;

    // 1. Numeric conversions
    double d = 3.14159;
    int i = static_cast<int>(d);
    std::cout << "double to int: " << i << std::endl;

    int a = 10;
    double result = static_cast<double>(a) / 3;
    std::cout << "10 / 3.0 = " << result << std::endl;

    // 2. Enum conversions
    enum Color { RED, GREEN, BLUE };
    int colorValue = static_cast<int>(GREEN);
    std::cout << "\nEnum to int: GREEN = " << colorValue << std::endl;

    Color color = static_cast<Color>(1);
    std::cout << "int to enum: 1 = " << (color == GREEN ? "GREEN" : "other") << std::endl;

    // 3. Pointer conversions (related types)
    class Base {
    public:
        virtual ~Base() = default;
        virtual void show() { std::cout << "Base" << std::endl; }
    };

    class Derived : public Base {
    public:
        void show() override { std::cout << "Derived" << std::endl; }
    };

    Derived derived;
    Base* basePtr = static_cast<Base*>(&derived);  // Upcast (safe)
    basePtr->show();

    // Downcast with static_cast (not type-safe!)
    Base base;
    // Derived* derivedPtr = static_cast<Derived*>(&base);  // Compiles but dangerous!

    // 4. void* conversions
    int value = 42;
    void* voidPtr = &value;
    int* intPtr = static_cast<int*>(voidPtr);
    std::cout << "\nvoid* to int*: " << *intPtr << std::endl;

    // 5. User-defined conversions
    std::cout << "\nstatic_cast is for well-defined conversions" << std::endl;

    std::cout << std::endl;
}

void demonstrateDynamicCast() {
    std::cout << "--- dynamic_cast ---" << std::endl;

    class Base {
    public:
        virtual ~Base() = default;
        virtual void show() { std::cout << "Base" << std::endl; }
    };

    class Derived1 : public Base {
    public:
        void show() override { std::cout << "Derived1" << std::endl; }
        void special() { std::cout << "Derived1 special function" << std::endl; }
    };

    class Derived2 : public Base {
    public:
        void show() override { std::cout << "Derived2" << std::endl; }
    };

    // dynamic_cast with pointers (returns nullptr on failure)
    Base* base = new Derived1();

    Derived1* d1 = dynamic_cast<Derived1*>(base);
    if (d1 != nullptr) {
        std::cout << "Successfully cast to Derived1" << std::endl;
        d1->special();
    }

    Derived2* d2 = dynamic_cast<Derived2*>(base);
    if (d2 == nullptr) {
        std::cout << "Failed to cast to Derived2 (as expected)" << std::endl;
    }

    // dynamic_cast with references (throws exception on failure)
    try {
        Derived1& ref1 = dynamic_cast<Derived1&>(*base);
        std::cout << "\nSuccessfully cast reference to Derived1" << std::endl;
        ref1.show();
    } catch (std::bad_cast& e) {
        std::cout << "Cast failed: " << e.what() << std::endl;
    }

    try {
        Derived2& ref2 = dynamic_cast<Derived2&>(*base);
        ref2.show();
    } catch (std::bad_cast& e) {
        std::cout << "Cast to Derived2 failed: " << e.what() << std::endl;
    }

    delete base;

    // Requirements for dynamic_cast:
    // 1. Requires polymorphic base class (virtual functions)
    // 2. Runtime type checking (RTTI)
    // 3. Only for pointers/references
    // 4. Safer than static_cast for downcasting

    std::cout << std::endl;
}

void demonstrateConstCast() {
    std::cout << "--- const_cast ---" << std::endl;

    // const_cast: Add or remove const qualifier

    // Removing const (dangerous!)
    const int constValue = 42;
    const int* constPtr = &constValue;

    // int* nonConstPtr = constPtr;  // Error!
    int* nonConstPtr = const_cast<int*>(constPtr);
    std::cout << "Removed const: " << *nonConstPtr << std::endl;

    // Modifying const object is undefined behavior!
    // *nonConstPtr = 100;  // DANGER! Undefined behavior

    // Safe use case: Passing to API that doesn't modify but isn't marked const
    auto legacyFunction = [](int* ptr) {
        // Function doesn't modify, but parameter isn't const
        std::cout << "Legacy function: " << *ptr << std::endl;
    };

    const int value = 10;
    legacyFunction(const_cast<int*>(&value));  // Safe if function doesn't modify

    // Adding const
    int nonConst = 20;
    const int* makeConst = const_cast<const int*>(&nonConst);
    std::cout << "Added const: " << *makeConst << std::endl;

    // const_cast with references
    const std::string constStr = "Hello";
    std::string& mutableStr = const_cast<std::string&>(constStr);
    // mutableStr += " World";  // Undefined behavior if original is const!

    std::cout << "\nUse const_cast sparingly and carefully!" << std::endl;

    std::cout << std::endl;
}

void demonstrateReinterpretCast() {
    std::cout << "--- reinterpret_cast ---" << std::endl;

    // reinterpret_cast: Low-level reinterpretation of bit pattern

    // 1. Pointer to integer
    int value = 42;
    int* ptr = &value;

    uintptr_t address = reinterpret_cast<uintptr_t>(ptr);
    std::cout << "Pointer as integer: 0x" << std::hex << address << std::dec << std::endl;

    int* ptrBack = reinterpret_cast<int*>(address);
    std::cout << "Back to pointer: " << *ptrBack << std::endl;

    // 2. Pointer to different pointer type
    double d = 3.14159;
    double* dPtr = &d;

    // Very dangerous! Type punning
    long long* llPtr = reinterpret_cast<long long*>(dPtr);
    std::cout << "\nDouble bits as long long: " << *llPtr << std::endl;

    // 3. Function pointer conversions
    void (*funcPtr)() = nullptr;
    void* voidFuncPtr = reinterpret_cast<void*>(funcPtr);

    // 4. Object pointer to byte pointer
    int number = 0x12345678;
    unsigned char* bytes = reinterpret_cast<unsigned char*>(&number);

    std::cout << "\nBytes of integer: ";
    for (size_t i = 0; i < sizeof(number); i++) {
        std::cout << std::hex << static_cast<int>(bytes[i]) << " ";
    }
    std::cout << std::dec << std::endl;

    std::cout << "\nreinterpret_cast is very dangerous!" << std::endl;
    std::cout << "Use only when absolutely necessary (e.g., low-level programming)" << std::endl;

    std::cout << std::endl;
}

void demonstrateImplicitConversions() {
    std::cout << "--- Implicit Conversions ---" << std::endl;

    // Numeric promotions
    int i = 10;
    double d = i;  // Implicit int to double
    std::cout << "Implicit int to double: " << d << std::endl;

    // Narrowing (warning or error in some contexts)
    double pi = 3.14159;
    // int truncated = pi;  // Implicit, but loses precision (warning)
    int truncated = static_cast<int>(pi);  // Explicit (better)
    std::cout << "Explicit narrowing: " << truncated << std::endl;

    // Pointer conversions
    int* intPtr = nullptr;
    void* voidPtr = intPtr;  // Implicit to void*
    std::cout << "Implicit to void*: " << voidPtr << std::endl;

    // Array to pointer decay
    int arr[5] = {1, 2, 3, 4, 5};
    int* ptr = arr;  // Implicit array to pointer
    std::cout << "Array decay: ptr[0] = " << ptr[0] << std::endl;

    // User-defined conversions
    class Fraction {
    public:
        Fraction(int num, int den = 1) : numerator(num), denominator(den) {}

        // Implicit conversion to double
        operator double() const {
            return static_cast<double>(numerator) / denominator;
        }

        // Explicit conversion (C++11)
        explicit operator int() const {
            return numerator / denominator;
        }

    private:
        int numerator, denominator;
    };

    Fraction f(3, 4);
    double fDouble = f;  // Implicit conversion
    std::cout << "\nFraction to double: " << fDouble << std::endl;

    // int fInt = f;  // Error: explicit conversion
    int fInt = static_cast<int>(f);  // OK
    std::cout << "Fraction to int (explicit): " << fInt << std::endl;

    std::cout << std::endl;
}

/*
 * C++ Cast Summary:
 *
 * static_cast<T>:
 * - Most common cast
 * - Compile-time type checking
 * - Numeric conversions, enum conversions
 * - Upcasting (derived to base)
 * - Downcasting (without runtime check - use carefully!)
 * - void* conversions
 *
 * dynamic_cast<T>:
 * - Runtime type checking (RTTI)
 * - Downcasting with safety (polymorphic types only)
 * - Returns nullptr for pointers on failure
 * - Throws bad_cast for references on failure
 * - Requires virtual functions in base class
 *
 * const_cast<T>:
 * - Add or remove const/volatile qualifiers
 * - Only cast that can remove const
 * - Modifying const object is undefined behavior
 * - Use sparingly (mainly for legacy APIs)
 *
 * reinterpret_cast<T>:
 * - Low-level bit reinterpretation
 * - Pointer to integer, different pointer types
 * - Very dangerous, platform-dependent
 * - Use only when absolutely necessary
 *
 * Best Practices:
 * 1. Avoid C-style casts
 * 2. Use static_cast for well-defined conversions
 * 3. Use dynamic_cast for safe downcasting
 * 4. Use const_cast only when needed for APIs
 * 5. Avoid reinterpret_cast except in low-level code
 * 6. Prefer implicit conversions when safe
 * 7. Use explicit keyword to prevent unwanted conversions
 * 8. Make casts visible and searchable in code
 */
