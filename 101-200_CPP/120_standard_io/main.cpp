/*
 * Program 120: Standard Input/Output
 *
 * Topics Covered:
 * - std::cin (standard input)
 * - std::cout (standard output)
 * - std::cerr (standard error)
 * - std::clog (standard logging)
 * - Stream manipulators (setw, setprecision, etc.)
 * - Formatting output
 * - Input validation
 * - Stream states
 * - getline and input methods
 * - Custom I/O for user types
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o standard_io main.cpp
 */

#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <limits>

void demonstrateBasicIO();
void demonstrateInputMethods();
void demonstrateOutputFormatting();
void demonstrateStreamManipulators();
void demonstrateStreamStates();
void demonstrateCustomIO();

int main() {
    std::cout << "=== C++ Standard Input/Output ===" << std::endl << std::endl;

    demonstrateBasicIO();
    demonstrateInputMethods();
    demonstrateOutputFormatting();
    demonstrateStreamManipulators();
    demonstrateStreamStates();
    demonstrateCustomIO();

    return 0;
}

void demonstrateBasicIO() {
    std::cout << "--- Basic I/O ---" << std::endl;

    // std::cout - standard output
    std::cout << "This is standard output" << std::endl;

    // std::cerr - standard error (unbuffered)
    std::cerr << "This is standard error" << std::endl;

    // std::clog - standard log (buffered)
    std::clog << "This is standard log" << std::endl;

    // Chaining output
    int x = 10;
    double y = 3.14;
    std::cout << "x = " << x << ", y = " << y << std::endl;

    // Different data types
    std::cout << "\n--- Output Different Types ---" << std::endl;
    std::cout << "Integer: " << 42 << std::endl;
    std::cout << "Float: " << 3.14f << std::endl;
    std::cout << "Double: " << 2.71828 << std::endl;
    std::cout << "Character: " << 'A' << std::endl;
    std::cout << "String: " << "Hello, C++" << std::endl;
    std::cout << "Boolean: " << true << " (1)" << std::endl;
    std::cout << "Boolean: " << std::boolalpha << true << " (true)" << std::endl;

    // std::cin - standard input (simulated with predefined values)
    std::cout << "\n--- Input (simulated) ---" << std::endl;
    // In real interaction:
    // int number;
    // std::cout << "Enter a number: ";
    // std::cin >> number;
    // std::cout << "You entered: " << number << std::endl;

    std::cout << std::endl;
}

void demonstrateInputMethods() {
    std::cout << "--- Input Methods ---" << std::endl;

    // Simulating input with stringstream
    std::istringstream input("42 3.14 Hello");

    // Reading different types
    int num;
    double d;
    std::string str;

    input >> num >> d >> str;
    std::cout << "Read: " << num << ", " << d << ", " << str << std::endl;

    // getline for full line
    std::istringstream lineInput("Hello World from C++");
    std::string line;
    std::getline(lineInput, line);
    std::cout << "getline: " << line << std::endl;

    // get for single character
    std::istringstream charInput("ABC");
    char ch;
    charInput.get(ch);
    std::cout << "get: " << ch << std::endl;

    // Reading until delimiter
    std::istringstream delimInput("apple,banana,cherry");
    std::string token;
    std::getline(delimInput, token, ',');
    std::cout << "Read until comma: " << token << std::endl;

    // Input validation example
    std::cout << "\n--- Input Validation ---" << std::endl;
    std::istringstream validInput("not_a_number");
    int value;

    if (validInput >> value) {
        std::cout << "Valid input: " << value << std::endl;
    } else {
        std::cout << "Invalid input" << std::endl;
        validInput.clear();  // Clear error state
    }

    // Ignore remaining input
    std::istringstream ignoreInput("123 456 789");
    int first;
    ignoreInput >> first;
    ignoreInput.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::cout << "Read first number: " << first << " (ignored rest)" << std::endl;

    std::cout << std::endl;
}

