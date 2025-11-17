/*
 * Program 171: constexpr Functions - Compile-Time Computation
 *
 * This program demonstrates:
 * - constexpr functions for compile-time evaluation
 * - constexpr variables and constants
 * - constexpr algorithms (C++20)
 * - constexpr containers (C++20)
 * - Benefits of compile-time computation
 */

#include <iostream>
#include <array>
#include <algorithm>
#include <numeric>
#include <string_view>
#include <cmath>

// ==============================================
// 1. Basic constexpr Functions
// ==============================================

constexpr int square(int x) {
    return x * x;
}

constexpr int cube(int x) {
    return x * x * x;
}

void basicConstexprDemo() {
    std::cout << "\n=== 1. Basic constexpr Functions ===\n";

    // Evaluated at compile time
    constexpr int result1 = square(5);
    constexpr int result2 = cube(3);

    std::cout << "square(5) = " << result1 << " (compile-time)\n";
    std::cout << "cube(3) = " << result2 << " (compile-time)\n";

    // Can also be used at runtime
    int x = 4;
    int result3 = square(x); // Evaluated at runtime
    std::cout << "square(4) = " << result3 << " (runtime)\n";
}

// ==============================================
// 2. constexpr with Conditionals and Loops
// ==============================================

constexpr int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

constexpr int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

constexpr int sumUpTo(int n) {
    int sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

void constexprControlFlowDemo() {
    std::cout << "\n=== 2. constexpr with Control Flow ===\n";

    constexpr int fact5 = factorial(5);
    constexpr int fib10 = fibonacci(10);
    constexpr int sum100 = sumUpTo(100);

    std::cout << "factorial(5) = " << fact5 << "\n";
    std::cout << "fibonacci(10) = " << fib10 << "\n";
    std::cout << "sum(1..100) = " << sum100 << "\n";
}

// ==============================================
// 3. constexpr Arrays and Containers
// ==============================================

constexpr std::array<int, 5> createArray() {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    return arr;
}

constexpr int arraySum(const std::array<int, 5>& arr) {
    int sum = 0;
    for (int val : arr) {
        sum += val;
    }
    return sum;
}

void constexprArrayDemo() {
    std::cout << "\n=== 3. constexpr Arrays ===\n";

    constexpr auto arr = createArray();
    constexpr int sum = arraySum(arr);

    std::cout << "Array: ";
    for (int val : arr) {
        std::cout << val << " ";
    }
    std::cout << "\n";
    std::cout << "Sum: " << sum << " (compile-time)\n";
}

// ==============================================
// 4. constexpr Classes and Constructors
// ==============================================

class Point {
private:
    int x, y;

public:
    constexpr Point(int x_val, int y_val) : x(x_val), y(y_val) {}

    constexpr int getX() const { return x; }
    constexpr int getY() const { return y; }

    constexpr int distanceSquared() const {
        return x * x + y * y;
    }

    constexpr Point operator+(const Point& other) const {
        return Point(x + other.x, y + other.y);
    }
};

void constexprClassDemo() {
    std::cout << "\n=== 4. constexpr Classes ===\n";

    constexpr Point p1(3, 4);
    constexpr Point p2(1, 2);
    constexpr Point p3 = p1 + p2;

    std::cout << "p1: (" << p1.getX() << ", " << p1.getY() << ")\n";
    std::cout << "p2: (" << p2.getX() << ", " << p2.getY() << ")\n";
    std::cout << "p3 = p1 + p2: (" << p3.getX() << ", " << p3.getY() << ")\n";
    std::cout << "p1.distanceSquared() = " << p1.distanceSquared() << "\n";
}

// ==============================================
// 5. constexpr Algorithms (C++20)
// ==============================================

void constexprAlgorithmsDemo() {
    std::cout << "\n=== 5. constexpr Algorithms (C++20) ===\n";

    constexpr std::array<int, 10> data = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};

    // Find maximum
    constexpr int max_val = *std::max_element(data.begin(), data.end());

    // Count even numbers
    constexpr int even_count = std::count_if(data.begin(), data.end(),
        [](int x) { return x % 2 == 0; });

    // Accumulate sum
    constexpr int sum = std::accumulate(data.begin(), data.end(), 0);

    std::cout << "Data: ";
    for (int val : data) {
        std::cout << val << " ";
    }
    std::cout << "\n";
    std::cout << "Maximum: " << max_val << "\n";
    std::cout << "Even count: " << even_count << "\n";
    std::cout << "Sum: " << sum << "\n";
}

