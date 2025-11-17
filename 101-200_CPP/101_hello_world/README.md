# Program 101: Hello World - Basic C++ Program Structure

## Description
A foundational C++ program that introduces the basic structure of a C++ application, including the main function, standard output, and fundamental programming concepts. This program demonstrates the essential components every C++ program needs and serves as the starting point for learning C++ programming.

## Learning Objectives
- Understand the basic structure and syntax of a C++ program
- Learn about the `main()` function as the program entry point
- Master standard input/output using `std::cout`, `std::cerr`, and `std::clog`
- Comprehend the difference between `std::endl` and `\n` for newlines
- Understand return values, exit codes, and their significance
- Learn about different comment styles (single-line and multi-line)
- Gain familiarity with the compilation process

## Features
- Classic "Hello, World!" demonstration
- Comprehensive output stream demonstrations (`std::cout`, `std::cerr`, `std::clog`)
- Multiple data type output examples
- `std::string` usage and operations
- Function declaration and definition examples
- Program structure and compilation process explanations
- Exit code demonstrations

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/101_hello_world
g++ -std=c++20 -Wall -Wextra -o hello_world main.cpp
```

### Execution
```bash
./hello_world
```

### Using CMake (Alternative)
```bash
mkdir build && cd build
cmake ..
make
./hello_world
```

## Key Concepts

### 1. Basic Program Structure
```cpp
#include <iostream>  // Preprocessor directive

int main() {         // Entry point
    std::cout << "Hello, World!" << std::endl;
    return 0;        // Exit code
}
```

### 2. Standard Output Streams
```cpp
// Standard output (buffered)
std::cout << "Standard output" << std::endl;

// Standard error (unbuffered)
std::cerr << "Error message" << std::endl;

// Standard log (buffered)
std::clog << "Log message" << std::endl;
```

### 3. std::endl vs '\n'
```cpp
std::cout << "Using std::endl (flushes buffer)" << std::endl;
std::cout << "Using \\n (no flush)\n";
```
- `std::endl`: Inserts newline AND flushes the buffer (slower but ensures immediate output)
- `'\n'`: Just adds a newline character (faster, buffer flushed later)

### 4. Outputting Different Data Types
```cpp
std::cout << "Integer: " << 42 << std::endl;
std::cout << "Float: " << 3.14159 << std::endl;
std::cout << "Character: " << 'A' << std::endl;
std::cout << "Boolean: " << true << std::endl;
std::cout << "String: " << "C++ is awesome!" << std::endl;
```

### 5. Comments
```cpp
// Single-line comment

/*
 * Multi-line comment
 * Can span multiple lines
 */
```

## Best Practices
1. Use meaningful variable and function names
2. Comment your code appropriately (explain WHY, not WHAT)
3. Follow consistent indentation (2 or 4 spaces, or tabs)
4. Use `std::endl` when you need to flush the buffer
5. Use `'\n'` for better performance when buffer flushing is not needed
6. Always return 0 from `main()` to indicate successful execution
7. Include necessary header files at the top
8. Organize code into functions for better modularity
9. Use C++ features over C equivalents (e.g., `std::cout` over `printf`)
10. Enable compiler warnings (`-Wall -Wextra`) during compilation

## Compilation Flags Explained
- `-std=c++20`: Use C++20 standard (modern C++ features)
- `-Wall`: Enable all common warnings
- `-Wextra`: Enable extra warnings beyond `-Wall`
- `-o`: Specify output file name

## Compilation Process
1. **Preprocessing**: Handle `#include`, `#define`, and other preprocessor directives
2. **Compilation**: Convert source code to assembly/object code
3. **Linking**: Link object files and libraries together
4. **Executable**: Create final runnable program

## Exit Codes
- `return 0` or `EXIT_SUCCESS`: Program completed successfully
- `return 1` or `EXIT_FAILURE`: General error occurred
- Other non-zero values: Specific error codes (application-defined)

## Resources and References
- [cppreference.com - main function](https://en.cppreference.com/w/cpp/language/main_function)
- [cppreference.com - Input/output library](https://en.cppreference.com/w/cpp/io)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [ISO C++ Official Website](https://isocpp.org/)
- [Learn C++](https://www.learncpp.com/)

## Navigation
- **Previous Program**: None (This is the first program)
- **Next Program**: [102 - Variables and Data Types](../102_variables_datatypes/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)

## Additional Notes
- Every C++ program must have exactly one `main()` function
- The `main()` function can have two signatures:
  - `int main()`
  - `int main(int argc, char* argv[])` (for command-line arguments)
- C++ is case-sensitive: `Main` ` `main`
- Statements end with semicolons (`;`)
- Blocks are defined with curly braces `{}`
- Indentation is not syntactically significant but crucial for readability
