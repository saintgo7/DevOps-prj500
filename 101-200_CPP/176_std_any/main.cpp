/*
 * Program 176: std::any - Type-Erased Values
 *
 * This program demonstrates:
 * - std::any basics (C++17)
 * - Type erasure and any_cast
 * - Checking and accessing stored types
 * - Practical use cases
 * - Comparison with variant and void*
 */

#include <iostream>
#include <any>
#include <string>
#include <vector>
#include <map>
#include <typeinfo>

// ==============================================
// 1. std::any Basics
// ==============================================

void anyBasicsDemo() {
    std::cout << "\n=== 1. std::any Basics ===\n";

    // Create empty any
    std::any empty;
    std::cout << "Empty any has value: " << std::boolalpha << empty.has_value() << "\n";

    // Store different types
    std::any a1 = 42;
    std::any a2 = 3.14;
    std::any a3 = std::string("Hello");
    std::any a4 = std::vector<int>{1, 2, 3};

    std::cout << "a1 has value: " << a1.has_value() << "\n";
    std::cout << "a2 has value: " << a2.has_value() << "\n";

    // Type information
    std::cout << "a1 type: " << a1.type().name() << "\n";
    std::cout << "a2 type: " << a2.type().name() << "\n";
    std::cout << "a3 type: " << a3.type().name() << "\n";
}

// ==============================================
// 2. any_cast - Accessing Stored Values
// ==============================================

void anyCastDemo() {
    std::cout << "\n=== 2. any_cast - Accessing Values ===\n";

    std::any value = 42;

    // any_cast by value
    try {
        int i = std::any_cast<int>(value);
        std::cout << "any_cast<int>: " << i << "\n";
    } catch (const std::bad_any_cast& e) {
        std::cout << "Error: " << e.what() << "\n";
    }

    // any_cast by pointer (returns nullptr if wrong type)
    if (int* p = std::any_cast<int>(&value)) {
        std::cout << "any_cast<int*>: " << *p << "\n";
    } else {
        std::cout << "Not an int\n";
    }

    // Wrong type cast (throws)
    value = std::string("Test");
    try {
        int i = std::any_cast<int>(value); // Will throw
        std::cout << "Value: " << i << "\n";
    } catch (const std::bad_any_cast& e) {
        std::cout << "Exception: " << e.what() << "\n";
    }

    // Safe cast with pointer
    if (std::string* s = std::any_cast<std::string>(&value)) {
        std::cout << "String value: " << *s << "\n";
    }
}

// ==============================================
// 3. Type Checking
// ==============================================

void typeCheckingDemo() {
    std::cout << "\n=== 3. Type Checking ===\n";

    std::any value = 3.14;

    // Check if has value
    if (value.has_value()) {
        std::cout << "Contains a value\n";
    }

    // Get type info
    const std::type_info& typeInfo = value.type();
    std::cout << "Type: " << typeInfo.name() << "\n";

    // Check specific type
    if (typeInfo == typeid(double)) {
        std::cout << "Is double: true\n";
    }

    if (typeInfo == typeid(int)) {
        std::cout << "Is int: true\n";
    } else {
        std::cout << "Is int: false\n";
    }
}

// ==============================================
// 4. Emplace and Reset
// ==============================================

void emplaceResetDemo() {
    std::cout << "\n=== 4. Emplace and Reset ===\n";

    std::any value;

    // Emplace constructs in-place
    value.emplace<std::string>("Constructed in place");
    std::cout << "After emplace: " << std::any_cast<std::string>(value) << "\n";

    // Assignment
    value = 42;
    std::cout << "After assignment: " << std::any_cast<int>(value) << "\n";

    // Reset clears the value
    value.reset();
    std::cout << "After reset, has value: " << std::boolalpha << value.has_value() << "\n";
}

// ==============================================
// 5. std::any in Containers
// ==============================================

void containersDemo() {
    std::cout << "\n=== 5. std::any in Containers ===\n";

    // Vector of any
    std::vector<std::any> heterogeneous = {
        42,
        3.14,
        std::string("Hello"),
        true,
        std::vector<int>{1, 2, 3}
    };

    std::cout << "Heterogeneous vector:\n";
    for (size_t i = 0; i < heterogeneous.size(); ++i) {
        const auto& item = heterogeneous[i];
        std::cout << "  [" << i << "] type: " << item.type().name();

        // Try to print value based on type
        if (item.type() == typeid(int)) {
            std::cout << ", value: " << std::any_cast<int>(item);
        } else if (item.type() == typeid(double)) {
            std::cout << ", value: " << std::any_cast<double>(item);
        } else if (item.type() == typeid(std::string)) {
            std::cout << ", value: " << std::any_cast<std::string>(item);
        } else if (item.type() == typeid(bool)) {
            std::cout << ", value: " << std::boolalpha << std::any_cast<bool>(item);
        }
        std::cout << "\n";
    }
}

