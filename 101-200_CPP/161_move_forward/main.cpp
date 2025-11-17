/*
 * Program 161: std::move and std::forward - Move Semantics and Perfect Forwarding
 *
 * This program demonstrates:
 * - std::move for enabling move semantics
 * - std::forward for perfect forwarding
 * - Rvalue references and move constructors
 * - Performance benefits of move semantics
 */

#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include <memory>

// Custom class to demonstrate move semantics
class Resource {
private:
    std::string name;
    std::vector<int> data;

public:
    // Constructor
    Resource(const std::string& n, size_t size) : name(n), data(size, 42) {
        std::cout << "Constructor: " << name << " (size: " << size << ")\n";
    }

    // Copy constructor
    Resource(const Resource& other) : name(other.name), data(other.data) {
        std::cout << "Copy Constructor: " << name << " - EXPENSIVE COPY\n";
    }

    // Move constructor
    Resource(Resource&& other) noexcept
        : name(std::move(other.name)), data(std::move(other.data)) {
        std::cout << "Move Constructor: " << name << " - EFFICIENT MOVE\n";
    }

    // Copy assignment
    Resource& operator=(const Resource& other) {
        if (this != &other) {
            name = other.name;
            data = other.data;
            std::cout << "Copy Assignment: " << name << " - EXPENSIVE COPY\n";
        }
        return *this;
    }

    // Move assignment
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) {
            name = std::move(other.name);
            data = std::move(other.data);
            std::cout << "Move Assignment: " << name << " - EFFICIENT MOVE\n";
        }
        return *this;
    }

    void display() const {
        std::cout << "Resource: " << name << ", data size: " << data.size() << "\n";
    }
};

// Function demonstrating std::move
Resource createResource(const std::string& name) {
    Resource res(name, 1000000);
    return res; // RVO (Return Value Optimization) may apply
}

// Function accepting rvalue reference
void processResource(Resource&& res) {
    std::cout << "Processing rvalue resource: ";
    res.display();
}

// Template function demonstrating perfect forwarding
template<typename T>
void wrapper(T&& arg) {
    // Without std::forward, arg would always be treated as lvalue
    // std::forward preserves the value category (lvalue or rvalue)
    std::cout << "Wrapper forwarding argument...\n";
    processResource(std::forward<T>(arg));
}

// Factory function using perfect forwarding
template<typename T, typename... Args>
std::unique_ptr<T> makeUnique(Args&&... args) {
    std::cout << "Factory creating object with perfect forwarding...\n";
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

// Demonstrating move with containers
void containerMoveExample() {
    std::cout << "\n=== Container Move Example ===\n";

    std::vector<std::string> source = {"C++", "is", "awesome"};
    std::cout << "Source size: " << source.size() << "\n";

    // Move the vector (no deep copy)
    std::vector<std::string> dest = std::move(source);
    std::cout << "After move - Dest size: " << dest.size() << "\n";
    std::cout << "After move - Source size: " << source.size() << " (moved-from state)\n";

    for (const auto& s : dest) {
        std::cout << s << " ";
    }
    std::cout << "\n";
}

// Demonstrating move vs copy performance
void moveVsCopyDemo() {
    std::cout << "\n=== Move vs Copy Performance ===\n";

    Resource r1("Original", 1000000);

    // Copy semantics
    std::cout << "\nUsing copy:\n";
    Resource r2 = r1;

    // Move semantics
    std::cout << "\nUsing move:\n";
    Resource r3 = std::move(r1);
    std::cout << "Note: r1 is now in moved-from state\n";
}

// Demonstrating perfect forwarding
void perfectForwardingDemo() {
    std::cout << "\n=== Perfect Forwarding Demo ===\n";

    Resource r("ForwardTest", 100);

    // Forward lvalue
    std::cout << "\nForwarding lvalue:\n";
    // wrapper(r); // This would fail because processResource expects rvalue

    // Forward rvalue
    std::cout << "\nForwarding rvalue:\n";
    wrapper(Resource("RValue", 100));
    wrapper(std::move(r));
}

// Demonstrating factory with perfect forwarding
void factoryDemo() {
    std::cout << "\n=== Factory Pattern with Perfect Forwarding ===\n";

    auto ptr1 = makeUnique<Resource>("Factory1", 500);
    auto ptr2 = makeUnique<Resource>("Factory2", 1000);

    ptr1->display();
    ptr2->display();
}

// Class demonstrating move-only type
class MoveOnly {
private:
    std::unique_ptr<int> data;
    std::string name;

public:
    MoveOnly(const std::string& n, int value)
        : data(std::make_unique<int>(value)), name(n) {
        std::cout << "MoveOnly created: " << name << "\n";
    }

    // Delete copy operations
    MoveOnly(const MoveOnly&) = delete;
    MoveOnly& operator=(const MoveOnly&) = delete;

    // Default move operations
    MoveOnly(MoveOnly&&) = default;
    MoveOnly& operator=(MoveOnly&&) = default;

    void display() const {
        std::cout << "MoveOnly: " << name << ", value: " << *data << "\n";
    }
};

void moveOnlyDemo() {
    std::cout << "\n=== Move-Only Type Demo ===\n";

    MoveOnly obj1("First", 42);
    // MoveOnly obj2 = obj1; // Error: copy deleted
    MoveOnly obj2 = std::move(obj1); // OK: move constructor

    obj2.display();
}

// Reference collapsing demonstration
template<typename T>
void referenceCollapsingDemo(T&& param) {
    std::cout << "\n=== Reference Collapsing ===\n";
    std::cout << "T&& can bind to both lvalues and rvalues\n";
    std::cout << "This is a universal/forwarding reference\n";

    // Use type traits to determine the type
    if constexpr (std::is_lvalue_reference_v<T>) {
        std::cout << "Received lvalue reference\n";
    } else {
        std::cout << "Received rvalue reference\n";
    }
}

int main() {
    std::cout << "=== C++ Move Semantics and Perfect Forwarding ===\n";

    // Demonstrate move vs copy
    moveVsCopyDemo();

    // Demonstrate container moves
    containerMoveExample();

    // Demonstrate perfect forwarding
    perfectForwardingDemo();

    // Demonstrate factory pattern
    factoryDemo();

    // Demonstrate move-only types
    moveOnlyDemo();

    // Demonstrate reference collapsing
    int x = 10;
    referenceCollapsingDemo(x);           // lvalue
    referenceCollapsingDemo(20);          // rvalue
    referenceCollapsingDemo(std::move(x)); // rvalue

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::move casts to rvalue reference (doesn't actually move)\n";
    std::cout << "2. std::forward preserves value category in templates\n";
    std::cout << "3. Move semantics avoid expensive copies\n";
    std::cout << "4. Perfect forwarding enables generic wrapper functions\n";
    std::cout << "5. T&& in templates is a forwarding reference, not rvalue ref\n";

    return 0;
}
