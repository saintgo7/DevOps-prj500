# Program 105: Loops in C++

## Description
A comprehensive exploration of loop constructs in C++, including traditional for loops, range-based for loops (C++11), while and do-while loops, nested loops, and loop control statements. This program demonstrates various looping patterns and best practices for iterative programming.

## Learning Objectives
- Master traditional `for` loop syntax and variations
- Use range-based `for` loops (C++11) for cleaner iteration
- Understand `while` and `do-while` loop differences
- Implement nested loops for multi-dimensional problems
- Apply `break` and `continue` statements effectively
- Recognize and control infinite loops
- Learn common loop patterns and algorithms
- Understand C++20 range-for enhancements

## Features
- Complete for loop variations (traditional, C++11 range-based, C++17/20 enhancements)
- while and do-while loop demonstrations
- Nested loop examples (multiplication tables, patterns, 2D arrays)
- break and continue statement usage
- Controlled infinite loop examples
- Common loop patterns: summing, finding min/max, searching, sorting
- Practical algorithms: factorial, Fibonacci, prime numbers
- Performance considerations and best practices

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/105_loops
g++ -std=c++20 -Wall -Wextra -o loops main.cpp
```

### Execution
```bash
./loops
```

## Key Concepts

### 1. Traditional for Loop
```cpp
// Basic for loop
for (int i = 1; i <= 5; i++) {
    std::cout << i << " ";
}

// Counting backwards
for (int i = 5; i >= 1; i--) {
    std::cout << i << " ";
}

// Step by 2
for (int i = 0; i <= 10; i += 2) {
    std::cout << i << " ";
}

// Multiple variables
for (int i = 0, j = 10; i < 5; i++, j--) {
    std::cout << "i=" << i << ",j=" << j << " ";
}

// Array iteration
int numbers[] = {10, 20, 30, 40, 50};
int size = sizeof(numbers) / sizeof(numbers[0]);
for (int i = 0; i < size; i++) {
    std::cout << numbers[i] << " ";
}
```

### 2. Range-Based for Loop (C++11)
```cpp
// Array
int numbers[] = {1, 2, 3, 4, 5};
for (int num : numbers) {
    std::cout << num << " ";
}

// Vector with const reference (efficient, no copying)
std::vector<std::string> fruits = {"Apple", "Banana", "Cherry"};
for (const std::string& fruit : fruits) {
    std::cout << fruit << " ";
}

// Using auto
for (auto fruit : fruits) {
    std::cout << fruit << " ";
}

// Modifying elements (use reference)
std::vector<int> values = {1, 2, 3, 4, 5};
for (int& val : values) {
    val *= 2;  // Double each value
}

// const auto& for efficiency (no copying)
for (const auto& str : longStrings) {
    std::cout << str << " ";
}

// C++20: Range-for with init statement
for (auto vec = std::vector{1, 2, 3}; auto val : vec) {
    std::cout << val << " ";
}
```

### 3. while Loop
```cpp
// Basic while loop
int count = 1;
while (count <= 5) {
    std::cout << count << " ";
    count++;
}

// Finding first power of 2 greater than 100
int power = 1;
while (power <= 100) {
    power *= 2;
}

// Processing with condition
int sum = 0, n = 1;
while (sum < 50) {
    sum += n;
    n++;
}

// Reading until sentinel value
std::vector<int> data = {5, 10, 15, -1, 20};  // -1 is sentinel
int index = 0;
while (index < data.size() && data[index] != -1) {
    std::cout << data[index] << " ";
    index++;
}
```

### 4. do-while Loop
```cpp
// Basic do-while (executes at least once)
int count = 1;
do {
    std::cout << count << " ";
    count++;
} while (count <= 5);

// Executes even when condition is initially false
int x = 10;
do {
    std::cout << x << " ";  // Prints 10
    x++;
} while (x < 5);  // False, but body executed once

// Menu-driven program pattern
int choice;
do {
    std::cout << "Menu: 1-Option A, 2-Option B, 3-Exit" << std::endl;
    std::cin >> choice;

    switch (choice) {
        case 1: /* Handle option A */ break;
        case 2: /* Handle option B */ break;
        case 3: std::cout << "Exiting..." << std::endl; break;
    }
} while (choice != 3);
```

### 5. Nested Loops
```cpp
// Multiplication table
for (int i = 1; i <= 5; i++) {
    for (int j = 1; j <= 5; j++) {
        std::cout << (i * j) << "\t";
    }
    std::cout << std::endl;
}

