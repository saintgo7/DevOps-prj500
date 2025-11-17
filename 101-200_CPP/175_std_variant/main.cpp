/*
 * Program 175: std::variant - Type-Safe Unions
 *
 * This program demonstrates:
 * - std::variant basics (C++17)
 * - Type-safe unions
 * - std::visit for variant visiting
 * - Pattern matching with variants
 * - Practical use cases
 */

#include <iostream>
#include <variant>
#include <string>
#include <vector>
#include <type_traits>

// ==============================================
// 1. std::variant Basics
// ==============================================

void variantBasicsDemo() {
    std::cout << "\n=== 1. std::variant Basics ===\n";

    // Variant can hold int, double, or string
    std::variant<int, double, std::string> var;

    std::cout << "Initial index: " << var.index() << "\n"; // 0 (first type)
    std::cout << "Initial value: " << std::get<int>(var) << "\n"; // Default constructed int

    // Assign different types
    var = 42;
    std::cout << "After int assignment:\n";
    std::cout << "  index: " << var.index() << " (int)\n";
    std::cout << "  value: " << std::get<int>(var) << "\n";

    var = 3.14;
    std::cout << "After double assignment:\n";
    std::cout << "  index: " << var.index() << " (double)\n";
    std::cout << "  value: " << std::get<double>(var) << "\n";

    var = std::string("Hello");
    std::cout << "After string assignment:\n";
    std::cout << "  index: " << var.index() << " (string)\n";
    std::cout << "  value: " << std::get<std::string>(var) << "\n";
}

// ==============================================
// 2. Accessing Variant Values
// ==============================================

void accessingValuesDemo() {
    std::cout << "\n=== 2. Accessing Variant Values ===\n";

    std::variant<int, double, std::string> var = 42;

    // Using std::get<T>
    try {
        int value = std::get<int>(var);
        std::cout << "std::get<int>: " << value << "\n";
    } catch (const std::bad_variant_access& e) {
        std::cout << "Error: " << e.what() << "\n";
    }

    // Using std::get<index>
    int value2 = std::get<0>(var); // Get first alternative
    std::cout << "std::get<0>: " << value2 << "\n";

    // Using std::get_if (returns pointer, nullptr if wrong type)
    if (auto* pval = std::get_if<int>(&var)) {
        std::cout << "std::get_if<int>: " << *pval << "\n";
    } else {
        std::cout << "Not an int\n";
    }

    // Wrong type access
    var = std::string("Test");
    if (auto* pval = std::get_if<int>(&var)) {
        std::cout << "Is int: " << *pval << "\n";
    } else {
        std::cout << "Not an int (safe check with get_if)\n";
    }
}

// ==============================================
// 3. std::holds_alternative
// ==============================================

void holdsAlternativeDemo() {
    std::cout << "\n=== 3. std::holds_alternative ===\n";

    std::variant<int, double, std::string> var = 3.14;

    std::cout << std::boolalpha;
    std::cout << "holds int: " << std::holds_alternative<int>(var) << "\n";
    std::cout << "holds double: " << std::holds_alternative<double>(var) << "\n";
    std::cout << "holds string: " << std::holds_alternative<std::string>(var) << "\n";
}

// ==============================================
// 4. std::visit - Visitor Pattern
// ==============================================

void visitDemo() {
    std::cout << "\n=== 4. std::visit - Visitor Pattern ===\n";

    using Variant = std::variant<int, double, std::string>;

    // Visitor using generic lambda
    auto visitor = [](const auto& value) {
        std::cout << "Value: " << value << " (type: " << typeid(value).name() << ")\n";
    };

    Variant var1 = 42;
    Variant var2 = 3.14;
    Variant var3 = std::string("Hello");

    std::visit(visitor, var1);
    std::visit(visitor, var2);
    std::visit(visitor, var3);
}

// ==============================================
// 5. Advanced std::visit with Overload
// ==============================================

// Helper for overloading lambdas
template<class... Ts>
struct overload : Ts... {
    using Ts::operator()...;
};

template<class... Ts>
overload(Ts...) -> overload<Ts...>; // Deduction guide

void advancedVisitDemo() {
    std::cout << "\n=== 5. Advanced std::visit with Overload ===\n";

    using Variant = std::variant<int, double, std::string>;

    // Different behavior for each type
    auto visitor = overload{
        [](int value) {
            std::cout << "Integer: " << value << " * 2 = " << (value * 2) << "\n";
        },
        [](double value) {
            std::cout << "Double: " << value << " * 3.14 = " << (value * 3.14) << "\n";
        },
        [](const std::string& value) {
            std::cout << "String: '" << value << "' (length: " << value.length() << ")\n";
        }
    };

    Variant var1 = 10;
    Variant var2 = 2.5;
    Variant var3 = std::string("C++17");

    std::visit(visitor, var1);
    std::visit(visitor, var2);
    std::visit(visitor, var3);
}

