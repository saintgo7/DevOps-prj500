/*
 * Program 105: Loops in C++
 *
 * Topics Covered:
 * - for loop (traditional)
 * - Range-based for loop (C++11)
 * - while loop
 * - do-while loop
 * - Nested loops
 * - break statement
 * - continue statement
 * - Infinite loops
 * - Loop control best practices
 * - Common loop patterns
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o loops main.cpp
 */

#include <iostream>
#include <vector>
#include <string>
#include <array>

void demonstrateForLoop();
void demonstrateRangeBasedFor();
void demonstrateWhileLoop();
void demonstrateDoWhileLoop();
void demonstrateNestedLoops();
void demonstrateBreakContinue();
void demonstrateInfiniteLoops();
void demonstrateCommonPatterns();

int main() {
    std::cout << "=== C++ Loops ===" << std::endl;
    std::cout << std::endl;

    // ============================================================
    // 1. Traditional for Loop
    // ============================================================

    demonstrateForLoop();

    // ============================================================
    // 2. Range-Based for Loop (C++11)
    // ============================================================

    demonstrateRangeBasedFor();

    // ============================================================
    // 3. while Loop
    // ============================================================

    demonstrateWhileLoop();

    // ============================================================
    // 4. do-while Loop
    // ============================================================

    demonstrateDoWhileLoop();

    // ============================================================
    // 5. Nested Loops
    // ============================================================

    demonstrateNestedLoops();

    // ============================================================
    // 6. break and continue
    // ============================================================

    demonstrateBreakContinue();

    // ============================================================
    // 7. Infinite Loops
    // ============================================================

    demonstrateInfiniteLoops();

    // ============================================================
    // 8. Common Loop Patterns
    // ============================================================

    demonstrateCommonPatterns();

    return 0;
}

/**
 * Demonstrates traditional for loop
 */
