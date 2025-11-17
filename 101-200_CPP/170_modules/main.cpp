/*
 * Program 170: C++20 Modules - Modern Code Organization
 *
 * This program demonstrates:
 * - Module basics with export and import
 * - Module interfaces and implementations
 * - Module partitions
 * - Global module fragment
 * - Benefits over traditional headers
 *
 * Note: C++20 modules support varies by compiler
 * GCC 11+: -std=c++20 -fmodules-ts
 * Clang 14+: -std=c++20 -fmodules
 * MSVC 2019+: /std:c++20
 *
 * This file demonstrates module concepts but may need
 * separate module files for full compilation.
 */

#include <iostream>
#include <vector>
#include <string>
#include <cmath>

/*
 * ==============================================
 * Module Basics (Conceptual Examples)
 * ==============================================
 *
 * 1. Module Interface File (math_module.ixx):
 *
 * export module math_module;
 *
 * export int add(int a, int b) {
 *     return a + b;
 * }
 *
 * export int multiply(int a, int b) {
 *     return a * b;
 * }
 *
 * 2. Using the Module:
 *
 * import math_module;
 *
 * int main() {
 *     int result = add(5, 3);
 * }
 *
 * ==============================================
 * Key Module Concepts
 * ==============================================
 */

// Since full module support requires separate files,
// this program demonstrates module concepts using
// traditional code with explanatory comments.

namespace ModuleConcepts {

// ==============================================
// 1. Module Interface Simulation
// ==============================================

// Module: math.operations
// This would be: export module math.operations;
namespace MathOperations {
    // Exported functions
    // In modules: export int add(int a, int b)
    int add(int a, int b) {
        return a + b;
    }

    int subtract(int a, int b) {
        return a - b;
    }

    int multiply(int a, int b) {
        return a * b;
    }

    double divide(double a, double b) {
        if (b == 0) {
            throw std::runtime_error("Division by zero");
        }
        return a / b;
    }

    // Private implementation (not exported)
    namespace internal {
        int helper_function() {
            return 42;
        }
    }
}

void moduleBasicsDemo() {
    std::cout << "\n=== 1. Module Basics ===\n";
    std::cout << "Module: math.operations\n";
    std::cout << "Exported: add, subtract, multiply, divide\n";
    std::cout << "Private: internal::helper_function\n\n";

    std::cout << "add(10, 5) = " << MathOperations::add(10, 5) << "\n";
    std::cout << "subtract(10, 5) = " << MathOperations::subtract(10, 5) << "\n";
    std::cout << "multiply(10, 5) = " << MathOperations::multiply(10, 5) << "\n";
    std::cout << "divide(10, 5) = " << MathOperations::divide(10, 5) << "\n";
}

// ==============================================
// 2. Module with Class Export
// ==============================================

// Module: geometry
// export module geometry;
namespace Geometry {
    // export class Point
    class Point {
    private:
        double x, y;

    public:
        Point(double x, double y) : x(x), y(y) {}

        double getX() const { return x; }
        double getY() const { return y; }

        double distanceFrom(const Point& other) const {
            double dx = x - other.x;
            double dy = y - other.y;
            return std::sqrt(dx * dx + dy * dy);
        }

        void print() const {
            std::cout << "Point(" << x << ", " << y << ")\n";
        }
    };

    // export class Circle
    class Circle {
    private:
        Point center;
        double radius;

    public:
        Circle(const Point& c, double r) : center(c), radius(r) {}

        double area() const {
            return 3.14159 * radius * radius;
        }

        double circumference() const {
            return 2 * 3.14159 * radius;
        }

        void print() const {
            std::cout << "Circle at ";
            center.print();
            std::cout << "  Radius: " << radius << "\n";
        }
    };
}

void moduleClassDemo() {
    std::cout << "\n=== 2. Module with Classes ===\n";
    std::cout << "Module: geometry\n";
    std::cout << "Exported: Point, Circle\n\n";

    Geometry::Point p1(0, 0);
    Geometry::Point p2(3, 4);

    p1.print();
    p2.print();
    std::cout << "Distance: " << p1.distanceFrom(p2) << "\n\n";

    Geometry::Circle circle(p1, 5.0);
    circle.print();
    std::cout << "Area: " << circle.area() << "\n";
    std::cout << "Circumference: " << circle.circumference() << "\n";
}

// ==============================================
// 3. Module Partitions (Conceptual)
// ==============================================

/*
 * Module partitions allow splitting a module into multiple files:
 *
 * // shapes:base (partition)
 * export module shapes:base;
 * export class Shape { ... };
 *
 * // shapes:circle (partition)
 * export module shapes:circle;
 * import :base;
 * export class Circle : public Shape { ... };
 *
 * // shapes (primary interface)
 * export module shapes;
 * export import :base;
 * export import :circle;
 *
 * Usage:
 * import shapes; // Gets everything
 */

namespace ShapesModule {
    // Base partition
    class Shape {
    protected:
        std::string name;

    public:
        explicit Shape(const std::string& n) : name(n) {}
        virtual ~Shape() = default;

        virtual double area() const = 0;
        virtual void print() const {
            std::cout << "Shape: " << name << "\n";
        }
    };