// ==============================================
// 6. Variant as Return Type
// ==============================================

using Result = std::variant<int, std::string>; // Success: int, Error: string

Result divide(int a, int b) {
    if (b == 0) {
        return std::string("Division by zero error");
    }
    return a / b;
}

void returnTypeDemo() {
    std::cout << "\n=== 6. Variant as Return Type ===\n";

    auto printResult = [](const Result& result) {
        std::visit(overload{
            [](int value) {
                std::cout << "  Success: " << value << "\n";
            },
            [](const std::string& error) {
                std::cout << "  Error: " << error << "\n";
            }
        }, result);
    };

    std::cout << "divide(10, 2):\n";
    printResult(divide(10, 2));

    std::cout << "divide(10, 0):\n";
    printResult(divide(10, 0));
}

// ==============================================
// 7. Variant State Machine
// ==============================================

struct Idle {};
struct Running { int progress; };
struct Paused { int savedProgress; };
struct Completed {};

using State = std::variant<Idle, Running, Paused, Completed>;

class StateMachine {
private:
    State state;

public:
    StateMachine() : state(Idle{}) {}

    void start() {
        state = Running{0};
    }

    void pause() {
        std::visit(overload{
            [this](const Running& r) {
                state = Paused{r.progress};
            },
            [](const auto&) {
                std::cout << "  Cannot pause from this state\n";
            }
        }, state);
    }

    void resume() {
        std::visit(overload{
            [this](const Paused& p) {
                state = Running{p.savedProgress};
            },
            [](const auto&) {
                std::cout << "  Cannot resume from this state\n";
            }
        }, state);
    }

    void complete() {
        state = Completed{};
    }

    void printState() const {
        std::cout << "State: ";
        std::visit(overload{
            [](const Idle&) { std::cout << "Idle"; },
            [](const Running& r) { std::cout << "Running (progress: " << r.progress << ")"; },
            [](const Paused& p) { std::cout << "Paused (saved: " << p.savedProgress << ")"; },
            [](const Completed&) { std::cout << "Completed"; }
        }, state);
        std::cout << "\n";
    }
};

void stateMachineDemo() {
    std::cout << "\n=== 7. Variant State Machine ===\n";

    StateMachine sm;

    sm.printState();

    sm.start();
    sm.printState();

    sm.pause();
    sm.printState();

    sm.resume();
    sm.printState();

    sm.complete();
    sm.printState();
}

// ==============================================
// 8. Variant with Custom Types
// ==============================================

struct Circle {
    double radius;
    double area() const { return 3.14159 * radius * radius; }
};

struct Rectangle {
    double width, height;
    double area() const { return width * height; }
};

struct Triangle {
    double base, height;
    double area() const { return 0.5 * base * height; }
};

using Shape = std::variant<Circle, Rectangle, Triangle>;

double calculateArea(const Shape& shape) {
    return std::visit([](const auto& s) { return s.area(); }, shape);
}

void customTypesDemo() {
    std::cout << "\n=== 8. Variant with Custom Types ===\n";

    std::vector<Shape> shapes;
    shapes.push_back(Circle{5.0});
    shapes.push_back(Rectangle{4.0, 6.0});
    shapes.push_back(Triangle{3.0, 4.0});

    for (size_t i = 0; i < shapes.size(); ++i) {
        double area = calculateArea(shapes[i]);
        std::cout << "Shape " << (i + 1) << " area: " << area << "\n";
    }
}

// ==============================================
// 9. Variant vs Union
// ==============================================

// Old C-style union (unsafe)
union OldUnion {
    int i;
    double d;
    // Cannot have string! (non-trivial type)
};

void variantVsUnionDemo() {
    std::cout << "\n=== 9. Variant vs Union ===\n";

    std::cout << "Old union limitations:\n";
    std::cout << "  - No type safety\n";
    std::cout << "  - Cannot track which member is active\n";
    std::cout << "  - Cannot hold non-trivial types\n";
    std::cout << "  - Manual lifetime management\n\n";

    std::cout << "std::variant advantages:\n";
    std::cout << "  - Type-safe\n";
    std::cout << "  - Tracks active alternative via index()\n";
    std::cout << "  - Can hold any type including strings, vectors, etc.\n";
    std::cout << "  - Automatic lifetime management\n";
    std::cout << "  - Visitor pattern support\n";
}

// ==============================================
// 10. Monostate for Empty Variant
// ==============================================

using OptionalInt = std::variant<std::monostate, int>;

