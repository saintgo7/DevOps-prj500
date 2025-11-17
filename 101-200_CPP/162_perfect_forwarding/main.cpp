/*
 * Program 162: Perfect Forwarding - Universal References and Forwarding References
 *
 * This program demonstrates:
 * - Universal/forwarding references (T&&)
 * - Perfect forwarding with std::forward
 * - Reference collapsing rules
 * - Common forwarding patterns
 */

#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <type_traits>
#include <memory>

// Helper function to display value category
template<typename T>
void printValueCategory() {
    std::cout << "Type analysis: ";
    if constexpr (std::is_lvalue_reference_v<T>) {
        std::cout << "lvalue reference";
    } else if constexpr (std::is_rvalue_reference_v<T>) {
        std::cout << "rvalue reference";
    } else {
        std::cout << "non-reference";
    }
    std::cout << "\n";
}

// Example class for demonstration
class Widget {
private:
    std::string name;
    int id;

public:
    Widget(const std::string& n, int i) : name(n), id(i) {
        std::cout << "Widget(" << name << ", " << id << ") constructed\n";
    }

    Widget(const Widget& other) : name(other.name), id(other.id) {
        std::cout << "Widget copied: " << name << "\n";
    }

    Widget(Widget&& other) noexcept : name(std::move(other.name)), id(other.id) {
        std::cout << "Widget moved: " << name << "\n";
    }

    void display() const {
        std::cout << "Widget[" << id << "]: " << name << "\n";
    }
};

// ==============================================
// 1. Universal Reference Basics
// ==============================================

// This is a universal/forwarding reference (T&&)
template<typename T>
void universalReference(T&& param) {
    std::cout << "\n--- Universal Reference ---\n";
    printValueCategory<T>();

    // param itself is always an lvalue (it has a name)
    // but T encodes whether the argument was lvalue or rvalue
}

// This is an rvalue reference (not universal) - Widget is concrete type
void rvalueReference(Widget&& param) {
    std::cout << "\n--- Rvalue Reference (non-universal) ---\n";
    std::cout << "Only binds to rvalues\n";
}

// ==============================================
// 2. Perfect Forwarding Pattern
// ==============================================

// Function overloads to show what gets called
void process(const Widget& w) {
    std::cout << "process(const Widget&) - lvalue overload\n";
}

void process(Widget&& w) {
    std::cout << "process(Widget&&) - rvalue overload\n";
}

// Perfect forwarding wrapper
template<typename T>
void forwardWrapper(T&& arg) {
    std::cout << "\nForwarding wrapper called:\n";
    printValueCategory<T>();

    // Without std::forward: always calls lvalue overload
    // process(arg); // arg is lvalue (has a name)

    // With std::forward: preserves value category
    process(std::forward<T>(arg));
}

// ==============================================
// 3. Variadic Template Perfect Forwarding
// ==============================================

template<typename... Args>
void variadicForward(Args&&... args) {
    std::cout << "\n--- Variadic Perfect Forwarding ---\n";
    std::cout << "Number of arguments: " << sizeof...(args) << "\n";

    // Forward all arguments
    (process(std::forward<Args>(args)), ...); // C++17 fold expression
}

// ==============================================
// 4. Factory Function with Perfect Forwarding
// ==============================================

template<typename T, typename... Args>
std::unique_ptr<T> createUnique(Args&&... args) {
    std::cout << "\nFactory creating object...\n";
    return std::make_unique<T>(std::forward<Args>(args)...);
}

// Emplace-like function
template<typename T>
class Container {
private:
    std::vector<T> items;

public:
    // Perfect forwarding in member function template
    template<typename... Args>
    void emplace_back(Args&&... args) {
        std::cout << "\nEmplacing item in container...\n";
        items.emplace_back(std::forward<Args>(args)...);
    }

    template<typename U>
    void push_back(U&& item) {
        std::cout << "\nPushing item to container...\n";
        printValueCategory<U>();
        items.push_back(std::forward<U>(item));
    }

    void display() const {
        std::cout << "\nContainer contents:\n";
        for (const auto& item : items) {
            item.display();
        }
    }
};

// ==============================================
// 5. Reference Collapsing Rules
// ==============================================

void demonstrateReferenceCollapsing() {
    std::cout << "\n=== Reference Collapsing Rules ===\n";
    std::cout << "T& & → T&\n";
    std::cout << "T& && → T&\n";
    std::cout << "T&& & → T&\n";
    std::cout << "T&& && → T&&\n";
    std::cout << "\nIn templates, T&& + collapsing = universal reference\n";

    int x = 10;

    // When passing lvalue: T deduced as int&
    // int& && collapses to int&
    universalReference(x);

    // When passing rvalue: T deduced as int
    // int&& stays as int&&
    universalReference(10);
    universalReference(std::move(x));
}

// ==============================================
// 6. Common Pitfalls
// ==============================================

// Pitfall 1: Using std::move instead of std::forward
template<typename T>
void incorrectForward(T&& arg) {
    std::cout << "\n--- Incorrect: Using move ---\n";
    process(std::move(arg)); // Always calls rvalue overload!
}

// Pitfall 2: Not forwarding at all
template<typename T>
void noForward(T&& arg) {
    std::cout << "\n--- Incorrect: Not forwarding ---\n";
    process(arg); // Always calls lvalue overload!
}