// ==============================================
// 6. Property Bag Pattern
// ==============================================

class PropertyBag {
private:
    std::map<std::string, std::any> properties;

public:
    template<typename T>
    void set(const std::string& key, const T& value) {
        properties[key] = value;
    }

    template<typename T>
    T get(const std::string& key) const {
        auto it = properties.find(key);
        if (it != properties.end()) {
            return std::any_cast<T>(it->second);
        }
        throw std::runtime_error("Property not found: " + key);
    }

    template<typename T>
    T get_or(const std::string& key, const T& defaultValue) const {
        auto it = properties.find(key);
        if (it != properties.end()) {
            try {
                return std::any_cast<T>(it->second);
            } catch (const std::bad_any_cast&) {
                return defaultValue;
            }
        }
        return defaultValue;
    }

    bool has(const std::string& key) const {
        return properties.find(key) != properties.end();
    }

    void remove(const std::string& key) {
        properties.erase(key);
    }
};

void propertyBagDemo() {
    std::cout << "\n=== 6. Property Bag Pattern ===\n";

    PropertyBag config;

    // Set various types
    config.set("port", 8080);
    config.set("host", std::string("localhost"));
    config.set("timeout", 5000);
    config.set("enabled", true);

    // Get values
    std::cout << "Port: " << config.get<int>("port") << "\n";
    std::cout << "Host: " << config.get<std::string>("host") << "\n";
    std::cout << "Timeout: " << config.get<int>("timeout") << "\n";
    std::cout << "Enabled: " << std::boolalpha << config.get<bool>("enabled") << "\n";

    // Get with default
    int buffer_size = config.get_or("buffer_size", 4096);
    std::cout << "Buffer size (default): " << buffer_size << "\n";

    // Check existence
    std::cout << "Has 'host': " << config.has("host") << "\n";
    std::cout << "Has 'unknown': " << config.has("unknown") << "\n";
}

// ==============================================
// 7. Event System with std::any
// ==============================================

struct Event {
    std::string type;
    std::any data;
};

class EventHandler {
public:
    void handleEvent(const Event& event) {
        std::cout << "Event: " << event.type << "\n";

        if (event.type == "click") {
            auto coords = std::any_cast<std::pair<int, int>>(event.data);
            std::cout << "  Click at (" << coords.first << ", " << coords.second << ")\n";
        } else if (event.type == "keypress") {
            auto key = std::any_cast<char>(event.data);
            std::cout << "  Key pressed: " << key << "\n";
        } else if (event.type == "message") {
            auto msg = std::any_cast<std::string>(event.data);
            std::cout << "  Message: " << msg << "\n";
        }
    }
};

void eventSystemDemo() {
    std::cout << "\n=== 7. Event System ===\n";

    EventHandler handler;

    handler.handleEvent({"click", std::make_pair(100, 200)});
    handler.handleEvent({"keypress", 'A'});
    handler.handleEvent({"message", std::string("Hello, World!")});
}

// ==============================================
// 8. std::any vs void* vs std::variant
// ==============================================

void comparisonDemo() {
    std::cout << "\n=== 8. Comparison: any vs void* vs variant ===\n\n";

    std::cout << "void* (C-style):\n";
    std::cout << "  + Small memory footprint\n";
    std::cout << "  - No type safety\n";
    std::cout << "  - Manual lifetime management\n";
    std::cout << "  - Dangerous, error-prone\n\n";

    std::cout << "std::variant:\n";
    std::cout << "  + Type-safe\n";
    std::cout << "  + Knows all possible types at compile-time\n";
    std::cout << "  + Efficient (no heap allocation)\n";
    std::cout << "  - Limited to predefined types\n";
    std::cout << "  - Size = largest alternative\n\n";

    std::cout << "std::any:\n";
    std::cout << "  + Type-safe\n";
    std::cout << "  + Can hold ANY type (runtime polymorphism)\n";
    std::cout << "  + Value semantics\n";
    std::cout << "  - Heap allocation for large types\n";
    std::cout << "  - Runtime type checking overhead\n";
    std::cout << "  - Larger size overhead\n";
}

// ==============================================
// 9. Custom Types with std::any
// ==============================================

struct Point {
    int x, y;

    Point(int x_, int y_) : x(x_), y(y_) {}

    void print() const {
        std::cout << "Point(" << x << ", " << y << ")\n";
    }
};

class Shape {
public:
    virtual ~Shape() = default;
    virtual void draw() const = 0;
};

class Circle : public Shape {
private:
    double radius;

public:
    Circle(double r) : radius(r) {}

    void draw() const override {
        std::cout << "Circle with radius " << radius << "\n";
    }
};

