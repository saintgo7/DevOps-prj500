/*
 * Program 173: Structured Bindings - Decomposition and Tuple Unpacking
 *
 * This program demonstrates:
 * - Structured bindings for decomposition (C++17)
 * - Binding to arrays, tuples, and structs
 * - Use with containers and algorithms
 * - Custom structured binding support
 * - Practical patterns and use cases
 */

#include <iostream>
#include <tuple>
#include <map>
#include <vector>
#include <string>
#include <array>
#include <utility>
#include <set>

// ==============================================
// 1. Basic Structured Bindings
// ==============================================

std::tuple<int, double, std::string> getPersonData() {
    return {25, 175.5, "Alice"};
}

void basicStructuredBindingsDemo() {
    std::cout << "\n=== 1. Basic Structured Bindings ===\n";

    // Old way (C++11)
    auto person = getPersonData();
    int age = std::get<0>(person);
    double height = std::get<1>(person);
    std::string name = std::get<2>(person);

    std::cout << "Old way: " << name << ", " << age << ", " << height << "cm\n";

    // New way (C++17) - structured bindings
    auto [age2, height2, name2] = getPersonData();

    std::cout << "Structured bindings: " << name2 << ", " << age2 << ", " << height2 << "cm\n";
}

// ==============================================
// 2. Binding to Arrays
// ==============================================

void arrayBindingsDemo() {
    std::cout << "\n=== 2. Array Bindings ===\n";

    int coords[3] = {10, 20, 30};

    // Decompose array
    auto [x, y, z] = coords;

    std::cout << "Coordinates: x=" << x << ", y=" << y << ", z=" << z << "\n";

    // Works with std::array too
    std::array<std::string, 3> colors = {"Red", "Green", "Blue"};
    auto [r, g, b] = colors;

    std::cout << "Colors: " << r << ", " << g << ", " << b << "\n";
}

// ==============================================
// 3. Binding to Structs
// ==============================================

struct Point {
    int x;
    int y;
};

struct Person {
    std::string name;
    int age;
    double salary;
};

void structBindingsDemo() {
    std::cout << "\n=== 3. Struct Bindings ===\n";

    Point p{100, 200};

    // Decompose struct members
    auto [px, py] = p;

    std::cout << "Point: (" << px << ", " << py << ")\n";

    Person person{"Bob", 30, 75000.50};

    auto [name, age, salary] = person;

    std::cout << "Person: " << name << ", age " << age << ", salary $" << salary << "\n";
}

// ==============================================
// 4. Binding to std::pair
// ==============================================

std::pair<std::string, int> getKeyValue() {
    return {"answer", 42};
}

void pairBindingsDemo() {
    std::cout << "\n=== 4. std::pair Bindings ===\n";

    // Old way
    auto kv = getKeyValue();
    std::cout << "Old way: " << kv.first << " = " << kv.second << "\n";

    // New way
    auto [key, value] = getKeyValue();
    std::cout << "Structured bindings: " << key << " = " << value << "\n";
}

// ==============================================
// 5. Binding in Range-Based For Loops
// ==============================================

void rangeForBindingsDemo() {
    std::cout << "\n=== 5. Range-Based For Loop Bindings ===\n";

    std::map<std::string, int> scores = {
        {"Alice", 95},
        {"Bob", 87},
        {"Charlie", 92}
    };

    // Old way
    std::cout << "Old way:\n";
    for (const auto& pair : scores) {
        std::cout << "  " << pair.first << ": " << pair.second << "\n";
    }

    // New way with structured bindings
    std::cout << "\nStructured bindings:\n";
    for (const auto& [name, score] : scores) {
        std::cout << "  " << name << ": " << score << "\n";
    }
}

// ==============================================
// 6. Reference Bindings
// ==============================================