// Pitfall 3: Forwarding multiple times
template<typename T>
void multipleForward(T&& arg) {
    std::cout << "\n--- Dangerous: Multiple forwards ---\n";
    process(std::forward<T>(arg));
    // process(std::forward<T>(arg)); // Dangerous if T is rvalue!
    std::cout << "Can only safely forward once!\n";
}

// ==============================================
// 7. Auto&& - Forwarding Reference
// ==============================================

void autoForwardingReference() {
    std::cout << "\n=== Auto&& as Forwarding Reference ===\n";

    Widget w1("AutoLvalue", 1);
    auto&& ref1 = w1; // lvalue → auto deduced as Widget&

    auto&& ref2 = Widget("AutoRvalue", 2); // rvalue → auto deduced as Widget

    std::cout << "ref1 binds to lvalue\n";
    ref1.display();

    std::cout << "ref2 binds to rvalue\n";
    ref2.display();
}

// ==============================================
// 8. Lambda and Perfect Forwarding (C++14)
// ==============================================

void lambdaForwarding() {
    std::cout << "\n=== Lambda Perfect Forwarding ===\n";

    // Generic lambda with forwarding
    auto forwarder = [](auto&& arg) {
        std::cout << "Lambda forwarding:\n";
        return process(std::forward<decltype(arg)>(arg));
    };

    Widget w("LambdaTest", 1);
    forwarder(w);
    forwarder(Widget("Temporary", 2));
}

// ==============================================
// 9. Const and Forwarding
// ==============================================

template<typename T>
void constForwarding(T&& arg) {
    std::cout << "\n--- Const Forwarding ---\n";
    std::cout << "Is const: " << std::is_const_v<std::remove_reference_t<T>> << "\n";
    std::cout << "Is lvalue ref: " << std::is_lvalue_reference_v<T> << "\n";
    std::cout << "Is rvalue ref: " << std::is_rvalue_reference_v<T> << "\n";
}

// ==============================================
// 10. Real-World Example: Thread Creation
// ==============================================

template<typename Func, typename... Args>
void threadWrapper(Func&& func, Args&&... args) {
    std::cout << "\n--- Thread Wrapper Example ---\n";
    std::cout << "Would create thread with perfect forwarding:\n";
    // In real code: std::thread t(std::forward<Func>(func), std::forward<Args>(args)...);

    // For demo, just call directly
    std::forward<Func>(func)(std::forward<Args>(args)...);
}

int main() {
    std::cout << "=== Perfect Forwarding and Universal References ===\n";

    // 1. Universal reference basics
    std::cout << "\n=== 1. Universal Reference Basics ===\n";
    Widget w1("Test1", 1);
    universalReference(w1);                    // T = Widget&
    universalReference(Widget("Temp", 2));     // T = Widget
    universalReference(std::move(w1));         // T = Widget

    // 2. Perfect forwarding
    std::cout << "\n=== 2. Perfect Forwarding Pattern ===\n";
    Widget w2("Test2", 2);
    forwardWrapper(w2);                        // Calls lvalue overload
    forwardWrapper(Widget("Temp2", 3));        // Calls rvalue overload

    // 3. Variadic forwarding
    std::cout << "\n=== 3. Variadic Perfect Forwarding ===\n";
    Widget w3("Test3", 3);
    Widget w4("Test4", 4);
    variadicForward(w3, Widget("Temp3", 5), std::move(w4));

    // 4. Factory pattern
    std::cout << "\n=== 4. Factory Pattern ===\n";
    auto ptr = createUnique<Widget>("Factory", 10);
    ptr->display();

    // 5. Container with perfect forwarding
    std::cout << "\n=== 5. Container Emplace ===\n";
    Container<Widget> container;
    Widget w5("ContainerItem", 5);
    container.push_back(w5);                   // lvalue
    container.push_back(Widget("TempItem", 6)); // rvalue
    container.emplace_back("EmplacedItem", 7); // construct in place
    container.display();

    // 6. Reference collapsing
    demonstrateReferenceCollapsing();

    // 7. Common pitfalls
    std::cout << "\n=== 6. Common Pitfalls ===\n";
    Widget w6("Pitfall", 6);
    incorrectForward(w6);
    noForward(Widget("NoForward", 7));

    // 8. Auto&&
    autoForwardingReference();

    // 9. Lambda forwarding
    lambdaForwarding();

    // 10. Const forwarding
    std::cout << "\n=== 9. Const Forwarding ===\n";
    const Widget w7("Const", 7);
    constForwarding(w7);
    constForwarding(Widget("NonConst", 8));

    // 11. Thread wrapper example
    auto task = [](const std::string& msg) {
        std::cout << "Task executing: " << msg << "\n";
    };
    threadWrapper(task, "Hello from thread wrapper");

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. T&& in template = universal/forwarding reference\n";
    std::cout << "2. Use std::forward<T> to preserve value category\n";
    std::cout << "3. Reference collapsing makes universal refs work\n";
    std::cout << "4. auto&& is also a forwarding reference\n";
    std::cout << "5. Only forward once - moving from forwarded value is dangerous\n";
    std::cout << "6. Perfect forwarding enables zero-overhead wrappers\n";

    return 0;
}