    // Circle partition
    class Circle : public Shape {
    private:
        double radius;

    public:
        Circle(double r) : Shape("Circle"), radius(r) {}

        double area() const override {
            return 3.14159 * radius * radius;
        }

        void print() const override {
            Shape::print();
            std::cout << "  Radius: " << radius << "\n";
            std::cout << "  Area: " << area() << "\n";
        }
    };

    // Rectangle partition
    class Rectangle : public Shape {
    private:
        double width, height;

    public:
        Rectangle(double w, double h)
            : Shape("Rectangle"), width(w), height(h) {}

        double area() const override {
            return width * height;
        }

        void print() const override {
            Shape::print();
            std::cout << "  Width: " << width << ", Height: " << height << "\n";
            std::cout << "  Area: " << area() << "\n";
        }
    };
}

void modulePartitionsDemo() {
    std::cout << "\n=== 3. Module Partitions ===\n";
    std::cout << "Module: shapes\n";
    std::cout << "Partitions: shapes:base, shapes:circle, shapes:rectangle\n\n";

    ShapesModule::Circle c(5.0);
    ShapesModule::Rectangle r(4.0, 6.0);

    c.print();
    std::cout << "\n";
    r.print();
}

// ==============================================
// 4. Global Module Fragment
// ==============================================

/*
 * Global module fragment allows including traditional headers:
 *
 * module;  // Start global module fragment
 *
 * #include <vector>
 * #include <string>
 *
 * export module my_module;  // End fragment, start module
 *
 * export void process(const std::vector<std::string>& data) {
 *     // Use vector and string
 * }
 */

namespace GlobalFragmentExample {
    // Simulated module that uses standard library
    std::vector<std::string> createNames() {
        return {"Alice", "Bob", "Charlie", "Diana"};
    }

    void printNames(const std::vector<std::string>& names) {
        std::cout << "Names: ";
        for (const auto& name : names) {
            std::cout << name << " ";
        }
        std::cout << "\n";
    }
}

void globalFragmentDemo() {
    std::cout << "\n=== 4. Global Module Fragment ===\n";
    std::cout << "Allows mixing traditional includes with modules\n\n";

    auto names = GlobalFragmentExample::createNames();
    GlobalFragmentExample::printNames(names);
}

// ==============================================
// 5. Module Interface vs Implementation
// ==============================================

/*
 * Module can separate interface from implementation:
 *
 * // calculator.ixx (interface)
 * export module calculator;
 *
 * export class Calculator {
 * public:
 *     int add(int a, int b);
 *     int multiply(int a, int b);
 * private:
 *     int complex_calculation(int x);
 * };
 *
 * // calculator.cpp (implementation)
 * module calculator;
 *
 * int Calculator::add(int a, int b) {
 *     return a + b;
 * }
 *
 * int Calculator::multiply(int a, int b) {
 *     return complex_calculation(a) * b;
 * }
 *
 * int Calculator::complex_calculation(int x) {
 *     return x * 2; // Internal implementation
 * }
 */

namespace CalculatorModule {
    class Calculator {
    public:
        int add(int a, int b) {
            return a + b;
        }

        int multiply(int a, int b) {
            return complex_calculation(a) * b;
        }

