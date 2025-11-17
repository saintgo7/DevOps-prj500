/*
 * Program 172: consteval and constinit - C++20 Constant Features
 *
 * This program demonstrates:
 * - consteval for immediate functions (compile-time only)
 * - constinit for constant initialization
 * - Differences between constexpr, consteval, and constinit
 * - Use cases and best practices
 *
 * Note: Requires C++20 compiler support
 * Compile with: g++ -std=c++20
 */

#include <iostream>
#include <array>
#include <string_view>

// ==============================================
// 1. consteval - Immediate Functions
// ==============================================

// consteval: MUST be evaluated at compile-time
consteval int square(int x) {
    return x * x;
}

consteval int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

void constevalBasicsDemo() {
    std::cout << "\n=== 1. consteval Basics ===\n";

    // Must be compile-time constant
    constexpr int result1 = square(5);
    constexpr int result2 = factorial(5);

    std::cout << "square(5) = " << result1 << "\n";
    std::cout << "factorial(5) = " << result2 << "\n";

    // This would be an error:
    // int x = 5;
    // int result = square(x); // ERROR: x is not a constant expression

    std::cout << "consteval functions are ALWAYS evaluated at compile-time\n";
}

// ==============================================
// 2. constexpr vs consteval
// ==============================================

constexpr int constexpr_func(int x) {
    return x * 2; // Can run at compile-time OR runtime
}

consteval int consteval_func(int x) {
    return x * 2; // MUST run at compile-time
}

void constexprVsConstevalDemo() {
    std::cout << "\n=== 2. constexpr vs consteval ===\n";

    // Both work with compile-time constants
    constexpr int ce_result = constexpr_func(10);
    constexpr int cv_result = consteval_func(10);

    std::cout << "constexpr_func(10) = " << ce_result << "\n";
    std::cout << "consteval_func(10) = " << cv_result << "\n";

    // constexpr can also run at runtime
    int runtime_val = 20;
    int runtime_result = constexpr_func(runtime_val);
    std::cout << "constexpr_func(runtime) = " << runtime_result << "\n";

    // consteval CANNOT run at runtime
    // int invalid = consteval_func(runtime_val); // ERROR!

    std::cout << "\nconstexpr: compile-time OR runtime\n";
    std::cout << "consteval: compile-time ONLY\n";
}

// ==============================================
// 3. consteval Use Cases
// ==============================================

// Compile-time validation
consteval bool isValidPort(int port) {
    return port >= 1024 && port <= 65535;
}

consteval int validatePort(int port) {
    if (!isValidPort(port)) {
        // This will cause a compile-time error if port is invalid
        throw "Invalid port number";
    }
    return port;
}

// Compile-time string validation
consteval bool isValidEmail(std::string_view email) {
    return email.find('@') != std::string_view::npos;
}

void constevalUseCasesDemo() {
    std::cout << "\n=== 3. consteval Use Cases ===\n";

    // Valid port - compiles fine
    constexpr int port1 = validatePort(8080);
    std::cout << "Valid port: " << port1 << "\n";

    // This would cause compile error:
    // constexpr int port2 = validatePort(80); // Too low!
    // constexpr int port3 = validatePort(99999); // Too high!

    // Email validation
    constexpr bool valid = isValidEmail("user@example.com");
    constexpr bool invalid = isValidEmail("not-an-email");

    std::cout << "Email validation (compile-time):\n";
    std::cout << "  'user@example.com': " << std::boolalpha << valid << "\n";
    std::cout << "  'not-an-email': " << invalid << "\n";

    std::cout << "\nconsteval provides compile-time guarantees!\n";
}

// ==============================================
// 4. constinit - Constant Initialization
// ==============================================

// constinit ensures static initialization (before main)
constinit int global_counter = 42;

// With constexpr for constant value
constexpr int compute_initial_value() {
    return 100;
}

constinit int initialized_global = compute_initial_value();

// constinit can be modified at runtime (unlike constexpr)
void modify_constinit() {
    global_counter = 100; // OK - constinit allows modification
    initialized_global = 200; // OK
}

