# Program 199: Debugging Tools

## Description
Explores debugging tools and techniques for C++ development, including GDB, Valgrind, AddressSanitizer, and other debugging utilities.

## Learning Objectives
- Use GDB for interactive debugging
- Detect memory errors with Valgrind
- Apply sanitizers (ASAN, UBSAN, TSAN)
- Debug with core dumps
- Use static analysis tools

## Features
- GDB usage and commands
- Valgrind memory debugging
- AddressSanitizer (ASAN)
- ThreadSanitizer (TSAN)
- UndefinedBehaviorSanitizer (UBSAN)
- Static analysis (cppcheck, clang-tidy)

## Compilation
```bash
# Debug build
g++ -std=c++17 -g main.cpp -o debugging_tools

# With sanitizers
g++ -std=c++17 -g -fsanitize=address,undefined main.cpp -o debugging_tools

# Run with Valgrind
valgrind --leak-check=full ./debugging_tools

# GDB
gdb ./debugging_tools
```

## Key Concepts
```cpp
// Common GDB commands:
// break main - Set breakpoint
// run - Start program
// next - Step over
// step - Step into
// print var - Print variable
// backtrace - Show call stack

// Compile with -g for debug symbols
// Use -fsanitize=address for memory errors
// Use -fsanitize=thread for race conditions
// Use -fsanitize=undefined for UB
```

## Best Practices
1. Enable debug symbols (-g)
2. Use sanitizers during development
3. Run Valgrind regularly
4. Learn GDB commands
5. Use static analysis tools
6. Test with different sanitizers

## Navigation
- **Previous**: [198 - Benchmarking](/home/user/DevOps-prj500/101-200_CPP/198_benchmarking/README.md)
- **Next**: [200 - Build Systems](/home/user/DevOps-prj500/101-200_CPP/200_build_systems/README.md)
