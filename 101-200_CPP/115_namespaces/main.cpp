/*
 * Program 115: Namespaces in C++
 *
 * Topics Covered:
 * - Namespace definition
 * - using declarations and directives
 * - Nested namespaces
 * - Anonymous/unnamed namespaces
 * - Namespace aliases
 * - Inline namespaces (C++11)
 * - Namespace scope resolution
 * - Best practices
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o namespaces main.cpp
 */

#include <iostream>
#include <string>

// Basic namespace
namespace Math {
    const double PI = 3.14159;

    int add(int a, int b) {
        return a + b;
    }

    int subtract(int a, int b) {
        return a - b;
    }

    namespace Advanced {
        double power(double base, int exp) {
            double result = 1.0;
            for (int i = 0; i < exp; i++) {
                result *= base;
            }
            return result;
        }
    }
}

// Nested namespaces (C++17 syntax)
namespace Company::Department::Team {
    std::string getName() {
        return "Engineering Team";
    }
}

// Anonymous namespace (internal linkage)
namespace {
    int internalCounter = 0;

    void internalFunction() {
        std::cout << "This function has internal linkage" << std::endl;
    }
}

// Multiple files can have same namespace
namespace Math {
    int multiply(int a, int b) {
        return a * b;
    }
}

// Inline namespace (C++11)
namespace Library {
    inline namespace v2 {
        void doSomething() {
            std::cout << "Version 2.0" << std::endl;
        }
    }

    namespace v1 {
        void doSomething() {
            std::cout << "Version 1.0" << std::endl;
        }
    }
}

void demonstrateBasicNamespaces();
void demonstrateUsingDeclarations();
void demonstrateNestedNamespaces();
void demonstrateAnonymousNamespaces();
void demonstrateNamespaceAliases();
void demonstrateInlineNamespaces();

int main() {
    std::cout << "=== C++ Namespaces ===" << std::endl << std::endl;

    demonstrateBasicNamespaces();
    demonstrateUsingDeclarations();
    demonstrateNestedNamespaces();
    demonstrateAnonymousNamespaces();
    demonstrateNamespaceAliases();
    demonstrateInlineNamespaces();

    return 0;
}

void demonstrateBasicNamespaces() {
    std::cout << "--- Basic Namespaces ---" << std::endl;

    // Accessing namespace members with :: (scope resolution)
    std::cout << "Math::PI = " << Math::PI << std::endl;
    std::cout << "Math::add(5, 3) = " << Math::add(5, 3) << std::endl;
    std::cout << "Math::multiply(4, 6) = " << Math::multiply(4, 6) << std::endl;

    // Preventing name conflicts
    namespace Graphics {
        int width = 800;
    }

    namespace Audio {
        int width = 2;  // No conflict!
    }

    std::cout << "\nGraphics::width = " << Graphics::width << std::endl;
    std::cout << "Audio::width = " << Audio::width << std::endl;

    std::cout << std::endl;
}

void demonstrateUsingDeclarations() {
    std::cout << "--- Using Declarations and Directives ---" << std::endl;

    // using declaration: brings specific name into scope
    using Math::PI;
    std::cout << "Using declaration - PI: " << PI << std::endl;

    // using directive: brings all names into scope
    {
        using namespace Math;
        std::cout << "Using directive - add(10, 20): " << add(10, 20) << std::endl;
        std::cout << "Using directive - subtract(30, 10): " << subtract(30, 10) << std::endl;
    }  // using directive scope ends

    // Can't use add() here without Math:: prefix
    // std::cout << add(5, 3) << std::endl;  // Error!

    // Multiple using declarations
    using Math::add;
    using Math::subtract;
    std::cout << "\nMultiple using declarations:" << std::endl;
    std::cout << "add(1, 2) = " << add(1, 2) << std::endl;
    std::cout << "subtract(5, 3) = " << subtract(5, 3) << std::endl;

    // Warning: using namespace std in global scope is bad practice!
    // using namespace std;  // Don't do this!

    std::cout << std::endl;
}

void demonstrateNestedNamespaces() {
    std::cout << "--- Nested Namespaces ---" << std::endl;

    // Accessing nested namespace
    double result = Math::Advanced::power(2, 10);
    std::cout << "2^10 = " << result << std::endl;

    // C++17 nested namespace syntax
    std::cout << "Team name: " << Company::Department::Team::getName() << std::endl;

    // using for nested namespaces
    using namespace Math::Advanced;
    std::cout << "power(3, 4) = " << power(3, 4) << std::endl;

    std::cout << std::endl;
}

void demonstrateAnonymousNamespaces() {
    std::cout << "--- Anonymous Namespaces ---" << std::endl;

    // Anonymous namespace members have internal linkage
    // They're visible only in this translation unit
    internalCounter++;
    std::cout << "Internal counter: " << internalCounter << std::endl;

    internalFunction();

    // Equivalent to static in C
    // Anonymous namespace is preferred in C++
    std::cout << "\nAnonymous namespaces provide internal linkage" << std::endl;
    std::cout << "Preferred over 'static' for file-scope variables" << std::endl;

    std::cout << std::endl;
}

void demonstrateNamespaceAliases() {
    std::cout << "--- Namespace Aliases ---" << std::endl;

    // Long namespace names can be aliased
    namespace CDT = Company::Department::Team;

    std::cout << "Using alias CDT: " << CDT::getName() << std::endl;

    // Useful for long nested namespaces
    namespace MA = Math::Advanced;
    std::cout << "MA::power(5, 2) = " << MA::power(5, 2) << std::endl;

    // Common pattern with std
    namespace fs = std::filesystem;  // In real code with <filesystem>

    std::cout << std::endl;
}

void demonstrateInlineNamespaces() {
    std::cout << "--- Inline Namespaces (C++11) ---" << std::endl;

    // Inline namespace members are accessible without qualification
    Library::doSomething();  // Calls v2::doSomething (inline)

    // Explicit version selection
    Library::v1::doSomething();
    Library::v2::doSomething();

    // Use case: Versioning
    std::cout << "\nInline namespaces are useful for versioning" << std::endl;
    std::cout << "Default version can be changed by making different namespace inline" << std::endl;

    std::cout << std::endl;
}

/*
 * Namespace Best Practices:
 *
 * 1. Never use 'using namespace' in header files
 * 2. Avoid 'using namespace std' in global scope
 * 3. Use namespaces to organize code logically
 * 4. Prefer using declarations over using directives
 * 5. Use anonymous namespaces for internal linkage
 * 6. Keep namespace names short but descriptive
 * 7. Use nested namespaces for hierarchical organization
 * 8. Consider inline namespaces for versioning
 * 9. Use namespace aliases for long names
 * 10. Document namespace purpose and organization
 *
 * Common Standard Library Namespaces:
 * - std           - Standard library
 * - std::chrono   - Time utilities
 * - std::filesystem - File system operations
 * - std::this_thread - Thread utilities
 * - std::literals - User-defined literals
 * - std::rel_ops  - Relational operators
 *
 * Namespace Anti-patterns:
 * ❌ using namespace std;  // Global scope
 * ❌ using namespace in headers
 * ❌ Too many nested levels (>3)
 * ❌ Single-letter namespace names
 * ❌ Namespace names that conflict with standard library
 */