void demonstrateOutputFormatting() {
    std::cout << "--- Output Formatting ---" << std::endl;

    // Width and fill
    std::cout << "Without formatting:" << std::endl;
    std::cout << 1 << std::endl;
    std::cout << 12 << std::endl;
    std::cout << 123 << std::endl;

    std::cout << "\nWith width(5):" << std::endl;
    std::cout << std::setw(5) << 1 << std::endl;
    std::cout << std::setw(5) << 12 << std::endl;
    std::cout << std::setw(5) << 123 << std::endl;

    std::cout << "\nWith width and fill:" << std::endl;
    std::cout << std::setfill('0') << std::setw(5) << 1 << std::endl;
    std::cout << std::setfill('0') << std::setw(5) << 12 << std::endl;
    std::cout << std::setfill('0') << std::setw(5) << 123 << std::endl;
    std::cout << std::setfill(' ');  // Reset to space

    // Precision for floating point
    double pi = 3.141592653589793;
    std::cout << "\nPrecision:" << std::endl;
    std::cout << "Default: " << pi << std::endl;
    std::cout << std::setprecision(3) << "Precision 3: " << pi << std::endl;
    std::cout << std::setprecision(10) << "Precision 10: " << pi << std::endl;

    // Fixed and scientific notation
    std::cout << "\nNotation:" << std::endl;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Fixed: " << pi << std::endl;
    std::cout << std::scientific;
    std::cout << "Scientific: " << pi << std::endl;
    std::cout << std::defaultfloat;  // Reset

    // Alignment
    std::cout << "\nAlignment:" << std::endl;
    std::cout << std::left << std::setw(10) << "Left" << "|" << std::endl;
    std::cout << std::right << std::setw(10) << "Right" << "|" << std::endl;
    std::cout << std::internal << std::setw(10) << -123 << "|" << std::endl;

    std::cout << std::endl;
}

void demonstrateStreamManipulators() {
    std::cout << "--- Stream Manipulators ---" << std::endl;

    // Boolean formatting
    bool flag = true;
    std::cout << "boolalpha: " << std::boolalpha << flag << std::endl;
    std::cout << "noboolalpha: " << std::noboolalpha << flag << std::endl;

    // Number bases
    int number = 255;
    std::cout << "\nNumber bases:" << std::endl;
    std::cout << "Decimal: " << std::dec << number << std::endl;
    std::cout << "Hexadecimal: " << std::hex << number << std::endl;
    std::cout << "Octal: " << std::oct << number << std::endl;
    std::cout << std::dec;  // Reset to decimal

    // Show base
    std::cout << "\nWith showbase:" << std::endl;
    std::cout << std::showbase;
    std::cout << "Hex: " << std::hex << number << std::endl;
    std::cout << "Oct: " << std::oct << number << std::endl;
    std::cout << std::noshowbase << std::dec;

    // Show positive sign
    std::cout << "\nShow positive:" << std::endl;
    std::cout << std::showpos << 42 << std::endl;
    std::cout << std::noshowpos;

    // Uppercase for hex/scientific
    std::cout << "\nUppercase:" << std::endl;
    std::cout << std::uppercase << std::hex << 0xabcd << std::endl;
    std::cout << std::scientific << 1.23e10 << std::endl;
    std::cout << std::nouppercase << std::defaultfloat << std::dec;

    // Show decimal point
    std::cout << "\nShow point:" << std::endl;
    std::cout << std::showpoint << 1.0 << std::endl;
    std::cout << std::noshowpoint;

    // Unit buffering
    std::cout << "\nUnitbuf (flush after each output):" << std::endl;
    std::cout << std::unitbuf << "Flushed " << "immediately" << std::endl;
    std::cout << std::nounitbuf;

    std::cout << std::endl;
}