void referenceBindingsDemo() {
    std::cout << "\n=== 6. Reference Bindings ===\n";

    std::tuple<int, int, int> data{1, 2, 3};

    // By value (copies)
    auto [a, b, c] = data;
    a = 100; // Doesn't modify original
    std::cout << "After value binding modification:\n";
    std::cout << "  Original: " << std::get<0>(data) << "\n";
    std::cout << "  Copy: " << a << "\n";

    // By reference (modifies original)
    auto& [x, y, z] = data;
    x = 200; // Modifies original
    std::cout << "\nAfter reference binding modification:\n";
    std::cout << "  Original: " << std::get<0>(data) << "\n";
    std::cout << "  Reference: " << x << "\n";

    // Const reference (read-only)
    const auto& [r1, r2, r3] = data;
    std::cout << "\nConst reference binding: " << r1 << ", " << r2 << ", " << r3 << "\n";
}

// ==============================================
// 7. Binding with std::tie (Pre-C++17 Alternative)
// ==============================================

void tieComparisonDemo() {
    std::cout << "\n=== 7. std::tie vs Structured Bindings ===\n";

    auto getData = []() {
        return std::make_tuple(42, 3.14, std::string("Hello"));
    };

    // Using std::tie (C++11)
    int val1;
    double val2;
    std::string val3;
    std::tie(val1, val2, val3) = getData();

    std::cout << "std::tie: " << val1 << ", " << val2 << ", " << val3 << "\n";

    // Using structured bindings (C++17)
    auto [v1, v2, v3] = getData();

    std::cout << "Structured bindings: " << v1 << ", " << v2 << ", " << v3 << "\n";

    std::cout << "\nStructured bindings are cleaner and more concise!\n";
}

// ==============================================
// 8. Multiple Return Values
// ==============================================

struct DivisionResult {
    int quotient;
    int remainder;
};

DivisionResult divide(int a, int b) {
    return {a / b, a % b};
}

std::tuple<bool, std::string> validateInput(const std::string& input) {
    if (input.empty()) {
        return {false, "Input is empty"};
    }
    if (input.length() < 3) {
        return {false, "Input too short"};
    }
    return {true, "Valid input"};
}

void multipleReturnsDemo() {
    std::cout << "\n=== 8. Multiple Return Values ===\n";

    // Struct return
    auto [quotient, remainder] = divide(17, 5);
    std::cout << "17 / 5 = " << quotient << " remainder " << remainder << "\n";

    // Tuple return
    auto [valid, message] = validateInput("Hello");
    std::cout << "Validation: " << std::boolalpha << valid << ", " << message << "\n";

    auto [valid2, message2] = validateInput("Hi");
    std::cout << "Validation: " << valid2 << ", " << message2 << "\n";
}

// ==============================================
// 9. Binding with Insert Operations
// ==============================================

void insertBindingsDemo() {
    std::cout << "\n=== 9. Bindings with Insert Operations ===\n";

    std::map<std::string, int> ages;

    // insert returns pair<iterator, bool>
    auto [it1, inserted1] = ages.insert({"Alice", 25});
    std::cout << "Insert Alice: " << (inserted1 ? "success" : "failed") << "\n";
    std::cout << "  Value: " << it1->first << " = " << it1->second << "\n";

    auto [it2, inserted2] = ages.insert({"Alice", 30}); // Duplicate key
    std::cout << "Insert Alice again: " << (inserted2 ? "success" : "failed") << "\n";
    std::cout << "  Existing value: " << it2->second << "\n";

    // insert_or_assign
    auto [it3, inserted3] = ages.insert_or_assign("Alice", 30);
    std::cout << "Insert or assign Alice: " << (inserted3 ? "inserted" : "assigned") << "\n";
    std::cout << "  Updated value: " << it3->second << "\n";
}

// ==============================================
// 10. Custom Type Support
// ==============================================

// To support structured bindings, provide:
// 1. std::tuple_size specialization
// 2. std::tuple_element specialization
// 3. get<> function

class Color {
private:
    int r, g, b;

public:
    Color(int red, int green, int blue) : r(red), g(green), b(blue) {}

    int red() const { return r; }
    int green() const { return g; }
    int blue() const { return b; }
};

// Support structured bindings for Color
namespace std {
    template<>
    struct tuple_size<Color> : integral_constant<size_t, 3> {};

    template<>
    struct tuple_element<0, Color> { using type = int; };

    template<>
    struct tuple_element<1, Color> { using type = int; };