// ==============================================
// 6. Compile-Time String Processing
// ==============================================

constexpr size_t constexprStrlen(const char* str) {
    size_t len = 0;
    while (str[len] != '\0') {
        ++len;
    }
    return len;
}

constexpr bool constexprStrEqual(const char* s1, const char* s2) {
    while (*s1 && *s2) {
        if (*s1 != *s2) return false;
        ++s1;
        ++s2;
    }
    return *s1 == *s2;
}

void constexprStringDemo() {
    std::cout << "\n=== 6. Compile-Time String Processing ===\n";

    constexpr const char* str1 = "Hello";
    constexpr const char* str2 = "World";
    constexpr const char* str3 = "Hello";

    constexpr size_t len1 = constexprStrlen(str1);
    constexpr bool equal1 = constexprStrEqual(str1, str2);
    constexpr bool equal2 = constexprStrEqual(str1, str3);

    std::cout << "Length of '" << str1 << "': " << len1 << "\n";
    std::cout << "'" << str1 << "' == '" << str2 << "': " << std::boolalpha << equal1 << "\n";
    std::cout << "'" << str1 << "' == '" << str3 << "': " << equal2 << "\n";
}

// ==============================================
// 7. constexpr Lookup Tables
// ==============================================

constexpr std::array<int, 256> createSquareTable() {
    std::array<int, 256> table{};
    for (size_t i = 0; i < table.size(); ++i) {
        table[i] = i * i;
    }
    return table;
}

void lookupTableDemo() {
    std::cout << "\n=== 7. Compile-Time Lookup Tables ===\n";

    constexpr auto square_table = createSquareTable();

    std::cout << "Square lookup table (compile-time generated):\n";
    for (int i = 0; i <= 10; ++i) {
        std::cout << i << "^2 = " << square_table[i] << "\n";
    }
}

// ==============================================
// 8. constexpr if (C++17)
// ==============================================

template<typename T>
constexpr auto getValue(T value) {
    if constexpr (std::is_integral_v<T>) {
        return value * 2;
    } else if constexpr (std::is_floating_point_v<T>) {
        return value * 3.14;
    } else {
        return value;
    }
}

void constexprIfDemo() {
    std::cout << "\n=== 8. constexpr if (C++17) ===\n";

    constexpr auto int_result = getValue(10);
    constexpr auto double_result = getValue(2.0);

    std::cout << "getValue(10) = " << int_result << " (integral)\n";
    std::cout << "getValue(2.0) = " << double_result << " (floating-point)\n";
}

// ==============================================
// 9. constexpr Lambda (C++17)
// ==============================================

void constexprLambdaDemo() {
    std::cout << "\n=== 9. constexpr Lambda (C++17) ===\n";

    constexpr auto add = [](int a, int b) constexpr {
        return a + b;
    };

    constexpr auto multiply = [](int a, int b) constexpr {
        return a * b;
    };

    constexpr int sum = add(5, 3);
    constexpr int product = multiply(5, 3);

    std::cout << "add(5, 3) = " << sum << "\n";
    std::cout << "multiply(5, 3) = " << product << "\n";
}

// ==============================================
// 10. Complex Compile-Time Computation
// ==============================================

// Compile-time prime checker
constexpr bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}