void demonstrateStreamStates() {
    std::cout << "--- Stream States ---" << std::endl;

    std::istringstream stream("123");

    // Stream state flags
    std::cout << "good(): " << stream.good() << std::endl;
    std::cout << "eof(): " << stream.eof() << std::endl;
    std::cout << "fail(): " << stream.fail() << std::endl;
    std::cout << "bad(): " << stream.bad() << std::endl;

    // Read data
    int value;
    stream >> value;
    std::cout << "\nAfter reading: " << value << std::endl;

    // Try to read more (EOF)
    stream >> value;
    std::cout << "After reading past end:" << std::endl;
    std::cout << "good(): " << stream.good() << std::endl;
    std::cout << "eof(): " << stream.eof() << std::endl;
    std::cout << "fail(): " << stream.fail() << std::endl;

    // Clear error state
    stream.clear();
    std::cout << "\nAfter clear():" << std::endl;
    std::cout << "good(): " << stream.good() << std::endl;
    std::cout << "fail(): " << stream.fail() << std::endl;

    // Failed input
    std::istringstream badStream("not_a_number");
    badStream >> value;
    std::cout << "\nAfter failed input:" << std::endl;
    std::cout << "fail(): " << badStream.fail() << std::endl;

    std::cout << std::endl;
}

class Point {
public:
    int x, y;

    Point(int x = 0, int y = 0) : x(x), y(y) {}

    // Output operator
    friend std::ostream& operator<<(std::ostream& os, const Point& p) {
        os << "(" << p.x << ", " << p.y << ")";
        return os;
    }

    // Input operator
    friend std::istream& operator>>(std::istream& is, Point& p) {
        char lparen, comma, rparen;
        is >> lparen >> p.x >> comma >> p.y >> rparen;
        return is;
    }
};

void demonstrateCustomIO() {
    std::cout << "--- Custom I/O for User Types ---" << std::endl;

    Point p1(10, 20);
    std::cout << "Point p1: " << p1 << std::endl;

    Point p2(5, 15);
    std::cout << "Point p2: " << p2 << std::endl;

    // Simulated input
    std::istringstream input("(30, 40)");
    Point p3;
    input >> p3;
    std::cout << "Read point: " << p3 << std::endl;

    // Using with streams
    std::ostringstream oss;
    oss << "Points: " << p1 << " and " << p2;
    std::cout << "\nStringstream: " << oss.str() << std::endl;

    std::cout << std::endl;
}

/*
 * Standard I/O Summary:
 *
 * Stream Objects:
 * - std::cin   - Standard input (buffered)
 * - std::cout  - Standard output (buffered)
 * - std::cerr  - Standard error (unbuffered)
 * - std::clog  - Standard log (buffered)
 *
 * Input Methods:
 * - operator>> - Formatted input
 * - getline()  - Read line
 * - get()      - Read character
 * - read()     - Read raw data
 * - ignore()   - Skip input
 *
 * Output Methods:
 * - operator<< - Formatted output
 * - put()      - Write character
 * - write()    - Write raw data
 * - flush()    - Flush buffer
 *
 * Manipulators:
 * - setw()         - Set field width
 * - setprecision() - Set decimal precision
 * - setfill()      - Set fill character
 * - left/right     - Alignment
 * - fixed/scientific - Float notation
 * - boolalpha      - Boolean as text
 * - hex/oct/dec    - Number base
 *
 * Stream States:
 * - good()  - No errors
 * - eof()   - End of file
 * - fail()  - Logical error
 * - bad()   - Read/write error
 * - clear() - Clear error flags
 *
 * Best Practices:
 * 1. Always validate input
 * 2. Check stream state after I/O
 * 3. Use getline for full lines
 * 4. Clear error states when recovering
 * 5. Use manipulators for formatting
 * 6. Implement << and >> for custom types
 * 7. Prefer std::string over C-strings
 * 8. Use std::cerr for error messages
 * 9. Flush output when needed (std::endl or std::flush)
 * 10. Handle I/O exceptions appropriately
 */