void demonstrateForLoop() {
    std::cout << "--- Traditional for Loop ---" << std::endl;

    // Basic for loop
    std::cout << "Counting 1 to 5: ";
    for (int i = 1; i <= 5; i++) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // Counting backwards
    std::cout << "Countdown: ";
    for (int i = 5; i >= 1; i--) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // Step by 2
    std::cout << "Even numbers 0-10: ";
    for (int i = 0; i <= 10; i += 2) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // Multiple variables in for loop
    std::cout << "Multiple variables: ";
    for (int i = 0, j = 10; i < 5; i++, j--) {
        std::cout << "i=" << i << ",j=" << j << " ";
    }
    std::cout << std::endl;

    // Iterating through array
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    std::cout << "Array elements: ";
    for (int i = 0; i < size; i++) {
        std::cout << numbers[i] << " ";
    }
    std::cout << std::endl;

    // For loop with C++17 init statement
    std::cout << "For loop with init (C++17): ";
    for (auto size = 5; int i = 0; i < size; i++) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates range-based for loop (C++11)
 */
void demonstrateRangeBasedFor() {
    std::cout << "--- Range-Based for Loop (C++11) ---" << std::endl;

    // Array
    int numbers[] = {1, 2, 3, 4, 5};
    std::cout << "Array: ";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // std::vector
    std::vector<std::string> fruits = {"Apple", "Banana", "Cherry", "Date"};
    std::cout << "Vector: ";
    for (const std::string& fruit : fruits) {
        std::cout << fruit << " ";
    }
    std::cout << std::endl;

    // Using auto
    std::cout << "Using auto: ";
    for (auto fruit : fruits) {
        std::cout << fruit << " ";
    }
    std::cout << std::endl;

    // Modifying elements (reference)
    std::vector<int> values = {1, 2, 3, 4, 5};
    std::cout << "Before modification: ";
    for (int val : values) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    // Double each value
    for (int& val : values) {
        val *= 2;
    }

    std::cout << "After modification: ";
    for (int val : values) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    // const auto& for efficiency (no copying)
    std::vector<std::string> longStrings = {"Hello", "World", "C++", "Programming"};
    std::cout << "Using const auto&: ";
    for (const auto& str : longStrings) {
        std::cout << str << " ";
    }
    std::cout << std::endl;

    // C++20: Range-based for with init statement
    std::cout << "Range-for with init (C++20): ";
    for (auto vec = std::vector{1, 2, 3}; auto val : vec) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates while loop
 */
void demonstrateWhileLoop() {
    std::cout << "--- while Loop ---" << std::endl;

    // Basic while loop
    int count = 1;
    std::cout << "Counting with while: ";
    while (count <= 5) {
        std::cout << count << " ";
        count++;
    }
    std::cout << std::endl;

    // Finding first power of 2 greater than 100
    int power = 1;
    while (power <= 100) {
        power *= 2;
    }
    std::cout << "First power of 2 > 100: " << power << std::endl;

    // Processing with condition
    int sum = 0;
    int n = 1;
    while (sum < 50) {
        sum += n;
        n++;
    }
    std::cout << "Sum when reaching 50: " << sum << " (added " << (n-1) << " numbers)" << std::endl;

    // Reading until sentinel value
    std::cout << "Reading numbers (conceptual): ";
    std::vector<int> data = {5, 10, 15, -1, 20};  // -1 is sentinel
    int index = 0;
    while (index < data.size() && data[index] != -1) {
        std::cout << data[index] << " ";
        index++;
    }
    std::cout << "(stopped at sentinel)" << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates do-while loop
 */
void demonstrateDoWhileLoop() {
    std::cout << "--- do-while Loop ---" << std::endl;

    // Basic do-while (executes at least once)
    int count = 1;
    std::cout << "Counting with do-while: ";
    do {
        std::cout << count << " ";
        count++;
    } while (count <= 5);
    std::cout << std::endl;

    // Executes even when condition is initially false
    std::cout << "Executes at least once: ";
    int x = 10;
    do {
        std::cout << x << " ";
        x++;
    } while (x < 5);  // False from the start, but still executes once
    std::cout << std::endl;

    // Menu-driven program pattern
    std::cout << "\n--- Menu Example (Simulated) ---" << std::endl;
    int choice;
    int iteration = 0;
    do {
        // Simulate user input
        iteration++;
        choice = (iteration == 1) ? 1 : (iteration == 2) ? 2 : 3;

        std::cout << "Menu: 1-Option A, 2-Option B, 3-Exit" << std::endl;
        std::cout << "Choice: " << choice << std::endl;

        switch (choice) {
            case 1:
                std::cout << "  You selected Option A" << std::endl;
                break;
            case 2:
                std::cout << "  You selected Option B" << std::endl;
                break;
            case 3:
                std::cout << "  Exiting..." << std::endl;
                break;
            default:
                std::cout << "  Invalid choice" << std::endl;
        }
    } while (choice != 3);

    std::cout << std::endl;
}

/**
 * Demonstrates nested loops
 */
void demonstrateNestedLoops() {
    std::cout << "--- Nested Loops ---" << std::endl;

    // Multiplication table
    std::cout << "Multiplication Table (5x5):" << std::endl;
    for (int i = 1; i <= 5; i++) {
        for (int j = 1; j <= 5; j++) {
            std::cout << (i * j) << "\t";
        }
        std::cout << std::endl;
    }

    // Pattern printing - right triangle
    std::cout << "\nRight Triangle Pattern:" << std::endl;
    for (int i = 1; i <= 5; i++) {
        for (int j = 1; j <= i; j++) {
            std::cout << "* ";
        }
        std::cout << std::endl;
    }

    // Pattern printing - pyramid
    std::cout << "\nPyramid Pattern:" << std::endl;
    for (int i = 1; i <= 5; i++) {
        // Print spaces
        for (int j = 1; j <= 5 - i; j++) {
            std::cout << " ";
        }
        // Print stars
        for (int j = 1; j <= 2 * i - 1; j++) {
            std::cout << "*";
        }
        std::cout << std::endl;
    }

    // 2D array traversal
    std::cout << "\n2D Array:" << std::endl;
    int matrix[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates break and continue statements
 */
void demonstrateBreakContinue() {
    std::cout << "--- break and continue ---" << std::endl;

    // break - exits the loop
    std::cout << "Using break (stop at 5): ";
    for (int i = 1; i <= 10; i++) {
        if (i == 6) {
            break;  // Exit loop when i is 6
        }
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // continue - skips current iteration
    std::cout << "Using continue (skip even): ";
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            continue;  // Skip even numbers
        }
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // Finding first occurrence
    std::cout << "\nFinding first occurrence:" << std::endl;
    std::vector<int> numbers = {1, 3, 5, 7, 9, 11, 13};
    int target = 9;

    for (int i = 0; i < numbers.size(); i++) {
        if (numbers[i] == target) {
            std::cout << "Found " << target << " at index " << i << std::endl;
            break;  // Stop searching once found
        }
    }

    // Skipping negative numbers
    std::cout << "\nProcessing only positive numbers:" << std::endl;
    std::vector<int> mixed = {5, -2, 8, -7, 3, -1, 9};
    std::cout << "Positive numbers: ";
    for (int num : mixed) {
        if (num < 0) {
            continue;  // Skip negative numbers
        }
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // break in nested loop (only breaks inner loop)
    std::cout << "\nbreak in nested loop:" << std::endl;
    for (int i = 1; i <= 3; i++) {
        std::cout << "Outer loop i=" << i << ": ";
        for (int j = 1; j <= 5; j++) {
            if (j == 4) {
                break;  // Only breaks inner loop
            }
            std::cout << j << " ";
        }
        std::cout << std::endl;
    }

    std::cout << std::endl;
}

/**
 * Demonstrates infinite loops
 */
void demonstrateInfiniteLoops() {
    std::cout << "--- Infinite Loops (Controlled) ---" << std::endl;

    // Infinite for loop (controlled with break)
    std::cout << "Infinite for with break: ";
    int count = 0;
    for (;;) {  // Infinite loop
        std::cout << count << " ";
        count++;
        if (count >= 5) {
            break;
        }
    }
    std::cout << std::endl;

    // Infinite while loop (controlled with break)
    std::cout << "Infinite while with break: ";
    count = 0;
    while (true) {  // Infinite loop
        std::cout << count << " ";
        count++;
        if (count >= 5) {
            break;
        }
    }
    std::cout << std::endl;

    // Infinite do-while loop
    std::cout << "Infinite do-while with break: ";
    count = 0;
    do {
        std::cout << count << " ";
        count++;
        if (count >= 5) {
            break;
        }
    } while (true);
    std::cout << std::endl;

    std::cout << std::endl;
}

/**
 * Demonstrates common loop patterns
 */
void demonstrateCommonPatterns() {
    std::cout << "--- Common Loop Patterns ---" << std::endl;

    // 1. Summing elements
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int num : numbers) {
        sum += num;
    }
    std::cout << "Sum of elements: " << sum << std::endl;

    // 2. Finding maximum
    int max = numbers[0];
    for (int num : numbers) {
        if (num > max) {
            max = num;
        }
    }
    std::cout << "Maximum element: " << max << std::endl;

    // 3. Finding minimum
    int min = numbers[0];
    for (int num : numbers) {
        if (num < min) {
            min = num;
        }
    }
    std::cout << "Minimum element: " << min << std::endl;

    // 4. Counting occurrences
    std::vector<int> data = {1, 2, 3, 2, 4, 2, 5};
    int target = 2;
    int count = 0;
    for (int num : data) {
        if (num == target) {
            count++;
        }
    }
    std::cout << "Count of " << target << ": " << count << std::endl;

    // 5. Reversing
    std::cout << "Reversed array: ";
    for (int i = numbers.size() - 1; i >= 0; i--) {
        std::cout << numbers[i] << " ";
    }
    std::cout << std::endl;

    // 6. Filtering
    std::cout << "Even numbers: ";
    for (int num : numbers) {
        if (num % 2 == 0) {
            std::cout << num << " ";
        }
    }
    std::cout << std::endl;

    // 7. Transforming
    std::cout << "Squared values: ";
    for (int num : numbers) {
        std::cout << (num * num) << " ";
    }
    std::cout << std::endl;

    // 8. Factorial
    int n = 5;
    long long factorial = 1;
    for (int i = 1; i <= n; i++) {
        factorial *= i;
    }
    std::cout << "Factorial of " << n << ": " << factorial << std::endl;

    // 9. Fibonacci sequence
    std::cout << "Fibonacci (first 10): ";
    int a = 0, b = 1;
    for (int i = 0; i < 10; i++) {
        std::cout << a << " ";
        int temp = a + b;
        a = b;
        b = temp;
    }
    std::cout << std::endl;

    // 10. Prime number check
    int number = 17;
    bool isPrime = true;
    if (number < 2) {
        isPrime = false;
    } else {
        for (int i = 2; i * i <= number; i++) {
            if (number % i == 0) {
                isPrime = false;
                break;
            }
        }
    }
    std::cout << number << " is " << (isPrime ? "prime" : "not prime") << std::endl;

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Prefer range-based for loops when you don't need the index
 * 2. Use const auto& in range-based loops to avoid copying
 * 3. Initialize loop counters where they're declared
 * 4. Avoid modifying loop control variables inside the loop body
 * 5. Use meaningful variable names, not just i, j, k
 * 6. Keep loop bodies short and simple
 * 7. Avoid infinite loops unless intentional (e.g., game loops)
 * 8. Use break and continue judiciously
 * 9. Consider loop invariants for correctness
 * 10. Prefer algorithms from <algorithm> for common operations
 * 11. Be careful with signed/unsigned comparisons in loop conditions
 * 12. Watch out for off-by-one errors
 */