// Generate array of first N primes
constexpr std::array<int, 10> generatePrimes() {
    std::array<int, 10> primes{};
    int count = 0;
    int candidate = 2;

    while (count < 10) {
        if (isPrime(candidate)) {
            primes[count++] = candidate;
        }
        ++candidate;
    }

    return primes;
}

// Compile-time GCD
constexpr int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

void complexComputationDemo() {
    std::cout << "\n=== 10. Complex Compile-Time Computation ===\n";

    constexpr auto primes = generatePrimes();

    std::cout << "First 10 primes (compile-time): ";
    for (int prime : primes) {
        std::cout << prime << " ";
    }
    std::cout << "\n";

    constexpr bool is97Prime = isPrime(97);
    constexpr bool is100Prime = isPrime(100);

    std::cout << "isPrime(97) = " << std::boolalpha << is97Prime << "\n";
    std::cout << "isPrime(100) = " << is100Prime << "\n";

    constexpr int gcd_result = gcd(48, 18);
    std::cout << "gcd(48, 18) = " << gcd_result << "\n";
}

// ==============================================
// 11. constexpr Benefits
// ==============================================

void benefitsDemo() {
    std::cout << "\n=== 11. Benefits of constexpr ===\n\n";

    std::cout << "1. Performance:\n";
    std::cout << "   - Computation moved to compile-time\n";
    std::cout << "   - Zero runtime overhead\n\n";

    std::cout << "2. Type Safety:\n";
    std::cout << "   - Compile-time errors for invalid values\n";
    std::cout << "   - Better than macros\n\n";

    std::cout << "3. Optimization:\n";
    std::cout << "   - Compiler can inline and optimize\n";
    std::cout << "   - No function call overhead\n\n";

    std::cout << "4. Flexibility:\n";
    std::cout << "   - Can still use at runtime if needed\n";
    std::cout << "   - Single implementation for both\n\n";

    std::cout << "5. Modern C++:\n";
    std::cout << "   - Replaces many preprocessor macros\n";
    std::cout << "   - More readable and maintainable\n\n";
}

// ==============================================
// 12. constexpr Limitations
// ==============================================

void limitationsDemo() {
    std::cout << "\n=== 12. constexpr Limitations ===\n\n";

    std::cout << "Cannot use in constexpr:\n";
    std::cout << "1. Dynamic memory allocation (new/delete)\n";
    std::cout << "2. Virtual functions (until C++20)\n";
    std::cout << "3. Exceptions (throw/try/catch)\n";
    std::cout << "4. goto statements\n";
    std::cout << "5. Non-constexpr functions\n\n";

    std::cout << "C++20 relaxes some restrictions:\n";
    std::cout << "- Allows dynamic allocation (with deallocation)\n";
    std::cout << "- Allows virtual functions\n";
    std::cout << "- Allows try-catch (not throw)\n";
}

int main() {
    std::cout << "=== C++ constexpr Functions ===\n";

    // 1. Basic constexpr
    basicConstexprDemo();

    // 2. Control flow
    constexprControlFlowDemo();

    // 3. Arrays
    constexprArrayDemo();

    // 4. Classes
    constexprClassDemo();

    // 5. Algorithms
    constexprAlgorithmsDemo();

    // 6. String processing
    constexprStringDemo();

    // 7. Lookup tables
    lookupTableDemo();

    // 8. constexpr if
    constexprIfDemo();

    // 9. Lambda
    constexprLambdaDemo();

    // 10. Complex computation
    complexComputationDemo();

    // 11. Benefits
    benefitsDemo();

    // 12. Limitations
    limitationsDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. constexpr enables compile-time evaluation\n";
    std::cout << "2. Can use loops, conditionals, and recursion\n";
    std::cout << "3. Works with arrays, classes, and algorithms\n";
    std::cout << "4. constexpr if for compile-time branching\n";
    std::cout << "5. Lambdas can be constexpr (C++17)\n";
    std::cout << "6. Great for lookup tables and compile-time checks\n";
    std::cout << "7. C++20 adds more flexibility to constexpr\n";

    return 0;
}