// Right triangle pattern
for (int i = 1; i <= 5; i++) {
    for (int j = 1; j <= i; j++) {
        std::cout << "* ";
    }
    std::cout << std::endl;
}

// 2D array traversal
int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        std::cout << matrix[i][j] << " ";
    }
    std::cout << std::endl;
}
```

### 6. break and continue
```cpp
// break - exits the loop
for (int i = 1; i <= 10; i++) {
    if (i == 6) {
        break;  // Exit loop when i is 6
    }
    std::cout << i << " ";
}  // Output: 1 2 3 4 5

// continue - skips current iteration
for (int i = 1; i <= 10; i++) {
    if (i % 2 == 0) {
        continue;  // Skip even numbers
    }
    std::cout << i << " ";
}  // Output: 1 3 5 7 9

// Finding first occurrence
for (int i = 0; i < numbers.size(); i++) {
    if (numbers[i] == target) {
        std::cout << "Found at index " << i << std::endl;
        break;  // Stop searching once found
    }
}

// break in nested loop (only breaks inner loop)
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 5; j++) {
        if (j == 4) {
            break;  // Only breaks inner loop
        }
        std::cout << j << " ";
    }
    std::cout << std::endl;
}
```

### 7. Infinite Loops
```cpp
// Infinite for loop (controlled with break)
for (;;) {  // or: for(int i = 0; ; i++)
    std::cout << count << " ";
    if (count >= 5) break;
    count++;
}

// Infinite while loop
while (true) {
    std::cout << count << " ";
    if (count >= 5) break;
    count++;
}

// Infinite do-while loop
do {
    std::cout << count << " ";
    if (count >= 5) break;
    count++;
} while (true);

// Game loop pattern
while (true) {
    processInput();
    updateGameState();
    render();
    if (exitRequested) break;
}
```

### 8. Common Loop Patterns
```cpp
// Summing elements
int sum = 0;
for (int num : numbers) {
    sum += num;
}

// Finding maximum
int max = numbers[0];
for (int num : numbers) {
    if (num > max) max = num;
}

// Counting occurrences
int count = 0;
for (int num : data) {
    if (num == target) count++;
}

// Reversing
for (int i = numbers.size() - 1; i >= 0; i--) {
    std::cout << numbers[i] << " ";
}

// Filtering (even numbers)
for (int num : numbers) {
    if (num % 2 == 0) {
        std::cout << num << " ";
    }
}

// Transforming (squaring)
for (int num : numbers) {
    std::cout << (num * num) << " ";
}

// Factorial
long long factorial = 1;
for (int i = 1; i <= n; i++) {
    factorial *= i;
}

// Fibonacci sequence
int a = 0, b = 1;
for (int i = 0; i < 10; i++) {
    std::cout << a << " ";
    int temp = a + b;
    a = b;
    b = temp;
}

// Prime number check
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
```

## Best Practices
1. **Prefer range-based for loops** when you don't need the index
2. **Use `const auto&`** in range-based loops to avoid copying
3. **Initialize loop counters** where they're declared
4. **Avoid modifying loop control variables** inside the loop body
5. **Use meaningful variable names**, not just i, j, k (except for simple iteration)
6. **Keep loop bodies short and simple** - extract complex logic to functions
7. **Avoid infinite loops** unless intentional (e.g., game loops, servers)
8. **Use break and continue judiciously** - don't abuse them
9. **Consider loop invariants** for correctness
10. **Prefer STL algorithms** from `<algorithm>` for common operations
11. **Be careful with signed/unsigned comparisons** in loop conditions
12. **Watch out for off-by-one errors** (< vs <=, array bounds)

## Resources and References
- [cppreference.com - for loop](https://en.cppreference.com/w/cpp/language/for)
- [cppreference.com - range-for](https://en.cppreference.com/w/cpp/language/range-for)
- [cppreference.com - while loop](https://en.cppreference.com/w/cpp/language/while)
- [cppreference.com - do-while loop](https://en.cppreference.com/w/cpp/language/do)
- [C++ Core Guidelines - Loops](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-for-range)

## Navigation
- **Previous Program**: [104 - Control Flow](../104_control_flow/README.md)
- **Next Program**: [106 - Functions](../106_functions/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
