# Program 120: Standard I/O in C++

## Description
Comprehensive exploration of standard input/output in C++ covering cin, cout, cerr, clog, formatting, manipulators, string streams, and I/O best practices. This program demonstrates console I/O operations and stream manipulation techniques.

## Learning Objectives
- Master console input with cin
- Use cout for formatted output
- Understand error streams (cerr, clog)
- Apply I/O manipulators
- Format numbers and text
- Work with string streams
- Handle I/O errors
- Use modern formatting (C++20)

## Features
- Console input/output operations
- Stream manipulators and formatting
- Error and log streams
- Input validation
- String streams for parsing
- Custom I/O manipulators
- Format library (C++20)

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/120_standard_io
g++ -std=c++20 -Wall -Wextra -o standard_io main.cpp
```

### Execution
```bash
./standard_io
```

## Key Concepts

### 1. Basic Output (cout)
```cpp
#include <iostream>

// Basic output
std::cout << "Hello, World!" << std::endl;
std::cout << "Value: " << 42 << '\n';

// Chaining output
std::cout << "Name: " << "John" << ", Age: " << 25 << '\n';

// endl vs '\n'
std::cout << "With endl" << std::endl;  // Flushes buffer
std::cout << "With newline\n";          // No flush (faster)

// Flush explicitly
std::cout << "Text" << std::flush;
```

### 2. Basic Input (cin)
```cpp
// Read single value
int age;
std::cout << "Enter age: ";
std::cin >> age;

// Read multiple values
std::string name;
int score;
std::cout << "Enter name and score: ";
std::cin >> name >> score;

// Read line
std::string fullName;
std::cout << "Enter full name: ";
std::getline(std::cin, fullName);

// Clear input buffer
std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
```

### 3. Error and Log Streams
```cpp
// cerr - unbuffered error stream
std::cerr << "Error: File not found\n";

// clog - buffered log stream
std::clog << "Log: Operation completed\n";

// Usage patterns
void processFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file) {
        std::cerr << "ERROR: Cannot open " << filename << '\n';
        return;
    }
    std::clog << "INFO: Processing " << filename << '\n';
    // Process file...
}
```

### 4. Format Manipulators
```cpp
#include <iomanip>

// Width and alignment
std::cout << std::setw(10) << "Name" << std::setw(10) << "Age" << '\n';
std::cout << std::setw(10) << "Alice" << std::setw(10) << 25 << '\n';

// Alignment
std::cout << std::left << std::setw(10) << "Left" << '\n';
std::cout << std::right << std::setw(10) << "Right" << '\n';

// Fill character
std::cout << std::setfill('*') << std::setw(20) << "Centered" << '\n';
std::cout << std::setfill(' ');  // Reset

// Precision (floating-point)
double pi = 3.14159265359;
std::cout << std::setprecision(3) << pi << '\n';  // 3.14
std::cout << std::fixed << std::setprecision(2) << pi << '\n';  // 3.14
std::cout << std::scientific << pi << '\n';  // 3.14e+00

// Number bases
int num = 255;
std::cout << "Dec: " << std::dec << num << '\n';
std::cout << "Hex: " << std::hex << num << '\n';
std::cout << "Oct: " << std::oct << num << '\n';
std::cout << std::dec;  // Reset to decimal

// Show base prefix
std::cout << std::showbase << std::hex << num << '\n';  // 0xff
std::cout << std::noshowbase;

// Boolean values
bool flag = true;
std::cout << flag << '\n';  // 1
std::cout << std::boolalpha << flag << '\n';  // true
std::cout << std::noboolalpha;
```

### 5. Input Validation
```cpp
int getValidInteger() {
    int value;
    while (true) {
        std::cout << "Enter integer: ";
        std::cin >> value;

        if (std::cin.fail()) {
            std::cin.clear();  // Clear error flags
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cerr << "Invalid input. Try again.\n";
        } else {
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            return value;
        }
    }
}

// Range validation
int getIntegerInRange(int min, int max) {
    int value;
    while (true) {
        value = getValidInteger();
        if (value >= min && value <= max) {
            return value;
        }
        std::cerr << "Value must be between " << min
                  << " and " << max << '\n';
    }
}
```

### 6. String Streams
```cpp
#include <sstream>

// Output string stream
std::ostringstream oss;
oss << "Value: " << 42 << ", Pi: " << 3.14;
std::string result = oss.str();