    private:
        int complex_calculation(int x) {
            // Private implementation detail
            return x * 2;
        }
    };
}

void interfaceImplementationDemo() {
    std::cout << "\n=== 5. Interface vs Implementation ===\n";
    std::cout << "Separate module interface (.ixx) from implementation (.cpp)\n\n";

    CalculatorModule::Calculator calc;
    std::cout << "add(5, 3) = " << calc.add(5, 3) << "\n";
    std::cout << "multiply(5, 3) = " << calc.multiply(5, 3) << "\n";
}

// ==============================================
// 6. Benefits of Modules
// ==============================================

void benefitsDemo() {
    std::cout << "\n=== 6. Benefits of Modules ===\n\n";

    std::cout << "1. Faster Compilation:\n";
    std::cout << "   - Modules are compiled once, not per translation unit\n";
    std::cout << "   - No repeated header parsing\n\n";

    std::cout << "2. Better Encapsulation:\n";
    std::cout << "   - Only exported entities are visible\n";
    std::cout << "   - Internal implementation is truly private\n\n";

    std::cout << "3. No Macro Leakage:\n";
    std::cout << "   - Macros don't leak between modules\n";
    std::cout << "   - Safer, more predictable code\n\n";

    std::cout << "4. Order Independence:\n";
    std::cout << "   - Import order doesn't matter\n";
    std::cout << "   - No header include guards needed\n\n";

    std::cout << "5. Logical Organization:\n";
    std::cout << "   - Clear module boundaries\n";
    std::cout << "   - Better code structure\n\n";
}

// ==============================================
// 7. Module Best Practices
// ==============================================

void bestPracticesDemo() {
    std::cout << "\n=== 7. Module Best Practices ===\n\n";

    std::cout << "1. One Module Per Component:\n";
    std::cout << "   - Keep modules focused and cohesive\n\n";

    std::cout << "2. Use Partitions for Large Modules:\n";
    std::cout << "   - Split complex modules into partitions\n\n";

    std::cout << "3. Export Interfaces, Not Implementation:\n";
    std::cout << "   - Only export what users need\n\n";

    std::cout << "4. Naming Conventions:\n";
    std::cout << "   - Use dots for hierarchy: std.core, std.io\n\n";

    std::cout << "5. Transition Gradually:\n";
    std::cout << "   - Can mix modules with traditional headers\n\n";

    std::cout << "6. Document Module Dependencies:\n";
    std::cout << "   - Clear import relationships\n\n";
}

// ==============================================
// 8. Example Module Structure
// ==============================================

/*
 * Project Structure:
 *
 * myproject/
 * ├── modules/
 * │   ├── core.ixx           (export module core;)
 * │   ├── utils.ixx          (export module utils;)
 * │   ├── math/
 * │   │   ├── math.ixx       (export module math;)
 * │   │   ├── basic.ixx      (export module math:basic;)
 * │   │   └── advanced.ixx   (export module math:advanced;)
 * │   └── io/
 * │       ├── io.ixx         (export module io;)
 * │       └── file.ixx       (export module io:file;)
 * └── main.cpp
 *
 * main.cpp:
 * import core;
 * import utils;
 * import math;
 * import io;
 *
 * int main() { ... }
 */

void moduleStructureDemo() {
    std::cout << "\n=== 8. Example Module Structure ===\n\n";

    std::cout << "Recommended project organization:\n\n";

    std::cout << "myproject/\n";
    std::cout << "├── modules/           (Module interface files)\n";
    std::cout << "│   ├── core.ixx\n";
    std::cout << "│   ├── utils.ixx\n";
    std::cout << "│   └── math.ixx\n";
    std::cout << "├── src/               (Implementation files)\n";
    std::cout << "│   ├── core.cpp\n";
    std::cout << "│   ├── utils.cpp\n";
    std::cout << "│   └── math.cpp\n";
    std::cout << "└── main.cpp           (Application entry)\n\n";

    std::cout << "Import in main.cpp:\n";
    std::cout << "import core;\n";
    std::cout << "import utils;\n";
    std::cout << "import math;\n";
}

// ==============================================
// 9. Standard Library Modules (C++23)
// ==============================================

/*
 * C++23 introduces standard library modules:
 *
 * import std;        // All standard library
 * import std.core;   // Core facilities
 * import std.io;     // I/O facilities
 * import std.regex;  // Regular expressions
 *
 * Instead of:
 * #include <iostream>
 * #include <vector>
 * #include <string>
 */

void standardModulesDemo() {
    std::cout << "\n=== 9. Standard Library Modules (C++23) ===\n\n";

    std::cout << "Traditional headers:\n";
    std::cout << "#include <iostream>\n";
    std::cout << "#include <vector>\n";
    std::cout << "#include <string>\n\n";

    std::cout << "C++23 modules:\n";
    std::cout << "import std;        // Everything\n";
    std::cout << "import std.core;   // Core only\n";
    std::cout << "import std.io;     // I/O only\n\n";

    std::cout << "Benefits: Faster compilation, cleaner code\n";
}

// ==============================================
// 10. Migration Path
// ==============================================

void migrationPathDemo() {
    std::cout << "\n=== 10. Migration from Headers to Modules ===\n\n";

    std::cout << "Step 1: Start with new modules for new code\n";
    std::cout << "Step 2: Use global module fragment for legacy includes\n";
    std::cout << "Step 3: Gradually convert headers to modules\n";
    std::cout << "Step 4: Use module partitions for organization\n";
    std::cout << "Step 5: Eventually pure module-based project\n\n";

    std::cout << "Compatible approach:\n";
    std::cout << "module;  // Global fragment\n";
    std::cout << "#include \"legacy.h\"\n";
    std::cout << "export module new_module;\n";
    std::cout << "export void new_function() { ... }\n";
}

} // namespace ModuleConcepts

int main() {
    std::cout << "=== C++20 Modules ===\n";
    std::cout << "Note: Full module support requires C++20 compiler\n";
    std::cout << "This demo shows module concepts using traditional code\n";

    using namespace ModuleConcepts;

    // 1. Module basics
    moduleBasicsDemo();

    // 2. Module with classes
    moduleClassDemo();

    // 3. Module partitions
    modulePartitionsDemo();

    // 4. Global fragment
    globalFragmentDemo();

    // 5. Interface vs implementation
    interfaceImplementationDemo();

    // 6. Benefits
    benefitsDemo();

    // 7. Best practices
    bestPracticesDemo();

    // 8. Module structure
    moduleStructureDemo();

    // 9. Standard library modules
    standardModulesDemo();

    // 10. Migration path
    migrationPathDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. Modules replace traditional header files\n";
    std::cout << "2. export declares public interface\n";
    std::cout << "3. import brings in module contents\n";
    std::cout << "4. Faster compilation than headers\n";
    std::cout << "5. Better encapsulation and isolation\n";
    std::cout << "6. No macro leakage between modules\n";
    std::cout << "7. C++23 adds standard library modules\n";

    return 0;
}
