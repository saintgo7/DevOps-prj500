# Program 115: Namespaces in C++

## Description
Comprehensive exploration of namespaces in C++ covering namespace declaration, nested namespaces, using directives, namespace aliases, anonymous namespaces, and best practices. This program demonstrates how namespaces organize code and prevent name collisions in large projects.

## Learning Objectives
- Understand namespace purpose and benefits
- Master namespace declaration and definition
- Work with nested and inline namespaces
- Use using declarations and directives appropriately
- Create namespace aliases
- Apply anonymous namespaces for internal linkage
- Follow namespace best practices

## Features
- Basic namespace declaration and usage
- Nested namespaces
- Inline namespaces (C++11)
- Using declarations and directives
- Namespace aliases
- Anonymous (unnamed) namespaces
- Argument-dependent lookup (ADL)
- Namespace versioning
- Best practices for organizing code

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/115_namespaces
g++ -std=c++20 -Wall -Wextra -o namespaces main.cpp
```

### Execution
```bash
./namespaces
```

## Key Concepts

### 1. Basic Namespace Declaration
```cpp
// Define a namespace
namespace MyNamespace {
    int value = 10;

    void function() {
        std::cout << "MyNamespace::function()\n";
    }

    class MyClass {
    public:
        void method() {
            std::cout << "MyClass::method()\n";
        }
    };
}

// Using namespace members
int main() {
    // Fully qualified name
    MyNamespace::function();

    // Create object from namespace
    MyNamespace::MyClass obj;
    obj.method();

    // Access variable
    std::cout << MyNamespace::value << '\n';

    return 0;
}

// Namespace can be reopened
namespace MyNamespace {
    void anotherFunction() {
        std::cout << "Another function\n";
    }
}
```

### 2. Nested Namespaces
```cpp
// Traditional nested namespaces
namespace Company {
    namespace Project {
        namespace Module {
            void function() {
                std::cout << "Nested function\n";
            }
        }
    }
}

// C++17 simplified syntax
namespace Company::Project::Module {
    void anotherFunction() {
        std::cout << "Another nested function\n";
    }
}

// Usage
int main() {
    Company::Project::Module::function();
    Company::Project::Module::anotherFunction();

    return 0;
}
```

### 3. Using Declarations and Directives
```cpp
namespace Math {
    const double PI = 3.14159;
    double square(double x) { return x * x; }
    double cube(double x) { return x * x * x; }
}

// Using declaration (bring specific name into scope)
using Math::PI;
using Math::square;

void example1() {
    std::cout << PI << '\n';        // OK
    std::cout << square(5) << '\n'; // OK
    // std::cout << cube(3) << '\n';  // Error! cube not in scope
    std::cout << Math::cube(3) << '\n';  // OK with full qualification
}

// Using directive (bring entire namespace into scope)
using namespace Math;

void example2() {
    std::cout << PI << '\n';     // OK
    std::cout << square(5) << '\n';  // OK
    std::cout << cube(3) << '\n';    // OK
}

// Scope of using declarations
void example3() {
    {
        using Math::PI;
        std::cout << PI << '\n';  // OK inside block
    }
    // std::cout << PI << '\n';  // Error! Outside block scope
}
```

### 4. Namespace Aliases
```cpp
namespace VeryLongCompanyName {
    namespace ProjectName {
        namespace ModuleName {
            void function() {
                std::cout << "Long namespace path\n";
            }
        }
    }
}

// Create alias for convenience
namespace VLCN = VeryLongCompanyName;
namespace Mod = VeryLongCompanyName::ProjectName::ModuleName;

// Usage
int main() {
    Mod::function();  // Much shorter!

    // Common alias for standard library
    namespace fs = std::filesystem;
    fs::path p = "/home/user";

    return 0;
}
```

### 5. Anonymous (Unnamed) Namespaces
```cpp
// File: helper.cpp

// Anonymous namespace (internal linkage)
namespace {
    // Only visible in this translation unit
    int internalCounter = 0;

    void internalHelper() {
        std::cout << "Internal helper\n";
    }

    class InternalClass {
        // Implementation details
    };
}

// Public function can use anonymous namespace members
void publicFunction() {
    internalCounter++;
    internalHelper();
}

// Equivalent to static in C (but preferred in C++)
// Old C style:
static int counter = 0;         // Internal linkage

// Modern C++ style (preferred):
namespace {
    int counter = 0;            // Internal linkage
}
```

### 6. Inline Namespaces (C++11)
```cpp
// Versioning with inline namespaces
namespace MyLib {
    // Old version
    namespace v1 {
        void function() {
            std::cout << "Version 1\n";
        }
    }

    // New version (inline makes it default)
    inline namespace v2 {
        void function() {
            std::cout << "Version 2\n";
        }
    }
}

// Usage
int main() {
    MyLib::function();       // Calls v2::function() (inline namespace)
    MyLib::v1::function();   // Explicitly call v1
    MyLib::v2::function();   // Explicitly call v2

    return 0;
}