// Input string stream
std::istringstream iss("10 20 30");
int a, b, c;
iss >> a >> b >> c;

// Parsing CSV
std::string csvLine = "Alice,25,Engineer";
std::istringstream csvStream(csvLine);
std::string name, job;
int age;

std::getline(csvStream, name, ',');
csvStream >> age;
csvStream.ignore();  // Skip comma
std::getline(csvStream, job);

// String stream for conversions
template<typename T>
std::string toString(const T& value) {
    std::ostringstream oss;
    oss << value;
    return oss.str();
}

template<typename T>
T fromString(const std::string& str) {
    std::istringstream iss(str);
    T value;
    iss >> value;
    return value;
}
```

### 7. Stream State
```cpp
// Check stream state
if (std::cin.good()) {
    // All good
}
if (std::cin.eof()) {
    // End of file
}
if (std::cin.fail()) {
    // Logical error
}
if (std::cin.bad()) {
    // Read/write error
}

// Boolean conversion
if (std::cin) {
    // Stream is good
}

// Clear errors
std::cin.clear();

// Reset stream state
std::cin.clear();
std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
```

### 8. Custom Manipulators
```cpp
// Simple manipulator
std::ostream& bold(std::ostream& os) {
    return os << "\033[1m";
}

std::ostream& reset(std::ostream& os) {
    return os << "\033[0m";
}

// Usage
std::cout << bold << "Bold text" << reset << '\n';

// Parameterized manipulator
struct color {
    int code;
    color(int c) : code(c) {}
};

std::ostream& operator<<(std::ostream& os, const color& c) {
    return os << "\033[" << c.code << "m";
}

// Usage
std::cout << color(31) << "Red text" << color(0) << '\n';
```

### 9. Format Library (C++20)
```cpp
#include <format>

// Basic formatting
std::string s = std::format("Hello, {}!", "World");

// Positional arguments
std::string s2 = std::format("{0} {1} {0}", "Hello", "World");
// "Hello World Hello"

// Named arguments (C++20)
std::string s3 = std::format("Name: {}, Age: {}", "Alice", 25);

// Format specifications
std::string s4 = std::format("{:10}", "Text");      // Width
std::string s5 = std::format("{:<10}", "Left");     // Left align
std::string s6 = std::format("{:>10}", "Right");    // Right align
std::string s7 = std::format("{:^10}", "Center");   // Center

// Numbers
std::string s8 = std::format("{:.2f}", 3.14159);    // 3.14
std::string s9 = std::format("{:x}", 255);          // ff
std::string s10 = std::format("{:b}", 255);         // 11111111

// Direct output
std::print("Hello, {}!\n", "World");
```

## Best Practices
1. **Use '\n' instead of endl** for better performance
2. **Validate user input** before using
3. **Clear error flags** after input errors
4. **Use string streams** for complex parsing
5. **Prefer format library** (C++20) for formatting
6. **Use cerr for errors**, cout for normal output
7. **Flush output explicitly** when needed
8. **Handle stream errors** appropriately
9. **Use manipulators** for consistent formatting
10. **Test with invalid input** to ensure robustness

## Common Patterns
```cpp
// 1. Menu input
int getMenuChoice() {
    std::cout << "1. Option 1\n";
    std::cout << "2. Option 2\n";
    std::cout << "3. Exit\n";
    std::cout << "Choice: ";
    return getIntegerInRange(1, 3);
}

// 2. Table output
void printTable(const std::vector<Person>& people) {
    std::cout << std::left
              << std::setw(20) << "Name"
              << std::setw(10) << "Age"
              << std::setw(15) << "City" << '\n';
    std::cout << std::string(45, '-') << '\n';

    for (const auto& p : people) {
        std::cout << std::setw(20) << p.name
                  << std::setw(10) << p.age
                  << std::setw(15) << p.city << '\n';
    }
}

// 3. Progress indicator
void showProgress(int current, int total) {
    int percent = (current * 100) / total;
    std::cout << '\r' << percent << "% complete" << std::flush;
}
```

## Resources and References
- [cppreference.com - iostream](https://en.cppreference.com/w/cpp/io)
- [cppreference.com - format](https://en.cppreference.com/w/cpp/utility/format)
- [C++ Core Guidelines - I/O](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rio-iostream)

## Navigation
- **Previous Program**: [119 - Error Handling](../119_error_handling/README.md)
- **Next Program**: [121 - Classes and Objects](../121_classes_objects/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