OptionalInt parseNumber(const std::string& str) {
    try {
        return std::stoi(str);
    } catch (...) {
        return std::monostate{}; // Represents "no value"
    }
}

void monostateDemo() {
    std::cout << "\n=== 10. std::monostate for Empty Variant ===\n";

    auto printOptional = [](const OptionalInt& opt) {
        std::visit(overload{
            [](std::monostate) {
                std::cout << "  No value\n";
            },
            [](int value) {
                std::cout << "  Value: " << value << "\n";
            }
        }, opt);
    };

    std::cout << "parseNumber(\"42\"):\n";
    printOptional(parseNumber("42"));

    std::cout << "parseNumber(\"invalid\"):\n";
    printOptional(parseNumber("invalid"));

    std::cout << "\nmonostate represents an empty/null state\n";
}

// ==============================================
// 11. Variant Comparison
// ==============================================

void comparisonDemo() {
    std::cout << "\n=== 11. Variant Comparison ===\n";

    using Variant = std::variant<int, std::string>;

    Variant var1 = 42;
    Variant var2 = 42;
    Variant var3 = 100;
    Variant var4 = std::string("Hello");

    std::cout << std::boolalpha;
    std::cout << "var1 (42) == var2 (42): " << (var1 == var2) << "\n";
    std::cout << "var1 (42) == var3 (100): " << (var1 == var3) << "\n";
    std::cout << "var1 (42) < var3 (100): " << (var1 < var3) << "\n";

    // Different types compare by index
    std::cout << "var1 (int) < var4 (string): " << (var1 < var4) << "\n";
}

// ==============================================
// 12. Practical Use Case: JSON-like Structure
// ==============================================

struct JsonValue;

using JsonNull = std::monostate;
using JsonBool = bool;
using JsonNumber = double;
using JsonString = std::string;
using JsonArray = std::vector<JsonValue>;

struct JsonValue {
    std::variant<JsonNull, JsonBool, JsonNumber, JsonString, JsonArray> value;

    JsonValue() : value(JsonNull{}) {}
    JsonValue(bool b) : value(b) {}
    JsonValue(double n) : value(n) {}
    JsonValue(const char* s) : value(std::string(s)) {}
    JsonValue(const std::string& s) : value(s) {}
    JsonValue(const JsonArray& a) : value(a) {}
};

void printJson(const JsonValue& json, int indent = 0) {
    std::string indentStr(indent * 2, ' ');

    std::visit(overload{
        [&](JsonNull) {
            std::cout << indentStr << "null";
        },
        [&](bool b) {
            std::cout << indentStr << (b ? "true" : "false");
        },
        [&](double n) {
            std::cout << indentStr << n;
        },
        [&](const std::string& s) {
            std::cout << indentStr << "\"" << s << "\"";
        },
        [&](const JsonArray& arr) {
            std::cout << indentStr << "[\n";
            for (size_t i = 0; i < arr.size(); ++i) {
                printJson(arr[i], indent + 1);
                if (i < arr.size() - 1) std::cout << ",";
                std::cout << "\n";
            }
            std::cout << indentStr << "]";
        }
    }, json.value);
}

void jsonDemo() {
    std::cout << "\n=== 12. JSON-like Structure ===\n";

    JsonArray arr = {
        JsonValue(42.0),
        JsonValue("Hello"),
        JsonValue(true),
        JsonValue(),
        JsonValue(JsonArray{JsonValue(1.0), JsonValue(2.0), JsonValue(3.0)})
    };

    JsonValue root(arr);

    std::cout << "JSON structure:\n";
    printJson(root);
    std::cout << "\n";
}

int main() {
    std::cout << "=== C++17 std::variant - Type-Safe Unions ===\n";

    // 1. Basics
    variantBasicsDemo();

    // 2. Accessing values
    accessingValuesDemo();

    // 3. holds_alternative
    holdsAlternativeDemo();

    // 4. std::visit
    visitDemo();

    // 5. Advanced visit
    advancedVisitDemo();

    // 6. Return type
    returnTypeDemo();

    // 7. State machine
    stateMachineDemo();

    // 8. Custom types
    customTypesDemo();

    // 9. vs Union
    variantVsUnionDemo();

    // 10. monostate
    monostateDemo();

    // 11. Comparison
    comparisonDemo();

    // 12. JSON example
    jsonDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::variant is type-safe union (C++17)\n";
    std::cout << "2. Can hold one of several alternative types\n";
    std::cout << "3. index() returns active alternative index\n";
    std::cout << "4. std::visit enables visitor pattern\n";
    std::cout << "5. std::get<T> or std::get_if<T> for access\n";
    std::cout << "6. std::monostate represents empty state\n";
    std::cout << "7. Great for error handling, state machines, polymorphism\n";

    return 0;
}