void constinitBasicsDemo() {
    std::cout << "\n=== 4. constinit Basics ===\n";

    std::cout << "Before modification:\n";
    std::cout << "  global_counter = " << global_counter << "\n";
    std::cout << "  initialized_global = " << initialized_global << "\n";

    modify_constinit();

    std::cout << "After modification:\n";
    std::cout << "  global_counter = " << global_counter << "\n";
    std::cout << "  initialized_global = " << initialized_global << "\n";

    std::cout << "\nconstinit ensures static initialization,\n";
    std::cout << "but allows runtime modification\n";
}

// ==============================================
// 5. Static Initialization Order Fiasco Solution
// ==============================================

// Problem: Global initialization order is undefined across translation units
// Solution: Use constinit to ensure static initialization

constinit int config_value = 42;

constexpr int get_config() {
    return config_value;
}

// This is guaranteed to be initialized at compile-time
constinit int derived_value = get_config() * 2;

void initOrderDemo() {
    std::cout << "\n=== 5. Static Initialization Order ===\n";

    std::cout << "config_value = " << config_value << "\n";
    std::cout << "derived_value = " << derived_value << "\n";

    std::cout << "\nconstinit prevents static initialization order fiasco\n";
    std::cout << "Guarantees initialization before dynamic initialization\n";
}

// ==============================================
// 6. constexpr vs constinit vs consteval
// ==============================================

void comparisonDemo() {
    std::cout << "\n=== 6. Comparison: constexpr vs constinit vs consteval ===\n\n";

    std::cout << "constexpr:\n";
    std::cout << "  - Variables: Immutable, compile-time constant\n";
    std::cout << "  - Functions: Can run at compile-time or runtime\n";
    std::cout << "  - Implies const for variables\n\n";

    std::cout << "consteval (C++20):\n";
    std::cout << "  - Functions only\n";
    std::cout << "  - MUST run at compile-time (immediate function)\n";
    std::cout << "  - Produces compile error if used with runtime values\n\n";

    std::cout << "constinit (C++20):\n";
    std::cout << "  - Variables only\n";
    std::cout << "  - Ensures static initialization\n";
    std::cout << "  - Does NOT imply const (can be modified)\n";
    std::cout << "  - Prevents dynamic initialization\n\n";
}

// ==============================================
// 7. consteval for Type Checking
// ==============================================

template<typename T>
consteval bool isIntegral() {
    return std::is_integral_v<T>;
}

template<typename T>
consteval void requireIntegral() {
    if (!isIntegral<T>()) {
        throw "Type must be integral";
    }
}

template<typename T>
void processValue(T value) {
    requireIntegral<T>(); // Compile-time type check
    std::cout << "Processing integral value: " << value << "\n";
}

void typeCheckingDemo() {
    std::cout << "\n=== 7. consteval for Type Checking ===\n";

    processValue(42);        // OK: int is integral
    processValue(100L);      // OK: long is integral

    // This would cause compile error:
    // processValue(3.14);   // ERROR: double is not integral
    // processValue("text"); // ERROR: const char* is not integral

    std::cout << "consteval enables compile-time type validation\n";
}

// ==============================================
// 8. consteval Lookup Tables
// ==============================================

consteval std::array<int, 10> createPowersOf2() {
    std::array<int, 10> result{};
    for (size_t i = 0; i < result.size(); ++i) {
        result[i] = 1 << i; // 2^i
    }
    return result;
}

void lookupTablesDemo() {
    std::cout << "\n=== 8. consteval Lookup Tables ===\n";

    constexpr auto powers = createPowersOf2();

    std::cout << "Powers of 2 (compile-time generated):\n";
    for (size_t i = 0; i < powers.size(); ++i) {
        std::cout << "  2^" << i << " = " << powers[i] << "\n";
    }
}

// ==============================================
// 9. constinit with Thread-Local Storage
// ==============================================

// Thread-local storage with constinit
constinit thread_local int thread_counter = 0;

void incrementThreadCounter() {
    ++thread_counter;
}

void threadLocalDemo() {
    std::cout << "\n=== 9. constinit with Thread-Local ===\n";

    std::cout << "Initial thread_counter: " << thread_counter << "\n";

    incrementThreadCounter();
    incrementThreadCounter();

    std::cout << "After increment: " << thread_counter << "\n";

    std::cout << "\nconstinit works with thread_local storage\n";
}

// ==============================================
// 10. Practical Example: Configuration Validation
// ==============================================

struct Config {
    int max_connections;
    int timeout_ms;
    int buffer_size;
};