// ABI versioning example
namespace MyLibrary {
    inline namespace v2_0 {
        class Widget {
        public:
            void newMethod() {}  // New in v2.0
        };
    }

    namespace v1_0 {
        class Widget {
            // Old interface
        };
    }
}
```

### 7. Argument-Dependent Lookup (ADL / Koenig Lookup)
```cpp
namespace MyNamespace {
    class MyClass {};

    void function(MyClass obj) {
        std::cout << "MyNamespace::function\n";
    }
}

int main() {
    MyNamespace::MyClass obj;

    // ADL: function found via argument's namespace
    function(obj);  // Works! No need for MyNamespace::function(obj)

    // Also works with operators
    MyNamespace::MyClass a, b;
    // operator<<(std::cout, obj);  // ADL for operators
}

// Practical example with std::cout
namespace MyNS {
    struct Point { int x, y; };

    // ADL allows this to work with std::cout
    std::ostream& operator<<(std::ostream& os, const Point& p) {
        return os << "(" << p.x << ", " << p.y << ")";
    }
}

int main() {
    MyNS::Point p{10, 20};
    std::cout << p << '\n';  // Works due to ADL!
}
```

### 8. Namespace Organization Patterns
```cpp
// Pattern 1: Feature-based organization
namespace Graphics {
    namespace Rendering {
        void render() {}
    }
    namespace Animation {
        void animate() {}
    }
}

// Pattern 2: Layer-based organization
namespace DataLayer {
    void saveData() {}
}
namespace BusinessLayer {
    void processData() {}
}
namespace PresentationLayer {
    void displayData() {}
}

// Pattern 3: Component-based organization
namespace UI {
    class Button {};
    class TextBox {};
}
namespace Database {
    class Connection {};
    class Query {};
}

// Pattern 4: Internal/External separation
namespace MyLibrary {
    // Public API
    void publicFunction();

    namespace detail {  // or 'internal'
        // Implementation details (not part of public API)
        void helperFunction();
    }
}
```

### 9. Global Namespace
```cpp
// Global namespace (no namespace declaration)
int globalVariable = 42;
void globalFunction() {}

// Access from within namespace
namespace MyNamespace {
    void function() {
        // Access global explicitly with ::
        ::globalVariable = 100;
        ::globalFunction();

        // Or implicitly (if no conflict)
        globalVariable = 200;
        globalFunction();
    }
}

// Avoid pollution of global namespace
// Bad:
int count;              // Global variable
void helper() {}        // Global function

// Good:
namespace MyApp {
    int count;          // In namespace
    void helper() {}    // In namespace
}
```

### 10. Using Namespace std
```cpp
// AVOID in header files!
// using namespace std;  // BAD in headers!

// OK in implementation files (with caution)
void function1() {
    using namespace std;
    cout << "Hello" << endl;  // OK in limited scope
}

// Better: Use specific using declarations
void function2() {
    using std::cout;
    using std::endl;
    cout << "Hello" << endl;
}

// Best: Fully qualify or use sparingly
void function3() {
    std::cout << "Hello" << std::endl;
}

// NEVER in header files
// my_header.h:
// using namespace std;  // VERY BAD! Pollutes all includers
```

## Best Practices
1. **Use namespaces** to organize code and prevent name collisions
2. **Never use `using namespace` in header files**
3. **Prefer specific `using` declarations** over `using namespace`
4. **Use nested namespaces** for logical organization
5. **Use anonymous namespaces** instead of static for internal linkage
6. **Create namespace aliases** for long names
7. **Use inline namespaces** for versioning
8. **Keep namespace names short** but descriptive
9. **Follow project conventions** for namespace structure
10. **Document namespace purpose** and organization

## Common Patterns
```cpp
// 1. Project namespace structure
namespace CompanyName {
    namespace ProductName {
        namespace Component {
            // Code here
        }
    }
}

// 2. Versioning
namespace MyLib {
    inline namespace v3 {
        // Current version (default)
    }
    namespace v2 {
        // Previous version (for compatibility)
    }
}

// 3. Internal implementation details
namespace MyLibrary {
    // Public API
    void publicFunction();

    namespace detail {
        // Private implementation (convention: 'detail' or 'internal')
        void implementationDetail();
    }
}

// 4. Traits and utilities
namespace MyLib {
    namespace traits {
        // Type traits
    }
    namespace utils {
        // Utility functions
    }
}
```

## Resources and References
- [cppreference.com - Namespaces](https://en.cppreference.com/w/cpp/language/namespace)
- [cppreference.com - ADL](https://en.cppreference.com/w/cpp/language/adl)
- [C++ Core Guidelines - Namespaces](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-using-directive)

## Navigation
- **Previous Program**: [114 - Preprocessor](../114_preprocessor/README.md)
- **Next Program**: [116 - Memory Management](../116_memory_management/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
