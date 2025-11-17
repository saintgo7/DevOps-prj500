/*
 * Program 101: Hello World - Basic C++ Program Structure
 *
 * Topics Covered:
 * - Basic program structure and syntax
 * - #include directives and iostream
 * - main() function (entry point)
 * - std::cout for output
 * - std::endl vs '\n' for newlines
 * - Return values and exit codes
 * - Comments (single-line and multi-line)
 * - Compilation process overview
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o hello_world main.cpp
 *
 * Execution:
 * ./hello_world
 */

#include <iostream>  // For std::cout, std::cerr, std::endl
#include <string>    // For std::string

// Single-line comment: This is a function declaration
void demonstrateBasicOutput();
void demonstrateDifferentOutputs();
void demonstrateReturnCodes();

/*
 * Multi-line comment:
 * The main() function is the entry point of every C++ program.
 * It must return an int value (exit code).
 * - Return 0 indicates successful execution
 * - Non-zero values indicate errors
 */
int main() {
    // ============================================================
    // 1. The Classic "Hello, World!"
    // ============================================================

    std::cout << "Hello, World!" << std::endl;

    // ============================================================
    // 2. Understanding std::cout
    // ============================================================

    // std::cout is the standard output stream
    // << is the stream insertion operator
    // It can be chained for multiple outputs
    std::cout << "Welcome to " << "C++ Programming!" << std::endl;

    // ============================================================
    // 3. std::endl vs '\n'
    // ============================================================

    std::cout << "Using std::endl (flushes buffer)" << std::endl;
    std::cout << "Using \\n (no flush)\n";

    // std::endl flushes the output buffer (slower but ensures immediate output)
    // '\n' just adds a newline (faster)

    std::cout << "Multiple\nLines\nUsing\n\\n\n";

    // ============================================================
    // 4. Outputting Different Data Types
    // ============================================================

    std::cout << "\n--- Different Data Types ---\n";

    // Integer
    std::cout << "Integer: " << 42 << std::endl;

    // Floating-point
    std::cout << "Float: " << 3.14159 << std::endl;

    // Character
    std::cout << "Character: " << 'A' << std::endl;

    // Boolean (0 = false, 1 = true by default)
    std::cout << "Boolean (true): " << true << std::endl;
    std::cout << "Boolean (false): " << false << std::endl;

    // String
    std::cout << "String: " << "C++ is awesome!" << std::endl;

    // ============================================================
    // 5. Using std::string
    // ============================================================

    std::cout << "\n--- Using std::string ---\n";

    std::string message = "Hello from std::string!";
    std::cout << message << std::endl;

    // ============================================================
    // 6. Demonstrating Function Calls
    // ============================================================

    std::cout << "\n--- Function Demonstrations ---\n";

    demonstrateBasicOutput();
    demonstrateDifferentOutputs();

    // ============================================================
    // 7. Program Structure Overview
    // ============================================================

    std::cout << "\n--- Program Structure ---\n";
    std::cout << "1. Preprocessor directives (#include)" << std::endl;
    std::cout << "2. Function declarations (prototypes)" << std::endl;
    std::cout << "3. main() function (program entry point)" << std::endl;
    std::cout << "4. Function definitions (implementation)" << std::endl;

    // ============================================================
    // 8. Compilation Process
    // ============================================================

    std::cout << "\n--- Compilation Process ---\n";
    std::cout << "1. Preprocessing: Handle #include, #define, etc." << std::endl;
    std::cout << "2. Compilation: Convert source to assembly/object code" << std::endl;
    std::cout << "3. Linking: Link object files and libraries" << std::endl;
    std::cout << "4. Executable: Create final runnable program" << std::endl;

    // ============================================================
    // 9. Exit Code
    // ============================================================

    std::cout << "\n--- Program Exit ---\n";
    std::cout << "Returning 0 from main() indicates success" << std::endl;

    // Return 0 to indicate successful execution
    return 0;  // EXIT_SUCCESS (defined in <cstdlib>)
}

/**
 * Function: demonstrateBasicOutput
 * Purpose: Show basic output functionality
 */
void demonstrateBasicOutput() {
    std::cout << "This is output from a separate function!" << std::endl;
    std::cout << "Functions help organize code into reusable blocks" << std::endl;
}

/**
 * Function: demonstrateDifferentOutputs
 * Purpose: Show different output streams
 */
void demonstrateDifferentOutputs() {
    std::cout << "\n--- Different Output Streams ---\n";

    // Standard output (buffered)
    std::cout << "std::cout - Standard output stream" << std::endl;

    // Standard error (unbuffered, typically shown in red in terminals)
    std::cerr << "std::cerr - Standard error stream" << std::endl;

    // Standard log (buffered)
    std::clog << "std::clog - Standard logging stream" << std::endl;
}

/**
 * Function: demonstrateReturnCodes
 * Purpose: Explain return codes (not called in main, just for reference)
 *
 * Note: In a real program, you would use different return codes for different errors:
 * - return 0;   // Success
 * - return 1;   // General error
 * - return 2;   // Misuse of command
 * - return 127; // Command not found
 * etc.
 */
void demonstrateReturnCodes() {
    std::cout << "Exit codes: 0 = success, non-zero = error" << std::endl;
}

/*
 * Additional Notes:
 *
 * 1. Every C++ program must have exactly one main() function
 * 2. The main() function can have two signatures:
 *    - int main()
 *    - int main(int argc, char* argv[])
 * 3. C++ is case-sensitive: "Main" != "main"
 * 4. Statements end with semicolons (;)
 * 5. Blocks are defined with curly braces {}
 * 6. Indentation is not syntactically significant but is important for readability
 *
 * Compilation Flags Explained:
 * -std=c++20  : Use C++20 standard
 * -Wall       : Enable all warnings
 * -Wextra     : Enable extra warnings
 * -o          : Specify output file name
 *
 * Best Practices:
 * 1. Use meaningful variable and function names
 * 2. Comment your code appropriately
 * 3. Follow consistent indentation (2 or 4 spaces)
 * 4. Use std::endl when you need to flush the buffer
 * 5. Use '\n' for better performance when buffer flushing is not needed
 */