consteval Config validateConfig(Config cfg) {
    if (cfg.max_connections <= 0 || cfg.max_connections > 10000) {
        throw "Invalid max_connections";
    }
    if (cfg.timeout_ms <= 0 || cfg.timeout_ms > 60000) {
        throw "Invalid timeout";
    }
    if (cfg.buffer_size < 1024 || cfg.buffer_size > 1048576) {
        throw "Invalid buffer_size";
    }
    return cfg;
}

constinit Config app_config = validateConfig({
    .max_connections = 100,
    .timeout_ms = 5000,
    .buffer_size = 8192
});

void configValidationDemo() {
    std::cout << "\n=== 10. Configuration Validation ===\n";

    std::cout << "Application configuration (validated at compile-time):\n";
    std::cout << "  max_connections: " << app_config.max_connections << "\n";
    std::cout << "  timeout_ms: " << app_config.timeout_ms << "\n";
    std::cout << "  buffer_size: " << app_config.buffer_size << "\n";

    // Can modify at runtime
    app_config.timeout_ms = 10000;
    std::cout << "\nAfter runtime modification:\n";
    std::cout << "  timeout_ms: " << app_config.timeout_ms << "\n";

    std::cout << "\nInvalid configs would cause compile errors!\n";
}

// ==============================================
// 11. consteval for Compile-Time Assertions
// ==============================================

consteval int requirePositive(int x) {
    if (x <= 0) {
        throw "Value must be positive";
    }
    return x;
}

consteval int requireInRange(int x, int min, int max) {
    if (x < min || x > max) {
        throw "Value out of range";
    }
    return x;
}

void compileTimeAssertionsDemo() {
    std::cout << "\n=== 11. Compile-Time Assertions ===\n";

    constexpr int positive_val = requirePositive(42);
    constexpr int range_val = requireInRange(50, 0, 100);

    std::cout << "Validated positive value: " << positive_val << "\n";
    std::cout << "Validated range value: " << range_val << "\n";

    // These would cause compile errors:
    // constexpr int invalid1 = requirePositive(-5);
    // constexpr int invalid2 = requireInRange(150, 0, 100);

    std::cout << "Invalid values caught at compile-time!\n";
}

// ==============================================
// 12. Best Practices
// ==============================================

void bestPracticesDemo() {
    std::cout << "\n=== 12. Best Practices ===\n\n";

    std::cout << "Use consteval when:\n";
    std::cout << "  - Function MUST run at compile-time\n";
    std::cout << "  - Compile-time validation needed\n";
    std::cout << "  - Generating lookup tables\n";
    std::cout << "  - Type checking at compile-time\n\n";

    std::cout << "Use constinit when:\n";
    std::cout << "  - Global/static variable initialization\n";
    std::cout << "  - Avoiding static initialization order fiasco\n";
    std::cout << "  - Thread-local storage\n";
    std::cout << "  - Need runtime modification\n\n";

    std::cout << "Use constexpr when:\n";
    std::cout << "  - Want flexibility (compile-time OR runtime)\n";
    std::cout << "  - Creating immutable constants\n";
    std::cout << "  - Most general-purpose use\n\n";
}

int main() {
    std::cout << "=== C++20 consteval and constinit ===\n";

    // 1. consteval basics
    constevalBasicsDemo();

    // 2. constexpr vs consteval
    constexprVsConstevalDemo();

    // 3. consteval use cases
    constevalUseCasesDemo();

    // 4. constinit basics
    constinitBasicsDemo();

    // 5. Initialization order
    initOrderDemo();

    // 6. Comparison
    comparisonDemo();

    // 7. Type checking
    typeCheckingDemo();

    // 8. Lookup tables
    lookupTablesDemo();

    // 9. Thread-local
    threadLocalDemo();

    // 10. Config validation
    configValidationDemo();

    // 11. Compile-time assertions
    compileTimeAssertionsDemo();

    // 12. Best practices
    bestPracticesDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. consteval: immediate functions (compile-time only)\n";
    std::cout << "2. constinit: ensures static initialization\n";
    std::cout << "3. consteval provides stronger guarantees than constexpr\n";
    std::cout << "4. constinit allows runtime modification (unlike constexpr)\n";
    std::cout << "5. Use consteval for validation and type checking\n";
    std::cout << "6. Use constinit to prevent initialization order issues\n";
    std::cout << "7. C++20 features for safer, more efficient code\n";

    return 0;
}