void customTypesDemo() {
    std::cout << "\n=== 9. Custom Types with std::any ===\n";

    // Store custom structs
    std::any point = Point{10, 20};

    if (auto* p = std::any_cast<Point>(&point)) {
        p->print();
    }

    // Store polymorphic objects (via pointer)
    std::any shape = std::make_shared<Circle>(5.0);

    if (auto sp = std::any_cast<std::shared_ptr<Circle>>(shape)) {
        sp->draw();
    }
}

// ==============================================
// 10. Move Semantics with std::any
// ==============================================

void moveSemanticsDemo() {
    std::cout << "\n=== 10. Move Semantics ===\n";

    std::any a1 = std::vector<int>{1, 2, 3, 4, 5};

    std::cout << "a1 size: " << std::any_cast<std::vector<int>>(a1).size() << "\n";

    // Move construction
    std::any a2 = std::move(a1);
    std::cout << "After move, a2 size: " << std::any_cast<std::vector<int>>(a2).size() << "\n";
    std::cout << "After move, a1 has value: " << std::boolalpha << a1.has_value() << "\n";

    // Extract value with move
    std::vector<int> vec = std::any_cast<std::vector<int>&&>(std::move(a2));
    std::cout << "Extracted vector size: " << vec.size() << "\n";
}

// ==============================================
// 11. Practical Use Case: Plugin System
// ==============================================

class Plugin {
public:
    virtual ~Plugin() = default;
    virtual std::string name() const = 0;
    virtual void execute(std::any context) = 0;
};

class LoggerPlugin : public Plugin {
public:
    std::string name() const override {
        return "Logger";
    }

    void execute(std::any context) override {
        if (auto* msg = std::any_cast<std::string>(&context)) {
            std::cout << "[LOG] " << *msg << "\n";
        }
    }
};

class CalculatorPlugin : public Plugin {
public:
    std::string name() const override {
        return "Calculator";
    }

    void execute(std::any context) override {
        if (auto* nums = std::any_cast<std::pair<int, int>>(&context)) {
            std::cout << "[CALC] " << nums->first << " + " << nums->second
                     << " = " << (nums->first + nums->second) << "\n";
        }
    }
};

void pluginSystemDemo() {
    std::cout << "\n=== 11. Plugin System ===\n";

    std::vector<std::unique_ptr<Plugin>> plugins;
    plugins.push_back(std::make_unique<LoggerPlugin>());
    plugins.push_back(std::make_unique<CalculatorPlugin>());

    // Execute plugins with different contexts
    for (auto& plugin : plugins) {
        std::cout << "Executing " << plugin->name() << " plugin:\n";

        if (plugin->name() == "Logger") {
            plugin->execute(std::string("Hello from plugin system"));
        } else if (plugin->name() == "Calculator") {
            plugin->execute(std::make_pair(10, 20));
        }
    }
}

// ==============================================
// 12. Performance Considerations
// ==============================================

void performanceDemo() {
    std::cout << "\n=== 12. Performance Considerations ===\n\n";

    std::cout << "std::any uses Small Object Optimization (SOO):\n";
    std::cout << "  - Small objects (≤ pointer size): stored inline\n";
    std::cout << "  - Large objects: heap allocated\n\n";

    std::cout << "Best practices:\n";
    std::cout << "  1. Use variant when types are known at compile-time\n";
    std::cout << "  2. Use any for true runtime polymorphism\n";
    std::cout << "  3. Avoid excessive any_cast in hot loops\n";
    std::cout << "  4. Consider shared_ptr<Base> for polymorphic types\n";
    std::cout << "  5. Use pointer cast (any_cast<T*>) for safe checking\n";
}

int main() {
    std::cout << "=== C++17 std::any - Type Erasure ===\n";

    // 1. Basics
    anyBasicsDemo();

    // 2. any_cast
    anyCastDemo();

    // 3. Type checking
    typeCheckingDemo();

    // 4. Emplace and reset
    emplaceResetDemo();

    // 5. Containers
    containersDemo();

    // 6. Property bag
    propertyBagDemo();

    // 7. Event system
    eventSystemDemo();

    // 8. Comparison
    comparisonDemo();

    // 9. Custom types
    customTypesDemo();

    // 10. Move semantics
    moveSemanticsDemo();

    // 11. Plugin system
    pluginSystemDemo();

    // 12. Performance
    performanceDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::any holds single value of any type (C++17)\n";
    std::cout << "2. Type erasure with runtime type information\n";
    std::cout << "3. any_cast for type-safe extraction\n";
    std::cout << "4. has_value() and type() for querying\n";
    std::cout << "5. Great for property bags, event systems, plugins\n";
    std::cout << "6. More type-safe than void*, more flexible than variant\n";
    std::cout << "7. Consider performance for critical code paths\n";

    return 0;
}