    template<>
    struct tuple_element<2, Color> { using type = int; };
}

template<size_t N>
int get(const Color& c) {
    if constexpr (N == 0) return c.red();
    else if constexpr (N == 1) return c.green();
    else if constexpr (N == 2) return c.blue();
}

void customTypeDemo() {
    std::cout << "\n=== 10. Custom Type Support ===\n";

    Color purple(128, 0, 128);

    auto [r, g, b] = purple;

    std::cout << "RGB: (" << r << ", " << g << ", " << b << ")\n";
}

// ==============================================
// 11. Ignoring Values
// ==============================================

void ignoringValuesDemo() {
    std::cout << "\n=== 11. Ignoring Values ===\n";

    auto getData = []() {
        return std::make_tuple(1, 2, 3, 4, 5);
    };

    // C++17: Cannot directly ignore values, but can use [[maybe_unused]]
    auto [a, b, c, d, e] = getData();
    [[maybe_unused]] auto unused = b; // Mark as intentionally unused
    [[maybe_unused]] auto unused2 = d;

    std::cout << "Using only: " << a << ", " << c << ", " << e << "\n";

    // Can use std::ignore with std::tie
    int x, z;
    std::tie(x, std::ignore, z, std::ignore, std::ignore) = getData();
    std::cout << "With std::tie: " << x << ", " << z << "\n";
}

// ==============================================
// 12. Practical Use Cases
// ==============================================

void practicalUseCasesDemo() {
    std::cout << "\n=== 12. Practical Use Cases ===\n";

    // 1. Processing map entries
    std::cout << "\n1. Map iteration:\n";
    std::map<std::string, std::vector<int>> data = {
        {"scores", {95, 87, 92}},
        {"ages", {25, 30, 28}}
    };

    for (const auto& [category, values] : data) {
        std::cout << "  " << category << ": ";
        for (int val : values) {
            std::cout << val << " ";
        }
        std::cout << "\n";
    }

    // 2. Function returning success + result
    std::cout << "\n2. Error handling pattern:\n";
    auto readFile = [](const std::string& filename) -> std::pair<bool, std::string> {
        if (filename.empty()) {
            return {false, "Invalid filename"};
        }
        return {true, "File contents: ..."};
    };

    if (auto [success, content] = readFile("data.txt"); success) {
        std::cout << "  " << content << "\n";
    } else {
        std::cout << "  Error: " << content << "\n";
    }

    // 3. Decomposing complex data structures
    std::cout << "\n3. Complex structures:\n";
    std::vector<std::tuple<std::string, int, double>> students = {
        {"Alice", 95, 3.9},
        {"Bob", 87, 3.5},
        {"Charlie", 92, 3.7}
    };

    for (const auto& [name, score, gpa] : students) {
        std::cout << "  " << name << ": score=" << score << ", GPA=" << gpa << "\n";
    }
}

int main() {
    std::cout << "=== C++17 Structured Bindings ===\n";

    // 1. Basic bindings
    basicStructuredBindingsDemo();

    // 2. Array bindings
    arrayBindingsDemo();

    // 3. Struct bindings
    structBindingsDemo();

    // 4. Pair bindings
    pairBindingsDemo();

    // 5. Range-for bindings
    rangeForBindingsDemo();

    // 6. Reference bindings
    referenceBindingsDemo();

    // 7. std::tie comparison
    tieComparisonDemo();

    // 8. Multiple returns
    multipleReturnsDemo();

    // 9. Insert bindings
    insertBindingsDemo();

    // 10. Custom types
    customTypeDemo();

    // 11. Ignoring values
    ignoringValuesDemo();

    // 12. Practical use cases
    practicalUseCasesDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. Structured bindings simplify decomposition (C++17)\n";
    std::cout << "2. Works with arrays, tuples, pairs, and structs\n";
    std::cout << "3. auto [x, y] = ... creates named bindings\n";
    std::cout << "4. Use auto& for references, const auto& for const\n";
    std::cout << "5. Great for map iteration and multiple returns\n";
    std::cout << "6. Custom types can support bindings via get<>\n";
    std::cout << "7. More readable than std::tie or std::get<>\n";

    return 0;
}
